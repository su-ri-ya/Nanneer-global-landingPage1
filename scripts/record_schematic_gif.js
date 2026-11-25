const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const htmlUrl = 'file:///C:/Nanneer global/draft 3/public/STP_SCADA_Process_Schematic_Client_Presentation.html';
const tempDir = path.join(__dirname, '..', 'public', 'images', 'frames');

if (!fs.existsSync(tempDir)) {
  fs.mkdirSync(tempDir, { recursive: true });
}

console.log('Launching headless Chrome...');
const chromeProcess = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9222',
  '--no-sandbox',
  '--disable-gpu',
  '--window-size=1600,900',
  `--user-data-dir=${process.env.TEMP}\\chrome_cdp_profile`,
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
  console.log('Waiting for Chrome CDP endpoint...');
  let pages = null;
  for (let i = 0; i < 20; i++) {
    await sleep(500);
    try {
      pages = await getJson('http://127.0.0.1:9222/json');
      if (pages && pages.length > 0) break;
    } catch (e) {
      // wait more
    }
  }

  if (!pages || pages.length === 0) {
    console.error('Could not connect to Chrome CDP.');
    chromeProcess.kill();
    process.exit(1);
  }

  const page = pages.find(p => p.type === 'page') || pages[0];
  console.log('Connecting to WebSocket:', page.webSocketDebuggerUrl);

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

  // Let animations start running for 1.5 seconds
  console.log('Page loaded, allowing SVG animations to run...');
  await sleep(1500);

  const numFrames = 20; // 20 frames
  const frameIntervalMs = 100; // 100ms per frame = 2 seconds total cycle
  console.log(`Capturing ${numFrames} sequential animation frames...`);

  const frameFiles = [];
  for (let i = 0; i < numFrames; i++) {
    const res = await sendCommand('Page.captureScreenshot', {
      format: 'png',
      quality: 85
    });

    if (res && res.result && res.result.data) {
      const filePath = path.join(tempDir, `frame_${String(i).padStart(3, '0')}.png`);
      fs.writeFileSync(filePath, Buffer.from(res.result.data, 'base64'));
      frameFiles.push(filePath);
    }
    await sleep(frameIntervalMs);
  }

  console.log(`Successfully captured ${frameFiles.length} frames.`);

  ws.close();
  chromeProcess.kill();
  console.log('Finished capturing frames.');
}

run().catch(err => {
  console.error('Error:', err);
  chromeProcess.kill();
  process.exit(1);
});
