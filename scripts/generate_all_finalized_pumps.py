import os
import math

output_dir = os.path.join("public", "schematic asserts", "pump")
os.makedirs(output_dir, exist_ok=True)

# Shared Flange Gradient
defs_metal_ring = """  <defs>
    <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>
  </defs>"""

# ==============================================================================
# 1. CENTRIFUGAL PUMPS (Flow Right, Left, Down, Up, Standalone)
# ==============================================================================
def generate_pump_svg(direction=None, is_running=True, is_animated=False):
    glass_bg = "#064E3B" if is_running else "#450A0A"
    glass_border = "#22C55E" if is_running else "#EF4444"
    vane_stroke = "#86EFAC" if is_running else "#FCA5A5"
    vane_sub_stroke = "#4ADE80" if is_running else "#F87171"
    hub_color = "#16A34A" if is_running else "#DC2626"
    arrow_color = "#16A34A" if is_running else "#DC2626"

    bolts = []
    for deg in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(deg)
        bx = round(12.5 * math.cos(rad), 2)
        by = round(12.5 * math.sin(rad), 2)
        bolts.append(f'      <circle cx="{bx}" cy="{by}" r="0.75" fill="#1E293B" stroke="#94A3B8" stroke-width="0.3" />')
    bolts_svg = "\n".join(bolts)

    bubbles_svg = ""
    if is_running:
        bubbles_svg = """        <circle cx="4" cy="3" r="0.6" fill="#FFFFFF" opacity="0.9" />
        <circle cx="-5" cy="4" r="0.5" fill="#FFFFFF" opacity="0.8" />
        <circle cx="6" cy="-5" r="0.7" fill="#FFFFFF" opacity="0.9" />
        <circle cx="-4" cy="-6" r="0.5" fill="#FFFFFF" opacity="0.8" />"""

    anim_svg = ""
    if is_running and is_animated:
        anim_svg = '        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.9s" repeatCount="indefinite" />\n'

    arrow_svg = ""
    if direction == "right":
        arrow_svg = f'    <!-- Flow Direction Arrow (Right) -->\n    <polygon points="14,-3 20,0 14,3" fill="{arrow_color}" />\n'
    elif direction == "left":
        arrow_svg = f'    <!-- Flow Direction Arrow (Left) -->\n    <polygon points="-14,-3 -20,0 -14,3" fill="{arrow_color}" />\n'
    elif direction == "down":
        arrow_svg = f'    <!-- Flow Direction Arrow (Down) -->\n    <polygon points="-3,14 0,20 3,14" fill="{arrow_color}" />\n'
    elif direction == "up":
        arrow_svg = f'    <!-- Flow Direction Arrow (Up) -->\n    <polygon points="-3,-14 0,-20 3,-14" fill="{arrow_color}" />\n'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
{defs_metal_ring}

  <g transform="translate(24, 24)">
    <!-- 1. Outer CNC Flange Volute Ring -->
    <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="#64748B" stroke-width="1" />

    <!-- Peripheral Flange Bolt Studs -->
{bolts_svg}

    <!-- 2. Optical Polycarbonate Sight-Glass Chamber -->
    <circle cx="0" cy="0" r="11" fill="{glass_bg}" stroke="{glass_border}" stroke-width="1.4" />

    <!-- 3. Centrifugal Fluid Vortex Impeller Dynamics -->
    <g>
{anim_svg}      <!-- Hydrodynamic Swirl Vanes -->
      <path d="M 0 0 C 3 3, 6 1, 9 7" stroke="{vane_stroke}" stroke-width="1" fill="none" opacity="0.9" />
      <path d="M 0 0 C -3 -3, -6 -1, -9 -7" stroke="{vane_stroke}" stroke-width="1" fill="none" opacity="0.9" />
      <path d="M 0 0 C 3 -3, 1 -6, 7 -9" stroke="{vane_sub_stroke}" stroke-width="0.9" fill="none" opacity="0.8" />
      <path d="M 0 0 C -3 3, -1 6, -7 9" stroke="{vane_sub_stroke}" stroke-width="0.9" fill="none" opacity="0.8" />
{bubbles_svg}
      <!-- Center Drive Shaft Impeller Hub -->
      <circle cx="0" cy="0" r="2.4" fill="{hub_color}" stroke="#FFFFFF" stroke-width="0.6" />
    </g>

    <!-- 4. Optical Specular Reflection Glare Arch across Upper Dome -->
    <path d="M -8.5 -5 A 9.5 9.5 0 0 1 8.5 -5" stroke="#FFFFFF" stroke-width="1.2" fill="none" opacity="0.65" stroke-linecap="round" />

{arrow_svg}  </g>
</svg>"""

# ==============================================================================
# 2. PRECISION SOLENOID DIAPHRAGM METERING PUMPS (Universal & Directional)
# ==============================================================================
def generate_dosing_pump_svg(injection_dir=None, is_running=True, is_animated=False):
    glass_bg = "#064E3B" if is_running else "#450A0A"
    glass_border = "#22C55E" if is_running else "#EF4444"
    status_color = "#16A34A" if is_running else "#DC2626"
    pulse_anim = ""
    if is_running and is_animated:
        pulse_anim = """        <animate attributeName="r" values="3.2; 5.2; 3.2" dur="0.75s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.7; 1; 0.7" dur="0.75s" repeatCount="indefinite" />"""

    # Directional Arrows
    arrow_svg = ""
    if injection_dir == "down":
        arrow_svg = f"""  <!-- Downward Injection Arrow into Pipeline Below -->
  <polygon points="12,41 15,46 18,41" fill="{status_color}" />"""
    elif injection_dir == "up":
        arrow_svg = f"""  <!-- Upward Injection Arrow into Overhead Pipeline -->
  <polygon points="15,2 12,7 18,7" fill="{status_color}" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <defs>
    <linearGradient id="dosingMetalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>
  </defs>

  <!-- Base Mounting Foot Bracket -->
  <rect x="22" y="34" width="18" height="4" rx="1" fill="#334155" stroke="#0F172A" stroke-width="0.8" />
  <circle cx="25" cy="36" r="0.9" fill="#94A3B8" />
  <circle cx="37" cy="36" r="0.9" fill="#94A3B8" />

  <!-- Heavy-Duty Chemical-Resistant Solenoid Drive Enclosure -->
  <rect x="22" y="14" width="18" height="20" rx="3" fill="#1E293B" stroke="#64748B" stroke-width="1" />
  
  <!-- Rear Motor Heat Dissipation Fins -->
  <line x1="33" y1="17" x2="33" y2="31" stroke="#334155" stroke-width="1.2" />
  <line x1="36" y1="17" x2="36" y2="31" stroke="#334155" stroke-width="1.2" />

  <!-- Electronic Stroke Control Dial / Knob -->
  <circle cx="27" cy="24" r="3.2" fill="#0F172A" stroke="#94A3B8" stroke-width="0.8" />
  <circle cx="27" cy="24" r="1.4" fill="{status_color}" />

  <!-- Top Nozzle Port (Injection Fitting) -->
  <rect x="12" y="5" width="6" height="8" rx="1" fill="#475569" stroke="#94A3B8" stroke-width="0.8" />
  <rect x="11" y="9" width="8" height="4" rx="0.5" fill="#334155" stroke="#64748B" stroke-width="0.8" />

  <!-- Bottom Nozzle Port (Chemical Intake Fitting) -->
  <rect x="12" y="35" width="6" height="8" rx="1" fill="#475569" stroke="#94A3B8" stroke-width="0.8" />
  <rect x="11" y="35" width="8" height="4" rx="0.5" fill="#334155" stroke="#64748B" stroke-width="0.8" />

{arrow_svg}

  <!-- Manual Degassing / Priming Relief Valve Knob -->
  <rect x="6" y="9" width="4" height="4" rx="1" fill="#D97706" stroke="#B45309" stroke-width="0.6" />

  <!-- PVDF Transparent Chemical Liquid-End Dosing Head Block -->
  <rect x="8" y="13" width="14" height="22" rx="2.5" fill="url(#dosingMetalGrad)" stroke="#0284C7" stroke-width="1.2" />

  <!-- Optical Diaphragm Stroke Sight Chamber -->
  <circle cx="15" cy="24" r="7" fill="{glass_bg}" stroke="{glass_border}" stroke-width="1.2" />
  
  <!-- Reciprocating Diaphragm Stroke Core -->
  <circle cx="15" cy="24" r="4.2" fill="{status_color}" stroke="#FFFFFF" stroke-width="0.6">
{pulse_anim}
  </circle>

  <!-- Specular Sheen Glare Arc -->
  <path d="M 10 21 A 5.5 5.5 0 0 1 20 21" stroke="#FFFFFF" stroke-width="1" fill="none" opacity="0.6" stroke-linecap="round" />
</svg>"""

combinations = [
    # Centrifugal: Flow Right (M1, M2, M12)
    ("pump-flow-right-running-animated.svg", "right", True, True),
    ("pump-flow-right-running-static.svg", "right", True, False),
    ("pump-flow-right-stopped-static.svg", "right", False, False),

    # Centrifugal: Flow Left (M3, M4)
    ("pump-flow-left-running-animated.svg", "left", True, True),
    ("pump-flow-left-running-static.svg", "left", True, False),
    ("pump-flow-left-stopped-static.svg", "left", False, False),

    # Centrifugal: Flow Down (M10, M11)
    ("pump-flow-down-running-animated.svg", "down", True, True),
    ("pump-flow-down-running-static.svg", "down", True, False),
    ("pump-flow-down-stopped-static.svg", "down", False, False),

    # Centrifugal: Flow Up (Universal Upward Flow)
    ("pump-flow-up-running-animated.svg", "up", True, True),
    ("pump-flow-up-running-static.svg", "up", True, False),
    ("pump-flow-up-stopped-static.svg", "up", False, False),

    # Centrifugal: Standalone (No Arrow)
    ("pump-running-animated.svg", None, True, True),
    ("pump-running-static.svg", None, True, False),
    ("pump-stopped-static.svg", None, False, False),
]

dosing_combinations = [
    # Dosing: Universal Clean (No Arrows - connects to any pipe direction)
    ("dosing-pump-running-animated.svg", None, True, True),
    ("dosing-pump-running-static.svg", None, True, False),
    ("dosing-pump-stopped-static.svg", None, False, False),

    # Dosing: Inject Down (Injecting downward into pipe below)
    ("dosing-pump-inject-down-running-animated.svg", "down", True, True),
    ("dosing-pump-inject-down-running-static.svg", "down", True, False),
    ("dosing-pump-inject-down-stopped-static.svg", "down", False, False),

    # Dosing: Inject Up (Injecting upward into overhead pipe)
    ("dosing-pump-inject-up-running-animated.svg", "up", True, True),
    ("dosing-pump-inject-up-running-static.svg", "up", True, False),
    ("dosing-pump-inject-up-stopped-static.svg", "up", False, False),
]

print("=== GENERATING 100% UNIVERSAL PUMP & DOSING MATRIX ===")
for filename, direction, is_running, is_animated in combinations:
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generate_pump_svg(direction, is_running, is_animated))
    print(f"  + Generated centrifugal pump: {filename}")

for filename, direction, is_running, is_animated in dosing_combinations:
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generate_dosing_pump_svg(direction, is_running, is_animated))
    print(f"  + Generated dosing pump: {filename}")

print(f"\nDone! Successfully generated {len(combinations) + len(dosing_combinations)} universal pump SVGs in '{output_dir}'.")
