---
title: Teste Zig-Zag (Z-manoeuvre)
tags:
  - belchior
  - manobrabilidade
  - manobras
  - zig-zag
sources:
  - MSC.137(76).pdf
updated: '2026-05-13'
---
# Teste Zig-Zag (Z-manoeuvre)

Manobra padrão definida pela [[MSC-137-76]], seção 4.2.5–4.2.9.
Avalia a **capacidade de correção de guinada** (*yaw-checking*) e **manutenção de rumo** (*course-keeping*).

![[msc1053-fig3-zigzag-10-10.png]]
![[manob21-fig76-77-curva-zigzag.png]]
![[manob21-fig79-80-zigzag-aproamento.png]]

## Conceito

Aplicação alternada de leme para ambos os bordos em resposta a desvios de rumo predefinidos.

## Procedimento — Teste 10°/10°

1. **1ª execução:** após aproximação estabilizada (taxa de guinada nula), aplicar **10° de leme** a BB ou BE
2. Quando o rumo desviar **10°** do rumo original → **2ª execução:** inverter o leme para 10° no bordo oposto
3. O navio continuará girando no sentido original (com taxa decrescente) e começará a girar no sentido inverso. Quando atingir **10°** no lado oposto → **3ª execução:** inverter novamente o leme

## Grandezas medidas

| Grandeza | Definição |
|----------|-----------|
| **1° ângulo de ultrapassagem** (*1st overshoot angle*) | Desvio de rumo adicional após a **2ª execução** |
| **2° ângulo de ultrapassagem** (*2nd overshoot angle*) | Desvio de rumo adicional após a **3ª execução** |

## Variantes

| Teste | Leme | Desvio de rumo |
|-------|------|----------------|
| **10°/10°** | 10° | 10° |
| **20°/20°** | 20° | 20° |

## Critérios IMO — Teste 10°/10° (seção 5.3.3)

### 1° Ângulo de Ultrapassagem

| L/V | Limite máximo |
|-----|--------------|
| < 10 s | **10°** |
| ≥ 30 s | **20°** |
| 10 s ≤ L/V < 30 s | **(5 + L/V / 2)°** |

### 2° Ângulo de Ultrapassagem

| L/V | Limite máximo |
|-----|--------------|
| < 10 s | **25°** |
| ≥ 30 s | **40°** |
| 10 s ≤ L/V < 30 s | **(17,5 + 0,75 · L/V)°** |

### Teste 20°/20°
- 1° ângulo de ultrapassagem ≤ **25°**

> L em metros, V em m/s. Navios lentos e grandes têm limites mais permissivos por sua maior inércia.

## Ver também

- [[circulo-de-evolucao]]
- [[teste-parada-atras]]
- [[criterios-manobrabilidade-imo]]
- [[geometria-navio-definicoes]]
