import os
import re

ASSET_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
os.makedirs(ASSET_DIR, exist_ok=True)

# Standard Unified 3-Layer Pipe Architecture
# Casing: 7px with #ssPipeGrad
# Fluid Core: 4px #0284c7
# Flow Dashes: 2.5px #bae6fd (stroke-dasharray="5 7", animation: 0.8s)

COMMON_DEFS = """
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
# 1. STANDARDIZED FLUSH PIPES (Edge-to-Edge: 0 to 200, center at 100)
# ==============================================================================

# Ferrule collar helper: flush to edge
def edge_ferrules(ends):
    tags = []
    for e in ends:
        if e == "left":
            tags.append('<rect x="0" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif e == "right":
            tags.append('<rect x="196" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif e == "top":
            tags.append('<rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
        elif e == "bottom":
            tags.append('<rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
    return "\n  ".join(tags)

pipe_flush_configs = {
    # Straights
    "pipe-horizontal": {
        "grad": "ssPipeGradH",
        "ends": ["left", "right"],
        "paths": {
            "flow-left-to-right": ("M 0 100 L 200 100", '<polygon points="108,97 116,100 108,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"),
            "flow-right-to-left": ("M 200 100 L 0 100", '<polygon points="92,97 84,100 92,103" fill="#0284c7" />', "from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }"),
        }
    },
    "pipe-vertical": {
        "grad": "ssPipeGradV",
        "ends": ["top", "bottom"],
        "paths": {
            "flow-top-to-bottom": ("M 100 0 L 100 200", '<polygon points="97,108 100,116 103,108" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"),
            "flow-bottom-to-top": ("M 100 200 L 100 0", '<polygon points="97,92 100,84 103,92" fill="#0284c7" />', "from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }"),
        }
    },
    # Elbows
    "pipe-elbow-left-to-up": {
        "grad": "ssPipeGradDiag",
        "ends": ["left", "top"],
        "paths": {
            "": ("M 0 100 L 100 100 L 100 0", '<polygon points="97,48 100,38 103,48" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-up-to-left": {
        "grad": "ssPipeGradDiag",
        "ends": ["top", "left"],
        "paths": {
            "": ("M 100 0 L 100 100 L 0 100", '<polygon points="48,97 38,100 48,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-left-to-down": {
        "grad": "ssPipeGradDiag",
        "ends": ["left", "bottom"],
        "paths": {
            "": ("M 0 100 L 100 100 L 100 200", '<polygon points="97,152 100,162 103,152" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-down-to-left": {
        "grad": "ssPipeGradDiag",
        "ends": ["bottom", "left"],
        "paths": {
            "": ("M 100 200 L 100 100 L 0 100", '<polygon points="48,97 38,100 48,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-right-to-up": {
        "grad": "ssPipeGradDiag",
        "ends": ["right", "top"],
        "paths": {
            "": ("M 200 100 L 100 100 L 100 0", '<polygon points="97,48 100,38 103,48" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-up-to-right": {
        "grad": "ssPipeGradDiag",
        "ends": ["top", "right"],
        "paths": {
            "": ("M 100 0 L 100 100 L 200 100", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-right-to-down": {
        "grad": "ssPipeGradDiag",
        "ends": ["right", "bottom"],
        "paths": {
            "": ("M 200 100 L 100 100 L 100 200", '<polygon points="97,152 100,162 103,152" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-elbow-down-to-right": {
        "grad": "ssPipeGradDiag",
        "ends": ["bottom", "right"],
        "paths": {
            "": ("M 100 200 L 100 100 L 200 100", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    # Tees
    "pipe-tee-branch-up": {
        "grad": "ssPipeGradH",
        "ends": ["left", "right", "top"],
        "paths": {
            "": ("M 0 100 L 200 100 M 100 100 L 100 0", '<polygon points="97,48 100,38 103,48" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-tee-branch-down": {
        "grad": "ssPipeGradH",
        "ends": ["left", "right", "bottom"],
        "paths": {
            "": ("M 0 100 L 200 100 M 100 100 L 100 200", '<polygon points="97,152 100,162 103,152" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-tee-branch-left": {
        "grad": "ssPipeGradV",
        "ends": ["top", "bottom", "left"],
        "paths": {
            "": ("M 100 0 L 100 200 M 100 100 L 0 100", '<polygon points="48,97 38,100 48,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    "pipe-tee-branch-right": {
        "grad": "ssPipeGradV",
        "ends": ["top", "bottom", "right"],
        "paths": {
            "": ("M 100 0 L 100 200 M 100 100 L 200 100", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
    # Cross
    "pipe-cross-4way": {
        "grad": "ssPipeGradH",
        "ends": ["left", "right", "top", "bottom"],
        "paths": {
            "": ("M 0 100 L 200 100 M 100 0 L 100 200", '<polygon points="152,97 162,100 152,103" fill="#0284c7" />', "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }")
        }
    },
}

generated_count = 0

for base_name, pcfg in pipe_flush_configs.items():
    grad_id = pcfg["grad"]
    ferrules = edge_ferrules(pcfg["ends"])

    # Dry Static
    first_path = list(pcfg["paths"].values())[0][0]
    dry_name = f"{base_name}-dry-static.svg"
    dry_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>{COMMON_DEFS}</defs>
  <path d="{first_path}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  {ferrules}
</svg>"""
    with open(os.path.join(ASSET_DIR, dry_name), "w", encoding="utf-8") as f:
        f.write(dry_content.strip() + "\n")
    generated_count += 1

    for flow_dir, (path_d, arrow_svg, kf_body) in pcfg["paths"].items():
        prefix = f"{base_name}-{flow_dir}" if flow_dir else base_name
        fluid_static_name = f"{prefix}-fluid-static.svg"
        fluid_anim_name = f"{prefix}-fluid-animated.svg"

        # Static
        static_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>{COMMON_DEFS}</defs>
  <path d="{path_d}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <path d="{path_d}" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  {arrow_svg}
  {ferrules}
</svg>"""
        with open(os.path.join(ASSET_DIR, fluid_static_name), "w", encoding="utf-8") as f:
            f.write(static_content.strip() + "\n")
        generated_count += 1

        # Animated
        css_anim = f"""
      @keyframes p-flow-anim {{ {kf_body} }}
      .anim-p-flow {{ stroke-dasharray: 5 7; animation: p-flow-anim 0.8s linear infinite; }}
"""
        anim_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>{css_anim}</style>
    {COMMON_DEFS}
  </defs>
  <path d="{path_d}" stroke="url(#{grad_id})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <path d="{path_d}" stroke="#0284c7" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="{path_d}" stroke="#bae6fd" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-p-flow"/>
  {arrow_svg}
  {ferrules}
</svg>"""
        with open(os.path.join(ASSET_DIR, fluid_anim_name), "w", encoding="utf-8") as f:
            f.write(anim_content.strip() + "\n")
        generated_count += 1

# ==============================================================================
# 2. STANDARDIZED CENTRIFUGAL PUMPS (Flush Nozzles matching 7px Casing & 4px Fluid)
# ==============================================================================
# Pump ViewBox: 0 0 300 264. Center: (150, 132).
# Left Suction Nozzle: Starts at x=0, y=132, goes to casing at x=84! (Perfect flush at x=0)
# Top Discharge Nozzle: Starts at y=0, x=150, goes to casing at y=66! (Perfect flush at y=0)

def make_flush_centrifugal(dn="dn50", direction="left-to-right", state="running"):
    is_run = (state == "running")
    is_fault = (state == "fault")

    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    fluid_fill = "url(#cp_fluid)" if is_run else ("#450a0a" if is_fault else "#0f172a")
    blade_color = "#38bdf8" if is_run else ("#f87171" if is_fault else "#64748b")
    blade_stroke = "#bae6fd" if is_run else ("#fca5a5" if is_fault else "#94a3b8")

    css = ""
    if is_run:
        css = """
      @keyframes spin-imp { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      @keyframes flow-glow { 0%, 100% { opacity: 0.35; r: 16px; } 50% { opacity: 0.85; r: 24px; } }
      .anim-imp { transform-origin: 150px 132px; animation: spin-imp 1.8s linear infinite; }
      .anim-flow { animation: flow-glow 2s ease-in-out infinite; }
"""
    elif is_fault:
        css = """
      @keyframes alert-pulse { 0%, 100% { stroke-opacity: 0.3; stroke-width: 3px; } 50% { stroke-opacity: 1; stroke-width: 6px; } }
      .anim-fault { animation: alert-pulse 0.9s ease-in-out infinite; }
"""

    imp_class = ' class="anim-imp"' if is_run else ""
    glow_class = ' class="anim-flow"' if is_run else ""
    fault_class = ' class="anim-fault"' if is_fault else ""

    if direction == "left-to-right":
        suction_pipe = '<path d="M 0 132 L 84 132" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M 0 132 L 84 132" stroke="#0284c7" stroke-width="4" fill="none"/><rect x="0" y="126.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
        discharge_pipe = '<path d="M 150 0 L 150 66" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M 150 0 L 150 66" stroke="#0284c7" stroke-width="4" fill="none"/><rect x="144.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
        motor_x = 180
    else:
        suction_pipe = '<path d="M 300 132 L 216 132" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M 300 132 L 216 132" stroke="#0284c7" stroke-width="4" fill="none"/><rect x="296" y="126.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
        discharge_pipe = '<path d="M 150 0 L 150 66" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M 150 0 L 150 66" stroke="#0284c7" stroke-width="4" fill="none"/><rect x="144.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
        motor_x = 55

    style_tag = f"<style>{css}</style>" if css else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 264" width="300" height="264">
  <defs>
    {style_tag}
    {COMMON_DEFS}
    <linearGradient id="cp_case" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" /><stop offset="50%" stop-color="#1e293b" /><stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="cp_fluid" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" /><stop offset="65%" stop-color="#0284c7" stop-opacity="0.7" /><stop offset="100%" stop-color="#0369a1" stop-opacity="0.4" />
    </radialGradient>
  </defs>

  <!-- Footing -->
  <rect x="70" y="212" width="160" height="14" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="100" y="200" width="100" height="12" fill="#334155"/>

  <!-- Drive Motor Housing -->
  <rect x="{motor_x}" y="96" width="65" height="72" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <line x1="{motor_x + 12}" y1="96" x2="{motor_x + 12}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 24}" y1="96" x2="{motor_x + 24}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 36}" y1="96" x2="{motor_x + 36}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 48}" y1="96" x2="{motor_x + 48}" y2="168" stroke="#334155" stroke-width="2"/>

  <!-- Volute Casing Outer Ring -->
  <circle cx="150" cy="132" r="66" fill="url(#cp_case)" stroke="#64748b" stroke-width="4"/>
  <circle cx="150" cy="132" r="54" fill="#0f172a" stroke="{ring_color}" stroke-width="3" stroke-dasharray="4 2"{fault_class}/>
  <circle cx="150" cy="132" r="46" fill="{fluid_fill}"/>
  <circle cx="150" cy="132" r="20" fill="#00e5ff" opacity="0.6"{glow_class}/>

  <!-- 4-Blade Impeller -->
  <g{imp_class}>
    <path d="M 150 132 Q 135 102 150 88 Q 165 102 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 180 117 194 132 Q 180 147 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 165 162 150 176 Q 135 162 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 120 147 106 132 Q 120 117 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <circle cx="150" cy="132" r="10" fill="#0f172a" stroke="{blade_color}" stroke-width="2"/>
    <circle cx="150" cy="132" r="4" fill="{blade_color}"/>
  </g>

  <!-- Flush Connection Nozzles (Matching 7px / 4px Pipe Core) -->
  {suction_pipe}
  {discharge_pipe}
</svg>"""

for dn in ["dn25", "dn50", "dn100"]:
    for direction in ["left-to-right", "right-to-left"]:
        # Running animated
        fname = f"centrifugal-pump-{dn}-flow-{direction}-running-animated.svg"
        with open(os.path.join(ASSET_DIR, fname), "w", encoding="utf-8") as f:
            f.write(make_flush_centrifugal(dn, direction, "running").strip() + "\n")
        generated_count += 1

        # Running static
        fname = f"centrifugal-pump-{dn}-flow-{direction}-running-static.svg"
        content = make_flush_centrifugal(dn, direction, "running").replace('class="anim-imp"', '').replace('class="anim-flow"', '').replace('<style>', '<!--').replace('</style>', '-->')
        with open(os.path.join(ASSET_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        generated_count += 1

        # Stopped static
        fname = f"centrifugal-pump-{dn}-flow-{direction}-stopped-static.svg"
        with open(os.path.join(ASSET_DIR, fname), "w", encoding="utf-8") as f:
            f.write(make_flush_centrifugal(dn, direction, "stopped").strip() + "\n")
        generated_count += 1

        # Fault animated
        fname = f"centrifugal-pump-{dn}-flow-{direction}-fault-animated.svg"
        with open(os.path.join(ASSET_DIR, fname), "w", encoding="utf-8") as f:
            f.write(make_flush_centrifugal(dn, direction, "fault").strip() + "\n")
        generated_count += 1

# ==============================================================================
# 3. STANDARDIZED VALVES (Flush 7px casing / 4px fluid core)
# ==============================================================================
# In-line Solenoid Valve: viewBox 0 0 200 200. Ports at (0, 100) and (200, 100)
def make_flush_solenoid(state="active-animated"):
    is_anim = ("animated" in state)
    is_active = ("active" in state)
    ring_color = "#10b981" if is_active else "#ef4444"
    css = """
      @keyframes v-stream { from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; } }
      .anim-v-dash { stroke-dasharray: 5 7; animation: v-stream 0.8s linear infinite; }
""" if is_anim else ""

    dash_line = '<path d="M 0 100 L 200 100" stroke="#bae6fd" stroke-width="2.5" fill="none" class="anim-v-dash"/>' if is_anim else ""
    arrow_line = '<polygon points="108,97 116,100 108,103" fill="#0284c7"/>' if is_active else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>{css}</style>
    {COMMON_DEFS}
  </defs>
  <!-- Through Pipe -->
  <path d="M 0 100 L 200 100" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 0 100 L 200 100" stroke="{('#0284c7' if is_active else '#475569')}" stroke-width="4" fill="none"/>
  {dash_line}
  {arrow_line}
  <!-- Solenoid Body -->
  <polygon points="60,82 100,100 60,118" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="140,82 100,100 140,118" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="{ring_color}" stroke-width="2"/>
  <!-- Solenoid Coil Actuator Top -->
  <rect x="88" y="44" width="24" height="34" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="100" y1="78" x2="100" y2="88" stroke="#cbd5e1" stroke-width="3"/>
  <!-- Ferrules -->
  <rect x="0" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="196" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""

with open(os.path.join(ASSET_DIR, "solenoid-valve-active-animated.svg"), "w", encoding="utf-8") as f:
    f.write(make_flush_solenoid("active-animated").strip() + "\n")
with open(os.path.join(ASSET_DIR, "solenoid-valve-active-static.svg"), "w", encoding="utf-8") as f:
    f.write(make_flush_solenoid("active-static").strip() + "\n")
with open(os.path.join(ASSET_DIR, "solenoid-valve-closed-static.svg"), "w", encoding="utf-8") as f:
    f.write(make_flush_solenoid("closed-static").strip() + "\n")

print(f"Successfully standardized {generated_count} assets with unified 7px casing / 4px core flush geometry!")
