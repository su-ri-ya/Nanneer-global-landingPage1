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

// Extract the main container or inner body content from schematic.html
let bodyContent = '';
const mainMatch = rawHtml.match(/<main[\s\S]*?<\/main>/i);
if (mainMatch) {
  bodyContent = mainMatch[0];
} else {
  const bodyMatch = rawHtml.match(/<body[\s\S]*?>([\s\S]*?)<\/body>/i);
  bodyContent = bodyMatch ? bodyMatch[1] : rawHtml;
}

// Replace relative image URLs with base64 data URLs
if (prestigeBase64) {
  bodyContent = bodyContent.replace(/src=["']\/images\/prestige-group-logo\.png["']/g, `src="${prestigeBase64}"`);
  bodyContent = bodyContent.replace(/["']\/images\/prestige-group-logo\.png["']/g, `"${prestigeBase64}"`);
}
if (ppmsBase64) {
  bodyContent = bodyContent.replace(/src=["']\/images\/ppms-logo\.jpg["']/g, `src="${ppmsBase64}"`);
  bodyContent = bodyContent.replace(/["']\/images\/ppms-logo\.jpg["']/g, `"${ppmsBase64}"`);
}

// Strip Next.js scripts and unneeded metadata
bodyContent = bodyContent.replace(/<script[\s\S]*?<\/script>/gi, '');

const finalDocument = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Prestige Tranquility STP - 950 KLD SCADA Process Schematic (Client Presentation Document)</title>
  <style>
    /* Inlined Tailwind & App Styles */
    ${rawCss}
    
    /* Presentation Document Bar */
    #doc-top-bar {
      background: linear-gradient(135deg, #091322 0%, #0f172a 100%);
      border-bottom: 1px solid rgba(56, 189, 248, 0.25);
      padding: 10px 20px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      color: #e2e8f0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      position: sticky;
      top: 0;
      z-index: 99999;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    .doc-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(14, 165, 233, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: #38bdf8;
      text-transform: uppercase;
    }
    .doc-pulse {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #22c55e;
      box-shadow: 0 0 8px #22c55e;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.2); }
    }
    .doc-btn {
      background: #1e293b;
      color: #f1f5f9;
      border: 1px solid #475569;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .doc-btn:hover {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    .doc-btn-primary {
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      border-color: #38bdf8;
      color: #fff;
    }
    .doc-btn-primary:hover {
      background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
    }
    
    @media print {
      #doc-top-bar { display: none !important; }
      body { background: #030712 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }
  </style>
</head>
<body class="bg-gray-950 text-slate-100 antialiased min-h-screen">
  <!-- Document Presentation Bar -->
  <div id="doc-top-bar">
    <div style="display: flex; align-items: center; gap: 12px;">
      <span class="doc-pill"><span class="doc-pulse"></span> Offline Client Presentation Document</span>
      <span style="font-weight: 700; font-size: 13px; color: #f8fafc; letter-spacing: -0.01em;">
        PRESTIGE TRANQUILITY &bull; 950 KLD STP LIVE SCADA SCHEMATIC
      </span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
      <button class="doc-btn" onclick="togglePlayPause()" id="playPauseBtn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
        Pause Animations
      </button>
      <button class="doc-btn" onclick="window.print()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print / PDF
      </button>
      <button class="doc-btn doc-btn-primary" onclick="toggleFullscreen()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
        Fullscreen Mode
      </button>
    </div>
  </div>

  <!-- Main Schematic Application -->
  <main class="min-h-screen bg-gray-950 p-2 sm:p-4 text-white">
    ${bodyContent}
  </main>

  <!-- Interactive Document Controller -->
  <script>
    // Fullscreen Toggle
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          alert('Error attempting to enable fullscreen: ' + err.message);
        });
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    // SVG SMIL Animation Play/Pause
    let isPaused = false;
    function togglePlayPause() {
      const svg = document.querySelector('svg');
      const btn = document.getElementById('playPauseBtn');
      if (!svg) return;

      if (!isPaused) {
        if (svg.pauseAnimations) svg.pauseAnimations();
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Resume Animations';
        isPaused = true;
      } else {
        if (svg.unpauseAnimations) svg.unpauseAnimations();
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg> Pause Animations';
        isPaused = false;
      }
    }

    // Live Clock Updater
    setInterval(() => {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
      const clockElems = document.querySelectorAll('.font-mono');
      clockElems.forEach(el => {
        if (el.textContent && el.textContent.includes(':') && el.textContent.length <= 11 && !el.textContent.includes('KLD') && !el.textContent.includes('m³')) {
          el.textContent = timeStr;
        }
      });
    }, 1000);
  </script>
</body>
</html>`;

const outPath1 = path.join(rootDir, 'public', 'STP_SCADA_Process_Schematic_Client_Presentation.html');
const outPath2 = path.join(rootDir, 'STP_SCADA_Process_Schematic_Client_Presentation.html');

fs.writeFileSync(outPath1, finalDocument, 'utf8');
fs.writeFileSync(outPath2, finalDocument, 'utf8');

console.log('SUCCESS: Generated standalone client presentation documents:');
console.log('1. ' + outPath1);
console.log('2. ' + outPath2);
console.log('Document size: ' + Math.round(finalDocument.length / 1024) + ' KB');
