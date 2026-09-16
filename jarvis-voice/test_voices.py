import asyncio, edge_tts, os, time, subprocess

VOICES = [
    ("pt-BR-AntonioNeural",              "Masculino — Antonio"),
    ("pt-BR-ThalitaMultilingualNeural",  "Feminino  — Thalita (multilingual)"),
    ("pt-BR-FranciscaNeural",            "Feminino  — Francisca"),
]

TEXT = "Olá. Sou o Jarvis, seu assistente pessoal. Como posso ajudá-lo hoje?"
OUT_DIR = r"C:\Users\mauri\Projetos\jarvis-voice"

async def generate(voice, path):
    c = edge_tts.Communicate(TEXT, voice, rate="+5%")
    await c.save(path)

async def main():
    print("\n=== Teste de Vozes PT-BR ===\n")
    for voice, label in VOICES:
        path = os.path.join(OUT_DIR, f"voz-{voice}.mp3")
        print(f"[{label}]")
        print(f"  Gerando...", end=" ", flush=True)
        await generate(voice, path)
        print(f"OK ({os.path.getsize(path)} bytes)")
        print(f"  Tocando: {voice}")
        subprocess.Popen(["start", "", path], shell=True)
        time.sleep(4)
        print()

asyncio.run(main())
print("=== Fim do teste ===")
print("Edite recipe.toml → voice_id para escolher a voz preferida.")
