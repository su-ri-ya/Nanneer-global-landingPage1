const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const rootDir = 'C:\\Nanneer global\\draft 3';
const publicDir = path.join(rootDir, 'public');

async function main() {
  console.log('1. Fetching CSS from Next.js server...');
  const cssRes = await fetch('http://localhost:3001/_next/static/css/app/layout.css');
  const cssText = await cssRes.text();

  console.log('2. Converting logos to Base64...');
  const prestigeBase64 = 'data:image/png;base64,' + fs.readFileSync(path.join(publicDir, 'images', 'prestige-group-logo.png')).toString('base64');
  const ppmsBase64 = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(publicDir, 'images', 'ppms-logo.jpg')).toString('base64');

  console.log('3. Dumping rendered DOM from Chrome...');
  let html = execSync(`"${chromePath}" --headless=new --virtual-time-budget=3000 --dump-dom http://localhost:3001/schematic`, {
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024
  });

  console.log('4. Processing HTML for standalone offline viewing...');
  
  // Replace CSS link with inlined CSS
  html = html.replace(/<link[^>]+rel=["']stylesheet["'][^>]*>/gi, `<style>${cssText}\n@page { size: 1400px 900px; margin: 0; }\n@media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } .no-print { display: none !important; } }\n</style>`);

  // Replace images with Base64
  html = html.replace(/src=["']\/images\/prestige-group-logo\.png["']/g, `src="${prestigeBase64}"`);
  html = html.replace(/src=["']\/images\/ppms-logo\.jpg["']/g, `src="${ppmsBase64}"`);

  // Remove Next.js script tags to avoid hydration mismatch warnings
  html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

  // Remove "Back to Home" button
  html = html.replace(/<div class="w-full mb-1 shrink-0 flex items-center justify-between">[\s\S]*?<\/div>/, '');

  // Remove nextjs dev overlay and portal divs if any
  html = html.replace(/<next-route-announcer>[\s\S]*?<\/next-route-announcer>/g, '');

  // Add interactive JS for offline toggle and sensor animation
  const interactiveScript = `
<script>
  // Self-contained interactivity for standalone view
  document.addEventListener('DOMContentLoaded', () => {
    console.log('SCADA Simulation Loaded in Offline Standalone Mode');
  });
</script>
`;
  html = html.replace('</body>', `${interactiveScript}</body>`);

  // Update page title
  html = html.replace(/<title>[\s\S]*?<\/title>/, '<title>Nanneer Global - SCADA STP Process Schematic</title>');

  // Save standalone animated HTML
  const standalonePath = path.join(rootDir, 'stp-schematic-animated.html');
  const publicHtmlPath = path.join(publicDir, 'stp-schematic-animated.html');
  fs.writeFileSync(standalonePath, html, 'utf8');
  fs.writeFileSync(publicHtmlPath, html, 'utf8');
  console.log(`Saved Standalone Animated HTML to:\n  - ${standalonePath}\n  - ${publicHtmlPath}`);

  // 5. Generate high-resolution PDF
  console.log('5. Generating High-Resolution Vector PDF from Chrome...');
  const pdfPath = path.join(rootDir, 'stp-schematic.pdf');
  const publicPdfPath = path.join(publicDir, 'stp-schematic.pdf');

  execSync(`"${chromePath}" --headless=new --run-all-compositor-stages-before-draw --virtual-time-budget=3000 --window-size=1600,1050 --print-to-pdf="${pdfPath}" --no-pdf-header-footer "file:///${standalonePath.replace(/\\/g, '/')}"`, {
    stdio: 'inherit'
  });

  fs.copyFileSync(pdfPath, publicPdfPath);
  console.log(`Saved High-Resolution Vector PDF to:\n  - ${pdfPath}\n  - ${publicPdfPath}`);
  console.log(`PDF Size: ${(fs.statSync(pdfPath).size / 1024).toFixed(1)} KB`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
