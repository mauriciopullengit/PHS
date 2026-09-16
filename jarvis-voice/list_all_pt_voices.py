import asyncio, edge_tts

async def main():
    voices = await edge_tts.list_voices()
    pt = [v for v in voices if v['Locale'].startswith('pt')]
    print(f"\nTotal de vozes PT encontradas: {len(pt)}\n")
    for v in sorted(pt, key=lambda x: x['ShortName']):
        print(f"  {v['ShortName']:<50} {v['Gender']:<8} {v['Locale']}")

asyncio.run(main())
