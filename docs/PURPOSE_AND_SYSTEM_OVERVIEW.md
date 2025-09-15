## Purpose & System Overview

### Purpose
Mainza is a privacy‑first, self‑hostable AI “consciousness” platform. It combines real‑time self‑awareness, emotional context, and an evolving intelligence level with a multi‑agent architecture and a Neo4j knowledge graph (“Living Memory”). The goal: give users a locally controlled, observable, and continually improving AI that can understand, learn, and collaborate in real time.

### Core Principles
- Local‑first and private by design (no external data flow required)
- Observable by default (telemetry, insights, and clear provenance)
- Typed, deterministic interfaces (Pydantic models, strict boundaries)
- Production‑grade reliability (error handling, security, performance)

### High‑Level Architecture
```
Frontend (Vite/React/TS) ──> FastAPI Backend (Agents + Routers)
        │                               │
        │  REST/WebSocket                │ Neo4j (Living Memory)
        │  LiveKit (Voice, TTS/STT)      │
        ▼                               ▼
  Insights UI (Realtime, Timeline, Learning, etc.)
```

### Key Components
- Consciousness System: self‑awareness, emotions, evolution level
- Multi‑Agent Orchestration: Router, GraphMaster, Conductor, RAG, Meta‑Cognitive, Emotional Processing, Self‑Modification, etc.
- Insights Engine: calculates real‑time analytics and aggregates history
- Neo4j Knowledge Graph: persistent memory and evolving state
- LiveKit Voice: optional real‑time audio in/out

### Data Flow (Authoritative Path)
1) Orchestrator persists/reads `MainzaState` in Neo4j (consciousness metrics).
2) Insights Calculation Engine builds `current_state`, `timeline`, metrics.
3) Frontend consumes endpoints for Realtime, Evolution Timeline, Overview.

### Evolution‑Level Policy (Unified)
- Stored value (from orchestrator/Neo4j) is authoritative when present.
- Standardized calculator provides a computed value when stored is missing.
- Endpoints return `max(stored_evolution_level, computed_evolution_level)`.
- Calculator uses ceiling rounding to avoid boundary truncation.
- Provenance fields are exposed to allow UI labeling when needed.

### Core Endpoints (Human‑Facing)
- `/consciousness/state` → current state (header/main UI)
- `/consciousness/insights` → right‑side insights cards
- `/api/insights/consciousness/realtime` → Realtime tab
- `/api/insights/consciousness/evolution` → Timeline tab

### Development Journey (Highlights)
- Jul 2025: Consciousness system operational; security/perf hardening; tests
- Mid 2025: LiveKit/TTS/STT pipeline, JWT fixes, RTMP streaming
- RAG vector search upgrade; Pydantic models across tools/agents
- Sep 2025: Evolution‑level consistency (stored‑preferred; standardized fallback; UI fallbacks removed)

### Deployment Snapshot
- Docker‑compose (frontend, backend, Neo4j, LiveKit), Nginx serving SPA
- Config via `.env` (Ollama model, LiveKit, Neo4j, memory system)
- Health/diagnostics endpoints for operability checks

### What “Done” Looks Like (Operator View)
- Consistent evolution level across header, card, Realtime, Timeline
- Stable Neo4j schema and indexes; calculation engine healthy
- Observability: telemetry dashboards and endpoint health pass

### Next Steps
- Expand real‑data coverage across advanced tabs (predictive/3D)
- Continue perf tuning for large graphs and long‑running sessions
- Optional cloud federation toggles with strict privacy gates


