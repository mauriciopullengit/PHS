# PowerShell Hybrid Setup

Este documento descreve apenas o projeto PowerShell. O projeto Playwright é separado e está documentado em `PLAYWRIGHT-SETUP.md`.

Este repositório inclui um fluxo PowerShell: CLI nativo para automação direta e um servidor MCP para automação total via Claude Code / VS Code.

## Como funciona

- Use `pwsh` como CLI principal para comandos imediatos e scripts simples.
- Use `mcp-powershell-exec` para registro de servidor MCP e execução de automação comandada por agentes.
- Mantenha o CLI leve e reserve o MCP para tarefas que exigem contexto de sessão ou integração com o modelo.

## Instalação

```bash
npm install --save-dev mcp-powershell-exec@^1.0.4
```

## Scripts npm

- `npm run powershell:cli`
  - Abre `pwsh` interativo.
- `npm run powershell:run -- "<PowerShell command>"`
  - Executa um comando PowerShell inline.
- `npm run powershell:script`
  - Executa o script de exemplo `powershell/example.ps1`.
- `npm run powershell:mcp`
  - Inicia o servidor MCP `mcp-powershell-exec`.

## VS Code Tasks

- `PowerShell: Start MCP server`
- `PowerShell: Run sample script`

## Claude Code / .claude.json

Adicione o servidor PowerShell ao `.claude.json`:

```json
{
  "mcpServers": {
    "powershell": {
      "type": "stdio",
      "command": "npx",
      "args": ["mcp-powershell-exec"]
    }
  }
}
```

## Uso

### Rodar um comando inline

```bash
npm run powershell:run -- "Write-Output 'hello from PowerShell'"
```

### Rodar o script de exemplo

```bash
npm run powershell:script
```

### Iniciar MCP para agentes

```bash
npm run powershell:mcp
```

## Recomendação

- Use o CLI `pwsh` como padrão para desenvolvimento e depuração rápida.
- Use `mcp-powershell-exec` quando precisar de automação guiada por agente ou de uma sessão PowerShell persistente.
