"""
Gera MP4 demo: audio Francisca + video reator em modo Speaking.
Usa ffprobe para medir duração do audio, grava video pelo mesmo tempo.
"""
import asyncio, edge_tts, subprocess, os, sys

AUDIO_OUT = r"C:\Users\mau\Projetos\jarvis-voice\francisca-demo.mp3"
VIDEO_TMP  = r"C:\Users\mau\Projetos\jarvis-voice\video-tmp\reactor-speaking.webm"
MP4_FINAL  = r"C:\Users\mau\Projetos\jarvis-voice\jarvis-voice-demo.mp4"
PAGE_URL   = "http://localhost:8765/arc-reactor-demo.html"

# ── 1. Gerar audio mais longo ─────────────────────────────────
TEXT = (
    "Olá. Sou Francisca, a voz do sistema Jarvis. "
    "Todos os sistemas estão operando normalmente. "
    "O reator de arco está ativo e respondendo à minha modulação de voz em tempo real. "
    "Cada sílaba que pronuncio gera uma variação no campo energético do núcleo. "
    "Os anéis orbitais aceleram conforme a frequência da minha voz aumenta. "
    "Aguardo seus comandos."
)

async def gen_audio():
    c = edge_tts.Communicate(TEXT, "pt-BR-FranciscaNeural", rate="+5%")
    data = b""
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            data += chunk["data"]
    with open(AUDIO_OUT, "wb") as f:
        f.write(data)
    print(f"[1] Audio gerado: {len(data)} bytes -> {AUDIO_OUT}")

asyncio.run(gen_audio())

# ── 2. Medir duração do audio ─────────────────────────────────
probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", AUDIO_OUT],
    capture_output=True, text=True
)
duration = float(probe.stdout.strip())
print(f"[2] Duracao do audio: {duration:.2f}s")

# ── 3. Gravar reator em modo Speaking pelo tempo exato ────────
record_script = f"""
import {{ chromium }} from 'playwright';
import {{ execSync }} from 'child_process';
import path from 'path';
import fs from 'fs';

const OUT_DIR = 'C:/Users/mau/Projetos/jarvis-voice/video-tmp';
const WEBM    = 'C:/Users/mau/Projetos/jarvis-voice/video-tmp/reactor-speaking.webm';
const DUR_MS  = {int(duration * 1000)};

fs.mkdirSync(OUT_DIR, {{ recursive: true }});

const browser = await chromium.launch({{ headless: true }});
const context = await browser.newContext({{
  viewport: {{ width: 860, height: 860 }},
  recordVideo: {{ dir: OUT_DIR, size: {{ width: 860, height: 860 }} }},
}});
const page = await context.newPage();
await page.goto('{PAGE_URL}', {{ waitUntil: 'networkidle' }});

// Activa modo Speaking imediatamente
await page.click('button:has-text("Falando")');
await page.waitForTimeout(DUR_MS + 500);

await context.close();
await browser.close();

// Renomear webm gerado
const files = fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.webm'));
if (files.length) {{
  const src = path.join(OUT_DIR, files[files.length-1]);
  fs.renameSync(src, WEBM);
  console.log('[ok] Video gravado: ' + WEBM);
}} else {{
  console.error('[erro] Nenhum webm encontrado');
  process.exit(1);
}}
"""

script_path = r"C:\Users\mau\Projetos\jarvis-voice\_record_speaking.mjs"
with open(script_path, "w") as f:
    f.write(record_script)

print(f"[3] Gravando video por {duration:.1f}s...")
subprocess.run(["node", script_path], check=True)

# ── 4. Combinar video + audio com ffmpeg ─────────────────────
print("[4] Combinando video + audio...")
subprocess.run([
    "ffmpeg", "-y",
    "-i", VIDEO_TMP,
    "-i", AUDIO_OUT,
    "-c:v", "libx264",
    "-c:a", "aac",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-shortest",
    MP4_FINAL
], check=True)

print(f"\n[OK] Demo final: {MP4_FINAL}")
os.startfile(MP4_FINAL)
