const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const rootDir = 'C:\\Nanneer global\\draft 3';
const publicDir = path.join(rootDir, 'public');

async function main() {
  console.log('1. Checking local dev server...');
  let port = 3000;
  let cssText = '';

  try {
    const cssRes = await fetch(`http://localhost:${port}/_next/static/css/app/layout.css`);
    cssText = await cssRes.text();
  } catch (e) {
    port = 3001;
    const cssRes = await fetch(`http://localhost:${port}/_next/static/css/app/layout.css`);
    cssText = await cssRes.text();
  }
  console.log(`Connected to dev server on port ${port}. Fetched ${(cssText.length / 1024).toFixed(1)} KB CSS.`);

  console.log('2. Converting partner logos to Base64 data URLs...');
  const prestigeBase64 = 'data:image/png;base64,' + fs.readFileSync(path.join(publicDir, 'images', 'prestige-group-logo.png')).toString('base64');
  const ppmsBase64 = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(publicDir, 'images', 'ppms-logo.jpg')).toString('base64');

  console.log('3. Dumping rendered SVG DOM from headless Chrome...');
  let html = execSync(`"${chromePath}" --headless=new --virtual-time-budget=4000 --dump-dom http://localhost:${port}/schematic`, {
    encoding: 'utf8',
    maxBuffer: 60 * 1024 * 1024
  });

  console.log('4. Assembling self-contained client presentation document...');

  // 4a. Inline full Tailwind CSS
  html = html.replace(/<link[^>]+rel=["']stylesheet["'][^>]*>/gi, `<style>
${cssText}

/* Presentation Bar Styling */
#client-header-bar {
  background: linear-gradient(135deg, #091322 0%, #0f172a 100%);
  border-bottom: 1px solid rgba(56, 189, 248, 0.3);
  padding: 8px 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #e2e8f0;
  font-family: ui-sans-serif, system-ui, sans-serif;
  position: sticky;
  top: 0;
  z-index: 99999;
  box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.client-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(56, 189, 248, 0.4);
  padding: 3px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #38bdf8;
  text-transform: uppercase;
}
.client-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 6px #22c55e;
}
.client-btn {
  background: #1e293b;
  color: #f1f5f9;
  border: 1px solid #475569;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.client-btn:hover {
  background: #0284c7;
  border-color: #38bdf8;
  color: #fff;
}
.client-btn-primary {
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
  border-color: #38bdf8;
  color: #fff;
}
.client-btn-primary:hover {
  background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}

@page { size: 1400px 900px; margin: 0; }
@media print { 
  #client-header-bar { display: none !important; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>`);

  // 4b. Inline Base64 images
  html = html.replace(/src=["']\/images\/prestige-group-logo\.png["']/g, `src="${prestigeBase64}"`);
  html = html.replace(/["']\/images\/prestige-group-logo\.png["']/g, `"${prestigeBase64}"`);
  html = html.replace(/src=["']\/images\/ppms-logo\.jpg["']/g, `src="${ppmsBase64}"`);
  html = html.replace(/["']\/images\/ppms-logo\.jpg["']/g, `"${ppmsBase64}"`);

  // 4c. Strip Next.js scripts
  html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

  // 4d. Remove "Back to Home" button link container
  html = html.replace(/<div class="w-full mb-1[^"]*shrink-0 flex items-center justify-between">[\s\S]*?<\/div>/, '');

  // 4e. Remove next-route-announcer
  html = html.replace(/<next-route-announcer>[\s\S]*?<\/next-route-announcer>/g, '');

  // 4f. Update title
  html = html.replace(/<title>[\s\S]*?<\/title>/, '<title>Prestige Tranquility 950 KLD STP — Process Schematic Client Document</title>');

  // 4g. Insert Presentation Top Bar right inside <body>
  const topBarHtml = `
  <div id="client-header-bar">
    <div style="display: flex; align-items: center; gap: 10px;">
      <span class="client-pill"><span class="client-dot"></span> CLIENT DOCUMENT</span>
      <span style="font-weight: 700; font-size: 13px; color: #f8fafc; letter-spacing: -0.01em;">
        PRESTIGE TRANQUILITY &bull; 950 KLD STP PROCESS SCHEMATIC &amp; SCADA SIMULATION
      </span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
      <button class="client-btn" onclick="togglePlayPause()" id="playPauseBtn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
        Pause Flow
      </button>
      <button class="client-btn" onclick="window.print()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Save as PDF / Print
      </button>
      <button class="client-btn client-btn-primary" onclick="toggleFullscreen()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
        Fullscreen
      </button>
    </div>
  </div>
  `;
  html = html.replace(/<body([^>]*)>/, `<body$1>\n${topBarHtml}`);

  // 4h. Interactive standalone scripts
  const interactiveScripts = `
<script>
  let isPaused = false;
  function togglePlayPause() {
    const svg = document.querySelector('svg');
    const btn = document.getElementById('playPauseBtn');
    if (!svg) return;

    if (!isPaused) {
      if (svg.pauseAnimations) svg.pauseAnimations();
      btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Resume Flow';
      isPaused = true;
    } else {
      if (svg.unpauseAnimations) svg.unpauseAnimations();
      btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg> Pause Flow';
      isPaused = false;
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        alert('Could not enter fullscreen: ' + err.message);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  // Interactive Live Clock in Telemetry
  setInterval(() => {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
    const clockElems = document.querySelectorAll('.font-mono');
    clockElems.forEach(el => {
      if (el.textContent && el.textContent.includes(':') && el.textContent.length <= 10 && !el.textContent.includes('KLD') && !el.textContent.includes('m³')) {
        el.textContent = timeStr;
      }
    });
  }, 1000);
</script>
`;
  html = html.replace('</body>', `${interactiveScripts}</body>`);

  // Write out files
  const out1 = path.join(rootDir, 'Prestige_Tranquility_950KLD_STP_Schematic_Client_Document.html');
  const out2 = path.join(publicDir, 'Prestige_Tranquility_950KLD_STP_Schematic_Client_Document.html');
  const out3 = path.join(publicDir, 'stp-schematic-animated.html');

  fs.writeFileSync(out1, html, 'utf8');
  fs.writeFileSync(out2, html, 'utf8');
  fs.writeFileSync(out3, html, 'utf8');

  console.log('SUCCESS! Generated standalone client HTML documents:');
  console.log(` - ${out1} (${(html.length / 1024).toFixed(1)} KB)`);
  console.log(` - ${out2}`);
  console.log(` - ${out3}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
