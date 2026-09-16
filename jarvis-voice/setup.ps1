# setup.ps1 — Instalação do Jarvis Voice no Windows
# TTS: Edge TTS PT-BR (Microsoft neural, grátis, sem API key)
# STT: FasterWhisper (local, grátis)
# LLM: Claude via ANTHROPIC_API_KEY (único serviço pago)

Write-Host "`n=== Jarvis Voice Setup (Edge TTS PT-BR) ===" -ForegroundColor Cyan

# 1. Verificar uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[+] Instalando uv..." -ForegroundColor Yellow
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
}

# 2. OpenJarvis com extras de voz e inferência cloud (Claude)
Write-Host "[+] Instalando OpenJarvis [inference-cloud, speech]..." -ForegroundColor Yellow
uv pip install "openjarvis[inference-cloud,speech]"

# 3. FasterWhisper — STT local PT-BR
Write-Host "[+] Instalando FasterWhisper (STT local)..." -ForegroundColor Yellow
uv pip install faster-whisper

# 4. Edge TTS — TTS PT-BR gratuito (Microsoft neural voices)
Write-Host "[+] Instalando edge-tts (TTS PT-BR gratuito)..." -ForegroundColor Yellow
uv pip install edge-tts

# 5. Criar .env se não existir
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "`n[!] Arquivo .env criado. Preencha sua chave:" -ForegroundColor Red
    Write-Host "    ANTHROPIC_API_KEY  <- obrigatório (único serviço pago)"
}

Write-Host "`n=== Setup concluído! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar (sempre use start.py — registra o Edge TTS antes do jarvis):"
Write-Host "  python start.py              # GUI + voz simultâneos (recomendado)"
Write-Host "  python start.py --chat       # CLI interativo com voz"
Write-Host "  python start.py --voice      # só voz contínua"
Write-Host "  python start.py --text-only  # sem TTS (debug)"
Write-Host ""
Write-Host "Vozes PT-BR disponíveis (edite recipe.toml → voice_id):"
Write-Host "  pt-BR-AntonioNeural            (masculino, padrão)"
Write-Host "  pt-BR-FranciscaNeural          (feminino)"
Write-Host "  pt-BR-ThalitaNeural            (feminino, jovem)"
Write-Host "  pt-BR-MacerioMultilingualNeural (masculino multilíngue)"
