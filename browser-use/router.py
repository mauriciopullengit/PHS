"""
Hybrid Browser Router — três modos de automação no mesmo Chrome.

Regra de roteamento:
  --harness   → browser-harness (CDP direto, LLM gera código Python)  ← RECOMENDADO
  --scripted  → agent-browser   (Rust, sem LLM, steps determinísticos)
  (padrão)    → browser-use     (LLM autônomo via biblioteca Python)

Usage:
    # Harness — linguagem natural, execução via CDP direto:
    uv run router.py --harness "vá para google.com e me diga o título"

    # Autônomo (LLM via browser-use):
    uv run router.py "encontre o menor preço de passagem SP→RJ"

    # Steps determinísticos (sem LLM):
    uv run router.py --scripted "open https://google.com | type @e12 python | click @e16"

    # Conectando ao Chrome compartilhado:
    uv run router.py --cdp "va para google.com e me diga o titulo"
    uv run router.py --scripted --cdp "open https://google.com | snapshot"
"""
import asyncio
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

CDP_PORT = 9222
CDP_URL  = f"http://localhost:{CDP_PORT}"


# ── agent-browser (scripted) ──────────────────────────────────────────────────

def run_scripted(steps: str, use_cdp: bool = False) -> int:
    """
    Executa steps via agent-browser CLI.
    Steps separados por '|' são executados em sequência.

    Exemplos de steps:
      open https://google.com
      snapshot
      click @e12
      type @e12 python | press Enter
    """
    cmds = [s.strip() for s in steps.split("|")]

    if use_cdp:
        connect_result = subprocess.run(
            ["agent-browser", "connect", str(CDP_PORT)],
            capture_output=True, text=True
        )
        if connect_result.returncode != 0:
            print(f"[router] Aviso: CDP connect retornou {connect_result.returncode}")
            print(connect_result.stderr)

    for cmd in cmds:
        parts = cmd.split()
        result = subprocess.run(["agent-browser"] + parts, capture_output=False)
        if result.returncode != 0:
            print(f"[router] Step falhou: {cmd}")
            return result.returncode

    return 0


# ── browser-use (autônomo) ────────────────────────────────────────────────────

async def run_autonomous(task: str, use_cdp: bool = False, use_sonnet: bool = False) -> str:
    """Delega para agent.py com os defaults token-efficient."""
    from agent import run
    cdp_url = CDP_URL if use_cdp else None
    return await run(task, use_sonnet=use_sonnet, cdp_url=cdp_url)


# ── snapshot helper ───────────────────────────────────────────────────────────

def snapshot(use_cdp: bool = False) -> str:
    """Retorna snapshot da página atual via agent-browser (rápido, sem LLM)."""
    if use_cdp:
        subprocess.run(["agent-browser", "connect", str(CDP_PORT)], capture_output=True)
    result = subprocess.run(["agent-browser", "snapshot"], capture_output=True, text=True)
    return result.stdout


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    scripted   = "--scripted"  in args
    use_harness = "--harness"  in args
    use_cdp    = "--cdp"       in args
    use_sonnet = "--sonnet"    in args

    args = [a for a in args if a not in ("--scripted", "--harness", "--cdp", "--sonnet")]
    task = " ".join(args) if args else ""

    if not task:
        print("Uso: uv run router.py [--harness|--scripted] [--cdp] [--sonnet] '<tarefa ou steps>'")
        sys.exit(1)

    if use_harness:
        print(f"[router] Modo: browser-harness (CDP direto)")
        print(f"[router] Tarefa: {task}\n")
        from harness_nl import run as harness_run
        sys.exit(harness_run(task))
    elif scripted:
        print(f"[router] Modo: agent-browser (scripted) | CDP: {use_cdp}")
        print(f"[router] Steps: {task}\n")
        code = run_scripted(task, use_cdp=use_cdp)
        sys.exit(code)
    else:
        model = "Sonnet" if use_sonnet else "Groq/Haiku"
        print(f"[router] Modo: browser-use (autônomo) | Modelo: {model} | CDP: {use_cdp}")
        print(f"[router] Tarefa: {task}\n")
        result = asyncio.run(run_autonomous(task, use_cdp=use_cdp, use_sonnet=use_sonnet))
        print(f"\n[router] Resultado: {result}")
