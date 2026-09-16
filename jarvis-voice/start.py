"""
start.py — Inicializa Jarvis Voice com Edge TTS PT-BR registrado.

Uso:
  python start.py              # GUI + voz (modo serve, porta 8000)
  python start.py --chat       # CLI interativo com voz
  python start.py --voice      # só voz contínua, sem GUI
  python start.py --text-only  # sem TTS (debug)
"""

import sys
import os
from pathlib import Path

# ── 1. Carregar .env ─────────────────────────────────────────────────────────
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

# ── 2. Registrar backend Edge TTS antes do OpenJarvis inicializar ─────────────
try:
    from edge_tts_backend import register_edge_tts_backend
    register_edge_tts_backend()
    print("[jarvis] Edge TTS PT-BR registrado com sucesso.")
except Exception as e:
    print(f"[AVISO] Edge TTS não pôde ser registrado: {e}")
    print("        Instale: pip install edge-tts")

# ── 3. Determinar modo de execução ────────────────────────────────────────────
recipe = Path(__file__).parent / "recipe.toml"
args = sys.argv[1:]
mode = "serve"  # padrão: GUI + voz simultâneos

if "--chat" in args:
    mode = "chat"
elif "--voice" in args:
    mode = "voice"
elif "--text-only" in args:
    mode = "chat"
    os.environ["JARVIS_NO_TTS"] = "1"

# ── 4. Iniciar OpenJarvis ─────────────────────────────────────────────────────
print(f"[jarvis] Iniciando modo '{mode}' com recipe: {recipe}")
print(f"[jarvis] GUI disponível em: http://localhost:8000 (se modo serve)")
print(f"[jarvis] Voz: Edge TTS PT-BR (pt-BR-FranciscaNeural) | STT: FasterWhisper\n")

try:
    from openjarvis.cli import main as jarvis_main
    sys.argv = ["jarvis", mode, "--recipe", str(recipe)]
    jarvis_main()
except ImportError:
    print("[ERRO] OpenJarvis não instalado. Execute: .\\setup.ps1")
    sys.exit(1)
