# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Glossary

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# Objetivo

Este documento reúne os principais termos técnicos utilizados pelo WINQuantLab.

Seu objetivo é padronizar conceitos, facilitar a leitura da documentação e evitar interpretações diferentes para um mesmo termo.

Os conceitos aqui descritos representam o significado adotado dentro deste projeto.

---

# A

## Analytics

Camada responsável pelo cálculo de métricas estatísticas produzidas durante o backtesting.

Exemplos:

- Profit Factor
- Drawdown
- Sharpe
- Sortino
- Expectancy

---

## API Pública

Conjunto de funções, classes e módulos destinados ao uso pelos usuários da biblioteca.

Mudanças na API pública devem preservar compatibilidade sempre que possível.

---

## ATR (Average True Range)

Indicador de volatilidade desenvolvido por J. Welles Wilder.

Mede a amplitude média das movimentações de preço.

---

# B

## Backtesting

Processo de executar uma estratégia utilizando dados históricos para avaliar seu comportamento antes da utilização em ambiente real.

---

## Break Even

Movimentação do Stop Loss para o preço de entrada da operação após determinadas condições serem atendidas.

---

# C

## Candle

Representação gráfica da movimentação de preços durante um período de tempo.

Cada candle é composto por:

- Open
- High
- Low
- Close

---

## CSV

Formato de arquivo utilizado para armazenamento tabular de dados.

É o formato padrão utilizado pelo WINQuantLab para importação de dados históricos.

---

# D

## DataFrame

Estrutura de dados do Pandas utilizada para armazenar séries históricas.

É a estrutura padrão utilizada em toda a biblioteca.

---

## DI+

Directional Indicator Positive.

Indicador utilizado pelo sistema DMI.

---

## DI-

Directional Indicator Negative.

Indicador utilizado pelo sistema DMI.

---

## Drawdown

Redução do patrimônio a partir de um pico anterior.

Uma das principais métricas utilizadas na avaliação de estratégias.

---

# E

## EMA

Exponential Moving Average.

Média móvel exponencial.

Atribui maior peso aos preços mais recentes.

---

## Expectancy

Valor esperado por operação.

Representa o retorno médio esperado considerando ganhos e perdas.

---

# G

## Grid Search

Método utilizado para testar automaticamente diferentes combinações de parâmetros.

---

# H

## HMA

Hull Moving Average.

Média móvel desenvolvida para reduzir atraso mantendo suavização.

---

# I

## Indicador

Ferramenta matemática utilizada para extrair informações do comportamento dos preços.

Indicadores não geram decisões automaticamente.

Eles fornecem informações que podem ser utilizadas por estratégias.

---

# M

## MACD

Moving Average Convergence Divergence.

Indicador de momentum baseado na diferença entre duas médias móveis exponenciais.

---

## Momentum

Indicador que mede a velocidade da movimentação dos preços.

---

# O

## OHLC

Sigla para:

- Open
- High
- Low
- Close

Representa os quatro preços fundamentais de um candle.

---

## OBV

On Balance Volume.

Indicador baseado na acumulação do volume.

---

# P

## Payoff

Relação entre ganho médio e perda média.

---

## Profit Factor

Relação entre lucro bruto e prejuízo bruto.

Uma das principais métricas utilizadas na avaliação de estratégias.

---

## Pullback

Movimento temporário contrário à tendência principal.

Frequentemente utilizado como ponto de entrada.

---

# R

## Refatoração

Processo de melhorar a estrutura interna do código sem alterar seu comportamento externo.

---

## Reports

Camada responsável pela geração e exportação de relatórios.

---

## RSI

Relative Strength Index.

Indicador de momentum desenvolvido por J. Welles Wilder.

---

# S

## Sharpe Ratio

Métrica utilizada para avaliar retorno ajustado ao risco.

---

## Slippage

Diferença entre o preço esperado e o preço efetivamente executado.

---

## SMA

Simple Moving Average.

Média móvel simples.

---

## Sortino Ratio

Métrica semelhante ao Sharpe, porém considera apenas volatilidade negativa.

---

## Strategy

Conjunto de regras responsáveis por definir entradas, saídas e gerenciamento de operações.

---

## SuperTrend

Indicador de tendência baseado no ATR.

---

# T

## TDD

Test Driven Development.

Metodologia baseada no ciclo:

- RED
- GREEN
- REFACTOR

---

## Timeframe

Intervalo de tempo utilizado na construção dos candles.

Exemplos:

- 1 minuto
- 5 minutos
- 15 minutos
- 60 minutos
- Diário

---

## Trailing Stop

Stop Loss móvel que acompanha a evolução favorável do preço.

---

## Trend

Família de indicadores responsáveis por identificar tendência de mercado.

---

# V

## Validator

Módulo responsável por validar dados antes de seu processamento.

---

## Visualization

Camada responsável pela apresentação gráfica dos resultados.

---

## Volatility

Família de indicadores utilizada para medir volatilidade do mercado.

---

## VWAP

Volume Weighted Average Price.

Preço médio ponderado pelo volume.

---

## VWMA

Volume Weighted Moving Average.

Média móvel ponderada pelo volume.

---

# W

## Weis Wave

Indicador baseado na acumulação de volume em ondas de mercado.

---

## Wilder Average

Método de suavização desenvolvido por J. Welles Wilder.

É utilizado em indicadores como RSI, ATR e ADX.

---

## WMA

Weighted Moving Average.

Média móvel ponderada.

---

# Evolução

Novos termos deverão ser adicionados sempre que surgirem novos conceitos durante o desenvolvimento do WINQuantLab.

Este glossário deve permanecer como a referência oficial de terminologia da biblioteca.
