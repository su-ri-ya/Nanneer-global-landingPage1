import base64
import os

ARTIFACT_DIR = 'C:/Users/suriya/.gemini/antigravity/brain/f2730100-5ab7-41de-99c3-0177792ddc03'

with open(os.path.join(ARTIFACT_DIR, '.user_uploaded/media_1794993503398_b503c34b.png'), 'rb') as f:
    b64_img = base64.b64encode(f.read()).decode('utf-8')

with open(os.path.join(ARTIFACT_DIR, 'scratch/test_ref_style.svg'), 'r') as f:
    svg_straight = f.read()
with open(os.path.join(ARTIFACT_DIR, 'scratch/test_ref_elbow.svg'), 'r') as f:
    svg_elbow = f.read()
with open(os.path.join(ARTIFACT_DIR, 'scratch/test_ref_tee.svg'), 'r') as f:
    svg_tee = f.read()

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 p-4 font-sans antialiased">
  <div class="max-w-4xl mx-auto space-y-4">
    <div class="border-b border-slate-800 pb-3">
      <h1 class="text-base font-bold text-white tracking-wide">3D Metallic Pipe Style vs. Your Reference Image</h1>
      <p class="text-xs text-slate-400">Comparing your uploaded reference pipe tiles with our newly styled 3D metallic vector SVGs</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-slate-900/80 rounded-xl border border-slate-800 p-3 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-amber-400">Your Uploaded Reference Photo</span>
          <span class="text-[11px] text-slate-400 font-mono">Original Reference</span>
        </div>
        <div class="bg-white rounded-lg p-2 flex items-center justify-center">
          <img src="data:image/png;base64,{b64_img}" alt="Reference Pipes" class="max-h-60 object-contain rounded" />
        </div>
        <ul class="text-[11px] text-slate-400 list-disc list-inside space-y-1">
          <li>3D cylindrical metallic steel gradient with upper specular highlight sheen</li>
          <li>Raised bolted flange collars at all pipe ends with inner dark rim</li>
          <li>Welded pipe joint seams and 45° mitered elbow corner welds</li>
          <li>Reinforced saddle collars on T-junction intersections</li>
        </ul>
      </div>

      <div class="bg-slate-900/80 rounded-xl border border-emerald-500/40 p-3 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-emerald-400">Our New 3D Vector SVG Match</span>
          <span class="text-[11px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Vector SVGs</span>
        </div>
        
        <div class="grid grid-cols-3 gap-2 bg-slate-900 rounded-lg p-2 border border-slate-800">
          <div class="bg-slate-950 rounded p-1 flex flex-col items-center">
            <span class="text-[10px] text-slate-400 mb-1">Straight</span>
            <div class="w-20 h-20">{svg_straight}</div>
          </div>
          <div class="bg-slate-950 rounded p-1 flex flex-col items-center">
            <span class="text-[10px] text-slate-400 mb-1">90° Miter Elbow</span>
            <div class="w-20 h-20">{svg_elbow}</div>
          </div>
          <div class="bg-slate-950 rounded p-1 flex flex-col items-center">
            <span class="text-[10px] text-slate-400 mb-1">Saddle Tee</span>
            <div class="w-20 h-20">{svg_tee}</div>
          </div>
        </div>

        <ul class="text-[11px] text-emerald-400/90 list-disc list-inside space-y-1">
          <li>100% scalable vector SVGs with exact metallic cylindrical gradient</li>
          <li>Heavy raised flange collars with bolted lip bevels & inner rims</li>
          <li>45° miter weld seams on corners + saddle weld sleeves on tees</li>
          <li>Integrated fluid cores (Blue, Brown, Green) with animated flow or dry</li>
        </ul>
      </div>
    </div>
  </div>
</body>
</html>"""

with open(os.path.join(ARTIFACT_DIR, 'pipe_reference_style_comparison.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated pipe_reference_style_comparison.html successfully!')
