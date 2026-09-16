---
name: Stoic Imperium
colors:
  primary: "#0d0c0b"
  on-primary: "#f0ead6"
  accent: "#c9a84c"
  surface: "#1a1814"
  muted: "rgba(240, 234, 214, 0.45)"
typography:
  headline:
    fontFamily: Fraunces
    fontSize: 120px
    fontWeight: 700
    letterSpacing: -0.02em
  display:
    fontFamily: Fraunces
    fontSize: 148px
    fontWeight: 900
    letterSpacing: -0.03em
  label:
    fontFamily: Space Mono
    fontSize: 20px
    fontWeight: 400
    letterSpacing: 0.28em
    textTransform: uppercase
  body:
    fontFamily: Spectral
    fontSize: 56px
    fontWeight: 400
    fontStyle: italic
    lineHeight: 1.5
rounded:
  none: 0px
spacing:
  sm: 16px
  md: 28px
  lg: 60px
motion:
  energy: calm
  easing:
    entry: "sine.out"
    exit: "power1.in"
    ambient: "sine.inOut"
  duration:
    entrance: 1.1
    hold: 3.5
    transition: 1.4
  atmosphere:
    - radial-gold-glow
    - ghost-type-bleed
    - hairline-gold-rules
  transition: blur-crossfade-calm
---

## Overview

Stoic Imperium é um estilo editorial cinematic-dark inspirado nos manuscritos romanos e no design de títulos de documentários de arte. A paleta é quase monocromática — preto quente, creme de pergaminho, ouro romano — com uma única cor de acento que nunca compete com o texto. Nada é decorativo por acidente; cada elemento estrutural ganha seu espaço.

## Colors

- **#0d0c0b** — fundo principal. Preto levemente amarronzado, não técnico. Evita o azul-gelo de fundo genérico.
- **#f0ead6** — texto principal. Creme de pergaminho, não branco puro. Reduz harshness na tela escura.
- **#c9a84c** — ouro romano. Acento único. Linhas estruturais, labels, detalhes de metadados.
- **rgba(240, 234, 214, 0.45)** — texto secundário/muted. Usa sempre via opacity, não uma cor separada.
- **#1a1814** — surface. Para fundos de cenas alternadas (levemente mais quente que o primary).

## Typography

**Fraunces** — headline e display. Serif óptico variável com personalidade literária. Aparece em 700 para títulos e 900 para displays grandes. O eixo óptico cria uma sensação manuscrita em tamanhos grandes.

**Space Mono** — labels e metadados. Monospaced cria tensão direta com o serif — máquina de escrever vs. manuscrito romano. Sempre em uppercase, letter-spacing largo. Recede; nunca performa.

**Spectral** — corpo de citações. Serif bookish, mais leve que Fraunces. Usado em itálico para dar à citação uma voz diferente dos títulos institucionais.

## Elevation

Flat + glow atmosférico. Sem sombras de caixa. Profundidade vem de:
- Radial gradient glow dourado centrado no elemento focal
- Ghost type em enorme escala, opacidade 5-8%, sangrando para fora do frame
- Texto principal em z-index acima de todos os decorativos

## Do's and Don'ts

**Faça:**
- Use ouro apenas em elementos estruturais e labels — nunca em texto hero
- Ghost type sempre sangra fora do frame (overflow: visible, mas clipped pelo overflow: hidden do .scene)
- Regras horizontais e verticais animadas com scaleX/scaleY do ponto de origem correto
- Eases lentos em todas as entradas (sine.out, expo.out) — nunca bounce, nunca elastic

**Não faça:**
- Sem bordas ou cards com border-radius — zero arredondamento no modo Stoic Imperium
- Sem branco puro (#ffffff) — sempre use #f0ead6
- Sem azuis, verdes, rosas ou qualquer acento além do ouro
- Sem box-shadow — glows são radial-gradient, não sombras
- Sem uppercase no texto hero — apenas em labels Space Mono
