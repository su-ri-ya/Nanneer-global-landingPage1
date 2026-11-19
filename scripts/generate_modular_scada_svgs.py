import os

OUT_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
os.makedirs(OUT_DIR, exist_ok=True)

svgs = {}

# ==============================================================================
# 1. PUMPS (MODULAR WITH CONNECTION SIZES, FLOW DIRECTIONS & STATES)
# ==============================================================================

def make_centrifugal(dn="dn50", direction="l2r", state="running", animated=False):
    cfg = {
        "dn25": {"pw": 16, "ph": 16, "fw": 6, "fh": 26},
        "dn50": {"pw": 24, "ph": 24, "fw": 8, "fh": 36},
        "dn100": {"pw": 34, "ph": 34, "fw": 12, "fh": 48},
    }[dn]

    if state == "running":
        ring_color = "#10b981"
        fluid_fill = "url(#cp_fluid)"
        blade_color = "#38bdf8"
        blade_stroke = "#bae6fd"
    elif state == "fault":
        ring_color = "#ef4444"
        fluid_fill = "#450a0a"
        blade_color = "#f87171"
        blade_stroke = "#fca5a5"
    else:  # stopped
        ring_color = "#475569"
        fluid_fill = "#0f172a"
        blade_color = "#64748b"
        blade_stroke = "#94a3b8"

    css = ""
    if animated:
        if state == "running":
            css = """
      @keyframes spin-impeller { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      @keyframes flow-glow { 0%, 100% { opacity: 0.35; r: 16px; } 50% { opacity: 0.85; r: 24px; } }
      .anim-impeller { transform-origin: 150px 132px; animation: spin-impeller 1.8s linear infinite; }
      .anim-flow { animation: flow-glow 2s ease-in-out infinite; }
"""
        elif state == "fault":
            css = """
      @keyframes alert-pulse { 0%, 100% { stroke-opacity: 0.3; stroke-width: 3px; } 50% { stroke-opacity: 1; stroke-width: 6px; } }
      .anim-fault { animation: alert-pulse 0.9s ease-in-out infinite; }
"""

    impeller_class = ' class="anim-impeller"' if animated and state == "running" else ""
    flow_class = ' class="anim-flow"' if animated and state == "running" else ""
    ring_class = ' class="anim-fault"' if animated and state == "fault" else ""

    pw, ph, fw, fh = cfg["pw"], cfg["ph"], cfg["fw"], cfg["fh"]
    if direction == "l2r":
        suction = f'<rect x="{84 - pw}" y="{132 - ph/2}" width="{pw}" height="{ph}" fill="#1e293b" stroke="#475569" stroke-width="2"/><rect x="{84 - pw - fw}" y="{132 - fh/2}" width="{fw}" height="{fh}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        discharge = f'<rect x="{150 - ph/2}" y="{66 - pw}" width="{ph}" height="{pw}" fill="#1e293b" stroke="#475569" stroke-width="2"/><rect x="{150 - fh/2}" y="{66 - pw - fw}" width="{fh}" height="{fw}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        motor_x = 180
    else:
        suction = f'<rect x="216" y="{132 - ph/2}" width="{pw}" height="{ph}" fill="#1e293b" stroke="#475569" stroke-width="2"/><rect x="{216 + pw}" y="{132 - fh/2}" width="{fw}" height="{fh}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        discharge = f'<rect x="{150 - ph/2}" y="{66 - pw}" width="{ph}" height="{pw}" fill="#1e293b" stroke="#475569" stroke-width="2"/><rect x="{150 - fh/2}" y="{66 - pw - fw}" width="{fh}" height="{fw}" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>'
        motor_x = 55

    style_tag = f"<style>{css}</style>" if css else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 264" width="300" height="264">
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
  </defs>
  <rect x="70" y="212" width="160" height="14" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="100" y="200" width="100" height="12" fill="#334155"/>
  <rect x="{motor_x}" y="96" width="65" height="72" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <circle cx="150" cy="132" r="66" fill="url(#cp_case)" stroke="#64748b" stroke-width="4"/>
  <circle cx="150" cy="132" r="54" fill="#0f172a" stroke="{ring_color}" stroke-width="3" stroke-dasharray="4 2"{ring_class}/>
  <circle cx="150" cy="132" r="46" fill="{fluid_fill}"/>
  <circle cx="150" cy="132" r="20" fill="#00e5ff" opacity="0.6"{flow_class}/>
  <g{impeller_class}>
    <path d="M 150 132 Q 135 102 150 88 Q 165 102 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 180 117 194 132 Q 180 147 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 165 162 150 176 Q 135 162 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <path d="M 150 132 Q 120 147 106 132 Q 120 117 150 132 Z" fill="{blade_color}" stroke="{blade_stroke}" stroke-width="1.5"/>
    <circle cx="150" cy="132" r="10" fill="#0f172a" stroke="{blade_color}" stroke-width="2"/>
  </g>
  {suction}
  {discharge}
</svg>"""

for dn in ["dn25", "dn50", "dn100"]:
    for direction in ["l2r", "r2l"]:
        svgs[f"pump-centrifugal-{dn}-flow-{direction}-running-animated.svg"] = make_centrifugal(dn, direction, "running", animated=True)
        svgs[f"pump-centrifugal-{dn}-flow-{direction}-running-static.svg"] = make_centrifugal(dn, direction, "running", animated=False)
        svgs[f"pump-centrifugal-{dn}-flow-{direction}-stopped-static.svg"] = make_centrifugal(dn, direction, "stopped", animated=False)
        svgs[f"pump-centrifugal-{dn}-flow-{direction}-fault-animated.svg"] = make_centrifugal(dn, direction, "fault", animated=True)

# RO Multistage Pump
def make_ro(dn="dn50", state="running", animated=False):
    is_run = (state == "running")
    is_fault = (state == "fault")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    fluid_opacity = "0.9" if (is_run or is_fault) else "0.0"
    stream_pulse = ' class="anim-ro-stream"' if animated and is_run else ""
    fault_pulse = ' class="anim-ro-fault"' if animated and is_fault else ""

    css = ""
    if animated:
        if is_run:
            css = "@keyframes ro-flow { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(-40px); opacity: 0.2; } } .anim-ro-stream { animation: ro-flow 1.5s linear infinite; }"
        elif is_fault:
            css = "@keyframes ro-alert { 0%, 100% { stroke-opacity: 0.3; stroke-width: 2px; } 50% { stroke-opacity: 1; stroke-width: 5px; } } .anim-ro-fault { animation: ro-alert 0.8s ease-in-out infinite; }"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 424" width="240" height="424">
  <defs><style>{css}</style></defs>
  <rect x="40" y="380" width="160" height="18" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="310" width="90" height="50" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="35" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="165" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="85" y="150" width="70" height="160" rx="3" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="105" y="160" width="30" height="140" rx="4" fill="#0f172a" stroke="{ring_color}" stroke-width="1.5"{fault_pulse}/>
  <g{stream_pulse} opacity="{fluid_opacity}">
    <circle cx="120" cy="280" r="5" fill="#00e5ff" /><circle cx="120" cy="240" r="6" fill="#38bdf8" />
    <circle cx="120" cy="200" r="5" fill="#67e8f9" /><circle cx="120" cy="160" r="4" fill="#e0f2fe" />
  </g>
  <rect x="75" y="35" width="90" height="90" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
</svg>"""

for dn in ["dn25", "dn50"]:
    svgs[f"pump-ro-high-pressure-{dn}-running-animated.svg"] = make_ro(dn, "running", animated=True)
    svgs[f"pump-ro-high-pressure-{dn}-running-static.svg"] = make_ro(dn, "running", animated=False)
    svgs[f"pump-ro-high-pressure-{dn}-stopped-static.svg"] = make_ro(dn, "stopped", animated=False)
    svgs[f"pump-ro-high-pressure-{dn}-fault-animated.svg"] = make_ro(dn, "fault", animated=True)

# Chemical Dosing Pump
def make_dosing(dn="dn15", state="running", animated=False):
    is_run = (state == "running")
    is_fault = (state == "fault")
    ring_color = "#10b981" if is_run else ("#ef4444" if is_fault else "#475569")
    diaphragm_class = ' class="anim-dp"' if animated and is_run else ""
    drop_class = ' class="anim-drop"' if animated and is_run else ""

    css = ""
    if animated and is_run:
        css = "@keyframes dp-stroke { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } } @keyframes drop-move { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(35px); opacity: 0; } } .anim-dp { transform-origin: 162px 187px; animation: dp-stroke 1.2s ease-in-out infinite; } .anim-drop { animation: drop-move 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite; }"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 390" width="230" height="390">
  <defs><style>{css}</style></defs>
  <rect x="35" y="110" width="30" height="150" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="65" y="125" width="85" height="120" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <rect x="135" y="145" width="55" height="85" rx="6" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
  <circle cx="162" cy="187" r="22" fill="#0f172a" stroke="{ring_color}" stroke-width="2"/>
  <circle cx="162" cy="187" r="16" fill="#f43f5e" opacity="{1.0 if (is_run or is_fault) else 0.2}"{diaphragm_class}/>
  <rect x="152" y="230" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="152" y="105" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g{drop_class} opacity="{1.0 if is_run else 0.0}">
    <ellipse cx="162" cy="285" rx="4" ry="6" fill="#f43f5e" />
  </g>
</svg>"""

for dn in ["dn15", "dn25"]:
    svgs[f"pump-chemical-dosing-{dn}-running-animated.svg"] = make_dosing(dn, "running", animated=True)
    svgs[f"pump-chemical-dosing-{dn}-running-static.svg"] = make_dosing(dn, "running", animated=False)
    svgs[f"pump-chemical-dosing-{dn}-stopped-static.svg"] = make_dosing(dn, "stopped", animated=False)
    svgs[f"pump-chemical-dosing-{dn}-fault-animated.svg"] = make_dosing(dn, "fault", animated=True)

# Submersible Sump Pump
def make_sump(dn="dn50", state="running", animated=False):
    is_run = (state == "running")
    ring_color = "#10b981" if is_run else ("#ef4444" if state == "fault" else "#475569")
    b_class = ' class="anim-sump-bub"' if animated and is_run else ""
    css = "@keyframes sump-b { 0% { transform: translateY(0); opacity: 0.2; } 100% { transform: translateY(-40px); opacity: 0; } } .anim-sump-bub { animation: sump-b 1.4s linear infinite; }" if (animated and is_run) else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 360" width="240" height="360">
  <defs><style>{css}</style></defs>
  <path d="M 95 65 Q 120 40 145 65" fill="none" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
  <rect x="75" y="65" width="90" height="180" rx="8" fill="#1e293b" stroke="#475569" stroke-width="3"/>
  <circle cx="120" cy="140" r="30" fill="#0f172a" stroke="{ring_color}" stroke-width="3"/>
  <rect x="65" y="245" width="110" height="30" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="150" y="90" width="55" height="24" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g{b_class} opacity="{1.0 if is_run else 0.0}">
    <circle cx="85" cy="240" r="4" fill="#bae6fd" /><circle cx="155" cy="235" r="3" fill="#bae6fd" />
  </g>
</svg>"""

for dn in ["dn50", "dn100"]:
    svgs[f"pump-submersible-sump-{dn}-running-animated.svg"] = make_sump(dn, "running", animated=True)
    svgs[f"pump-submersible-sump-{dn}-running-static.svg"] = make_sump(dn, "running", animated=False)
    svgs[f"pump-submersible-sump-{dn}-stopped-static.svg"] = make_sump(dn, "stopped", animated=False)
    svgs[f"pump-submersible-sump-{dn}-fault-animated.svg"] = make_sump(dn, "fault", animated=True)


# ==============================================================================
# 2. UNIVERSAL TANKS & BASINS
# ==============================================================================

# Cylindrical Vertical Storage Tank (Raw, Feed, Treated, Chemical, Soft Water)
svgs["tank-cylindrical-vertical-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes t-wave { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(10px); } }
      .anim-t-wave { animation: t-wave 2.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="60" width="254" height="87" rx="6" fill="#0284c7" fill-opacity="0.85"/>
  <g class="anim-t-wave">
    <path d="M 33 60 Q 96 52 160 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
  <!-- Dip inlet & bottom drain -->
  <line x1="50" y1="20" x2="50" y2="70" stroke="#94a3b8" stroke-width="4"/>
  <line x1="270" y1="130" x2="300" y2="130" stroke="#94a3b8" stroke-width="4"/>
</svg>"""

svgs["tank-cylindrical-vertical-fluid-static.svg"] = svgs["tank-cylindrical-vertical-fluid-animated.svg"].replace('class="anim-t-wave"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-cylindrical-vertical-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="50" y1="20" x2="50" y2="70" stroke="#475569" stroke-width="4"/>
  <line x1="270" y1="130" x2="300" y2="130" stroke="#475569" stroke-width="4"/>
</svg>"""

# Conical Hopper Tank (Clarifiers, Lamella hoppers, Thickened sludge)
svgs["tank-conical-hopper-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 192" width="320" height="192">
  <defs>
    <style>
      @keyframes clar-sweep { 0%, 100% { transform: scaleX(1); } 50% { transform: scaleX(-1); } }
      .anim-clar { transform-origin: 160px 48px; animation: clar-sweep 6s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="40" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <polygon points="30,70 145,170 175,170 290,70" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>
  <polygon points="33,70 147,167 173,167 287,70" fill="#0369a1" fill-opacity="0.85"/>
  <rect x="150" y="16" width="20" height="24" rx="3" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g class="anim-clar">
    <line x1="160" y1="36" x2="160" y2="140" stroke="#94a3b8" stroke-width="4"/>
    <line x1="160" y1="140" x2="230" y2="90" stroke="#cbd5e1" stroke-width="3"/>
  </g>
</svg>"""

svgs["tank-conical-hopper-fluid-static.svg"] = svgs["tank-conical-hopper-fluid-animated.svg"].replace('class="anim-clar"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-conical-hopper-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 192" width="320" height="192">
  <rect x="30" y="30" width="260" height="40" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <polygon points="30,70 145,170 175,170 290,70" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>
  <rect x="150" y="16" width="20" height="24" rx="3" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>"""

# Aeration Basin with Bottom Diffusers (MBBR, Activated Sludge, SBR)
svgs["tank-aeration-diffuser-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes bub-rise { 0% { transform: translateY(0); opacity: 0.1; } 50% { opacity: 0.8; } 100% { transform: translateY(-70px); opacity: 0; } }
      @keyframes wave-sway { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(10px); } }
      .anim-bubs { animation: bub-rise 2s linear infinite; }
      .anim-waves { animation: wave-sway 2.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="33" y="60" width="254" height="87" rx="6" fill="#0e7490" fill-opacity="0.9"/>
  <g class="anim-waves">
    <path d="M 33 60 Q 65 52 97 60 T 161 60 T 225 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
  <line x1="50" y1="135" x2="270" y2="135" stroke="#94a3b8" stroke-width="4"/>
  <g class="anim-bubs">
    <circle cx="75" cy="125" r="3.5" fill="#e0f2fe"/>
    <circle cx="115" cy="120" r="3" fill="#e0f2fe"/>
    <circle cx="155" cy="125" r="3" fill="#e0f2fe"/>
    <circle cx="195" cy="120" r="3.5" fill="#e0f2fe"/>
    <circle cx="235" cy="125" r="3" fill="#e0f2fe"/>
  </g>
</svg>"""

svgs["tank-aeration-diffuser-fluid-static.svg"] = svgs["tank-aeration-diffuser-fluid-animated.svg"].replace('class="anim-bubs"', '').replace('class="anim-waves"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-aeration-diffuser-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="50" y1="135" x2="270" y2="135" stroke="#475569" stroke-width="4"/>
</svg>"""

# Agitator Reaction Tank (Flash mixer, Flocculator, Neutralization, Chemical dosing tank)
svgs["tank-agitator-mixer-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 318" width="300" height="318">
  <defs>
    <style>
      @keyframes spin-ag { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-ag { transform-origin: 150px 240px; animation: spin-ag 0.8s linear infinite; }
    </style>
  </defs>
  <rect x="40" y="80" width="220" height="200" rx="10" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="44" y="110" width="212" height="166" rx="6" fill="#1d4ed8" fill-opacity="0.8"/>
  <rect x="30" y="70" width="240" height="12" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="125" y="24" width="50" height="46" rx="5" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <line x1="150" y1="70" x2="150" y2="240" stroke="#cbd5e1" stroke-width="5"/>
  <g class="anim-ag">
    <ellipse cx="150" cy="240" rx="42" ry="8" fill="#60a5fa" />
    <ellipse cx="150" cy="240" rx="8" ry="42" fill="#93c5fd" />
    <circle cx="150" cy="240" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
  </g>
</svg>"""

svgs["tank-agitator-mixer-fluid-static.svg"] = svgs["tank-agitator-mixer-fluid-animated.svg"].replace('class="anim-ag"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-agitator-mixer-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 318" width="300" height="318">
  <rect x="40" y="80" width="220" height="200" rx="10" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="30" y="70" width="240" height="12" fill="#334155" stroke="#475569" stroke-width="2"/>
  <line x1="150" y1="70" x2="150" y2="240" stroke="#64748b" stroke-width="5"/>
</svg>"""

# Open Basin / Reservoir (Rainwater pond, equalization basin, raw water reservoir)
svgs["basin-open-reservoir-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 230" width="380" height="230">
  <defs>
    <style>
      @keyframes wave-p { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(12px); } }
      .anim-p { animation: wave-p 3s ease-in-out infinite; }
    </style>
  </defs>
  <polygon points="20,190 60,70 320,70 360,190" fill="#1c1917" stroke="#44403c" stroke-width="4"/>
  <polygon points="50,185 80,100 300,100 330,185" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <g class="anim-p">
    <path d="M 80 100 Q 135 92 190 100 T 300 100" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>
</svg>"""

svgs["basin-open-reservoir-fluid-static.svg"] = svgs["basin-open-reservoir-fluid-animated.svg"].replace('class="anim-p"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["basin-open-reservoir-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 230" width="380" height="230">
  <polygon points="20,190 60,70 320,70 360,190" fill="#1c1917" stroke="#44403c" stroke-width="4"/>
  <polygon points="50,185 80,140 300,140 330,185" fill="#292524" stroke="#44403c" stroke-width="2"/>
</svg>"""


# ==============================================================================
# 3. UNIVERSAL FILTRATION, SEPARATION & MEMBRANES
# ==============================================================================

# FRP Pressure Vessel Filter (PSF, ACF, Softener, MGF)
svgs["vessel-pressure-filter-frp-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <defs>
    <style>
      @keyframes v-stream { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(45px); opacity: 0.2; } }
      .anim-vs { animation: v-stream 1.5s linear infinite; }
    </style>
  </defs>
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="90" y="92" width="96" height="60" fill="#38bdf8" opacity="0.6"/>
  <rect x="90" y="152" width="96" height="70" fill="#ca8a04" opacity="0.8"/>
  <rect x="90" y="222" width="96" height="75" fill="#475569" opacity="0.8"/>
  <g class="anim-vs">
    <line x1="120" y1="100" x2="120" y2="125" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="156" y1="110" x2="156" y2="135" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>"""

svgs["vessel-pressure-filter-frp-fluid-static.svg"] = svgs["vessel-pressure-filter-frp-fluid-animated.svg"].replace('class="anim-vs"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["vessel-pressure-filter-frp-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 384" width="276" height="384">
  <line x1="60" y1="320" x2="60" y2="365" stroke="#475569" stroke-width="6"/>
  <line x1="216" y1="320" x2="216" y2="365" stroke="#475569" stroke-width="6"/>
  <rect x="48" y="70" width="180" height="250" rx="30" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="88" y="90" width="100" height="210" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

# Micron Cartridge Filter
svgs["filter-cartridge-micron-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 272 360" width="272" height="360">
  <defs>
    <style>
      @keyframes mic-f { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.9; } }
      .anim-mf { animation: mic-f 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="56" y="80" width="160" height="230" rx="20" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="96" y="100" width="80" height="190" rx="4" fill="#38bdf8" stroke="#0284c7" stroke-width="2" class="anim-mf"/>
  <line x1="136" y1="100" x2="136" y2="290" stroke="#bae6fd" stroke-width="3"/>
</svg>"""

svgs["filter-cartridge-micron-fluid-static.svg"] = svgs["filter-cartridge-micron-fluid-animated.svg"].replace('class="anim-mf"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["filter-cartridge-micron-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 272 360" width="272" height="360">
  <rect x="56" y="80" width="160" height="230" rx="20" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <rect x="96" y="100" width="80" height="190" rx="4" fill="#1e293b" stroke="#334155" stroke-width="2"/>
</svg>"""

# Reverse Osmosis (RO) Membrane Skid
svgs["skid-membrane-ro-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 280" width="350" height="280">
  <defs>
    <style>
      @keyframes ro-s { 0% { transform: translateX(0); opacity: 0.2; } 50% { opacity: 0.9; } 100% { transform: translateX(50px); opacity: 0.2; } }
      .anim-ros { animation: ro-s 1.5s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="235" width="290" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="60" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="278" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="65" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="75" y="115" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="75" y="165" width="200" height="36" rx="18" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="110" y="77" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="127" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="177" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <g class="anim-ros">
    <circle cx="130" cy="83" r="3" fill="#00e5ff"/><circle cx="170" cy="83" r="3.5" fill="#38bdf8"/>
    <circle cx="130" cy="133" r="3" fill="#00e5ff"/><circle cx="170" cy="133" r="3.5" fill="#38bdf8"/>
    <circle cx="130" cy="183" r="3" fill="#00e5ff"/><circle cx="170" cy="183" r="3.5" fill="#38bdf8"/>
  </g>
  <line x1="66" y1="83" x2="66" y2="183" stroke="#0284c7" stroke-width="6"/>
  <line x1="284" y1="83" x2="284" y2="183" stroke="#10b981" stroke-width="6"/>
</svg>"""

svgs["skid-membrane-ro-fluid-static.svg"] = svgs["skid-membrane-ro-fluid-animated.svg"].replace('class="anim-ros"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["skid-membrane-ro-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 280" width="350" height="280">
  <rect x="30" y="235" width="290" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="65" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="115" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="165" width="200" height="36" rx="18" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>"""

# Ultrafiltration (UF) Skid
svgs["skid-membrane-uf-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 328 344" width="328" height="344">
  <defs>
    <style>
      @keyframes uf-s { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(40px); opacity: 0.2; } }
      .anim-ufs { animation: uf-s 1.4s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="300" width="268" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="50" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="40" y="275" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="58" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="116" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="174" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="232" y="75" width="38" height="190" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <g class="anim-ufs">
    <line x1="77" y1="120" x2="77" y2="145" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="135" y1="140" x2="135" y2="165" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
    <line x1="193" y1="125" x2="193" y2="150" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="251" y1="145" x2="251" y2="170" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  </g>
</svg>"""

svgs["skid-membrane-uf-fluid-static.svg"] = svgs["skid-membrane-uf-fluid-animated.svg"].replace('class="anim-ufs"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["skid-membrane-uf-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 328 344" width="328" height="344">
  <rect x="30" y="300" width="268" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="58" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="116" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="174" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="232" y="75" width="38" height="190" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""

# Sludge Filter Press (Recessed Plate & Frame)
svgs["press-sludge-filter-clamped-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260" width="340" height="260">
  <defs>
    <style>
      @keyframes drp { 0% { transform: translateY(0); opacity: 0.9; } 100% { transform: translateY(35px); opacity: 0; } }
      .anim-drp { animation: drp 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
    </style>
  </defs>
  <rect x="25" y="200" width="290" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="60" width="24" height="145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="275" y="60" width="24" height="145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="64" y1="80" x2="275" y2="80" stroke="#94a3b8" stroke-width="6"/>
  <line x1="64" y1="180" x2="275" y2="180" stroke="#94a3b8" stroke-width="6"/>
  <g fill="#475569" stroke="#1e293b" stroke-width="1.5">
    <rect x="75" y="85" width="8" height="90" rx="1"/><rect x="85" y="85" width="8" height="90" rx="1"/>
    <rect x="95" y="85" width="8" height="90" rx="1"/><rect x="105" y="85" width="8" height="90" rx="1"/>
    <rect x="115" y="85" width="8" height="90" rx="1"/><rect x="125" y="85" width="8" height="90" rx="1"/>
    <rect x="135" y="85" width="8" height="90" rx="1"/><rect x="145" y="85" width="8" height="90" rx="1"/>
    <rect x="155" y="85" width="8" height="90" rx="1"/><rect x="165" y="85" width="8" height="90" rx="1"/>
  </g>
  <rect x="180" y="115" width="95" height="30" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <g class="anim-drp">
    <circle cx="100" cy="190" r="3" fill="#38bdf8"/><circle cx="140" cy="190" r="3" fill="#38bdf8"/>
  </g>
</svg>"""

svgs["press-sludge-filter-clamped-static.svg"] = svgs["press-sludge-filter-clamped-animated.svg"].replace('class="anim-drp"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["press-sludge-filter-open-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260" width="340" height="260">
  <rect x="25" y="200" width="290" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="40" y="60" width="24" height="145" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="275" y="60" width="24" height="145" fill="#334155" stroke="#475569" stroke-width="2"/>
  <g fill="#334155" stroke="#1e293b" stroke-width="1.5">
    <rect x="75" y="85" width="8" height="90" rx="1"/><rect x="95" y="85" width="8" height="90" rx="1"/>
    <rect x="115" y="85" width="8" height="90" rx="1"/><rect x="135" y="85" width="8" height="90" rx="1"/>
  </g>
  <rect x="210" y="115" width="65" height="30" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""

# Lamella Tube Settler
svgs["settler-lamella-clarifier-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 252" width="300" height="252">
  <defs>
    <style>
      @keyframes fl-s { 0% { transform: translate(0, 0); opacity: 0.1; } 50% { opacity: 0.8; } 100% { transform: translate(-25px, 35px); opacity: 0.1; } }
      .anim-fls { animation: fl-s 2s linear infinite; }
    </style>
  </defs>
  <polygon points="30,40 270,40 270,140 180,220 120,220 30,140" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <polygon points="34,60 266,60 266,138 178,216 122,216 34,138" fill="#0284c7" fill-opacity="0.8"/>
  <line x1="70" y1="130" x2="120" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="95" y1="130" x2="145" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="120" y1="130" x2="170" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="145" y1="130" x2="195" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <line x1="170" y1="130" x2="220" y2="60" stroke="#94a3b8" stroke-width="4"/>
  <g class="anim-fls">
    <circle cx="140" cy="75" r="3" fill="#78350f"/><circle cx="165" cy="85" r="3.5" fill="#78350f"/>
  </g>
</svg>"""

svgs["settler-lamella-clarifier-fluid-static.svg"] = svgs["settler-lamella-clarifier-fluid-animated.svg"].replace('class="anim-fls"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["settler-lamella-clarifier-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 252" width="300" height="252">
  <polygon points="30,40 270,40 270,140 180,220 120,220 30,140" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <line x1="70" y1="130" x2="120" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="95" y1="130" x2="145" y2="60" stroke="#475569" stroke-width="4"/>
  <line x1="120" y1="130" x2="170" y2="60" stroke="#475569" stroke-width="4"/>
</svg>"""

# Dissolved Air Flotation (DAF)
svgs["tank-flotation-daf-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="340" height="240">
  <defs>
    <style>
      @keyframes mic-b { 0% { transform: translateY(0); opacity: 0.1; } 50% { opacity: 0.9; } 100% { transform: translateY(-70px); opacity: 0; } }
      .anim-mb { animation: mic-b 1.8s linear infinite; }
    </style>
  </defs>
  <polygon points="30,60 270,60 270,180 230,210 70,210 30,180" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <polygon points="34,80 266,80 266,178 228,206 72,206 34,178" fill="#0284c7" fill-opacity="0.8"/>
  <rect x="34" y="70" width="232" height="16" fill="#854d0e" fill-opacity="0.8"/>
  <polygon points="266,70 310,70 310,120 266,86" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <line x1="80" y1="190" x2="220" y2="190" stroke="#38bdf8" stroke-width="4"/>
  <g class="anim-mb">
    <circle cx="100" cy="180" r="2" fill="#e0f2fe"/><circle cx="115" cy="165" r="2.5" fill="#bae6fd"/>
    <circle cx="130" cy="180" r="1.5" fill="#e0f2fe"/><circle cx="145" cy="160" r="2" fill="#bae6fd"/>
  </g>
</svg>"""

svgs["tank-flotation-daf-fluid-static.svg"] = svgs["tank-flotation-daf-fluid-animated.svg"].replace('class="anim-mb"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["tank-flotation-daf-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="340" height="240">
  <polygon points="30,60 270,60 270,180 230,210 70,210 30,180" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <polygon points="266,70 310,70 310,120 266,86" fill="#1e293b" stroke="#475569" stroke-width="2"/>
</svg>"""


# ==============================================================================
# 4. UTILITIES, VALVES & INSTRUMENTS
# ==============================================================================

# Aeration Blower
svgs["blower-rotary-running-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 264" width="264" height="264">
  <defs>
    <style>
      @keyframes spin-b { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-sb { transform-origin: 132px 132px; animation: spin-b 0.8s linear infinite; }
    </style>
  </defs>
  <rect x="66" y="210" width="132" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <circle cx="132" cy="132" r="70" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
  <circle cx="132" cy="132" r="58" fill="#0f172a" stroke="#10b981" stroke-width="3" stroke-dasharray="3 3"/>
  <g class="anim-sb">
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

svgs["blower-rotary-running-static.svg"] = svgs["blower-rotary-running-animated.svg"].replace('class="anim-sb"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["blower-rotary-stopped-static.svg"] = svgs["blower-rotary-running-static.svg"].replace('#10b981', '#475569').replace('#67e8f9', '#64748b').replace('#38bdf8', '#475569')

# Cooling Tower (HVAC & Industrial Process)
svgs["cooling-tower-induced-draft-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 336 368" width="336" height="368">
  <defs>
    <style>
      @keyframes spin-c { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      @keyframes c-rain { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.9; } 100% { transform: translateY(40px); opacity: 0.1; } }
      .anim-cf { transform-origin: 168px 42px; animation: spin-c 0.9s linear infinite; }
      .anim-cr { animation: c-rain 1.1s linear infinite; }
    </style>
  </defs>
  <line x1="50" y1="300" x2="50" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="286" y1="300" x2="286" y2="345" stroke="#475569" stroke-width="6"/>
  <rect x="40" y="270" width="256" height="35" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <rect x="52" y="140" width="232" height="120" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <g class="anim-cr">
    <line x1="80" y1="150" x2="80" y2="168" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="120" y1="160" x2="120" y2="178" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="168" y1="150" x2="168" y2="172" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
  </g>
  <path d="M 100 105 L 120 40 L 216 40 L 236 105 Z" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <g class="anim-cf">
    <ellipse cx="168" cy="42" rx="42" ry="7" fill="#67e8f9" fill-opacity="0.9" />
    <ellipse cx="168" cy="42" rx="7" ry="42" fill="#38bdf8" fill-opacity="0.9" />
    <circle cx="168" cy="42" r="9" fill="#0f172a" stroke="#bae6fd" stroke-width="2"/>
  </g>
</svg>"""

svgs["cooling-tower-induced-draft-fluid-static.svg"] = svgs["cooling-tower-induced-draft-fluid-animated.svg"].replace('class="anim-cf"', '').replace('class="anim-cr"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["cooling-tower-induced-draft-dry-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 336 368" width="336" height="368">
  <line x1="50" y1="300" x2="50" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="286" y1="300" x2="286" y2="345" stroke="#475569" stroke-width="6"/>
  <rect x="40" y="270" width="256" height="35" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="52" y="140" width="232" height="120" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <path d="M 100 105 L 120 40 L 216 40 L 236 105 Z" fill="#1e293b" stroke="#475569" stroke-width="3"/>
</svg>"""

# UV Disinfection Reactor
svgs["reactor-uv-disinfection-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 344 208" width="344" height="208">
  <defs>
    <style>
      @keyframes uv-g { 0%, 100% { opacity: 0.45; } 50% { opacity: 1; } }
      .anim-uvg { animation: uv-g 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="52" y="64" width="240" height="80" rx="8" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <rect x="80" y="78" width="184" height="52" rx="6" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
  <rect x="90" y="99" width="164" height="10" rx="5" fill="#c084fc" class="anim-uvg"/>
</svg>"""

svgs["reactor-uv-disinfection-active-static.svg"] = svgs["reactor-uv-disinfection-active-animated.svg"].replace('class="anim-uvg"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["reactor-uv-disinfection-inactive-static.svg"] = svgs["reactor-uv-disinfection-active-static.svg"].replace('#a855f7', '#475569').replace('#c084fc', '#334155')

# Solenoid Valve
svgs["valve-solenoid-inline-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <style>
      @keyframes vl-f { 0% { transform: translateX(0); opacity: 0.2; } 50% { opacity: 1; } 100% { transform: translateX(30px); opacity: 0.2; } }
      .anim-vlf { animation: vl-f 1.4s linear infinite; }
    </style>
  </defs>
  <polygon points="50,90 120,120 50,150" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <polygon points="190,90 120,120 190,150" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <circle cx="120" cy="120" r="32" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="120" cy="120" r="24" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  <rect x="105" y="45" width="30" height="45" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <g class="anim-vlf">
    <polygon points="85,120 75,115 75,125" fill="#38bdf8"/>
    <polygon points="155,120 145,115 145,125" fill="#38bdf8"/>
  </g>
</svg>"""

svgs["valve-solenoid-inline-active-static.svg"] = svgs["valve-solenoid-inline-active-animated.svg"].replace('class="anim-vlf"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["valve-solenoid-inline-closed-static.svg"] = svgs["valve-solenoid-inline-active-static.svg"].replace('#10b981', '#ef4444').replace('#38bdf8', '#475569')

# Multiport Valve
svgs["valve-multiport-block-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 324 296" width="324" height="296">
  <defs>
    <style>
      @keyframes mp-s { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      .anim-mps { transform-origin: 162px 148px; animation: mp-s 6s linear infinite; }
    </style>
  </defs>
  <rect x="100" y="86" width="124" height="124" rx="14" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
  <circle cx="162" cy="148" r="44" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
  <g class="anim-mps">
    <circle cx="162" cy="120" r="6" fill="#38bdf8"/>
    <circle cx="190" cy="148" r="6" fill="#38bdf8"/>
    <circle cx="162" cy="176" r="6" fill="#38bdf8"/>
    <circle cx="134" cy="148" r="6" fill="#38bdf8"/>
  </g>
</svg>"""

svgs["valve-multiport-block-static.svg"] = svgs["valve-multiport-block-active-animated.svg"].replace('class="anim-mps"', '').replace('<style>', '<!--').replace('</style>', '-->')

# Pressure Gauge
svgs["gauge-analog-pressure-active-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 304 192" width="304" height="192">
  <defs>
    <style>
      @keyframes ng-o { 0%, 100% { transform: rotate(-35deg); } 50% { transform: rotate(-25deg); } }
      .anim-ngo { transform-origin: 152px 95px; animation: ng-o 1.6s ease-in-out infinite; }
    </style>
  </defs>
  <rect x="144" y="145" width="16" height="35" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <circle cx="152" cy="95" r="60" fill="#334155" stroke="#94a3b8" stroke-width="3"/>
  <circle cx="152" cy="95" r="50" fill="#0f172a" stroke="#475569" stroke-width="2"/>
  <path d="M 115 115 A 42 42 0 1 1 189 115" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <path d="M 130 65 A 42 42 0 0 1 174 65" fill="none" stroke="#10b981" stroke-width="4"/>
  <g class="anim-ngo">
    <line x1="152" y1="95" x2="152" y2="62" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
    <circle cx="152" cy="95" r="7" fill="#ef4444"/>
  </g>
</svg>"""

svgs["gauge-analog-pressure-static.svg"] = svgs["gauge-analog-pressure-active-animated.svg"].replace('class="anim-ngo"', '').replace('<style>', '<!--').replace('</style>', '-->')

# Water Tanker Supply Station
svgs["supply-water-tanker-fluid-animated.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 376 328" width="376" height="328">
  <defs>
    <style>
      @keyframes h-p { 0% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -30; } }
      .anim-hp { stroke-dasharray: 10 5; animation: h-p 1.2s linear infinite; }
    </style>
  </defs>
  <rect x="30" y="250" width="316" height="12" rx="3" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="50" y="90" width="220" height="120" rx="40" fill="#0284c7" stroke="#38bdf8" stroke-width="3"/>
  <circle cx="100" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <circle cx="160" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <circle cx="300" cy="225" r="24" fill="#0f172a" stroke="#64748b" stroke-width="5"/>
  <path d="M 160 210 Q 160 270 210 270 L 260 270" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round" class="anim-hp"/>
</svg>"""

svgs["supply-water-tanker-fluid-static.svg"] = svgs["supply-water-tanker-fluid-animated.svg"].replace('class="anim-hp"', '').replace('<style>', '<!--').replace('</style>', '-->')
svgs["supply-water-tanker-dry-static.svg"] = svgs["supply-water-tanker-fluid-static.svg"].replace('#0284c7', '#1e293b').replace('#38bdf8', '#475569')

# Facility Building
svgs["facility-commercial-building-static.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 368" width="240" height="368">
  <rect x="30" y="330" width="180" height="14" rx="3" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="40" y="50" width="160" height="280" rx="4" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <g fill="#0284c7" fill-opacity="0.4" stroke="#334155" stroke-width="1.5">
    <rect x="55" y="70" width="25" height="35" rx="2"/><rect x="90" y="70" width="25" height="35" rx="2"/>
    <rect x="125" y="70" width="25" height="35" rx="2"/><rect x="160" y="70" width="25" height="35" rx="2"/>
    <rect x="55" y="120" width="25" height="35" rx="2"/><rect x="90" y="120" width="25" height="35" rx="2"/>
    <rect x="125" y="120" width="25" height="35" rx="2"/><rect x="160" y="120" width="25" height="35" rx="2"/>
    <rect x="55" y="170" width="25" height="35" rx="2"/><rect x="90" y="170" width="25" height="35" rx="2"/>
    <rect x="125" y="170" width="25" height="35" rx="2"/><rect x="160" y="170" width="25" height="35" rx="2"/>
  </g>
</svg>"""

# ==============================================================================
# WRITE ALL CONSOLIDATED GENERIC SVGS TO DISK
# ==============================================================================

print(f"Writing {len(svgs)} modular SCADA SVG components to {OUT_DIR}...")
for fname, content in svgs.items():
    if "<text" in content.lower():
        raise ValueError(f"Strict rule violated: <text> tag found in {fname}")
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Done! Successfully generated {len(svgs)} generic SCADA SVG symbols.")
