# Figma Design System & Artboard Import Guide: Nanneer Global

This directory contains the complete production Figma assets for the Nanneer Global landing page.

---

## 📁 Available Figma Assets

1. **`public/Nanneer_Global_Figma_Artboards.svg`**  
   A high-resolution vector artboard document containing **all 4 Desktop Screen Frames (1440 × 900)**, full navigation, component layers, icons, cards, and data tables.
2. **`public/figma_design_tokens.json`**  
   Figma Variables & Tokens Studio compatible token file containing the entire Light Blue color palette, fluid typography scales, border radiuses, and surface specifications.

---

## 🚀 How to Import into Figma (3 Methods)

### Method 1: Instant Drag & Drop (Fastest — 10 Seconds)
1. Open [Figma](https://www.figma.com/) (Desktop App or Web).
2. Create or open any project canvas.
3. Simply **drag and drop** the file `C:\Nanneer global\draft 3\public\Nanneer_Global_Figma_Artboards.svg` directly onto the Figma canvas.
4. Figma will instantly generate 4 editable vector frames:
   * **Frame 1:** Hero & 4 Daily Headaches
   * **Frame 2:** The Solution (3 Modules)
   * **Frame 3:** Performance Targets & Monthly STP Performance Report Card
   * **Frame 4:** Facility Assessment & Contact Form
5. All text, rectangles, vectors, pill buttons, and colors will be native and fully editable!

---

### Method 2: HTML-to-Figma Auto-Layout Import (100% Native Auto-Layout & Real Fonts)
If you want Figma to automatically generate full **Figma Auto-Layout frames** with nested components directly from the running code:
1. Ensure your local server is running: `http://localhost:3000/`.
2. In Figma, install the free community plugin: **"html.to.design"** or **"Builder.io"**.
3. Open the plugin inside Figma and enter your local URL: `http://localhost:3000/`.
4. Click **Import**.
5. The plugin will recreate the entire live website inside Figma as organized Auto-Layout components with Google Fonts applied!

---

### Method 3: Figma Tokens Studio / Variables Import
1. In Figma, open the **Tokens Studio** plugin or Figma **Local Variables**.
2. Click **Import / Load Tokens**.
3. Select `C:\Nanneer global\draft 3\public\figma_design_tokens.json`.
4. All color tokens (`brand.primary`, `typography.headline`, `surface.card`) and type scales will be bound to your Figma document.
