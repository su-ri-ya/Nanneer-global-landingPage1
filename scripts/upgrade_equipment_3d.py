import os
import glob
import re
import xml.etree.ElementTree as ET

BASE_DIR = 'public/schematic-assets'

# Common 3D Filters & Highlights matching components/ScadaSchematicSimulation.tsx
SHADOW_DEFS = """    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.28" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.16" />
    </filter>
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.32" />
      <stop offset="12%" stop-color="#ffffff" stop-opacity="0.75" />
      <stop offset="28%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="70%" stop-color="#000000" stop-opacity="0.0" />
      <stop offset="90%" stop-color="#000000" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22" />
    </linearGradient>"""

def upgrade_equipment_3d():
    print("=== UPGRADING EQUIPMENT WITH 3D DEPTH & BOTTOM SHADOWS ===")
    
    # 1. Tanks
    tank_files = glob.glob(os.path.join(BASE_DIR, 'tanks', '*.svg'))
    for fpath in tank_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject SHADOW_DEFS if not present
        if 'id="bottomShadow"' not in content:
            if '<defs>' in content:
                content = content.replace('<defs>', f'<defs>\n{SHADOW_DEFS}')
            else:
                content = re.sub(r'(<svg[^>]*>)', f'\\1\n  <defs>\n{SHADOW_DEFS}\n  </defs>', content)

        # Add bottom shadow grounding ellipse if not present
        # Tanks have viewBox 320 180, tank hull from y=30 to 150, cx=160
        if 'class="ground-shadow"' not in content:
            shadow_tag = '  <!-- 3D Grounding Bottom Contact Shadow -->\n  <ellipse cx="160" cy="154" rx="132" ry="7" fill="#0f172a" opacity="0.35" filter="url(#bottomShadow)" class="ground-shadow"/>\n'
            # Insert right before Tank Outer Hull or first rect
            if '<!-- Tank Outer Hull -->' in content:
                content = content.replace('<!-- Tank Outer Hull -->', f'{shadow_tag}  <!-- Tank Outer Hull -->')
            elif '<rect' in content:
                content = re.sub(r'(<rect)', f'{shadow_tag}  \\1', content, count=1)

        # Add specular sheen overlay on tank hull
        if 'class="sheen-overlay"' not in content:
            sheen_tag = '\n  <!-- 3D Cylindrical Specular Sheen Overlay -->\n  <rect x="30" y="30" width="260" height="120" rx="8" fill="url(#specularSheen)" pointer-events="none" class="sheen-overlay"/>'
            content = content.replace('</svg>', f'{sheen_tag}\n</svg>')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"  + Upgraded {len(tank_files)} Tanks with 3D bottom contact shadows & cylindrical highlights")

if __name__ == '__main__':
    upgrade_equipment_3d()
