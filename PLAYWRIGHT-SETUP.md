# Playwright MCP + CLI Setup

## Objetivo
Ter dois modos de automação:
- `@playwright/mcp` para automação total via MCP
- Playwright CLI + scripts rápidos para uso econômico e comandos diretos

## Configuração já aplicada
### 1) MCP via VS Code / Claude Code
Em `.vscode/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser",
        "chrome",
        "--console-level",
        "warning"
      ]
    }
  }
}
```

### 2) Scripts CLI rápidos em `package.json`

```json
"scripts": {
  "playright:mcp": "npx @playwright/mcp@latest --browser chrome --console-level warning",
  "playright:cli": "npx playwright",
  "playright:test": "npx playwright test",
  "playright:codegen": "npx playwright codegen",
  "playright:open": "npx playwright open"
}
```

### 3) Tarefas VS Code em `.vscode/tasks.json`

- `Playright: Start MCP server`
- `Playright: Run tests`
- `Playright: Codegen`
- `Playright: Open URL`

## Como usar

### Usar `@playwright/mcp`
- Iniciar servidor MCP:

```bash
npm run playright:mcp
```

- Use este servidor no Claude Code/VS Code como MCP server.

### Usar Playwright CLI + SKILLs
- Executar comandos rápidos:

```bash
npm run playright:test
npm run playright:codegen
npm run playright:open
```

- No VS Code, abra a paleta e execute `Tasks: Run Task`.

## Quando usar cada opção

- `@playwright/mcp`:
  - navegação interativa complexa
  - automação exploratória
  - manter estado de browser entre comandos

- Playwright CLI + SKILLs:
  - tarefas mais diretas e repetitivas
  - testes rápidos
  - reduzir overhead de token

## Dica rápida
Use MCP para sessões de navegador longas ou automação guiada.
Use CLI quando precisar de execução simples e menor custo de contexto.
