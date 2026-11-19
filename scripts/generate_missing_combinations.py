import os
import re

BASE_DIR = 'public/schematic-assets'
VALVES_DIR = os.path.join(BASE_DIR, 'valves')
INST_DIR = os.path.join(BASE_DIR, 'instruments-utilities')
PUMPS_DIR = os.path.join(BASE_DIR, 'pumps')

DEFS_BLOCK = """  <defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <style>
      @keyframes v-stream { from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; } }
      @keyframes v-stream-rev { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; } }
      @keyframes alert-pulse { 0%, 100% { stroke-opacity: 0.3; stroke-width: 3px; } 50% { stroke-opacity: 1; stroke-width: 6px; } }
      @keyframes fit-glow { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
      @keyframes pg-pulse { 0%, 100% { transform: rotate(-15deg); } 50% { transform: rotate(15deg); } }
      .anim-v-dash { stroke-dasharray: 5 7; animation: v-stream 0.8s linear infinite; }
      .anim-v-dash-rev { stroke-dasharray: 5 7; animation: v-stream-rev 0.8s linear infinite; }
      .anim-fault { animation: alert-pulse 0.9s ease-in-out infinite; }
      .anim-fit { animation: fit-glow 1.5s ease-in-out infinite; }
      .anim-needle { transform-origin: 100px 75px; animation: pg-pulse 2s ease-in-out infinite; }
    </style>
  </defs>"""

def generate_vertical_valves():
    print("Generating Vertical Valves...")
    
    # 1. Solenoid Valve Vertical Active Animated
    sol_v_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <!-- Through Vertical Pipe -->
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 100 0 L 100 200" stroke="#0284c7" stroke-width="4" fill="none"/>
  <path d="M 100 0 L 100 200" stroke="#bae6fd" stroke-width="2.5" fill="none" class="anim-v-dash"/>
  <polygon points="97,108 100,116 103,108" fill="#0284c7"/>
  <!-- Solenoid Body (Vertical Orientation) -->
  <polygon points="82,60 100,100 118,60" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="82,140 100,100 118,140" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <!-- Side Actuator Coil -->
  <rect x="122" y="88" width="34" height="24" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="100" x2="122" y2="100" stroke="#cbd5e1" stroke-width="3"/>
  <!-- Sanitary Collars -->
  <rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'solenoid-valve-vertical-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(sol_v_anim.strip() + '\n')

    # 2. Solenoid Valve Vertical Active Static
    sol_v_static = sol_v_anim.replace('class="anim-v-dash"', '')
    with open(os.path.join(VALVES_DIR, 'solenoid-valve-vertical-active-static.svg'), 'w', encoding='utf-8') as f:
        f.write(sol_v_static.strip() + '\n')

    # 3. Solenoid Valve Vertical Closed Static
    sol_v_closed = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <!-- Through Vertical Pipe (Dry / Isolated) -->
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <!-- Solenoid Body (Closed / Red Indicator) -->
  <polygon points="82,60 100,100 118,60" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="82,140 100,100 118,140" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#ef4444" stroke-width="2"/>
  <!-- Side Actuator Coil -->
  <rect x="122" y="88" width="34" height="24" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="100" x2="122" y2="100" stroke="#cbd5e1" stroke-width="3"/>
  <!-- Sanitary Collars -->
  <rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'solenoid-valve-vertical-closed-static.svg'), 'w', encoding='utf-8') as f:
        f.write(sol_v_closed.strip() + '\n')

    # 4. Manual Isolation Valve Vertical Open Static
    man_v_open = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 100 0 L 100 200" stroke="#0284c7" stroke-width="4" fill="none"/>
  <!-- Valve Body -->
  <polygon points="84,70 100,100 116,70" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="84,130 100,100 116,130" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <!-- Lever Handle (In-line / Open) -->
  <line x1="100" y1="100" x2="145" y2="100" stroke="#10b981" stroke-width="4" stroke-linecap="round"/>
  <circle cx="145" cy="100" r="4.5" fill="#10b981"/>
  <!-- Sanitary Collars -->
  <rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'manual-isolation-valve-vertical-open-static.svg'), 'w', encoding='utf-8') as f:
        f.write(man_v_open.strip() + '\n')

    # 5. Manual Isolation Valve Vertical Closed Static
    man_v_closed = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <!-- Valve Body -->
  <polygon points="84,70 100,100 116,70" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="84,130 100,100 116,130" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
  <!-- Lever Handle (Perpendicular / Closed) -->
  <line x1="100" y1="100" x2="100" y2="55" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
  <circle cx="100" cy="55" r="4.5" fill="#ef4444"/>
  <!-- Sanitary Collars -->
  <rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'manual-isolation-valve-vertical-closed-static.svg'), 'w', encoding='utf-8') as f:
        f.write(man_v_closed.strip() + '\n')

def generate_directional_nrv():
    print("Generating Directional NRV Check Valves & Multiport Modes...")
    
    # 1. NRV Horizontal Flow Right to Left (Animated & Static)
    nrv_r2l_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <path d="M 200 100 L 0 100" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 200 100 L 0 100" stroke="#0284c7" stroke-width="4" fill="none"/>
  <path d="M 200 100 L 0 100" stroke="#bae6fd" stroke-width="2.5" fill="none" class="anim-v-dash-rev"/>
  <polygon points="92,97 84,100 92,103" fill="#0284c7"/>
  <!-- Valve Body -->
  <rect x="65" y="75" width="70" height="50" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="20" fill="#0f172a" stroke="#0284c7" stroke-width="2"/>
  <!-- Flapper swinging open to Left for Right-to-Left flow -->
  <line x1="110" y1="85" x2="88" y2="105" stroke="#10b981" stroke-width="3" stroke-linecap="round"/>
  <circle cx="110" cy="85" r="3" fill="#10b981"/>
  <!-- Flanges -->
  <rect x="0" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="196" y="94.5" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'check-valve-nrv-horizontal-flow-right-to-left-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(nrv_r2l_anim.strip() + '\n')
    
    nrv_r2l_static = nrv_r2l_anim.replace('class="anim-v-dash-rev"', '')
    with open(os.path.join(VALVES_DIR, 'check-valve-nrv-horizontal-flow-right-to-left-static.svg'), 'w', encoding='utf-8') as f:
        f.write(nrv_r2l_static.strip() + '\n')

    # 2. NRV Vertical Flow Top to Bottom (Animated & Static)
    nrv_v_t2b_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 100 0 L 100 200" stroke="#0284c7" stroke-width="4" fill="none"/>
  <path d="M 100 0 L 100 200" stroke="#bae6fd" stroke-width="2.5" fill="none" class="anim-v-dash"/>
  <polygon points="97,108 100,116 103,108" fill="#0284c7"/>
  <!-- Valve Body -->
  <rect x="75" y="65" width="50" height="70" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="20" fill="#0f172a" stroke="#0284c7" stroke-width="2"/>
  <!-- Flapper swinging open downward -->
  <line x1="85" y1="90" x2="105" y2="112" stroke="#10b981" stroke-width="3" stroke-linecap="round"/>
  <circle cx="85" cy="90" r="3" fill="#10b981"/>
  <!-- Collars -->
  <rect x="94.5" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="94.5" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'check-valve-nrv-vertical-flow-top-to-bottom-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(nrv_v_t2b_anim.strip() + '\n')

    nrv_v_t2b_static = nrv_v_t2b_anim.replace('class="anim-v-dash"', '')
    with open(os.path.join(VALVES_DIR, 'check-valve-nrv-vertical-flow-top-to-bottom-static.svg'), 'w', encoding='utf-8') as f:
        f.write(nrv_v_t2b_static.strip() + '\n')

    # 3. Multiport Backwash & Rinse Modes
    mp_backwash = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <rect x="40" y="40" width="120" height="120" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="100" cy="100" r="42" fill="#0f172a" stroke="#d97706" stroke-width="3"/>
  <!-- Backwash Reverse Flow Indicator Arrows -->
  <path d="M 70 100 L 130 100 M 130 100 L 100 130" stroke="#d97706" stroke-width="4" stroke-linecap="round" fill="none"/>
  <circle cx="100" cy="100" r="14" fill="#d97706" class="anim-fit"/>
  <!-- Ports -->
  <rect x="0" y="93" width="40" height="14" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="160" y="93" width="40" height="14" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="0" width="14" height="40" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="160" width="14" height="40" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'multiport-valve-block-backwash-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(mp_backwash.strip() + '\n')

    mp_rinse = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <rect x="40" y="40" width="120" height="120" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="100" cy="100" r="42" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
  <!-- Fast Rinse Downward Drain Indicator -->
  <path d="M 100 70 L 100 130 M 90 120 L 100 130 L 110 120" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" fill="none"/>
  <circle cx="100" cy="100" r="14" fill="#0284c7" class="anim-fit"/>
  <!-- Ports -->
  <rect x="0" y="93" width="40" height="14" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="160" y="93" width="40" height="14" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="0" width="14" height="40" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="160" width="14" height="40" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
</svg>"""
    with open(os.path.join(VALVES_DIR, 'multiport-valve-block-rinse-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(mp_rinse.strip() + '\n')

def generate_vertical_instruments():
    print("Generating Vertical Flow Meters & Side-Mount Pressure Gauges...")

    # 1. Flow Meter Vertical Active Animated & Static
    fit_v_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <!-- Vertical Flanged Spool Tube -->
  <rect x="90" y="30" width="20" height="140" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="82" y="25" width="36" height="6" rx="1.5" fill="#475569"/>
  <rect x="82" y="169" width="36" height="6" rx="1.5" fill="#475569"/>
  <!-- Sensor Head -->
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <!-- Side Transmitter Neck & Display Puck -->
  <rect x="120" y="95" width="22" height="10" fill="#64748b"/>
  <circle cx="152" cy="100" r="18" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <circle cx="152" cy="100" r="12" fill="#10b981" fill-opacity="0.3" class="anim-fit"/>
  <circle cx="152" cy="100" r="4" fill="#10b981"/>
</svg>"""
    with open(os.path.join(INST_DIR, 'flow-meter-vertical-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(fit_v_anim.strip() + '\n')
    
    fit_v_static = fit_v_anim.replace('class="anim-fit"', '')
    with open(os.path.join(INST_DIR, 'flow-meter-vertical-static.svg'), 'w', encoding='utf-8') as f:
        f.write(fit_v_static.strip() + '\n')

    # 2. Side-Mount Pressure Gauges (Left & Right)
    pg_side_left_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <!-- Threaded Process Nipple (Entering from Left pipe) -->
  <rect x="135" y="95" width="35" height="10" fill="#64748b" stroke="#475569" stroke-width="1.5"/>
  <rect x="165" y="90" width="8" height="20" rx="1.5" fill="#334155"/>
  <!-- Gauge Dial Body -->
  <circle cx="90" cy="100" r="42" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <circle cx="90" cy="100" r="36" fill="#1e293b"/>
  <!-- Dial Ticks -->
  <line x1="62" y1="100" x2="68" y2="100" stroke="#94a3b8" stroke-width="2"/>
  <line x1="90" y1="72" x2="90" y2="78" stroke="#94a3b8" stroke-width="2"/>
  <line x1="118" y1="100" x2="112" y2="100" stroke="#94a3b8" stroke-width="2"/>
  <!-- Needle with Pulse Animation -->
  <g class="anim-needle" style="transform-origin: 90px 100px;">
    <line x1="90" y1="100" x2="90" y2="75" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="90" cy="100" r="4.5" fill="#ef4444"/>
  </g>
</svg>"""
    with open(os.path.join(INST_DIR, 'pressure-gauge-side-mount-left-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(pg_side_left_anim.strip() + '\n')
    
    pg_side_left_static = pg_side_left_anim.replace('class="anim-needle"', '')
    with open(os.path.join(INST_DIR, 'pressure-gauge-side-mount-left-static.svg'), 'w', encoding='utf-8') as f:
        f.write(pg_side_left_static.strip() + '\n')

    pg_side_right_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{DEFS_BLOCK}
  <!-- Threaded Process Nipple (Entering from Right pipe) -->
  <rect x="30" y="95" width="35" height="10" fill="#64748b" stroke="#475569" stroke-width="1.5"/>
  <rect x="27" y="90" width="8" height="20" rx="1.5" fill="#334155"/>
  <!-- Gauge Dial Body -->
  <circle cx="110" cy="100" r="42" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <circle cx="110" cy="100" r="36" fill="#1e293b"/>
  <!-- Dial Ticks -->
  <line x1="82" y1="100" x2="88" y2="100" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="72" x2="110" y2="78" stroke="#94a3b8" stroke-width="2"/>
  <line x1="138" y1="100" x2="132" y2="100" stroke="#94a3b8" stroke-width="2"/>
  <!-- Needle with Pulse Animation -->
  <g class="anim-needle" style="transform-origin: 110px 100px;">
    <line x1="110" y1="100" x2="110" y2="75" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="110" cy="100" r="4.5" fill="#ef4444"/>
  </g>
</svg>"""
    with open(os.path.join(INST_DIR, 'pressure-gauge-side-mount-right-active-animated.svg'), 'w', encoding='utf-8') as f:
        f.write(pg_side_right_anim.strip() + '\n')
    
    pg_side_right_static = pg_side_right_anim.replace('class="anim-needle"', '')
    with open(os.path.join(INST_DIR, 'pressure-gauge-side-mount-right-static.svg'), 'w', encoding='utf-8') as f:
        f.write(pg_side_right_static.strip() + '\n')

def generate_bidirectional_ro_pumps():
    print("Generating RO High Pressure Pumps Right-to-Left...")
    
    sizes = ['dn25', 'dn50']
    for sz in sizes:
        base_orig = os.path.join(PUMPS_DIR, f"ro-high-pressure-pump-{sz}-running-animated.svg")
        if not os.path.exists(base_orig):
            continue
        
        # We can construct the 4 states for R2L
        # Running Animated
        r2l_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 424" width="240" height="424">
{DEFS_BLOCK}
  <!-- 3D Grounding Bottom Contact Shadow -->
  <ellipse cx="120.0" cy="389.0" rx="76.8" ry="7.0" fill="#0f172a" opacity="0.35" filter="url(#bottomShadow)" class="ground-shadow"/>
  <rect x="40" y="380" width="160" height="18" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="75" y="310" width="90" height="50" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <!-- Right Suction (x=165) and Left High Pressure Discharge (x=35) -->
  <rect x="165" y="322" width="40" height="26" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
  <rect x="35" y="322" width="40" height="26" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <rect x="85" y="150" width="70" height="160" rx="3" fill="#475569" stroke="#64748b" stroke-width="2"/>
  <rect x="105" y="160" width="30" height="140" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
  <g class="anim-ro-stream" opacity="0.9">
    <circle cx="120" cy="280" r="5" fill="#00e5ff" /><circle cx="120" cy="240" r="6" fill="#38bdf8" />
    <circle cx="120" cy="200" r="5" fill="#67e8f9" /><circle cx="120" cy="160" r="4" fill="#e0f2fe" />
  </g>
  <rect x="75" y="35" width="90" height="90" rx="6" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
</svg>"""
        with open(os.path.join(PUMPS_DIR, f"ro-high-pressure-pump-{sz}-flow-right-to-left-running-animated.svg"), 'w', encoding='utf-8') as f:
            f.write(r2l_anim.strip() + '\n')

        # Running Static
        r2l_static = r2l_anim.replace('class="anim-ro-stream"', '')
        with open(os.path.join(PUMPS_DIR, f"ro-high-pressure-pump-{sz}-flow-right-to-left-running-static.svg"), 'w', encoding='utf-8') as f:
            f.write(r2l_static.strip() + '\n')

        # Stopped Static
        r2l_stopped = re.sub(r'<g class="anim-ro-stream"[\s\S]*?</g>', '', r2l_anim).replace('stroke="#10b981"', 'stroke="#64748b"')
        with open(os.path.join(PUMPS_DIR, f"ro-high-pressure-pump-{sz}-flow-right-to-left-stopped-static.svg"), 'w', encoding='utf-8') as f:
            f.write(r2l_stopped.strip() + '\n')

        # Fault Animated
        r2l_fault = r2l_stopped.replace('stroke="#64748b"', 'stroke="#ef4444" class="anim-fault"')
        with open(os.path.join(PUMPS_DIR, f"ro-high-pressure-pump-{sz}-flow-right-to-left-fault-animated.svg"), 'w', encoding='utf-8') as f:
            f.write(r2l_fault.strip() + '\n')

if __name__ == '__main__':
    generate_vertical_valves()
    generate_directional_nrv()
    generate_vertical_instruments()
    generate_bidirectional_ro_pumps()
    print("All missing combinations successfully generated!")
