import os
import re

BASE_DIR = 'public/schematic-assets'

ALERT_STYLE = """    <style>
      @keyframes alert-pulse { 0%, 100% { stroke-opacity: 0.3; stroke-width: 3px; } 50% { stroke-opacity: 1; stroke-width: 6px; } }
      .anim-fault { animation: alert-pulse 0.9s ease-in-out infinite; }
    </style>"""

FILES = [
    'pumps/chemical-dosing-pump-dn15-fault-animated.svg',
    'pumps/chemical-dosing-pump-dn25-fault-animated.svg',
    'pumps/submersible-sump-pump-dn50-fault-animated.svg',
    'pumps/submersible-sump-pump-dn100-fault-animated.svg',
    'instruments-utilities/aeration-blower-flow-left-to-right-fault-animated.svg',
    'instruments-utilities/aeration-blower-flow-right-to-left-fault-animated.svg'
]

for rel in FILES:
    path = os.path.join(BASE_DIR, rel)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace empty style with alert style
    if '<defs><style></style></defs>' in content:
        content = content.replace('<defs><style></style></defs>', f"<defs>\n{ALERT_STYLE}\n  </defs>")
    elif '<defs>' in content and '</defs>' in content:
        content = re.sub(r'<defs>[\s\S]*?</defs>', f"<defs>\n{ALERT_STYLE}\n  </defs>", content)
    else:
        # inject defs right after <svg ...>
        content = re.sub(r'(<svg[^>]*>)', f"\\1\n  <defs>\n{ALERT_STYLE}\n  </defs>", content)
    
    # 2. Add class="anim-fault" to the red warning stroke
    # E.g. stroke="#ef4444"
    if 'stroke="#ef4444"' in content and 'anim-fault' not in content:
        content = re.sub(r'(stroke="#ef4444"[^/]*?)(\s*/?>)', r'\1 class="anim-fault"\2', content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {rel} with pulsing fault animation")

print("All 6 fault-animated files successfully updated!")
