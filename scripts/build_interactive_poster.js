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

// Extract Schematic SVG
const targetViewBox = 'viewBox="-65 0 1405 710"';
const viewBoxPos = rawHtml.indexOf(targetViewBox);
if (viewBoxPos === -1) {
  console.error('ERROR: Could not locate schematic SVG viewBox in .next/server/app/schematic.html');
  process.exit(1);
}

const svgStart = rawHtml.lastIndexOf('<svg', viewBoxPos);
const svgEnd = rawHtml.indexOf('</svg>', viewBoxPos) + 6;
let svgContent = rawHtml.substring(svgStart, svgEnd);

// Add unique ID to SVG for programmatic animation control
svgContent = svgContent.replace(
  '<svg',
  '<svg id="schematic-svg" style="width:100%;height:100%;max-height:100%;max-width:100%;display:block;"'
);

// Add interactive cursor and click hooks to pump elements
const pumpTags = [
  { tag: 'MBBR PUMP 1', id: 'M1' },
  { tag: 'MBBR PUMP 2', id: 'M2' },
  { tag: 'MBBR PUMP 3', id: 'M3' },
  { tag: 'MBBR PUMP 4', id: 'M4' },
  { tag: 'FF PUMP 1', id: 'M10' },
  { tag: 'FF PUMP 2', id: 'M11' },
  { tag: 'FLUSHING PUMP', id: 'M12' },
  { tag: 'BLOWER 1', id: 'BL1' },
  { tag: 'BLOWER 2', id: 'BL2' }
];

pumpTags.forEach(p => {
  const searchPattern = new RegExp(`(<text[^>]*>${p.tag}</text>)`, 'g');
  svgContent = svgContent.replace(searchPattern, `$1<rect x="-35" y="-35" width="70" height="70" fill="transparent" class="interactive-pump" onclick="inspectAsset('${p.id}')" style="cursor:pointer;" title="Click to inspect ${p.tag}"/>`);
});

// Construct Complete Standalone Interactive Poster HTML
const posterHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Prestige Tranquility 950 KLD STP — Interactive SCADA Process Digital Twin Poster</title>
  <style>
    /* Inlined App & Tailwind Styles */
    ${rawCss}

    /* Interactive Poster Custom Styles */
    * { box-sizing: border-box; }
    html, body {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: #f8fafc;
      user-select: none;
    }

    #poster-container {
      display: flex;
      flex-direction: column;
      width: 100vw;
      height: 100vh;
      background: linear-gradient(180deg, #090e17 0%, #0b1322 100%);
    }

    /* Executive Top Poster Header */
    #poster-header {
      height: 58px;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(56, 189, 248, 0.2);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      gap: 12px;
      z-index: 50;
      flex-shrink: 0;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      height: 36px;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    .brand-divider {
      width: 1px;
      height: 28px;
      background: rgba(148, 163, 184, 0.25);
    }
    .title-block {
      display: flex;
      flex-direction: column;
    }
    .plant-title {
      font-size: 13px;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .plant-subtitle {
      font-size: 10px;
      font-weight: 600;
      color: #38bdf8;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    /* Guided Stage Walkthrough Pills */
    .stage-pills-bar {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(30, 41, 59, 0.7);
      padding: 3px 6px;
      border-radius: 9999px;
      border: 1px solid rgba(71, 85, 105, 0.4);
    }
    .stage-pill {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .stage-pill:hover {
      color: #ffffff;
      background: rgba(56, 189, 248, 0.15);
    }
    .stage-pill.active {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.6);
      font-weight: 700;
    }

    /* Action Controls */
    .controls-section {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .ctrl-btn {
      background: rgba(30, 41, 59, 0.9);
      border: 1px solid rgba(71, 85, 105, 0.5);
      color: #e2e8f0;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .ctrl-btn:hover {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    .ctrl-btn-primary {
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      border-color: #38bdf8;
      color: #fff;
    }

    /* Poster Canvas Area */
    #schematic-canvas-wrapper {
      flex: 1;
      min-height: 0;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 8px 12px;
      overflow: hidden;
      background: radial-gradient(circle at 50% 50%, #0d1527 0%, #060911 100%);
    }

    #schematic-svg {
      filter: drop-shadow(0 4px 20px rgba(0,0,0,0.5));
    }

    .interactive-pump {
      transition: all 0.2s ease;
    }
    .interactive-pump:hover {
      stroke: #38bdf8;
      stroke-width: 2px;
      fill: rgba(56, 189, 248, 0.15);
    }

    /* Stage Information Callout Card */
    #stage-info-banner {
      position: absolute;
      bottom: 14px;
      left: 16px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 10px;
      padding: 10px 16px;
      max-width: 480px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      gap: 4px;
      z-index: 40;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .banner-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 9.5px;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #38bdf8;
    }
    .banner-title {
      font-size: 13px;
      font-weight: 700;
      color: #ffffff;
    }
    .banner-desc {
      font-size: 11px;
      color: #cbd5e1;
      line-height: 1.4;
    }

    /* Asset Telemetry Popover Modal */
    #telemetry-drawer {
      position: absolute;
      top: 70px;
      right: 16px;
      width: 320px;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
      padding: 16px;
      z-index: 100;
      display: none;
      flex-direction: column;
      gap: 12px;
      animation: slideInRight 0.25s ease-out;
    }
    @keyframes slideInRight {
      from { opacity: 0; transform: translateX(20px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .drawer-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      border-bottom: 1px solid rgba(56, 189, 248, 0.2);
      padding-bottom: 8px;
    }
    .drawer-title {
      font-size: 14px;
      font-weight: 800;
      color: #f8fafc;
    }
    .drawer-tag {
      font-size: 10px;
      font-family: monospace;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      padding: 2px 6px;
      border-radius: 4px;
    }
    .drawer-close {
      background: transparent;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      font-size: 18px;
      line-height: 1;
    }
    .drawer-close:hover { color: #fff; }
    
    .telemetry-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .telemetry-item {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(71, 85, 105, 0.4);
      padding: 6px 10px;
      border-radius: 6px;
    }
    .item-label {
      font-size: 9.5px;
      color: #94a3b8;
      font-weight: 600;
      text-transform: uppercase;
    }
    .item-val {
      font-size: 13px;
      font-weight: 700;
      color: #f1f5f9;
      font-family: monospace;
      margin-top: 2px;
    }

    .toggle-pump-btn {
      width: 100%;
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      border: 1px solid #38bdf8;
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }
    .toggle-pump-btn:hover {
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);
    }

    /* Live Pulsing Dot */
    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #22c55e;
      box-shadow: 0 0 8px #22c55e;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.3); }
    }

    @media (max-width: 1024px) {
      .stage-pills-bar { display: none; }
      #stage-info-banner { max-width: 90%; }
    }
  </style>
</head>
<body>
  <div id="poster-container">
    <!-- Top Executive Header -->
    <header id="poster-header">
      <div class="brand-section">
        ${prestigeBase64 ? `<img src="${prestigeBase64}" class="brand-logo" alt="Prestige Group">` : ''}
        <div class="brand-divider"></div>
        <div class="title-block">
          <span class="plant-title">
            <span class="pulse-dot"></span>
            PRESTIGE TRANQUILITY &bull; 950 KLD STP
          </span>
          <span class="plant-subtitle">Real-Time SCADA Process Digital Twin Poster</span>
        </div>
        ${ppmsBase64 ? `<img src="${ppmsBase64}" class="brand-logo" style="margin-left:8px;" alt="PPMS">` : ''}
      </div>

      <!-- Guided Stage Walkthrough Pills -->
      <nav class="stage-pills-bar">
        <button class="stage-pill active" onclick="selectStage('all')">Complete Plant Flow</button>
        <button class="stage-pill" onclick="selectStage('stage1')">1. Equalization & Screening</button>
        <button class="stage-pill" onclick="selectStage('stage2')">2. MBBR Aeration</button>
        <button class="stage-pill" onclick="selectStage('stage3')">3. Clarification & Sludge</button>
        <button class="stage-pill" onclick="selectStage('stage4')">4. Tertiary Media</button>
        <button class="stage-pill" onclick="selectStage('stage5')">5. Treated Distribution</button>
      </nav>

      <!-- Action Controls -->
      <div class="controls-section">
        <button class="ctrl-btn" id="playBtn" onclick="togglePlay()">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          <span id="playText">Pause</span>
        </button>
        <button class="ctrl-btn ctrl-btn-primary" onclick="toggleFullscreen()">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
          Fullscreen
        </button>
      </div>
    </header>

    <!-- Main Schematic Poster Canvas -->
    <main id="schematic-canvas-wrapper">
      ${svgContent}

      <!-- Stage Information Callout Card -->
      <div id="stage-info-banner">
        <span class="banner-badge">Process Flow Overview</span>
        <span class="banner-title" id="stage-title">Prestige Tranquility 950 KLD Complete Hydraulic Train</span>
        <span class="banner-desc" id="stage-desc">
          Continuous 24/7 automated SCADA biological wastewater recycling. Click any pump (M1–M11, BL1, BL2) on the poster to inspect live motor telemetry and interlocks.
        </span>
      </div>

      <!-- Interactive Equipment Telemetry Popover Drawer -->
      <div id="telemetry-drawer">
        <div class="drawer-header">
          <div>
            <div class="drawer-title" id="drawer-name">Raw Sewage Pump 1</div>
            <span class="drawer-tag" id="drawer-tag">PUMP-M1</span>
          </div>
          <button class="drawer-close" onclick="closeDrawer()">&times;</button>
        </div>

        <div class="telemetry-grid">
          <div class="telemetry-item">
            <div class="item-label">Operating Status</div>
            <div class="item-val" id="drawer-status" style="color:#22c55e;">RUNNING</div>
          </div>
          <div class="telemetry-item">
            <div class="item-label">Design Flow</div>
            <div class="item-val" id="drawer-flow">45.0 m³/hr</div>
          </div>
          <div class="telemetry-item">
            <div class="item-label">Motor Rating</div>
            <div class="item-val" id="drawer-power">5.5 kW</div>
          </div>
          <div class="telemetry-item">
            <div class="item-label">VFD Frequency</div>
            <div class="item-val" id="drawer-freq">48.2 Hz</div>
          </div>
        </div>

        <button class="toggle-pump-btn" id="toggle-pump-action" onclick="toggleCurrentPump()">
          Toggle Duty / Standby Switch
        </button>
      </div>
    </main>
  </div>

  <script>
    // ==========================================
    // 1. ASSET DATABASE & STATE MANAGEMENT
    // ==========================================
    const assets = {
      M1: { tag: 'M1', name: 'Raw Sewage Feed Pump 1', status: 'RUNNING', flow: '45.0 m³/hr', power: '5.5 kW', freq: '48.2 Hz' },
      M2: { tag: 'M2', name: 'Raw Sewage Feed Pump 2', status: 'STANDBY', flow: '0.0 m³/hr', power: '5.5 kW', freq: '0.0 Hz' },
      M3: { tag: 'M3', name: 'MBBR Recirculation Pump 3', status: 'STANDBY', flow: '0.0 m³/hr', power: '1.5 kW', freq: '0.0 Hz' },
      M4: { tag: 'M4', name: 'MBBR Recirculation Pump 4', status: 'RUNNING', flow: '6.8 m³/hr', power: '1.5 kW', freq: '46.0 Hz' },
      M10: { tag: 'M10', name: 'Filter Feed Pump 1', status: 'RUNNING', flow: '50.0 m³/hr', power: '7.5 kW', freq: '50.0 Hz' },
      M11: { tag: 'M11', name: 'Filter Feed Pump 2', status: 'STANDBY', flow: '0.0 m³/hr', power: '7.5 kW', freq: '0.0 Hz' },
      M12: { tag: 'M12', name: 'Flushing Booster Pump', status: 'RUNNING', flow: '30.0 m³/hr', power: '5.5 kW', freq: '49.1 Hz' },
      BL1: { tag: 'BL1', name: 'Fine Bubble Air Blower 1', status: 'STANDBY', flow: '0 CFM', power: '22 kW', freq: '0 RPM' },
      BL2: { tag: 'BL2', name: 'Fine Bubble Air Blower 2', status: 'RUNNING', flow: '1,450 CFM', power: '22 kW', freq: '1,450 RPM' }
    };

    let activeAssetId = null;

    function inspectAsset(id) {
      const a = assets[id];
      if (!a) return;
      activeAssetId = id;

      document.getElementById('drawer-name').textContent = a.name;
      document.getElementById('drawer-tag').textContent = 'PUMP-' + a.tag;
      
      const statusEl = document.getElementById('drawer-status');
      statusEl.textContent = a.status;
      statusEl.style.color = a.status === 'RUNNING' ? '#22c55e' : '#ef4444';

      document.getElementById('drawer-flow').textContent = a.flow;
      document.getElementById('drawer-power').textContent = a.power;
      document.getElementById('drawer-freq').textContent = a.freq;

      document.getElementById('telemetry-drawer').style.display = 'flex';
    }

    function closeDrawer() {
      document.getElementById('telemetry-drawer').style.display = 'none';
      activeAssetId = null;
    }

    function toggleCurrentPump() {
      if (!activeAssetId || !assets[activeAssetId]) return;
      const a = assets[activeAssetId];
      if (a.status === 'RUNNING') {
        a.status = 'STANDBY';
        a.flow = '0.0 m³/hr';
        a.freq = '0.0 Hz';
      } else {
        a.status = 'RUNNING';
        a.flow = '45.0 m³/hr';
        a.freq = '48.2 Hz';
      }
      inspectAsset(activeAssetId);
    }

    // ==========================================
    // 2. GUIDED STAGE WALKTHROUGH
    // ==========================================
    const stages = {
      all: {
        badge: 'Plant Hydraulic Overview',
        title: 'Prestige Tranquility 950 KLD Complete Hydraulic Train',
        desc: 'Continuous 24/7 automated SCADA biological wastewater recycling. Click any pump (M1–M11, BL1, BL2) on the poster to inspect live motor telemetry and interlocks.'
      },
      stage1: {
        badge: 'Stage 1 : Primary Screening & Equalization',
        title: 'Bar Screen Chamber & Raw Sewage Sump',
        desc: 'Buffers peak hydraulic domestic inflow and traps suspended solids. Raw Sewage transfer pumps (M1 Duty, M2 Standby) meter effluent into biological digestion at 45 m³/hr.'
      },
      stage2: {
        badge: 'Stage 2 : Biological Aeration (MBBR)',
        title: 'Twin MBBR Aeration Basins with Fine-Bubble Diffusers',
        desc: 'High-surface-area fluidized biomedia carrier beds oxidize dissolved carbonaceous BOD and nitrify ammonia. Twin air blowers (BL2 Duty, BL1 Standby) maintain DO at 2.4 mg/L.'
      },
      stage3: {
        badge: 'Stage 3 : Secondary Clarification',
        title: 'Conical Hopper Clarifier & Sludge Handling',
        desc: 'Slow-speed bridge scraper settles bio-floc to conical bottom. Supernatant overflows into Filter Feed tank while RAS pump returns active biomass; excess sludge is routed to filter press.'
      },
      stage4: {
        badge: 'Stage 4 : Tertiary Media Filtration',
        title: 'Dual Media Pressure Sand & Carbon Filters (PSF / ACF)',
        desc: 'Filter feed pumps (M10 Duty, M11 Standby) deliver 50 m³/hr through multi-grade silica sand (removes turbidity < 2 NTU) and activated carbon (adsorbs color, odor, and residual organics).'
      },
      stage5: {
        badge: 'Stage 5 : Final Disinfection & Dual Distribution',
        title: 'Chlorine Contact & Dual Supply Headers (Flushing & Gardening)',
        desc: '100% recycled water complies strictly with CPCB/KSPCB norms (BOD < 5 mg/L, TSS < 2 mg/L), pressurized into dedicated headers for toilet flushing and landscape irrigation.'
      }
    };

    function selectStage(key) {
      // Update Pills UI
      const pills = document.querySelectorAll('.stage-pill');
      pills.forEach(p => p.classList.remove('active'));
      const activeBtn = Array.from(pills).find(p => p.getAttribute('onclick').includes(key));
      if (activeBtn) activeBtn.classList.add('active');

      // Update Callout Banner
      const s = stages[key] || stages.all;
      const banner = document.getElementById('stage-info-banner');
      banner.querySelector('.banner-badge').textContent = s.badge;
      document.getElementById('stage-title').textContent = s.title;
      document.getElementById('stage-desc').textContent = s.desc;
    }

    // ==========================================
    // 3. PLAY/PAUSE & ANIMATION CONTROLLER
    // ==========================================
    let isPlaying = true;
    function togglePlay() {
      const svg = document.getElementById('schematic-svg');
      const text = document.getElementById('playText');
      if (!svg) return;

      if (isPlaying) {
        if (svg.pauseAnimations) svg.pauseAnimations();
        text.textContent = 'Resume';
        isPlaying = false;
      } else {
        if (svg.unpauseAnimations) svg.unpauseAnimations();
        text.textContent = 'Pause';
        isPlaying = true;
      }
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          alert('Could not enter fullscreen: ' + err.message);
        });
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    // ==========================================
    // 4. LIVE TELEMETRY JITTER & CLOCKS
    // ==========================================
    setInterval(() => {
      // Live system clock
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
      const monoElements = document.querySelectorAll('.font-mono');
      monoElements.forEach(el => {
        if (el.textContent && el.textContent.includes(':') && el.textContent.length <= 11 && !el.textContent.includes('KLD') && !el.textContent.includes('m³')) {
          el.textContent = timeStr;
        }
      });
    }, 1000);
  </script>
</body>
</html>`;

const outPath1 = path.join(rootDir, 'Prestige_STP_950KLD_Interactive_Poster.html');
const outPath2 = path.join(rootDir, 'public', 'Prestige_STP_950KLD_Interactive_Poster.html');

fs.writeFileSync(outPath1, posterHtml, 'utf8');
fs.writeFileSync(outPath2, posterHtml, 'utf8');

console.log('SUCCESS: Generated Interactive SCADA Digital Poster:');
console.log('1.', outPath1);
console.log('2.', outPath2);
console.log('Poster file size: ' + Math.round(posterHtml.length / 1024) + ' KB');
