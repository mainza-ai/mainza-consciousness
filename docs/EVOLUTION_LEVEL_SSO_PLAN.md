## Evolution Level Single-Source-of-Truth (SSOT) Plan

### Problem
Different endpoints compute/choose evolution level independently, causing 5 vs 6 mismatches. Timing, freshness, and rounding diverge across paths (state vs insights realtime/evolution vs card).

### Goal
One authoritative resolver layer that all endpoints call. Same input policy, same rounding, same provenance. Zero drift across UI.

### Module: `backend/utils/evolution_level_service.py`
- `async get_current_level(context?: dict) -> { level:int, stored:int|None, computed:int, source:str, stored_ts:int|None, freshness:'fresh'|'stale'|'missing' }`
- `get_full_context() -> {consciousness_level, emotional_state, self_awareness_score, total_interactions}`
- `normalize_timeline(entries:list) -> list` (replaces <=1 or <computed with computed)

### Resolution Policy
1) Read stored from orchestrator/Neo4j with timestamp.
2) Compute via standardized calculator (ceiling) from full context.
3) Freshness window (default 90s):
   - If stored present and fresh → use stored (source=stored).
   - Else → use max(stored, computed) (source=reconciled). No writes in phase 1.
4) Always return both stored and computed; include provenance.

### Integration
- `/consciousness/state`: replace local logic with service.get_current_level()
- Insights realtime/evolution: use service for current_state and service.normalize_timeline()
- `/consciousness/insights` card: use service for text

### Config & Ops
- `EVOLUTION_FRESHNESS_SECONDS` (default 90)
- Optional cache TTL = freshness
- Logs one structured line per resolution: {stored, computed, level, source}

### Rollout
1) Implement read‑only service (no writes)
2) Refactor four endpoints to call service
3) Docker verify: all show same level + provenance


