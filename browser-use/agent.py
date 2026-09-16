"""
Browser-use wrapper — token-efficient, multi-provider.

Providers suportados (configurar via .env):
  GOOGLE_API_KEY   → Gemini (grátis via AI Studio)
  ANTHROPIC_API_KEY → Claude (pago)

Usage:
    uv run agent.py "pesquise o preço do bitcoin"
    uv run agent.py --sonnet "tarefa complexa"          (Claude Sonnet se tiver crédito)
    uv run agent.py --cdp "http://localhost:9222" "..."  (browser compartilhado)
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile

load_dotenv(Path(__file__).parent / ".env")

# Modelos Groq (gratuitos)
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Modelos Gemini (gratuitos via AI Studio)
GEMINI_FLASH = "gemini-2.0-flash"

# Modelos Claude (pagos)
CLAUDE_HAIKU  = "claude-haiku-4-5-20251001"
CLAUDE_SONNET = "claude-sonnet-4-6"


def _make_llm(use_sonnet: bool = False):
    """Escolhe provider: Groq (grátis) → Gemini → Claude (pago)."""
    groq_key      = os.getenv("GROQ_API_KEY")
    google_key    = os.getenv("GOOGLE_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if groq_key:
        from browser_use.llm.groq.chat import ChatGroq
        print(f"Provider: Groq ({GROQ_MODEL})")
        return ChatGroq(
            model=GROQ_MODEL,
            api_key=groq_key,
            temperature=0.0,
        )

    if google_key:
        from browser_use.llm.google import ChatGoogle
        print(f"Provider: Google Gemini ({GEMINI_FLASH})")
        return ChatGoogle(model=GEMINI_FLASH, api_key=google_key, temperature=0.0)

    if anthropic_key:
        from browser_use.llm import ChatAnthropic
        model = CLAUDE_SONNET if use_sonnet else CLAUDE_HAIKU
        print(f"Provider: Anthropic Claude ({model})")
        return ChatAnthropic(model=model, api_key=anthropic_key, max_tokens=4096)

    raise EnvironmentError(
        "Nenhuma API key encontrada. Configure GROQ_API_KEY, GOOGLE_API_KEY ou ANTHROPIC_API_KEY no .env"
    )


async def run(
    task: str,
    *,
    use_sonnet: bool = False,
    cdp_url: str | None = None,
    max_steps: int = 15,
) -> str:
    """
    Executa tarefa de browser com defaults token-efficient:
    - use_vision=False  → sem screenshots (~70% menos tokens)
    - max_steps cap     → não roda indefinidamente
    - cdp_url           → conecta a Chrome já aberto (compartilha com Playwright MCP)
    """
    llm = _make_llm(use_sonnet)

    profile = BrowserProfile(
        cdp_url=cdp_url if cdp_url else None,
        headless=False,
        keep_alive=bool(cdp_url),
    )

    agent = Agent(
        task=task,
        llm=llm,
        browser_profile=profile,
        use_vision=False,
        max_actions_per_step=5,
    )

    result = await agent.run(max_steps=max_steps)
    return result.final_result() or "Tarefa concluída sem resultado textual."


if __name__ == "__main__":
    args = sys.argv[1:]
    use_sonnet = "--sonnet" in args
    cdp_url = None

    if "--cdp" in args:
        idx = args.index("--cdp")
        cdp_url = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    args = [a for a in args if a != "--sonnet"]
    task = " ".join(args) if args else "Vá para google.com e diga o título da página."

    print(f"vision: OFF | CDP: {cdp_url or 'próprio'}")
    print(f"Tarefa: {task}\n")

    result = asyncio.run(run(task, use_sonnet=use_sonnet, cdp_url=cdp_url))
    print("\nResultado:", result)
