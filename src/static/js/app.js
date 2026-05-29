import { fetchFilters, fetchRecommendations } from "./api.js";
import { PreferencesForm } from "./components/PreferencesForm.js";
import { RecommendationCard } from "./components/RecommendationCard.js";
import { FallbackAlert } from "./components/FallbackAlert.js";
import { Loader } from "./components/Loader.js";
import { EmptyState } from "./components/EmptyState.js";

document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize state components
    const emptyState = new EmptyState("empty-state");
    const loader = new Loader("loading-state");
    const fallbackAlert = new FallbackAlert("fallback-alert", "fallback-reason");
    const recsContainer = document.getElementById("recommendations-container");
    
    // 2. Initialize input controller
    const preferencesForm = new PreferencesForm("preferences-form", {
        onSubmit: async (payload) => {
            // Apply visual transitions to loading states
            emptyState.hide();
            recsContainer.classList.add("hidden");
            loader.show();
            fallbackAlert.hide();
            preferencesForm.setLoading(true);
            
            try {
                const data = await fetchRecommendations(payload);
                renderRecommendations(data);
            } catch (error) {
                console.error("API Error:", error);
                loader.hide();
                emptyState.show(
                    "Search Request Failed",
                    "We encountered an error while processing your request. Please ensure the backend server is running and try again."
                );
            } finally {
                preferencesForm.setLoading(false);
            }
        }
    });
    
    // 3. Load dynamic options on mount
    async function initFilters() {
        try {
            const data = await fetchFilters();
            preferencesForm.populateFilters(data.locations, data.cuisines);
        } catch (error) {
            console.error("Initialization Error:", error);
            preferencesForm.setError();
        }
    }
    
    // 4. Render results layout
    function renderRecommendations(data) {
        loader.hide();
        const recs = data.recommendations;
        
        // Show fallback alert if backend running on database-only fallback
        if (data.fallback_mode) {
            fallbackAlert.show(data.fallback_reason, "AI Mode Offline");
        } else if (data.query_relaxed) {
            fallbackAlert.show(`No exact matches found. To give you recommendations, we relaxed your ${data.query_relaxed} preference.`, "Search Criteria Relaxed");
        } else {
            fallbackAlert.hide();
        }
        
        // Check for empty dataset recommendations list
        if (!recs || recs.length === 0) {
            emptyState.show(
                "No Restaurants Found",
                "We couldn't find any matching restaurants in that area, even after relaxing search bounds. Try adjusting your preferences or selecting a different location."
            );
            return;
        }
        
        // Flush previous results
        recsContainer.innerHTML = "";
        
        // Dynamically build and mount components
        recs.forEach(rec => {
            const card = RecommendationCard.render(rec);
            recsContainer.appendChild(card);
        });
        
        // Reveal list container
        recsContainer.classList.remove("hidden");
    }

    // Initialize dropdown elements on load
    initFilters();
});
