// Render the social cards (1200x630) and app icons with headless Chrome.
// No dependencies (Node 22+). Run from the repo root:
//   node .build/og_cards.mjs
// Writes assets/img/og/og-*.jpg, assets/img/apple-touch-icon.png, assets/img/favicon-32.png
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const ROOT = resolve(new URL('..', import.meta.url).pathname);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const TMP = mkdtempSync(join(tmpdir(), 'og-'));
const PORT = 9341;
mkdirSync(join(ROOT, 'assets/img/og'), { recursive: true });

const CARDS = [
  { out: 'og-home', bg: 'assets/img/hero/hero-poster.jpg', pos: '60% 50%', title: 'I build AI that sees.', lines: ['I build AI', 'that sees.'], line: 'Applied AI, iOS and backend engineer in Los Angeles.', chip: 'downtown_la 0.98', box: [800, 214, 228, 120] },
  { out: 'og-fitandfine', bg: 'assets/img/web/atmo-fitandfine.jpg', pos: '70% 50%', title: 'FitandFine', line: 'A solo-built iOS nutrition app with four Claude agents.', chip: 'ios_app 0.99', box: [688, 300, 330, 210] },
  { out: 'og-fitform', bg: 'assets/img/web/atmo-fitform.jpg', pos: '70% 50%', title: 'FitForm', line: 'A patent-pending camera coach for exercise form.', chip: 'pose 33/33', box: [736, 70, 300, 440] },
  { out: 'og-chatdb', bg: 'assets/img/web/atmo-chatdb.jpg', pos: '60% 50%', title: 'Chat-DB', line: 'Ask a database in plain English. Check the query before it runs.', chip: 'sql 0.92', box: [720, 130, 270, 360] },
  { out: 'og-safesense', bg: 'assets/img/web/atmo-safesense.jpg', pos: '70% 50%', title: 'SafeSense', line: 'A fire alarm that reaches you when nobody is home.', chip: 'smoke 0.97', box: [744, 150, 340, 330] },
  { out: 'og-facehand', bg: 'assets/img/web/atmo-facehand.jpg', pos: '70% 50%', title: 'Face & Hand Recognition', lines: ['Face & Hand', 'Recognition'], line: 'Count fingers on camera. Light the matching LEDs.', chip: 'leds 5/5', box: [700, 300, 330, 200] },
  { out: 'og-roboticarm', bg: 'assets/img/web/atmo-roboticarm.jpg', pos: '70% 50%', title: 'Gesture-Controlled Robotic Arm', lines: ['Gesture-Controlled', 'Robotic Arm'], line: 'A servo arm that mirrors your hand.', chip: 'servo_arm 0.98', box: [780, 90, 290, 430] },
];

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,700..800&family=Atkinson+Hyperlegible+Mono:wght@500&family=Atkinson+Hyperlegible+Next:wght@400;600&display=block';

function cardHtml(c) {
  const [bx, by, bw, bh] = c.box;
  const big = c.title.length > 22;
  const title = (c.lines || [c.title]).map(esc).join('<br>');
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="${FONTS}"><style>
  *{margin:0;box-sizing:border-box}
  html,body{width:1200px;height:630px;overflow:hidden;background:#0D1424}
  .bg{position:absolute;inset:0;background:url('file://${join(ROOT, c.bg)}') ${c.pos}/cover no-repeat}
  .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,14,26,.94) 0%,rgba(9,14,26,.78) 38%,rgba(9,14,26,.2) 70%,rgba(9,14,26,.35) 100%),linear-gradient(0deg,rgba(9,14,26,.6),rgba(9,14,26,0) 40%)}
  .brand{position:absolute;left:64px;top:56px;display:flex;align-items:center;gap:16px;font:600 24px 'Atkinson Hyperlegible Next';color:#ECE9E1}
  .mark{width:52px;height:52px;border-radius:12px;display:grid;place-items:center;background:#1B2640;border:1.5px solid #5C6884;font:800 19px 'Archivo';font-stretch:125%}
  .copy{position:absolute;left:64px;bottom:52px;width:580px;display:flex;flex-direction:column;align-items:flex-start;gap:18px}
  h1{white-space:nowrap;font:800 ${big ? 56 : 80}px/1.02 'Archivo';font-stretch:120%;letter-spacing:-.025em;color:#ECE9E1;text-shadow:0 4px 30px rgba(5,5,10,.6)}
  p{font:400 26px/1.35 'Atkinson Hyperlegible Next';color:#DCDFE8;margin-bottom:10px;text-wrap:balance}
  .url{display:flex;align-items:center;gap:10px;font:500 19px 'Atkinson Hyperlegible Mono';color:#ECE9E1;padding:9px 14px;border-radius:8px;background:rgba(9,14,26,.7);border:1px solid rgba(124,147,255,.4)}
  .dot{width:7px;height:7px;border-radius:1.5px;background:#7C93FF}
  .box{position:absolute;left:${bx}px;top:${by}px;width:${bw}px;height:${bh}px;
    background:linear-gradient(#7C93FF,#7C93FF) top left/26px 2.5px,linear-gradient(#7C93FF,#7C93FF) top left/2.5px 26px,
    linear-gradient(#7C93FF,#7C93FF) top right/26px 2.5px,linear-gradient(#7C93FF,#7C93FF) top right/2.5px 26px,
    linear-gradient(#7C93FF,#7C93FF) bottom left/26px 2.5px,linear-gradient(#7C93FF,#7C93FF) bottom left/2.5px 26px,
    linear-gradient(#7C93FF,#7C93FF) bottom right/26px 2.5px,linear-gradient(#7C93FF,#7C93FF) bottom right/2.5px 26px;background-repeat:no-repeat}
  .box span{position:absolute;left:0;bottom:calc(100% + 10px);display:flex;align-items:center;gap:8px;white-space:nowrap;font:500 16px 'Atkinson Hyperlegible Mono';color:#ECE9E1;padding:7px 11px;border-radius:7px;background:rgba(9,14,26,.75);border:1px solid rgba(124,147,255,.4)}
  </style></head><body>
  <div class="bg"></div><div class="shade"></div>
  <div class="box"><span><i class="dot"></i>${esc(c.chip)}</span></div>
  <div class="brand"><span class="mark">AS</span>Aditya Sidham</div>
  <div class="copy"><h1>${title}</h1><p>${esc(c.line)}</p>
  <div class="url"><i class="dot"></i>adityasidham.site</div></div>
  </body></html>`;
}

function iconHtml(size) {
  // square, opaque: iOS rounds the corners itself
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="${FONTS}"><style>
  *{margin:0}html,body{width:${size}px;height:${size}px;overflow:hidden;background:#0D1424}
  svg{display:block;width:${size}px;height:${size}px}</style></head><body>
  <svg viewBox="0 0 64 64"><rect width="64" height="64" fill="#0D1424"/>
  <path d="M10 20V10h10M44 10h10v10M54 44v10H44M20 54H10V44" fill="none" stroke="#7C93FF" stroke-width="3" stroke-linecap="round"/>
  <text x="32" y="40.5" text-anchor="middle" font-family="Archivo" font-stretch="125%" font-size="21" font-weight="800" letter-spacing="-.8" fill="#ECE9E1">AS</text></svg>
  </body></html>`;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${PORT}`, `--user-data-dir=${join(TMP, 'p')}`,
  '--hide-scrollbars', '--allow-file-access-from-files', '--no-first-run', 'about:blank'], { stdio: 'ignore' });
let ws, id = 0;
const pending = new Map();
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

async function render(html, w, h, file, format) {
  const page = join(TMP, 'page.html');
  writeFileSync(page, html);
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'file://' + page });
  await sleep(600);
  await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300)))', awaitPromise: true });
  const r = await send('Page.captureScreenshot', { format, quality: format === 'jpeg' ? 88 : undefined, clip: { x: 0, y: 0, width: w, height: h, scale: 1 } });
  writeFileSync(file, Buffer.from(r.result.data, 'base64'));
  console.log('wrote', file.replace(ROOT + '/', ''));
}

try {
  for (let i = 0; i < 50 && !ws; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const t = list.find(x => x.type === 'page');
      if (t) { ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.addEventListener('open', r, { once: true })); }
    } catch { await sleep(200); }
  }
  ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
  await send('Page.enable');
  for (const c of CARDS) await render(cardHtml(c), 1200, 630, join(ROOT, 'assets/img/og', c.out + '.jpg'), 'jpeg');
  await render(iconHtml(180), 180, 180, join(ROOT, 'assets/img/apple-touch-icon.png'), 'png');
  await render(iconHtml(32), 32, 32, join(ROOT, 'assets/img/favicon-32.png'), 'png');
} finally {
  ws && ws.close();
  chrome.kill();
}
