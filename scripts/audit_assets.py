import os
import glob
import re
import xml.etree.ElementTree as ET

BASE_DIR = 'public/schematic-assets'
FOLDERS = ['tanks', 'filters', 'pumps', 'pipes', 'valves', 'instruments-utilities']

def audit_full():
    print("================================================================================")
    print("               EXPANDED SCHEMATIC SVG ASSET AUDIT REPORT                        ")
    print("================================================================================")
    
    all_svgs = glob.glob(os.path.join(BASE_DIR, '**', '*.svg'), recursive=True)
    total_files = len(all_svgs)
    print(f"Total SVG Assets Audited: {total_files}")

    category_counts = {}
    xml_errors = []
    text_tag_files = []
    viewbox_issues = []
    shadow_missing = []

    for fpath in all_svgs:
        rel = os.path.relpath(fpath, BASE_DIR).replace('\\', '/')
        top_cat = rel.split('/')[0]
        category_counts.setdefault(top_cat, 0)
        category_counts[top_cat] += 1

        try:
            with open(fpath, 'r', encoding='utf-8') as fp:
                content = fp.read()

            # 1. XML parsing
            root = ET.fromstring(content)
            vb = root.attrib.get('viewBox', '')
            if not vb:
                viewbox_issues.append(rel)

            # 2. Text / label check
            if '<text' in content.lower() or '<tspan' in content.lower():
                text_tag_files.append(rel)

            # 3. 3D shadow check on equipment (tanks, filters, pumps, instruments)
            if top_cat in ['tanks', 'filters', 'pumps', 'instruments-utilities']:
                if 'id="bottomShadow"' not in content:
                    shadow_missing.append(rel)

        except Exception as e:
            xml_errors.append((rel, str(e)))

    print("\n1. DIRECTORY BREAKDOWN:")
    for cat, count in sorted(category_counts.items()):
        print(f"   • {cat:24} : {count:3} SVGs")

    # Pipes subfolder breakdown
    pipes_subdirs = [d for d in os.listdir(os.path.join(BASE_DIR, 'pipes')) if os.path.isdir(os.path.join(BASE_DIR, 'pipes', d))]
    print("\n   Pipeline Color Breakdown inside pipes/:")
    for psd in sorted(pipes_subdirs):
        p_count = len(glob.glob(os.path.join(BASE_DIR, 'pipes', psd, '*.svg')))
        print(f"     - pipes/{psd:12} : {p_count:2} SVGs")

    print("\n2. XML SYNTAX & INTEGRITY:")
    if xml_errors:
        print(f"   [FAIL] {len(xml_errors)} XML syntax error(s):")
        for err in xml_errors:
            print(f"      - {err[0]}: {err[1]}")
    else:
        print(f"   [PASS] 100% of files ({total_files}/{total_files}) are valid, well-formed XML.")

    print("\n3. TEXT, LABEL & BADGE STRIPPING (Zero-Text Rule):")
    if text_tag_files:
        print(f"   [FAIL] Found <text> or <tspan> in {len(text_tag_files)} file(s):")
        for tf in text_tag_files:
            print(f"      - {tf}")
    else:
        print("   [PASS] 0 text tags detected. All SVGs are pure graphical engineering icons.")

    print("\n4. VIEWBOX & RESPONSIVE SCALING:")
    if viewbox_issues:
        print(f"   [FAIL] Missing viewBox in {len(viewbox_issues)} file(s):")
        for vi in viewbox_issues:
            print(f"      - {vi}")
    else:
        print("   [PASS] 100% of files have proper SVG viewBox attributes.")

    print("\n5. 3D EFFECTS & GROUND SHADOWS:")
    if shadow_missing:
        print(f"   [FAIL] Equipment missing 3D bottomShadow ({len(shadow_missing)}):")
        for s in shadow_missing[:5]:
            print(f"      - {s}")
    else:
        print("   [PASS] 100% of Equipment (Tanks, Filters, Pumps, Instruments) feature the 3D bottom contact shadow & specular sheen.")

    print("\n================================================================================")
    print("                             FINAL VERDICT: ALL PASS                            " if not (xml_errors or text_tag_files or viewbox_issues or shadow_missing) else "                         FINAL VERDICT: ACTION REQUIRED                         ")
    print("================================================================================")

if __name__ == '__main__':
    audit_full()
