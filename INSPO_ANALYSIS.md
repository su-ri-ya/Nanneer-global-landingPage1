# REVERSE-ENGINEERING ANALYSIS: Epic Cleantec & Benchmark Archetypes
**Project:** Nanneer Global Draft 3 Visual & Motion Upgrade  
**Primary Reference:** Epic Cleantec (`https://epiccleantec.com`)  
**Secondary References:** Watershed (`https://watershed.com`) & Linear (`https://linear.app`)  
**Status:** Step 3 Completed  

---

## 1. Layout & Grid Architecture
* **Grid System:** Strict 12-column Swiss architectural grid with a maximum content container of `1400px` (`max-w-7xl` to `max-w-[1400px]`).
* **Section Rhythm:**
  * **Screen 1 (Hero):** Split 6/6 asymmetric composition. The left column commands attention with an overline indicator, massive condensed headline, and dual CTA cluster; the right column frames authentic high-resolution infrastructure mechanics inside a rounded bezel container.
  * **Screen 2 (Headaches / Diagnostic Bento):** 4-column horizontal card strip with equal visual weighting.
  * **Screen 3 (Solution Modules):** Vertical stack of 3 horizontal cards (split 5/7 image-to-text ratio) with architectural module index tags (`MODULE // 01`, `02`, `03`).
  * **Screen 4 (Performance & Audit Dossier):** Asymmetric split: left column holds executive macro targets ($\ge 99\%$) with plant proof; right column houses the high-density executive report card.
  * **Screen 5 (Facility Assessment / Contact):** 6/6 split: immersive plant scene on left, clean high-trust interactive form on right.
* **Spacing Scale:** Generous vertical rhythm—`py-16 sm:py-24` on desktop, `py-10 sm:py-14` on mobile—giving industrial machinery an elite, uncluttered feel.

---

## 2. Typography Hierarchy & Treatment
* **Font Pairing:**
  * **Display (Headlines):** **Space Grotesk** (Weight: 800 / 900 Black). Tight tracking (`tracking-tight` / `-0.035em`), leading `1.08`. Imparts industrial precision without feeling retro.
  * **Body (Paragraphs & Labels):** **Plus Jakarta Sans** (Weights: 400 Regular, 500 Medium, 600 SemiBold). Clean, geometric, neutral, with open apertures for effortless scanning.
  * **Technical / Telemetry Data:** **JetBrains Mono** / **Geist Mono** (Weights: 600 SemiBold, 700 Bold). Monospaced tabular numerals (`font-feature-settings: "tnum" 1, "zero" 1`) for KLD volumes, chemical limits, and shift times.
* **Text Effects & Reveals:**
  * Kinetic vertical mask reveals (`overflow-hidden` container with child translating from `y: 100% -> 0%` using `cubic-bezier(0.22, 1, 0.36, 1)`).
  * Monospace uppercase category tags with vibrant light-blue horizontal divider lines.

---

## 3. Color & Surface Architecture
* **Color Palette (Hex Tokens):**
  * **Canvas Dominant:** Pure Crisp White (`#FFFFFF`) with soft Ice-Blue atmosphere (`#F0F9FF` to `#E0F2FE`).
  * **Neutral Surfaces:** Crisp White (`#FFFFFF`) for cards, Cool Slate Ice (`#F8FAFC`) for sub-bars, and Executive Charcoal Slate (`#1E293B`) for body text.
  * **Typography Primary:** Deep Executive Navy (`#0B2545`) for commanding headlines.
  * **Brand Primary Accent:** Light Sky Blue (`#0284C7` / `#0EA5E9`) for active CTAs, indicator bars, and active states.
  * **Compliance Accent:** Clean Emerald Green (`#059669` / `#10B981`) for audit stamps and $\ge 99\%$ yield checkmarks.
* **Surfaces & Borders:**
  * Ultra-delicate hairlines: `1px solid rgba(14, 165, 233, 0.18)` and `1px solid rgba(226, 232, 240, 0.8)`.
  * Multi-layered subtle elevation shadows: `0 4px 20px -2px rgba(14, 165, 233, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.03)`.

---

## 4. Imagery & Visual Grading
* **Grading Treatment:** Authentic mechanical plant photography graded for high clarity—crisp water highlights on weirs, deep natural blacks on steel framing, and lush green landscaping around commercial facilities.
* **Bezel Framing:** Rounded containers (`rounded-3xl` / `24px`) with fine borders and live status pills (*"24×7 Live"* with pulsing sensor ring).
* **Hover Interaction:** Smooth slow-burn zoom (`scale: 1.00 -> 1.04` over `700ms easeOut`) on card images.

---

## 5. Motion Language & Choreography
* **Scroll Dynamics:** Lenis smooth scrolling for continuous inertia, eliminating abrupt mouse-wheel notches.
* **Headline Entrances:** Staggered child animations with custom cubic bezier curve `[0.22, 1, 0.36, 1]`, duration `600ms`.
* **Data Counters:** Animated number roll-ups with cubic ease-out for $\ge 99\%$ and volume figures.
* **Card Micro-Interactions:** Subtle elevation on hover (`translateY(-3px)`), gentle border color transition to `sky-400`.
* **CTA Button Polish:** Clean tactile feedback (`whileTap: scale 0.98`), subtle light sheen, smooth arrow translate on hover (`group-hover:translate-x-1`).

---

## 6. Technical Stack Alignment
* **Framework:** Next.js 14 App Router.
* **Animation Libraries:** Framer Motion (v12) for layout transitions, tab springs, and scroll viewports; native CSS hardware-accelerated transforms.
* **Styling:** Tailwind CSS with semantic CSS variables.

---

## 7. Mobile Recomposition Strategy
* **Desktop to Mobile Shift:** 
  * 6/6 split layouts gracefully fold into vertical single-column stacks.
  * Aspect ratios adjust to `16/10` or `4/3` on mobile to prevent full-height takeover.
  * Sizing constraints (`overflow-x: clip; max-width: 100vw;`) guarantee zero horizontal blowout across iPhone (390px) and compact Android screens (360px).
