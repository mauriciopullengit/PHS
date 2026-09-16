"""
Lança Chrome com CDP na porta 9222 para compartilhar com:
  - Playwright MCP  (@playwright/mcp --cdp-endpoint http://localhost:9222)
  - browser-use     (BrowserProfile(cdp_url="http://localhost:9222"))

Usage:
    uv run launch_chrome.py
    python launch_chrome.py
"""
import os
import subprocess
import sys

CDP_PORT = 9222
CDP_URL  = f"http://localhost:{CDP_PORT}"

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\mauri\AppData\Local\Google\Chrome\Application\chrome.exe",
]


def find_chrome() -> str | None:
    return next((p for p in CHROME_PATHS if os.path.exists(p)), None)


def launch():
    chrome = find_chrome()
    if not chrome:
        print("Chrome nao encontrado nos paths padrao.")
        print("Defina CHROME_PATH=<caminho> e tente novamente.")
        sys.exit(1)

    proc = subprocess.Popen([
        chrome,
        f"--remote-debugging-port={CDP_PORT}",
        "--no-first-run",
        "--no-default-browser-check",
    ])

    print(f"Chrome iniciado (PID {proc.pid})")
    print(f"CDP disponivel em: {CDP_URL}")
    print()
    print("Para usar com Playwright MCP, atualize settings.json:")
    print(f'  "--cdp-endpoint", "{CDP_URL}"')
    print()
    print("Para usar com browser-use:")
    print(f'  uv run agent.py --cdp "{CDP_URL}" "sua tarefa"')


if __name__ == "__main__":
    launch()
