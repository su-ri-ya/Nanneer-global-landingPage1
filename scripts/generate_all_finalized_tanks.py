import os
import shutil

TARGET_DIR = os.path.join('public', 'schematic asserts', 'tank')

# Clean directory
if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
os.makedirs(TARGET_DIR, exist_ok=True)

# Shared base filter
FILTER_BOTTOM_SHADOW = """    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>"""

GRAD_GLASS_CYLINDER = """    <linearGradient id="glassCylinderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.5" />
      <stop offset="8%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="22%" stop-color="#F8FAFC" stop-opacity="0.3" />
      <stop offset="70%" stop-color="#E0F2FE" stop-opacity="0.2" />
      <stop offset="92%" stop-color="#38BDF8" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.5" />
    </linearGradient>"""

GRAD_GLASS_RIM = """    <linearGradient id="glassRimGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#94A3B8" stop-opacity="0.8" />
      <stop offset="25%" stop-color="#FFFFFF" stop-opacity="0.95" />
      <stop offset="70%" stop-color="#E2E8F0" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#64748B" stop-opacity="0.9" />
    </linearGradient>"""

GRAD_SPECULAR_SHEEN = """    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.35" />
      <stop offset="30%" stop-color="#FFFFFF" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </linearGradient>"""

# ==============================================================================
# 1. COLLECTION TANK
# ==============================================================================
def gen_collection_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#795548" stop-opacity="0.90" />
      <stop offset="45%" stop-color="#5D4037" stop-opacity="0.94" />
      <stop offset="100%" stop-color="#3E2723" stop-opacity="0.97" />
    </linearGradient>
    <linearGradient id="rawSewageWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A1887F" stop-opacity="0.90" />
      <stop offset="40%" stop-color="#6D4C41" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#3E2723" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="rawSewageWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8D6E63" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#4E342E" stop-opacity="0.92" />
    </linearGradient>
    <clipPath id="collectionTankFluidClip">
      <path d="M 2 16 Q 87.5 24 173 16 L 173 76 Q 87.5 93 2 76 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    # Fluid block
    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Raw Sewage Fluid Body with Active Animated Waves & Falling Drops -->
    <g clip-path="url(#collectionTankFluidClip)">
      <path d="M 2 45 Q 87.5 57 173 45 L 173 76 Q 87.5 93 2 76 Z" fill="url(#rawSewageGrad)" />
      <!-- Wave Layer 1: Back Wave -->
      <path d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 240 95 L -60 95 Z" fill="url(#rawSewageWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <!-- Wave Layer 2: Front Wave -->
      <path d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z" fill="url(#rawSewageWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <!-- 3D Liquid Meniscus -->
      <ellipse cx="87.5" cy="45" rx="85.5" ry="6.5" fill="#5D4037" opacity="0.35" />

      <!-- Dynamic Wastewater Dropping Stream & Droplets -->
      <g id="collection-tank-water-drops">
        <line x1="17" y1="20" x2="17" y2="45" stroke="#8D6E63" stroke-width="1.6" stroke-dasharray="3 3" opacity="0.6">
          <animate attributeName="stroke-dashoffset" from="12" to="0" dur="0.5s" repeatCount="indefinite" />
        </line>
        <ellipse cx="17" cy="22" rx="1.6" ry="2.2" fill="#8D6E63">
          <animate attributeName="cy" values="20; 45" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.9; 1; 0.2" dur="0.65s" repeatCount="indefinite" />
        </ellipse>
        <ellipse cx="17" cy="22" rx="1.3" ry="1.9" fill="#A1887F">
          <animate attributeName="cy" values="20; 45" begin="0.22s" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.9; 1; 0.2" begin="0.22s" dur="0.65s" repeatCount="indefinite" />
        </ellipse>
        <ellipse cx="17" cy="22" rx="1.5" ry="2.0" fill="#6D4C41">
          <animate attributeName="cy" values="20; 45" begin="0.44s" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.9; 1; 0.2" begin="0.44s" dur="0.65s" repeatCount="indefinite" />
        </ellipse>
        <!-- Expanding Surface Ripples -->
        <ellipse cx="17" cy="45" rx="2" ry="0.8" fill="none" stroke="#D7CCC8" stroke-width="0.8">
          <animate attributeName="rx" values="1.5; 8" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="ry" values="0.6; 2.2" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.9; 0" dur="0.65s" repeatCount="indefinite" />
        </ellipse>
        <ellipse cx="17" cy="45" rx="2" ry="0.8" fill="none" stroke="#D7CCC8" stroke-width="0.8">
          <animate attributeName="rx" values="1.5; 8" begin="0.32s" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="ry" values="0.6; 2.2" begin="0.32s" dur="0.65s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.9; 0" begin="0.32s" dur="0.65s" repeatCount="indefinite" />
        </ellipse>
      </g>
    </g>
    <!-- Inlet Nozzle Stub -->
    <path d="M 0 16 L 17 16 L 17 20" stroke="#8D6E63" stroke-width="4.5" fill="none" stroke-linejoin="round" />
    <rect x="13" y="19" width="8" height="2.5" rx="0.8" fill="#5D4037" />"""
        else:
            fluid_content = """    <!-- Raw Sewage Fluid Body (Static) -->
    <g clip-path="url(#collectionTankFluidClip)">
      <path d="M 2 45 Q 87.5 57 173 45 L 173 76 Q 87.5 93 2 76 Z" fill="url(#rawSewageGrad)" />
      <ellipse cx="87.5" cy="45" rx="85.5" ry="6.5" fill="#5D4037" opacity="0.35" />
      <line x1="17" y1="20" x2="17" y2="45" stroke="#8D6E63" stroke-width="1.6" stroke-dasharray="3 3" opacity="0.6" />
      <ellipse cx="17" cy="32" rx="1.6" ry="2.2" fill="#8D6E63" />
      <ellipse cx="17" cy="45" rx="4" ry="1.2" fill="none" stroke="#D7CCC8" stroke-width="0.8" opacity="0.7" />
    </g>
    <!-- Inlet Nozzle Stub -->
    <path d="M 0 16 L 17 16 L 17 20" stroke="#8D6E63" stroke-width="4.5" fill="none" stroke-linejoin="round" />
    <rect x="13" y="19" width="8" height="2.5" rx="0.8" fill="#5D4037" />"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 205 125" width="205" height="125">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="102" cy="104" rx="88" ry="8" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 76 Q 87.5 94 175 76 L 175 14 Q 87.5 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Cylindrical Specular Glare -->
    <rect x="6" y="16" width="16" height="58" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim Opening -->
    <ellipse cx="87.5" cy="14" rx="87.5" ry="8" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    <ellipse cx="87.5" cy="14" rx="82" ry="5.5" fill="none" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3 3" opacity="0.6" />
  </g>
</svg>"""

# ==============================================================================
# 2. MBBR AERATION TANK (100% Faithful - ZERO internal pipes, ZERO K1 media)
# ==============================================================================
def gen_aeration_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A1887F" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#8D6E63" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#5D4037" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="mbbrWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#BCAAA4" stop-opacity="0.92" />
      <stop offset="45%" stop-color="#8D6E63" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#4E342E" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="mbbrWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A1887F" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#5D4037" stop-opacity="0.92" />
    </linearGradient>
    <clipPath id="mbbrTankFluidClip">
      <path d="M 2 16 Q 70 24 138 16 L 138 76 Q 70 93 2 76 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        bubbles_list = [
            {"cx": 24, "r": 1.8, "dur": 3.4, "delay": 0.0, "sway": 2.0},
            {"cx": 32, "r": 2.4, "dur": 2.8, "delay": 0.8, "sway": -2.5},
            {"cx": 42, "r": 1.5, "dur": 3.8, "delay": 1.6, "sway": 1.8},
            {"cx": 50, "r": 2.2, "dur": 3.0, "delay": 0.4, "sway": -1.5},
            {"cx": 60, "r": 1.6, "dur": 3.6, "delay": 2.0, "sway": 2.2},
            {"cx": 68, "r": 2.5, "dur": 2.7, "delay": 1.1, "sway": -2.0},
            {"cx": 78, "r": 1.7, "dur": 3.5, "delay": 0.2, "sway": 1.6},
            {"cx": 86, "r": 2.3, "dur": 2.9, "delay": 1.9, "sway": -2.4},
            {"cx": 96, "r": 1.5, "dur": 3.9, "delay": 0.6, "sway": 1.5},
            {"cx": 104, "r": 2.2, "dur": 3.1, "delay": 2.3, "sway": -1.8},
            {"cx": 114, "r": 1.8, "dur": 3.3, "delay": 1.4, "sway": 2.0},
            {"cx": 28, "r": 1.4, "dur": 4.1, "delay": 2.7, "sway": -1.2},
            {"cx": 56, "r": 2.0, "dur": 3.2, "delay": 1.0, "sway": 1.7},
            {"cx": 74, "r": 1.6, "dur": 3.7, "delay": 2.5, "sway": -1.9},
            {"cx": 92, "r": 2.1, "dur": 3.0, "delay": 0.9, "sway": 2.1},
            {"cx": 110, "r": 1.5, "dur": 4.0, "delay": 1.7, "sway": -1.4},
        ]

        if is_anim:
            bubbles_xml = ""
            for b in bubbles_list:
                bubbles_xml += f"""        <circle cx="{b['cx']}" cy="78" r="{b['r']}" fill="#FFFFFF" stroke="#7DD3FC" stroke-width="0.5" opacity="0.85">
          <animate attributeName="cy" values="78; 67; 56; 46" keyTimes="0; 0.35; 0.75; 1" dur="{b['dur']}s" begin="{b['delay']}s" repeatCount="indefinite" />
          <animate attributeName="cx" values="{b['cx']}; {b['cx'] + b['sway']}; {b['cx'] - b['sway']}; {b['cx']}" keyTimes="0; 0.33; 0.66; 1" dur="{b['dur']}s" begin="{b['delay']}s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.1; 0.85; 0.9; 0" keyTimes="0; 0.15; 0.85; 1" dur="{b['dur']}s" begin="{b['delay']}s" repeatCount="indefinite" />
        </circle>\n"""

            fluid_content = f"""    <!-- Aerated Bio-Mix Fluid Body (50% Waterline) -->
    <g clip-path="url(#mbbrTankFluidClip)">
      <path d="M 2 45 Q 70 59 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#mbbrWaterGrad)" />
      <!-- Wave Layer 1: Back Wave -->
      <path d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z" fill="url(#mbbrWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <!-- Wave Layer 2: Front Wave -->
      <path d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z" fill="url(#mbbrWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <!-- Soft Meniscus Blend -->
      <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#A1887F" opacity="0.35" />
    </g>

    <!-- 16 Rising Aeration Micro-Bubbles (Exact from Schematic) -->
    <g id="mbbr-aeration-bubbles">
{bubbles_xml}    </g>"""
        else:
            bubbles_xml = ""
            for b in bubbles_list:
                bubbles_xml += f"""        <circle cx="{b['cx']}" cy="60" r="{b['r']}" fill="#FFFFFF" stroke="#7DD3FC" stroke-width="0.5" opacity="0.85" />\n"""
            fluid_content = f"""    <!-- Aerated Bio-Mix Fluid Body (Static) -->
    <g clip-path="url(#mbbrTankFluidClip)">
      <path d="M 2 45 Q 70 59 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#mbbrWaterGrad)" />
      <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#A1887F" opacity="0.35" />
    </g>
    <g id="mbbr-aeration-bubbles">
{bubbles_xml}    </g>"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 125" width="170" height="125">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="104" rx="72" ry="8" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Cylindrical Specular Glare -->
    <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93C5FD" stroke-width="1" stroke-dasharray="2 2" />
  </g>
</svg>"""

# ==============================================================================
# 3. SECONDARY CLARIFIER / TUBE SETTLER
# ==============================================================================
def gen_clarifier_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}
    <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="70%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>"""

    if has_fluid:
        defs += """
    <linearGradient id="clarifierWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#D2C59D" stop-opacity="0.88" />
      <stop offset="35%" stop-color="#B8AA7B" stop-opacity="0.86" />
      <stop offset="100%" stop-color="#786940" stop-opacity="0.92" />
    </linearGradient>
    <linearGradient id="clarifierWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F5EEDC" stop-opacity="0.95" />
      <stop offset="40%" stop-color="#D2C59D" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#8C7B4F" stop-opacity="0.94" />
    </linearGradient>
    <linearGradient id="clarifierWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#B8AA7B" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#5C4F2E" stop-opacity="0.9" />
    </linearGradient>
    <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5D4037" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#3E2723" stop-opacity="0.97" />
      <stop offset="100%" stop-color="#211109" stop-opacity="0.99" />
    </linearGradient>
    <clipPath id="clarifierWaterClip">
      <path d="M 2 16 L 2 54 L 138 54 L 138 16 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Supernatant Clarified Water Zone -->
    <g clip-path="url(#clarifierWaterClip)">
      <path d="M 2 45 L 2 54 L 138 54 L 138 45 Z" fill="url(#clarifierWaterGrad)" opacity="0.88" />
      <path d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 54 L -60 54 Z" fill="url(#clarifierWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <path d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 54 L -88 54 Z" fill="url(#clarifierWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#D2C59D" opacity="0.35" />
    </g>

    <!-- Settled Biological Sludge Blanket in Conical Hopper Apex -->
    <path d="M 2 54 L 54 88 Q 70 93 86 88 L 138 54 Z" fill="url(#sludgeWaterGrad)" />

    <!-- Peripheral V-Notch Overflow Weir Trough -->
    <path d="M 4 20 L 136 20" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.75" />

    <!-- Submerged Rotating Clarifier Bridge & Scraper Rake Arm -->
    <g transform="translate(70, 52)">
      <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" stroke-width="1.5" />
      <circle cx="0" cy="0" r="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.2" />
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="2.5s" repeatCount="indefinite" />
        <line x1="-12" y1="0" x2="12" y2="0" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
        <line x1="0" y1="-12" x2="0" y2="12" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
        <!-- Rake Teeth Sweepers -->
        <line x1="-8" y1="-3" x2="-8" y2="3" stroke="#15803D" stroke-width="1.2" />
        <line x1="8" y1="-3" x2="8" y2="3" stroke="#15803D" stroke-width="1.2" />
        <line x1="-3" y1="-8" x2="3" y2="-8" stroke="#15803D" stroke-width="1.2" />
        <line x1="-3" y1="8" x2="3" y2="8" stroke="#15803D" stroke-width="1.2" />
      </g>
      <circle cx="0" cy="0" r="3.5" fill="#15803D" />
    </g>"""
        else:
            fluid_content = """    <!-- Supernatant Clarified Water Zone (Static) -->
    <g clip-path="url(#clarifierWaterClip)">
      <path d="M 2 45 L 2 54 L 138 54 L 138 45 Z" fill="url(#clarifierWaterGrad)" opacity="0.88" />
      <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#D2C59D" opacity="0.35" />
    </g>
    <!-- Settled Biological Sludge Blanket -->
    <path d="M 2 54 L 54 88 Q 70 93 86 88 L 138 54 Z" fill="url(#sludgeWaterGrad)" />
    <!-- Peripheral V-Notch Overflow Weir Trough -->
    <path d="M 4 20 L 136 20" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.75" />
    <!-- Scraper Rake Arm -->
    <g transform="translate(70, 52)">
      <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" stroke-width="1.5" />
      <circle cx="0" cy="0" r="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.2" />
      <line x1="-12" y1="0" x2="12" y2="0" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
      <line x1="0" y1="-12" x2="0" y2="12" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
      <circle cx="0" cy="0" r="3.5" fill="#15803D" />
    </g>"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 130" width="170" height="130">
{defs}
  <!-- 3D Ground Contact Shadow under Conical Tip -->
  <ellipse cx="85" cy="112" rx="58" ry="7" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Conical Hopper Tank Hull (Cylindrical Upper + 60° Conical Funnel Bottom) -->
    <path d="M 0 14 L 0 54 L 54 88 Q 70 93 86 88 L 140 54 L 140 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Specular Glare -->
    <rect x="5" y="16" width="14" height="42" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim Opening -->
    <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    <ellipse cx="70" cy="14" rx="65" ry="5.0" fill="none" stroke="#93C5FD" stroke-width="1" stroke-dasharray="2 2" />
  </g>
</svg>"""

# ==============================================================================
# 4. SLUDGE HOLDING TANK
# ==============================================================================
def gen_sludge_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5D4037" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#3E2723" stop-opacity="0.97" />
      <stop offset="100%" stop-color="#211109" stop-opacity="0.99" />
    </linearGradient>
    <linearGradient id="sludgeWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8D6E63" stop-opacity="0.95" />
      <stop offset="40%" stop-color="#5D4037" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#271406" stop-opacity="0.98" />
    </linearGradient>
    <linearGradient id="sludgeWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6D4C41" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#3E2723" stop-opacity="0.95" />
    </linearGradient>
    <clipPath id="sludgeTankFluidClip">
      <path d="M 2 14 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 14 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Thickened Biological Sludge Body with Dual Waves -->
    <path d="M 2 39 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 39 Z" fill="url(#sludgeWaterGrad)" />
    <ellipse cx="57.5" cy="39" rx="55.5" ry="5.5" fill="#5D4037" stroke="#8D6E63" stroke-width="0.8" opacity="0.95" />

    <g clip-path="url(#sludgeTankFluidClip)">
      <path d="M 2 39 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 39 Z" fill="url(#sludgeWaterGrad)" />
      <!-- Sludge Wave 1 -->
      <path d="M -50 39 q 12.5 -4.5, 25 0 t 25 0 t 25 0 t 25 0 t 25 0 t 25 0 t 25 0 L 165 75 L -50 75 Z" fill="url(#sludgeWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-50 0" to="0 0" dur="3.4s" repeatCount="indefinite" />
      </path>
      <!-- Sludge Wave 2 -->
      <path d="M -72 39 q 18 -5.5, 36 0 t 36 0 t 36 0 t 36 0 t 36 0 L 180 75 L -72 75 Z" fill="url(#sludgeWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-72 0" dur="2.4s" repeatCount="indefinite" />
      </path>
      <ellipse cx="57.5" cy="39" rx="55.5" ry="5.5" fill="#8D6E63" opacity="0.3" />
    </g>"""
        else:
            fluid_content = """    <!-- Thickened Biological Sludge Body (Static) -->
    <path d="M 2 39 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 39 Z" fill="url(#sludgeWaterGrad)" />
    <ellipse cx="57.5" cy="39" rx="55.5" ry="5.5" fill="#5D4037" stroke="#8D6E63" stroke-width="0.8" opacity="0.95" />"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 145 110" width="145" height="110">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="72" cy="94" rx="48" ry="6" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- Conical Hopper Vessel Hull -->
    <path d="M 0 12 L 0 46 L 42 68 Q 57.5 73 73 68 L 115 46 L 115 12 Z" fill="url(#glassCylinderGrad)" stroke="#94A3B8" stroke-width="1.5" />

{fluid_content}

    <!-- Specular Highlight Glare -->
    <rect x="4" y="14" width="12" height="32" rx="2" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Flange Rim -->
    <ellipse cx="57.5" cy="12" rx="57.5" ry="6.5" fill="url(#glassRimGrad)" stroke="#94A3B8" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 5. FILTER FEED TANK
# ==============================================================================
def gen_filter_feed_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#D1F4EC" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#80CBC4" stop-opacity="0.86" />
      <stop offset="100%" stop-color="#00695C" stop-opacity="0.92" />
    </linearGradient>
    <linearGradient id="filterFeedWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.95" />
      <stop offset="40%" stop-color="#4DD0E1" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#00838F" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="filterFeedWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#80CBC4" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#004D40" stop-opacity="0.92" />
    </linearGradient>
    <clipPath id="filterFeedTankFluidClip">
      <path d="M 2 16 Q 70 24 138 16 L 138 76 Q 70 93 2 76 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Secondary Settled Effluent Fluid Body with Waves -->
    <g clip-path="url(#filterFeedTankFluidClip)">
      <path d="M 2 45 Q 70 57 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#filterFeedGrad)" />
      <!-- Wave Layer 1: Back Wave -->
      <path d="M -60 45 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z" fill="url(#filterFeedWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <!-- Wave Layer 2: Front Wave -->
      <path d="M -88 45 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z" fill="url(#filterFeedWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <!-- 3D Liquid Meniscus -->
      <ellipse cx="70" cy="45" rx="68" ry="6.0" fill="#E0F2FE" opacity="0.3" />
    </g>"""
        else:
            fluid_content = """    <!-- Secondary Settled Effluent Fluid Body (Static) -->
    <g clip-path="url(#filterFeedTankFluidClip)">
      <path d="M 2 45 Q 70 57 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#filterFeedGrad)" />
      <ellipse cx="70" cy="45" rx="68" ry="6.0" fill="#E0F2FE" opacity="0.3" />
    </g>"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 125" width="170" height="125">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="104" rx="72" ry="8" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Cylindrical Specular Glare -->
    <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 6. TREATED WATER TANK (100% Clean Interior - ZERO internal pipes, ZERO arrows)
# ==============================================================================
def gen_treated_water_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#38BDF8" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="treatedWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F0F9FF" stop-opacity="0.95" />
      <stop offset="40%" stop-color="#38BDF8" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="treatedWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#0369A1" stop-opacity="0.90" />
    </linearGradient>
    <clipPath id="treatedWaterTankFluidClip">
      <path d="M 2 16 Q 70 24 138 16 L 138 74 Q 70 89 2 74 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Treated Pure Water Fluid Body with Waves -->
    <g clip-path="url(#treatedWaterTankFluidClip)">
      <path d="M 2 48 Q 70 59 138 48 L 138 74 Q 70 89 2 74 Z" fill="url(#treatedWaterGrad)" />
      <!-- Wave Layer 1: Back Wave -->
      <path d="M -60 48 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z" fill="url(#treatedWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <!-- Wave Layer 2: Front Wave -->
      <path d="M -88 48 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z" fill="url(#treatedWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <!-- 3D Liquid Meniscus -->
      <ellipse cx="70" cy="48" rx="68" ry="6.0" fill="#E0F2FE" opacity="0.3" />
    </g>"""
        else:
            fluid_content = """    <!-- Treated Pure Water Fluid Body (Static) -->
    <g clip-path="url(#treatedWaterTankFluidClip)">
      <path d="M 2 48 Q 70 59 138 48 L 138 74 Q 70 89 2 74 Z" fill="url(#treatedWaterGrad)" />
      <ellipse cx="70" cy="48" rx="68" ry="6.0" fill="#E0F2FE" opacity="0.3" />
    </g>"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 125" width="170" height="125">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="102" rx="72" ry="8" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Cylindrical Glare Streak (Clean Interior - ZERO arrows, ZERO dip lines) -->
    <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 7. SOFT WATER TANK
# ==============================================================================
def gen_soft_water_tank(state):
    is_anim = state == 'fluid-animated'
    has_fluid = 'fluid' in state

    defs = f"""  <defs>
{FILTER_BOTTOM_SHADOW}
{GRAD_GLASS_CYLINDER}
{GRAD_GLASS_RIM}
{GRAD_SPECULAR_SHEEN}"""

    if has_fluid:
        defs += """
    <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ECFEFF" stop-opacity="0.98" />
      <stop offset="45%" stop-color="#06B6D4" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.98" />
    </linearGradient>
    <linearGradient id="softWaterWaveFront" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96" />
      <stop offset="40%" stop-color="#67E8F9" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#0EA5E9" stop-opacity="0.96" />
    </linearGradient>
    <linearGradient id="softWaterWaveBack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A5F3FC" stop-opacity="0.70" />
      <stop offset="100%" stop-color="#0891B2" stop-opacity="0.92" />
    </linearGradient>
    <clipPath id="softWaterTankFluidClip">
      <path d="M 2 16 Q 70 24 138 16 L 138 74 Q 70 89 2 74 Z" />
    </clipPath>"""

    defs += "\n  </defs>"

    if has_fluid:
        if is_anim:
            fluid_content = """    <!-- Pristine Polished Soft Water Body with Waves -->
    <g clip-path="url(#softWaterTankFluidClip)">
      <path d="M 2 48 Q 70 59 138 48 L 138 74 Q 70 89 2 74 Z" fill="url(#softWaterGrad)" />
      <!-- Wave Layer 1: Back Wave -->
      <path d="M -60 48 q 15 -5.5, 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 t 30 0 L 210 95 L -60 95 Z" fill="url(#softWaterWaveBack)">
        <animateTransform attributeName="transform" type="translate" from="-60 0" to="0 0" dur="3.2s" repeatCount="indefinite" />
      </path>
      <!-- Wave Layer 2: Front Wave -->
      <path d="M -88 48 q 22 -6.5, 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 t 44 0 L 264 95 L -88 95 Z" fill="url(#softWaterWaveFront)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-88 0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <!-- 3D Liquid Meniscus -->
      <ellipse cx="70" cy="48" rx="68" ry="6.0" fill="#F0F9FF" opacity="0.35" />
    </g>"""
        else:
            fluid_content = """    <!-- Pristine Polished Soft Water Body (Static) -->
    <g clip-path="url(#softWaterTankFluidClip)">
      <path d="M 2 48 Q 70 59 138 48 L 138 74 Q 70 89 2 74 Z" fill="url(#softWaterGrad)" />
      <ellipse cx="70" cy="48" rx="68" ry="6.0" fill="#F0F9FF" opacity="0.35" />
    </g>"""
    else:
        fluid_content = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 125" width="170" height="125">
{defs}
  <!-- 3D Ground Contact Shadow -->
  <ellipse cx="85" cy="102" rx="72" ry="8" fill="#0F172A" opacity="0.25" filter="url(#bottomShadow)" />

  <g transform="translate(15, 12)">
    <!-- 2.5D Glass Cylinder Body & Dish Bottom -->
    <path d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />

{fluid_content}

    <!-- Cylindrical Glare Streak -->
    <rect x="5" y="16" width="14" height="54" rx="3" fill="url(#specularSheen)" pointer-events="none" />

    <!-- 3D Top Glass Vessel Flange & Rim -->
    <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
  </g>
</svg>"""

# ==============================================================================
# 8. FACILITY BUILDING (Light Architectural Theme)
# ==============================================================================
def gen_facility_building(state):
    is_anim = state == 'animated' or state == 'fluid-animated'

    defs = """  <defs>
    <linearGradient id="buildingFacadeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="25%" stop-color="#F8FAFC" />
      <stop offset="70%" stop-color="#F1F5F9" />
      <stop offset="100%" stop-color="#E2E8F0" />
    </linearGradient>
    <linearGradient id="buildingGlassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#BAE6FD" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#7DD3FC" stop-opacity="0.95" />
    </linearGradient>
    <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="70%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.35" />
      <stop offset="30%" stop-color="#FFFFFF" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </linearGradient>
  </defs>"""

    beacon_anim = """      <circle cx="38" cy="0" r="1.6" fill="#0284C7">
        <animate attributeName="opacity" values="1; 0.3; 1" dur="1.2s" repeatCount="indefinite" />
      </circle>""" if is_anim else """      <circle cx="38" cy="0" r="1.6" fill="#0284C7" />"""

    badge_anim = """      <circle cx="-18" cy="0" r="1.8" fill="#16A34A">
        <animate attributeName="opacity" values="1; 0.4; 1" dur="2s" repeatCount="indefinite" />
      </circle>""" if is_anim else """      <circle cx="-18" cy="0" r="1.8" fill="#16A34A" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75 125" width="75" height="125">
{defs}
  <g transform="translate(10, 22)">
    <!-- 1. 3D Grounding Soft Contact Shadow -->
    <ellipse cx="26" cy="80" rx="26" ry="5.5" fill="#64748B" opacity="0.25" />
    <ellipse cx="26" cy="80" rx="18" ry="3.2" fill="#334155" opacity="0.30" />

    <!-- 2. Architectural Concrete Foundation Pedestal -->
    <rect x="0" y="74" width="52" height="6" rx="1.5" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1" />
    <line x1="1" y1="75" x2="51" y2="75" stroke="#FFFFFF" stroke-width="0.8" opacity="0.9" />

    <!-- 3. Main Architectural Tower Body (2.5D Stepped Light Monolith) -->
    <rect x="4" y="14" width="44" height="60" rx="2" fill="url(#buildingFacadeGrad)" stroke="#94A3B8" stroke-width="1.2" />

    <!-- 4. Rooftop Parapet, Terrace & Perimeter Railing -->
    <rect x="2" y="10" width="48" height="4.5" rx="1" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="0.8" />
    <line x1="5" y1="8" x2="47" y2="8" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3 1.5" opacity="0.85" />

    <!-- Rooftop HVAC Mechanical Penthouse -->
    <rect x="8" y="3.5" width="16" height="7" rx="1" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="0.8" />
    <line x1="10" y1="5.5" x2="22" y2="5.5" stroke="#94A3B8" stroke-width="0.7" />
    <line x1="10" y1="7.5" x2="22" y2="7.5" stroke="#94A3B8" stroke-width="0.7" />

    <!-- Telecommunications Mast & Active Beacon -->
    <line x1="38" y1="10" x2="38" y2="0" stroke="#64748B" stroke-width="1.2" />
{beacon_anim}

    <!-- 5. Curtain-Wall Panoramic Window Bays & Architectural Spandrels -->
    <!-- Floor 4 -->
    <rect x="7" y="16" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <rect x="25" y="16" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <line x1="15" y1="16" x2="15" y2="25.5" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="33" y1="16" x2="33" y2="25.5" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="4" y1="27.5" x2="48" y2="27.5" stroke="#CBD5E1" stroke-width="1.4" />

    <!-- Floor 3 -->
    <rect x="7" y="29.5" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <rect x="25" y="29.5" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <line x1="15" y1="29.5" x2="15" y2="39" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="33" y1="29.5" x2="33" y2="39" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="4" y1="41" x2="48" y2="41" stroke="#CBD5E1" stroke-width="1.4" />

    <!-- Floor 2 -->
    <rect x="7" y="43" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <rect x="25" y="43" width="16" height="9.5" rx="1" fill="url(#buildingGlassGrad)" stroke="#38BDF8" stroke-width="0.6" />
    <line x1="15" y1="43" x2="15" y2="52.5" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="33" y1="43" x2="33" y2="52.5" stroke="#0284C7" stroke-width="0.5" opacity="0.5" />
    <line x1="4" y1="54.5" x2="48" y2="54.5" stroke="#CBD5E1" stroke-width="1.4" />

    <!-- Ground Floor Entrance Lobby & Canopy -->
    <rect x="14" y="58" width="20" height="16" rx="1" fill="#FFFFFF" stroke="#0284C7" stroke-width="0.8" />
    <rect x="11" y="56.5" width="26" height="2.5" rx="0.5" fill="#0284C7" opacity="0.9" />
    <rect x="16" y="60" width="7.5" height="14" fill="#E0F2FE" stroke="#38BDF8" stroke-width="0.5" />
    <rect x="24.5" y="60" width="7.5" height="14" fill="#E0F2FE" stroke="#38BDF8" stroke-width="0.5" />
    <line x1="24" y1="60" x2="24" y2="74" stroke="#0284C7" stroke-width="0.6" />

    <!-- 6. Cylindrical Glass Specular Glare -->
    <rect x="6" y="15" width="8" height="58" rx="2" fill="url(#specularSheen)" opacity="0.8" pointer-events="none" />

    <!-- 7. Industrial Sewer Discharge Manifold (ANSI Flange) -->
    <g id="building-sewer-discharge-manifold" transform="translate(45, 26)">
      <rect x="0" y="0" width="5.5" height="8" rx="1" fill="url(#metalRingGrad)" stroke="#64748B" stroke-width="0.8" />
      <circle cx="2.7" cy="1.6" r="0.65" fill="#334155" />
      <circle cx="2.7" cy="6.4" r="0.65" fill="#334155" />
    </g>

    <!-- 8. Precision SCADA Identification Badge (Light Mode) -->
    <g transform="translate(26, -8)">
      <rect x="-24" y="-7" width="48" height="14" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="1" />
{badge_anim}
      <text x="3" y="-1.5" fill="#0369A1" font-size="4.6" font-weight="bold" text-anchor="middle" font-family="monospace">BUILDING</text>
      <text x="3" y="3.5" fill="#64748B" font-size="3" font-weight="bold" text-anchor="middle" font-family="monospace">SEWER SOURCE</text>
    </g>
  </g>
</svg>"""

def main():
    print("=== REGENERATING 100% FAITHFUL SCHEMATIC TANK SVGS ===")

    tanks = {
        'collection-tank': gen_collection_tank,
        'aeration-tank': gen_aeration_tank,
        'clarifier-tank': gen_clarifier_tank,
        'sludge-holding-tank': gen_sludge_tank,
        'filter-feed-tank': gen_filter_feed_tank,
        'treated-water-tank': gen_treated_water_tank,
        'soft-water-tank': gen_soft_water_tank,
        'facility-building': gen_facility_building,
    }

    count = 0
    for name, func in tanks.items():
        if name == 'facility-building':
            st_list = ['animated', 'static']
        else:
            st_list = ['fluid-animated', 'fluid-static', 'dry-static']

        for st in st_list:
            svg = func(st).strip() + '\n'
            filename = f"{name}-{st}.svg"
            path = os.path.join(TARGET_DIR, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(svg)
            count += 1
            print(f"  + Generated: {filename}")

    print(f"\nDone! Successfully generated {count} SVGs strictly matching the schematic in '{TARGET_DIR}'.")

if __name__ == '__main__':
    main()
