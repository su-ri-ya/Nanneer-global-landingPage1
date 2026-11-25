const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const schematicHtmlPath = path.join(rootDir, '.next', 'server', 'app', 'schematic.html');
const cssPath = path.join(rootDir, '.next', 'static', 'css', '123c800b08904078.css');
const prestigeLogoPath = path.join(rootDir, 'public', 'images', 'prestige-group-logo.png');
const ppmsLogoPath = path.join(rootDir, 'public', 'images', 'ppms-logo.jpg');

console.log('Reading source files...');
const rawHtml = fs.readFileSync(schematicHtmlPath, 'utf8');
const rawCss = fs.existsSync(cssPath) ? fs.readFileSync(cssPath, 'utf8') : '';

// Base64 encode logos
let prestigeBase64 = '';
if (fs.existsSync(prestigeLogoPath)) {
  prestigeBase64 = `data:image/png;base64,${fs.readFileSync(prestigeLogoPath).toString('base64')}`;
}
let ppmsBase64 = '';
if (fs.existsSync(ppmsLogoPath)) {
  ppmsBase64 = `data:image/jpeg;base64,${fs.readFileSync(ppmsLogoPath).toString('base64')}`;
}

// Extract the exact body content before scripts
const bodyStart = rawHtml.indexOf('<body');
const bodyOpenTagEnd = rawHtml.indexOf('>', bodyStart) + 1;
const scriptStart = rawHtml.indexOf('<script', bodyOpenTagEnd);
let bodyInner = rawHtml.substring(bodyOpenTagEnd, scriptStart);

// Replace relative logo URLs with embedded base64 data URLs
if (prestigeBase64) {
  bodyInner = bodyInner.replace(/src=["']\/images\/prestige-group-logo\.png["']/g, `src="${prestigeBase64}"`);
  bodyInner = bodyInner.replace(/["']\/images\/prestige-group-logo\.png["']/g, `"${prestigeBase64}"`);
}
if (ppmsBase64) {
  bodyInner = bodyInner.replace(/src=["']\/images\/ppms-logo\.jpg["']/g, `src="${ppmsBase64}"`);
  bodyInner = bodyInner.replace(/["']\/images\/ppms-logo\.jpg["']/g, `"${ppmsBase64}"`);
}

// Remove any remaining Next.js script tags inside bodyInner if any
bodyInner = bodyInner.replace(/<script[\s\S]*?<\/script>/gi, '');

// Clean "Back to Home" button if present, replace with Fullscreen toggle & title
bodyInner = bodyInner.replace(
  /<a[^>]*href="\/"[^>]*>[\s\S]*?Back to Home<\/span><\/a>/i,
  `<div style="display:flex;align-items:center;gap:10px;">
    <button onclick="toggleFullscreen()" style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,0.15);transition:background 0.2s;">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
      FULLSCREEN
    </button>
    <span style="font-size:11px;font-weight:700;color:#0369a1;background:#e0f2fe;padding:3px 10px;border-radius:9999px;border:1px solid #bae6fd;">
      PRESTIGE TRANQUILITY &bull; 950 KLD SCADA PROCESS DIGITAL TWIN
    </span>
  </div>`
);

const finalHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Prestige Tranquility 950 KLD STP — Real-Time SCADA Digital Twin Poster</title>
  <style>
    ${rawCss}
    
    html, body {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #f8fafc;
      -webkit-font-smoothing: antialiased;
    }
  </style>
</head>
<body class="min-h-screen bg-slate-50 text-slate-900 antialiased selection:bg-teal-500 selection:text-white">
  ${bodyInner}

  <script>
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.log('Fullscreen failed:', err);
        });
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    // Live clock updater
    setInterval(() => {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
      const monoSpans = document.querySelectorAll('.font-mono');
      monoSpans.forEach(el => {
        if (el.textContent && el.textContent.includes(':') && el.textContent.length <= 11 && !el.textContent.includes('KLD') && !el.textContent.includes('m³')) {
          el.textContent = timeStr;
        }
      });
    }, 1000);
  </script>
</body>
</html>`;

const outPath1 = path.join(rootDir, 'Prestige_STP_950KLD_Animated_Poster.html');
const outPath2 = path.join(rootDir, 'public', 'Prestige_STP_950KLD_Animated_Poster.html');

fs.writeFileSync(outPath1, finalHtml, 'utf8');
fs.writeFileSync(outPath2, finalHtml, 'utf8');

console.log('SUCCESS: Generated 100% exact full schematic poster:');
console.log('1.', outPath1);
console.log('2.', outPath2);
console.log('Size:', Math.round(finalHtml.length / 1024), 'KB');
