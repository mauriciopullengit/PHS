---
title: Manobra Espiral e Pull-Out
tags:
  - belchior
  - manobrabilidade
  - manobras
  - estabilidade
sources:
  - MSC.1-Circ.1053.pdf
updated: '2026-05-13'
---
# Manobra Espiral e Pull-Out

Manobras adicionais para avaliação de [[estabilidade-dinamica-navio]], conforme [[MSC-Circ-1053]] Apêndice 4.
Usadas quando os testes padrão ([[teste-zig-zag]], [[circulo-de-evolucao]]) indicam instabilidade dinâmica.

---

![[msc1053-fig-A4-2-espiral-navio-estavel.png]]
![[msc1053-fig-A4-3-espiral-navio-instavel.png]]
![[manob21-fig64-66-espiral-dieudonne.png]]
![[manob21-fig67-68-resultados-espiral.png]]

## 1. Espiral Direta (*Direct Spiral Manoeuvre*)

**Objetivo:** Obter a relação taxa de guinada / ângulo de leme em regime permanente (a curva espiral completa).

**Procedimento:**
1. Aproximação estabilizada
2. Aplicar leme ~15° e manter até taxa de guinada constante por ~1 min
3. Reduzir o leme em incrementos de ~5° — a cada passo, aguardar regime permanente
4. Repetir para BB e BE, de grandes ângulos a zero

**Limitação:** Muito demorado, especialmente para navios grandes e lentos. Sensível a condições ambientais.

---

## 2. Espiral Reversa (*Reverse Spiral Manoeuvre*)

**Objetivo:** Obter a mesma curva mais rapidamente, incluindo o ramo instável.

**Procedimento:** O navio é governado para manter uma taxa de guinada constante; mede-se o ângulo de leme médio necessário para produzir essa taxa.

**Requisito:** Indicador de taxa de guinada calibrado + indicador de ângulo de leme preciso.

---

## 3. Espiral Simplificada (*Simplified Spiral*)

Reduz o teste a **3 pontos** medidos ao final do círculo de evolução:

1. Taxa de guinada em ângulo de leme máximo
2. Taxa de guinada com leme ao centro → se → 0: navio estável (encerrar)
3. Aplicar leme oposto igual a **metade da largura de loop admissível**:
   - Se o navio continua girando no sentido oposto ao leme → instável além do limite

**Largura de loop admissível:**

| L/V | Loop máximo |
|-----|-------------|
| < 9 s | 0° |
| 9 s ≤ L/V ≤ 45 s | −3 + (L/V)/3 graus |
| > 45 s | 12° |

---

![[msc1053-fig-A4-1-pull-out-test.png]]

## 4. Pull-Out Manoeuvre

**Objetivo:** Indicação simples da estabilidade dinâmica em linha reta.

**Procedimento:** Ao final do círculo de evolução, o leme é retornado ao centro e mantido até que a taxa de guinada se estabilize.

**Interpretação:**
- Taxa de guinada → **zero**: navio estável
- Taxa de guinada → **valor residual** (em ambos os bordos): navio instável — a magnitude indica o grau de instabilidade

---

## 5. VSZZ — Very Small Zig-Zag (0°/5°)

Variação do zig-zag que simula o comportamento de um navio sendo governado em linha reta.
Executa ~20 ultrapassagens (vs. 2–3 no teste padrão). Avalia o ângulo de ultrapassagem em regime de longo prazo.

---

## Relação com os testes padrão

```
Indicação de instabilidade no zig-zag 10°/10°
    ↓
Espiral simplificada (rápida, ao final do círculo)
    ↓
Se confirmado → Espiral direta ou reversa (análise detalhada)
    ↓
Pull-out (quantifica o grau de instabilidade)
```

## Ver também

- [[estabilidade-dinamica-navio]]
- [[teste-zig-zag]]
- [[circulo-de-evolucao]]
- [[MSC-Circ-1053]]
