import os

output_dir = os.path.join("public", "schematic asserts", "valve")
os.makedirs(output_dir, exist_ok=True)

defs_svg = """  <defs>
    <linearGradient id="metalFlangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>
  </defs>"""

# ==============================================================================
# 1. SOLENOID / MOTORIZED AUTOMATED VALVES (Horizontal V-SOL & Vertical V-CLR)
# ==============================================================================
def generate_solenoid_valve(orientation="horizontal", is_open=True, is_animated=False, fluid_pulse="#BAE6FD"):
    core_fill = "#DCFCE7" if is_open else "#FEE2E2"
    core_stroke = "#16A34A" if is_open else "#DC2626"
    coil_fill = "#15803D" if is_open else "#B91C1C"
    led_fill = "#22C55E" if is_open else "#EF4444"

    pulse_core_anim = ""
    led_anim = ""
    flow_stream = ""

    if is_open and is_animated:
        pulse_core_anim = """
      <animate attributeName="r" values="2;4.2;2" dur="0.9s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.7;1;0.7" dur="0.9s" repeatCount="indefinite" />"""
        led_anim = """
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite" />"""

        if orientation == "horizontal":
            flow_stream = f"""
  <!-- Animated Horizontal Process Stream -->
  <line x1="6" y1="26" x2="42" y2="26" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite" />
  </line>"""
        else:
            flow_stream = f"""
  <!-- Animated Vertical Process Stream -->
  <line x1="26" y1="6" x2="26" y2="42" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite" />
  </line>"""

    if orientation == "horizontal":
        body = f"""  <!-- Horizontal In-Line Pipe Connection Flanges -->
  <rect x="6" y="20" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="20" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Twin Triangular Body -->
  <polygon points="10,18 24,26 10,34" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="38,18 24,26 38,34" fill="#334155" stroke="#0F172A" stroke-width="1.2" />{flow_stream}

  <!-- Center Seat -->
  <circle cx="24" cy="26" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="24" cy="26" r="2.5" fill="{core_stroke}">{pulse_core_anim}
  </circle>

  <!-- Top Solenoid Electrical Actuator Coil Head -->
  <line x1="24" y1="26" x2="24" y2="15" stroke="#64748B" stroke-width="2.5" />
  <rect x="18" y="5" width="12" height="11" rx="2" fill="#1E293B" stroke="{core_stroke}" stroke-width="1.2" />
  <rect x="20" y="7" width="8" height="3" rx="0.5" fill="{coil_fill}" />
  <circle cx="24" cy="13" r="1.5" fill="{led_fill}">{led_anim}
  </circle>"""
    else:
        body = f"""  <!-- Vertical In-Line Pipe Connection Flanges -->
  <rect x="20" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="20" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Twin Triangular Body -->
  <polygon points="18,10 26,24 34,10" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="18,38 26,24 34,38" fill="#334155" stroke="#0F172A" stroke-width="1.2" />{flow_stream}

  <!-- Center Seat -->
  <circle cx="26" cy="24" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="26" cy="24" r="2.5" fill="{core_stroke}">{pulse_core_anim}
  </circle>

  <!-- Side Solenoid Electrical Actuator Coil Head -->
  <line x1="26" y1="24" x2="15" y2="24" stroke="#64748B" stroke-width="2.5" />
  <rect x="5" y="18" width="11" height="12" rx="2" fill="#1E293B" stroke="{core_stroke}" stroke-width="1.2" />
  <rect x="7" y="20" width="3" height="8" rx="0.5" fill="{coil_fill}" />
  <circle cx="13" cy="24" r="1.5" fill="{led_fill}">{led_anim}
  </circle>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

# ==============================================================================
# 2. MANUAL BALL VALVES (Horizontal & Vertical, Open & Closed)
# ==============================================================================
def generate_manual_valve(orientation="horizontal", is_open=True, is_animated=False, fluid_pulse="#BAE6FD"):
    lever_color = "#16A34A" if is_open else "#DC2626"
    core_fill = "#DCFCE7" if is_open else "#FEE2E2"
    core_stroke = "#16A34A" if is_open else "#DC2626"

    flow_stream = ""
    if is_open and is_animated:
        if orientation == "horizontal":
            flow_stream = f"""
  <!-- Animated Horizontal Process Stream -->
  <line x1="6" y1="24" x2="42" y2="24" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite" />
  </line>"""
        else:
            flow_stream = f"""
  <!-- Animated Vertical Process Stream -->
  <line x1="24" y1="6" x2="24" y2="42" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite" />
  </line>"""

    if orientation == "horizontal":
        lever_svg = (
            f'<line x1="24" y1="18" x2="38" y2="18" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
            if is_open
            else f'<line x1="24" y1="18" x2="24" y2="4" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        )
        body = f"""  <!-- Horizontal In-Line Pipe Connection Flanges -->
  <rect x="6" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- ASME Twin Triangular Valve Body -->
  <polygon points="10,16 24,24 10,32" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="38,16 24,24 38,32" fill="#334155" stroke="#0F172A" stroke-width="1.2" />{flow_stream}

  <!-- Center Valve Seat & Stem Boss -->
  <circle cx="24" cy="24" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="24" cy="24" r="3" fill="#1E293B" stroke="#64748B" stroke-width="0.6" />

  <!-- Stem & Actuating Hand Lever -->
  <line x1="24" y1="24" x2="24" y2="18" stroke="#475569" stroke-width="2" />
  {lever_svg}"""
    else:
        lever_svg = (
            f'<line x1="18" y1="24" x2="18" y2="38" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
            if is_open
            else f'<line x1="18" y1="24" x2="4" y2="24" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        )
        body = f"""  <!-- Vertical In-Line Pipe Connection Flanges -->
  <rect x="18" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="18" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- ASME Twin Triangular Valve Body -->
  <polygon points="16,10 24,24 32,10" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="16,38 24,24 32,38" fill="#334155" stroke="#0F172A" stroke-width="1.2" />{flow_stream}

  <!-- Center Valve Seat & Stem Boss -->
  <circle cx="24" cy="24" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="24" cy="24" r="3" fill="#1E293B" stroke="#64748B" stroke-width="0.6" />

  <!-- Stem & Actuating Hand Lever -->
  <line x1="24" y1="24" x2="18" y2="24" stroke="#475569" stroke-width="2" />
  {lever_svg}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

# ==============================================================================
# 3. CHECK VALVES (NON-RETURN / NRV)
# ==============================================================================
def generate_check_valve(orientation="horizontal", is_animated=False):
    anim_tag = ""
    if is_animated:
        anim_tag = """
    <animate attributeName="opacity" values="0.6;1;0.6" dur="0.9s" repeatCount="indefinite" />"""

    if orientation == "horizontal":
        body = f"""  <!-- Horizontal Flanges -->
  <rect x="6" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="10" y="18" width="28" height="12" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Forward Flow Direction Arrow & Internal Check Flap -->
  <polygon points="20,20 28,24 20,28" fill="#38BDF8" stroke="#0284C7" stroke-width="0.8">{anim_tag}
  </polygon>
  <line x1="17" y1="20" x2="17" y2="28" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />"""
    else:
        body = f"""  <!-- Vertical Flanges -->
  <rect x="18" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="18" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="18" y="10" width="12" height="28" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Downward Flow Direction Arrow & Internal Check Flap -->
  <polygon points="20,20 24,28 28,20" fill="#38BDF8" stroke="#0284C7" stroke-width="0.8">{anim_tag}
  </polygon>
  <line x1="20" y1="17" x2="28" y2="17" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

print("=== GENERATING COMPLETE SUITE OF IN-LINE & SOLENOID VALVES (ANIMATED & STATIC) ===")

VALVES = [
    # 1. Horizontal Solenoid Valve (V-SOL / Water Solenoid)
    ("valve-solenoid-horizontal-open-animated.svg", generate_solenoid_valve("horizontal", is_open=True, is_animated=True)),
    ("valve-solenoid-horizontal-open-static.svg", generate_solenoid_valve("horizontal", is_open=True, is_animated=False)),
    ("valve-solenoid-horizontal-open.svg", generate_solenoid_valve("horizontal", is_open=True, is_animated=False)),
    ("valve-solenoid-horizontal-closed-static.svg", generate_solenoid_valve("horizontal", is_open=False, is_animated=False)),
    ("valve-solenoid-horizontal-closed.svg", generate_solenoid_valve("horizontal", is_open=False, is_animated=False)),

    # V-SOL Aliases
    ("valve-water-solenoid-horizontal-open-animated.svg", generate_solenoid_valve("horizontal", is_open=True, is_animated=True)),
    ("valve-water-solenoid-horizontal-open-static.svg", generate_solenoid_valve("horizontal", is_open=True, is_animated=False)),
    ("valve-water-solenoid-horizontal-closed-static.svg", generate_solenoid_valve("horizontal", is_open=False, is_animated=False)),

    # 2. Vertical Solenoid Valve (V-CLR / Clarifier Valve)
    ("valve-solenoid-vertical-open-animated.svg", generate_solenoid_valve("vertical", is_open=True, is_animated=True, fluid_pulse="#EFE8D0")),
    ("valve-solenoid-vertical-open-static.svg", generate_solenoid_valve("vertical", is_open=True, is_animated=False)),
    ("valve-solenoid-vertical-open.svg", generate_solenoid_valve("vertical", is_open=True, is_animated=False)),
    ("valve-solenoid-vertical-closed-static.svg", generate_solenoid_valve("vertical", is_open=False, is_animated=False)),
    ("valve-solenoid-vertical-closed.svg", generate_solenoid_valve("vertical", is_open=False, is_animated=False)),

    # V-CLR Aliases
    ("valve-clarifier-vertical-open-animated.svg", generate_solenoid_valve("vertical", is_open=True, is_animated=True, fluid_pulse="#EFE8D0")),
    ("valve-clarifier-vertical-open-static.svg", generate_solenoid_valve("vertical", is_open=True, is_animated=False)),
    ("valve-clarifier-vertical-closed-static.svg", generate_solenoid_valve("vertical", is_open=False, is_animated=False)),

    # 3. Manual Ball Valves (Horizontal & Vertical)
    ("valve-manual-horizontal-open-animated.svg", generate_manual_valve("horizontal", is_open=True, is_animated=True)),
    ("valve-manual-horizontal-open-static.svg", generate_manual_valve("horizontal", is_open=True, is_animated=False)),
    ("valve-manual-horizontal-open.svg", generate_manual_valve("horizontal", is_open=True, is_animated=False)),
    ("valve-manual-horizontal-closed-static.svg", generate_manual_valve("horizontal", is_open=False, is_animated=False)),
    ("valve-manual-horizontal-closed.svg", generate_manual_valve("horizontal", is_open=False, is_animated=False)),

    ("valve-manual-vertical-open-animated.svg", generate_manual_valve("vertical", is_open=True, is_animated=True)),
    ("valve-manual-vertical-open-static.svg", generate_manual_valve("vertical", is_open=True, is_animated=False)),
    ("valve-manual-vertical-open.svg", generate_manual_valve("vertical", is_open=True, is_animated=False)),
    ("valve-manual-vertical-closed-static.svg", generate_manual_valve("vertical", is_open=False, is_animated=False)),
    ("valve-manual-vertical-closed.svg", generate_manual_valve("vertical", is_open=False, is_animated=False)),

    # 4. Check Valves (NRV)
    ("valve-check-horizontal-open-animated.svg", generate_check_valve("horizontal", is_animated=True)),
    ("valve-check-horizontal-open-static.svg", generate_check_valve("horizontal", is_animated=False)),
    ("valve-check-horizontal.svg", generate_check_valve("horizontal", is_animated=False)),

    ("valve-check-vertical-open-animated.svg", generate_check_valve("vertical", is_animated=True)),
    ("valve-check-vertical-open-static.svg", generate_check_valve("vertical", is_animated=False)),
    ("valve-check-vertical.svg", generate_check_valve("vertical", is_animated=False)),
]

count = 0
for fname, content in VALVES:
    fpath = os.path.join(output_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print(f"  + Generated: {fname}")

print(f"\nDone! Successfully generated {count} valve SVGs with animated & static states in '{output_dir}'.")
