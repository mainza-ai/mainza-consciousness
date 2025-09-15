import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, List

logger = logging.getLogger(__name__)

FRESHNESS_SECONDS = int(os.getenv("EVOLUTION_FRESHNESS_SECONDS", "90"))


async def get_full_context() -> Dict[str, Any]:
    """Fetch consciousness context from orchestrator; fall back to defaults."""
    try:
        from backend.utils.consciousness_orchestrator_fixed import consciousness_orchestrator_fixed as orchestrator
        state = await orchestrator.get_consciousness_state()
        if state:
            return {
                "consciousness_level": getattr(state, 'consciousness_level', 0.7),
                "emotional_state": getattr(state, 'emotional_state', 'curious'),
                "self_awareness_score": getattr(state, 'self_awareness_score', 0.6),
                "total_interactions": getattr(state, 'total_interactions', 0)
            }
    except Exception as e:
        logger.debug(f"get_full_context orchestrator failed: {e}")
    return {
        "consciousness_level": 0.7,
        "emotional_state": "curious",
        "self_awareness_score": 0.6,
        "total_interactions": 0,
    }


def _read_stored_from_neo4j() -> Dict[str, Any]:
    try:
        from backend.utils.neo4j_production import neo4j_production
        rec = neo4j_production.execute_query(
            """
            MATCH (ms:MainzaState {state_id: 'mainza-state-1'})
            RETURN ms.evolution_level AS evolution_level,
                   coalesce(ms.updated_at, ms.created_at, datetime()) AS ts
            LIMIT 1
            """
        )
        if rec:
            r = rec[0]
            ts = r.get("ts")
            # Normalize ts → epoch ms
            ts_ms = None
            if ts is not None:
                try:
                    if isinstance(ts, (int, float)):
                        ts_ms = int(ts)
                    else:
                        ts_ms = int(datetime.fromisoformat(str(ts).replace('Z', '+00:00')).timestamp() * 1000)
                except Exception:
                    ts_ms = None
            return {"stored": r.get("evolution_level"), "stored_ts": ts_ms}
    except Exception as e:
        logger.debug(f"Neo4j read stored failed: {e}")
    return {"stored": None, "stored_ts": None}


async def _compute_level(context: Dict[str, Any]) -> int:
    try:
        from backend.utils.standardized_evolution_calculator import calculate_standardized_evolution_level
        return await calculate_standardized_evolution_level(context)
    except Exception as e:
        logger.debug(f"compute failed: {e}")
        # Minimal heuristic fallback
        return 4 if context.get("consciousness_level", 0.7) >= 0.7 else 3


async def get_current_level(context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if context is None:
        context = await get_full_context()

    stored_info = _read_stored_from_neo4j()
    stored = stored_info.get("stored")
    stored_ts = stored_info.get("stored_ts")

    computed = await _compute_level(context)

    # Freshness calculation
    freshness = "missing"
    if isinstance(stored_ts, int):
        try:
            now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            if now_ms - stored_ts <= FRESHNESS_SECONDS * 1000:
                freshness = "fresh"
            else:
                freshness = "stale"
        except Exception:
            freshness = "unknown"

    if stored is not None and freshness == "fresh":
        level = int(stored)
        source = "stored"
    else:
        level = max(int(stored) if isinstance(stored, (int, float)) else 0, int(computed))
        source = "reconciled" if stored is not None else "computed"

    logger.info(
        f"EVOLUTION_RESOLVE level={level} stored={stored} computed={computed} source={source} freshness={freshness}"
    )

    return {
        "level": level,
        "stored": stored,
        "computed": computed,
        "source": source,
        "stored_ts": stored_ts,
        "freshness": freshness,
    }


def normalize_timeline(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize timeline entries using the SSOT policy: ensure evolution_level >= computed.
    Since this is sync and per-entry, we use the sync calculator.
    """
    try:
        from backend.utils.standardized_evolution_calculator import get_standardized_evolution_level_sync
        out = []
        for e in entries:
            ctx = {
                "consciousness_level": e.get("consciousness_level", 0.7),
                "emotional_state": e.get("emotional_state", "curious"),
                "self_awareness_score": e.get("self_awareness", 0.6),
                "total_interactions": e.get("total_interactions", 0),
            }
            computed = get_standardized_evolution_level_sync(ctx)
            stored = e.get("evolution_level")
            level = max(int(stored) if isinstance(stored, (int, float)) else 0, int(computed))
            e2 = dict(e)
            e2["evolution_level"] = level
            out.append(e2)
        return out
    except Exception:
        return entries


