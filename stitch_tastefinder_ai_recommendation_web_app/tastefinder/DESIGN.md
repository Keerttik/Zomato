---
name: TasteFinder
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#5b403f'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#7c5800'
  on-secondary: '#ffffff'
  secondary-container: '#feb700'
  on-secondary-container: '#6b4b00'
  tertiary: '#4648d4'
  on-tertiary: '#ffffff'
  tertiary-container: '#6063ee'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdea8'
  secondary-fixed-dim: '#ffba20'
  on-secondary-fixed: '#271900'
  on-secondary-fixed-variant: '#5e4200'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  display-lg:
    fontFamily: DM Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: DM Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: DM Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: DM Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 64px
---

## Brand & Style
The design system is engineered to feel like a premium culinary concierge—polished, warm, and deeply rooted in the vibrant, tech-forward food culture of Bangalore. It avoids the clinical coldness of typical SaaS products in favor of an "appetizing" interface that prioritizes high-quality food photography and clear, AI-driven insights.

The aesthetic follows a **Modern Corporate** direction with **Tactile** influences. It utilizes soft backgrounds to reduce eye strain during long discovery sessions, paired with high-impact primary accents that mirror the urgency and excitement of dining. The goal is to evoke a sense of reliability and local expertise, moving away from generic templates to a custom, curated experience that feels as sophisticated as the city's top-tier establishments.

## Colors
This design system employs a warm, high-contrast palette optimized for food-focused content:

- **Primary (#E23744):** A vibrant coral-red used for primary actions, brand moments, and critical feedback. It provides the energy necessary for a discovery app.
- **Secondary (#FFB800):** A warm amber specifically reserved for ratings, reviews, and "must-try" highlights.
- **Tertiary (#6366F1):** A sophisticated indigo-purple used exclusively for AI-generated insights and "Why we recommend this" badges to separate logic from metadata.
- **Neutral (#1A1A1A):** A deep charcoal for primary text, ensuring maximum legibility against the off-white backgrounds.
- **Surface:** Uses `#F8F8F8` (Off-white) for the main canvas and `#F0F0F0` (Warm Gray) for secondary containers to create a soft, multi-layered depth without the harshness of pure white.

## Typography
The typography strategy balances geometric personality with systematic utility:

- **Headlines:** DM Sans is used for its modern, friendly apertures and high-impact weights. It anchors the restaurant names and section titles, providing a distinct brand voice.
- **Body & Metadata:** Inter is utilized for all functional text, including menus, AI explanations, and distance markers. Its neutral character ensures that long-form AI reasoning remains highly readable.
- **Hierarchy:** Use `display-lg` for curated collections, `headline-md` for restaurant card titles, and `label-md` for category tags and status indicators.

## Layout & Spacing
The design system utilizes a **8px linear scale** for consistent rhythm across all components.

- **Grid Model:** A 12-column fluid grid for desktop and a 4-column fluid grid for mobile.
- **Gutter & Margins:** Mobile layouts use 16px margins to maximize screen real estate for food photography. Tablet and Desktop transition to 24px and 64px respectively.
- **Containment:** Related elements (like a restaurant name and its rating) should use `sm` (8px) spacing, while distinct sections should use `xl` (32px) to provide sufficient visual breathing room.

## Elevation & Depth
Depth is achieved through **Tonal Layering** supplemented by **Ambient Shadows**. This creates a hierarchy that feels physical but clean.

- **Level 0 (Base):** Off-white background (#F8F8F8).
- **Level 1 (Cards):** Pure white surface (#FFFFFF) with a soft, 12% opacity shadow: `0px 4px 20px rgba(0, 0, 0, 0.08)`. Use this for restaurant listings.
- **Level 2 (Active/Floating):** Raised elements like floating action buttons (FABs) or active AI badges use a tighter, more saturated shadow to indicate interactivity: `0px 8px 24px rgba(226, 55, 68, 0.15)`.
- **Interaction:** On hover or tap, cards should subtly lift (negative Y-offset) rather than darken, maintaining the light, airy feel of the system.

## Shapes
The shape language is defined by a consistent **Rounded (0.5rem / 8px base)** logic that scales to **12px - 16px** for larger containers.

- **Standard Elements (8px):** Input fields, small buttons, and notification toasts.
- **Card Elements (16px):** Restaurant cards and image containers. This generous radius softens the UI and feels more approachable.
- **Pill (Full):** Used exclusively for category chips, rating badges, and "AI Verified" labels to distinguish them from actionable buttons.

## Components
Consistent implementation of these components ensures a unified user experience:

- **Primary Buttons:** High-contrast coral background with white text. Use 16px internal padding and 12px corner radius. Bold weight DM Sans.
- **Discovery Cards:** 16px corner radius. Images should occupy the top 60% of the card with a subtle inner 1px border (#000000 0.05) to define the edge against white backgrounds.
- **AI Recommendation Badges:** Use the Tertiary indigo (#6366F1) with 10% opacity for the background and 100% opacity for the text. Include a small "sparkle" icon.
- **Input Fields:** Soft warm-gray background (#F0F0F0) with no border in resting state; transitions to a 2px Primary coral border on focus.
- **Map Pins:** Custom teardrop shape using the Primary coral for restaurants and Tertiary indigo for the "User Location" or "AI Pick" highlights.
- **Rating Chips:** Secondary amber (#FFB800) backgrounds with charcoal text, always featuring a star icon for instant recognition.