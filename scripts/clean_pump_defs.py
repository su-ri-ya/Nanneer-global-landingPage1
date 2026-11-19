import os

pumps_dir = os.path.join("public", "schematic-assets", "pumps")
cleaned_files = 0

for f in sorted(os.listdir(pumps_dir)):
    fpath = os.path.join(pumps_dir, f)
    with open(fpath, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # Check if ssPipe defs exist
    if "ssPipeShadow" in c or "ssPipeGradH" in c:
        # Clean out ssPipeShadow filter
        c = c.replace("""    <filter id="ssPipeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>""", "")
        c = c.replace("""    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.25" />
    </filter>""", "")
        # Clean out ssPipe gradients
        c = c.replace("""    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>""", "")
        c = c.replace("""    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>""", "")
        c = c.replace("""    <linearGradient id="ssPipeGradDiag" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>""", "")
        
        # Clean unused styles in RO pump flow-right-to-left
        if "anim-v-dash" in c:
            c = c.replace("""    <style>
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
    </style>""", "<style>@keyframes ro-flow { 0% { transform: translateY(0); opacity: 0.2; } 50% { opacity: 0.95; } 100% { transform: translateY(-40px); opacity: 0.2; } } .anim-ro-stream { animation: ro-flow 1.5s linear infinite; }</style>")

        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(c)
        cleaned_files += 1

print(f"Cleaned unused defs from {cleaned_files} pump SVGs.")
