---
title: Métodos de Predição de Manobrabilidade
tags:
  - belchior
  - manobrabilidade
  - predicao
  - modelo
sources:
  - MSC.1-Circ.1053.pdf
updated: '2026-05-13'
---
# Métodos de Predição de Manobrabilidade

Métodos para prever a manobrabilidade de um navio na fase de projeto, conforme [[MSC-Circ-1053]] Cap. 3.

## Os Três Métodos (seção 3.1)

### 1. Dados de Experiência e Navios Similares
O mais simples. Assume que o novo navio terá características próximas às de navios existentes similares.
Menor custo, menor precisão.

### 2. Ensaios em Modelo Reduzido (*Model Tests*)
Considerado o **método mais confiável** na época da publicação.

Dois tipos:
- **Modelo livre (*free-running*):** executa as manobras padrão em escala reduzida — resultados diretos
- **Modelo cativo (*captive model*):** modelo forçado em movimentos específicos para medir forças hidrodinâmicas → coeficientes para modelo matemático

#### Instalações para modelo livre
- Bacias de manobra offshore
- Tanques de reboque convencionais (largura suficiente para zig-zag 10°/10°)
- Lagos (ao ar livre — dependente de condições climáticas)

#### PMM — Planar Motion Mechanism
Dispositivo de modelo cativo que combina modos de deriva e guinada (estáticos e oscilatórios).
Permite testes em tanques de reboque convencionais (longos e estreitos).
Origem: testes de submarinos em plano vertical.

#### Rotating Arm (*Braço Rotativo*)
Bacia circular com braço do centro à circunferência. O modelo percorre círculos de diâmetros variados.
Determina coeficientes de guinada e combinação de guinada + deriva.

### 3. Modelo Matemático (*Mathematical Model*)
Conjunto de equações que descrevem a dinâmica do navio em manobra.

Dois tipos de modelo matemático:
- **Modelo de resposta (*response model*):** relaciona entrada (leme) com saída (movimento) diretamente
- **Modelo de forças hidrodinâmicas (*hydrodynamic force model*):** baseado nas forças hidrodinâmicas e interferências mútuas — permite estimar variações por mudança de forma ou condição de carga

## Condição dos Ensaios

Os padrões se aplicam à **plena carga**. Navios que fazem provas em lastro devem extraporar os resultados para plena carga por modelo ou simulação — ver [[correcao-condicoes-nao-padrao]].

## Efeito de Escala (*Scale Effects*)

- Modelos livres sofrem efeitos de escala (modelo mais estável que o navio real)
- Modelos grandes → menores efeitos de escala
- Modelos cativos permitem correções mais fáceis

## Fluxo de Predição por Modelo Matemático

```
Dimensões e planos do navio
    ↓
Estimação dos coeficientes hidrodinâmicos
(dados históricos / PMM / cálculo teórico / fórmulas semi-empíricas)
    ↓
Equações do movimento
    ↓
Simulação numérica das manobras padrão
    ↓
Comparação com os critérios IMO → verificação
```

## Ver também

- [[condicoes-prova-manobrabilidade]]
- [[correcao-condicoes-nao-padrao]]
- [[criterios-manobrabilidade-imo]]
- [[MSC-Circ-1053]]
