import os

OUT_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
os.makedirs(OUT_DIR, exist_ok=True)

# Exact Polished Stainless Steel 316 Pipeline Gradients and Styles from ScadaSchematicSimulation.tsx
PIPE_DEFS = """
    <filter id="ssPipeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>

    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" />
      <stop offset="85%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>

    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" />
      <stop offset="85%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>

    <linearGradient id="ssPipeGradDiag" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" />
      <stop offset="85%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
"""

# Helper to generate sleek tri-clamp sanitary connection collars at pipe ends
def make_sleek_collars(ends):
    collars = []
    for end in ends:
        if end == "left":
            collars.append('<rect x="8" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif end == "right":
            collars.append('<rect x="188" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif end == "top":
            collars.append('<rect x="94.5" y="8" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif end == "bottom":
            collars.append('<rect x="94.5" y="188" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
    return "\n  ".join(collars)

# Sleek 3-Layer Pipe Geometry (matching ScadaSchematicSimulation.tsx)
pipe_definitions = {
    # 1. Straight Horizontal
    "pipe-straight-horizontal": {
        "casing_grad": "ssPipeGradH",
        "path": "M 10 100 L 190 100",
        "arrow": '<polygon points="108,97 116,100 108,103" fill="#0284c7" />',
        "ends": ["left", "right"],
    },

    # 2. Straight Vertical
    "pipe-straight-vertical": {
        "casing_grad": "ssPipeGradV",
        "path": "M 100 10 L 100 190",
        "arrow": '<polygon points="97,108 100,116 103,108" fill="#0284c7" />',
        "ends": ["top", "bottom"],
    },

    # 3. 90° Elbow: Left to Up
    "pipe-elbow-left-up": {
        "casing_grad": "ssPipeGradDiag",
        "path": "M 10 100 L 100 100 L 100 10",
        "arrow": '<polygon points="97,48 100,38 103,48" fill="#0284c7" />',
        "ends": ["left", "top"],
    },

    # 4. 90° Elbow: Left to Down
    "pipe-elbow-left-down": {
        "casing_grad": "ssPipeGradDiag",
        "path": "M 10 100 L 100 100 L 100 190",
        "arrow": '<polygon points="97,152 100,162 103,152" fill="#0284c7" />',
        "ends": ["left", "bottom"],
    },

    # 5. 90° Elbow: Right to Up
    "pipe-elbow-right-up": {
        "casing_grad": "ssPipeGradDiag",
        "path": "M 190 100 L 100 100 L 100 10",
        "arrow": '<polygon points="97,48 100,38 103,48" fill="#0284c7" />',
        "ends": ["right", "top"],
    },

    # 6. 90° Elbow: Right to Down
    "pipe-elbow-right-down": {
        "casing_grad": "ssPipeGradDiag",
        "path": "M 190 100 L 100 100 L 100 190",
        "arrow": '<polygon points="97,152 100,162 103,152" fill="#0284c7" />',
        "ends": ["right", "bottom"],
    },

    # 7. Tee: Up Branch
    "pipe-tee-up": {
        "casing_grad": "ssPipeGradH",
        "path": "M 10 100 L 190 100 M 100 100 L 100 10",
        "arrow": '<polygon points="97,48 100,38 103,48" fill="#0284c7" />',
        "ends": ["left", "right", "top"],
    },

    # 8. Tee: Down Branch
    "pipe-tee-down": {
        "casing_grad": "ssPipeGradH",
        "path": "M 10 100 L 190 100 M 100 100 L 100 190",
        "arrow": '<polygon points="97,152 100,162 103,152" fill="#0284c7" />',
        "ends": ["left", "right", "bottom"],
    },

    # 9. Tee: Left Branch
    "pipe-tee-left": {
        "casing_grad": "ssPipeGradV",
        "path": "M 100 10 L 100 190 M 100 100 L 10 100",
        "arrow": '<polygon points="48,97 38,100 48,103" fill="#0284c7" />',
        "ends": ["top", "bottom", "left"],
    },

    # 10. Tee: Right Branch
    "pipe-tee-right": {
        "casing_grad": "ssPipeGradV",
        "path": "M 100 10 L 100 190 M 100 100 L 190 100",
        "arrow": '<polygon points="152,97 162,100 152,103" fill="#0284c7" />',
        "ends": ["top", "bottom", "right"],
    },

    # 11. Cross 4-Way
    "pipe-cross-4way": {
        "casing_grad": "ssPipeGradH",
        "path": "M 10 100 L 190 100 M 100 10 L 100 190",
        "arrow": '<polygon points="152,97 162,100 152,103" fill="#0284c7" />',
        "ends": ["left", "right", "top", "bottom"],
    },
}

pipe_svgs = {}

for name, cfg in pipe_definitions.items():
    grad_id = cfg["casing_grad"]
    path_d = cfg["path"]
    arrow_svg = cfg["arrow"]
    collars_svg = make_sleek_collars(cfg["ends"])

    # 1. Dry / Empty Stainless Steel Pipe (Static)
    dry_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    {PIPE_DEFS}
  </defs>

  <!-- 1. Outer Stainless Steel Casing (7px) -->
  <path d="{path_d}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- Sleek Tri-Clamp End Ferrules -->
  {collars_svg}
</svg>"""
    pipe_svgs[f"{name}-dry-static.svg"] = dry_svg

    # 2. With Fluid (Static) - Exactly as rendered on ScadaSchematicSimulation
    fluid_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    {PIPE_DEFS}
  </defs>

  <!-- 1. Outer Stainless Steel Casing (7px) -->
  <path d="{path_d}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- 2. Inner Process Fluid Core (4px Cerulean Blue) -->
  <path d="{path_d}" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- 3. Directional Flow Arrow -->
  {arrow_svg}

  <!-- Sleek Tri-Clamp End Ferrules -->
  {collars_svg}
</svg>"""
    pipe_svgs[f"{name}-fluid-static.svg"] = fluid_svg

    # 3. With Fluid (Animated Flow Dashes) - Identical to live schematic animation
    css_anim = """
      @keyframes schematic-flow {
        from { stroke-dashoffset: 24; }
        to { stroke-dashoffset: 0; }
      }
      .anim-schematic-dash {
        stroke-dasharray: 5 7;
        animation: schematic-flow 0.8s linear infinite;
      }
"""
    anim_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>{css_anim}</style>
    {PIPE_DEFS}
  </defs>

  <!-- 1. Outer Stainless Steel Casing (7px) -->
  <path d="{path_d}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- 2. Inner Process Fluid Core (4px Cerulean Blue) -->
  <path d="{path_d}" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- 3. Live Animated Flow Dashes (2.5px Light Cyan, 5 7 pattern) -->
  <path d="{path_d}" stroke="#bae6fd" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-schematic-dash"/>

  <!-- 4. Directional Flow Arrow -->
  {arrow_svg}

  <!-- Sleek Tri-Clamp End Ferrules -->
  {collars_svg}
</svg>"""
    pipe_svgs[f"{name}-fluid-animated.svg"] = anim_svg

# ==============================================================================
# Also generate dedicated PSF, ACF, and expanded Blower assets
# ==============================================================================

# PSF (Pressure Sand Filter - 3 distinct graded layers: sand, garnet, gravel)
PSF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <defs>
    <style>
      @keyframes psf-stream { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(40px); opacity: 0.2; } }
      .anim-psf { animation: psf-stream 1.5s linear infinite; }
    </style>
  </defs>
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <!-- Graded Sand Bed Layers -->
  <rect x="90" y="92" width="96" height="60" fill="#fef08a" opacity="0.9"/>
  <rect x="90" y="152" width="96" height="70" fill="#ca8a04" opacity="0.9"/>
  <rect x="90" y="222" width="96" height="75" fill="#78350f" opacity="0.9"/>
  <g class="anim-psf">
    <line x1="120" y1="100" x2="120" y2="125" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="156" y1="110" x2="156" y2="135" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

pipe_svgs["filter-pressure-sand-psf-fluid-animated.svg"] = PSF_ANIM
pipe_svgs["filter-pressure-sand-psf-fluid-static.svg"] = PSF_ANIM.replace('class="anim-psf"', '').replace('<style>', '<!--').replace('</style>', '-->')
pipe_svgs["filter-pressure-sand-psf-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

# ACF (Activated Carbon Filter - deep charcoal black granular carbon bed)
ACF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <defs>
    <style>
      @keyframes acf-stream { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(40px); opacity: 0.2; } }
      .anim-acf { animation: acf-stream 1.5s linear infinite; }
    </style>
  </defs>
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <!-- Charcoal Black GAC Bed -->
  <rect x="90" y="92" width="96" height="150" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <rect x="90" y="242" width="96" height="55" fill="#475569" opacity="0.8"/>
  <g class="anim-acf">
    <line x1="120" y1="100" x2="120" y2="125" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="156" y1="110" x2="156" y2="135" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

pipe_svgs["filter-activated-carbon-acf-fluid-animated.svg"] = ACF_ANIM
pipe_svgs["filter-activated-carbon-acf-fluid-static.svg"] = ACF_ANIM.replace('class="anim-acf"', '').replace('<style>', '<!--').replace('</style>', '-->')
pipe_svgs["filter-activated-carbon-acf-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

# Expanded Blower (with Intake silencer, Rotary lobe/turbine, and States)
def make_expanded_blower(direction="l2r", state="running"):
    is_run = (state == "running")
    is_fault = (state == "fault")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    spin_class = ' class="anim-bl-spin"' if is_run else ""
    css = """
      @keyframes bl-rot { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-bl-spin { transform-origin: 132px 132px; animation: bl-rot 0.8s linear infinite; }
""" if is_run else ""

    silencer_x = 35 if direction == "l2r" else 200
    discharge_x = 180 if direction == "l2r" else 45

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 264" width="264" height="264">
  <defs><style>{css}</style></defs>
  <rect x="66" y="210" width="132" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <!-- Intake Silencer / Filter -->
  <rect x="{silencer_x}" y="115" width="30" height="34" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="{silencer_x + 6}" y1="120" x2="{silencer_x + 6}" y2="144" stroke="#0f172a" stroke-width="2"/>
  <line x1="{silencer_x + 14}" y1="120" x2="{silencer_x + 14}" y2="144" stroke="#0f172a" stroke-width="2"/>
  <line x1="{silencer_x + 22}" y1="120" x2="{silencer_x + 22}" y2="144" stroke="#0f172a" stroke-width="2"/>
  <!-- Casing -->
  <circle cx="132" cy="132" r="66" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
  <circle cx="132" cy="132" r="54" fill="#0f172a" stroke="{ring_color}" stroke-width="3" stroke-dasharray="3 3"/>
  <g{spin_class}>
    <path d="M 132 132 Q 120 100 132 86 Q 140 100 132 132 Z" fill="{('#67e8f9' if is_run else '#64748b')}"/>
    <path d="M 132 132 Q 155 110 165 100 Q 155 125 132 132 Z" fill="{('#38bdf8' if is_run else '#475569')}"/>
    <path d="M 132 132 Q 164 120 178 132 Q 164 140 132 132 Z" fill="{('#67e8f9' if is_run else '#64748b')}"/>
    <path d="M 132 132 Q 155 155 165 164 Q 140 155 132 132 Z" fill="{('#38bdf8' if is_run else '#475569')}"/>
    <path d="M 132 132 Q 120 164 132 178 Q 140 164 132 132 Z" fill="{('#67e8f9' if is_run else '#64748b')}"/>
    <path d="M 132 132 Q 110 155 100 165 Q 110 140 132 132 Z" fill="{('#38bdf8' if is_run else '#475569')}"/>
    <path d="M 132 132 Q 100 120 86 132 Q 100 140 132 132 Z" fill="{('#67e8f9' if is_run else '#64748b')}"/>
    <path d="M 132 132 Q 110 110 100 100 Q 125 110 132 132 Z" fill="{('#38bdf8' if is_run else '#475569')}"/>
    <circle cx="132" cy="132" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  </g>
  <!-- Discharge Line -->
  <rect x="{discharge_x}" y="122" width="28" height="20" fill="#334155" stroke="#64748b" stroke-width="2"/>
</svg>"""

pipe_svgs["blower-rotary-flow-l2r-running-animated.svg"] = make_expanded_blower("l2r", "running")
pipe_svgs["blower-rotary-flow-l2r-running-static.svg"] = make_expanded_blower("l2r", "running").replace('class="anim-bl-spin"', '').replace('<style>', '<!--').replace('</style>', '-->')
pipe_svgs["blower-rotary-flow-l2r-stopped-static.svg"] = make_expanded_blower("l2r", "stopped")
pipe_svgs["blower-rotary-flow-l2r-fault-animated.svg"] = make_expanded_blower("l2r", "fault")

pipe_svgs["blower-rotary-flow-r2l-running-animated.svg"] = make_expanded_blower("r2l", "running")
pipe_svgs["blower-rotary-flow-r2l-running-static.svg"] = make_expanded_blower("r2l", "running").replace('class="anim-bl-spin"', '').replace('<style>', '<!--').replace('</style>', '-->')
pipe_svgs["blower-rotary-flow-r2l-stopped-static.svg"] = make_expanded_blower("r2l", "stopped")
pipe_svgs["blower-rotary-flow-r2l-fault-animated.svg"] = make_expanded_blower("r2l", "fault")

print(f"Updating {len(pipe_svgs)} sleek SCADA pipe & equipment SVGs in {OUT_DIR}...")
for fname, content in pipe_svgs.items():
    if "<text" in content.lower():
        raise ValueError(f"Strict rule violated: <text> tag found in {fname}")
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"  + Updated {fname}")

print("All sleek SCADA pipe fittings, PSF, ACF, and Blower assets successfully updated!")
