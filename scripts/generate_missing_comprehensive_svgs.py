import os

OUT_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
os.makedirs(OUT_DIR, exist_ok=True)

svgs = {}

# Common Pipe Gradients
PIPE_DEFS = """
    <filter id="ssPipeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="ssPipeGradDiag" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
"""

# ==============================================================================
# 1. BIDIRECTIONAL PIPE FLOW COMBINATIONS
# ==============================================================================

# A. Horizontal Pipe (Right to Left: flow-r2l)
svgs["pipe-straight-horizontal-flow-r2l-fluid-animated.svg"] = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes flow-r2l {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: 24; }} }}
      .anim-flow-r2l {{ stroke-dasharray: 5 7; animation: flow-r2l 0.8s linear infinite; }}
    </style>
    {PIPE_DEFS}
  </defs>
  <path d="M 190 100 L 10 100" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <path d="M 190 100 L 10 100" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 190 100 L 10 100" stroke="#bae6fd" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-flow-r2l"/>
  <polygon points="92,97 84,100 92,103" fill="#0284c7" />
  <rect x="8" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="188" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""

svgs["pipe-straight-horizontal-flow-r2l-fluid-static.svg"] = svgs["pipe-straight-horizontal-flow-r2l-fluid-animated.svg"].replace('class="anim-flow-r2l"', '').replace('<style>', '<!--').replace('</style>', '-->')

# B. Vertical Pipe (Bottom to Top: flow-b2t / Riser)
svgs["pipe-straight-vertical-flow-b2t-fluid-animated.svg"] = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes flow-b2t {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: 24; }} }}
      .anim-flow-b2t {{ stroke-dasharray: 5 7; animation: flow-b2t 0.8s linear infinite; }}
    </style>
    {PIPE_DEFS}
  </defs>
  <path d="M 100 190 L 100 10" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <path d="M 100 190 L 100 10" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 100 190 L 100 10" stroke="#bae6fd" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-flow-b2t"/>
  <polygon points="97,92 100,84 103,92" fill="#0284c7" />
  <rect x="94.5" y="8" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="188" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""

svgs["pipe-straight-vertical-flow-b2t-fluid-static.svg"] = svgs["pipe-straight-vertical-flow-b2t-fluid-animated.svg"].replace('class="anim-flow-b2t"', '').replace('<style>', '<!--').replace('</style>', '-->')

# C. Reverse Elbows (Reverse Flow Direction)
elbow_reverses = {
    # Up to Left (reverse of left-up)
    "pipe-elbow-up-left": ("M 100 10 L 100 100 L 10 100", '<polygon points="48,97 38,100 48,103" fill="#0284c7" />', ["top", "left"]),
    # Down to Left (reverse of left-down)
    "pipe-elbow-down-left": ("M 100 190 L 100 100 L 10 100", '<polygon points="48,97 38,100 48,103" fill="#0284c7" />', ["bottom", "left"]),
    # Up to Right (reverse of right-up)
    "pipe-elbow-up-right": ("M 100 10 L 100 100 L 190 100", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', ["top", "right"]),
    # Down to Right (reverse of right-down)
    "pipe-elbow-down-right": ("M 100 190 L 100 100 L 190 100", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', ["bottom", "right"]),
}

for ename, (epath, earrow, eends) in elbow_reverses.items():
    svgs[f"{ename}-fluid-animated.svg"] = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes ef-flow {{ from {{ stroke-dashoffset: 24; }} to {{ stroke-dashoffset: 0; }} }}
      .anim-ef {{ stroke-dasharray: 5 7; animation: ef-flow 0.8s linear infinite; }}
    </style>
    {PIPE_DEFS}
  </defs>
  <path d="{epath}" stroke="url(#ssPipeGradDiag)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <path d="{epath}" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="{epath}" stroke="#bae6fd" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-ef"/>
  {earrow}
</svg>"""
    svgs[f"{ename}-fluid-static.svg"] = svgs[f"{ename}-fluid-animated.svg"].replace('class="anim-ef"', '').replace('<style>', '<!--').replace('</style>', '-->')


# ==============================================================================
# 2. WATER SOFTENER RESIN COLUMN (GOLDEN AMBER CATION RESIN BED)
# ==============================================================================

SOFTENER_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <defs>
    <style>
      @keyframes soft-stream { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(40px); opacity: 0.2; } }
      .anim-soft { animation: soft-stream 1.5s linear infinite; }
    </style>
  </defs>
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <!-- Golden Cation Exchange Resin Bed -->
  <rect x="90" y="92" width="96" height="150" fill="#f59e0b" opacity="0.9"/>
  <!-- Support Gravel Underbed -->
  <rect x="90" y="242" width="96" height="55" fill="#ca8a04" opacity="0.8"/>
  <g class="anim-soft">
    <circle cx="118" cy="115" r="3" fill="#00e5ff"/>
    <circle cx="158" cy="130" r="3.5" fill="#38bdf8"/>
    <circle cx="138" cy="165" r="3" fill="#e0f2fe"/>
  </g>
</svg>"""

svgs["filter-water-softener-resin-fluid-animated.svg"] = SOFTENER_ANIM
svgs["filter-water-softener-resin-fluid-static.svg"] = SOFTENER_ANIM.replace('class="anim-soft"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["filter-water-softener-resin-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""


# ==============================================================================
# 3. VALVES: CHECK / NON-RETURN (NRV) & MANUAL BUTTERFLY ISOLATION
# ==============================================================================

# A. Non-Return Check Valve (NRV Horizontal)
svgs["valve-check-non-return-horizontal-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-flow { 0% { transform: translateX(0); opacity: 0.2; } 50% { opacity: 1; } 100% { transform: translateX(25px); opacity: 0.2; } }
      .anim-nrv { animation: nrv-flow 1.2s linear infinite; }
    </style>
  </defs>
  <rect x="25" y="88" width="150" height="24" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <!-- Disc Casing Flange -->
  <circle cx="100" cy="100" r="30" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <!-- Internal Swing Check Disc & Seat (Flow L to R) -->
  <line x1="90" y1="80" x2="90" y2="120" stroke="#94a3b8" stroke-width="4"/>
  <line x1="90" y1="80" x2="114" y2="105" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <!-- Left/Right Flanges -->
  <rect x="20" y="82" width="6" height="36" rx="1.5" fill="#475569"/>
  <rect x="174" y="82" width="6" height="36" rx="1.5" fill="#475569"/>
  <g class="anim-nrv">
    <polygon points="65,100 58,96 58,104" fill="#38bdf8"/>
    <polygon points="140,100 133,96 133,104" fill="#38bdf8"/>
  </g>
</svg>"""

svgs["valve-check-non-return-horizontal-static.svg"] = svgs["valve-check-non-return-horizontal-active-animated.svg"].replace('class="anim-nrv"', '').replace('<style>', '<!--').replace('</style>', '-->')

# B. Non-Return Check Valve (NRV Vertical - Riser)
svgs["valve-check-non-return-vertical-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-vflow { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 1; } 100% { transform: translateY(-25px); opacity: 0.2; } }
      .anim-nrv-v { animation: nrv-vflow 1.2s linear infinite; }
    </style>
  </defs>
  <rect x="88" y="25" width="24" height="150" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="30" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <line x1="80" y1="110" x2="120" y2="110" stroke="#94a3b8" stroke-width="4"/>
  <line x1="80" y1="110" x2="105" y2="86" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <rect x="82" y="20" width="36" height="6" rx="1.5" fill="#475569"/>
  <rect x="82" y="174" width="36" height="6" rx="1.5" fill="#475569"/>
  <g class="anim-nrv-v">
    <polygon points="100,140 96,147 104,147" fill="#38bdf8"/>
    <polygon points="100,65 96,72 104,72" fill="#38bdf8"/>
  </g>
</svg>"""

svgs["valve-check-non-return-vertical-static.svg"] = svgs["valve-check-non-return-vertical-active-animated.svg"].replace('class="anim-nrv-v"', '').replace('<style>', '<!--').replace('</style>', '-->')

# C. Manual Butterfly / Ball Isolation Valve (Open vs Closed)
svgs["valve-manual-isolation-open-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <polygon points="40,80 100,100 40,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="160,80 100,100 160,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Open (parallel to flow) -->
  <line x1="100" y1="100" x2="100" y2="60" stroke="#64748b" stroke-width="4"/>
  <rect x="95" y="45" width="55" height="10" rx="3" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
</svg>"""

svgs["valve-manual-isolation-closed-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <polygon points="40,80 100,100 40,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="160,80 100,100 160,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Closed (perpendicular to flow) -->
  <line x1="100" y1="100" x2="100" y2="60" stroke="#64748b" stroke-width="4"/>
  <rect x="72" y="45" width="55" height="10" rx="3" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5"/>
</svg>"""


# ==============================================================================
# 4. HORIZONTAL CYLINDRICAL TANK (CIP / BRINE / STORAGE)
# ==============================================================================

svgs["tank-cylindrical-horizontal-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 220" width="360" height="220">
  <defs>
    <style>
      @keyframes ht-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(12px); } }
      .anim-ht { animation: ht-wave 2.6s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Saddle Supports -->
  <polygon points="80,160 110,160 120,200 70,200" fill="#334155" stroke="#475569" stroke-width="2"/>
  <polygon points="250,160 280,160 290,200 240,200" fill="#334155" stroke="#475569" stroke-width="2"/>
  <!-- Dish Head Cylinder Body -->
  <rect x="50" y="45" width="260" height="120" rx="40" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="54" y="80" width="252" height="82" rx="20" fill="#0284c7" fill-opacity="0.85"/>
  <g class="anim-ht">
    <path d="M 54 80 Q 117 72 180 80 T 306 80" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
  <!-- Top Manhole & Nozzles -->
  <rect x="165" y="30" width="30" height="15" fill="#334155" stroke="#64748b" stroke-width="2"/>
</svg>"""

svgs["tank-cylindrical-horizontal-fluid-static.svg"] = svgs["tank-cylindrical-horizontal-fluid-animated.svg"].replace('class="anim-ht"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-cylindrical-horizontal-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 220" width="360" height="220">
  <polygon points="80,160 110,160 120,200 70,200" fill="#334155" stroke="#475569" stroke-width="2"/>
  <polygon points="250,160 280,160 290,200 240,200" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="50" y="45" width="260" height="120" rx="40" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="165" y="30" width="30" height="15" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>"""


# ==============================================================================
# 5. IN-LINE SCADA SENSORS: FLOW METER (FIT) & LEVEL TRANSMITTER (LIT)
# ==============================================================================

# A. Electromagnetic Flow Meter (FIT - in-line sensor spool)
svgs["sensor-flow-meter-electromagnetic-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes fit-glow { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
      .anim-fit { animation: fit-glow 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Flanged Flow Tube Spool -->
  <rect x="30" y="90" width="140" height="20" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="25" y="82" width="6" height="36" rx="1.5" fill="#475569"/>
  <rect x="169" y="82" width="6" height="36" rx="1.5" fill="#475569"/>
  <!-- Sensor Head / Magnetic Coil Housing -->
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <!-- Transmitter Transmitter Neck & Display Puck Top -->
  <rect x="95" y="58" width="10" height="22" fill="#64748b"/>
  <circle cx="100" cy="48" r="18" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <!-- Display Window Glow -->
  <circle cx="100" cy="48" r="12" fill="#10b981" fill-opacity="0.3" class="anim-fit"/>
  <circle cx="100" cy="48" r="4" fill="#10b981"/>
</svg>"""

svgs["sensor-flow-meter-electromagnetic-static.svg"] = svgs["sensor-flow-meter-electromagnetic-active-animated.svg"].replace('class="anim-fit"', '').replace('<style>', '<!--').replace('</style>', '-->')

# B. Ultrasonic / Radar Level Transmitter (LIT - tank top nozzle mount)
svgs["sensor-level-transmitter-ultrasonic-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 200" width="160" height="200">
  <defs>
    <style>
      @keyframes lit-pulse {
        0% { transform: translateY(0) scale(0.6); opacity: 0.9; }
        100% { transform: translateY(50px) scale(1.3); opacity: 0; }
      }
      .anim-lit-wave { transform-origin: 80px 105px; animation: lit-pulse 1.4s ease-out infinite; }
    </style>
  </defs>
  <!-- Transmitter Enclosure Head -->
  <rect x="62" y="30" width="36" height="42" rx="4" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <circle cx="80" cy="51" r="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <circle cx="80" cy="51" r="4" fill="#10b981"/>
  <!-- Mounting Flange -->
  <rect x="52" y="72" width="56" height="8" rx="1.5" fill="#475569" stroke="#64748b" stroke-width="1.5"/>
  <!-- Ultrasonic Transducer Cone Nozzle -->
  <polygon points="68,80 92,80 86,105 74,105" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <!-- Emitted Acoustic / Radar Waves -->
  <g class="anim-lit-wave">
    <path d="M 65 120 Q 80 130 95 120" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M 58 135 Q 80 150 102 135" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
  </g>
</svg>"""

svgs["sensor-level-transmitter-ultrasonic-static.svg"] = svgs["sensor-level-transmitter-ultrasonic-active-animated.svg"].replace('class="anim-lit-wave"', '').replace('<style>', '<!--').replace('</style>', '-->')

print(f"Generating {len(svgs)} additional comprehensive SVGs into {OUT_DIR}...")
for fname, content in svgs.items():
    if "<text" in content.lower():
        raise ValueError(f"Strict rule violated: <text> tag found in {fname}")
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"  + Generated {fname}")

print("All comprehensive assets successfully written!")
