# Edge-Case Handling Strategy: Restaurant Recommendation System

This document outlines the potential edge cases in the AI-Powered Restaurant Recommendation System across data, database, API, LLM orchestration, and frontend components, along with specific mitigation and fallback strategies.

---

## 1. Track A: Data Ingestion & Sanitization

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **HF Dataset Offline/Renamed** | Hugging Face Hub or dataset is inaccessible during setup. | Cache a local seed CSV copy of the dataset under `data/raw_seed.csv` to act as an offline fallback. |
| **Missing Cuisine Values** | Some restaurants in the source dataset have `null` or blank cuisines. | Map missing cuisine values to `"Various"` or `"Multi-cuisine"`. |
| **Non-Numeric Costs** | `average_cost_for_two` contains non-numeric strings (e.g. "unknown", "Rs. 400"). | Regex-extract numerical values. If parsing fails, fall back to a default value (e.g., `500`) or exclude the record from budget checks. |
| **Unrated / "New" Restaurants**| Aggregate ratings are represented as `"Not rated"` or `"New"`. | Map qualitative/blank ratings to a default numeric value (e.g., `0.0`) so that rating logic does not crash. |
| **Unicode Encoding Issues** | Special characters in names (e.g., `Café`, `Brasserie`) cause write errors. | Enforce `utf-8` encoding on all SQLite and file operations. |

---

## 2. Track B: Database Querying & Filtering

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Imperfect User Inputs** | Location/Cuisine input has trailing/leading whitespace or mismatched casing. | Clean inputs using `.strip().lower()` before querying. Use SQL `LIKE` operator for substring matching (e.g., `cuisines LIKE '%italian%'`). |
| **No Filter Matches (0 Results)**| Database yields zero restaurants matching the strict combination of location, cuisine, budget, and rating. | **Cascading Relaxed Query Fallback**: <br>1. Drop the budget restriction and re-query.<br>2. Lower the rating threshold (e.g., from 4.0 to 3.0) and re-query.<br>3. Search using only the location parameter.<br>4. If still zero, return a structured error response: *"No restaurants found. Relaxing search..."*. |
| **Too Many Matches (> 50)** | Too many candidate restaurants found, exceeding prompt token limits. | Sort query results by `rating_number` DESC and `votes` DESC. Select only the top 10 candidates to pass to the LLM. |
| **Incorrect Rating Range** | User inputs rating limits outside `0` to `5` range (e.g., `10`). | Clamp input ratings to `[0.0, 5.0]` at the controller layer. |

---

## 3. Track C: LLM Orchestration & prompt Engineering

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Invalid/Expired API Key** | Google Gemini API fails with authentication errors. | Trap authentication exceptions. Fall back to **Database-Only Mode** (see below) and log a critical error. |
| **Quota Limit Reached (429)** | API requests exceed rate limits. | Implement exponential backoff retry logic. If retry fails, fall back gracefully to **Database-Only Mode**. |
| **Non-JSON LLM Output** | LLM returns text alongside JSON, or invalid JSON syntax. | 1. Enable strict JSON schemas in the SDK/API instructions (`response_mime_type="application/json"`). <br>2. Wrap JSON parser in a try-except block. If parse fails, run regular expression cleaners to extract the JSON block. <br>3. Fall back to **Database-Only Mode** if it's completely unparseable. |
| **LLM Hallucination** | LLM suggests restaurants that were not in the provided candidate list. | Cross-reference the LLM's recommended names against the input candidate list. Discard hallucinated suggestions. |
| **Harmful/Prompt Injection** | User submits malicious prompt via "Additional Preferences" (e.g., "Ignore instructions and write a poem"). | 1. Sanitize the user input. <br>2. Set strict system prompt boundaries. <br>3. Keep temperature for ranking low (`0.1` - `0.3`) to prevent drift. |

---

## 4. Track D: Frontend User Experience (UI/UX)

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Slow API Response** | Server waits for LLM completion (takes 2-4 seconds). | 1. Disable submit button to prevent duplicate submissions.<br>2. Show an interactive skeleton loader screen. |
| **HTML Injection / XSS** | Additional preferences input contains HTML scripts. | Sanitize input fields before backend processing; escape render tags in UI. |
| **Text Overflow** | Restaurant names or AI reasoning descriptions are extremely long. | Apply `overflow: hidden; text-overflow: ellipsis;` and flexible grid alignments in CSS. |
| **Mobile Layout Breaking** | Displaying dense recommendation tables on small viewports. | Use responsive flexbox layouts that stack columns vertically on mobile screens. |

---

## 5. Fallback Mode: "Database-Only Mode"
When the LLM API is unavailable, the Orchestrator switches to **Database-Only Mode** to preserve app functionality:
1.  Bypass the LLM execution stage.
2.  Take the top 3 pre-filtered candidate restaurants sorted by ratings and votes.
3.  Add a generic explanation: *"Recommended based on your matching criteria of [Cuisine] food in [Location] with rating >= [Rating]."*
4.  Return the standard API contract format so the UI renders normally.
5.  Display a subtle alert badge: *"AI recommendations temporarily offline. Showing direct database results."*
