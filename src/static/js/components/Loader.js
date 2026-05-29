/**
 * Loader component manages the loading screen skeleton state.
 */
export class Loader {
    constructor(elementId) {
        this.element = document.getElementById(elementId);
    }

    show() {
        this.element.classList.remove("hidden");
    }

    hide() {
        this.element.classList.add("hidden");
    }
}
