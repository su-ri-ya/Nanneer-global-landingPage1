import os

valve_dir = os.path.join("public", "schematic asserts", "valve")
os.makedirs(valve_dir, exist_ok=True)

# Shared clean gradient
defs_svg = """  <defs>
    <linearGradient id="metalFlangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>
  </defs>"""

# ==============================================================================
# 1. MANUAL IN-LINE BALL VALVE (Horizontal & Vertical, Open & Closed)
# Standard 48x48 canvas, center at (24, 24)
# ==============================================================================
def generate_manual_valve(orientation="horizontal", is_open=True):
    lever_color = "#16A34A" if is_open else "#DC2626"
    lever_stroke = "#15803D" if is_open else "#B91C1C"
    core_fill = "#DCFCE7" if is_open else "#FEE2E2"
    core_stroke = "#16A34A" if is_open else "#DC2626"

    if orientation == "horizontal":
        # Horizontal flow along y=24: Left flange at x=6, Right flange at x=42
        # Open: Lever aligned with pipe (horizontal); Closed: Lever perpendicular (vertical)
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
  <polygon points="38,16 24,24 38,32" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Center Valve Seat & Stem Boss -->
  <circle cx="24" cy="24" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="24" cy="24" r="3" fill="#1E293B" stroke="#64748B" stroke-width="0.6" />

  <!-- Stem & Actuating Hand Lever -->
  <line x1="24" y1="24" x2="24" y2="18" stroke="#475569" stroke-width="2" />
  {lever_svg}"""
    else:
        # Vertical flow along x=24: Top flange at y=6, Bottom flange at y=42
        # Open: Lever aligned with pipe (vertical); Closed: Lever perpendicular (horizontal)
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
  <polygon points="16,38 24,24 32,38" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

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
# 2. SOLENOID / MOTORIZED AUTOMATED VALVE (Horizontal & Vertical, Open & Closed)
# ==============================================================================
def generate_solenoid_valve(orientation="horizontal", is_open=True):
    core_fill = "#DCFCE7" if is_open else "#FEE2E2"
    core_stroke = "#16A34A" if is_open else "#DC2626"
    coil_fill = "#15803D" if is_open else "#B91C1C"

    if orientation == "horizontal":
        body = f"""  <!-- Horizontal In-Line Pipe Connection Flanges -->
  <rect x="6" y="20" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="20" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Twin Triangular Body -->
  <polygon points="10,18 24,26 10,34" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="38,18 24,26 38,34" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Center Seat -->
  <circle cx="24" cy="26" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="24" cy="26" r="2.5" fill="{core_stroke}" />

  <!-- Top Solenoid Electrical Actuator Coil Head -->
  <line x1="24" y1="26" x2="24" y2="15" stroke="#64748B" stroke-width="2.5" />
  <rect x="18" y="5" width="12" height="11" rx="2" fill="#1E293B" stroke="{core_stroke}" stroke-width="1.2" />
  <rect x="20" y="7" width="8" height="3" rx="0.5" fill="{coil_fill}" />
  <circle cx="24" cy="13" r="1.2" fill="#FFFFFF" />"""
    else:
        body = f"""  <!-- Vertical In-Line Pipe Connection Flanges -->
  <rect x="20" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="20" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Twin Triangular Body -->
  <polygon points="18,10 26,24 34,10" fill="#334155" stroke="#0F172A" stroke-width="1.2" />
  <polygon points="18,38 26,24 34,38" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Center Seat -->
  <circle cx="26" cy="24" r="7" fill="{core_fill}" stroke="{core_stroke}" stroke-width="1.4" />
  <circle cx="26" cy="24" r="2.5" fill="{core_stroke}" />

  <!-- Side Solenoid Electrical Actuator Coil Head -->
  <line x1="26" y1="24" x2="15" y2="24" stroke="#64748B" stroke-width="2.5" />
  <rect x="5" y="18" width="11" height="12" rx="2" fill="#1E293B" stroke="{core_stroke}" stroke-width="1.2" />
  <rect x="7" y="20" width="3" height="8" rx="0.5" fill="{coil_fill}" />
  <circle cx="13" cy="24" r="1.2" fill="#FFFFFF" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

# ==============================================================================
# 3. CHECK VALVE (NON-RETURN VALVE / NRV) (Horizontal & Vertical)
# ==============================================================================
def generate_check_valve(orientation="horizontal"):
    if orientation == "horizontal":
        body = """  <!-- Horizontal Flanges -->
  <rect x="6" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="10" y="18" width="28" height="12" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Forward Flow Direction Arrow & Internal Check Flap -->
  <polygon points="20,20 28,24 20,28" fill="#38BDF8" stroke="#0284C7" stroke-width="0.8" />
  <line x1="17" y1="20" x2="17" y2="28" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />"""
    else:
        body = """  <!-- Vertical Flanges -->
  <rect x="18" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="18" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="18" y="10" width="12" height="28" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Downward Flow Direction Arrow & Internal Check Flap -->
  <polygon points="20,20 24,28 28,20" fill="#38BDF8" stroke="#0284C7" stroke-width="0.8" />
  <line x1="20" y1="17" x2="28" y2="17" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

print("=== GENERATING MODULAR IN-LINE PIPELINE VALVES FOR ADMIN FRONTEND ===")

valves_to_generate = [
    # Manual Ball Valves
    ("valve-manual-horizontal-open.svg", generate_manual_valve("horizontal", True)),
    ("valve-manual-horizontal-closed.svg", generate_manual_valve("horizontal", False)),
    ("valve-manual-vertical-open.svg", generate_manual_valve("vertical", True)),
    ("valve-manual-vertical-closed.svg", generate_manual_valve("vertical", False)),

    # Solenoid / Motorized Valves
    ("valve-solenoid-horizontal-open.svg", generate_solenoid_valve("horizontal", True)),
    ("valve-solenoid-horizontal-closed.svg", generate_solenoid_valve("horizontal", False)),
    ("valve-solenoid-vertical-open.svg", generate_solenoid_valve("vertical", True)),
    ("valve-solenoid-vertical-closed.svg", generate_solenoid_valve("vertical", False)),

    # Check Valves (NRV)
    ("valve-check-horizontal.svg", generate_check_valve("horizontal")),
    ("valve-check-vertical.svg", generate_check_valve("vertical")),
]

for filename, content in valves_to_generate:
    filepath = os.path.join(valve_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  + Generated: {filename}")

print(f"\nDone! Successfully generated {len(valves_to_generate)} modular in-line valves in '{valve_dir}'.")
