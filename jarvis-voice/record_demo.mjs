import { chromium } from 'playwright';
import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';

const OUT_DIR  = 'C:/Users/mau/Projetos/jarvis-voice/video-tmp';
const MP4_OUT  = 'C:/Users/mau/Projetos/jarvis-voice/jarvis-demo.mp4';
const PAGE_URL = 'http://localhost:8765/arc-reactor-demo.html';

fs.mkdirSync(OUT_DIR, { recursive: true });

console.log('[1] Abrindo browser...');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 900, height: 700 },
  recordVideo: { dir: OUT_DIR, size: { width: 900, height: 700 } },
});
const page = await context.newPage();

await page.goto(PAGE_URL, { waitUntil: 'networkidle' });
console.log('[2] Pagina carregada. Simulando estados...');

// Idle por 3s
await page.waitForTimeout(3000);

// Ouvindo
await page.click('button:has-text("Ouvindo")');
await page.waitForTimeout(3000);

// Pensando
await page.click('button:has-text("Pensando")');
await page.waitForTimeout(4000);

// Falando
await page.click('button:has-text("Falando")');
await page.waitForTimeout(4000);

// Volta idle
await page.click('button:has-text("Idle")');
await page.waitForTimeout(2000);

console.log('[3] Encerrando e salvando video...');
await context.close();
await browser.close();

// Encontrar o webm gerado
const webms = fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.webm'));
if (!webms.length) { console.error('Nenhum video encontrado'); process.exit(1); }
const webmPath = path.join(OUT_DIR, webms[0]);
console.log(`[4] Convertendo ${webmPath} → MP4 via ffmpeg...`);

execSync(`ffmpeg -y -i "${webmPath}" -c:v libx264 -pix_fmt yuv420p -crf 18 "${MP4_OUT}"`, { stdio: 'inherit' });

console.log(`\n[OK] Video salvo em: ${MP4_OUT}`);
