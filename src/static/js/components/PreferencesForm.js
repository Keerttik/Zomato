/**
 * PreferencesForm component manages form controls, slider states, dynamic dropdown options,
 * and handles user submission events.
 */
export class PreferencesForm {
    /**
     * @param {string} formId - ID of the form element.
     * @param {Object} config - Configuration callbacks.
     * @param {Function} config.onSubmit - Callback function triggered on form submission.
     */
    constructor(formId, config = {}) {
        this.form = document.getElementById(formId);
        this.locationSelect = this.form.querySelector("#location");
        this.cuisineSelect = this.form.querySelector("#cuisine");
        this.ratingInput = this.form.querySelector("#min-rating");
        this.ratingVal = this.form.querySelector("#rating-val");
        this.submitBtn = this.form.querySelector("#submit-btn");
        
        // Budget slider elements
        this.minBudgetInput = this.form.querySelector("#min-budget");
        this.maxBudgetInput = this.form.querySelector("#max-budget");
        this.minBudgetVal = this.form.querySelector("#min-budget-val");
        this.maxBudgetVal = this.form.querySelector("#max-budget-val");
        this.budgetRangeText = this.form.querySelector("#budget-range-text");
        this.budgetTrack = this.form.querySelector("#budget-track");

        this.onSubmitCallback = config.onSubmit || (() => {});
        this._initEvents();
    }

    /**
     * Helper to format values as currency (₹)
     * @private
     */
    _formatCurrency(val, isMax = false) {
        if (!isMax && val <= 0) {
            return "₹1";
        }
        if (isMax && val >= 2000) {
            return "₹2,000+";
        }
        return `₹${Number(val).toLocaleString('en-IN')}`;
    }

    /**
     * Updates the highlighted portion of the budget slider track.
     * @private
     */
    _updateBudgetTrack() {
        const minVal = parseInt(this.minBudgetInput.value);
        const maxVal = parseInt(this.maxBudgetInput.value);
        
        // Calculate percentage positions
        const percent1 = (minVal / 2000) * 100;
        const percent2 = (maxVal / 2000) * 100;
        
        // Fill blue color between the two thumbs
        this.budgetTrack.style.background = `linear-gradient(to right, rgba(255, 255, 255, 0.08) ${percent1}%, #3b82f6 ${percent1}%, #3b82f6 ${percent2}%, rgba(255, 255, 255, 0.08) ${percent2}%)`;
    }

    /**
     * Updates bubble pills and centered text range strings.
     * @private
     */
    _updateBudgetLabels() {
        const minVal = parseInt(this.minBudgetInput.value);
        const maxVal = parseInt(this.maxBudgetInput.value);
        
        const minStr = this._formatCurrency(minVal);
        const maxStr = this._formatCurrency(maxVal, true);
        
        this.minBudgetVal.value = minStr;
        this.maxBudgetVal.value = maxStr;
        this.budgetRangeText.textContent = `${minStr}-${maxStr}`;
    }

    /**
     * Initializes events for the form controls.
     * @private
     */
    _initEvents() {
        // Real-time rating slider update
        this.ratingInput.addEventListener("input", (e) => {
            this.ratingVal.textContent = Number(e.target.value).toFixed(1);
        });

        // Initialize budget slider states on load
        this._updateBudgetTrack();
        this._updateBudgetLabels();

        // Budget handles collision detection and track updates
        const handleBudgetChange = (isMinTrigger) => {
            let minVal = parseInt(this.minBudgetInput.value);
            let maxVal = parseInt(this.maxBudgetInput.value);
            
            const minGap = 50; // Keep a small gap between handles

            if (isMinTrigger) {
                if (minVal >= maxVal - minGap) {
                    this.minBudgetInput.value = maxVal - minGap;
                }
            } else {
                if (maxVal <= minVal + minGap) {
                    this.maxBudgetInput.value = minVal + minGap;
                }
            }
            
            this._updateBudgetTrack();
            this._updateBudgetLabels();
        };

        this.minBudgetInput.addEventListener("input", () => handleBudgetChange(true));
        this.maxBudgetInput.addEventListener("input", () => handleBudgetChange(false));

        // Form focus handler for budget input bubbles (show raw numeric editing values)
        this.minBudgetVal.addEventListener("focus", () => {
            let val = parseInt(this.minBudgetInput.value);
            this.minBudgetVal.value = val <= 0 ? 1 : val;
        });

        this.maxBudgetVal.addEventListener("focus", () => {
            let val = parseInt(this.maxBudgetInput.value);
            this.maxBudgetVal.value = val;
        });

        // Form commit handlers on input field blur or enter keys
        const commitMinTypedValue = () => {
            let val = parseInt(this.minBudgetVal.value.replace(/[^0-9]/g, ''));
            if (isNaN(val)) {
                val = parseInt(this.minBudgetInput.value);
            }
            let maxVal = parseInt(this.maxBudgetInput.value);
            const minGap = 50;
            
            if (val < 0) val = 0;
            if (val >= maxVal - minGap) {
                val = maxVal - minGap;
            }
            
            this.minBudgetInput.value = val;
            this._updateBudgetTrack();
            this._updateBudgetLabels();
        };

        const commitMaxTypedValue = () => {
            let val = parseInt(this.maxBudgetVal.value.replace(/[^0-9]/g, ''));
            if (isNaN(val)) {
                val = parseInt(this.maxBudgetInput.value);
            }
            let minVal = parseInt(this.minBudgetInput.value);
            const minGap = 50;
            
            if (val > 2000) val = 2000;
            if (val <= minVal + minGap) {
                val = minVal + minGap;
            }
            
            this.maxBudgetInput.value = val;
            this._updateBudgetTrack();
            this._updateBudgetLabels();
        };

        this.minBudgetVal.addEventListener("blur", commitMinTypedValue);
        this.minBudgetVal.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                commitMinTypedValue();
                this.minBudgetVal.blur();
            }
        });

        this.maxBudgetVal.addEventListener("blur", commitMaxTypedValue);
        this.maxBudgetVal.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                commitMaxTypedValue();
                this.maxBudgetVal.blur();
            }
        });

        // Submit listener interceptor
        this.form.addEventListener("submit", (e) => {
            e.preventDefault();
            
            const location = this.locationSelect.value;
            const cuisine = this.cuisineSelect.value || null;
            
            const minBudget = Math.max(1, parseInt(this.minBudgetInput.value));
            const maxBudget = parseInt(this.maxBudgetInput.value);
            
            const minRating = parseFloat(this.ratingInput.value);
            const additionalPrefs = this.form.querySelector("#additional-prefs").value.trim() || null;
            
            this.onSubmitCallback({
                location,
                cuisine,
                min_budget: minBudget,
                max_budget: maxBudget,
                min_rating: minRating,
                additional_preferences: additionalPrefs
            });
        });
    }

    /**
     * Populates location and cuisine options inside the dropdown selectors.
     * @param {string[]} locations - List of unique location strings.
     * @param {string[]} cuisines - List of unique cuisine strings.
     */
    populateFilters(locations, cuisines) {
        // Location dropdown
        this.locationSelect.innerHTML = '<option value="" disabled selected>Select neighborhood...</option>';
        locations.forEach(loc => {
            const opt = document.createElement("option");
            opt.value = loc;
            opt.textContent = loc;
            this.locationSelect.appendChild(opt);
        });

        // Cuisine dropdown
        this.cuisineSelect.innerHTML = '<option value="">Any Cuisine</option>';
        cuisines.forEach(cuis => {
            const opt = document.createElement("option");
            opt.value = cuis;
            opt.textContent = cuis;
            this.cuisineSelect.appendChild(opt);
        });
    }

    /**
     * Toggles submit button states to show interactive loading signals.
     * @param {boolean} isLoading - Loading status.
     */
    setLoading(isLoading) {
        if (isLoading) {
            this.submitBtn.disabled = true;
            this.submitBtn.querySelector("span").textContent = "Curating list...";
            this.submitBtn.querySelector("i").className = "fa-solid fa-spinner fa-spin";
        } else {
            this.submitBtn.disabled = false;
            this.submitBtn.querySelector("span").textContent = "Get Recommendations";
            this.submitBtn.querySelector("i").className = "fa-solid fa-chevron-right";
        }
    }

    /**
     * Shows error state on select fields in case API config or server is offline.
     */
    setError() {
        this.locationSelect.innerHTML = '<option value="" disabled>Error loading options</option>';
    }
}
