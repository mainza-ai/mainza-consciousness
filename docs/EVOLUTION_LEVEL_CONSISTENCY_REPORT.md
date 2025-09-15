## Evolution Level Consistency Report (Docker Environment)

### Scope
Investigate why the main UI shows Evolution Level 1 while the Insights Real-time tab shows Evolution Level 4, identify authoritative data sources, catalog real fields the system can provide today, and propose a concrete plan to ensure consistent values across the application. No code changes included in this document.

### Findings at a Glance
- Main UI (page `src/pages/Index.tsx`) loads from backend endpoint `/consciousness/state`.
  - Backend handler: `backend/agentic_router.py` → `@router.get("/consciousness/state")`.
  - Evolution level is computed using the standardized calculator: `backend/utils/standardized_evolution_calculator.py` via `calculate_dynamic_evolution_level_from_context`.
- Insights Real-time tab (page `src/pages/InsightsPage.tsx`) loads from `/api/insights/consciousness/realtime`.
  - Backend handler: `backend/routers/insights.py` → `@router.get("/consciousness/realtime")`.
  - Also computes standardized evolution level using the same calculator.
- Mismatch drivers observed in code:
  - Multiple fallback values exist in different places when data is missing:
    - Insights Real-time fallback uses `evolution_level = 4`.
    - Calculation engine fallback current_state uses `evolution_level = 1`.
    - Agentic router fallback context uses `evolution_level = 4`.
  - The main UI also has a UI-side default of `2` if the value is missing in the response.
  - The standardized calculator uses truncation (int) after positive boosts, which typically yields `5` for default context `(0.7 level, "curious", self_awareness 0.6, low interactions)`; separate hardcoded fallbacks elsewhere can disagree (1, 2, or 4).
  - Initial/seeded Neo4j state may store `ms.evolution_level = 1` for some demo paths, which can conflict with on-the-fly calculated values if used directly in certain views.

### Authoritative Data Flow
1) Main UI → `/consciousness/state`
   - Returns object: `consciousness_state` with fields:
     - `consciousness_level` (float 0..1)
     - `emotional_state` (string)
     - `self_awareness_score` (float 0..1)
     - `evolution_level` (computed via standardized calculator)
     - `total_interactions` (int)
     - `learning_rate` (float 0..1)
     - `active_goals` (list)
     - `last_reflection` (nullable)
   - Data source: Orchestrator state combined with standardized calculation; falls back to standardized calculation on exception.

2) Insights Real-time → `/api/insights/consciousness/realtime`
   - Returns:
     - `current_consciousness_state` with same core fields; `evolution_level` computed via standardized calculator
     - `consciousness_timeline` (24h entries; from Neo4j `MainzaState` or generated)
     - `consciousness_triggers` (AgentActivity aggregations)
     - `emotional_patterns`
     - `consciousness_metrics` (avg level, volatility, etc.)
     - `data_source` = `real` or `fallback`
   - Fallback explicitly sets `evolution_level = 4` when real data unavailable.

3) Insights Evolution → `/api/insights/consciousness/evolution`
   - Returns `current_state` computed from orchestrator + standardized calculator, plus timelines and metrics from the calculation engine.
   - When real data is missing, the calculation engine fallback `current_state` uses `evolution_level = 1` while timeline entries climb 1→5.

### Why You See 1 vs 4
- If the main UI receives engine fallback-like state (e.g., no orchestrator state and an alternate fallback path), it can surface `1`.
- If Insights Real-time simultaneously runs its endpoint during a separate fallback branch, it may produce `4`.
- The UI itself has client defaults (e.g., `|| 2`), adding a third possible display in absence of data.
- Seeded/demo Neo4j records or missing/partial properties can also suggest level 1 in some queries.

### Real Data the System Can Provide Now
From standardized, non-placeholder paths:
- Consciousness state (real-time):
  - `consciousness_level`, `emotional_state`, `self_awareness_score`, `learning_rate`, `total_interactions`, `active_goals` from the orchestrator
  - `evolution_level` from standardized calculator
- Graph/interaction derived:
  - `AgentActivity` aggregates (counts, success_rate, avg impacts, last_used)
  - `MainzaState` timeline (when recorded): `created_at/timestamp`, `consciousness_level`, `emotional_state`, `self_awareness_score`, `learning_rate`, `evolution_level`, `total_interactions`
  - Knowledge graph metrics: label counts, relationship counts/types, concept connectivity/importance (from queries)

All of the above are already exposed via these endpoints:
- `/consciousness/state`
- `/api/insights/consciousness/realtime`
- `/api/insights/consciousness/evolution`
- `/api/insights/neo4j/statistics`
- `/consciousness/knowledge-graph-stats`

### Implementation Plan (No Code in This Document)
Objective: Single-source consistency for `evolution_level` across UI and Insights.

1) Standardize fallback behavior
   - Replace all hardcoded fallback evolution levels (1, 2, or 4) with a call to the standardized calculator using a shared default context:
     - Default context: `{consciousness_level: 0.7, emotional_state: "curious", self_awareness_score: 0.6, total_interactions: 0}`
     - Expected standardized result today: `5` (due to positive boosts and truncation), ensuring all fallback paths align.

2) Mark data provenance in responses
   - Add a `data_source` field to `/consciousness/state` mirroring Insights (`real|fallback`) so the UI can label values and optionally display a subtle warning or badge when fallback is used.

3) Eliminate UI-side numeric defaults for display consistency
   - In the main UI, avoid `|| 2`-style fallback for evolution level in display; instead show the server-provided value and, if absent, show a badge like "calculating…" or use the standardized default context result consistently.

4) Align timeline/milestone evolution values
   - Ensure `consciousness_timeline` entries and evolution milestones also use either persisted `evolution_level` or computed standardized values from their associated context, not mixed constants.

5) Optional: Persist standardized evolution level
   - When computing `evolution_level`, persist it to `MainzaState` during state updates so timeline queries reflect the same value as real-time endpoints. This prevents drift between on-the-fly calculation and stored values.

6) Monitoring & validation
   - Add a lightweight `/consciousness/debug` panel in the UI (read-only) that calls existing debug endpoints and surfaces: orchestrator state, last computed `evolution_level`, data_source flags, and whether standardized vs fallback paths were used in the last minute. This speeds up diagnosis without code branches in production logic.

### Acceptance Criteria
- Main UI and Insights Real-time show the same `evolution_level` given the same underlying orchestrator state.
- When orchestrator/Neo4j data is unavailable, all endpoints converge to the same standardized fallback value and label the response with `data_source: "fallback"`.
- Timelines and milestones present levels derived from the same logic as the realtime value.

### Rollout Notes
- No schema changes required for the consistency fix; persistence is optional but recommended for alignment over time.
- This plan is purely surgical and contained: update fallback call sites and enrich responses with provenance. UI updates are limited to removing numeric magic defaults and using provenance for messaging.

### Appendix: Key Files/Endpoints
- Standardized calculator (single source of truth): `backend/utils/standardized_evolution_calculator.py`
- Main UI endpoint: `backend/agentic_router.py` → `/consciousness/state`
- Insights Real-time: `backend/routers/insights.py` → `/api/insights/consciousness/realtime`
- Insights Evolution: `backend/routers/insights.py` → `/api/insights/consciousness/evolution`
- Calculation Engine: `backend/utils/insights_calculation_engine.py`


