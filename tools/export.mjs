// Renders the brochure to print PDFs and PNG previews.
//   node export.mjs            → brochure/dist/*.pdf + *.png
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../brochure/', import.meta.url));
const dist = join(root, 'dist');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2' };

const server = createServer(async (req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^([/\\])+/, '');
  try {
    const body = await readFile(join(root, path || 'index.html'));
    res.writeHead(200, { 'content-type': types[extname(path)] ?? 'application/octet-stream' }).end(body);
  } catch { res.writeHead(404).end(); }
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}/index.html`;

await mkdir(dist, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1800, height: 1000 }, deviceScaleFactor: 2.5 });

async function load(query = '') {
  await page.goto(base + query, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.ready === '1');
  await page.emulateMedia({ reducedMotion: 'reduce' });
}

// screen previews (trim size)
await load();
const sheets = await page.$$('.sheet');
await sheets[0].screenshot({ path: join(dist, 'side-a-outside.png') });
await sheets[1].screenshot({ path: join(dist, 'side-b-inside.png') });

// print PDFs: trim, and with 3 mm bleed
await page.pdf({ path: join(dist, 'Elevatus_Trifold_A5_trim.pdf'), printBackground: true, preferCSSPageSize: true });
await load('?bleed=1');
await page.pdf({ path: join(dist, 'Elevatus_Trifold_A5_bleed3mm.pdf'), printBackground: true, preferCSSPageSize: true });

await browser.close();
server.close();
console.log('exported to', dist);
