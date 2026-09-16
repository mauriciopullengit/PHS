import asyncio, edge_tts

async def main():
    voices = await edge_tts.list_voices()
    pt_br = [v for v in voices if v['Locale'].startswith('pt-BR')]
    for v in pt_br:
        print(f"{v['ShortName']:<45} {v['Gender']}")

asyncio.run(main())
