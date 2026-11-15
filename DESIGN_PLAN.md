# DESIGN PLAN: Adapting Awwwards Craft to Nanneer Global
**Project:** Nanneer Global Draft 3 Visual & Motion Upgrade  
**Primary Reference:** Epic Cleantec  
**Secondary References:** Watershed & Linear  
**Status:** Step 4 Completed — Awaiting User Approval Before Code  

---

## 1. The Adapted Design System

### A. Color Architecture (Light Blue & Executive Navy)
* **Canvas Dominant:** `#FFFFFF` (Pristine White) with ambient `#F0F9FF` (Ice Blue gradient) and delicate SVG blueprint grid.
* **Neutral Hierarchy:**
  * Headlines & Wordmarks: `#0B2545` (Executive Deep Navy)
  * Primary Body Text: `#1E293B` (Slate 800)
  * Secondary / Captions: `#475569` (Slate 600)
  * Card Surfaces: `#FFFFFF` (Crisp White) and `#FAFDFE` (Subtle Ice tint)
  * Borders / Dividers: `rgba(14, 165, 233, 0.18)` (Sky hairline) and `rgba(226, 232, 240, 0.8)` (Slate hairline)
* **Primary Brand Accent:** `#0284C7` (Sky 600) & `#0EA5E9` (Sky 500) for active CTAs, indicator bars, radio checks, and key links.
* **Compliance Accent:** `#059669` (Emerald 600) for $\ge 99\%$ yield badges, verified checkmarks, and audit approvals.

### B. Typography System
* **Display Font:** **Space Grotesk** (Weights: 700, 800 Black). Tight tracking (`-0.035em`), leading `1.08`.
* **Body Font:** **Plus Jakarta Sans** (Weights: 400 Regular, 500 Medium, 600 SemiBold). Clean, geometric, neutral.
* **Data & Monospace:** **JetBrains Mono** (`font-mono-data`). Tabular figures for KLD volumes, chemical limits, shift times, and module indices.
* **Fluid Scale (CSS Clamp):**
  * Hero Display: `clamp(2.5rem, 5vw + 1rem, 4.25rem)`
  * Section Headers: `clamp(1.75rem, 3vw + 0.5rem, 2.75rem)`
  * Module Titles: `clamp(1.2rem, 1.5vw + 0.5rem, 1.5rem)`
  * Body Text: `clamp(0.875rem, 0.5vw + 0.75rem, 1rem)`

### C. Motion Tokens
* **Primary Easing:** `cubic-bezier(0.22, 1, 0.36, 1)` (fluid natural decel).
* **Durations:**
  * Micro-interactions (hover, taps, icons): `180ms – 240ms`
  * Card entrances & staggered lists: `500ms – 600ms`
  * Number counters: `1200ms`
  * Image slow zoom: `700ms`

---

## 2. Section-by-Section Implementation Mapping

| Section | Layout Pattern | Visual & Motion Technique | Adapted to Our Site |
| :--- | :--- | :--- | :--- |
| **1. Navbar** | Sticky frosted glass | • Translucent glass on scroll (`bg-white/95 backdrop-blur-md`).<br>• Sky-blue underline indicator on nav hover.<br>• Solid Sky-Blue CTA button with smooth arrow translate. | 100% preservation of all links: *Why Nanneer, Our Approach, Performance, Contact, Concepts HUD, Discuss Your STP*. |
| **2. Hero Section** | Split 6/6 asymmetric grid | • Overline indicator dash with kinetic entry.<br>• Staggered vertical mask reveals for headline: *"Your STP Is Running. But Is It Delivering?"*<br>• Soft organic wave gradient at bottom-left.<br>• Plant photo inside rounded bezel with live sensor pulse pill (*"24×7 Live"*). | Preserves all hero text, dual CTAs (*Discuss Your STP* + *See Sample Report*), and callout with zero changes. |
| **3. Headaches Strip** | 4-column horizontal bento | • Clean white cards with light-blue icon pods (`bg-sky-50 text-sky-600 border-sky-200`).<br>• Subtle hover elevation (`translateY(-3px)`) and border glow.<br>• High-contrast navy titles and slate descriptions. | Preserves all 4 cards: *Water Wastage, Unexpected Incidents, Poor Documentation, Manpower Dependency*. |
| **4. The Solution (3 Modules)** | 3 horizontal stacked cards | • Horizontal split (40% image on left, 60% text/icon on right).<br>• Architectural index tag (`MODULE // 01`, `02`, `03`).<br>• Image slow-burn zoom on card hover.<br>• Centered bottom pill button: *"Discuss Your STP ->"* with sky-blue outline. | Preserves all 3 modules: *24×7 Plant Operations, Maximum Water Recovery, Digital Monitoring & Accountability*. |
| **5. Performance & Targets** | Asymmetric data showcase | • Left column: 3 KPI target cards with animated number roll-ups ($\ge 99\%$) with droplet, gear, and user icons.<br>• Fine print disclaimer in clean slate.<br>• Lower plant photo with *"Clarification Tank Verified"* live status.<br>• Right column: Executive **Monthly STP Performance Report Card** with deep navy header, sub-header metadata, 6 clean data modules, and *"View Sample Performance Report ->"* CTA. | Preserves all report parameters: Water Balance (14,850 / 14,713 / 14,566 KLD), Lab Parameters (pH 7.2, BOD 6, COD 28, TSS 8), Equipment uptime (99.4%), Manpower shifts (100%), and WhatsApp video evidence. |
| **6. Facility Assessment Form** | 6/6 split conversion card | • Left column: STP plant photo with *"STP"* sign badge.<br>• Right column: Clean white form card with vertical sky indicator bar.<br>• Interactive radio pills with smooth selected state (`bg-white border-sky-500 font-bold`).<br>• Submit CTA with arrow animation + Quick Phone & WhatsApp buttons. | Preserves all form options: 4 building types, capacity input, 4 improvement options, submission state. |
| **7. Audit Modal** | High-density dialog | • Deep navy executive header with certified audit badge.<br>• 3 interactive tabs (*Executive Summary, Lab Parameters, Shift Logs*) with smooth spring transitions.<br>• Clean tabular data and deck download action. | Interactive audit modal triggered by both *"See Sample Report"* and *"View Sample Performance Report"*. |
| **8. Footer** | Multi-column directory | • Clean slate-50 background with fine border.<br>• Nanneer Global wordmark, CPCB compliance badge, site navigation, and interactive deck links.<br>• Smooth "Back to top" action. | Preserves all credits, links, and deck downloads. |

---

## 3. Mandatory Hard Rules (Verification Checklist)
- [x] **Zero text changes**: No titles, paragraphs, labels, or numbers will be modified.
- [x] **Section structure locked**: Section order and hierarchy remain 100% faithful to the reference.
- [x] **Color palette locked**: Light Blue as the main color, pristine white canvas, deep navy typography.
- [x] **Technical reliability**: 0 build errors, 0 runtime console errors, 100% responsive across mobile (360px), tablet (768px), and desktop (1440px).

---

## 4. Next Step
Awaiting your approval on **DESIGN_PLAN.md**. Once you confirm, we will begin the code implementation and Quality Loop!
