# Design System Specification: The Academic Atelier

## 1. Overview & Creative North Star
This design system moves away from the "transactional" feel of standard marketplaces and adopts the persona of **"The Academic Atelier."** In this vision, we treat education as a premium, curated experience rather than a commodity. 

The aesthetic is rooted in **Editorial Sophistication**. We reject the rigid, boxed-in layouts of traditional software in favor of intentional asymmetry, overlapping elements, and high-contrast typography scales. By utilizing generous whitespace and tonal depth, we create an environment that feels authoritative yet breathing—instilling trust through professional restraint.

**Core Principles:**
*   **Intentional Asymmetry:** Break the grid with offset imagery and staggered card placements to create a dynamic, "designed" feel.
*   **Depth through Tone:** Eliminate lines. Use the interplay of surface shades to define boundaries.
*   **Authority via Typography:** Use massive display scales against condensed labels to create a hierarchy that feels like a high-end journal.

---

## 2. Colors & Surface Architecture
The color palette uses deep, intellectual blues and growth-oriented greens, layered to provide a sense of physical space.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning or containment. 
Boundaries must be defined through:
1.  **Background Shifts:** Place a `surface_container_low` section against a `surface` background.
2.  **Tonal Transitions:** Use `surface_container_highest` for interactive areas to naturally "lift" them from the page.

### Surface Hierarchy & Nesting
Treat the UI as a series of nested physical layers. 
*   **The Base:** `surface` (#faf8ff) for the main canvas.
*   **The Content Block:** `surface_container_low` (#f3f3fe) for large sectioning.
*   **The Hero Card:** `surface_container_lowest` (#ffffff) to provide the highest contrast and "pop" against the background.
*   **The Interactive Layer:** `surface_container_high` (#e7e7f3) for hovered states or secondary information clusters.

### Signature Textures & Glassmorphism
*   **Glass Elements:** For floating navigation or filter bars, use `surface` at 70% opacity with a `24px` backdrop-blur.
*   **Tonal Gradients:** For primary Call-to-Actions (CTAs), use a subtle linear gradient from `primary` (#004ac6) to `primary_container` (#2563eb). This provides a "soul" and depth that a flat fill cannot achieve.

---

## 3. Typography
We use **Inter** as our sole typeface, relying on extreme scale and weight contrast to drive the editorial narrative.

*   **Display (lg/md):** Reserved for hero messaging. Set with `-0.02em` letter-spacing. This is your "Editorial Voice."
*   **Headline (sm/md):** Used for section starts. These should often be paired with a `label-md` "kicker" text above them in `secondary` (#006c49) for a magazine-style look.
*   **Body (lg):** The primary reading weight. Ensure a line height of `1.6` to maintain the "clean and modern" promise.
*   **Label (md/sm):** Always uppercase with `0.05em` letter-spacing when used for categories or metadata. This adds a layer of professional "polish."

---

## 4. Elevation & Depth
Elevation is achieved through **Tonal Layering**, not structural shadows.

*   **The Layering Principle:** To lift a tutor's profile card, do not reach for a shadow first. Place the card (`surface_container_lowest`) on a `surface_container_low` background. The color delta provides the "lift."
*   **Ambient Shadows:** When a floating effect is required (e.g., a modal or a floating CTA), use a shadow with a `40px` blur and `4%` opacity, using the `on_surface` color as the base. It should feel like a soft glow of light, not a dark smudge.
*   **The "Ghost Border" Fallback:** For accessibility in dark mode or high-density grids, use the `outline_variant` token at **15% opacity**. This "Ghost Border" provides a hint of a edge without cluttering the visual field.

---

## 5. Components

### Buttons
*   **Primary:** High-rounded (`full`), using the signature gradient. `on_primary` text.
*   **Secondary:** `surface_container_highest` background with `primary` text. No border.
*   **Tertiary:** Text-only with `primary` color, using an underline that only appears on hover.

### Cards (Tutor Profiles / Course Listings)
*   **Rule:** Forbid divider lines. 
*   **Structure:** Use `xl` (1.5rem) corner radius. Use `surface_container_lowest` for the card body. 
*   **Asymmetry:** Position the tutor’s image so it slightly breaks the top boundary of the card or is offset to the left, creating a custom, non-templated appearance.

### Input Fields
*   **Styling:** Use `surface_container_low` for the field fill. 
*   **State:** On focus, transition to `surface_container_lowest` and apply a 2px "Ghost Border" using the `primary` color at 30% opacity.

### Selection Chips
*   **Unselected:** `surface_container_high`.
*   **Selected:** `secondary` (#006c49) with `on_secondary` (#ffffff) text. Use `md` (0.75rem) roundedness.

### Professional Spotlight (Custom Component)
A large-format component for featured tutors. Use a two-column layout:
*   **Left:** A high-quality, cut-out (PNG) image of the tutor overlapping a `primary_fixed` decorative circle.
*   **Right:** `headline-lg` text with a `body-lg` bio, utilizing `surface_container_low` as a background "plate" that only covers 80% of the section.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use white space as a functional tool. If a section feels crowded, increase the vertical padding (use 128px or 160px for desktop sections).
*   **Do** use `secondary` (#006c49) sparingly for "Success," "Verified," or "Growth" indicators to maintain its impact.
*   **Do** ensure high-quality, lifestyle photography. Images should have natural light and "academic" environments (libraries, clean workspaces).

### Don't:
*   **Don't** use 100% opaque lines to separate content. It breaks the premium editorial feel.
*   **Don't** use standard "drop shadows" with high opacity.
*   **Don't** center-align everything. Use left-aligned typography for a more professional, structured look.
*   **Don't** use pure black for text. Always use `on_surface` (#191b23) to keep the contrast soft and readable.