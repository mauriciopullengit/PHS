Playwright hybrid workflow

Resumo
- Recomendação: usar CLI para desenvolvimento/testes/CI e MCP (`@playwright/mcp`) para agentes que precisam de sessões persistentes e introspecção.

Comandos úteis

```bash
# instalar navegadores
npx playwright install

# rodar testes (Playwright Test)
npm run playwright:test

# gerar código interativo
npm run playwright:codegen https://example.com

# abrir URL no navegador
npm run playwright:open https://example.com

# capturar screenshot
npm run playwright:screenshot https://example.com example.png -- --browser=chromium

# iniciar MCP server (local)
npx @playwright/mcp@latest --browser chrome
```

VS Code
- Use as Tasks (Command Palette → Run Task):
  - `Playwright: Install Browsers`
  - `Playwright: Start MCP server`
  - `Playwright: Run tests` (default test task)
  - `Playwright: Codegen`
  - `Playwright: Screenshot Example`

Arquivo `package.json` (scripts relevantes)
- `playwright:install`, `playwright:cli`, `playwright:mcp`, `playwright:test`, `playwright:codegen`, `playwright:open`, `playwright:screenshot`

Sugestões
- CI: adicione `npx playwright install --with-deps` no job de setup.
- Para agentes com orçamento de tokens: prefira invocar `npx playwright` via CLI-Skill invés de MCP quando possível.
