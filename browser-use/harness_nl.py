"""
Linguagem natural → browser-harness.

Traduz a tarefa para código Python e executa via browser-harness (CDP).
Auto-inicia Chrome se não estiver rodando na porta 9222/9223.

Usage:
    uv run harness_nl.py "vá para google.com e me diga o título"
    uv run harness_nl.py --no-launch "tarefa" (não tenta abrir Chrome)
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

SYSTEM_PROMPT = """You are a browser automation code generator. Convert the user's natural language task into Python code that uses browser-harness helpers.

Available helpers (pre-imported, no need to import):
- new_tab(url)               — open URL in new tab (prefer over goto_url)
- goto_url(url)              — navigate current tab
- wait_for_load(timeout=15)  — wait for page to finish loading
- page_info()                — returns dict with title, url, text content
- click_at_xy(x, y)          — click at coordinates
- fill_input(selector, text) — fill an input field (CSS selector)
- type_text(text)            — type text at current focus
- press_key(key)             — press a key (e.g. "Return", "Tab", "Escape")
- scroll(x, y, dy=-300)      — scroll at position
- capture_screenshot(path)   — save screenshot to path
- list_tabs()                — list open tabs
- switch_tab(target)         — switch to tab by index or url substring
- close_tab()                — close current tab
- wait(seconds)              — sleep
- wait_for_element(selector, timeout=10) — wait for CSS selector
- js(expression)             — evaluate JavaScript in page
- http_get(url)              — fetch URL without browser (returns text)
- ensure_real_tab()          — ensure we have a real browser tab

Rules:
- Return ONLY executable Python code. No markdown, no backticks, no explanations.
- Use new_tab() for first navigation (not goto_url), to avoid clobbering user's tabs.
- Always call wait_for_load() after navigation.
- Use print() to return results to the user.
- For search tasks: new_tab("https://google.com"), wait_for_load(), fill_input('textarea[name="q"]', query), press_key("Return"), wait_for_load(), print(page_info())
"""


def _chrome_running() -> bool:
    for port in (9222, 9223):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=0.5).close()
            return True
        except OSError:
            pass
    return False


CDP_PROFILE = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "chrome-harness-profile")


def _launch_chrome() -> bool:
    """
    Lança Chrome com CDP na porta 9222.
    Usa --user-data-dir isolado para funcionar mesmo com Chrome já aberto.
    """
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\mau\AppData\Local\Google\Chrome\Application\chrome.exe",
    ]
    chrome = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not chrome:
        print("[harness] Chrome não encontrado. Instale o Chrome e tente novamente.", flush=True)
        return False

    print("[harness] Iniciando Chrome CDP (perfil isolado)...", flush=True)
    subprocess.Popen([
        chrome,
        "--remote-debugging-port=9222",
        f"--user-data-dir={CDP_PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
    ])

    for _ in range(30):
        time.sleep(0.5)
        if _chrome_running():
            print("[harness] Chrome pronto.", flush=True)
            return True

    print("[harness] Timeout aguardando Chrome. Tente novamente.", flush=True)
    return False


def _strip_fences(code: str) -> str:
    """Remove markdown code fences (```python ... ```) se o LLM os incluir."""
    lines = code.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1).close()
        return True
    except OSError:
        return False


def _load_personal_data() -> str:
    path = Path(__file__).parent / "personal_data.json"
    if not path.exists():
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    return f"\n\nDados pessoais do usuário (use quando a tarefa pedir preenchimento de formulários):\n{json.dumps(data, ensure_ascii=False, indent=2)}"


def _generate_code(task: str) -> str:
    """Usa o melhor LLM disponível para gerar código browser-harness."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key    = os.getenv("GOOGLE_API_KEY")
    groq_key      = os.getenv("GROQ_API_KEY")
    ollama_model  = os.getenv("OLLAMA_MODEL", "mistral")

    personal_ctx = _load_personal_data()

    if _ollama_running():
        payload = json.dumps({
            "model": ollama_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + personal_ctx},
                {"role": "user", "content": task},
            ],
            "stream": False,
            "options": {"temperature": 0},
        }).encode()
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        print(f"[harness] Gerando com Ollama ({ollama_model}) — pode levar ~40s no CPU...", flush=True)
        resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
        return _strip_fences(resp["message"]["content"].strip())

    if anthropic_key:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": task}],
        )
        return resp.content[0].text.strip()

    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import HumanMessage, SystemMessage
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_key, temperature=0)
            resp = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=task)])
            return resp.content.strip()
        except Exception:
            pass

    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            resp = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": task},
                ],
                temperature=0.0,
                max_tokens=1024,
            )
            return resp.choices[0].message.content.strip()
        except ImportError:
            pass

    raise EnvironmentError(
        "Nenhuma API key encontrada. Configure ANTHROPIC_API_KEY, GOOGLE_API_KEY ou GROQ_API_KEY no .env"
    )


def run(task: str, auto_launch: bool = True) -> int:
    if auto_launch and not _chrome_running():
        if not _launch_chrome():
            print("[harness] Erro: Chrome não encontrado. Abra o Chrome manualmente e tente novamente.")
            return 1

    print(f"[harness] Gerando código para: {task}", flush=True)
    code = _generate_code(task)
    print(f"[harness] Executando:\n{'-'*40}\n{code}\n{'-'*40}", flush=True)

    env = os.environ.copy()
    for port in (9222, 9223):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=0.5).close()
            env["BU_CDP_URL"] = f"http://127.0.0.1:{port}"
            break
        except OSError:
            pass

    result = subprocess.run(
        ["browser-harness"],
        input=code,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.returncode


if __name__ == "__main__":
    args = sys.argv[1:]
    auto_launch = "--no-launch" not in args
    args = [a for a in args if a != "--no-launch"]

    if not args:
        print("Uso: uv run harness_nl.py [--no-launch] '<tarefa em linguagem natural>'")
        sys.exit(1)

    task = " ".join(args)
    sys.exit(run(task, auto_launch=auto_launch))
