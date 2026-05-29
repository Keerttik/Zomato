/**
 * FallbackAlert component manages the display of database fallback warnings.
 */
export class FallbackAlert {
    constructor(elementId, reasonId) {
        this.element = document.getElementById(elementId);
        this.reasonElement = document.getElementById(reasonId);
        this.titleElement = this.element.querySelector("h4");
    }

    show(reason = "Groq API error occurred. Showing structured database sorting results instead.", title = "AI Mode Offline") {
        if (this.titleElement) {
            this.titleElement.textContent = title;
        }
        this.reasonElement.textContent = reason;
        this.element.classList.remove("hidden");
    }

    hide() {
        this.element.classList.add("hidden");
    }
}
