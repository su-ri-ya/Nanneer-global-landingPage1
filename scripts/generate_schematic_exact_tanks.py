import os
import re

BASE_DIR = 'public/schematic-assets'
TANKS_DIR = os.path.join(BASE_DIR, 'tanks')

# Common Defs matching ScadaSchematicSimulation.tsx
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
    <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#a1887f" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#8d6e63" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#5d4037" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#9e8d72" stop-opacity="0.85" />
      <stop offset="45%" stop-color="#6b7852" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#4a5636" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#7dd3fc" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.92" />
    </linearGradient>
    <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0f9ff" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0f9ff" stop-opacity="0.98" />
      <stop offset="45%" stop-color="#38bdf8" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.98" />
    </linearGradient>
    <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5d4037" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#3e2723" stop-opacity="0.97" />
      <stop offset="100%" stop-color="#211109" stop-opacity="0.99" />
    </linearGradient>
  </defs>"""

# ==============================================================================
# 1. COLLECTION TANK (2.5D Dished Cylinder + Meniscus + Intake Screen + Diffuser)
# ==============================================================================
def get_collection_tank(state):
    anim_tag = """    <circle cx="45" cy="72" r="2.0" fill="#d7ccc8" opacity="0.7">
      <animate attributeName="cy" values="72;34" dur="1.4s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.8;0" dur="1.4s" begin="0.1s" repeatCount="indefinite" />
    </circle>
    <circle cx="80" cy="74" r="2.8" fill="#d7ccc8" opacity="0.75">
      <animate attributeName="cy" values="74;34" dur="1.1s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.85;0" dur="1.1s" begin="0.3s" repeatCount="indefinite" />
    </circle>
    <circle cx="115" cy="72" r="2.2" fill="#d7ccc8" opacity="0.7">
      <animate attributeName="cy" values="72;34" dur="1.3s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.8;0" dur="1.3s" begin="0s" repeatCount="indefinite" />
    </circle>
    <circle cx="145" cy="74" r="2.4" fill="#d7ccc8" opacity="0.75">
      <animate attributeName="cy" values="74;34" dur="1.2s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.85;0" dur="1.2s" begin="0.2s" repeatCount="indefinite" />
    </circle>"""

    fluid_block = """  <!-- Raw Sewage Fluid Volume with 3D Dish Bottom & Curved Meniscus -->
  <path d="M 2 32 Q 87.5 44 173 32 L 173 76 Q 87.5 93 2 76 Z" fill="url(#rawSewageGrad)" />
  <ellipse cx="87.5" cy="32" rx="85.5" ry="6.5" fill="#8d6e63" stroke="#d7ccc8" stroke-width="0.8" opacity="0.95" />
  <ellipse cx="87.5" cy="32" rx="80" ry="4.5" fill="#a1887f" opacity="0.4" />"""

    bubbles_block = f"""  <!-- Submerged Bottom Air Diffuser Pipe & Bubbles -->
  <line x1="30" y1="74" x2="160" y2="74" stroke="#d97706" stroke-width="2" stroke-linecap="round" />
  <g>
{anim_tag if state == 'fluid-animated' else ''}
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" width="200" height="120">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="100" cy="100" rx="88" ry="8" fill="#0b2545" opacity="0.22" filter="url(#bottomShadow)" />

  <g transform="translate(12, 10)">
    <!-- 2.5D Cylindrical Hull with Curved Dished Bottom -->
    <path d="M 0 76 Q 87.5 94 175 76 L 175 14 Q 87.5 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#64748b" stroke-width="1.5" />

{fluid_block if 'fluid' in state else ''}

    <!-- Submerged Coarse Bar Screen Cutaway (Raw Inlet Baffle) -->
    <g transform="translate(8, 25)">
      <rect x="0" y="0" width="22" height="48" rx="2" fill="#334155" opacity="0.3" stroke="#64748b" stroke-width="1" />
      <line x1="4" y1="2" x2="4" y2="46" stroke="#94a3b8" stroke-width="0.8" />
      <line x1="8" y1="2" x2="8" y2="46" stroke="#94a3b8" stroke-width="0.8" />
      <line x1="12" y1="2" x2="12" y2="46" stroke="#94a3b8" stroke-width="0.8" />
      <line x1="16" y1="2" x2="16" y2="46" stroke="#94a3b8" stroke-width="0.8" />
      <line x1="20" y1="2" x2="20" y2="46" stroke="#94a3b8" stroke-width="0.8" />
    </g>

{bubbles_block if 'fluid' in state else ''}

    <!-- Cylindrical Specular Light Glare (Left Streak & Right Rim Light) -->
    <rect x="6" y="16" width="16" height="58" rx="3" fill="url(#specularSheen)" pointer-events="none" />
    <line x1="168" y1="16" x2="168" y2="76" stroke="#ffffff" stroke-width="1.2" opacity="0.4" />

    <!-- 3D Top Glass Vessel Flange & Rim Opening -->
    <ellipse cx="87.5" cy="14" rx="87.5" ry="8" fill="url(#glassRimGrad)" stroke="#94a3b8" stroke-width="1.5" />
    <ellipse cx="87.5" cy="14" rx="82" ry="5.5" fill="none" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3 3" />
  </g>
</svg>"""

# ==============================================================================
# 2. AERATION MBBR TANK (2.5D Dished Cylinder + Tumbling K1 Media + EPDM Grid)
# ==============================================================================
def get_aeration_tank(state):
    anim_bubbles = """    <circle cx="22" cy="74" r="2.2" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="74;26" dur="1.1s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.1s" begin="0s" repeatCount="indefinite" />
    </circle>
    <circle cx="46" cy="75" r="3.0" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="75;26" dur="0.9s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="0.9s" begin="0.2s" repeatCount="indefinite" />
    </circle>
    <circle cx="70" cy="74" r="2.0" fill="#e0f2fe" opacity="0.8">
      <animate attributeName="cy" values="74;26" dur="1.3s" begin="0.4s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.3s" begin="0.4s" repeatCount="indefinite" />
    </circle>
    <circle cx="94" cy="75" r="2.8" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="75;26" dur="1.0s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.0s" begin="0.1s" repeatCount="indefinite" />
    </circle>
    <circle cx="112" cy="74" r="2.4" fill="#e0f2fe" opacity="0.8">
      <animate attributeName="cy" values="74;26" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
    </circle>"""

    k1_carriers = """    <!-- Tumbling Kaldnes K1 Biofilm Media Carriers -->
    <g>
      <g>
        <animateTransform attributeName="transform" type="translate" values="0,0; 2,-4; -2,-7; 0,0" dur="3.2s" repeatCount="indefinite" />
        <circle cx="22" cy="44" r="3.4" fill="#f8fafc" stroke="#0284c7" stroke-width="0.8" opacity="0.88" />
        <line x1="19.6" y1="44" x2="24.4" y2="44" stroke="#0284c7" stroke-width="0.6" />
        <line x1="22" y1="41.6" x2="22" y2="46.4" stroke="#0284c7" stroke-width="0.6" />
      </g>
      <g>
        <animateTransform attributeName="transform" type="translate" values="0,0; -3,-5; 2,-8; 0,0" dur="2.8s" repeatCount="indefinite" />
        <circle cx="50" cy="66" r="4.0" fill="#fbbf24" stroke="#d97706" stroke-width="0.8" opacity="0.9" />
        <line x1="47" y1="66" x2="53" y2="66" stroke="#d97706" stroke-width="0.6" />
        <line x1="50" y1="63" x2="50" y2="69" stroke="#d97706" stroke-width="0.6" />
      </g>
      <g>
        <animateTransform attributeName="transform" type="translate" values="0,0; 2,-3; -1,-6; 0,0" dur="3.5s" repeatCount="indefinite" />
        <circle cx="80" cy="50" r="3.2" fill="#f8fafc" stroke="#0284c7" stroke-width="0.8" opacity="0.88" />
        <line x1="77.8" y1="50" x2="82.2" y2="50" stroke="#0284c7" stroke-width="0.6" />
        <line x1="80" y1="47.8" x2="80" y2="52.2" stroke="#0284c7" stroke-width="0.6" />
      </g>
      <g>
        <animateTransform attributeName="transform" type="translate" values="0,0; -2,-4; 3,-7; 0,0" dur="2.5s" repeatCount="indefinite" />
        <circle cx="104" cy="68" r="3.6" fill="#fbbf24" stroke="#d97706" stroke-width="0.8" opacity="0.9" />
        <line x1="101.4" y1="68" x2="106.6" y2="68" stroke="#d97706" stroke-width="0.6" />
        <line x1="104" y1="65.4" x2="104" y2="70.6" stroke="#d97706" stroke-width="0.6" />
      </g>
    </g>""" if state == 'fluid-animated' else """    <g>
      <circle cx="22" cy="44" r="3.4" fill="#f8fafc" stroke="#0284c7" stroke-width="0.8" opacity="0.88" />
      <circle cx="50" cy="66" r="4.0" fill="#fbbf24" stroke="#d97706" stroke-width="0.8" opacity="0.9" />
      <circle cx="80" cy="50" r="3.2" fill="#f8fafc" stroke="#0284c7" stroke-width="0.8" opacity="0.88" />
      <circle cx="104" cy="68" r="3.6" fill="#fbbf24" stroke="#d97706" stroke-width="0.8" opacity="0.9" />
    </g>"""

    fluid_block = f"""  <!-- Aerated Mixed Liquor Fluid Volume -->
  <path d="M 2 24 Q 70 38 138 24 L 138 76 Q 70 93 2 76 Z" fill="url(#mbbrWaterGrad)" />
  <ellipse cx="70" cy="24" rx="68" ry="6.5" fill="#6b7852" stroke="#a3e635" stroke-width="0.8" opacity="0.92" />
  <ellipse cx="70" cy="24" rx="62" ry="4.5" fill="#9e8d72" opacity="0.4" />
{k1_carriers}"""

    bubbles_block = f"""  <!-- Bottom Fine-Bubble EPDM Aeration Diffuser Grid -->
  <line x1="18" y1="74" x2="122" y2="74" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" />
  <g>
{anim_bubbles if state == 'fluid-animated' else ''}
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 120" width="170" height="120">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="100" rx="72" ry="8" fill="#0b2545" opacity="0.22" filter="url(#bottomShadow)" />

  <g transform="translate(15, 10)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

    <!-- Internal Retention Sieve Screen on Effluent Weir (Right Edge) -->
    <g transform="translate(126, 26)">
      <rect x="0" y="0" width="10" height="48" rx="1.5" fill="#1e293b" opacity="0.35" stroke="#0284c7" stroke-width="1" />
      <line x1="1" y1="8" x2="9" y2="8" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="1 1" />
      <line x1="1" y1="16" x2="9" y2="16" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="1 1" />
      <line x1="1" y1="24" x2="9" y2="24" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="1 1" />
      <line x1="1" y1="32" x2="9" y2="32" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="1 1" />
      <line x1="1" y1="40" x2="9" y2="40" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="1 1" />
    </g>

{bubbles_block if 'fluid' in state else ''}

    <!-- Cylindrical Specular Glare -->
    <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" pointer-events="none" />
    <line x1="134" y1="16" x2="134" y2="76" stroke="#ffffff" stroke-width="1.2" opacity="0.4" />

    <!-- 3D Top Glass Vessel Flange & Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="1.5" />
    <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93c5fd" stroke-width="1" stroke-dasharray="2 2" />
  </g>
</svg>"""

# ==============================================================================
# 3. SECONDARY CLARIFIER (60° Conical Hopper + Center Bridge Scraper Rake)
# ==============================================================================
def get_clarifier_tank(state):
    rake_anim = """    <g>
      <animateTransform attributeName="transform" type="rotate" values="-4 70 20; 4 70 20; -4 70 20" dur="4.5s" repeatCount="indefinite" />
      <line x1="70" y1="20" x2="70" y2="82" stroke="#475569" stroke-width="2.5" />
      <path d="M 30 68 L 70 84 L 110 68" stroke="#64748b" stroke-width="2.5" fill="none" />
      <line x1="42" y1="73" x2="42" y2="81" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="56" y1="78" x2="56" y2="85" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="84" y1="78" x2="84" y2="85" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="98" y1="73" x2="98" y2="81" stroke="#94a3b8" stroke-width="1.5" />
    </g>""" if state == 'fluid-animated' else """    <g>
      <line x1="70" y1="20" x2="70" y2="82" stroke="#475569" stroke-width="2.5" />
      <path d="M 30 68 L 70 84 L 110 68" stroke="#64748b" stroke-width="2.5" fill="none" />
      <line x1="42" y1="73" x2="42" y2="81" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="56" y1="78" x2="56" y2="85" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="84" y1="78" x2="84" y2="85" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="98" y1="73" x2="98" y2="81" stroke="#94a3b8" stroke-width="1.5" />
    </g>"""

    fluid_block = """  <!-- Supernatant Clarified Water Zone -->
  <path d="M 2 22 L 2 54 L 138 54 L 138 22 Z" fill="#bae6fd" opacity="0.85" />
  <!-- Settled Biological Sludge Blanket (Bottom Hopper) -->
  <path d="M 2 54 L 54 88 Q 70 93 86 88 L 138 54 Z" fill="#5d4037" opacity="0.95" />
  <!-- Peripheral V-Notch Overflow Weir -->
  <path d="M 4 20 L 136 20" stroke="#38bdf8" stroke-width="1.5" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 125" width="170" height="125">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow under Conical Tip -->
  <ellipse cx="85" cy="108" rx="55" ry="7" fill="#0b2545" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 10)">
    <!-- 2.5D Conical Hopper Tank Hull (Cylindrical Upper + 60° Conical Funnel Bottom) -->
    <path d="M 0 14 L 0 54 L 54 88 Q 70 93 86 88 L 140 54 L 140 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

    <!-- Rotating Center Bridge Scraper Rake Mechanism -->
    <rect x="15" y="8" width="110" height="6" rx="1.5" fill="#334155" stroke="#64748b" stroke-width="1" />
{rake_anim}

    <!-- Top Flange Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 4. SLUDGE HOLDING TANK (Conical Hopper + Thickened Sludge)
# ==============================================================================
def get_sludge_tank(state):
    fluid_block = """  <!-- Thickened Sludge Fluid Body -->
  <path d="M 2 34 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 34 Z" fill="url(#sludgeWaterGrad)" />
  <ellipse cx="57.5" cy="34" rx="55.5" ry="5.5" fill="#5d4037" stroke="#8d6e63" stroke-width="0.8" opacity="0.95" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 110" width="150" height="110">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="75" cy="94" rx="48" ry="6" fill="#0b2545" opacity="0.24" filter="url(#bottomShadow)" />

  <g transform="translate(17, 10)">
    <!-- Conical Hopper Vessel Hull -->
    <path d="M 0 12 L 0 46 L 42 68 Q 57.5 73 73 68 L 115 46 L 115 12 Z" fill="url(#glassCylinderGrad)" stroke="#475569" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

    <!-- 3D Top Flange Rim -->
    <ellipse cx="57.5" cy="12" rx="57.5" ry="6.5" fill="url(#glassRimGrad)" stroke="#64748b" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 5. CYLINDRICAL CLEAN WATER TANKS (Filter Feed, Treated Water, Soft Water)
# ==============================================================================
def get_clean_water_tank(tank_type, state):
    if tank_type == 'filter-feed':
        grad = 'url(#filterFeedGrad)'
        meniscus_color = '#7dd3fc'
        stroke_color = '#0284c7'
    elif tank_type == 'treated':
        grad = 'url(#treatedWaterGrad)'
        meniscus_color = '#bae6fd'
        stroke_color = '#0284c7'
    else:  # soft water
        grad = 'url(#softWaterGrad)'
        meniscus_color = '#38bdf8'
        stroke_color = '#0369a1'

    wave_anim = """    <g>
      <ellipse cx="70" cy="24" rx="68" ry="6.5" fill="{meniscus_color}" stroke="{stroke_color}" stroke-width="0.8" opacity="0.9">
        <animate attributeName="ry" values="6.5;7.5;6.5" dur="2.4s" repeatCount="indefinite" />
      </ellipse>
    </g>""".format(meniscus_color=meniscus_color, stroke_color=stroke_color) if state == 'fluid-animated' else f"""    <ellipse cx="70" cy="24" rx="68" ry="6.5" fill="{meniscus_color}" stroke="{stroke_color}" stroke-width="0.8" opacity="0.9" />"""

    fluid_block = f"""  <!-- Water Fluid Volume with 3D Dish Bottom & Meniscus -->
  <path d="M 2 24 Q 70 38 138 24 L 138 76 Q 70 93 2 76 Z" fill="{grad}" />
{wave_anim}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 120" width="170" height="120">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="100" rx="72" ry="8" fill="#0b2545" opacity="0.22" filter="url(#bottomShadow)" />

  <g transform="translate(15, 10)">
    <!-- 2.5D Cylindrical Vessel Hull with Curved Dish Bottom -->
    <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="{stroke_color}" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

    <!-- Specular Light Glare -->
    <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" pointer-events="none" />
    <line x1="134" y1="16" x2="134" y2="76" stroke="#ffffff" stroke-width="1.2" opacity="0.4" />

    <!-- 3D Top Rim Flange -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="{stroke_color}" stroke-width="1.5" />
    <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93c5fd" stroke-width="1" stroke-dasharray="2 2" />
  </g>
</svg>"""

# ==============================================================================
# 6. FLASH MIXER & FLOCCULATOR TANKS (Dished Cylinder + Agitators)
# ==============================================================================
def get_mixer_tank(mixer_type, state):
    is_flash = mixer_type == 'flash-mixer'
    agitator = """    <!-- Center Vertical Agitator Drive & High-Speed Turbine Impeller -->
    <rect x="62" y="4" width="16" height="12" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1" />
    <line x1="70" y1="16" x2="70" y2="72" stroke="#475569" stroke-width="2.5" />
    <path d="M 52 70 L 88 70 M 52 66 L 52 74 M 88 66 L 88 74" stroke="#0284c7" stroke-width="2.5" />""" if is_flash else """    <!-- Slow Multi-Paddle Flocculation Reel -->
    <rect x="62" y="4" width="16" height="12" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1" />
    <line x1="70" y1="16" x2="70" y2="78" stroke="#475569" stroke-width="2.5" />
    <rect x="44" y="40" width="52" height="12" fill="none" stroke="#64748b" stroke-width="1.8" />
    <rect x="40" y="60" width="60" height="14" fill="none" stroke="#64748b" stroke-width="1.8" />"""

    vortex_anim = """      <animateTransform attributeName="transform" type="rotate" values="0 70 70; 360 70 70" dur="0.8s" repeatCount="indefinite" />""" if (state == 'fluid-animated' and is_flash) else ""

    fluid_block = f"""  <!-- Process Fluid Volume -->
  <path d="M 2 28 Q 70 42 138 28 L 138 76 Q 70 93 2 76 Z" fill="url(#filterFeedGrad)" />
  <ellipse cx="70" cy="28" rx="68" ry="6.5" fill="#7dd3fc" stroke="#0284c7" stroke-width="0.8" opacity="0.9" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 120" width="170" height="120">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="100" rx="72" ry="8" fill="#0b2545" opacity="0.22" filter="url(#bottomShadow)" />

  <g transform="translate(15, 10)">
    <!-- 2.5D Dished Cylinder Hull -->
    <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284c7" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

    <g>
{agitator}
{vortex_anim}
    </g>

    <!-- 3D Top Rim Flange -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284c7" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 7. HORIZONTAL BULLET STORAGE TANK (Hemispherical Dish Ends + Saddles)
# ==============================================================================
def get_horizontal_tank(state):
    fluid_block = """  <!-- Fluid Volume with Horizontal Meniscus -->
  <path d="M 32 50 Q 18 65 32 80 L 168 80 Q 182 65 168 50 Z" fill="url(#treatedWaterGrad)" />
  <line x1="32" y1="50" x2="168" y2="50" stroke="#bae6fd" stroke-width="1.5" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" width="200" height="120">
{COMMON_DEFS}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="100" cy="102" rx="88" ry="7" fill="#0b2545" opacity="0.25" filter="url(#bottomShadow)" />

  <!-- Saddle Support Feet -->
  <rect x="45" y="85" width="14" height="14" fill="#334155" stroke="#475569" stroke-width="1.2" />
  <rect x="141" y="85" width="14" height="14" fill="#334155" stroke="#475569" stroke-width="1.2" />

  <!-- Horizontal Vessel Hull with Hemispherical Dished Heads -->
  <path d="M 30 35 L 170 35 Q 192 60 170 85 L 30 85 Q 8 60 30 35 Z" fill="url(#glassCylinderGrad)" stroke="#64748b" stroke-width="2" />

{fluid_block if 'fluid' in state else ''}

  <!-- Top Inspection Manway Dome -->
  <rect x="90" y="24" width="20" height="11" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.2" />
  <ellipse cx="100" cy="24" rx="12" ry="3.5" fill="url(#glassRimGrad)" stroke="#94a3b8" stroke-width="1.2" />

  <!-- Cylindrical Highlight Sheen -->
  <line x1="30" y1="42" x2="170" y2="42" stroke="#ffffff" stroke-width="2.5" opacity="0.4" stroke-linecap="round" />
</svg>"""

# ==============================================================================
# 8. RAINWATER HARVESTING POND (Natural Embankment Reservoir)
# ==============================================================================
def get_rainwater_pond(state):
    ripple_anim = """    <ellipse cx="100" cy="65" rx="40" ry="16" fill="none" stroke="#7dd3fc" stroke-width="1.2" opacity="0.8">
      <animate attributeName="rx" values="35;65" dur="2.5s" repeatCount="indefinite" />
      <animate attributeName="ry" values="14;26" dur="2.5s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.8;0" dur="2.5s" repeatCount="indefinite" />
    </ellipse>""" if state == 'fluid-animated' else ""

    fluid_block = f"""  <!-- Water Surface -->
  <ellipse cx="100" cy="65" rx="72" ry="28" fill="url(#treatedWaterGrad)" stroke="#38bdf8" stroke-width="1.5" />
{ripple_anim}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" width="200" height="120">
{COMMON_DEFS}
  <!-- Embankment Basin Hull -->
  <ellipse cx="100" cy="65" rx="88" ry="38" fill="#1e293b" stroke="#475569" stroke-width="2.5" />
  <ellipse cx="100" cy="65" rx="80" ry="33" fill="#334155" />

{fluid_block if 'fluid' in state else ''}

  <!-- Overflow Weir Notch & Aerator Float -->
  <circle cx="100" cy="65" r="5" fill="#f8fafc" stroke="#0284c7" stroke-width="1" />
</svg>"""

def update_all_tanks():
    print("=== REGENERATING ALL 33 TANKS WITH EXACT SCHEMATIC GEOMETRIES ===")
    states = ['dry-static', 'fluid-static', 'fluid-animated']

    tanks_map = {
        'collection-tank': get_collection_tank,
        'aeration-tank': get_aeration_tank,
        'clarifier-tank': get_clarifier_tank,
        'sludge-holding-tank': get_sludge_tank,
        'filter-feed-tank': lambda st: get_clean_water_tank('filter-feed', st),
        'treated-water-tank': lambda st: get_clean_water_tank('treated', st),
        'soft-water-tank': lambda st: get_clean_water_tank('soft', st),
        'flash-mixer-tank': lambda st: get_mixer_tank('flash-mixer', st),
        'flocculator-tank': lambda st: get_mixer_tank('flocculator', st),
        'horizontal-storage-tank': get_horizontal_tank,
        'rainwater-pond': get_rainwater_pond
    }

    count = 0
    for tank_name, generator in tanks_map.items():
        for st in states:
            xml_content = generator(st)
            filename = f"{tank_name}-{st}.svg"
            filepath = os.path.join(TANKS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(xml_content.strip() + '\n')
            count += 1
            print(f"  + Generated {filename}")

    print(f"Successfully updated {count} tank SVGs with 100% exact schematic page geometry!")

if __name__ == '__main__':
    update_all_tanks()
