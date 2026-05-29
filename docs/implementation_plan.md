# Phase-Wise Implementation Plan: AI-Powered Restaurant Recommendation System

This implementation plan divides the project into 8 chronological phases (Phases 0-7) across 5 engineering tracks: **Foundation**, **Data**, **Core**, **AI**, and **Delivery**.

---

## Plan Overview (Timeline)

```mermaid
gantt
    title Implementation Phases Timeline (Indicative)
    dateFormat  YYYY-MM-DD
    axisFormat  %m-%d
    
    section Foundation
    Phase 0: Project Setup :active, p0, 2026-05-17, 1d
    
    section Data
    Phase 1: Data Ingestion :active, p1, 2026-05-18, 2d
    
    section Core
    Phase 2: Models and Repository :active, p2, 2026-05-20, 2d
    Phase 3: Filter Service :active, p3, 2026-05-21, 2d
    
    section AI
    Phase 4: LLM Integration :active, p4, 2026-05-23, 2d
    Phase 5: Orchestrator :active, p5, 2026-05-24, 2d
    
    section Delivery
    Phase 6: Presentation Layer :active, p6, 2026-05-25, 3d
    Phase 7: Hardening and Ship :active, p7, 2026-05-28, 2d
```

---

## Tracks & Phases

### Track A: Foundation
#### Phase 0: Project Setup (2026-05-17)
*   **Goal**: Configure project directories, initialize virtual environment, and install base packages.
*   **Tasks**:
    *   Initialize folders: `src/`, `data/`, `docs/`, `src/static/`.
    *   Configure Python `.venv` and create `requirements.txt` containing dependencies (`fastapi`, `uvicorn`, `requests`, `groq`, `python-dotenv`).
    *   Create base config loader (`src/config.py`) to manage settings and API keys.

---

### Track B: Data
#### Phase 1: Data Ingestion (2026-05-18 to 2026-05-20)
*   **Goal**: Secure and clean dataset from Hugging Face.
*   **Tasks**:
    *   Write `src/ingest.py` script to fetch Zomato restaurant data from [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation).
    *   Standardize city/locality strings, convert rating values to float, clean currency formats, and handle null average costs.
    *   Export cleaned output to a staging JSON/CSV.

---

### Track C: Core
#### Phase 2: Models and Repository (2026-05-20 to 2026-05-22)
*   **Goal**: Establish data schema and persistent database setup.
*   **Tasks**:
    *   Create SQLite schema layout for `restaurants` table in `src/db/models.py`.
    *   Create DB utility repository (`src/db/repository.py`) to handle database connections, insertions, and basic retrieval operations.
    *   Implement migration task in `src/ingest.py` to populate SQLite from Phase 1 clean staging file.

#### Phase 3: Filter Service (2026-05-21 to 2026-05-23)
*   **Goal**: Build database filter services and lookup routes.
*   **Tasks**:
    *   Develop structured SQL filter functions queryable by location, cuisine matching, rating thresholds, and mapped budgets (Low/Medium/High).
    *   Create API endpoint `/api/filters` to supply front-end options (all available cities & cuisines).
    *   Verify queries yield correct and capped candidate lists.

---

### Track D: AI
#### Phase 4: LLM Integration (2026-05-23 to 2026-05-25)
*   **Goal**: Connect to Groq API, configure prompts, and enforce JSON structures.
*   **Tasks**:
    *   Initialize Groq SDK client wrapper in `src/ai/client.py`.
    *   Draft system instructions forcing JSON mode matching schema contracts.
    *   Develop template engine that renders candidate list context dynamically into LLM prompts.

#### Phase 5: Orchestrator (2026-05-24 to 2026-05-26)
*   **Goal**: Form the backend service layer uniting database filters and AI generation.
*   **Tasks**:
    *   Build Orchestrator controller executing: query database → compile prompt → fetch LLM recommendation → parse response → return to controller.
    *   Implement routing endpoints (`POST /api/recommendations`) to trigger orchestrations.
    *   Design exception handlers for empty results, LLM failure, or JSON syntax issues.

---

### Track E: Delivery
#### Phase 6: Presentation Layer (2026-05-25 to 2026-05-28)
*   **Goal**: Develop the user interface with premium styling.
*   **Tasks**:
    *   Create `src/static/index.html` structure with dynamic forms (input textareas, sliders, selection boxes).
    *   Write CSS stylesheet implementing glassmorphism patterns, deep dark gradients, and responsive typography.
    *   Write JavaScript handlers to consume backend REST endpoints and dynamically compile UI cards with custom AI explanations.

#### Phase 7: Hardening and Ship (2026-05-28 to 2026-05-30)
*   **Goal**: Test end-to-end behavior, tune temperature, and finalize documentation.
*   **Tasks**:
    *   Conduct manual browser verification of layouts and responsiveness.
    *   Optimize prompt parameters (e.g. temperature adjustments for ranking vs explanation tone).
    *   Verify fallback handling for edge cases.
    *   Clean source files and finalize repository README.
