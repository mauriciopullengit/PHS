import asyncio, edge_tts, os, time, subprocess

VOICES = [
    ("pt-PT-DuarteNeural",  "Masculino PT-PT -- Duarte (sotaque europeu)"),
    ("pt-PT-RaquelNeural",  "Feminino  PT-PT -- Raquel (sotaque europeu)"),
]

TEXT = "Ola. Sou o Jarvis, seu assistente pessoal. Como posso ajuda-lo hoje?"
OUT_DIR = r"C:\Users\mau\Projetos\jarvis-voice"

async def main():
    print("\n=== Vozes PT-PT (sotaque europeu) ===\n")
    for voice, label in VOICES:
        path = os.path.join(OUT_DIR, f"voz-{voice}.mp3")
        print(f"[{label}]")
        c = edge_tts.Communicate(TEXT, voice, rate="+5%")
        await c.save(path)
        print(f"  Gerando... OK ({os.path.getsize(path)} bytes)")
        print(f"  Tocando...")
        subprocess.Popen(["start", "", path], shell=True)
        time.sleep(5)
        print()

asyncio.run(main())
print("Fim.")
