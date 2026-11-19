import os
import re

OUT_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets\svg-animated"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Centrifugal Pump Animated (Spinning Impeller & Flow Pulse)
SVG_PUMP_CENTRIFUGAL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 264" width="300" height="264">
  <defs>
    <style>
      @keyframes spin-cw {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes pulse-flow {
        0%, 100% { opacity: 0.35; r: 16px; }
        50% { opacity: 0.85; r: 24px; }
      }
      .animated-impeller {
        transform-origin: 150px 132px;
        animation: spin-cw 1.8s linear infinite;
      }
      .animated-flow {
        animation: pulse-flow 2s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_pc_case" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="50%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="an_pc_fluid" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" />
      <stop offset="65%" stop-color="#0284c7" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.4" />
    </radialGradient>
    <filter id="an_pc_shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.5" />
    </filter>
  </defs>

  <!-- Mounting Base -->
  <rect x="70" y="212" width="160" height="14" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" filter="url(#an_pc_shadow)"/>
  <rect x="100" y="200" width="100" height="12" fill="#334155" />

  <!-- Motor Housing -->
  <rect x="180" y="96" width="65" height="72" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2" />
  <line x1="192" y1="96" x2="192" y2="168" stroke="#334155" stroke-width="2" />
  <line x1="204" y1="96" x2="204" y2="168" stroke="#334155" stroke-width="2" />
  <line x1="216" y1="96" x2="216" y2="168" stroke="#334155" stroke-width="2" />
  <line x1="228" y1="96" x2="228" y2="168" stroke="#334155" stroke-width="2" />

  <!-- Pump Volute Casing Outer Ring -->
  <circle cx="150" cy="132" r="66" fill="url(#an_pc_case)" stroke="#64748b" stroke-width="4" filter="url(#an_pc_shadow)"/>
  <!-- Status Ring (Emerald Green Active) -->
  <circle cx="150" cy="132" r="54" fill="#0f172a" stroke="#10b981" stroke-width="3" stroke-dasharray="4 2" />

  <!-- Fluid Chamber Glow -->
  <circle cx="150" cy="132" r="46" fill="url(#an_pc_fluid)" />
  <circle cx="150" cy="132" r="20" fill="#00e5ff" class="animated-flow" />

  <!-- Rotating 4-Blade Impeller (CSS Keyframe Spin) -->
  <g class="animated-impeller">
    <path d="M 150 132 Q 135 102 150 88 Q 165 102 150 132 Z" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5" />
    <path d="M 150 132 Q 180 117 194 132 Q 180 147 150 132 Z" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5" />
    <path d="M 150 132 Q 165 162 150 176 Q 135 162 150 132 Z" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5" />
    <path d="M 150 132 Q 120 147 106 132 Q 120 117 150 132 Z" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5" />
    <!-- Hub Bolt -->
    <circle cx="150" cy="132" r="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <circle cx="150" cy="132" r="4" fill="#38bdf8" />
  </g>

  <!-- Discharge Nozzle (Top) -->
  <rect x="138" y="44" width="24" height="24" fill="#1e293b" stroke="#475569" stroke-width="2" />
  <rect x="132" y="38" width="36" height="8" rx="2" fill="#334155" stroke="#64748b" stroke-width="2" />
  <!-- Suction Flange (Left) -->
  <rect x="62" y="120" width="24" height="24" fill="#1e293b" stroke="#475569" stroke-width="2" />
  <rect x="56" y="114" width="8" height="36" rx="2" fill="#334155" stroke="#64748b" stroke-width="2" />

  <!-- Directional Flow Arrow Loop -->
  <path d="M 124 96 A 38 38 0 0 1 176 96" fill="none" stroke="#67e8f9" stroke-width="3" stroke-linecap="round" />
  <polygon points="182,96 172,90 174,102" fill="#67e8f9" />
</svg>
"""

# 2. SCADA Aeration Blower Animated (Rapid Rotary Impeller Spin)
SVG_BLOWER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 264" width="264" height="264">
  <defs>
    <style>
      @keyframes spin-blower {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      .animated-blower-blades {
        transform-origin: 132px 132px;
        animation: spin-blower 0.8s linear infinite;
      }
    </style>
    <linearGradient id="an_bl_casing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="50%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="an_bl_center" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="80%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0f172a" />
    </radialGradient>
  </defs>
  <!-- Base Plate -->
  <rect x="66" y="210" width="132" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="88" y="196" width="88" height="14" fill="#334155"/>
  <!-- Outer Casing -->
  <circle cx="132" cy="132" r="70" fill="url(#an_bl_casing)" stroke="#64748b" stroke-width="4"/>
  <!-- Status Ring (Emerald Running) -->
  <circle cx="132" cy="132" r="58" fill="#0f172a" stroke="#10b981" stroke-width="3" stroke-dasharray="3 3"/>
  <circle cx="132" cy="132" r="50" fill="#0284c7" fill-opacity="0.2"/>

  <!-- Rapid Spinning Multi-Blade Impeller -->
  <g class="animated-blower-blades">
    <!-- 8 aerodynamic curved blades -->
    <path d="M 132 132 Q 120 100 132 86 Q 140 100 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 155 110 165 100 Q 155 125 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 164 120 178 132 Q 164 140 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 155 155 165 164 Q 140 155 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 120 164 132 178 Q 140 164 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 110 155 100 165 Q 110 140 132 132 Z" fill="#38bdf8" />
    <path d="M 132 132 Q 100 120 86 132 Q 100 140 132 132 Z" fill="#67e8f9" />
    <path d="M 132 132 Q 110 110 100 100 Q 125 110 132 132 Z" fill="#38bdf8" />
    <!-- Hub -->
    <circle cx="132" cy="132" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <circle cx="132" cy="132" r="6" fill="#38bdf8"/>
  </g>

  <!-- Discharge Flange Top Right -->
  <path d="M 172 88 L 210 60 L 218 72 L 182 98 Z" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="212" y="56" width="10" height="24" rx="2" fill="#475569" transform="rotate(35 217 68)"/>
</svg>
"""

# 3. RO High-Pressure Multistage Pump Animated (Upward Fluid Pulsing & Cooling Fan)
SVG_PUMP_RO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 424" width="240" height="424">
  <defs>
    <style>
      @keyframes stage-flow {
        0% { transform: translateY(0); opacity: 0.3; }
        50% { opacity: 0.95; }
        100% { transform: translateY(-40px); opacity: 0.3; }
      }
      @keyframes motor-fan {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
      }
      .animated-stream {
        animation: stage-flow 1.5s linear infinite;
      }
      .animated-motor-pulse {
        animation: motor-fan 0.8s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_ro_casing" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="25%" stop-color="#94a3b8" />
      <stop offset="60%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
    <linearGradient id="an_ro_fluid" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="50%" stop-color="#00e5ff" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>
  </defs>
  <!-- Floor Base -->
  <rect x="40" y="380" width="160" height="18" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="65" y="360" width="110" height="20" fill="#334155" stroke="#64748b" stroke-width="1.5"/>

  <!-- Lower Suction/Discharge Pump Base -->
  <rect x="75" y="310" width="90" height="50" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <!-- Suction Port -->
  <rect x="35" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="25" y="316" width="10" height="38" rx="2" fill="#475569"/>
  <!-- Discharge Port -->
  <rect x="165" y="322" width="40" height="26" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="205" y="316" width="10" height="38" rx="2" fill="#475569"/>

  <!-- Vertical Stainless Multistage Barrel -->
  <rect x="85" y="150" width="70" height="160" rx="3" fill="url(#an_ro_casing)" stroke="#64748b" stroke-width="2"/>
  <!-- Sight Glass Tube -->
  <rect x="105" y="160" width="30" height="140" rx="4" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <!-- Fluid Upward Pulse -->
  <g class="animated-stream">
    <circle cx="120" cy="280" r="5" fill="#00e5ff" />
    <circle cx="120" cy="240" r="6" fill="#38bdf8" />
    <circle cx="120" cy="200" r="5" fill="#67e8f9" />
    <circle cx="120" cy="160" r="4" fill="#e0f2fe" />
    <path d="M 112 290 Q 120 270 128 290" fill="none" stroke="#00e5ff" stroke-width="2"/>
    <path d="M 112 250 Q 120 230 128 250" fill="none" stroke="#00e5ff" stroke-width="2"/>
    <path d="M 112 210 Q 120 190 128 210" fill="none" stroke="#00e5ff" stroke-width="2"/>
  </g>

  <!-- Stage Ring Clamps -->
  <line x1="85" y1="180" x2="155" y2="180" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="210" x2="155" y2="210" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="240" x2="155" y2="240" stroke="#334155" stroke-width="3"/>
  <line x1="85" y1="270" x2="155" y2="270" stroke="#334155" stroke-width="3"/>

  <!-- Lantern Coupling -->
  <rect x="80" y="125" width="80" height="25" fill="#334155" stroke="#475569" stroke-width="2"/>
  <line x1="95" y1="125" x2="95" y2="150" stroke="#1e293b" stroke-width="3"/>
  <line x1="120" y1="125" x2="120" y2="150" stroke="#1e293b" stroke-width="3"/>
  <line x1="145" y1="125" x2="145" y2="150" stroke="#1e293b" stroke-width="3"/>

  <!-- Top Electric Motor -->
  <rect x="75" y="35" width="90" height="90" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <rect x="70" y="25" width="100" height="10" rx="3" fill="#334155" class="animated-motor-pulse"/>
  <!-- Cooling Fins -->
  <line x1="85" y1="35" x2="85" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="95" y1="35" x2="95" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="105" y1="35" x2="105" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="115" y1="35" x2="115" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="125" y1="35" x2="125" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="135" y1="35" x2="135" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="145" y1="35" x2="145" y2="125" stroke="#334155" stroke-width="2"/>
  <line x1="155" y1="35" x2="155" y2="125" stroke="#334155" stroke-width="2"/>
  <!-- Eyebolt -->
  <circle cx="120" cy="18" r="8" fill="none" stroke="#64748b" stroke-width="3"/>
</svg>
"""

# 4. Chemical Dosing Metering Pump Animated (Pulsing Diaphragm Stroke & Droplet Injection)
SVG_PUMP_DOSING = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 390" width="230" height="390">
  <defs>
    <style>
      @keyframes diaphragm-stroke {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.12); }
      }
      @keyframes inject-drop {
        0% { transform: translateY(0); opacity: 1; }
        80% { transform: translateY(30px); opacity: 0.8; }
        100% { transform: translateY(45px); opacity: 0; }
      }
      .animated-diaphragm {
        transform-origin: 115px 190px;
        animation: diaphragm-stroke 1.2s ease-in-out infinite;
      }
      .animated-drop {
        animation: inject-drop 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      }
    </style>
    <linearGradient id="an_dp_body" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <radialGradient id="an_dp_chem" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f43f5e" />
      <stop offset="70%" stop-color="#be123c" />
      <stop offset="100%" stop-color="#881337" />
    </radialGradient>
  </defs>
  <!-- Wall Mount Bracket -->
  <rect x="35" y="110" width="30" height="150" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <circle cx="50" cy="130" r="4" fill="#64748b"/>
  <circle cx="50" cy="240" r="4" fill="#64748b"/>

  <!-- Drive Motor Housing -->
  <rect x="65" y="125" width="85" height="120" rx="8" fill="url(#an_dp_body)" stroke="#64748b" stroke-width="2"/>
  <!-- Status LED -->
  <circle cx="130" cy="145" r="5" fill="#10b981"/>

  <!-- Liquid End / PVDF Dosing Head -->
  <rect x="135" y="145" width="55" height="85" rx="6" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
  <!-- Pulsing Diaphragm Window -->
  <circle cx="162" cy="187" r="22" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
  <circle cx="162" cy="187" r="16" fill="url(#an_dp_chem)" class="animated-diaphragm"/>

  <!-- Suction Valve (Bottom Port) -->
  <rect x="152" y="230" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="148" y1="270" x2="176" y2="270" stroke="#94a3b8" stroke-width="3"/>

  <!-- Droplets Injected Downward -->
  <g class="animated-drop">
    <ellipse cx="162" cy="290" rx="4" ry="6" fill="#f43f5e" />
  </g>

  <!-- Discharge Valve (Top Port) -->
  <rect x="152" y="105" width="20" height="40" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <line x1="148" y1="105" x2="176" y2="105" stroke="#94a3b8" stroke-width="3"/>
  <path d="M 162 105 L 162 70 L 195 70" fill="none" stroke="#f43f5e" stroke-width="4" stroke-linecap="round"/>
</svg>
"""

# 5. HVAC Cooling Tower Animated (Top Fan Spin & Cascading Falling Drops)
SVG_COOLING_TOWER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 336 368" width="336" height="368">
  <defs>
    <style>
      @keyframes spin-fan {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes water-cascade {
        0% { transform: translateY(0); opacity: 0.2; }
        50% { opacity: 0.9; }
        100% { transform: translateY(40px); opacity: 0.1; }
      }
      .animated-fan-blades {
        transform-origin: 168px 56px;
        animation: spin-fan 0.9s linear infinite;
      }
      .animated-rain {
        animation: water-cascade 1.1s linear infinite;
      }
    </style>
    <linearGradient id="an_ct_basin" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#075985" />
    </linearGradient>
    <linearGradient id="an_ct_fill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
  </defs>

  <!-- Structural Legs -->
  <line x1="50" y1="300" x2="50" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="110" y1="300" x2="110" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="226" y1="300" x2="226" y2="345" stroke="#475569" stroke-width="6"/>
  <line x1="286" y1="300" x2="286" y2="345" stroke="#475569" stroke-width="6"/>

  <!-- Cold Water Basin -->
  <rect x="40" y="270" width="256" height="35" rx="4" fill="url(#an_ct_basin)" stroke="#38bdf8" stroke-width="2"/>
  <line x1="42" y1="278" x2="294" y2="278" stroke="#67e8f9" stroke-width="2" stroke-dasharray="8 4"/>

  <!-- PVC Honeycomb Fill Chamber -->
  <rect x="52" y="140" width="232" height="120" fill="url(#an_ct_fill)" stroke="#475569" stroke-width="2"/>
  <!-- Louver Grid Lines -->
  <line x1="52" y1="164" x2="284" y2="164" stroke="#334155" stroke-width="2"/>
  <line x1="52" y1="188" x2="284" y2="188" stroke="#334155" stroke-width="2"/>
  <line x1="52" y1="212" x2="284" y2="212" stroke="#334155" stroke-width="2"/>
  <line x1="52" y1="236" x2="284" y2="236" stroke="#334155" stroke-width="2"/>

  <!-- Cascading Falling Water Droplets -->
  <g class="animated-rain">
    <line x1="80" y1="150" x2="80" y2="168" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="120" y1="160" x2="120" y2="178" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="168" y1="150" x2="168" y2="172" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="210" y1="165" x2="210" y2="183" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="250" y1="152" x2="250" y2="170" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="100" y1="195" x2="100" y2="215" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="150" y1="200" x2="150" y2="220" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
    <line x1="190" y1="192" x2="190" y2="212" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    <line x1="230" y1="205" x2="230" y2="225" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
  </g>

  <!-- Hot Water Spray Distribution Header -->
  <rect x="62" y="125" width="212" height="12" fill="#334155" stroke="#64748b" stroke-width="1.5"/>

  <!-- Drift Eliminator Pack -->
  <rect x="70" y="105" width="196" height="18" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>

  <!-- Fan Cowl / Shroud Top -->
  <path d="M 100 105 L 120 40 L 216 40 L 236 105 Z" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <ellipse cx="168" cy="40" rx="48" ry="14" fill="#0f172a" stroke="#64748b" stroke-width="2"/>

  <!-- Top Induced Draft Fan Blades (Spinning) -->
  <g class="animated-fan-blades">
    <ellipse cx="168" cy="42" rx="42" ry="7" fill="#67e8f9" fill-opacity="0.9" />
    <ellipse cx="168" cy="42" rx="7" ry="42" fill="#38bdf8" fill-opacity="0.9" />
    <circle cx="168" cy="42" r="9" fill="#0f172a" stroke="#bae6fd" stroke-width="2"/>
  </g>
</svg>
"""

# 6. STP MBBR Aeration Bio-Reactor Animated (Wavy Meniscus, Rising Bubbles & Floating K1 Carriers)
SVG_STP_MBBR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180">
  <defs>
    <style>
      @keyframes bubble-rise {
        0% { transform: translateY(0); opacity: 0.1; }
        50% { opacity: 0.8; }
        100% { transform: translateY(-70px); opacity: 0; }
      }
      @keyframes carrier-tumble {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(180deg); }
      }
      @keyframes wave-sway {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
      }
      .animated-bubbles {
        animation: bubble-rise 2s linear infinite;
      }
      .animated-carriers {
        animation: carrier-tumble 3.5s ease-in-out infinite;
      }
      .animated-wave {
        animation: wave-sway 2.5s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_mbbr_liquor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0891b2" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#0e7490" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#155e75" stop-opacity="0.95" />
    </linearGradient>
  </defs>

  <!-- Tank Cylindrical Hull -->
  <rect x="30" y="30" width="260" height="120" rx="8" fill="#0f172a" stroke="#475569" stroke-width="3"/>

  <!-- Aerated Mixed Liquor Volume -->
  <rect x="33" y="60" width="254" height="87" rx="6" fill="url(#an_mbbr_liquor)"/>

  <!-- Undulating Surface Wave -->
  <g class="animated-wave">
    <path d="M 33 60 Q 65 52 97 60 T 161 60 T 225 60 T 287 60" fill="none" stroke="#67e8f9" stroke-width="3"/>
  </g>

  <!-- Coarse Bubble Diffuser Pipe at Bottom -->
  <line x1="50" y1="135" x2="270" y2="135" stroke="#94a3b8" stroke-width="4"/>
  <circle cx="80" cy="135" r="3" fill="#cbd5e1"/>
  <circle cx="120" cy="135" r="3" fill="#cbd5e1"/>
  <circle cx="160" cy="135" r="3" fill="#cbd5e1"/>
  <circle cx="200" cy="135" r="3" fill="#cbd5e1"/>
  <circle cx="240" cy="135" r="3" fill="#cbd5e1"/>

  <!-- Rising Aeration Bubbles -->
  <g class="animated-bubbles">
    <circle cx="75" cy="125" r="3.5" fill="#e0f2fe"/>
    <circle cx="85" cy="110" r="2.5" fill="#bae6fd"/>
    <circle cx="115" cy="120" r="3" fill="#e0f2fe"/>
    <circle cx="125" cy="100" r="4" fill="#bae6fd"/>
    <circle cx="155" cy="125" r="3" fill="#e0f2fe"/>
    <circle cx="165" cy="105" r="2" fill="#bae6fd"/>
    <circle cx="195" cy="120" r="3.5" fill="#e0f2fe"/>
    <circle cx="205" cy="95" r="4" fill="#bae6fd"/>
    <circle cx="235" cy="125" r="3" fill="#e0f2fe"/>
    <circle cx="245" cy="105" r="2.5" fill="#bae6fd"/>
  </g>

  <!-- Tumbling K1 Biofilm Media Carriers -->
  <g class="animated-carriers">
    <circle cx="100" cy="85" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="140" cy="95" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="180" cy="80" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <circle cx="220" cy="90" r="7" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
  </g>

  <!-- Effluent Retention Sieve Grid (Right) -->
  <rect x="270" y="50" width="14" height="40" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
  <line x1="274" y1="55" x2="274" y2="85" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="280" y1="55" x2="280" y2="85" stroke="#94a3b8" stroke-width="1.5"/>
</svg>
"""

# 7. STP Secondary Clarifier Animated (Conical Hopper with Rotating Scraper Arm)
SVG_STP_CLARIFIER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 192" width="320" height="192">
  <defs>
    <style>
      @keyframes bridge-sweep {
        0%, 100% { transform: scaleX(1); }
        50% { transform: scaleX(-1); }
      }
      @keyframes ripple-launder {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
      }
      .animated-scraper {
        transform-origin: 160px 48px;
        animation: bridge-sweep 6s ease-in-out infinite;
      }
      .animated-launder {
        animation: ripple-launder 2s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_sc_clarified" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.8" />
      <stop offset="60%" stop-color="#0369a1" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#78350f" stop-opacity="0.95" />
    </linearGradient>
  </defs>

  <!-- Top Cylindrical Rim -->
  <rect x="30" y="30" width="260" height="40" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
  <!-- 60 Degree Conical Sludge Hopper -->
  <polygon points="30,70 145,170 175,170 290,70" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>

  <!-- Liquid & Settled Sludge Bed -->
  <polygon points="33,70 147,167 173,167 287,70" fill="url(#an_sc_clarified)"/>

  <!-- Peripheral V-Notch Overflow Launder -->
  <rect x="30" y="35" width="16" height="12" fill="#0284c7" class="animated-launder"/>
  <rect x="274" y="35" width="16" height="12" fill="#0284c7" class="animated-launder"/>

  <!-- Center Drive Hub -->
  <rect x="150" y="16" width="20" height="24" rx="3" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="160" cy="28" r="4" fill="#10b981"/>

  <!-- Rotating Scraper Bridge Arm with Rake Teeth -->
  <g class="animated-scraper">
    <line x1="160" y1="36" x2="160" y2="140" stroke="#94a3b8" stroke-width="4"/>
    <!-- Angled Rake Arm -->
    <line x1="160" y1="140" x2="230" y2="90" stroke="#cbd5e1" stroke-width="3"/>
    <!-- Teeth -->
    <line x1="180" y1="126" x2="180" y2="136" stroke="#94a3b8" stroke-width="2"/>
    <line x1="200" y1="112" x2="200" y2="122" stroke="#94a3b8" stroke-width="2"/>
    <line x1="220" y1="98" x2="220" y2="108" stroke="#94a3b8" stroke-width="2"/>
  </g>

  <!-- Bottom Sludge Apex Extraction Line -->
  <rect x="152" y="170" width="16" height="16" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>
"""

# 8. ETP Flash Mixer Tank Animated (High-Speed Turbine Impeller Spin & Dosing Vortex)
SVG_ETP_FLASH_MIXER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 318" width="300" height="318">
  <defs>
    <style>
      @keyframes spin-flash {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes vortex-pulse {
        0%, 100% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.15); opacity: 0.95; }
      }
      .animated-turbine {
        transform-origin: 150px 240px;
        animation: spin-flash 0.6s linear infinite;
      }
      .animated-vortex {
        transform-origin: 150px 140px;
        animation: vortex-pulse 1.4s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_fm_fluid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="50%" stop-color="#334155" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
  </defs>

  <!-- Tank Vessel -->
  <rect x="40" y="80" width="220" height="200" rx="10" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="44" y="110" width="212" height="166" rx="6" fill="url(#an_fm_fluid)"/>

  <!-- Chemical Dosing Vortex Shimmer -->
  <ellipse cx="150" cy="115" rx="55" ry="14" fill="#a855f7" fill-opacity="0.5" class="animated-vortex"/>

  <!-- Gear Motor on Top Bridge -->
  <rect x="30" y="70" width="240" height="12" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="125" y="24" width="50" height="46" rx="5" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>

  <!-- Vertical Shaft -->
  <line x1="150" y1="70" x2="150" y2="240" stroke="#cbd5e1" stroke-width="5"/>

  <!-- High-Speed Turbine Impeller (Fast Spin) -->
  <g class="animated-turbine">
    <ellipse cx="150" cy="240" rx="42" ry="8" fill="#a855f7" />
    <ellipse cx="150" cy="240" rx="8" ry="42" fill="#d8b4fe" />
    <circle cx="150" cy="240" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
  </g>
</svg>
"""

# 9. ETP Flocculator Tank Animated (Dual Slow Paddle Agitators Rotating)
SVG_ETP_FLOCCULATOR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 318" width="360" height="318">
  <defs>
    <style>
      @keyframes paddle-spin-1 {
        0%, 100% { transform: scaleX(1); }
        50% { transform: scaleX(-1); }
      }
      @keyframes paddle-spin-2 {
        0%, 100% { transform: scaleX(-1); }
        50% { transform: scaleX(1); }
      }
      .animated-paddle-1 {
        transform-origin: 120px 200px;
        animation: paddle-spin-1 4s ease-in-out infinite;
      }
      .animated-paddle-2 {
        transform-origin: 240px 200px;
        animation: paddle-spin-2 4s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_floc_fluid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.9" />
    </linearGradient>
  </defs>

  <!-- Basin -->
  <rect x="30" y="90" width="300" height="190" rx="10" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <rect x="34" y="120" width="292" height="156" rx="6" fill="url(#an_floc_fluid)"/>

  <!-- Top Walkway Bridge -->
  <rect x="20" y="80" width="320" height="14" fill="#334155" stroke="#475569" stroke-width="2"/>

  <!-- Drive Units -->
  <rect x="100" y="42" width="40" height="38" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <rect x="220" y="42" width="40" height="38" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2"/>

  <!-- Shafts -->
  <line x1="120" y1="80" x2="120" y2="240" stroke="#cbd5e1" stroke-width="4"/>
  <line x1="240" y1="80" x2="240" y2="240" stroke="#cbd5e1" stroke-width="4"/>

  <!-- Paddle Agitator 1 -->
  <g class="animated-paddle-1">
    <rect x="80" y="160" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="80" y="210" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
  </g>

  <!-- Paddle Agitator 2 -->
  <g class="animated-paddle-2">
    <rect x="200" y="160" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="200" y="210" width="80" height="16" rx="3" fill="#60a5fa" stroke="#93c5fd" stroke-width="1.5"/>
  </g>
</svg>
"""

# 10. ETP DAF (Dissolved Air Flotation) Tank Animated (Micro-Bubble Cloud & Top Scum Skimmer)
SVG_ETP_DAF = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240" width="340" height="240">
  <defs>
    <style>
      @keyframes micro-bubble {
        0% { transform: translateY(0); opacity: 0.1; }
        60% { opacity: 0.9; }
        100% { transform: translateY(-80px); opacity: 0; }
      }
      @keyframes scum-skimmer {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(35px); }
      }
      .animated-microbubbles {
        animation: micro-bubble 1.8s linear infinite;
      }
      .animated-skimmer {
        animation: scum-skimmer 4s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_daf_water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#075985" stop-opacity="0.95" />
    </linearGradient>
  </defs>

  <!-- DAF Flotation Hull -->
  <polygon points="30,60 270,60 270,180 230,210 70,210 30,180" fill="#0f172a" stroke="#475569" stroke-width="3"/>
  <polygon points="34,80 266,80 266,178 228,206 72,206 34,178" fill="url(#an_daf_water)"/>

  <!-- Top Floating Scum Layer -->
  <rect x="34" y="70" width="232" height="16" fill="#854d0e" fill-opacity="0.8"/>

  <!-- Scum Beach Ramp (Right) -->
  <polygon points="266,70 310,70 310,120 266,86" fill="#1e293b" stroke="#475569" stroke-width="2"/>

  <!-- Reciprocating Scum Skimmer Flight -->
  <g class="animated-skimmer">
    <line x1="80" y1="62" x2="160" y2="62" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="120" y="58" width="12" height="24" rx="2" fill="#e2e8f0"/>
  </g>

  <!-- Micro-Bubble Sparger Header at Bottom -->
  <line x1="80" y1="190" x2="220" y2="190" stroke="#38bdf8" stroke-width="4"/>

  <!-- Dense Micro-Bubble Cloud (Dissolved Air) -->
  <g class="animated-microbubbles">
    <circle cx="100" cy="180" r="2" fill="#e0f2fe"/>
    <circle cx="115" cy="165" r="2.5" fill="#bae6fd"/>
    <circle cx="130" cy="180" r="1.5" fill="#e0f2fe"/>
    <circle cx="145" cy="160" r="2" fill="#bae6fd"/>
    <circle cx="160" cy="175" r="2.5" fill="#e0f2fe"/>
    <circle cx="175" cy="165" r="1.5" fill="#bae6fd"/>
    <circle cx="190" cy="180" r="2" fill="#e0f2fe"/>
    <circle cx="205" cy="160" r="2.5" fill="#bae6fd"/>
  </g>
</svg>
"""

# 11. SCADA UV Light Reactor Animated (Pulsing Violet Germicidal Radiation Wave)
SVG_SCADA_UV = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 344 208" width="344" height="208">
  <defs>
    <style>
      @keyframes uv-glow {
        0%, 100% { opacity: 0.45; }
        50% { opacity: 1; }
      }
      @keyframes uv-wave-move {
        0% { transform: translateX(-15px); }
        50% { transform: translateX(15px); }
        100% { transform: translateX(-15px); }
      }
      .animated-uv-core {
        animation: uv-glow 1.5s ease-in-out infinite;
      }
      .animated-uv-waves {
        animation: uv-wave-move 2.2s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_uv_tube" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="50%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
  </defs>

  <!-- Reactor Cylinder Chamber -->
  <rect x="52" y="64" width="240" height="80" rx="8" fill="url(#an_uv_tube)" stroke="#64748b" stroke-width="3"/>
  <!-- Sight Glass Quartz Window -->
  <rect x="80" y="78" width="184" height="52" rx="6" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>

  <!-- Quartz Lamp Sleeve Core Glow -->
  <rect x="90" y="99" width="164" height="10" rx="5" fill="#c084fc" class="animated-uv-core"/>

  <!-- Germicidal UV Radiation Wave Rays -->
  <g class="animated-uv-waves">
    <path d="M 94 90 Q 110 82 126 90 T 158 90 T 190 90 T 222 90 T 250 90" fill="none" stroke="#d8b4fe" stroke-width="2.5" opacity="0.8"/>
    <path d="M 94 118 Q 110 126 126 118 T 158 118 T 190 118 T 222 118 T 250 118" fill="none" stroke="#d8b4fe" stroke-width="2.5" opacity="0.8"/>
  </g>

  <!-- In/Out Flanges -->
  <rect x="36" y="80" width="16" height="48" rx="2" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="292" y="80" width="16" height="48" rx="2" fill="#334155" stroke="#475569" stroke-width="2"/>
</svg>
"""

# 12. SCADA Analog Pressure Gauge Animated (Subtle Throbbing Pointer Oscillation)
SVG_SCADA_GAUGE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 304 192" width="304" height="192">
  <defs>
    <style>
      @keyframes needle-oscillate {
        0%, 100% { transform: rotate(-35deg); }
        50% { transform: rotate(-25deg); }
      }
      .animated-needle {
        transform-origin: 152px 100px;
        animation: needle-oscillate 1.6s ease-in-out infinite;
      }
    </style>
    <linearGradient id="an_pg_bezel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="50%" stop-color="#334155" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
  </defs>

  <!-- Mounting Stem Pipe -->
  <rect x="144" y="145" width="16" height="35" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="138" y="175" width="28" height="10" rx="2" fill="#334155"/>

  <!-- Circular Bezel -->
  <circle cx="152" cy="95" r="60" fill="url(#an_pg_bezel)" stroke="#94a3b8" stroke-width="3"/>
  <!-- Dial Face -->
  <circle cx="152" cy="95" r="50" fill="#0f172a" stroke="#475569" stroke-width="2"/>

  <!-- Dial Scale Arc -->
  <path d="M 115 115 A 42 42 0 1 1 189 115" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <!-- Green Safe Zone Arc -->
  <path d="M 130 65 A 42 42 0 0 1 174 65" fill="none" stroke="#10b981" stroke-width="4"/>

  <!-- Tick Marks -->
  <line x1="118" y1="112" x2="124" y2="108" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="112" y1="95" x2="119" y2="95" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="122" y1="74" x2="128" y2="79" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="152" y1="56" x2="152" y2="64" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="182" y1="74" x2="176" y2="79" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="192" y1="95" x2="185" y2="95" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="186" y1="112" x2="180" y2="108" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Throbbing Pressure Needle -->
  <g class="animated-needle">
    <line x1="152" y1="95" x2="152" y2="62" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
    <circle cx="152" cy="95" r="7" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
  </g>
</svg>
"""

# 13. Solenoid Valve Animated (Active Green Pulse & Flowing Arrows)
SVG_SOLENOID_VALVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <style>
      @keyframes valve-flow {
        0% { transform: translateX(0); opacity: 0.2; }
        50% { opacity: 1; }
        100% { transform: translateX(30px); opacity: 0.2; }
      }
      @keyframes status-pulse {
        0%, 100% { stroke-opacity: 0.6; stroke-width: 3px; }
        50% { stroke-opacity: 1; stroke-width: 5px; }
      }
      .animated-arrow-stream {
        animation: valve-flow 1.4s linear infinite;
      }
      .animated-status-ring {
        animation: status-pulse 2s ease-in-out infinite;
      }
    </style>
  </defs>

  <!-- Valve Body (Hourglass Flow Path) -->
  <polygon points="50,90 120,120 50,150" fill="#334155" stroke="#64748b" stroke-width="3"/>
  <polygon points="190,90 120,120 190,150" fill="#334155" stroke="#64748b" stroke-width="3"/>

  <!-- Valve Center Hub -->
  <circle cx="120" cy="120" r="32" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <!-- Status Ring (Active Green Pulse) -->
  <circle cx="120" cy="120" r="24" fill="#0f172a" stroke="#10b981" class="animated-status-ring"/>
  <circle cx="120" cy="120" r="10" fill="#10b981"/>

  <!-- Solenoid Coil Actuator Top -->
  <rect x="105" y="45" width="30" height="45" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="120" y1="90" x2="120" y2="105" stroke="#cbd5e1" stroke-width="4"/>

  <!-- Moving Fluid Arrows -->
  <g class="animated-arrow-stream">
    <polygon points="85,120 75,115 75,125" fill="#38bdf8"/>
    <polygon points="155,120 145,115 145,125" fill="#38bdf8"/>
  </g>
</svg>
"""

# 14. RO Membrane Skid Animated (Horizontal Vessel Fluid Flow Streams)
SVG_RO_SKID = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 280" width="350" height="280">
  <defs>
    <style>
      @keyframes ro-stream {
        0% { transform: translateX(0); opacity: 0.2; }
        50% { opacity: 0.9; }
        100% { transform: translateX(50px); opacity: 0.2; }
      }
      .animated-ro-flow {
        animation: ro-stream 1.5s linear infinite;
      }
    </style>
    <linearGradient id="an_ro_skid_vessel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="35%" stop-color="#94a3b8" />
      <stop offset="70%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
  </defs>

  <!-- Structural Skid Rack Frame -->
  <rect x="30" y="235" width="290" height="14" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="60" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>
  <rect x="278" y="50" width="12" height="185" fill="#334155" stroke="#475569" stroke-width="2"/>

  <!-- 3x Horizontal FRP Membrane Pressure Vessels -->
  <!-- Vessel 1 -->
  <rect x="75" y="65" width="200" height="36" rx="18" fill="url(#an_ro_skid_vessel)" stroke="#64748b" stroke-width="2"/>
  <!-- Vessel 2 -->
  <rect x="75" y="115" width="200" height="36" rx="18" fill="url(#an_ro_skid_vessel)" stroke="#64748b" stroke-width="2"/>
  <!-- Vessel 3 -->
  <rect x="75" y="165" width="200" height="36" rx="18" fill="url(#an_ro_skid_vessel)" stroke="#64748b" stroke-width="2"/>

  <!-- Sight Window Flow Lines -->
  <rect x="110" y="77" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="127" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <rect x="110" y="177" width="130" height="12" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>

  <!-- Moving Fluid Pulses Inside Vessels -->
  <g class="animated-ro-flow">
    <circle cx="130" cy="83" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="83" r="3.5" fill="#38bdf8"/>
    <circle cx="210" cy="83" r="3" fill="#e0f2fe"/>
    <circle cx="130" cy="133" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="133" r="3.5" fill="#38bdf8"/>
    <circle cx="210" cy="133" r="3" fill="#e0f2fe"/>
    <circle cx="130" cy="183" r="3" fill="#00e5ff"/>
    <circle cx="170" cy="183" r="3.5" fill="#38bdf8"/>
    <circle cx="210" cy="183" r="3" fill="#e0f2fe"/>
  </g>

  <!-- Feed Manifold (Left Header) -->
  <line x1="66" y1="83" x2="66" y2="183" stroke="#0284c7" stroke-width="6"/>
  <!-- Permeate Manifold (Right Header) -->
  <line x1="284" y1="83" x2="284" y2="183" stroke="#10b981" stroke-width="6"/>
</svg>
"""

# 15. Ultrafiltration (UF) Skid Animated (Vertical Hollow Fiber Filtration Streams)
SVG_UF_SKID = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 328 344" width="328" height="344">
  <defs>
    <style>
      @keyframes uf-flow {
        0% { transform: translateY(0); opacity: 0.2; }
        50% { opacity: 0.95; }
        100% { transform: translateY(40px); opacity: 0.2; }
      }
      .animated-uf-stream {
        animation: uf-flow 1.4s linear infinite;
      }
    </style>
    <linearGradient id="an_uf_module" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="40%" stop-color="#64748b" />
      <stop offset="80%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
  </defs>

  <!-- Base Skid -->
  <rect x="30" y="300" width="268" height="16" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>

  <!-- Upper Header Manifold -->
  <rect x="40" y="50" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
  <!-- Lower Header Manifold -->
  <rect x="40" y="275" width="248" height="18" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>

  <!-- 4x Vertical Hollow Fiber Membrane Modules -->
  <rect x="58" y="75" width="38" height="190" rx="6" fill="url(#an_uf_module)" stroke="#64748b" stroke-width="2"/>
  <rect x="116" y="75" width="38" height="190" rx="6" fill="url(#an_uf_module)" stroke="#64748b" stroke-width="2"/>
  <rect x="174" y="75" width="38" height="190" rx="6" fill="url(#an_uf_module)" stroke="#64748b" stroke-width="2"/>
  <rect x="232" y="75" width="38" height="190" rx="6" fill="url(#an_uf_module)" stroke="#64748b" stroke-width="2"/>

  <!-- Sight Glass with Downward Filtration Streams -->
  <g class="animated-uf-stream">
    <line x1="77" y1="120" x2="77" y2="145" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="135" y1="140" x2="135" y2="165" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
    <line x1="193" y1="125" x2="193" y2="150" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
    <line x1="251" y1="145" x2="251" y2="170" stroke="#00e5ff" stroke-width="3" stroke-linecap="round"/>
  </g>
</svg>
"""

ASSETS = {
    "pump-centrifugal-animated.svg": SVG_PUMP_CENTRIFUGAL,
    "scada-blower-animated.svg": SVG_BLOWER,
    "pump-ro-high-pressure-animated.svg": SVG_PUMP_RO,
    "pump-chemical-dosing-animated.svg": SVG_PUMP_DOSING,
    "hvac-cooling-tower-animated.svg": SVG_COOLING_TOWER,
    "stp-mbbr-aeration-tank-animated.svg": SVG_STP_MBBR,
    "stp-secondary-clarifier-animated.svg": SVG_STP_CLARIFIER,
    "etp-flash-mixer-tank-animated.svg": SVG_ETP_FLASH_MIXER,
    "etp-flocculator-tank-animated.svg": SVG_ETP_FLOCCULATOR,
    "etp-daf-flotation-tank-animated.svg": SVG_ETP_DAF,
    "scada-uv-light-animated.svg": SVG_SCADA_UV,
    "scada-pressure-gauge-animated.svg": SVG_SCADA_GAUGE,
    "scada-water-solenoid-valve-animated.svg": SVG_SOLENOID_VALVE,
    "ro-membrane-skid-animated.svg": SVG_RO_SKID,
    "uf-ultrafiltration-skid-animated.svg": SVG_UF_SKID,
}

print(f"Generating {len(ASSETS)} standalone animated SVG files into {OUT_DIR}...")
for fname, content in ASSETS.items():
    # Verify no <text> tags
    if "<text" in content.lower():
        raise ValueError(f"Error: <text> tag found in {fname}")
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"  + Wrote {fname}")

print("All animated SVGs generated successfully!")
