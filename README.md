# Projetos — Playwright Hybrid Setup

Este repositório contém utilitários e configuração para um fluxo híbrido Playwright (CLI + MCP).

## Resumo
Use a CLI (`npx playwright`) como padrão para desenvolvimento, geração de código e CI; reserve o MCP (`@playwright/mcp`) para agentes que precisam de sessões persistentes e introspecção.

## Comandos rápidos
```bash
# instalar navegadores
npx playwright install

# rodar todos os testes
npm run playwright:test

# gerar código interativo
npm run playwright:codegen https://example.com

# abrir URL no navegador
npm run playwright:open https://example.com

# capturar screenshot
npm run playwright:screenshot https://example.com example.png -- --browser=chromium

# iniciar MCP server localmente
npx @playwright/mcp@latest --browser chrome
```

## VS Code
Use as Tasks (Command Palette → Run Task):
- `Playwright: Install Browsers`
- `Playwright: Start MCP server`
- `Playwright: Run tests` (default test task)
- `Playwright: Codegen`
- `Playwright: Screenshot Example`

## CI (GitHub Actions)
Workflow: `.github/workflows/playwright.yml` instala navegadores e executa os testes automaticamente em pushes e pull requests.

## Recomendações
- Configure `.claude.json` por projeto (já presente) para registrar o MCP localmente.
- Para CI: use `npx playwright install --with-deps` antes de rodar os testes.

---

Arquivo adicional: `PLAYWRIGHT-README.md` contém instruções rápidas específicas do Playwright.
