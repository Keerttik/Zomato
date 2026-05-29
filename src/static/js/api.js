/**
 * API service client to interact with the backend FastAPI endpoints.
 */

// Support dynamic base URL injection for decoupled deployment (e.g., Vercel + Railway)
const API_BASE_URL = window.ENV?.API_URL || "";

export async function fetchFilters() {
    const response = await fetch(`${API_BASE_URL}/api/filters`);
    if (!response.ok) {
        throw new Error("Failed to fetch filter metadata.");
    }
    return await response.json();
}

export async function fetchRecommendations(payload) {
    const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });
    if (!response.ok) {
        throw new Error("Failed to retrieve recommendations from orchestrator.");
    }
    return await response.json();
}
