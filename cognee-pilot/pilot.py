"""
Piloto Cognee 100% local (Ollama) sobre amostra do Projeto Belchior.
Objetivo: medir se o recall via knowledge graph com modelo GRATUITO local
responde perguntas que exigem CONECTAR varias notas (o ponto forte de um grafo
vs. RAG simples). Zero custo de API.
"""
import asyncio, glob, os, time, sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

import cognee
from cognee import SearchType

SAMPLE = str(Path(__file__).parent / "sample_belchior")

# Perguntas escolhidas para EXIGIR conexao entre notas distintas:
PERGUNTAS = [
    "Quais sao os criterios de manobrabilidade exigidos pela IMO e quais testes "
    "especificos avaliam cada criterio?",
    "Qual a diferenca entre a curva de giro (circulo de evolucao) e o teste de "
    "zig-zag, e o que cada um mede sobre o navio?",
    "Como as condicoes de prova (calado, velocidade, aguas profundas) afetam os "
    "resultados dos testes de manobrabilidade?",
]

def sep(t): print("\n" + "="*70 + f"\n{t}\n" + "="*70)

async def main():
    # 1) reset limpo
    try:
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)
    except Exception as e:
        print("[reset] aviso:", e)

    # 2) ingestao
    arquivos = sorted(glob.glob(os.path.join(SAMPLE, "*.md")))
    sep(f"INGESTAO — {len(arquivos)} notas de manobrabilidade")
    for a in arquivos: print("  +", os.path.basename(a))
    t0 = time.time()
    await cognee.add(arquivos)
    print(f"[add] concluido em {time.time()-t0:.1f}s")

    # 3) construcao do grafo (entity extraction via mistral local — passo lento)
    sep("COGNIFY — construindo knowledge graph com mistral local")
    t0 = time.time()
    await cognee.cognify()
    print(f"[cognify] grafo construido em {time.time()-t0:.1f}s")

    # 4) consultas que exigem raciocinio sobre o grafo
    for i, q in enumerate(PERGUNTAS, 1):
        sep(f"PERGUNTA {i}: {q}")
        t0 = time.time()
        res = await cognee.search(query_text=q, query_type=SearchType.GRAPH_COMPLETION)
        dt = time.time()-t0
        if isinstance(res, list):
            for r in res: print(getattr(r, "text", r) if not isinstance(r, str) else r)
        else:
            print(res)
        print(f"\n[tempo: {dt:.1f}s]")

if __name__ == "__main__":
    asyncio.run(main())
