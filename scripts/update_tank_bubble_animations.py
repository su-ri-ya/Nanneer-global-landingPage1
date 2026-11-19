import os
import re

BASE_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"
TANKS_DIR = os.path.join(BASE_DIR, "tanks")
FILTERS_DIR = os.path.join(BASE_DIR, "filters")

# 1. Collection Tank with Staggered Coarse Air Diffuser Bubbles
COLLECTION_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes coll-wave {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
      }
      .anim-c-wave { animation: coll-wave 2.8s ease-in-out infinite; }
    </style>
    <linearGradient id="ct_liquor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#334155" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#1e293b" stop-opacity="0.98" />
    </linearGradient>
  </defs>

  <!-- Tank Outer Hull -->
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>

  <!-- Sewage Raw Influent Volume -->
  <rect x="33" y="65" width="254" height="82" rx="6" fill="url(#ct_liquor)"/>

  <!-- Undulating Surface Wave -->
  <g class="anim-c-wave">
    <path d="M 33 65 Q 96 58 160 65 T 287 65" fill="none" stroke="#94a3b8" stroke-width="3"/>
  </g>

  <!-- Coarse Bar Screen Cutaway (Left Influent) -->
  <rect x="33" y="55" width="16" height="50" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
  <line x1="38" y1="58" x2="38" y2="102" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="44" y1="58" x2="44" y2="102" stroke="#94a3b8" stroke-width="1.5"/>

  <!-- Submerged Bottom Air Diffuser Pipe -->
  <line x1="50" y1="135" x2="270" y2="135" stroke="#d97706" stroke-width="3" stroke-linecap="round"/>
  <circle cx="75" cy="135" r="3" fill="#ca8a04"/>
  <circle cx="115" cy="135" r="3" fill="#ca8a04"/>
  <circle cx="155" cy="135" r="3" fill="#ca8a04"/>
  <circle cx="195" cy="135" r="3" fill="#ca8a04"/>
  <circle cx="235" cy="135" r="3" fill="#ca8a04"/>

  <!-- Staggered Rising Coarse Bubbles (Matching Website Schematic Exact Durations & Delays) -->
  <g>
    <!-- Stream 1 -->
    <circle cx="75" cy="135" r="4" fill="#cbd5e1" opacity="0.7">
      <animate attributeName="cy" values="135;68" dur="1.4s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.85;0" dur="1.4s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="r" values="3.0;4.8" dur="1.4s" begin="0.1s" repeatCount="indefinite" />
    </circle>
    <!-- Stream 2 -->
    <circle cx="115" cy="135" r="5" fill="#e2e8f0" opacity="0.75">
      <animate attributeName="cy" values="135;68" dur="1.1s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.9;0" dur="1.1s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="r" values="3.5;5.5" dur="1.1s" begin="0.3s" repeatCount="indefinite" />
    </circle>
    <!-- Stream 3 -->
    <circle cx="155" cy="135" r="4.2" fill="#cbd5e1" opacity="0.7">
      <animate attributeName="cy" values="135;68" dur="1.3s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.85;0" dur="1.3s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="r" values="3.0;5.0" dur="1.3s" begin="0.s" repeatCount="indefinite" />
    </circle>
    <!-- Stream 4 -->
    <circle cx="195" cy="135" r="4.8" fill="#e2e8f0" opacity="0.75">
      <animate attributeName="cy" values="135;68" dur="1.2s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.9;0" dur="1.2s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="r" values="3.2;5.2" dur="1.2s" begin="0.2s" repeatCount="indefinite" />
    </circle>
    <!-- Stream 5 -->
    <circle cx="235" cy="135" r="3.8" fill="#cbd5e1" opacity="0.7">
      <animate attributeName="cy" values="135;68" dur="1.5s" begin="0.4s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.85;0" dur="1.5s" begin="0.4s" repeatCount="indefinite" />
      <animate attributeName="r" values="2.8;4.5" dur="1.5s" begin="0.4s" repeatCount="indefinite" />
    </circle>
    <!-- Stream 6 -->
    <circle cx="255" cy="135" r="4.4" fill="#e2e8f0" opacity="0.75">
      <animate attributeName="cy" values="135;68" dur="1.0s" begin="0.5s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.2;0.9;0" dur="1.0s" begin="0.5s" repeatCount="indefinite" />
      <animate attributeName="r" values="3.0;5.0" dur="1.0s" begin="0.5s" repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Left Inlet & Right Bottom Drain -->
  <line x1="50" y1="20" x2="50" y2="70" stroke="#94a3b8" stroke-width="4"/>
  <line x1="270" y1="130" x2="300" y2="130" stroke="#94a3b8" stroke-width="4"/>
</svg>"""

# 2. Aeration Tank (MBBR) with Fine EPDM Diffuser Grid, Rising Staggered Bubbles & Tumbling Media
AERATION_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes mbbr-wave {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
      }
      @keyframes carrier-sway {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(180deg); }
      }
      .anim-a-wave { animation: mbbr-wave 2.5s ease-in-out infinite; }
      .anim-k1 { animation: carrier-sway 3.5s ease-in-out infinite; }
    </style>
    <linearGradient id="at_liquor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0891b2" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#0e7490" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#155e75" stop-opacity="0.95" />
    </linearGradient>
  </defs>

  <!-- Tank Outer Hull -->
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>

  <!-- Aerated Mixed Liquor Volume -->
  <rect x="33" y="60" width="254" height="87" rx="6" fill="url(#at_liquor)"/>

  <!-- Undulating Surface Wave -->
  <g class="anim-a-wave">
    <path d="M 33 60 Q 65 52 97 60 T 161 60 T 225 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>

  <!-- Bottom Fine-Bubble EPDM Aeration Diffuser Grid -->
  <line x1="45" y1="135" x2="275" y2="135" stroke="#d97706" stroke-width="3" stroke-linecap="round"/>
  <circle cx="65" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="95" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="125" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="155" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="185" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="215" cy="135" r="3.5" fill="#ca8a04"/>
  <circle cx="245" cy="135" r="3.5" fill="#ca8a04"/>

  <!-- Staggered Rising Fine Bubbles (Exact Durations & Delays from Schematic Page) -->
  <g>
    <!-- Bubble Stream 1 -->
    <circle cx="65" cy="135" r="2.2" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="135;62" dur="1.1s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.1s" begin="0s" repeatCount="indefinite" />
      <animate attributeName="r" values="1.8;3.2" dur="1.1s" begin="0s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 2 -->
    <circle cx="95" cy="135" r="3.0" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="135;62" dur="0.9s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="0.9s" begin="0.2s" repeatCount="indefinite" />
      <animate attributeName="r" values="2.2;3.8" dur="0.9s" begin="0.2s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 3 -->
    <circle cx="125" cy="135" r="2.0" fill="#e0f2fe" opacity="0.8">
      <animate attributeName="cy" values="135;62" dur="1.3s" begin="0.4s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.3s" begin="0.4s" repeatCount="indefinite" />
      <animate attributeName="r" values="1.6;3.0" dur="1.3s" begin="0.4s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 4 -->
    <circle cx="155" cy="135" r="2.8" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="135;62" dur="1.0s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.0s" begin="0.1s" repeatCount="indefinite" />
      <animate attributeName="r" values="2.0;3.6" dur="1.0s" begin="0.1s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 5 -->
    <circle cx="185" cy="135" r="2.4" fill="#e0f2fe" opacity="0.8">
      <animate attributeName="cy" values="135;62" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
      <animate attributeName="r" values="1.8;3.4" dur="0.8s" begin="0.3s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 6 -->
    <circle cx="215" cy="135" r="2.6" fill="#ffffff" opacity="0.85">
      <animate attributeName="cy" values="135;62" dur="1.2s" begin="0.15s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.2s" begin="0.15s" repeatCount="indefinite" />
      <animate attributeName="r" values="1.9;3.5" dur="1.2s" begin="0.15s" repeatCount="indefinite" />
    </circle>
    <!-- Bubble Stream 7 -->
    <circle cx="245" cy="135" r="2.5" fill="#e0f2fe" opacity="0.8">
      <animate attributeName="cy" values="135;62" dur="1.05s" begin="0.35s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.3;0.95;0" dur="1.05s" begin="0.35s" repeatCount="indefinite" />
      <animate attributeName="r" values="1.8;3.3" dur="1.05s" begin="0.35s" repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Tumbling K1 Biofilm Media Carriers (Yellow Wheels) -->
  <g class="anim-k1">
    <circle cx="85" cy="85" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="125" cy="95" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="165" cy="80" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="205" cy="90" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="235" cy="82" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
  </g>

  <!-- Sieve Screen at Effluent Exit (Right) -->
  <rect x="270" y="52" width="14" height="42" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
  <line x1="274" y1="56" x2="274" y2="90" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="280" y1="56" x2="280" y2="90" stroke="#94a3b8" stroke-width="1.5"/>
</svg>"""

with open(os.path.join(TANKS_DIR, "collection-tank-fluid-animated.svg"), "w", encoding="utf-8") as f:
    f.write(COLLECTION_ANIM.strip() + "\n")
print("  + Updated collection-tank-fluid-animated.svg with staggered coarse air diffuser bubbles")

with open(os.path.join(TANKS_DIR, "aeration-tank-fluid-animated.svg"), "w", encoding="utf-8") as f:
    f.write(AERATION_ANIM.strip() + "\n")
print("  + Updated aeration-tank-fluid-animated.svg with EPDM diffuser grid & staggered rising fine bubbles")

def make_static(svg_xml):
    # Remove <style>...</style> block
    s = re.sub(r'<style>[\s\S]*?</style>', '', svg_xml)
    # Remove <animate ... /> tags
    s = re.sub(r'<animate[\s\S]*?/>', '', s)
    # Remove animation classes
    s = s.replace('class="anim-c-wave"', '').replace('class="anim-a-wave"', '').replace('class="anim-k1"', '')
    # Remove empty <style> or empty lines
    return s.strip() + '\n'

with open(os.path.join(TANKS_DIR, "collection-tank-fluid-static.svg"), "w", encoding="utf-8") as f:
    f.write(make_static(COLLECTION_ANIM))

with open(os.path.join(TANKS_DIR, "aeration-tank-fluid-static.svg"), "w", encoding="utf-8") as f:
    f.write(make_static(AERATION_ANIM))

print("Both Collection and Aeration tanks updated successfully!")

