### Consciousness Tab Failure Report (2025-09-14)

Problem
- The Insights page consciousness tab showed fallback messaging and Graphmaster-related errors.
- Root cause: `/api/insights/consciousness/evolution` computed `evolution_level` locally and sometimes diverged from `/consciousness/state` and realtime. This caused provenance mismatches and triggered fallback handling in the UI.

Fix
- Implemented SSOT module `backend/utils/evolution_level_service.py` with `get_current_level` and `normalize_timeline`.
- Refactored `backend/routers/insights.py` evolution endpoint to:
  - Normalize timelines and milestones via `normalize_timeline`.
  - Resolve `current_state.evolution_level` via `get_current_level` and expose stored/computed provenance.

Verification
- Endpoints now align: `/consciousness/state`, `/api/insights/consciousness/realtime`, `/api/insights/consciousness/evolution`.
- UI should no longer show fallback for the consciousness tab when backend is healthy.

Next Steps
- Tune freshness window via `EVOLUTION_FRESHNESS_SECONDS` if real-time drift is observed.

