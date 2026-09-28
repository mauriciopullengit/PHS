
import { chromium } from 'playwright';
import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';

const OUT_DIR = 'C:/Users/mau/Projetos/jarvis-voice/video-tmp';
const WEBM    = 'C:/Users/mau/Projetos/jarvis-voice/video-tmp/reactor-speaking.webm';
const DUR_MS  = 20952;

fs.mkdirSync(OUT_DIR, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 860, height: 860 },
  recordVideo: { dir: OUT_DIR, size: { width: 860, height: 860 } },
});
const page = await context.newPage();
await page.goto('http://localhost:8765/arc-reactor-demo.html', { waitUntil: 'networkidle' });

// Activa modo Speaking imediatamente
await page.click('button:has-text("Falando")');
await page.waitForTimeout(DUR_MS + 500);

await context.close();
await browser.close();

// Renomear webm gerado
const files = fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.webm'));
if (files.length) {
  const src = path.join(OUT_DIR, files[files.length-1]);
  fs.renameSync(src, WEBM);
  console.log('[ok] Video gravado: ' + WEBM);
} else {
  console.error('[erro] Nenhum webm encontrado');
  process.exit(1);
}
