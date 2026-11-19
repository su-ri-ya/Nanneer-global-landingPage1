import os

# Base paths
blower_dir = os.path.join("public", "schematic asserts", "blower")
vessel_dir = os.path.join("public", "schematic asserts", "vessel")
valve_dir = os.path.join("public", "schematic asserts", "valve")

os.makedirs(blower_dir, exist_ok=True)
os.makedirs(vessel_dir, exist_ok=True)
os.makedirs(valve_dir, exist_ok=True)

# ==============================================================================
# 1. BLOWERS (public/schematic asserts/blower)
# Exact geometry from components/ScadaSchematicSimulation.tsx (No corner dot)
# ==============================================================================
def generate_blower_svg(is_running=True, is_animated=False):
    fill_inner = "#DCFCE7" if is_running else "#FCE7F3"
    stroke_inner = "#16A34A" if is_running else "#F43F5E"
    blade_stroke = "#15803D" if is_running else "#BE123C"
    blade_width = "1.8" if is_running else "1.6"

    anim = ""
    if is_running and is_animated:
        anim = '        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.8s" repeatCount="indefinite" />\n'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40">
  <defs>
    <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>
  </defs>
  <g transform="translate(20, 20)">
    <!-- 1. Outer CNC Flange Volute Ring -->
    <circle cx="0" cy="0" r="14" fill="url(#metalRingGrad)" stroke="{stroke_inner}" stroke-width="1" />
    
    <!-- 2. Inner Blower Chamber -->
    <circle cx="0" cy="0" r="11" fill="{fill_inner}" stroke="{stroke_inner}" stroke-width="1.8" />
    
    <!-- 3. 8-Blade Blower Rotor -->
    <g>
{anim}      <path d="M -6 0 L 6 0 M 0 -6 L 0 6 M -4 -4 L 4 4 M -4 4 L 4 -4" stroke="{blade_stroke}" stroke-width="{blade_width}" stroke-linecap="round" />
    </g>
  </g>
</svg>"""

# ==============================================================================
# 2. FILTRATION VESSELS (public/schematic asserts/vessel)
# Option 3: Precision Industrial ASME Standard (PSF, ACF, Softener)
# ==============================================================================
def generate_vessel_svg(vessel_type="PSF"):
    # Coordinates & gauge text per vessel type
    manifold_x = 14 if vessel_type == "PSF" else 58 if vessel_type == "ACF" else 36
    gauge_x = 62 if vessel_type == "PSF" else 20 if vessel_type == "ACF" else 62
    gauge_val = "2.80B" if vessel_type == "PSF" else "2.10B" if vessel_type == "ACF" else "12ppm"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 130" width="84" height="130">
  <defs>
    <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0369A1" />
      <stop offset="25%" stop-color="#38BDF8" />
      <stop offset="50%" stop-color="#0284C7" />
      <stop offset="85%" stop-color="#0369A1" />
      <stop offset="100%" stop-color="#075985" />
    </linearGradient>
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.35" />
      <stop offset="30%" stop-color="#FFFFFF" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </linearGradient>
  </defs>

  <g transform="translate(1, 0)">
    <!-- Structural Stand / Base Legs -->
    <g id="vessel-stand">
      <!-- Left Structural Support Leg & Gusset Bracket -->
      <polygon points="10,102 10,112 4,102" fill="#0369A1" stroke="#0284C7" stroke-width="1" />
      <rect x="10" y="102" width="6" height="22" rx="1" fill="#075985" stroke="#0284C7" stroke-width="1.2" />
      <rect x="6" y="123" width="14" height="3" rx="1" fill="#0F172A" stroke="#38BDF8" stroke-width="1" />
      <circle cx="8" cy="124.5" r="0.8" fill="#FFFFFF" />
      <circle cx="18" cy="124.5" r="0.8" fill="#FFFFFF" />

      <!-- Right Structural Support Leg & Gusset Bracket -->
      <polygon points="72,102 72,112 78,102" fill="#0369A1" stroke="#0284C7" stroke-width="1" />
      <rect x="66" y="102" width="6" height="22" rx="1" fill="#075985" stroke="#0284C7" stroke-width="1.2" />
      <rect x="62" y="123" width="14" height="3" rx="1" fill="#0F172A" stroke="#38BDF8" stroke-width="1" />
      <circle cx="64" cy="124.5" r="0.8" fill="#FFFFFF" />
      <circle cx="74" cy="124.5" r="0.8" fill="#FFFFFF" />

      <!-- Horizontal Cross-Tie Stabilizer Beam -->
      <line x1="16" y1="117" x2="66" y2="117" stroke="#0284C7" stroke-width="1.8" />

      <!-- Bottom Drain Outlet Nozzle Flange -->
      <rect x="38" y="113" width="6" height="7" fill="#CBD5E1" stroke="#0284C7" stroke-width="1" />
      <line x1="35" y1="120" x2="47" y2="120" stroke="#0284C7" stroke-width="1.5" />
    </g>

    <!-- ASME Steel Shell -->
    <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2.2" />
    <rect x="1" y="22" width="80" height="78" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2.2" />
    <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2.2" />

    <!-- Heavy Girth Weld Seams -->
    <line x1="1" y1="32" x2="81" y2="32" stroke="#38BDF8" stroke-width="1.8" stroke-dasharray="3 2" />
    <line x1="1" y1="92" x2="81" y2="92" stroke="#38BDF8" stroke-width="1.8" stroke-dasharray="3 2" />

    <!-- Top Flanged Inspection Manway Hatch -->
    <rect x="30" y="2" width="22" height="6" rx="1.5" fill="#CBD5E1" stroke="#0284C7" stroke-width="1.2" />
    <circle cx="34" cy="5" r="0.9" fill="#475569" />
    <circle cx="41" cy="5" r="0.9" fill="#475569" />
    <circle cx="48" cy="5" r="0.9" fill="#475569" />

    <!-- Frontal 5-Valve Manifold Pipe Tree -->
    <g transform="translate({manifold_x}, 36)">
      <line x1="0" y1="0" x2="0" y2="52" stroke="#0284C7" stroke-width="3" />
      <circle cx="0" cy="10" r="4.5" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.2" />
      <polygon points="-3,10 0,7 3,10" fill="#15803D" />
      <circle cx="0" cy="42" r="4.5" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.2" />
      <polygon points="-3,42 0,45 3,42" fill="#15803D" />
    </g>

    <!-- Dial Pressure / Hardness Gauge -->
    <g transform="translate({gauge_x}, 28)">
      <circle cx="0" cy="0" r="7.5" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
      <circle cx="0" cy="0" r="6" fill="#F0F9FF" />
      <line x1="0" y1="0" x2="3.5" y2="-3" stroke="#DC2626" stroke-width="1" />
      <circle cx="0" cy="0" r="1.2" fill="#0F172A" />
      <text x="0" y="12" text-anchor="middle" fill="#0369A1" font-size="5" font-weight="bold" font-family="monospace">
        {gauge_val}
      </text>
    </g>

    <!-- Specular Reflection Sheen -->
    <rect x="5" y="10" width="8" height="96" rx="2" fill="url(#specularSheen)" opacity="0.5" />
  </g>
</svg>"""

# ==============================================================================
# 3. UKL 4-PORT MULTIPORT VALVE (public/schematic asserts/valve)
# Exact geometry from components/ScadaSchematicSimulation.tsx
# ==============================================================================
def generate_mpv_svg(mode="SERVICE", is_animated=False):
    angle_map = {
        "SERVICE": 0,
        "DRAIN": 90,
        "BACKWASH": 180,
        "RINSE": 270,
    }
    angle = angle_map.get(mode, 0)

    fluid_anim = ""
    if is_animated and mode == "SERVICE":
        fluid_anim = """    <!-- Animated Fluid Flow Stream (Service Downflow) -->
    <circle cx="30" cy="30" r="14.2" fill="none" stroke="#38BDF8" stroke-width="1" opacity="0.3">
      <animate attributeName="opacity" values="0.15;0.7;0.15" dur="1.8s" repeatCount="indefinite" />
    </circle>
    <g>
      <path d="M 30 10 L 30 23 M 30 37 L 30 50" stroke="#BAE6FD" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="3 3">
        <animate attributeName="stroke-dashoffset" from="12" to="0" dur="0.8s" repeatCount="indefinite" />
      </path>
      <circle cx="30" cy="30" r="5" fill="#38BDF8" opacity="0.2">
        <animate attributeName="r" values="3;6;3" dur="1.2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.3;0.1;0.3" dur="1.2s" repeatCount="indefinite" />
      </circle>
    </g>"""
    elif is_animated and (mode in ["BACKWASH", "RINSE", "DRAIN"]):
        fluid_anim = """    <!-- Animated Fluid Flow Stream (Flush to Drain) -->
    <path d="M 30 30 L 50 30" stroke="#FCA5A5" stroke-width="2" stroke-linecap="round" stroke-dasharray="3 3">
      <animate attributeName="stroke-dashoffset" from="12" to="0" dur="0.8s" repeatCount="indefinite" />
    </path>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <defs>
    <radialGradient id="mpvCasingGrad" cx="45%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#27272A" />
      <stop offset="60%" stop-color="#18181B" />
      <stop offset="100%" stop-color="#09090B" />
    </radialGradient>
    <linearGradient id="mpvDialGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8" />
      <stop offset="30%" stop-color="#0284C7" />
      <stop offset="85%" stop-color="#1D4ED8" />
      <stop offset="100%" stop-color="#1E3A8A" />
    </linearGradient>
    <linearGradient id="mpvBoltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="mpvHandleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3F3F46" />
      <stop offset="45%" stop-color="#27272A" />
      <stop offset="100%" stop-color="#18181B" />
    </linearGradient>
  </defs>

  <!-- 4 Threaded Pipe Union Nozzles (Orthogonal 4-Way Configuration) -->
  <!-- Port 1: Top (12 o'clock - Inlet) -->
  <g id="p1-top">
    <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" stroke-width="0.8" />
    <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" stroke-width="0.6" />
  </g>

  <!-- Port 2: Bottom (6 o'clock - Filtered Outlet) -->
  <g id="p2-bottom" transform="rotate(180 30 30)">
    <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" stroke-width="0.8" />
    <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" stroke-width="0.6" />
  </g>

  <!-- Port 3: Left (9 o'clock - Manifold Connection / Drain) -->
  <g id="p3-left" transform="rotate(270 30 30)">
    <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" stroke-width="0.8" />
    <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" stroke-width="0.6" />
  </g>

  <!-- Port 4: Right (3 o'clock - Drain / Manifold) -->
  <g id="p4-right" transform="rotate(90 30 30)">
    <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181B" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="5" x2="36" y2="5" stroke="#3F3F46" stroke-width="0.8" />
    <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3F3F46" stroke-width="0.8" />
    <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272A" stroke="#09090B" stroke-width="0.8" />
    <line x1="24" y1="8" x2="24" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="30" y1="8" x2="30" y2="13" stroke="#3F3F46" stroke-width="0.6" />
    <line x1="36" y1="8" x2="36" y2="13" stroke="#3F3F46" stroke-width="0.6" />
  </g>

  <!-- Main Outer Casing Flange Body -->
  <circle cx="30" cy="30" r="23" fill="url(#mpvCasingGrad)" stroke="#3F3F46" stroke-width="1.2" />
  <circle cx="30" cy="30" r="21.5" fill="none" stroke="#18181B" stroke-width="1" />

  <!-- 12 Flange Perimeter Hex Bolts -->
  <circle cx="49.2" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="49.0" cy="29.8" r="0.4" fill="#FFFFFF" />
  <circle cx="46.6" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="46.4" cy="39.4" r="0.4" fill="#FFFFFF" />
  <circle cx="39.6" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="39.4" cy="46.4" r="0.4" fill="#FFFFFF" />
  <circle cx="30" cy="49.2" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="29.8" cy="49.0" r="0.4" fill="#FFFFFF" />
  <circle cx="20.4" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="20.2" cy="46.4" r="0.4" fill="#FFFFFF" />
  <circle cx="13.4" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="13.2" cy="39.4" r="0.4" fill="#FFFFFF" />
  <circle cx="10.8" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="10.6" cy="29.8" r="0.4" fill="#FFFFFF" />
  <circle cx="13.4" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="13.2" cy="20.2" r="0.4" fill="#FFFFFF" />
  <circle cx="20.4" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="20.2" cy="13.2" r="0.4" fill="#FFFFFF" />
  <circle cx="30" cy="10.8" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="29.8" cy="10.6" r="0.4" fill="#FFFFFF" />
  <circle cx="39.6" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="39.4" cy="13.2" r="0.4" fill="#FFFFFF" />
  <circle cx="46.6" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
  <circle cx="46.4" cy="20.2" r="0.4" fill="#FFFFFF" />

  <!-- Inner Bezel Ring -->
  <circle cx="30" cy="30" r="16" fill="#09090B" stroke="#27272A" stroke-width="0.8" />

  <!-- Blue Dial Plate Face -->
  <circle cx="30" cy="30" r="14.8" fill="url(#mpvDialGrad)" stroke="#38BDF8" stroke-width="0.6" />
  <circle cx="30" cy="30" r="13.6" fill="none" stroke="#60A5FA" stroke-width="0.4" stroke-opacity="0.5" />

{fluid_anim}

  <!-- 4 Dial Cycle Step Markings -->
  <!-- 1. Top (0°): SERVICE -->
  <g transform="rotate(0 30 30)">
    <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
  </g>

  <!-- 2. Right (90°): DRAIN -->
  <g transform="rotate(90 30 30)">
    <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
  </g>

  <!-- 3. Bottom (180°): BACKWASH -->
  <g transform="rotate(180 30 30)">
    <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
  </g>

  <!-- 4. Left (270°): RINSE -->
  <g transform="rotate(270 30 30)">
    <polygon points="30,16.5 28,18.8 32,18.8" fill="#FACC15" />
  </g>

  <!-- Central Rotor Boss -->
  <circle cx="30" cy="30" r="7" fill="#18181B" stroke="#09090B" stroke-width="1" />

  <!-- Rotary Selector Handle Lever -->
  <g transform="rotate({angle} 30 30)">
    <path d="M 28 30 L 27.5 22 L 25 12 C 25 8.5 35 8.5 35 12 L 32.5 22 L 32 30 Z" fill="url(#mpvHandleGrad)" stroke="#09090B" stroke-width="0.8" />
    <line x1="30" y1="11" x2="30" y2="24" stroke="#52525B" stroke-width="0.7" stroke-linecap="round" />
    <polygon points="30,8.5 28.8,11 31.2,11" fill="#FACC15" />
    <circle cx="30" cy="30" r="3.6" fill="#18181B" stroke="#3F3F46" stroke-width="0.7" />
    <circle cx="30" cy="30" r="1.8" fill="url(#mpvBoltGrad)" stroke="#475569" stroke-width="0.3" />
    <circle cx="29.5" cy="29.5" r="0.5" fill="#FFFFFF" />
  </g>
</svg>"""

print("=== GENERATING FINALIZED BLOWERS, VESSELS & VALVES SVGS ===")

# 1. Blowers
blower_combos = [
    ("blower-running-animated.svg", True, True),
    ("blower-running-static.svg", True, False),
    ("blower-stopped-static.svg", False, False),
]
for fname, is_run, is_anim in blower_combos:
    fpath = os.path.join(blower_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(generate_blower_svg(is_run, is_anim))
    print(f"  + Generated blower: {fname}")

# 2. Vessels
vessel_combos = [
    ("psf-vessel.svg", "PSF"),
    ("acf-vessel.svg", "ACF"),
    ("softener-vessel.svg", "SOFTENER"),
]
for fname, vtype in vessel_combos:
    fpath = os.path.join(vessel_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(generate_vessel_svg(vtype))
    print(f"  + Generated vessel: {fname}")

# 3. Multiport Valves
valve_combos = [
    ("multiport-valve-service-animated.svg", "SERVICE", True),
    ("multiport-valve-service-static.svg", "SERVICE", False),
    ("multiport-valve-drain-static.svg", "DRAIN", False),
    ("multiport-valve-backwash-static.svg", "BACKWASH", False),
    ("multiport-valve-rinse-static.svg", "RINSE", False),
]
for fname, mode, is_anim in valve_combos:
    fpath = os.path.join(valve_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(generate_mpv_svg(mode, is_anim))
    print(f"  + Generated valve: {fname}")

print(f"\nDone! All blowers, vessels, and multiport valves generated strictly matching the schematic.")
