# Projetos — Playwright e PowerShell são projetos diferentes

Este repositório agrupa dois projetos distintos de automação:
- `Playwright`: automação de navegador com Playwright CLI e MCP
- `PowerShell`: automação de shell com PowerShell CLI e MCP

## Resumo
Cada fluxo é separado. Use Playwright para navegador e PowerShell para shell, com CLI como opção preferida de baixo custo e MCP apenas quando precisar de agentes e sessões persistentes.

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
Workflow: `.github/workflows/powershell.yml` executa o script PowerShell de exemplo em Windows.

## PowerShell project
Este fluxo é separado do Playwright. Use `pwsh` para PowerShell CLI e `mcp-powershell-exec` para automação total via MCP.

### Comandos rápidos
```bash
# iniciar PowerShell MCP server localmente
npx mcp-powershell-exec

# rodar comando em linha
npm run powershell:run -- "Write-Output 'hello from PowerShell'"

# rodar script de exemplo
npm run powershell:script

# abrir PowerShell interativo
npm run powershell:cli
```

### VS Code
Use as Tasks:
- `PowerShell: Start MCP server`
- `PowerShell: Run sample script`

### Recomendações
- Configure `.claude.json` por projeto para registrar o MCP localmente.
- Use `pwsh` como CLI padrão; reserve `mcp-powershell-exec` para agentes que precisam de sessões persistentes.
- Para CI: use `npx playwright install --with-deps` antes de rodar os testes.
- `POWERSHELL-SETUP.md` contém instruções rápidas específicas do PowerShell.

---

Projetos separados:
- `PLAYWRIGHT-SETUP.md` — guia do Playwright
- `POWERSHELL-SETUP.md` — guia do PowerShell

Arquivo adicional: `PLAYWRIGHT-README.md` contém instruções rápidas específicas do Playwright.
