import os

valves_dir = os.path.join("public", "schematic-assets", "valves")

# 1. Manual Isolation Valves
manual_iso_h_open = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Manual Isolation Valve Horizontal (Open) -->
  <polygon points="40,80 100,100 40,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="160,80 100,100 160,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Open (parallel to horizontal flow) -->
  <line x1="100" y1="100" x2="100" y2="60" stroke="#64748b" stroke-width="4"/>
  <rect x="95" y="45" width="55" height="10" rx="3" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
</svg>'''

manual_iso_h_closed = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Manual Isolation Valve Horizontal (Closed) -->
  <polygon points="40,80 100,100 40,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="160,80 100,100 160,120" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Closed (perpendicular to horizontal flow) -->
  <line x1="100" y1="100" x2="100" y2="60" stroke="#64748b" stroke-width="4"/>
  <rect x="72" y="45" width="55" height="10" rx="3" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5"/>
</svg>'''

manual_iso_v_open = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Manual Isolation Valve Vertical (Open) -->
  <polygon points="80,40 100,100 120,40" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="80,160 100,100 120,160" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Open (parallel to vertical flow) -->
  <line x1="100" y1="100" x2="60" y2="100" stroke="#64748b" stroke-width="4"/>
  <rect x="45" y="95" width="10" height="55" rx="3" fill="#10b981" stroke="#059669" stroke-width="1.5"/>
</svg>'''

manual_iso_v_closed = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Manual Isolation Valve Vertical (Closed) -->
  <polygon points="80,40 100,100 120,40" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <polygon points="80,160 100,100 120,160" fill="#334155" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="16" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <!-- Lever Handle Closed (perpendicular to vertical flow) -->
  <line x1="100" y1="100" x2="60" y2="100" stroke="#64748b" stroke-width="4"/>
  <rect x="45" y="72" width="10" height="55" rx="3" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5"/>
</svg>'''

# 2. Solenoid Valves Horizontal
solenoid_h_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes sol-pulse { 0%, 100% { stroke-opacity: 0.6; stroke-width: 2px; } 50% { stroke-opacity: 1; stroke-width: 3.5px; } }
      .anim-sol-active { animation: sol-pulse 1.4s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Solenoid Valve Horizontal (Active Animated) -->
  <polygon points="55,80 100,100 55,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="145,80 100,100 145,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2.5" class="anim-sol-active"/>
  <circle cx="100" cy="100" r="6" fill="#10b981"/>
  <!-- Solenoid Coil Actuator Top -->
  <rect x="86" y="42" width="28" height="36" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="100" y1="78" x2="100" y2="88" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="92" y="48" width="16" height="5" rx="1" fill="#64748b"/>
  <rect x="92" y="57" width="16" height="5" rx="1" fill="#64748b"/>
</svg>'''

solenoid_h_static_active = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Solenoid Valve Horizontal (Active Static) -->
  <polygon points="55,80 100,100 55,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="145,80 100,100 145,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <circle cx="100" cy="100" r="6" fill="#10b981"/>
  <!-- Solenoid Coil Actuator Top -->
  <rect x="86" y="42" width="28" height="36" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="100" y1="78" x2="100" y2="88" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="92" y="48" width="16" height="5" rx="1" fill="#64748b"/>
  <rect x="92" y="57" width="16" height="5" rx="1" fill="#64748b"/>
</svg>'''

solenoid_h_static_closed = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Solenoid Valve Horizontal (Closed Static) -->
  <polygon points="55,80 100,100 55,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="145,80 100,100 145,120" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#ef4444" stroke-width="2"/>
  <circle cx="100" cy="100" r="6" fill="#ef4444"/>
  <!-- Solenoid Coil Actuator Top -->
  <rect x="86" y="42" width="28" height="36" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="100" y1="78" x2="100" y2="88" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="92" y="48" width="16" height="5" rx="1" fill="#64748b"/>
  <rect x="92" y="57" width="16" height="5" rx="1" fill="#64748b"/>
</svg>'''

# 3. Solenoid Valves Vertical
solenoid_v_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes sol-pulse-v { 0%, 100% { stroke-opacity: 0.6; stroke-width: 2px; } 50% { stroke-opacity: 1; stroke-width: 3.5px; } }
      .anim-sol-active { animation: sol-pulse-v 1.4s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Solenoid Valve Vertical (Active Animated) -->
  <polygon points="80,55 100,100 120,55" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="80,145 100,100 120,145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2.5" class="anim-sol-active"/>
  <circle cx="100" cy="100" r="6" fill="#10b981"/>
  <!-- Side Actuator Coil -->
  <rect x="122" y="86" width="36" height="28" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="100" x2="122" y2="100" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="128" y="92" width="5" height="16" rx="1" fill="#64748b"/>
  <rect x="137" y="92" width="5" height="16" rx="1" fill="#64748b"/>
</svg>'''

solenoid_v_static_active = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Solenoid Valve Vertical (Active Static) -->
  <polygon points="80,55 100,100 120,55" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="80,145 100,100 120,145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <circle cx="100" cy="100" r="6" fill="#10b981"/>
  <!-- Side Actuator Coil -->
  <rect x="122" y="86" width="36" height="28" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="100" x2="122" y2="100" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="128" y="92" width="5" height="16" rx="1" fill="#64748b"/>
  <rect x="137" y="92" width="5" height="16" rx="1" fill="#64748b"/>
</svg>'''

solenoid_v_static_closed = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Solenoid Valve Vertical (Closed Static) -->
  <polygon points="80,55 100,100 120,55" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <polygon points="80,145 100,100 120,145" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <circle cx="100" cy="100" r="22" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="14" fill="#0f172a" stroke="#ef4444" stroke-width="2"/>
  <circle cx="100" cy="100" r="6" fill="#ef4444"/>
  <!-- Side Actuator Coil -->
  <rect x="122" y="86" width="36" height="28" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="100" x2="122" y2="100" stroke="#cbd5e1" stroke-width="3.5"/>
  <rect x="128" y="92" width="5" height="16" rx="1" fill="#64748b"/>
  <rect x="137" y="92" width="5" height="16" rx="1" fill="#64748b"/>
</svg>'''

# 4. Check Valves / Non-Return Valves (NRV)
# Horizontal Flow: Left to Right
check_h_lr_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-disc-pulse { 0%, 100% { stroke-opacity: 0.7; } 50% { stroke-opacity: 1; } }
      .anim-nrv-disc { animation: nrv-disc-pulse 1.2s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Check Valve NRV Horizontal L->R (Active Animated) -->
  <rect x="65" y="75" width="70" height="50" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Open Disc swinging to Right -->
  <line x1="90" y1="82" x2="90" y2="118" stroke="#94a3b8" stroke-width="3"/>
  <line x1="90" y1="84" x2="112" y2="106" stroke="#10b981" stroke-width="3.5" stroke-linecap="round" class="anim-nrv-disc"/>
  <circle cx="90" cy="84" r="3" fill="#10b981"/>
</svg>'''

check_h_lr_static = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Check Valve NRV Horizontal L->R (Static) -->
  <rect x="65" y="75" width="70" height="50" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Closed Disc on Seat -->
  <line x1="90" y1="82" x2="90" y2="118" stroke="#94a3b8" stroke-width="3"/>
  <line x1="90" y1="84" x2="90" y2="116" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="90" cy="84" r="3" fill="#10b981"/>
</svg>'''

# Horizontal Flow: Right to Left
check_h_rl_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-disc-pulse { 0%, 100% { stroke-opacity: 0.7; } 50% { stroke-opacity: 1; } }
      .anim-nrv-disc { animation: nrv-disc-pulse 1.2s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Check Valve NRV Horizontal R->L (Active Animated) -->
  <rect x="65" y="75" width="70" height="50" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Open Disc swinging to Left -->
  <line x1="110" y1="82" x2="110" y2="118" stroke="#94a3b8" stroke-width="3"/>
  <line x1="110" y1="84" x2="88" y2="106" stroke="#10b981" stroke-width="3.5" stroke-linecap="round" class="anim-nrv-disc"/>
  <circle cx="110" cy="84" r="3" fill="#10b981"/>
</svg>'''

check_h_rl_static = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Check Valve NRV Horizontal R->L (Static) -->
  <rect x="65" y="75" width="70" height="50" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Closed Disc on Seat -->
  <line x1="110" y1="82" x2="110" y2="118" stroke="#94a3b8" stroke-width="3"/>
  <line x1="110" y1="84" x2="110" y2="116" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="110" cy="84" r="3" fill="#10b981"/>
</svg>'''

# Vertical Flow: Bottom to Top (Upward flow)
check_v_bt_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-disc-pulse { 0%, 100% { stroke-opacity: 0.7; } 50% { stroke-opacity: 1; } }
      .anim-nrv-disc { animation: nrv-disc-pulse 1.2s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Check Valve NRV Vertical B->T Upward (Active Animated) -->
  <rect x="75" y="65" width="50" height="70" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Open Disc swinging Upward -->
  <line x1="82" y1="110" x2="118" y2="110" stroke="#94a3b8" stroke-width="3"/>
  <line x1="84" y1="110" x2="106" y2="88" stroke="#10b981" stroke-width="3.5" stroke-linecap="round" class="anim-nrv-disc"/>
  <circle cx="84" cy="110" r="3" fill="#10b981"/>
</svg>'''

check_v_bt_static = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Check Valve NRV Vertical B->T Upward (Static) -->
  <rect x="75" y="65" width="50" height="70" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Closed Disc on Seat -->
  <line x1="82" y1="110" x2="118" y2="110" stroke="#94a3b8" stroke-width="3"/>
  <line x1="84" y1="110" x2="116" y2="110" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="84" cy="110" r="3" fill="#10b981"/>
</svg>'''

# Vertical Flow: Top to Bottom (Downward flow)
check_v_tb_anim = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes nrv-disc-pulse { 0%, 100% { stroke-opacity: 0.7; } 50% { stroke-opacity: 1; } }
      .anim-nrv-disc { animation: nrv-disc-pulse 1.2s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Check Valve NRV Vertical T->B Downward (Active Animated) -->
  <rect x="75" y="65" width="50" height="70" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Open Disc swinging Downward -->
  <line x1="82" y1="90" x2="118" y2="90" stroke="#94a3b8" stroke-width="3"/>
  <line x1="84" y1="90" x2="106" y2="112" stroke="#10b981" stroke-width="3.5" stroke-linecap="round" class="anim-nrv-disc"/>
  <circle cx="84" cy="90" r="3" fill="#10b981"/>
</svg>'''

check_v_tb_static = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Check Valve NRV Vertical T->B Downward (Static) -->
  <rect x="75" y="65" width="50" height="70" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="100" cy="100" r="22" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
  <!-- Internal Seat & Closed Disc on Seat -->
  <line x1="82" y1="90" x2="118" y2="90" stroke="#94a3b8" stroke-width="3"/>
  <line x1="84" y1="90" x2="116" y2="90" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="84" cy="90" r="3" fill="#10b981"/>
</svg>'''

# 5. Multiport Valve Blocks
multiport_backwash = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes mp-glow { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
      .anim-mp-glow { animation: mp-glow 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Multiport Valve Block (Backwash Animated) -->
  <rect x="44" y="44" width="112" height="112" rx="10" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="100" cy="100" r="40" fill="#0f172a" stroke="#d97706" stroke-width="3"/>
  <!-- Backwash Routing Flow Arrow -->
  <path d="M 75 100 L 125 100 M 125 100 L 100 125" stroke="#d97706" stroke-width="4" stroke-linecap="round" fill="none"/>
  <circle cx="100" cy="100" r="12" fill="#d97706" class="anim-mp-glow"/>
  <!-- Connection Ports (Housing-bound Nozzles) -->
  <rect x="26" y="93" width="18" height="14" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="156" y="93" width="18" height="14" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="26" width="14" height="18" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="156" width="14" height="18" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
</svg>'''

multiport_rinse = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes mp-glow { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
      .anim-mp-glow { animation: mp-glow 1.5s ease-in-out infinite; }
    </style>
  </defs>
  <!-- Multiport Valve Block (Rinse Animated) -->
  <rect x="44" y="44" width="112" height="112" rx="10" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
  <circle cx="100" cy="100" r="40" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
  <!-- Fast Rinse Routing Flow Arrow -->
  <path d="M 100 75 L 100 125 M 92 117 L 100 125 L 108 117" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" fill="none"/>
  <circle cx="100" cy="100" r="12" fill="#0284c7" class="anim-mp-glow"/>
  <!-- Connection Ports (Housing-bound Nozzles) -->
  <rect x="26" y="93" width="18" height="14" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="156" y="93" width="18" height="14" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="26" width="14" height="18" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <rect x="93" y="156" width="14" height="18" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
</svg>'''

updates = {
    # Manual Isolation
    "manual-isolation-valve-open-static.svg": manual_iso_h_open,
    "manual-isolation-valve-closed-static.svg": manual_iso_h_closed,
    "manual-isolation-valve-vertical-open-static.svg": manual_iso_v_open,
    "manual-isolation-valve-vertical-closed-static.svg": manual_iso_v_closed,
    # Solenoid Horizontal
    "solenoid-valve-active-animated.svg": solenoid_h_anim,
    "solenoid-valve-active-static.svg": solenoid_h_static_active,
    "solenoid-valve-closed-static.svg": solenoid_h_static_closed,
    # Solenoid Vertical
    "solenoid-valve-vertical-active-animated.svg": solenoid_v_anim,
    "solenoid-valve-vertical-active-static.svg": solenoid_v_static_active,
    "solenoid-valve-vertical-closed-static.svg": solenoid_v_static_closed,
    # Check Valve NRV Horizontal
    "check-valve-nrv-horizontal-active-animated.svg": check_h_lr_anim,
    "check-valve-nrv-horizontal-static.svg": check_h_lr_static,
    "check-valve-nrv-horizontal-flow-right-to-left-active-animated.svg": check_h_rl_anim,
    "check-valve-nrv-horizontal-flow-right-to-left-static.svg": check_h_rl_static,
    # Check Valve NRV Vertical
    "check-valve-nrv-vertical-active-animated.svg": check_v_bt_anim,
    "check-valve-nrv-vertical-static.svg": check_v_bt_static,
    "check-valve-nrv-vertical-flow-top-to-bottom-active-animated.svg": check_v_tb_anim,
    "check-valve-nrv-vertical-flow-top-to-bottom-static.svg": check_v_tb_static,
    # Multiport Blocks
    "multiport-valve-block-backwash-animated.svg": multiport_backwash,
    "multiport-valve-block-rinse-animated.svg": multiport_rinse,
}

for fname, content in updates.items():
    fpath = os.path.join(valves_dir, fname)
    with open(fpath, "w", encoding="utf-8") as fp:
        fp.write(content)
    print(f"Updated {fname}: pure valve, 0 embedded pipes.")

print("\nAll target valve SVGs successfully stripped of embedded pipes!")
