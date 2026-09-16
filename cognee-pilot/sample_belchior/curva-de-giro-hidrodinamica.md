---
title: Curva de Giro — Teoria Hidrodinâmica
tags: [belchior, manobrabilidade, giro, hidrodinamica]
sources: [A MANOBRABILIDADE DO NAVIO NO SÉCULO 21.pdf]
updated: 2026-05-14
---

# Curva de Giro — Teoria Hidrodinâmica

> Santos, E. M. — *A Manobrabilidade do Navio no Século 21*, Cap. 6
> (Complementa [[circulo-de-evolucao]] — baseado em MSC.137(76))

## Definições (Cap. 6.1)

| Grandeza | Definição |
|---|---|
| **Avanço** | Distância percorrida na direção original ao completar 90° de guinada |
| **Transferência** | Distância perpendicular ao rumo original ao completar 90° |
| **Diâmetro tático** | Distância máxima perpendicular ao rumo original (ponto em 180°) |
| **Diâmetro de giro estacionário** | Diâmetro do círculo de giro em regime |
| **Ponto pivô** | Ponto de rotação instantâneo — desloca-se para a proa na 1ª fase |

![[pna3-fig20-trajetoria-giro-avanco-transferencia.png]]
![[pna3-fig21-3-fases-transientes-giro.png]]
![[pna3-fig24-adernamento-tempo-giro-boreste.png]]
![[pna3-fig25-reducao-velocidade-diametro-giro.png]]
![[manob21-fig123-perda-velocidade-guinada-VLCC.png]]

## Três fases do giro

```
Fase 1: v=0, r=0 → v≠0, r≠0, v̇≠0, ṙ≠0   (deflexão inicial do leme)
Fase 2: v≠0, r≠0, v̇≠0, ṙ≠0               (transitória — curva acelerada)
Fase 3: v≠0, r≠0, v̇=0, ṙ=0               (regime estacionário)
```

Na fase 3 (regime): equilíbrio entre força do leme, força hidrodinâmica do casco e inércia → raio constante R.

## Raio de giro (teoria linear)

Para navios estáveis com δ pequeno:
```
L/R = δ · [Nδ'·Yv' - Yδ'·Nv'] / [(Yr'-Δ')·Nv' - Nr'·Yv']
```
- **R ∝ L** (comprimento do navio)
- **R ∝ 1/δ** (inversamente proporcional ao ângulo de leme)
- Navios mercantes: diâmetro tático típico = **2 a 4L** com leme a toda

### Validade:
Teoria linear só é precisa para diâmetros ≥ 4L e δ abaixo do máximo. Navios instáveis não podem ser analisados com essa fórmula.

## Adernamento durante o giro

**Fase 1 (inicial):** aderna para o lado **contrário** ao giro — força do leme empurra a popa para fora.  
**Fases 2 e 3:** aderna para o lado do **giro** — força centrífuga supera o momento do leme.

**Momento de adernamento (fase estável):**
```
MA ≈ Y_δ·δ·y₁ - (Y_v·v + Y_r·r)·y₂ - F_inercia·y₃
```

**Ângulo de adernamento (PIANC):**
```
θ = V²·B_M / (g·R·GM)
```
- Aumenta com: velocidade, boca (B_M), raio pequeno
- Diminui com: GM (estabilidade transversal)

## Efeito da variação das derivadas no raio de giro

| Derivada | Efeito em R (navios estáveis com leme grande) |
|---|---|
| ↑ Y'v | Diminui R (navios de guerra, rebocadores) |
| ↑ N'v | Se negativo → diminui R; contribui para estabilidade |
| ↑ N'r | Mais negativo → aumenta R (amortecimento) |

**Navios em lastro:** razão L/T aumenta → Y'v diminui → potencial desestabilizador → maior R.

## Influência da redução de velocidade no diâmetro tático

Durante o giro a velocidade cai tipicamente 30–40% para navios mercantes. A redução da velocidade aumenta o efeito relativo do leme, mas diminui as forças de sustentação do casco.

## Critérios IMO para a curva de giro

**MSC.137(76) [[circulo-de-evolucao]]:**
- Avanço ≤ 4,5L
- Diâmetro tático ≤ 5L

---

*Relacionado:* [[circulo-de-evolucao]] | [[criterios-manobrabilidade-imo]] | [[estabilidade-movimento-navio]] | [[asa-casco-derivadas-hidrodinamicas]]
