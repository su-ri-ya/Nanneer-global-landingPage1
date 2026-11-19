import os
import glob
import zipfile

pumps_dir = os.path.join("public", "schematic-assets", "pumps")
files = glob.glob(os.path.join(pumps_dir, "*.svg"))

bs = """    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0b2545" flood-opacity="0.28" />
    </filter>"""

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if 'id="bottomShadow"' not in c:
        if '<defs>' in c:
            c = c.replace('<defs>', '<defs>\n' + bs)
        else:
            idx = c.find('>')
            c = c[:idx+1] + '\n  <defs>\n' + bs + '\n  </defs>' + c[idx+1:]
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c)

print(f"Updated all pumps with bottomShadow")

zip_path = "public/schematic-assets.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk("public/schematic-assets"):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, "public")
            zf.write(full_path, rel_path)
print("Zip updated.")
