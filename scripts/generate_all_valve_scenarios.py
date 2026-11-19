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
# 1. SOLENOID / MOTORIZED AUTOMATED VALVES
# States: open-animated, open-static, closed-static, fault-animated, fault-static
# Directions:
#   Horizontal: l2r (left to right), r2l (right to left)
#   Vertical:   t2b (top to bottom), b2t (bottom to top)
# ==============================================================================
def generate_solenoid_valve(orientation="horizontal", state="open-animated", direction="normal", fluid_pulse="#BAE6FD"):
    # Determine colors based on state
    if state.startswith("open"):
        core_fill = "#DCFCE7"
        core_stroke = "#16A34A"
        coil_fill = "#15803D"
        led_fill = "#22C55E"
    elif state.startswith("fault"):
        core_fill = "#FEF08A"
        core_stroke = "#CA8A04"
        coil_fill = "#A16207"
        led_fill = "#EAB308"
    else:  # closed
        core_fill = "#FEE2E2"
        core_stroke = "#DC2626"
        coil_fill = "#B91C1C"
        led_fill = "#EF4444"

    is_animated = "animated" in state
    pulse_core_anim = ""
    led_anim = ""
    flow_stream = ""

    if is_animated:
        if state.startswith("fault"):
            led_anim = """
      <animate attributeName="opacity" values="0.2;1;0.2" dur="0.4s" repeatCount="indefinite" />"""
            pulse_core_anim = """
      <animate attributeName="opacity" values="0.4;1;0.4" dur="0.5s" repeatCount="indefinite" />"""
        elif state.startswith("open"):
            pulse_core_anim = """
      <animate attributeName="r" values="2;4.2;2" dur="0.9s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.7;1;0.7" dur="0.9s" repeatCount="indefinite" />"""
            led_anim = """
      <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite" />"""

            # Directional flow animation
            if orientation == "horizontal":
                from_val = "20" if direction == "normal" else "0"
                to_val = "0" if direction == "normal" else "20"
                flow_stream = f"""
  <!-- Animated Horizontal Process Stream ({'L->R' if direction=='normal' else 'R->L'}) -->
  <line x1="6" y1="26" x2="42" y2="26" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="{from_val}" to="{to_val}" dur="0.8s" repeatCount="indefinite" />
  </line>"""
            else:
                from_val = "20" if direction == "normal" else "0"
                to_val = "0" if direction == "normal" else "20"
                flow_stream = f"""
  <!-- Animated Vertical Process Stream ({'T->B' if direction=='normal' else 'B->T'}) -->
  <line x1="26" y1="6" x2="26" y2="42" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="{from_val}" to="{to_val}" dur="0.8s" repeatCount="indefinite" />
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
# 2. MANUAL BALL VALVES
# States: open-animated, open-static, closed-static, fault-animated, fault-static
# Directions:
#   Horizontal: l2r, r2l
#   Vertical:   t2b, b2t
# ==============================================================================
def generate_manual_valve(orientation="horizontal", state="open-animated", direction="normal", fluid_pulse="#BAE6FD"):
    if state.startswith("open"):
        lever_color = "#16A34A"
        core_fill = "#DCFCE7"
        core_stroke = "#16A34A"
    elif state.startswith("fault"):
        lever_color = "#EAB308"
        core_fill = "#FEF08A"
        core_stroke = "#CA8A04"
    else:  # closed
        lever_color = "#DC2626"
        core_fill = "#FEE2E2"
        core_stroke = "#DC2626"

    flow_stream = ""
    is_animated = "animated" in state

    if is_animated and state.startswith("open"):
        if orientation == "horizontal":
            from_val = "20" if direction == "normal" else "0"
            to_val = "0" if direction == "normal" else "20"
            flow_stream = f"""
  <!-- Animated Horizontal Process Stream ({'L->R' if direction=='normal' else 'R->L'}) -->
  <line x1="6" y1="24" x2="42" y2="24" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="{from_val}" to="{to_val}" dur="0.8s" repeatCount="indefinite" />
  </line>"""
        else:
            from_val = "20" if direction == "normal" else "0"
            to_val = "0" if direction == "normal" else "20"
            flow_stream = f"""
  <!-- Animated Vertical Process Stream ({'T->B' if direction=='normal' else 'B->T'}) -->
  <line x1="24" y1="6" x2="24" y2="42" stroke="{fluid_pulse}" stroke-width="2.5" stroke-dasharray="4 6" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="{from_val}" to="{to_val}" dur="0.8s" repeatCount="indefinite" />
  </line>"""

    if orientation == "horizontal":
        if state.startswith("open"):
            lever_svg = f'<line x1="24" y1="18" x2="38" y2="18" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        elif state.startswith("fault"):
            # 45-degree intermediate position
            lever_svg = f'<line x1="24" y1="18" x2="34" y2="8" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        else:
            # Perpendicular closed position
            lever_svg = f'<line x1="24" y1="18" x2="24" y2="4" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'

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
        if state.startswith("open"):
            lever_svg = f'<line x1="18" y1="24" x2="18" y2="38" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        elif state.startswith("fault"):
            lever_svg = f'<line x1="18" y1="24" x2="8" y2="14" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'
        else:
            lever_svg = f'<line x1="18" y1="24" x2="4" y2="24" stroke="{lever_color}" stroke-width="3" stroke-linecap="round" />'

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
# Directions:
#   Horizontal: l2r, r2l
#   Vertical:   t2b, b2t
# ==============================================================================
def generate_check_valve(orientation="horizontal", is_animated=False, direction="normal", is_closed=False):
    anim_tag = ""
    arrow_color = "#DC2626" if is_closed else "#38BDF8"
    arrow_stroke = "#991B1B" if is_closed else "#0284C7"

    if is_animated and not is_closed:
        anim_tag = """
    <animate attributeName="opacity" values="0.6;1;0.6" dur="0.9s" repeatCount="indefinite" />"""

    if orientation == "horizontal":
        if direction == "normal":  # L -> R
            arrow_points = "20,20 28,24 20,28"
            flap_line = '<line x1="17" y1="20" x2="17" y2="28" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />'
        else:  # R -> L
            arrow_points = "28,20 20,24 28,28"
            flap_line = '<line x1="31" y1="20" x2="31" y2="28" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />'

        body = f"""  <!-- Horizontal Flanges -->
  <rect x="6" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="38" y="18" width="4" height="12" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="10" y="18" width="28" height="12" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Flow Direction Arrow & Internal Check Flap -->
  <polygon points="{arrow_points}" fill="{arrow_color}" stroke="{arrow_stroke}" stroke-width="0.8">{anim_tag}
  </polygon>
  {flap_line}"""
    else:
        if direction == "normal":  # T -> B
            arrow_points = "20,20 24,28 28,20"
            flap_line = '<line x1="20" y1="17" x2="28" y2="17" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />'
        else:  # B -> T
            arrow_points = "20,28 24,20 28,28"
            flap_line = '<line x1="20" y1="31" x2="28" y2="31" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" />'

        body = f"""  <!-- Vertical Flanges -->
  <rect x="18" y="6" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />
  <rect x="18" y="38" width="12" height="4" rx="1" fill="url(#metalFlangeGrad)" stroke="#64748B" stroke-width="0.8" />

  <!-- Valve Body -->
  <rect x="18" y="10" width="12" height="28" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.2" />

  <!-- Flow Direction Arrow & Internal Check Flap -->
  <polygon points="{arrow_points}" fill="{arrow_color}" stroke="{arrow_stroke}" stroke-width="0.8">{anim_tag}
  </polygon>
  {flap_line}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
{body}
</svg>"""

# ==============================================================================
# 4. MULTIPORT VALVES (FAULT / ALARM STATES)
# ==============================================================================
def generate_multiport_fault(is_animated=False, is_4port=False):
    anim_tag = ""
    if is_animated:
        anim_tag = """
      <animate attributeName="opacity" values="0.3;1;0.3" dur="0.5s" repeatCount="indefinite" />"""

    ports = """
  <!-- Top, Bottom, Left, Right Ports -->
  <rect x="20" y="2" width="8" height="6" fill="#1E293B" stroke="#475569" stroke-width="1" />
  <rect x="20" y="40" width="8" height="6" fill="#1E293B" stroke="#475569" stroke-width="1" />
  <rect x="2" y="20" width="6" height="8" fill="#1E293B" stroke="#475569" stroke-width="1" />
  <rect x="40" y="20" width="6" height="8" fill="#1E293B" stroke="#475569" stroke-width="1" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_svg}
  {ports}
  <!-- Central Rotary Valve Body -->
  <circle cx="24" cy="24" r="16" fill="#0F172A" stroke="#CA8A04" stroke-width="2" />
  <circle cx="24" cy="24" r="11" fill="#FEF08A" stroke="#EAB308" stroke-width="1.5">{anim_tag}
  </circle>

  <!-- Rotary Knob / Handle In Alarm Angle -->
  <polygon points="24,14 27,24 21,24" fill="#A16207" />
  <circle cx="24" cy="24" r="4" fill="#EAB308" stroke="#713F12" stroke-width="1" />
</svg>"""

# ==============================================================================
# BUILD DICTIONARY OF ALL FILES TO GENERATE
# ==============================================================================
files = {}

# --- A. WATER SOLENOID (V-SOL) ---
# Horizontal L2R
files["valve-water-solenoid-horizontal-open-animated.svg"] = generate_solenoid_valve("horizontal", "open-animated", "normal", "#BAE6FD")
files["valve-water-solenoid-horizontal-open-static.svg"] = generate_solenoid_valve("horizontal", "open-static", "normal")
files["valve-water-solenoid-horizontal-closed-static.svg"] = generate_solenoid_valve("horizontal", "closed-static", "normal")
files["valve-water-solenoid-horizontal-fault-animated.svg"] = generate_solenoid_valve("horizontal", "fault-animated", "normal")
files["valve-water-solenoid-horizontal-fault-static.svg"] = generate_solenoid_valve("horizontal", "fault-static", "normal")
# Horizontal Reverse R2L
files["valve-water-solenoid-horizontal-open-animated-r2l.svg"] = generate_solenoid_valve("horizontal", "open-animated", "reverse", "#BAE6FD")

# Vertical T2B
files["valve-water-solenoid-vertical-open-animated.svg"] = generate_solenoid_valve("vertical", "open-animated", "normal", "#BAE6FD")
files["valve-water-solenoid-vertical-open-static.svg"] = generate_solenoid_valve("vertical", "open-static", "normal")
files["valve-water-solenoid-vertical-closed-static.svg"] = generate_solenoid_valve("vertical", "closed-static", "normal")
files["valve-water-solenoid-vertical-fault-animated.svg"] = generate_solenoid_valve("vertical", "fault-animated", "normal")
files["valve-water-solenoid-vertical-fault-static.svg"] = generate_solenoid_valve("vertical", "fault-static", "normal")
# Vertical Reverse B2T
files["valve-water-solenoid-vertical-open-animated-b2t.svg"] = generate_solenoid_valve("vertical", "open-animated", "reverse", "#BAE6FD")


# --- B. CLARIFIER VALVE (V-CLR) ---
# Vertical T2B
files["valve-clarifier-vertical-open-animated.svg"] = generate_solenoid_valve("vertical", "open-animated", "normal", "#EFE8D0")
files["valve-clarifier-vertical-open-static.svg"] = generate_solenoid_valve("vertical", "open-static", "normal")
files["valve-clarifier-vertical-closed-static.svg"] = generate_solenoid_valve("vertical", "closed-static", "normal")
files["valve-clarifier-vertical-fault-animated.svg"] = generate_solenoid_valve("vertical", "fault-animated", "normal")
files["valve-clarifier-vertical-fault-static.svg"] = generate_solenoid_valve("vertical", "fault-static", "normal")
# Vertical Reverse B2T
files["valve-clarifier-vertical-open-animated-b2t.svg"] = generate_solenoid_valve("vertical", "open-animated", "reverse", "#EFE8D0")

# Horizontal L2R
files["valve-clarifier-horizontal-open-animated.svg"] = generate_solenoid_valve("horizontal", "open-animated", "normal", "#EFE8D0")
files["valve-clarifier-horizontal-open-static.svg"] = generate_solenoid_valve("horizontal", "open-static", "normal")
files["valve-clarifier-horizontal-closed-static.svg"] = generate_solenoid_valve("horizontal", "closed-static", "normal")
files["valve-clarifier-horizontal-fault-animated.svg"] = generate_solenoid_valve("horizontal", "fault-animated", "normal")
files["valve-clarifier-horizontal-fault-static.svg"] = generate_solenoid_valve("horizontal", "fault-static", "normal")
# Horizontal Reverse R2L
files["valve-clarifier-horizontal-open-animated-r2l.svg"] = generate_solenoid_valve("horizontal", "open-animated", "reverse", "#EFE8D0")


# --- C. GENERIC SOLENOID VALVE ---
# Horizontal L2R & R2L
files["valve-solenoid-horizontal-open-animated.svg"] = generate_solenoid_valve("horizontal", "open-animated", "normal")
files["valve-solenoid-horizontal-open-animated-r2l.svg"] = generate_solenoid_valve("horizontal", "open-animated", "reverse")
files["valve-solenoid-horizontal-open-static.svg"] = generate_solenoid_valve("horizontal", "open-static", "normal")
files["valve-solenoid-horizontal-open.svg"] = generate_solenoid_valve("horizontal", "open-static", "normal")
files["valve-solenoid-horizontal-closed-static.svg"] = generate_solenoid_valve("horizontal", "closed-static", "normal")
files["valve-solenoid-horizontal-closed.svg"] = generate_solenoid_valve("horizontal", "closed-static", "normal")
files["valve-solenoid-horizontal-fault-animated.svg"] = generate_solenoid_valve("horizontal", "fault-animated", "normal")
files["valve-solenoid-horizontal-fault-static.svg"] = generate_solenoid_valve("horizontal", "fault-static", "normal")

# Vertical T2B & B2T
files["valve-solenoid-vertical-open-animated.svg"] = generate_solenoid_valve("vertical", "open-animated", "normal")
files["valve-solenoid-vertical-open-animated-b2t.svg"] = generate_solenoid_valve("vertical", "open-animated", "reverse")
files["valve-solenoid-vertical-open-static.svg"] = generate_solenoid_valve("vertical", "open-static", "normal")
files["valve-solenoid-vertical-open.svg"] = generate_solenoid_valve("vertical", "open-static", "normal")
files["valve-solenoid-vertical-closed-static.svg"] = generate_solenoid_valve("vertical", "closed-static", "normal")
files["valve-solenoid-vertical-closed.svg"] = generate_solenoid_valve("vertical", "closed-static", "normal")
files["valve-solenoid-vertical-fault-animated.svg"] = generate_solenoid_valve("vertical", "fault-animated", "normal")
files["valve-solenoid-vertical-fault-static.svg"] = generate_solenoid_valve("vertical", "fault-static", "normal")


# --- D. MANUAL BALL VALVES ---
# Horizontal L2R & R2L
files["valve-manual-horizontal-open-animated.svg"] = generate_manual_valve("horizontal", "open-animated", "normal")
files["valve-manual-horizontal-open-animated-r2l.svg"] = generate_manual_valve("horizontal", "open-animated", "reverse")
files["valve-manual-horizontal-open-static.svg"] = generate_manual_valve("horizontal", "open-static", "normal")
files["valve-manual-horizontal-open.svg"] = generate_manual_valve("horizontal", "open-static", "normal")
files["valve-manual-horizontal-closed-static.svg"] = generate_manual_valve("horizontal", "closed-static", "normal")
files["valve-manual-horizontal-closed.svg"] = generate_manual_valve("horizontal", "closed-static", "normal")
files["valve-manual-horizontal-fault-animated.svg"] = generate_manual_valve("horizontal", "fault-animated", "normal")
files["valve-manual-horizontal-fault-static.svg"] = generate_manual_valve("horizontal", "fault-static", "normal")

# Vertical T2B & B2T
files["valve-manual-vertical-open-animated.svg"] = generate_manual_valve("vertical", "open-animated", "normal")
files["valve-manual-vertical-open-animated-b2t.svg"] = generate_manual_valve("vertical", "open-animated", "reverse")
files["valve-manual-vertical-open-static.svg"] = generate_manual_valve("vertical", "open-static", "normal")
files["valve-manual-vertical-open.svg"] = generate_manual_valve("vertical", "open-static", "normal")
files["valve-manual-vertical-closed-static.svg"] = generate_manual_valve("vertical", "closed-static", "normal")
files["valve-manual-vertical-closed.svg"] = generate_manual_valve("vertical", "closed-static", "normal")
files["valve-manual-vertical-fault-animated.svg"] = generate_manual_valve("vertical", "fault-animated", "normal")
files["valve-manual-vertical-fault-static.svg"] = generate_manual_valve("vertical", "fault-static", "normal")


# --- E. CHECK VALVES (NRV) ---
# Horizontal (L2R & R2L)
files["valve-check-horizontal-open-animated.svg"] = generate_check_valve("horizontal", is_animated=True, direction="normal")
files["valve-check-horizontal-open-static.svg"] = generate_check_valve("horizontal", is_animated=False, direction="normal")
files["valve-check-horizontal.svg"] = generate_check_valve("horizontal", is_animated=False, direction="normal")
files["valve-check-horizontal-closed-static.svg"] = generate_check_valve("horizontal", is_animated=False, direction="normal", is_closed=True)

files["valve-check-horizontal-reverse-open-animated.svg"] = generate_check_valve("horizontal", is_animated=True, direction="reverse")
files["valve-check-horizontal-reverse-open-static.svg"] = generate_check_valve("horizontal", is_animated=False, direction="reverse")
files["valve-check-horizontal-reverse-closed-static.svg"] = generate_check_valve("horizontal", is_animated=False, direction="reverse", is_closed=True)

# Vertical (T2B & B2T)
files["valve-check-vertical-open-animated.svg"] = generate_check_valve("vertical", is_animated=True, direction="normal")
files["valve-check-vertical-open-static.svg"] = generate_check_valve("vertical", is_animated=False, direction="normal")
files["valve-check-vertical.svg"] = generate_check_valve("vertical", is_animated=False, direction="normal")
files["valve-check-vertical-closed-static.svg"] = generate_check_valve("vertical", is_animated=False, direction="normal", is_closed=True)

files["valve-check-vertical-reverse-open-animated.svg"] = generate_check_valve("vertical", is_animated=True, direction="reverse")
files["valve-check-vertical-reverse-open-static.svg"] = generate_check_valve("vertical", is_animated=False, direction="reverse")
files["valve-check-vertical-reverse-closed-static.svg"] = generate_check_valve("vertical", is_animated=False, direction="reverse", is_closed=True)


# --- F. MULTIPORT FAULT / ALARM STATES ---
files["multiport-valve-fault-animated.svg"] = generate_multiport_fault(is_animated=True)
files["multiport-valve-fault-static.svg"] = generate_multiport_fault(is_animated=False)
files["multiport-valve-4port-fault-animated.svg"] = generate_multiport_fault(is_animated=True, is_4port=True)
files["multiport-valve-4port-fault-static.svg"] = generate_multiport_fault(is_animated=False, is_4port=True)

# Write all files
count = 0
for fname, content in files.items():
    fpath = os.path.join(output_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

print(f"Generated {count} valve scenario SVGs successfully.")
