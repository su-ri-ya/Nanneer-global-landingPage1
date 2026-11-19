import os
import re

OUT_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
os.makedirs(OUT_DIR, exist_ok=True)

svg_registry = {}

# ==============================================================================
# 1. PUMPS (CENTRIFUGAL, RO MULTISTAGE, SUBMERSIBLE, CHEMICAL DOSING)
# ==============================================================================

def make_centrifugal_pump(dn="dn50", direction="l2r", state="running", animated=False):
    """
    dn: 'dn25' (small), 'dn50' (medium), 'dn100' (large)
    direction: 'l2r' (suction left, discharge top), 'r2l' (suction right, discharge top)
    state: 'running', 'stopped', 'fault'
    animated: bool
    """
    nozzle_scales = {
        "dn25": {"pw": 16, "ph": 16, "fw": 6, "fh": 26, "label": "DN25"},
        "dn50": {"pw": 24, "ph": 24, "fw": 8, "fh": 36, "label": "DN50"},
        "dn100": {"pw": 34, "ph": 34, "fw": 12, "fh": 48, "label": "DN100"},
    }
    cfg = nozzle_scales[dn]
    
    # Colors according to state
    if state == "running":
        ring_color = "#10b981"
        fluid_fill = "url(#cp_fluid)"
        blade_color = "#38bdf8"
        blade_stroke = "#bae6fd"
        glow_pulse = True
        fault_pulse = False
    elif state == "fault":
        ring_color = "#ef4444"
        fluid_fill = "#450a0a"
        blade_color = "#f87171"
        blade_stroke = "#fca5a5"
        glow_pulse = False
        fault_pulse = True
    else: # stopped
        ring_color = "#475569"
        fluid_fill = "#0f172a"
        blade_color = "#64748b"
        blade_stroke = "#94a3b8"
        glow_pulse = False
        fault_pulse = False

    css_block = ""
    if animated:
        if state == "running":
            css_block = """
      @keyframes spin-impeller {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes flow-glow {
        0%, 100% { opacity: 0.35; r: 16px; }
        50% { opacity: 0.85; r: 24px; }
      }
      .anim-impeller {
        transform-origin: 150px 132px;
        animation: spin-impeller 1.8s linear infinite;
      }
      .anim-flow {
        animation: flow-glow 2s ease-in-out infinite;
      }
"""
        elif state == "fault":
            css_block = """
      @keyframes alert-pulse {
        0%, 100% { stroke-opacity: 0.3; stroke-width: 3px; }
        50% { stroke-opacity: 1; stroke-width: 6px; }
      }
      .anim-fault {
        animation: alert-pulse 0.9s ease-in-out infinite;
      }
"""

    impeller_class = ' class="anim-impeller"' if animated and state == "running" else ""
    flow_class = ' class="anim-flow"' if animated and state == "running" else ""
    ring_class = ' class="anim-fault"' if animated and state == "fault" else ""

    # Suction and discharge port geometry based on direction
    pw, ph, fw, fh = cfg["pw"], cfg["ph"], cfg["fw"], cfg["fh"]
    if direction == "l2r":
        # Suction Left
        suction_pipe = f'<rect x="{84 - pw}" y="{132 - ph/2}" width="{pw}" height="{ph}" fill="#1e293b" stroke="#475569" stroke-width="2"/>'
        suction_flange = f'<rect x="{84 - pw - fw}" y="{132 - fh/2}" width="{fw}" height="{fh}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        # Discharge Top
        discharge_pipe = f'<rect x="{150 - ph/2}" y="{66 - pw}" width="{ph}" height="{pw}" fill="#1e293b" stroke="#475569" stroke-width="2"/>'
        discharge_flange = f'<rect x="{150 - fh/2}" y="{66 - pw - fw}" width="{fh}" height="{fw}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        motor_x = 180
    else: # r2l
        # Suction Right
        suction_pipe = f'<rect x="216" y="{132 - ph/2}" width="{pw}" height="{ph}" fill="#1e293b" stroke="#475569" stroke-width="2"/>'
        suction_flange = f'<rect x="{216 + pw}" y="{132 - fh/2}" width="{fw}" height="{fh}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        # Discharge Top
        discharge_pipe = f'<rect x="{150 - ph/2}" y="{66 - pw}" width="{ph}" height="{pw}" fill="#1e293b" stroke="#475569" stroke-width="2"/>'
        discharge_flange = f'<rect x="{150 - fh/2}" y="{66 - pw - fw}" width="{fh}" height="{fw}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        motor_x = 55

    style_tag = f"<style>{css_block}</style>" if css_block else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 264" width="300" height="264">
  <defs>
    {style_tag}
    <linearGradient id="cp_case" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="50%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="cp_fluid" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" />
      <stop offset="65%" stop-color="#0284c7" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.4" />
    </radialGradient>
    <filter id="cp_shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.5" />
    </filter>
  </defs>

  <!-- Mounting Footing -->
  <rect x="70" y="212" width="160" height="14" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" filter="url(#cp_shadow)"/>
  <rect x="100" y="200" width="100" height="12" fill="#334155"/>

  <!-- Drive Motor Housing -->
  <rect x="{motor_x}" y="96" width="65" height="72" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <line x1="{motor_x + 12}" y1="96" x2="{motor_x + 12}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 24}" y1="96" x2="{motor_x + 24}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 36}" y1="96" x2="{motor_x + 36}" y2="168" stroke="#334155" stroke-width="2"/>
  <line x1="{motor_x + 48}" y1="96" x2="{motor_x + 48}" y2="168" stroke="#334155" stroke-width="2"/>

  <!-- Casing Outer Ring -->
  <circle cx="150" cy="132" r="66" fill="url(#cp_case)" stroke="#64748b" stroke-width="4" filter="url(#cp_shadow)"/>
  <!-- Status Indicator Ring -->
  <circle cx="150" cy="132" r="54" fill="#0f172a" stroke="{ring_color}" stroke-width="3" stroke-dasharray="4 2"{ring_class}/>

  <!-- Fluid Chamber -->
  <circle cx="150" cy="132" r="46" fill="{fluid_fill}"/>
  <circle cx="150" cy="132" r="20" fill="#00e5ff" opacity="0.6"{flow_class}/>

  <!-- 4-Blade Impeller -->
  <g{impeller_class}>
    <path d="M 150 132 Q 135 102 150 88 Q 165 102 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 180 117 194 132 Q 180 147 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 165 162 150 176 Q 135 162 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 120 147 106 132 Q 120 117 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <circle cx="150" cy="132" r="10" fill="#0f172a" stroke="{blade_color}" stroke-width="2"/>
    <circle cx="150" cy="132" r="4" fill="{blade_color}"/>
  </g>

  <!-- Ports / Flanges -->
  {suction_pipe}
  {suction_flange}
  {discharge_pipe}
  {discharge_flange}
</svg>
"""
    return svg

# Generate all centrifugal combinations: dn25, dn50, dn100 x l2r, r2l x states
for dn in ["dn25", "dn50", "dn100"]:
    for direction in ["l2r", "r2l"]:
        # Running animated
        svg_registry[f"pump-centrifugal-{dn}-flow-{direction}-running-animated.svg"] = make_centrifugal_pump(dn, direction, "running", animated=True)
        # Running static
        svg_registry[f"pump-centrifugal-{dn}-flow-{direction}-running-static.svg"] = make_centrifugal_pump(dn, direction, "running", animated=False)
        # Stopped static
        svg_registry[f"pump-centrifugal-{dn}-flow-{direction}-stopped-static.svg"] = make_centrifugal_pump(dn, direction, "stopped", animated=False)
        # Fault animated
        svg_registry[f"pump-centrifugal-{dn}-flow-{direction}-fault-animated.svg"] = make_centrifugal_pump(dn, direction, "fault", animated=True)

# 2. RO Multistage High-Pressure Pump Combinations
def make_ro_pump(dn="dn50", state="running", animated=False):
    is_run = (state == "running")
    is_fault = (state == "fault")
    is_stop = (state == "stopped")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    fluid_opacity = "0.9" if (is_run or is_fault) else "0.0"
    stream_pulse = ' class="anim-ro-stream"' if animated and is_run else ""
    fault_pulse = ' class="anim-ro-fault"' if animated and is_fault else ""

    css = ""
    if animated:
        if is_run:
            css = """
      @keyframes ro-flow {
        0% { transform: translateY(0); opacity: 0.2; }
        50% { opacity: 0.95; }
        100% { transform: translateY(-40px); opacity: 0.2; }
      }
      .anim-ro-stream { animation: ro-flow 1.5s linear infinite; }
"""
        elif is_fault:
            css = """
      @keyframes ro-alert {
        0%, 100% { stroke-opacity: 0.3; stroke-width: 2px; }
        50% { stroke-opacity: 1; stroke-width: 5px; }
      }
      .anim-ro-fault { animation: ro-alert 0.8s ease-in-out infinite; }
"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 424" width="240" height="424">
  <defs>
    <style>{css}</style>
    <linearGradient id="ro_casing" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="25%" stop-color="#94a3b8" />
      <stop offset="60%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
  </defs>
  <rect x="40" y="380" width="160" height="18" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="65" y="360" width="110" height="20" fill="#334155" stroke="#64748b" stroke-width="1.5"/>

  <!-- Pump Base -->
  <rect x="75" y="310" width="90" height="50" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="35" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="25" y="316" width="10" height="38" rx="2" fill="#475569"/>
  <rect x="165" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="205" y="316" width="10" height="38" rx="2" fill="#475569"/>

  <!-- Multistage Barrel -->
  <rect x="85" y="150" width="70" height="160" rx="3" fill="url(#ro_casing)" stroke="#64748b" stroke-width="2"/>
  <rect x="105" y="160" width="30" height="140" rx="4" fill="#0f172a" stroke="{ring_color}" stroke-width="1.5"{fault_pulse}/>

  <!-- Flow Stream -->
  <g{stream_pulse} opacity="{fluid_opacity}">
    <circle cx="120" cy="280" r="5" fill="#00e5ff" />
    <circle cx="120" cy="240" r="6" fill="#38bdf8" />
    <circle cx="120" cy="200" r="5" fill="#67e8f9" />
    <circle cx="120" cy="160" r="4" fill="#e0f2fe" />
  </g>

  <!-- Stage Clamps -->
  <line x1="85" y1="180" x2="155" y2="180" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="210" x2="155" y2="210" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="240" x2="155" y2="240" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="270" x2="155" y2="270" stroke="#334155" stroke-width="3"/>

  <!-- Drive Motor -->
  <rect x="80" y="125" width="80" height="25" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="35" width="90" height="90" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <rect x="70" y="25" width="100" height="10" rx="3" fill="#334155"/>
  <circle cx="120" cy="18" r="8" fill="none" stroke="#64748b" stroke-width="3"/>
</svg>
"""

for dn in ["dn25", "dn50"]:
    svg_registry[f"pump-ro-high-pressure-{dn}-running-animated.svg"] = make_ro_pump(dn, "running", animated=True)
    svg_registry[f"pump-ro-high-pressure-{dn}-running-static.svg"] = make_ro_pump(dn, "running", animated=False)
    svg_registry[f"pump-ro-high-pressure-{dn}-stopped-static.svg"] = make_ro_pump(dn, "stopped", animated=False)
    svg_registry[f"pump-ro-high-pressure-{dn}-fault-animated.svg"] = make_ro_pump(dn, "fault", animated=True)

# 3. Chemical Dosing Pump Combinations
def make_dosing_pump(dn="dn15", state="running", animated=False):
    is_run = (state == "running")
    is_fault = (state == "fault")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    diaphragm_class = ' class="anim-dosing-diaphragm"' if animated and is_run else ""
    drop_class = ' class="anim-dosing-drop"' if animated and is_run else ""
    chem_opacity = "1.0" if (is_run or is_fault) else "0.15"

    css = ""
    if animated:
        if is_run:
            css = """
      @keyframes stroke-pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
      @keyframes drop-inject { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(35px); opacity: 0; } }
      .anim-dosing-diaphragm { transform-origin: 162px 187px; animation: stroke-pulse 1.2s ease-in-out infinite; }
      .anim-dosing-drop { animation: drop-inject 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
"""
        elif is_fault:
            css = """
      @keyframes fault-blink { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
      .anim-dosing-diaphragm { animation: fault-blink 0.7s infinite; }
"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 390" width="230" height="390">
  <defs>
    <style>{css}</style>
    <radialGradient id="dp_chem" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f43f5e" />
      <stop offset="70%" stop-color="#be123c" />
      <stop offset="100%" stop-color="#881337" />
    </radialGradient>
  </defs>
  <rect x="35" y="110" width="30" height="150" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="65" y="125" width="85" height="120" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <circle cx="130" cy="145" r="5" fill="{ring_color}"/>

  <!-- Liquid Head -->
  <rect x="135" y="145" width="55" height="85" rx="6" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
  <circle cx="162" cy="187" r="22" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
  <circle cx="162" cy="187" r="16" fill="url(#dp_chem)" opacity="{chem_opacity}"{diaphragm_class}/>

  <!-- Ports -->
  <rect x="152" y="230" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="148" y1="270" x2="176" y2="270" stroke="#94a3b8" stroke-width="3"/>
  <rect x="152" y="105" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="148" y1="105" x2="176" y2="105" stroke="#94a3b8" stroke-width="3"/>

  <g{drop_class} opacity="{1.0 if is_run else 0.0}">
    <ellipse cx="162" cy="285" rx="4" ry="6" fill="#f43f5e" />
  </g>
</svg>
"""

for dn in ["dn15", "dn25"]:
    svg_registry[f"pump-chemical-dosing-{dn}-running-animated.svg"] = make_dosing_pump(dn, "running", animated=True)
    svg_registry[f"pump-chemical-dosing-{dn}-running-static.svg"] = make_dosing_pump(dn, "running", animated=False)
    svg_registry[f"pump-chemical-dosing-{dn}-stopped-static.svg"] = make_dosing_pump(dn, "stopped", animated=False)
    svg_registry[f"pump-chemical-dosing-{dn}-fault-animated.svg"] = make_dosing_pump(dn, "fault", animated=True)

# 4. Submersible Sump Pump
def make_submersible_pump(dn="dn50", state="running", animated=False):
    is_run = (state == "running")
    is_fault = (state == "fault")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    bubble_class = ' class="anim-sump-bubble"' if animated and is_run else ""

    css = ""
    if animated and is_run:
        css = """
      @keyframes sump-bub { 0% { transform: translateY(0); opacity: 0.2; } 100% { transform: translateY(-40px); opacity: 0; } }
      .anim-sump-bubble { animation: sump-bub 1.4s linear infinite; }
"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 360" width="240" height="360">
  <defs>
    <style>{css}</style>
  </defs>
  <!-- Handle -->
  <path d="M 95 65 Q 120 40 145 65" fill="none" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
  <!-- Submersible Pump Body -->
  <rect x="75" y="65" width="90" height="180" rx="8" fill="#1e293b" stroke="#475569" stroke-width="3"/>
  <circle cx="120" cy="140" r="30" fill="#0f172a" stroke="{ring_color}" stroke-width="3"/>
  <circle cx="120" cy="140" r="12" fill="#38bdf8"/>

  <!-- Suction Strainer -->
  <rect x="65" y="245" width="110" height="30" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="75" y1="250" x2="75" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="90" y1="250" x2="90" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="105" y1="250" x2="105" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="120" y1="250" x2="120" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="135" y1="250" x2="135" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="150" y1="250" x2="150" y2="270" stroke="#0f172a" stroke-width="3"/>
  <line x1="165" y1="250" x2="165" y2="270" stroke="#0f172a" stroke-width="3"/>

  <!-- Discharge Riser Pipe -->
  <rect x="150" y="90" width="55" height="24" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="205" y="82" width="10" height="40" rx="2" fill="#475569"/>

  <g{bubble_class} opacity="{1.0 if is_run else 0.0}">
    <circle cx="85" cy="240" r="4" fill="#bae6fd" />
    <circle cx="155" cy="235" r="3" fill="#bae6fd" />
    <circle cx="120" cy="230" r="4.5" fill="#e0f2fe" />
  </g>
</svg>
"""

for dn in ["dn50", "dn100"]:
    svg_registry[f"pump-submersible-sump-{dn}-running-animated.svg"] = make_submersible_pump(dn, "running", animated=True)
    svg_registry[f"pump-submersible-sump-{dn}-running-static.svg"] = make_submersible_pump(dn, "running", animated=False)
    svg_registry[f"pump-submersible-sump-{dn}-stopped-static.svg"] = make_submersible_pump(dn, "stopped", animated=False)
    svg_registry[f"pump-submersible-sump-{dn}-fault-animated.svg"] = make_submersible_pump(dn, "fault", animated=True)


# ==============================================================================
# 2. ALL PROCESS EQUIPMENT (ANIMATED, FLUID STATIC, DRY STATIC)
# ==============================================================================

# Helper to register 3 states: fluid-animated, fluid-static, dry-static
def register_equipment_trio(base_name, svg_animated, svg_fluid_static, svg_dry_static):
    svg_registry[f"{base_name}-fluid-animated.svg"] = svg_animated
    svg_registry[f"{base_name}-fluid-static.svg"] = svg_fluid_static
    svg_registry[f"{base_name}-dry-static.svg"] = svg_dry_static

# --- WTP Tanker Supply ---
WTP_TANKER_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 376 328" width="376" height="328">
  <defs>
    <style>
      @keyframes hose-pulse {
        0% { stroke-dashoffset: 0; }
        100% { stroke-dashoffset: -30; }
      }
      .anim-hose { stroke-dasharray: 10 5; animation: hose-pulse 1.2s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="250" width="316" height="12" rx="3" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="50" y="90" width="220" height="120" rx="40" fill="#0284c7" stroke="#38bdf8" stroke-width="3"/>
  <ellipse cx="60" cy="150" rx="20" ry="58" fill="#0369a1" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 270 120 L 330 120 L 330 210 L 270 210 Z" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <rect x="290" y="130" width="30" height="30" rx="4" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>
  <circle cx="100" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <circle cx="160" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <circle cx="300" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <!-- Animated Hose -->
  <path d="M 160 210 Q 160 270 210 270 L 260 270" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round" class="anim-hose"/>
</svg>"""

WTP_TANKER_FLUID = WTP_TANKER_ANIM.replace('class="anim-hose"', '').replace('<style>', '<!--').replace('</style>', '-->')
WTP_TANKER_DRY = WTP_TANKER_FLUID.replace('#0284c7', '#1e293b').replace('#0369a1', '#0f172a').replace('#38bdf8', '#475569')

register_equipment_trio("wtp-tanker-supply", WTP_TANKER_ANIM, WTP_TANKER_FLUID, WTP_TANKER_DRY)


# --- WTP Rainwater Pond ---
WTP_POND_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 230" width="380" height="230">
  <defs>
    <style>
      @keyframes wave-pond {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(12px); }
      }
      .anim-pond-wave { animation: wave-pond 3s ease-in-out infinite; }
    </style>
  </defs>
  <polygon points="20,190 60,70 320,70 360,190" fill="#1c1917" stroke="#44403c" stroke-width="4"/>
  <polygon points="50,185 80,100 300,100 330,185" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <g class="anim-pond-wave">
    <path d="M 80 100 Q 135 92 190 100 T 300 100" fill="none" stroke="#67e8f9" stroke-width="3"/>
    <path d="M 90 120 Q 145 114 200 120 T 290 120" fill="none" stroke="#38bdf8" stroke-width="2" opacity="0.7"/>
  </g>
</svg>"""

WTP_POND_FLUID = WTP_POND_ANIM.replace('class="anim-pond-wave"', '').replace('<style>', '<!--').replace('</style>', '-->')
WTP_POND_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 230" width="380" height="230">
  <polygon points="20,190 60,70 320,70 360,190" fill="#1c1917" stroke="#44403c" stroke-width="4"/>
  <polygon points="50,185 80,140 300,140 330,185" fill="#292524" stroke="#44403c" stroke-width="2"/>
  <line x1="120" y1="160" x2="160" y2="165" stroke="#44403c" stroke-width="2"/>
  <line x1="220" y1="162" x2="260" y2="158" stroke="#44403c" stroke-width="2"/>
</svg>"""

register_equipment_trio("wtp-rainwater-pond", WTP_POND_ANIM, WTP_POND_FLUID, WTP_POND_DRY)


# --- WTP Multi-Grade Filter (MGF) ---
WTP_MGF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <defs>
    <style>
      @keyframes mgf-flow {
        0% { transform: translateY(0); opacity: 0.2; }
        50% { opacity: 0.9; }
        100% { transform: translateY(50px); opacity: 0.2; }
      }
      .anim-mgf { animation: mgf-flow 1.6s linear infinite; }
    </style>
  </defs>
  <!-- Legs -->
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <!-- Vessel Shell -->
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <!-- 4-Layer Bed Sight Glass -->
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="90" y="92" width="96" height="40" fill="#fef08a" opacity="0.8"/>
  <rect x="90" y="132" width="96" height="50" fill="#ca8a04" opacity="0.8"/>
  <rect x="90" y="182" width="96" height="55" fill="#854d0e" opacity="0.8"/>
  <rect x="90" y="237" width="96" height="60" fill="#475569" opacity="0.8"/>
  <!-- Downward Flow Streams -->
  <g class="anim-mgf">
    <line x1="110" y1="100" x2="110" y2="125" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="138" y1="120" x2="138" y2="145" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="166" y1="110" x2="166" y2="135" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

WTP_MGF_FLUID = WTP_MGF_ANIM.replace('class="anim-mgf"', '').replace('<style>', '<!--').replace('</style>', '-->')
WTP_MGF_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <line x1="138" y1="90" x2="138" y2="280" stroke="#475569" stroke-width="4"/>
</svg>"""

register_equipment_trio("wtp-multi-grade-filter-mgf", WTP_MGF_ANIM, WTP_MGF_FLUID, WTP_MGF_DRY)


# --- ETP Flash Mixer Tank ---
ETP_FLASH_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 318" width="300" height="318">
  <defs>
    <style>
      @keyframes spin-flash { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-flash-spin { transform-origin: 150px 240px; animation: spin-flash 0.6s linear infinite; }
    </style>
  </defs>
  <rect x="40" y="80" width="220" height="200" rx="10" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="44" y="110" width="212" height="166" rx="6" fill="#334155"/>
  <ellipse cx="150" cy="115" rx="55" ry="14" fill="#a855f7" fill-opacity="0.5"/>
  <rect x="30" y="70" width="240" height="12" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="125" y="24" width="50" height="46" rx="5" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <line x1="150" y1="70" x2="150" y2="240" stroke="#cbd5e1" stroke-width="5"/>
  <g class="anim-flash-spin">
    <ellipse cx="150" cy="240" rx="42" ry="8" fill="#a855f7" />
    <ellipse cx="150" cy="240" rx="8" ry="42" fill="#d8b4fe" />
    <circle cx="150" cy="240" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
  </g>
</svg>"""

ETP_FLASH_FLUID = ETP_FLASH_ANIM.replace('class="anim-flash-spin"', '').replace('<style>', '<!--').replace('</style>', '-->')
ETP_FLASH_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 318" width="300" height="318">
  <rect x="40" y="80" width="220" height="200" rx="10" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="30" y="70" width="240" height="12" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="125" y="24" width="50" height="46" rx="5" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <line x1="150" y1="70" x2="150" y2="240" stroke="#64748b" stroke-width="5"/>
  <ellipse cx="150" cy="240" rx="42" ry="8" fill="#475569" />
</svg>"""

register_equipment_trio("etp-flash-mixer-tank", ETP_FLASH_ANIM, ETP_FLASH_FLUID, ETP_FLASH_DRY)


# --- ETP Flocculator Tank ---
ETP_FLOC_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 318" width="360" height="318">
  <defs>
    <style>
      @keyframes paddle-rock-1 { 0%, 100% { transform: scaleX(1); } 50% { transform: scaleX(-1); } }
      @keyframes paddle-rock-2 { 0%, 100% { transform: scaleX(-1); } 50% { transform: scaleX(1); } }
      .anim-floc-p1 { transform-origin: 120px 200px; animation: paddle-rock-1 4s ease-in-out infinite; }
      .anim-floc-p2 { transform-origin: 240px 200px; animation: paddle-rock-2 4s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="90" width="300" height="190" rx="10" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="34" y="120" width="292" height="156" rx="6" fill="#1d4ed8" fill-opacity="0.8"/>
  <rect x="20" y="80" width="320" height="14" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="100" y="42" width="40" height="38" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <rect x="220" y="42" width="40" height="38" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <line x1="120" y1="80" x2="120" y2="240" stroke="#cbd5e1" stroke-width="4"/>
  <line x1="240" y1="80" x2="240" y2="240" stroke="#cbd5e1" stroke-width="4"/>
  <g class="anim-floc-p1">
    <rect x="80" y="160" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="80" y="210" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
  </g>
  <g class="anim-floc-p2">
    <rect x="200" y="160" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="200" y="210" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
  </g>
</svg>"""

ETP_FLOC_FLUID = ETP_FLOC_ANIM.replace('class="anim-floc-p1"', '').replace('class="anim-floc-p2"', '').replace('<style>', '<!--').replace('</style>', '-->')
ETP_FLOC_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 318" width="360" height="318">
  <rect x="30" y="90" width="300" height="190" rx="10" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="20" y="80" width="320" height="14" fill="#334155" stroke="#475569" stroke-width="2"/>
  <line x1="120" y1="80" x2="120" y2="240" stroke="#64748b" stroke-width="4"/>
  <line x1="240" y1="80" x2="240" y2="240" stroke="#64748b" stroke-width="4"/>
  <rect x="80" y="180" width="80" height="16" rx="3" fill="#475569"/>
  <rect x="200" y="180" width="80" height="16" rx="3" fill="#475569"/>
</svg>"""

register_equipment_trio("etp-flocculator-tank", ETP_FLOC_ANIM, ETP_FLOC_FLUID, ETP_FLOC_DRY)


# --- ETP Lamella Settler ---
ETP_LAMELLA_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 252" width="300" height="252">
  <defs>
    <style>
      @keyframes floc-slide { 0% { transform: translate(0, 0); opacity: 0.1; } 50% { opacity: 0.8; } 100% { transform: translate(-25px, 35px); opacity: 0.1; } }
      .anim-floc-slide { animation: floc-slide 2s linear infinite; }
    </style>
  </defs>
  <polygon points="30,40 270,40 270,140 180,220 120,220 30,140" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <polygon points="34,60 266,60 266,138 178,216 122,216 34,138" fill="#0284c7" fill-opacity="0.8"/>
  <!-- 60 Degree Lamella Plate Pack -->
  <line x1="70" y1="130" x2="120" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="95" y1="130" x2="145" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="120" y1="130" x2="170" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="145" y1="130" x2="195" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="170" y1="130" x2="220" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <g class="anim-floc-slide">
    <circle cx="140" cy="75" r="3" fill="#78350f"/>
    <circle cx="165" cy="85" r="3.5" fill="#78350f"/>
    <circle cx="190" cy="95" r="3" fill="#78350f"/>
  </g>
</svg>"""

ETP_LAMELLA_FLUID = ETP_LAMELLA_ANIM.replace('class="anim-floc-slide"', '').replace('<style>', '<!--').replace('</style>', '-->')
ETP_LAMELLA_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 252" width="300" height="252">
  <polygon points="30,40 270,40 270,140 180,220 120,220 30,140" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="70" y1="130" x2="120" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="95" y1="130" x2="145" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="120" y1="130" x2="170" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="145" y1="130" x2="195" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="170" y1="130" x2="220" y2="60" stroke="#475569" stroke-width="4"/>
</svg>"""

register_equipment_trio("etp-lamella-tube-settler", ETP_LAMELLA_ANIM, ETP_LAMELLA_FLUID, ETP_LAMELLA_DRY)


# --- ETP DAF Tank ---
ETP_DAF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="340" height="240">
  <defs>
    <style>
      @keyframes micro-bub { 0% { transform: translateY(0); opacity: 0.1; } 50% { opacity: 0.9; } 100% { transform: translateY(-70px); opacity: 0; } }
      .anim-micro-bub { animation: micro-bub 1.8s linear infinite; }
    </style>
  </defs>
  <polygon points="30,60 270,60 270,180 230,210 70,210 30,180" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <polygon points="34,80 266,80 266,178 228,206 72,206 34,178" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="34" y="70" width="232" height="16" fill="#854d0e" fill-opacity="0.8"/>
  <polygon points="266,70 310,70 310,120 266,86" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <line x1="80" y1="190" x2="220" y2="190" stroke="#38bdf8" stroke-width="4"/>
  <g class="anim-micro-bub">
    <circle cx="100" cy="180" r="2" fill="#e0f2fe"/>
    <circle cx="115" cy="165" r="2.5" fill="#bae6fd"/>
    <circle cx="130" cy="180" r="1.5" fill="#e0f2fe"/>
    <circle cx="145" cy="160" r="2" fill="#bae6fd"/>
    <circle cx="160" cy="175" r="2.5" fill="#e0f2fe"/>
    <circle cx="190" cy="180" r="2" fill="#e0f2fe"/>
  </g>
</svg>"""

ETP_DAF_FLUID = ETP_DAF_ANIM.replace('class="anim-micro-bub"', '').replace('<style>', '<!--').replace('</style>', '-->')
ETP_DAF_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="340" height="240">
  <polygon points="30,60 270,60 270,180 230,210 70,210 30,180" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <polygon points="266,70 310,70 310,120 266,86" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""

register_equipment_trio("etp-daf-flotation-tank", ETP_DAF_ANIM, ETP_DAF_FLUID, ETP_DAF_DRY)


# --- ETP Sludge Filter Press ---
ETP_PRESS_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260" width="340" height="260">
  <defs>
    <style>
      @keyframes press-drip { 0% { transform: translateY(0); opacity: 0.9; } 100% { transform: translateY(35px); opacity: 0; } }
      .anim-press-drip { animation: press-drip 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
    </style>
  </defs>
  <rect x="25" y="200" width="290" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="60" width="24" height="145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="275" y="60" width="24" height="145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="64" y1="80" x2="275" y2="80" stroke="#94a3b8" stroke-width="6"/>
  <line x1="64" y1="180" x2="275" y2="180" stroke="#94a3b8" stroke-width="6"/>
  <!-- Clamped Recessed Plate Pack -->
  <g fill="#475569" stroke="#1e293b" stroke-width="1.5">
    <rect x="75" y="85" width="8" height="90" rx="1"/>
    <rect x="85" y="85" width="8" height="90" rx="1"/>
    <rect x="95" y="85" width="8" height="90" rx="1"/>
    <rect x="105" y="85" width="8" height="90" rx="1"/>
    <rect x="115" y="85" width="8" height="90" rx="1"/>
    <rect x="125" y="85" width="8" height="90" rx="1"/>
    <rect x="135" y="85" width="8" height="90" rx="1"/>
    <rect x="145" y="85" width="8" height="90" rx="1"/>
    <rect x="155" y="85" width="8" height="90" rx="1"/>
    <rect x="165" y="85" width="8" height="90" rx="1"/>
    <rect x="175" y="85" width="8" height="90" rx="1"/>
    <rect x="185" y="85" width="8" height="90" rx="1"/>
  </g>
  <!-- Hydraulic Ram -->
  <rect x="200" y="115" width="75" height="30" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <g class="anim-press-drip">
    <circle cx="100" cy="190" r="3" fill="#38bdf8"/>
    <circle cx="140" cy="190" r="3" fill="#38bdf8"/>
    <circle cx="170" cy="190" r="3" fill="#38bdf8"/>
  </g>
</svg>"""

ETP_PRESS_FLUID = ETP_PRESS_ANIM.replace('class="anim-press-drip"', '').replace('<style>', '<!--').replace('</style>', '-->')
ETP_PRESS_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260" width="340" height="260">
  <rect x="25" y="200" width="290" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="60" width="24" height="145" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="275" y="60" width="24" height="145" fill="#334155" stroke="#475569" stroke-width="2"/>
  <line x1="64" y1="80" x2="275" y2="80" stroke="#64748b" stroke-width="6"/>
  <line x1="64" y1="180" x2="275" y2="180" stroke="#64748b" stroke-width="6"/>
  <!-- Separated open plates -->
  <g fill="#334155" stroke="#1e293b" stroke-width="1.5">
    <rect x="75" y="85" width="8" height="90" rx="1"/>
    <rect x="95" y="85" width="8" height="90" rx="1"/>
    <rect x="115" y="85" width="8" height="90" rx="1"/>
    <rect x="135" y="85" width="8" height="90" rx="1"/>
    <rect x="155" y="85" width="8" height="90" rx="1"/>
  </g>
  <rect x="210" y="115" width="65" height="30" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""

register_equipment_trio("etp-sludge-filter-press", ETP_PRESS_ANIM, ETP_PRESS_FLUID, ETP_PRESS_DRY)


# --- RO Membrane Skid ---
RO_SKID_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 280" width="350" height="280">
  <defs>
    <style>
      @keyframes ro-flow { 0% { transform: translateX(0); opacity: 0.2; } 50% { opacity: 0.9; } 100% { transform: translateX(50px); opacity: 0.2; } }
      .anim-ro-flow { animation: ro-flow 1.5s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="235" width="290" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="60" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="278" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <!-- 3 Vessels -->
  <rect x="75" y="65" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="75" y="115" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="75" y="165" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="110" y="77" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="127" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="177" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <g class="anim-ro-flow">
    <circle cx="130" cy="83" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="83" r="3.5" fill="#38bdf8"/>
    <circle cx="130" cy="133" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="133" r="3.5" fill="#38bdf8"/>
    <circle cx="130" cy="183" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="183" r="3.5" fill="#38bdf8"/>
  </g>
  <line x1="66" y1="83" x2="66" y2="183" stroke="#0284c7" stroke-width="6"/>
  <line x1="284" y1="83" x2="284" y2="183" stroke="#10b981" stroke-width="6"/>
</svg>"""

RO_SKID_FLUID = RO_SKID_ANIM.replace('class="anim-ro-flow"', '').replace('<style>', '<!--').replace('</style>', '-->')
RO_SKID_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 280" width="350" height="280">
  <rect x="30" y="235" width="290" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="60" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="278" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="65" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="115" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="165" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>"""

register_equipment_trio("ro-membrane-skid", RO_SKID_ANIM, RO_SKID_FLUID, RO_SKID_DRY)


# --- UF Skid ---
UF_SKID_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 328 344" width="328" height="344">
  <defs>
    <style>
      @keyframes uf-flow { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(40px); opacity: 0.2; } }
      .anim-uf { animation: uf-flow 1.4s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="300" width="268" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="50" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="40" y="275" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="58" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="116" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="174" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="232" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g class="anim-uf">
    <line x1="77" y1="120" x2="77" y2="145" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="135" y1="140" x2="135" y2="165" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
    <line x1="193" y1="125" x2="193" y2="150" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="251" y1="145" x2="251" y2="170" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  </g>
</svg>"""

UF_SKID_FLUID = UF_SKID_ANIM.replace('class="anim-uf"', '').replace('<style>', '<!--').replace('</style>', '-->')
UF_SKID_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 328 344" width="328" height="344">
  <rect x="30" y="300" width="268" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="50" width="248" height="18" rx="4" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="275" width="248" height="18" rx="4" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="58" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="116" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="174" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="232" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""

register_equipment_trio("uf-ultrafiltration-skid", UF_SKID_ANIM, UF_SKID_FLUID, UF_SKID_DRY)


# --- Micron Cartridge Filter ---
MICRON_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 272 360" width="272" height="360">
  <defs>
    <style>
      @keyframes m-flow { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.9; } }
      .anim-m-flow { animation: m-flow 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="56" y="80" width="160" height="230" rx="20" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="96" y="100" width="80" height="190" rx="4" fill="#38bdf8" stroke="#0284c7" stroke-width="2" class="anim-m-flow"/>
  <line x1="136" y1="100" x2="136" y2="290" stroke="#bae6fd" stroke-width="3"/>
  <!-- Swing bolts -->
  <circle cx="56" cy="80" r="5" fill="#94a3b8"/>
  <circle cx="216" cy="80" r="5" fill="#94a3b8"/>
</svg>"""

MICRON_FLUID = MICRON_ANIM.replace('class="anim-m-flow"', '').replace('<style>', '<!--').replace('</style>', '-->')
MICRON_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 272 360" width="272" height="360">
  <rect x="56" y="80" width="160" height="230" rx="20" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="96" y="100" width="80" height="190" rx="4" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <line x1="136" y1="100" x2="136" y2="290" stroke="#475569" stroke-width="3"/>
</svg>"""

register_equipment_trio("micron-cartridge-filter", MICRON_ANIM, MICRON_FLUID, MICRON_DRY)


# --- HVAC Cooling Tower ---
CT_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 336 368" width="336" height="368">
  <defs>
    <style>
      @keyframes spin-ct { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      @keyframes ct-rain { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.9; } 100% { transform: translateY(40px); opacity: 0.1; } }
      .anim-ct-fan { transform-origin: 168px 42px; animation: spin-ct 0.9s linear infinite; }
      .anim-ct-rain { animation: ct-rain 1.1s linear infinite; }
    </style>
  </defs>
  <line x1="50" y1="300" x2="50" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="286" y1="300" x2="286" y2="345" stroke="#475569" stroke-width="6"/>
  <rect x="40" y="270" width="256" height="35" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="52" y="140" width="232" height="120" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <g class="anim-ct-rain">
    <line x1="80" y1="150" x2="80" y2="168" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="120" y1="160" x2="120" y2="178" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="168" y1="150" x2="168" y2="172" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="210" y1="165" x2="210" y2="183" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="250" y1="152" x2="250" y2="170" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
  </g>
  <path d="M 100 105 L 120 40 L 216 40 L 236 105 Z" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <g class="anim-ct-fan">
    <ellipse cx="168" cy="42" rx="42" ry="7" fill="#67e8f9" fill-opacity="0.9" />
    <ellipse cx="168" cy="42" rx="7" ry="42" fill="#38bdf8" fill-opacity="0.9" />
    <circle cx="168" cy="42" r="9" fill="#0f172a" stroke="#bae6fd" stroke-width="2"/>
  </g>
</svg>"""

CT_FLUID = CT_ANIM.replace('class="anim-ct-fan"', '').replace('class="anim-ct-rain"', '').replace('<style>', '<!--').replace('</style>', '-->')
CT_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 336 368" width="336" height="368">
  <line x1="50" y1="300" x2="50" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="286" y1="300" x2="286" y2="345" stroke="#475569" stroke-width="6"/>
  <rect x="40" y="270" width="256" height="35" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="52" y="140" width="232" height="120" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <path d="M 100 105 L 120 40 L 216 40 L 236 105 Z" fill="#1e293b" stroke="#475569" stroke-width="3"/>
</svg>"""

register_equipment_trio("hvac-cooling-tower", CT_ANIM, CT_FLUID, CT_DRY)


# --- STP Collection Tank ---
STP_COLL_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 180" width="390" height="180">
  <defs>
    <style>
      @keyframes coll-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(10px); } }
      @keyframes coll-bub { 0% { transform: translateY(0); opacity: 0.1; } 50% { opacity: 0.8; } 100% { transform: translateY(-50px); opacity: 0; } }
      .anim-coll-wave { animation: coll-wave 2.8s ease-in-out infinite; }
      .anim-coll-bub { animation: coll-bub 2s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="330" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="34" y="65" width="322" height="82" rx="6" fill="#334155"/>
  <g class="anim-coll-wave">
    <path d="M 34 65 Q 90 58 146 65 T 258 65 T 356 65" fill="none" stroke="#64748b" stroke-width="3"/>
  </g>
  <g class="anim-coll-bub">
    <circle cx="80" cy="130" r="3.5" fill="#94a3b8"/>
    <circle cx="160" cy="135" r="4" fill="#94a3b8"/>
    <circle cx="240" cy="125" r="3" fill="#94a3b8"/>
  </g>
</svg>"""

STP_COLL_FLUID = STP_COLL_ANIM.replace('class="anim-coll-wave"', '').replace('class="anim-coll-bub"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_COLL_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 180" width="390" height="180">
  <rect x="30" y="30" width="330" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
</svg>"""

register_equipment_trio("stp-collection-tank", STP_COLL_ANIM, STP_COLL_FLUID, STP_COLL_DRY)


# --- STP MBBR Aeration Bio-Reactor ---
STP_MBBR_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes bubble-rise { 0% { transform: translateY(0); opacity: 0.1; } 50% { opacity: 0.8; } 100% { transform: translateY(-70px); opacity: 0; } }
      @keyframes carrier-tumble { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-12px) rotate(180deg); } }
      @keyframes wave-sway { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(10px); } }
      .anim-bubbles { animation: bubble-rise 2s linear infinite; }
      .anim-carriers { animation: carrier-tumble 3.5s ease-in-out infinite; }
      .anim-wave { animation: wave-sway 2.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="60" width="254" height="87" rx="6" fill="#0e7490" fill-opacity="0.9"/>
  <g class="anim-wave">
    <path d="M 33 60 Q 65 52 97 60 T 161 60 T 225 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
  <g class="anim-bubbles">
    <circle cx="75" cy="125" r="3.5" fill="#e0f2fe"/>
    <circle cx="115" cy="120" r="3" fill="#e0f2fe"/>
    <circle cx="155" cy="125" r="3" fill="#e0f2fe"/>
    <circle cx="195" cy="120" r="3.5" fill="#e0f2fe"/>
    <circle cx="235" cy="125" r="3" fill="#e0f2fe"/>
  </g>
  <g class="anim-carriers">
    <circle cx="100" cy="85" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="140" cy="95" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="180" cy="80" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="220" cy="90" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
  </g>
</svg>"""

STP_MBBR_FLUID = STP_MBBR_ANIM.replace('class="anim-bubbles"', '').replace('class="anim-carriers"', '').replace('class="anim-wave"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_MBBR_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="50" y1="135" x2="270" y2="135" stroke="#475569" stroke-width="4"/>
</svg>"""

register_equipment_trio("stp-mbbr-aeration-tank", STP_MBBR_ANIM, STP_MBBR_FLUID, STP_MBBR_DRY)


# --- STP Secondary Clarifier ---
STP_CLAR_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 192" width="320" height="192">
  <defs>
    <style>
      @keyframes bridge-sweep { 0%, 100% { transform: scaleX(1); } 50% { transform: scaleX(-1); } }
      .anim-scraper { transform-origin: 160px 48px; animation: bridge-sweep 6s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="40" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <polygon points="30,70 145,170 175,170 290,70" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>
  <polygon points="33,70 147,167 173,167 287,70" fill="#0369a1" fill-opacity="0.85"/>
  <rect x="150" y="16" width="20" height="24" rx="3" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g class="anim-scraper">
    <line x1="160" y1="36" x2="160" y2="140" stroke="#94a3b8" stroke-width="4"/>
    <line x1="160" y1="140" x2="230" y2="90" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="180" y1="126" x2="180" y2="136" stroke="#94a3b8" stroke-width="2"/>
    <line x1="200" y1="112" x2="200" y2="122" stroke="#94a3b8" stroke-width="2"/>
  </g>
</svg>"""

STP_CLAR_FLUID = STP_CLAR_ANIM.replace('class="anim-scraper"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_CLAR_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 192" width="320" height="192">
  <rect x="30" y="30" width="260" height="40" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <polygon points="30,70 145,170 175,170 290,70" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>
  <rect x="150" y="16" width="20" height="24" rx="3" fill="#334155" stroke="#475569" stroke-width="2"/>
  <line x1="160" y1="36" x2="160" y2="140" stroke="#475569" stroke-width="4"/>
</svg>"""

register_equipment_trio("stp-secondary-clarifier", STP_CLAR_ANIM, STP_CLAR_FLUID, STP_CLAR_DRY)


# --- STP Sludge Holding Tank ---
STP_SLUDGE_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 148" width="270" height="148">
  <defs>
    <style>
      @keyframes sludge-wave { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }
      .anim-sludge { animation: sludge-wave 2s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="20" y="20" width="230" height="25" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <polygon points="20,45 110,128 160,128 250,45" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <polygon points="23,45 112,125 158,125 247,45" fill="#78350f" fill-opacity="0.9" class="anim-sludge"/>
</svg>"""

STP_SLUDGE_FLUID = STP_SLUDGE_ANIM.replace('class="anim-sludge"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_SLUDGE_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 148" width="270" height="148">
  <rect x="20" y="20" width="230" height="25" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <polygon points="20,45 110,128 160,128 250,45" fill="#0f172a" stroke="#475569" stroke-width="2"/>
</svg>"""

register_equipment_trio("stp-sludge-holding-tank", STP_SLUDGE_ANIM, STP_SLUDGE_FLUID, STP_SLUDGE_DRY)


# --- STP Filter Feed Tank ---
STP_FFT_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes fft-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(8px); } }
      .anim-fft { animation: fft-wave 2.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="65" width="254" height="82" rx="6" fill="#0284c7" fill-opacity="0.8"/>
  <g class="anim-fft">
    <path d="M 33 65 Q 96 58 160 65 T 287 65" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
</svg>"""

STP_FFT_FLUID = STP_FFT_ANIM.replace('class="anim-fft"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_FFT_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
</svg>"""

register_equipment_trio("stp-filter-feed-tank", STP_FFT_ANIM, STP_FFT_FLUID, STP_FFT_DRY)


# --- STP Pressure Sand Filter (PSF) ---
STP_PSF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
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
  <rect x="90" y="92" width="96" height="60" fill="#fef08a" opacity="0.8"/>
  <rect x="90" y="152" width="96" height="70" fill="#ca8a04" opacity="0.8"/>
  <rect x="90" y="222" width="96" height="75" fill="#475569" opacity="0.8"/>
  <g class="anim-psf">
    <line x1="120" y1="100" x2="120" y2="125" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="156" y1="110" x2="156" y2="135" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

STP_PSF_FLUID = STP_PSF_ANIM.replace('class="anim-psf"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_PSF_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

register_equipment_trio("stp-pressure-sand-filter-psf", STP_PSF_ANIM, STP_PSF_FLUID, STP_PSF_DRY)


# --- STP Activated Carbon Filter (ACF) ---
STP_ACF_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
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
  <rect x="90" y="92" width="96" height="160" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <g class="anim-acf">
    <line x1="120" y1="100" x2="120" y2="125" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="156" y1="110" x2="156" y2="135" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

STP_ACF_FLUID = STP_ACF_ANIM.replace('class="anim-acf"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_ACF_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

register_equipment_trio("stp-activated-carbon-filter-acf", STP_ACF_ANIM, STP_ACF_FLUID, STP_ACF_DRY)


# --- STP Water Softener Column ---
STP_SOFTCOL_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 324" width="270" height="324">
  <defs>
    <style>
      @keyframes resin-flow { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(35px); opacity: 0.2; } }
      .anim-resin { animation: resin-flow 1.5s linear infinite; }
    </style>
  </defs>
  <rect x="50" y="50" width="170" height="230" rx="28" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="85" y="70" width="100" height="190" rx="6" fill="#f59e0b" fill-opacity="0.8"/>
  <g class="anim-resin">
    <circle cx="115" cy="110" r="3" fill="#00e5ff"/>
    <circle cx="155" cy="120" r="3.5" fill="#38bdf8"/>
  </g>
</svg>"""

STP_SOFTCOL_FLUID = STP_SOFTCOL_ANIM.replace('class="anim-resin"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_SOFTCOL_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 324" width="270" height="324">
  <rect x="50" y="50" width="170" height="230" rx="28" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="85" y="70" width="100" height="190" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

register_equipment_trio("stp-water-softener-column", STP_SOFTCOL_ANIM, STP_SOFTCOL_FLUID, STP_SOFTCOL_DRY)


# --- STP Treated Water Tank ---
STP_TWT_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 176" width="320" height="176">
  <defs>
    <style>
      @keyframes twt-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(8px); } }
      .anim-twt { animation: twt-wave 2.4s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="116" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="60" width="254" height="83" rx="6" fill="#0284c7" fill-opacity="0.85"/>
  <g class="anim-twt">
    <path d="M 33 60 Q 96 52 160 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
  <line x1="50" y1="20" x2="50" y2="85" stroke="#94a3b8" stroke-width="5"/>
  <polygon points="45,85 55,85 50,95" fill="#38bdf8"/>
</svg>"""

STP_TWT_FLUID = STP_TWT_ANIM.replace('class="anim-twt"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_TWT_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 176" width="320" height="176">
  <rect x="30" y="30" width="260" height="116" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="50" y1="20" x2="50" y2="85" stroke="#64748b" stroke-width="5"/>
</svg>"""

register_equipment_trio("stp-treated-water-tank", STP_TWT_ANIM, STP_TWT_FLUID, STP_TWT_DRY)


# --- STP Soft Water Tank ---
STP_SWT_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 176" width="320" height="176">
  <defs>
    <style>
      @keyframes swt-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(8px); } }
      .anim-swt { animation: swt-wave 2.4s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="116" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="60" width="254" height="83" rx="6" fill="#0284c7" fill-opacity="0.85"/>
  <g class="anim-swt">
    <path d="M 33 60 Q 96 52 160 60 T 287 60" fill="none" stroke="#38bdf8" stroke-width="3"/>
  </g>
</svg>"""

STP_SWT_FLUID = STP_SWT_ANIM.replace('class="anim-swt"', '').replace('<style>', '<!--').replace('</style>', '-->')
STP_SWT_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 176" width="320" height="176">
  <rect x="30" y="30" width="260" height="116" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
</svg>"""

register_equipment_trio("stp-soft-water-tank", STP_SWT_ANIM, STP_SWT_FLUID, STP_SWT_DRY)


# --- Facility Commercial Building ---
svg_registry["facility-commercial-building-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 368" width="240" height="368">
  <rect x="30" y="330" width="180" height="14" rx="3" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="40" y="50" width="160" height="280" rx="4" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <!-- Windows -->
  <g fill="#0284c7" fill-opacity="0.4" stroke="#334155" stroke-width="1.5">
    <rect x="55" y="70" width="25" height="35" rx="2"/>
    <rect x="90" y="70" width="25" height="35" rx="2"/>
    <rect x="125" y="70" width="25" height="35" rx="2"/>
    <rect x="160" y="70" width="25" height="35" rx="2"/>
    <rect x="55" y="120" width="25" height="35" rx="2"/>
    <rect x="90" y="120" width="25" height="35" rx="2"/>
    <rect x="125" y="120" width="25" height="35" rx="2"/>
    <rect x="160" y="120" width="25" height="35" rx="2"/>
    <rect x="55" y="170" width="25" height="35" rx="2"/>
    <rect x="90" y="170" width="25" height="35" rx="2"/>
    <rect x="125" y="170" width="25" height="35" rx="2"/>
    <rect x="160" y="170" width="25" height="35" rx="2"/>
    <rect x="55" y="220" width="25" height="35" rx="2"/>
    <rect x="90" y="220" width="25" height="35" rx="2"/>
    <rect x="125" y="220" width="25" height="35" rx="2"/>
    <rect x="160" y="220" width="25" height="35" rx="2"/>
  </g>
</svg>"""


# ==============================================================================
# 3. SCADA BLOWERS, INSTRUMENTS & VALVES
# ==============================================================================

# Blower
svg_registry["scada-blower-running-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 264" width="264" height="264">
  <defs>
    <style>
      @keyframes spin-bl { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-bl { transform-origin: 132px 132px; animation: spin-bl 0.8s linear infinite; }
    </style>
  </defs>
  <rect x="66" y="210" width="132" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <circle cx="132" cy="132" r="70" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
  <circle cx="132" cy="132" r="58" fill="#0f172a" stroke="#10b981" stroke-width="3" stroke-dasharray="3 3"/>
  <g class="anim-bl">
    <path d="M 132 132 Q 120 100 132 86 Q 140 100 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 155 110 165 100 Q 155 125 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 164 120 178 132 Q 164 140 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 155 155 165 164 Q 140 155 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 120 164 132 178 Q 140 164 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 110 155 100 165 Q 110 140 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 100 120 86 132 Q 100 140 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 110 110 100 100 Q 125 110 132 132 Z" fill="#38bdf8" />
    <circle cx="132" cy="132" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  </g>
</svg>"""

svg_registry["scada-blower-running-static.svg"] = svg_registry["scada-blower-running-animated.svg"].replace('class="anim-bl"', '').replace('<style>', '<!--').replace('</style>', '-->')
svg_registry["scada-blower-stopped-static.svg"] = svg_registry["scada-blower-running-static.svg"].replace('#10b981', '#475569').replace('#67e8f9', '#64748b').replace('#38bdf8', '#475569')

# UV Light
svg_registry["scada-uv-light-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 344 208" width="344" height="208">
  <defs>
    <style>
      @keyframes uv-glow { 0%, 100% { opacity: 0.45; } 50% { opacity: 1; } }
      .anim-uv-core { animation: uv-glow 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="52" y="64" width="240" height="80" rx="8" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <rect x="80" y="78" width="184" height="52" rx="6" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <rect x="90" y="99" width="164" height="10" rx="5" fill="#c084fc" class="anim-uv-core"/>
</svg>"""

svg_registry["scada-uv-light-active-static.svg"] = svg_registry["scada-uv-light-active-animated.svg"].replace('class="anim-uv-core"', '').replace('<style>', '<!--').replace('</style>', '-->')
svg_registry["scada-uv-light-inactive-static.svg"] = svg_registry["scada-uv-light-active-static.svg"].replace('#a855f7', '#475569').replace('#c084fc', '#334155')

# Solenoid Valve
svg_registry["scada-water-solenoid-valve-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <style>
      @keyframes v-flow { 0% { transform: translateX(0); opacity: 0.2; } 50% { opacity: 1; } 100% { transform: translateX(30px); opacity: 0.2; } }
      .anim-v-flow { animation: v-flow 1.4s linear infinite; }
    </style>
  </defs>
  <polygon points="50,90 120,120 50,150" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <polygon points="190,90 120,120 190,150" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <circle cx="120" cy="120" r="32" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="120" cy="120" r="24" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  <rect x="105" y="45" width="30" height="45" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <g class="anim-v-flow">
    <polygon points="85,120 75,115 75,125" fill="#38bdf8"/>
    <polygon points="155,120 145,115 145,125" fill="#38bdf8"/>
  </g>
</svg>"""

svg_registry["scada-water-solenoid-valve-active-static.svg"] = svg_registry["scada-water-solenoid-valve-active-animated.svg"].replace('class="anim-v-flow"', '').replace('<style>', '<!--').replace('</style>', '-->')
svg_registry["scada-water-solenoid-valve-closed-static.svg"] = svg_registry["scada-water-solenoid-valve-active-static.svg"].replace('#10b981', '#ef4444').replace('#38bdf8', '#475569')

# Clarifier Underflow Valve
svg_registry["scada-clarifier-valve-active-animated.svg"] = svg_registry["scada-water-solenoid-valve-active-animated.svg"]
svg_registry["scada-clarifier-valve-active-static.svg"] = svg_registry["scada-water-solenoid-valve-active-static.svg"]
svg_registry["scada-clarifier-valve-closed-static.svg"] = svg_registry["scada-water-solenoid-valve-closed-static.svg"]

# Multiport Valve
svg_registry["scada-acf-multiport-valve-block-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 324 296" width="324" height="296">
  <defs>
    <style>
      @keyframes mp-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-mp { transform-origin: 162px 148px; animation: mp-spin 6s linear infinite; }
    </style>
  </defs>
  <rect x="100" y="86" width="124" height="124" rx="14" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
  <circle cx="162" cy="148" r="44" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  <g class="anim-mp">
    <circle cx="162" cy="120" r="6" fill="#38bdf8"/>
    <circle cx="190" cy="148" r="6" fill="#38bdf8"/>
    <circle cx="162" cy="176" r="6" fill="#38bdf8"/>
    <circle cx="134" cy="148" r="6" fill="#38bdf8"/>
  </g>
</svg>"""

svg_registry["scada-acf-multiport-valve-block-static.svg"] = svg_registry["scada-acf-multiport-valve-block-active-animated.svg"].replace('class="anim-mp"', '').replace('<style>', '<!--').replace('</style>', '-->')

# Pressure Gauge
svg_registry["scada-pressure-gauge-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 304 192" width="304" height="192">
  <defs>
    <style>
      @keyframes needle-oscillate { 0%, 100% { transform: rotate(-35deg); } 50% { transform: rotate(-25deg); } }
      .anim-needle { transform-origin: 152px 95px; animation: needle-oscillate 1.6s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="144" y="145" width="16" height="35" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <circle cx="152" cy="95" r="60" fill="#334155" stroke="#94a3b8" stroke-width="3"/>
  <circle cx="152" cy="95" r="50" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <path d="M 115 115 A 42 42 0 1 1 189 115" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <path d="M 130 65 A 42 42 0 0 1 174 65" fill="none" stroke="#10b981" stroke-width="4"/>
  <g class="anim-needle">
    <line x1="152" y1="95" x2="152" y2="62" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
    <circle cx="152" cy="95" r="7" fill="#ef4444"/>
  </g>
</svg>"""

svg_registry["scada-pressure-gauge-static.svg"] = svg_registry["scada-pressure-gauge-active-animated.svg"].replace('class="anim-needle"', '').replace('<style>', '<!--').replace('</style>', '-->')


# ==============================================================================
# WRITE ALL SVGS INTO SINGLE DIRECTORY AND VERIFY
# ==============================================================================

print(f"Generating {len(svg_registry)} total pure-graphic SVG combinations into single folder: {OUT_DIR}...")
for fname, content in svg_registry.items():
    if "<text" in content.lower():
        raise ValueError(f"Strict rule violated: <text> tag found in {fname}")
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Successfully generated all {len(svg_registry)} SVGs directly in {OUT_DIR}!")
