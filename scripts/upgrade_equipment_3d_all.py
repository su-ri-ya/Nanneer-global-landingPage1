import os
import glob
import re

BASE_DIR = 'public/schematic-assets'

SHADOW_DEFS = """    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.32" />
      <stop offset="12%" stop-color="#ffffff" stop-opacity="0.75" />
      <stop offset="28%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="70%" stop-color="#000000" stop-opacity="0.0" />
      <stop offset="90%" stop-color="#000000" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22" />
    </linearGradient>"""

def upgrade_all_equipment_3d():
    print("=== UPGRADING FILTERS, PUMPS, INSTRUMENTS WITH 3D SHADOWS ===")
    
    # 1. Filters (viewBox 276 384 or similar)
    filter_files = glob.glob(os.path.join(BASE_DIR, 'filters', '*.svg'))
    for fpath in filter_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'id="bottomShadow"' not in content:
            if '<defs>' in content:
                content = content.replace('<defs>', f'<defs>\n{SHADOW_DEFS}')
            else:
                content = re.sub(r'(<svg[^>]*>)', f'\\1\n  <defs>\n{SHADOW_DEFS}\n  </defs>', content)
        
        # Add grounding contact shadow
        if 'class="ground-shadow"' not in content:
            shadow_tag = '  <!-- 3D Grounding Bottom Contact Shadow -->\n  <ellipse cx="138" cy="366" rx="96" ry="8" fill="#0f172a" opacity="0.35" filter="url(#bottomShadow)" class="ground-shadow"/>\n'
            content = re.sub(r'(<svg[^>]*>[\s\S]*?</defs>\s*)', f'\\1\n{shadow_tag}', content)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"  + Upgraded {len(filter_files)} Filters")

    # 2. Pumps (viewBox 300 264 or similar)
    pump_files = glob.glob(os.path.join(BASE_DIR, 'pumps', '*.svg'))
    for fpath in pump_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'id="bottomShadow"' not in content:
            if '<defs>' in content:
                content = content.replace('<defs>', f'<defs>\n{SHADOW_DEFS}')
            else:
                content = re.sub(r'(<svg[^>]*>)', f'\\1\n  <defs>\n{SHADOW_DEFS}\n  </defs>', content)
        
        if 'class="ground-shadow"' not in content:
            # Check viewBox to get center cx and cy
            vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
            if vb_match:
                w, h = float(vb_match.group(1)), float(vb_match.group(2))
                cx = w / 2
                cy = h - 35
                rx = w * 0.32
                ry = 7
                shadow_tag = f'  <!-- 3D Grounding Bottom Contact Shadow -->\n  <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#0f172a" opacity="0.35" filter="url(#bottomShadow)" class="ground-shadow"/>\n'
                content = re.sub(r'(<svg[^>]*>[\s\S]*?</defs>\s*)', f'\\1\n{shadow_tag}', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"  + Upgraded {len(pump_files)} Pumps")

    # 3. Instruments & Utilities
    inst_files = glob.glob(os.path.join(BASE_DIR, 'instruments-utilities', '*.svg'))
    for fpath in inst_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'id="bottomShadow"' not in content:
            if '<defs>' in content:
                content = content.replace('<defs>', f'<defs>\n{SHADOW_DEFS}')
            else:
                content = re.sub(r'(<svg[^>]*>)', f'\\1\n  <defs>\n{SHADOW_DEFS}\n  </defs>', content)
        
        if 'class="ground-shadow"' not in content:
            vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
            if vb_match:
                w, h = float(vb_match.group(1)), float(vb_match.group(2))
                cx = w / 2
                cy = h - 25
                rx = w * 0.35
                ry = 7
                shadow_tag = f'  <!-- 3D Grounding Bottom Contact Shadow -->\n  <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#0f172a" opacity="0.32" filter="url(#bottomShadow)" class="ground-shadow"/>\n'
                content = re.sub(r'(<svg[^>]*>[\s\S]*?</defs>\s*)', f'\\1\n{shadow_tag}', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"  + Upgraded {len(inst_files)} Instruments & Utilities")

if __name__ == '__main__':
    upgrade_all_equipment_3d()
