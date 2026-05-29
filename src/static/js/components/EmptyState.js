/**
 * EmptyState component manages the empty/initial/no-results dashboard display.
 */
export class EmptyState {
    constructor(elementId) {
        this.element = document.getElementById(elementId);
        this.titleElement = this.element.querySelector("h3");
        this.descElement = this.element.querySelector("p");
    }

    show(title = "Hungry for suggestions?", desc = "Select your location and preferences, and let our AI curate the perfect dining recommendations for you.") {
        this.titleElement.textContent = title;
        this.descElement.textContent = desc;
        this.element.classList.remove("hidden");
    }

    hide() {
        this.element.classList.add("hidden");
    }
}
