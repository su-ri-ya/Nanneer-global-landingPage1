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

  console.log('4. Assembling fine-tuned client presentation document...');

  // 4a. Inline full Tailwind CSS & Custom Presentation Bar
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
  flex-shrink: 0;
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
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  user-select: none;
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
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
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

  // 4g. Adjust body and container classes for 100% zero-scroll lock
  // Replace body class with viewport-locking flex container
  html = html.replace(/<body class="[^"]*"/, '<body class="h-screen max-h-screen overflow-hidden flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-teal-500 selection:text-white"');
  
  // Replace inner container from h-screen max-h-screen to flex-1 min-h-0
  html = html.replace(/class="h-screen max-h-screen bg-slate-50 flex flex-col p-1 sm:p-2[^"]*overflow-hidden/, 'class="w-full flex-1 min-h-0 bg-slate-50 flex flex-col p-1 sm:p-2 [@media(max-height:500px)]:p-0.5 overflow-hidden');

  // 4h. Insert Presentation Top Bar right inside <body> (WITHOUT Save as PDF / Print button)
  const topBarHtml = `
  <div id="client-header-bar">
    <div style="display: flex; align-items: center; gap: 10px;">
      <span class="client-pill"><span class="client-dot"></span> CLIENT DOCUMENT</span>
      <span style="font-weight: 700; font-size: 13px; color: #f8fafc; letter-spacing: -0.01em;">
        PRESTIGE TRANQUILITY &bull; 950 KLD STP PROCESS SCHEMATIC &amp; SCADA SIMULATION
      </span>
      <span style="font-size: 11px; color: #94a3b8; font-family: monospace;" class="hidden md:inline">
        [MBBR Biological + Tertiary Media Filtration]
      </span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
      <button class="client-btn" onclick="togglePlayPause()" id="playPauseBtn" title="Pause or resume flow animation">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" id="playPauseIcon"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
        <span id="playPauseText">Pause Flow</span>
      </button>
      <button class="client-btn client-btn-primary" onclick="toggleFullscreen()" id="fullscreenBtn" title="Toggle Fullscreen (or press F)">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" id="fullscreenIcon"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
        <span id="fullscreenText">Fullscreen</span>
      </button>
    </div>
  </div>
  `;
  html = html.replace(/<body([^>]*)>/, `<body$1>\n${topBarHtml}`);

  // 4i. Interactive standalone scripts (Fullscreen, Speed 1x/2x/5x, Play/Pause, Live Clock)
  const interactiveScripts = `
<script>
  // 1. Play / Pause Control
  let isPaused = false;
  function togglePlayPause() {
    const svg = document.querySelector('svg');
    const btn = document.getElementById('playPauseBtn');
    const text = document.getElementById('playPauseText');
    const icon = document.getElementById('playPauseIcon');
    if (!svg) return;

    if (!isPaused) {
      if (svg.pauseAnimations) svg.pauseAnimations();
      if (text) text.textContent = 'Resume Flow';
      if (icon) icon.outerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" id="playPauseIcon"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
      isPaused = true;
    } else {
      if (svg.unpauseAnimations) svg.unpauseAnimations();
      if (text) text.textContent = 'Pause Flow';
      if (icon) icon.outerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" id="playPauseIcon"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>';
      isPaused = false;
    }
  }

  // 2. Fullscreen Control with Full State Synchronization
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

  document.addEventListener('fullscreenchange', () => {
    const btn = document.getElementById('fullscreenBtn');
    const text = document.getElementById('fullscreenText');
    const icon = document.getElementById('fullscreenIcon');
    if (document.fullscreenElement) {
      if (text) text.textContent = 'Exit Fullscreen';
      if (icon) icon.outerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" id="fullscreenIcon"><path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path></svg>';
    } else {
      if (text) text.textContent = 'Fullscreen';
      if (icon) icon.outerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" id="fullscreenIcon"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>';
    }
  });

  // Keyboard Shortcut: press 'F' to toggle fullscreen, Space to play/pause
  window.addEventListener('keydown', (e) => {
    if (e.key === 'f' || e.key === 'F') {
      toggleFullscreen();
    } else if (e.key === ' ') {
      e.preventDefault();
      togglePlayPause();
    }
  });

  // 3. Interactive Speed Controls (1x, 2x, 5x)
  let currentSpeed = 1;
  const originalDurs = new Map();

  function setSimSpeed(multiplier) {
    currentSpeed = multiplier;
    const animElements = document.querySelectorAll('svg animate, svg animateTransform');
    animElements.forEach((el, index) => {
      if (!originalDurs.has(index)) {
        const rawDur = el.getAttribute('dur') || '1s';
        const sec = parseFloat(rawDur) || 1;
        originalDurs.set(index, sec);
      }
      const baseSec = originalDurs.get(index);
      el.setAttribute('dur', (baseSec / multiplier) + 's');
    });

    // Update active button UI
    const speedButtons = document.querySelectorAll('.flex.items-center.bg-white.rounded-md button');
    speedButtons.forEach(btn => {
      const txt = btn.textContent.trim();
      if (txt === multiplier + 'x') {
        btn.className = 'px-1.5 sm:px-2 py-0.5 text-[9px] sm:text-[10px] font-mono rounded bg-sky-600 text-white font-bold';
      } else {
        btn.className = 'px-1.5 sm:px-2 py-0.5 text-[9px] sm:text-[10px] font-mono rounded text-slate-600 hover:text-slate-900';
      }
    });
  }

  // Bind speed buttons
  document.addEventListener('DOMContentLoaded', () => {
    const speedButtons = document.querySelectorAll('.flex.items-center.bg-white.rounded-md button');
    speedButtons.forEach(btn => {
      const txt = btn.textContent.trim();
      const mult = parseInt(txt);
      if (!isNaN(mult)) {
        btn.addEventListener('click', () => setSimSpeed(mult));
      }
    });

    // Bind card pause button
    const cardPauseBtn = document.querySelector('button.text-amber-700');
    if (cardPauseBtn) {
      cardPauseBtn.addEventListener('click', togglePlayPause);
    }
  });

  // 4. Interactive Live Clock in Telemetry
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

  console.log('SUCCESS! Generated fine-tuned client HTML documents:');
  console.log(` - ${out1} (${(html.length / 1024).toFixed(1)} KB)`);
  console.log(` - ${out2}`);
  console.log(` - ${out3}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
