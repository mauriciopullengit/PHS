# Playright Skill Guide

## Objetivo
Ter um atalho claro para o fluxo Playwright no workspace. Este guia é apenas para o projeto Playwright — o projeto PowerShell é separado.
- MCP total via `@playwright/mcp`
- CLI rápido via `npx playwright`

## Comandos disponíveis

### MCP Playwright
- `npm run playright:mcp`
- Inicia o servidor Playwright MCP com configuração mínima de logs.

### CLI rápido
- `npm run Playright`
- `npm run playright:test`
- `npm run playright:codegen`
- `npm run playright:open`

## Uso recomendado

- Use `npm run Playright` para o comando base do Playwright CLI.
- Use `npm run playright:mcp` quando quiser automação total via MCP.
- Use `npm run playright:test` para rodar testes Playwright.
- Use `npm run playright:codegen` quando precisar gerar código de automação.
- Use `npm run playright:open` para abrir URLs com Playwright.

## Como executar no VS Code
1. Abra o terminal integrado.
2. Digite `npm run Playright` ou `npm run playright:mcp`.
3. Para tarefas rápidas, use `Terminal > Run Task` e escolha `Playright: ...`.

## Nota
O alias `Playright` foi adicionado propositalmente com `P` maiúsculo para combinar com o nome da skill que você pediu.
