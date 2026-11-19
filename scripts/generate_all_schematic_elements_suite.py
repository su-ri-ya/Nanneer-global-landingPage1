import os
import zipfile
import xml.etree.ElementTree as ET

BASE_DIR = 'public/schematic asserts'
VALVES_DIR = os.path.join(BASE_DIR, 'valve')
TANKS_DIR = os.path.join(BASE_DIR, 'tank')
PUMPS_DIR = os.path.join(BASE_DIR, 'pump')
FILTERS_DIR = os.path.join(BASE_DIR, 'vessel')
INSTRUMENTS_DIR = os.path.join(BASE_DIR, 'blower')
UTILITY_DIR = os.path.join(BASE_DIR, 'utility')

for d in [VALVES_DIR, TANKS_DIR, PUMPS_DIR, FILTERS_DIR, INSTRUMENTS_DIR, UTILITY_DIR]:
    os.makedirs(d, exist_ok=True)

# Common SVG definitions
COMMON_DEFS = """  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
    <linearGradient id="glassCylinderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.5" />
      <stop offset="8%" stop-color="#ffffff" stop-opacity="0.85" />
      <stop offset="22%" stop-color="#f8fafc" stop-opacity="0.3" />
      <stop offset="70%" stop-color="#e0f2fe" stop-opacity="0.2" />
      <stop offset="92%" stop-color="#38bdf8" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.5" />
    </linearGradient>
    <linearGradient id="glassRimGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#94a3b8" stop-opacity="0.8" />
      <stop offset="25%" stop-color="#ffffff" stop-opacity="0.95" />
      <stop offset="70%" stop-color="#e2e8f0" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#64748b" stop-opacity="0.9" />
    </linearGradient>
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.35" />
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    {custom_defs}
  </defs>"""

# --------------------------------------------------------------------------------------------------
# 1. 4-PORT MULTIPORT VALVE (MPV) & DUAL MANIFOLDS
# --------------------------------------------------------------------------------------------------
def generate_4port_multiport_valves():
    print("Generating 4-Port Multiport Valves...")
    mpv_defs = """
    <radialGradient id="mpvCasingGrad" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#27272a" />
      <stop offset="60%" stop-color="#18181b" />
      <stop offset="100%" stop-color="#09090b" />
    </radialGradient>
    <radialGradient id="mpvDialGrad" cx="35%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="70%" stop-color="#0369a1" />
      <stop offset="100%" stop-color="#075985" />
    </radialGradient>
    <linearGradient id="mpvBoltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="50%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="mpvHandleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3f3f46" />
      <stop offset="35%" stop-color="#27272a" />
      <stop offset="70%" stop-color="#18181b" />
      <stop offset="100%" stop-color="#09090b" />
    </linearGradient>
    """

    # Angles: SERVICE=0, DRAIN=90, BACKWASH=180, RINSE=270
    modes = [
        ("service", 0, "SERVICE", "downflow"),
        ("drain", 90, "DRAIN", "rightflow"),
        ("backwash", 180, "BACKWASH", "rightflow"),
        ("rinse", 270, "RINSE", "rightflow")
    ]

    for mode_name, angle, label, flow_type in modes:
        for is_anim in [False, True]:
            state_str = "animated" if is_anim else "static"
            fname = f"multiport-valve-4port-{mode_name}-{state_str}.svg"

            flow_markup = ""
            if is_anim:
                if flow_type == "downflow":
                    flow_markup = """
      <path d="M 100 35 L 100 80 M 100 120 L 100 165" stroke="#bae6fd" stroke-width="5" stroke-linecap="round" stroke-dasharray="8 8">
        <animate attributeName="stroke-dashoffset" from="32" to="0" dur="0.8s" repeatCount="indefinite" />
      </path>
      <circle cx="100" cy="100" r="16" fill="#38bdf8" opacity="0.25">
        <animate attributeName="r" values="10;18;10" dur="1.2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.35;0.1;0.35" dur="1.2s" repeatCount="indefinite" />
      </circle>
                    """
                else: # rightflow to drain
                    flow_markup = """
      <path d="M 100 100 L 165 100" stroke="#fca5a5" stroke-width="6" stroke-linecap="round" stroke-dasharray="8 8">
        <animate attributeName="stroke-dashoffset" from="32" to="0" dur="0.8s" repeatCount="indefinite" />
      </path>
      <circle cx="100" cy="100" r="14" fill="#ef4444" opacity="0.25">
        <animate attributeName="r" values="8;16;8" dur="1.0s" repeatCount="indefinite" />
      </circle>
                    """

            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    {mpv_defs}
  </defs>

  <!-- 3D Grounding Drop Shadow -->
  <circle cx="100" cy="104" r="76" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(100, 100) scale(2.4) translate(-30, -30)">
    <!-- 4 Threaded Pipe Union Nozzles (Orthogonal: Top, Bottom, Left, Right) -->
    <!-- Port 1: Top Nozzle (12 o'clock) -->
    <g id="p1-top">
      <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181b" stroke="#09090b" stroke-width="0.8" />
      <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="5" x2="36" y2="5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3f3f46" stroke-width="0.8" />
      <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272a" stroke="#09090b" stroke-width="0.8" />
    </g>

    <!-- Port 2: Bottom Nozzle (6 o'clock) -->
    <g id="p2-bottom" transform="rotate(180 30 30)">
      <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181b" stroke="#09090b" stroke-width="0.8" />
      <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="5" x2="36" y2="5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3f3f46" stroke-width="0.8" />
      <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272a" stroke="#09090b" stroke-width="0.8" />
    </g>

    <!-- Port 3: Left Nozzle (9 o'clock) -->
    <g id="p3-left" transform="rotate(270 30 30)">
      <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181b" stroke="#09090b" stroke-width="0.8" />
      <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="5" x2="36" y2="5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3f3f46" stroke-width="0.8" />
      <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272a" stroke="#09090b" stroke-width="0.8" />
    </g>

    <!-- Port 4: Right Nozzle (3 o'clock) -->
    <g id="p4-right" transform="rotate(90 30 30)">
      <rect x="23" y="0" width="14" height="10" rx="1" fill="#18181b" stroke="#09090b" stroke-width="0.8" />
      <line x1="24" y1="2.5" x2="36" y2="2.5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="5" x2="36" y2="5" stroke="#3f3f46" stroke-width="0.8" />
      <line x1="24" y1="7.5" x2="36" y2="7.5" stroke="#3f3f46" stroke-width="0.8" />
      <rect x="20.5" y="8" width="19" height="5" rx="1.5" fill="#27272a" stroke="#09090b" stroke-width="0.8" />
    </g>

    <!-- Main Outer Casing Flange Body -->
    <circle cx="30" cy="30" r="23" fill="url(#mpvCasingGrad)" stroke="#3f3f46" stroke-width="1.2" />
    <circle cx="30" cy="30" r="21.5" fill="none" stroke="#18181b" stroke-width="1" />

    <!-- 12 Flange Perimeter Hex Bolts -->
    <circle cx="49.2" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="46.6" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="39.6" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="30" cy="49.2" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="20.4" cy="46.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="13.4" cy="39.6" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="10.8" cy="30" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="13.4" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="20.4" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="30" cy="10.8" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="39.6" cy="13.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />
    <circle cx="46.6" cy="20.4" r="1.4" fill="url(#mpvBoltGrad)" stroke="#334155" stroke-width="0.4" />

    <!-- Inner Bezel Ring & Blue Dial Plate -->
    <circle cx="30" cy="30" r="16" fill="#09090b" stroke="#27272a" stroke-width="0.8" />
    <circle cx="30" cy="30" r="14.8" fill="url(#mpvDialGrad)" stroke="#38bdf8" stroke-width="0.6" />
    <circle cx="30" cy="30" r="13.6" fill="none" stroke="#60a5fa" stroke-width="0.4" stroke-opacity="0.5" />

    <!-- 4 Dial Cycle Position Pointers (0°, 90°, 180°, 270°) -->
    <polygon points="30,16.5 28,18.8 32,18.8" fill="#facc15" />
    <polygon points="43.5,30 41.2,28 41.2,32" fill="#facc15" />
    <polygon points="30,43.5 28,41.2 32,41.2" fill="#facc15" />
    <polygon points="16.5,30 18.8,28 18.8,32" fill="#facc15" />

    <!-- Miniature Brand Icon (Lower-Left 225°) -->
    <rect x="17" y="33" width="4.8" height="3.5" rx="0.5" fill="#ffffff" stroke="#16a34a" stroke-width="0.3" />
    <circle cx="19.4" cy="34.8" r="1" fill="#0284c7" />

    <!-- Central Rotor Boss -->
    <circle cx="30" cy="30" r="7" fill="#18181b" stroke="#09090b" stroke-width="1" />

    <!-- Rotary Selector Handle Lever -->
    <g transform="rotate({angle} 30 30)">
      <path d="M 28 30 L 27.5 22 L 25 12 C 25 8.5 35 8.5 35 12 L 32.5 22 L 32 30 Z" fill="url(#mpvHandleGrad)" stroke="#09090b" stroke-width="0.8" />
      <line x1="30" y1="11" x2="30" y2="24" stroke="#52525b" stroke-width="0.7" stroke-linecap="round" />
      <polygon points="30,8.5 28.8,11 31.2,11" fill="#facc15" />
      <circle cx="30" cy="30" r="3.6" fill="#18181b" stroke="#3f3f46" stroke-width="0.7" />
      <circle cx="30" cy="30" r="1.8" fill="url(#mpvBoltGrad)" stroke="#475569" stroke-width="0.3" />
    </g>
  </g>
  {flow_markup}
</svg>"""
            fpath = os.path.join(VALVES_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.write(svg_content.strip())
            print(f"   Created {fname}")

    # Dual-Manifolds (Left for ACF, Right for PSF)
    for side in ["left", "right"]:
        for is_anim in [False, True]:
            state_str = "animated" if is_anim else "static"
            fname = f"valve-to-vessel-dual-manifold-{side}-{state_str}.svg"

            # Center tee at (100, 100), branching to top (100, 50) and bottom (100, 150)
            if side == "left":
                # Trunk from right (valve nozzle at 170, 100) to tee (100, 100), branches go left to vessel (30, 50) and (30, 150)
                path_trunk = "M 170 100 L 100 100"
                path_top = "M 100 100 L 100 50 L 30 50"
                path_bot = "M 30 150 L 100 150 L 100 100"
                flanges = """
    <line x1="30" y1="40" x2="30" y2="60" stroke="#0369a1" stroke-width="4" />
    <line x1="30" y1="140" x2="30" y2="160" stroke="#0369a1" stroke-width="4" />
                """
                arrows = """
    <polygon points="46,44 32,50 46,56" fill="#0284c7" />
    <polygon points="54,144 68,150 54,156" fill="#0284c7" />
                """
                anim_markup = """
    <path d="M 170 100 L 100 100 L 100 50 L 30 50" stroke="#bae6fd" stroke-width="3" stroke-dasharray="6 8" fill="none">
      <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
    </path>
    <path d="M 30 150 L 100 150 L 100 100 L 170 100" stroke="#bae6fd" stroke-width="3" stroke-dasharray="6 8" fill="none">
      <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
    </path>
                """ if is_anim else ""
            else:
                # Trunk from left (valve nozzle at 30, 100) to tee (100, 100), branches go right to vessel (170, 50) and (170, 150)
                path_trunk = "M 30 100 L 100 100"
                path_top = "M 100 100 L 100 50 L 170 50"
                path_bot = "M 170 150 L 100 150 L 100 100"
                flanges = """
    <line x1="170" y1="40" x2="170" y2="60" stroke="#0369a1" stroke-width="4" />
    <line x1="170" y1="140" x2="170" y2="160" stroke="#0369a1" stroke-width="4" />
                """
                arrows = """
    <polygon points="154,44 168,50 154,56" fill="#0284c7" />
    <polygon points="146,144 132,150 146,156" fill="#0284c7" />
                """
                anim_markup = """
    <path d="M 30 100 L 100 100 L 100 50 L 170 50" stroke="#bae6fd" stroke-width="3" stroke-dasharray="6 8" fill="none">
      <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
    </path>
    <path d="M 170 150 L 100 150 L 100 100 L 30 100" stroke="#bae6fd" stroke-width="3" stroke-dasharray="6 8" fill="none">
      <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
    </path>
                """ if is_anim else ""

            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.25" />
    </filter>
  </defs>

  <!-- Dual Manifold Pipe Tree -->
  <g filter="url(#bottomShadow)">
    <path d="{path_trunk}" stroke="#0284c7" stroke-width="7" fill="none" stroke-linecap="round" />
    <path d="{path_top}" stroke="#0284c7" stroke-width="7" fill="none" stroke-linejoin="round" />
    <path d="{path_bot}" stroke="#0284c7" stroke-width="7" fill="none" stroke-linejoin="round" />
    {flanges}
    {arrows}
    <!-- Center Tee Junction Fitting -->
    <circle cx="100" cy="100" r="7" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
    {anim_markup}
  </g>
</svg>"""
            fpath = os.path.join(VALVES_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.write(svg_content.strip())
            print(f"   Created {fname}")

    # Clarifier Butterfly Valve
    for state in ["open-static", "open-animated", "closed-static"]:
        is_open = "open" in state
        is_anim = "animated" in state
        body_color = "#16a34a" if is_open else "#dc2626"
        fill_color = "#dcfce7" if is_open else "#fee2e2"
        disc_transform = "rotate(0 100 100)" if is_open else "rotate(90 100 100)"

        pulse = """
    <circle cx="100" cy="100" r="32" fill="none" stroke="#22c55e" stroke-width="2" opacity="0.6">
      <animate attributeName="r" values="24;36;24" dur="1.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.7;0.1;0.7" dur="1.2s" repeatCount="indefinite" />
    </circle>
        """ if is_anim else ""

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
  </defs>

  <g filter="url(#bottomShadow)">
    <!-- Valve Body Flange Ring -->
    <circle cx="100" cy="100" r="48" fill="#1e293b" stroke="#334155" stroke-width="4" />
    <circle cx="100" cy="100" r="38" fill="#0f172a" stroke="{body_color}" stroke-width="3" />
    {pulse}
    <!-- Internal Butterfly Disc -->
    <g transform="{disc_transform}">
      <ellipse cx="100" cy="100" rx="34" ry="7" fill="{fill_color}" stroke="{body_color}" stroke-width="2.5" />
      <line x1="100" y1="62" x2="100" y2="138" stroke="{body_color}" stroke-width="3.5" stroke-linecap="round" />
    </g>
    <!-- Top Actuator Stem -->
    <rect x="94" y="38" width="12" height="18" fill="#475569" stroke="#1e293b" stroke-width="1.5" />
    <circle cx="100" cy="36" r="8" fill="{body_color}" stroke="#0f172a" stroke-width="1.5" />
  </g>
</svg>"""
        fpath = os.path.join(VALVES_DIR, f"clarifier-butterfly-valve-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg_content.strip())
        print(f"   Created clarifier-butterfly-valve-{state}.svg")

# --------------------------------------------------------------------------------------------------
# 2. TANKS WITH UPDATED WATER COLORS & SPECULAR SHEEN
# --------------------------------------------------------------------------------------------------
def generate_updated_tanks():
    print("\nGenerating Updated Tanks...")
    tank_defs = """
    <!-- Collection Tank (Dark Sludge Brown Influent) -->
    <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#795548" stop-opacity="0.90" />
      <stop offset="45%" stop-color="#5d4037" stop-opacity="0.94" />
      <stop offset="100%" stop-color="#3e2723" stop-opacity="0.97" />
    </linearGradient>
    <linearGradient id="rawSewageWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#a1887f" stop-opacity="0.90" />
      <stop offset="40%" stop-color="#6d4c41" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#3e2723" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="rawSewageWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8d6e63" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#4e342e" stop-opacity="0.92" />
    </linearGradient>

    <!-- MBBR Aeration Tank (Murky Raw Sewage / Bio-Mix) -->
    <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#a1887f" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#8d6e63" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#5d4037" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="mbbrWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d7ccc8" stop-opacity="0.88" />
      <stop offset="40%" stop-color="#8d6e63" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#5d4037" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="mbbrWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#a1887f" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#4e342e" stop-opacity="0.90" />
    </linearGradient>

    <!-- Clarifier Tank (Amber Supernatant) -->
    <linearGradient id="clarifierWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d2c59d" stop-opacity="0.88" />
      <stop offset="35%" stop-color="#b8aa7b" stop-opacity="0.86" />
      <stop offset="68%" stop-color="#8d6e63" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#3e2723" stop-opacity="0.98" />
    </linearGradient>
    <linearGradient id="clarifierWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#efe8d0" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#d2c59d" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#a69865" stop-opacity="0.92" />
    </linearGradient>
    <linearGradient id="clarifierWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c4b788" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#8c7c4e" stop-opacity="0.88" />
    </linearGradient>

    <!-- Sludge Holding Tank (Dense Thickened WAS) -->
    <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5d4037" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#3e2723" stop-opacity="0.97" />
      <stop offset="100%" stop-color="#211109" stop-opacity="0.99" />
    </linearGradient>

    <!-- Filter Feed Tank (Pre-Filtered Secondary Effluent) -->
    <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#80cbc4" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#00695c" stop-opacity="0.92" />
    </linearGradient>

    <!-- Treated Clean Water Tank -->
    <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0f9ff" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.95" />
    </linearGradient>

    <!-- Soft Water Tank -->
    <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0f9ff" stop-opacity="0.98" />
      <stop offset="45%" stop-color="#06b6d4" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.98" />
    </linearGradient>

    <clipPath id="stdTankFluidClip">
      <path d="M 12 36 Q 100 48 188 36 L 188 142 Q 100 162 12 142 Z" />
    </clipPath>
    <clipPath id="clarifierFluidClip">
      <path d="M 12 36 Q 100 48 188 36 L 188 95 L 12 95 Z" />
    </clipPath>
    """

    # 1. Collection Tank
    for state in ["dry-static", "fluid-static", "fluid-animated"]:
        is_fluid = "fluid" in state
        is_anim = "animated" in state

        fluid_markup = ""
        if is_fluid:
            anim_w1 = """
          <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
            """ if is_anim else ""
            anim_w2 = """
          <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
            """ if is_anim else ""

            fluid_markup = f"""
    <!-- Fluid Volume (Dark Sludge Brown Influent) -->
    <g clipPath="url(#stdTankFluidClip)">
      <path d="M 12 80 Q 100 98 188 80 L 188 142 Q 100 162 12 142 Z" fill="url(#rawSewageGrad)" />
      <!-- Wave 1: Back Wave -->
      <path d="M -60 80 q 20 -7, 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 L 260 160 L -60 160 Z" fill="url(#rawSewageWaveBack)">
        {anim_w1}
      </path>
      <!-- Wave 2: Front Wave -->
      <path d="M -88 80 q 28 -8, 56 0 t 56 0 t 56 0 t 56 0 t 56 0 t 56 0 L 320 160 L -88 160 Z" fill="url(#rawSewageWaveFront)">
        {anim_w2}
      </path>
      <!-- Surface Meniscus -->
      <ellipse cx="100" cy="80" rx="88" ry="8" fill="#5d4037" opacity="0.35" />
    </g>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 180" width="200" height="180">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    {tank_defs}
  </defs>

  <!-- 3D Ground Shadow -->
  <ellipse cx="100" cy="162" rx="92" ry="12" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- 2.5D Glass Cylinder Tank Hull -->
  <path d="M 10 142 Q 100 164 190 142 L 190 32 Q 100 52 10 32 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2.5" />
  {fluid_markup}
  <!-- Cylindrical Specular Glare -->
  <rect x="18" y="34" width="20" height="110" rx="4" fill="url(#specularSheen)" opacity="0.8" />
  <!-- Top Flange Rim -->
  <ellipse cx="100" cy="32" rx="90" ry="10" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="2" />
</svg>"""
        fpath = os.path.join(TANKS_DIR, f"collection-tank-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg.strip())
        print(f"   Created collection-tank-{state}.svg")

    # 2. MBBR Aeration Tank
    for state in ["dry-static", "fluid-static", "fluid-animated"]:
        is_fluid = "fluid" in state
        is_anim = "animated" in state

        fluid_markup = ""
        if is_fluid:
            anim_w1 = '<animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />' if is_anim else ""
            anim_w2 = '<animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />' if is_anim else ""
            
            bubbles = ""
            if is_anim:
                bubbles = """
      <!-- Rising Aeration Micro-Bubbles -->
      <g fill="#ffffff" stroke="#7dd3fc" stroke-width="0.5" opacity="0.85">
        <circle cx="40" cy="140" r="2.2"><animate attributeName="cy" values="140;110;85" dur="2.8s" repeatCount="indefinite" /></circle>
        <circle cx="70" cy="140" r="2.8"><animate attributeName="cy" values="140;105;85" dur="2.4s" begin="0.4s" repeatCount="indefinite" /></circle>
        <circle cx="100" cy="140" r="2.0"><animate attributeName="cy" values="140;115;85" dur="3.0s" begin="0.8s" repeatCount="indefinite" /></circle>
        <circle cx="130" cy="140" r="2.5"><animate attributeName="cy" values="140;108;85" dur="2.6s" begin="0.2s" repeatCount="indefinite" /></circle>
        <circle cx="160" cy="140" r="2.2"><animate attributeName="cy" values="140;112;85" dur="2.9s" begin="1.1s" repeatCount="indefinite" /></circle>
      </g>
                """

            fluid_markup = f"""
    <!-- Fluid Volume (Bio-Mix) -->
    <g clipPath="url(#stdTankFluidClip)">
      <path d="M 12 85 Q 100 102 188 85 L 188 142 Q 100 162 12 142 Z" fill="url(#mbbrWaterGrad)" />
      <!-- Wave 1: Back Wave -->
      <path d="M -60 85 q 20 -7, 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 L 260 160 L -60 160 Z" fill="url(#mbbrWaveBack)">
        {anim_w1}
      </path>
      <!-- Wave 2: Front Wave -->
      <path d="M -88 85 q 28 -8, 56 0 t 56 0 t 56 0 t 56 0 t 56 0 t 56 0 L 320 160 L -88 160 Z" fill="url(#mbbrWaveFront)">
        {anim_w2}
      </path>
      <!-- Surface Meniscus -->
      <ellipse cx="100" cy="85" rx="88" ry="8" fill="#a1887f" opacity="0.35" />
      {bubbles}
      <!-- Suspended K1 Bio-Carriers -->
      <g fill="#f8fafc" stroke="#cbd5e1" stroke-width="0.8" opacity="0.75">
        <circle cx="45" cy="115" r="4.5" />
        <circle cx="65" cy="100" r="4.0" />
        <circle cx="85" cy="122" r="5.0" />
        <circle cx="115" cy="105" r="4.2" />
        <circle cx="135" cy="120" r="4.8" />
        <circle cx="155" cy="110" r="4.2" />
      </g>
    </g>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 180" width="200" height="180">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    {tank_defs}
  </defs>

  <!-- 3D Ground Shadow -->
  <ellipse cx="100" cy="162" rx="92" ry="12" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- 2.5D Glass Cylinder Tank Hull -->
  <path d="M 10 142 Q 100 164 190 142 L 190 32 Q 100 52 10 32 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2.5" />
  {fluid_markup}
  <!-- Cylindrical Specular Glare -->
  <rect x="18" y="34" width="20" height="110" rx="4" fill="url(#specularSheen)" opacity="0.8" />
  <!-- Top Flange Rim -->
  <ellipse cx="100" cy="32" rx="90" ry="10" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="2" />
</svg>"""
        fpath = os.path.join(TANKS_DIR, f"mbbr-aeration-tank-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg.strip())
        print(f"   Created mbbr-aeration-tank-{state}.svg")

    # 3. Clarifier Tank (Conical Hopper + Supernatant + Sludge Blanket + Scraper Arm)
    for state in ["dry-static", "fluid-static", "fluid-animated", "arm-rotating-animated"]:
        is_fluid = state != "dry-static"
        is_anim = "animated" in state
        is_arm_rotate = state == "arm-rotating-animated" or state == "fluid-animated"

        fluid_markup = ""
        if is_fluid:
            anim_w1 = '<animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />' if is_anim else ""
            anim_w2 = '<animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />' if is_anim else ""

            arm_anim = '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3.5s" repeatCount="indefinite" />' if is_arm_rotate else ""

            fluid_markup = f"""
    <!-- Supernatant Clarified Water Zone (Upper Section Amber) -->
    <g clipPath="url(#clarifierFluidClip)">
      <path d="M 12 70 L 12 95 L 188 95 L 188 70 Z" fill="url(#clarifierWaterGrad)" />
      <!-- Wave 1: Back Wave -->
      <path d="M -60 70 q 20 -6, 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0 L 260 110 L -60 110 Z" fill="url(#clarifierWaveBack)">
        {anim_w1}
      </path>
      <!-- Wave 2: Front Wave -->
      <path d="M -88 70 q 28 -7, 56 0 t 56 0 t 56 0 t 56 0 t 56 0 t 56 0 L 320 110 L -88 110 Z" fill="url(#clarifierWaveFront)">
        {anim_w2}
      </path>
      <!-- Surface Meniscus -->
      <ellipse cx="100" cy="70" rx="88" ry="8" fill="#d2c59d" opacity="0.35" />
    </g>

    <!-- Settled Biological Sludge Blanket in Conical Hopper Apex -->
    <path d="M 12 95 L 75 146 Q 100 154 125 146 L 188 95 Z" fill="url(#sludgeWaterGrad)" />

    <!-- Submerged Clarifier Bridge & Rotating Scraper Rake Arm -->
    <g transform="translate(100, 92)">
      <circle cx="0" cy="0" r="22" fill="#1e293b" stroke="#16a34a" stroke-width="2" />
      <circle cx="0" cy="0" r="16" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5" />
      <g>
        {arm_anim}
        <line x1="-16" y1="0" x2="16" y2="0" stroke="#15803d" stroke-width="3" stroke-linecap="round" />
        <line x1="0" y1="-16" x2="0" y2="16" stroke="#15803d" stroke-width="3" stroke-linecap="round" />
        <line x1="-11" y1="-4" x2="-11" y2="4" stroke="#15803d" stroke-width="1.8" />
        <line x1="11" y1="-4" x2="11" y2="4" stroke="#15803d" stroke-width="1.8" />
      </g>
      <circle cx="0" cy="0" r="4.5" fill="#15803d" />
    </g>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 180" width="200" height="180">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    {tank_defs}
  </defs>

  <!-- 3D Ground Shadow -->
  <ellipse cx="100" cy="162" rx="72" ry="10" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- 2.5D Conical Hopper Tank Hull (Upper Cylinder + 60° Funnel Apex) -->
  <path d="M 10 32 L 10 95 L 75 146 Q 100 154 125 146 L 190 95 L 190 32 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2.5" />
  {fluid_markup}
  <!-- Cylindrical Specular Glare -->
  <rect x="18" y="34" width="20" height="60" rx="4" fill="url(#specularSheen)" opacity="0.8" />
  <!-- Top Flange Rim -->
  <ellipse cx="100" cy="32" rx="90" ry="10" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="2" />
</svg>"""
        fpath = os.path.join(TANKS_DIR, f"clarifier-tank-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg.strip())
        print(f"   Created clarifier-tank-{state}.svg")

# --------------------------------------------------------------------------------------------------
# 3. PUMPS & BLOWERS (2.5D SIGHT-GLASS WITH VORTEX IMPELLER)
# --------------------------------------------------------------------------------------------------
def generate_pumps_and_blowers():
    print("\nGenerating Pumps & Blowers...")
    directions = [
        ("flow-left-to-right", 0),
        ("flow-right-to-left", 180),
        ("flow-vertical-up", 270),
        ("flow-vertical-down", 90)
    ]
    states = [
        ("running-animated", "#16a34a", "#dcfce7", True),
        ("running-static", "#16a34a", "#dcfce7", False),
        ("stopped-static", "#dc2626", "#fee2e2", False),
        ("standby-static", "#d97706", "#fef3c7", False),
        ("fault-animated", "#ef4444", "#450a0a", True)
    ]

    for dir_name, rot_deg in directions:
        for state_name, stroke_col, fill_col, is_anim in states:
            fname = f"centrifugal-pump-{dir_name}-{state_name}.svg"

            anim_markup = ""
            if is_anim:
                anim_markup = """
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.5s" repeatCount="indefinite" />
                """ if state_name != "fault-animated" else """
      <animate attributeName="opacity" values="0.4;1;0.4" dur="0.8s" repeatCount="indefinite" />
                """

            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    <radialGradient id="pumpVoluteGrad" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="70%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </radialGradient>
  </defs>

  <!-- 3D Ground Shadow & Footing Bracket -->
  <rect x="70" y="150" width="60" height="12" rx="3" fill="#0f172a" opacity="0.3" filter="url(#bottomShadow)" />
  <rect x="76" y="142" width="48" height="10" rx="2" fill="#334155" stroke="#1e293b" stroke-width="1.5" />

  <!-- Pump Volute Casing (Rotated for Flow Direction) -->
  <g transform="translate(100, 100) rotate({rot_deg}) translate(-100, -100)">
    <!-- Suction / Discharge Flange Stubs -->
    <rect x="25" y="88" width="25" height="24" rx="2" fill="#334155" stroke="#1e293b" stroke-width="2" />
    <rect x="150" y="88" width="25" height="24" rx="2" fill="#334155" stroke="#1e293b" stroke-width="2" />

    <!-- 2.5D Casing Ring -->
    <circle cx="100" cy="100" r="50" fill="url(#pumpVoluteGrad)" stroke="#475569" stroke-width="3" />
    <circle cx="100" cy="100" r="42" fill="#09090b" stroke="{stroke_col}" stroke-width="2.5" />

    <!-- Sight-Glass Well -->
    <circle cx="100" cy="100" r="32" fill="{fill_col}" stroke="{stroke_col}" stroke-width="2" />

    <!-- Vortex Impeller -->
    <g transform="translate(100, 100)">
      <g>
        {anim_markup}
        <path d="M 0 0 Q 15 -10 24 -4 Q 10 10 0 0 Z" fill="{stroke_col}" opacity="0.9" />
        <path d="M 0 0 Q -10 15 -4 24 Q 10 10 0 0 Z" fill="{stroke_col}" opacity="0.9" />
        <path d="M 0 0 Q -15 10 -24 4 Q -10 -10 0 0 Z" fill="{stroke_col}" opacity="0.9" />
        <path d="M 0 0 Q 10 -15 4 -24 Q -10 -10 0 0 Z" fill="{stroke_col}" opacity="0.9" />
        <circle cx="0" cy="0" r="6" fill="#1e293b" stroke="{stroke_col}" stroke-width="1.5" />
      </g>
    </g>

    <!-- Specular Reflection Sheen -->
    <path d="M 72 75 A 36 36 0 0 1 128 75" stroke="#ffffff" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.5" />
  </g>
</svg>"""
            fpath = os.path.join(PUMPS_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.write(svg_content.strip())

    print("   Created centrifugal pump suite (20 variations).")

    # Chemical Dosing Pump (Hexagonal Diaphragm)
    for state in ["active-animated", "active-static", "stopped-static"]:
        is_anim = "animated" in state
        is_stopped = "stopped" in state
        stroke_col = "#dc2626" if is_stopped else "#16a34a"
        fill_col = "#fee2e2" if is_stopped else "#dcfce7"

        anim_markup = """
      <circle cx="100" cy="100" r="18" fill="#16a34a" opacity="0.25">
        <animate attributeName="r" values="12;24;12" dur="0.9s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.4;0.05;0.4" dur="0.9s" repeatCount="indefinite" />
      </circle>
        """ if is_anim else ""

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
  </defs>

  <!-- 3D Ground Shadow -->
  <ellipse cx="100" cy="162" rx="48" ry="10" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- Dosing Pump Hexagonal Head -->
  <g transform="translate(100, 100)">
    <!-- Base mounting block -->
    <rect x="-35" y="42" width="70" height="14" rx="2" fill="#334155" stroke="#1e293b" stroke-width="1.5" />
    <!-- Diaphragm Hexagon Chamber -->
    <polygon points="0,-48 42,-24 42,24 0,48 -42,24 -42,-24" fill="{fill_col}" stroke="{stroke_col}" stroke-width="3.5" />
    <!-- Pulse Diaphragm Core -->
    {anim_markup}
    <circle cx="0" cy="0" r="14" fill="{stroke_col}" />
    <!-- Top & Bottom Dosing Check Valves -->
    <rect x="-8" y="-62" width="16" height="14" rx="2" fill="#475569" stroke="#1e293b" stroke-width="1.5" />
    <rect x="-8" y="48" width="16" height="14" rx="2" fill="#475569" stroke="#1e293b" stroke-width="1.5" />
  </g>
</svg>"""
        fpath = os.path.join(PUMPS_DIR, f"chemical-dosing-pump-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg_content.strip())
        print(f"   Created chemical-dosing-pump-{state}.svg")

# --------------------------------------------------------------------------------------------------
# 4. FILTERS & INSTRUMENTS (ASME STEEL SHELLS & UTILITIES)
# --------------------------------------------------------------------------------------------------
def generate_filters_and_instruments():
    print("\nGenerating Filters & Instruments...")
    filter_defs = """
    <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="25%" stop-color="#0284c7" />
      <stop offset="55%" stop-color="#0369a1" />
      <stop offset="85%" stop-color="#075985" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="sandMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d97706" />
      <stop offset="50%" stop-color="#b45309" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>
    <linearGradient id="carbonMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="50%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="resinMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" />
      <stop offset="50%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#b45309" />
    </linearGradient>
    """

    filter_types = [
        ("pressure-sand-filter-psf", "sandMediaGrad", "#bae6fd"),
        ("activated-carbon-filter-acf", "carbonMediaGrad", "#bae6fd"),
        ("water-softener-resin", "resinMediaGrad", "#e0f2fe")
    ]

    for f_id, media_grad, water_col in filter_types:
        for state in ["dry-static", "fluid-static", "fluid-animated"]:
            is_fluid = state != "dry-static"
            is_anim = "animated" in state

            media_markup = ""
            if is_fluid:
                anim_flow = """
        <line x1="30" y1="50" x2="30" y2="130" stroke="#bae6fd" stroke-width="2.5" stroke-dasharray="5 7" opacity="0.9">
          <animate attributeName="stroke-dashoffset" from="0" to="24" dur="0.9s" repeatCount="indefinite" />
        </line>
        <line x1="60" y1="50" x2="60" y2="130" stroke="#bae6fd" stroke-width="2.5" stroke-dasharray="5 7" opacity="0.9">
          <animate attributeName="stroke-dashoffset" from="0" to="24" dur="0.8s" repeatCount="indefinite" />
        </line>
        <line x1="90" y1="50" x2="90" y2="130" stroke="#bae6fd" stroke-width="2.5" stroke-dasharray="5 7" opacity="0.9">
          <animate attributeName="stroke-dashoffset" from="0" to="24" dur="0.85s" repeatCount="indefinite" />
        </line>
                """ if is_anim else ""

                media_markup = f"""
      <!-- Internal Active Filtration Bed -->
      <rect x="2" y="45" width="116" height="85" fill="url(#{media_grad})" />
      {anim_flow}
      <!-- Bottom Lateral Collector Arm -->
      <line x1="15" y1="135" x2="105" y2="135" stroke="#cbd5e1" stroke-width="3.5" stroke-linecap="round" />
      <line x1="30" y1="130" x2="30" y2="140" stroke="#94a3b8" stroke-width="1.8" />
      <line x1="60" y1="130" x2="60" y2="140" stroke="#94a3b8" stroke-width="1.8" />
      <line x1="90" y1="130" x2="90" y2="140" stroke="#94a3b8" stroke-width="1.8" />
                """

            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 200" width="160" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
    {filter_defs}
  </defs>

  <!-- 3D Ground Support Shadow -->
  <ellipse cx="80" cy="188" rx="64" ry="8" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- Structural Steel Stand Legs -->
  <rect x="22" y="148" width="8" height="36" rx="1.5" fill="#075985" stroke="#0284c7" stroke-width="1.5" />
  <rect x="90" y="148" width="8" height="36" rx="1.5" fill="#075985" stroke="#0284c7" stroke-width="1.5" />
  <line x1="30" y1="168" x2="90" y2="168" stroke="#0284c7" stroke-width="2.5" />

  <!-- ASME Pressure Filter Vessel Shell -->
  <g transform="translate(20, 10)">
    <!-- Dished Top Head -->
    <path d="M 1 35 C 1 10, 119 10, 119 35 Z" fill="url(#filterVesselGrad)" stroke="#0284c7" stroke-width="3" />
    <!-- Straight Shell Body -->
    <rect x="1" y="35" width="118" height="105" fill="url(#filterVesselGrad)" stroke="#0284c7" stroke-width="3" />
    <!-- Dished Bottom Head -->
    <path d="M 1 140 C 1 165, 119 165, 119 140 Z" fill="url(#filterVesselGrad)" stroke="#0284c7" stroke-width="3" />
    {media_markup}
    <!-- Top Flanged Inspection Manway Hatch -->
    <rect x="44" y="6" width="32" height="10" rx="2" fill="#cbd5e1" stroke="#0284c7" stroke-width="2" />
    <!-- Specular Curvature Highlight -->
    <rect x="8" y="16" width="12" height="135" rx="3" fill="#ffffff" opacity="0.3" />
  </g>
</svg>"""
            fpath = os.path.join(FILTERS_DIR, f"{f_id}-{state}.svg")
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.write(svg_content.strip())
            print(f"   Created {f_id}-{state}.svg")

    # UV Disinfection Reactor
    for state in ["active-animated", "active-static", "inactive-static"]:
        is_active = "active" in state
        is_anim = "animated" in state
        uv_glow = """
      <rect x="40" y="75" width="120" height="50" rx="4" fill="#06b6d4" opacity="0.45">
        <animate attributeName="opacity" values="0.3;0.7;0.3" dur="1.4s" repeatCount="indefinite" />
      </rect>
      <line x1="30" y1="100" x2="170" y2="100" stroke="#bae6fd" stroke-width="4" stroke-dasharray="6 8">
        <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.7s" repeatCount="indefinite" />
      </line>
        """ if is_anim else ('''
      <rect x="40" y="75" width="120" height="50" rx="4" fill="#06b6d4" opacity="0.35" />
        ''' if is_active else "")

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>
  </defs>

  <!-- Grounding Shadow -->
  <rect x="30" y="152" width="140" height="12" rx="4" fill="#0f172a" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- UV Chamber Body -->
  <g filter="url(#bottomShadow)">
    <rect x="30" y="65" width="140" height="70" rx="10" fill="#1e293b" stroke="#334155" stroke-width="3" />
    <rect x="40" y="75" width="120" height="50" rx="5" fill="#0f172a" stroke="#0284c7" stroke-width="2" />
    {uv_glow}
    <!-- Quartz Sleeve & UV Lamp Tube -->
    <rect x="45" y="94" width="110" height="12" rx="3" fill="#ffffff" stroke="#38bdf8" stroke-width="1.5" opacity="0.9" />
    <!-- Flanged Inlet/Outlet End Caps -->
    <rect x="18" y="85" width="14" height="30" rx="2" fill="#475569" stroke="#1e293b" stroke-width="2" />
    <rect x="168" y="85" width="14" height="30" rx="2" fill="#475569" stroke="#1e293b" stroke-width="2" />
  </g>
</svg>"""
        fpath = os.path.join(UTILITY_DIR, f"uv-disinfection-system-{state}.svg")
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(svg_content.strip())
        print(f"   Created uv-disinfection-system-{state}.svg")

# --------------------------------------------------------------------------------------------------
# 5. PACKAGING INTO ZIP
# --------------------------------------------------------------------------------------------------
def package_zip():
    zip_path = "public/schematic-assets.zip"
    print(f"\nCompressing updated assets into {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, "public")
                zf.write(full_path, rel_path)
    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Zip created successfully ({zip_size_mb:.2f} MB).")

if __name__ == "__main__":
    generate_4port_multiport_valves()
    generate_updated_tanks()
    generate_pumps_and_blowers()
    generate_filters_and_instruments()
    package_zip()
    print("\nALL SCHEMATIC SVG ASSETS GENERATION COMPLETED!")
