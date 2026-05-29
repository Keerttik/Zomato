/**
 * RecommendationCard component compiles and builds the HTML layout for a single restaurant pick.
 */
export class RecommendationCard {
    /**
     * Renders a recommendation item and returns the corresponding DOM element.
     * @param {Object} rec - The recommendation data object.
     * @returns {HTMLElement} The card container element.
     */
    static render(rec) {
        const card = document.createElement("div");
        card.className = "rec-card glass-panel";
        
        const ratingText = rec.rating > 0 
            ? `${Number(rec.rating).toFixed(1)} <i class="fa-solid fa-star"></i>` 
            : "New / Unrated";
            
        card.innerHTML = `
            <div class="card-header">
                <div class="restaurant-title">
                    <div class="rank-badge rank-${rec.rank}">${rec.rank}</div>
                    <div>
                        <h3 class="restaurant-name">${rec.name}</h3>
                        <p class="restaurant-cuisines"><i class="fa-solid fa-bowl-food"></i> ${rec.cuisine}</p>
                    </div>
                </div>
                <div class="meta-badges">
                    <span class="card-rating-badge">${ratingText}</span>
                    <span class="card-cost-badge">${rec.currency}${rec.cost_for_two} for two</span>
                </div>
            </div>
            
            <div class="explanation-box">
                <div class="explanation-title">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    <span>AI Recommendation Rationale</span>
                </div>
                <p class="explanation-text">"${rec.ai_explanation}"</p>
            </div>
        `;
        return card;
    }
}
