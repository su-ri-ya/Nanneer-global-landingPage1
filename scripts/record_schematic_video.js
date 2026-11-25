const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const htmlUrl = 'file:///C:/Nanneer global/draft 3/public/Prestige_STP_950KLD_Animated_Poster.html';
const framesDir = path.join(__dirname, '..', 'public', 'images', 'video_frames');

if (!fs.existsSync(framesDir)) {
  fs.mkdirSync(framesDir, { recursive: true });
}

console.log('Starting headless Chrome for Video Recording (1920x1080)...');
const chromeProcess = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9223',
  '--no-sandbox',
  '--disable-gpu',
  '--window-size=1920,1080',
  `--user-data-dir=${process.env.TEMP}\\chrome_video_profile`,
  htmlUrl
]);

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function run() {
  console.log('Connecting to Chrome CDP...');
  let pages = null;
  for (let i = 0; i < 20; i++) {
    await sleep(400);
    try {
      pages = await getJson('http://127.0.0.1:9223/json');
      if (pages && pages.length > 0) break;
    } catch (e) {}
  }

  if (!pages || pages.length === 0) {
    console.error('Failed to connect to Chrome.');
    chromeProcess.kill();
    process.exit(1);
  }

  const page = pages.find(p => p.type === 'page') || pages[0];
  const ws = new WebSocket(page.webSocketDebuggerUrl);

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  let messageId = 1;
  const callbacks = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg);
      callbacks.delete(msg.id);
    }
  };

  function sendCommand(method, params = {}) {
    return new Promise((resolve) => {
      const id = messageId++;
      callbacks.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  // Let fluid flow stabilize
  await sleep(1500);

  const totalFrames = 30; // 30 frames at ~66ms intervals = 2.0s loop
  console.log(`Recording ${totalFrames} high-resolution 1080p frames...`);

  for (let i = 0; i < totalFrames; i++) {
    const res = await sendCommand('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: false
    });

    if (res && res.result && res.result.data) {
      const filePath = path.join(framesDir, `frame_${String(i).padStart(3, '0')}.png`);
      fs.writeFileSync(filePath, Buffer.from(res.result.data, 'base64'));
    }
    await sleep(65);
  }

  console.log('Frame capture complete.');
  ws.close();
  chromeProcess.kill();
}

run().catch(err => {
  console.error('Error:', err);
  chromeProcess.kill();
  process.exit(1);
});
