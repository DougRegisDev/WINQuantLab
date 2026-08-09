# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Roadmap

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# Objetivo

Este documento apresenta o plano de evolução do WINQuantLab até a versão estável 1.0.

O roadmap é organizado em fases de desenvolvimento. Cada fase representa um conjunto de funcionalidades relacionadas e somente será considerada concluída após atender aos critérios de qualidade definidos pelo projeto.

---

# Status Atual

| Fase | Status |
|------|--------|
| Foundation | ✅ Concluída |
| Moving Average | ✅ Concluída |
| Momentum | ✅ Concluída |
| Trend | ⏳ Planejada |
| Volume | ⏳ Planejada |
| Volatility | ⏳ Planejada |
| Strategies | ⏳ Planejada |
| Backtesting | ⏳ Planejada |
| Analytics | ⏳ Planejada |
| Reports | ⏳ Planejada |
| Visualization | ⏳ Planejada |
| Release 1.0 | ⏳ Planejada |

---

# Fase 1 — Foundation

## Dados

- [x] CSV Loader
- [x] Validator
- [x] Normalizer
- [x] Column Mapping

## Infraestrutura

- [x] Estrutura inicial do projeto
- [x] Configuração do Ruff
- [x] Pytest
- [x] Tipagem estática
- [x] Documentação inicial

---

# Fase 2 — Moving Average

## Indicadores

- [x] SMA
- [x] EMA
- [x] WMA
- [x] HMA

## Base matemática

- [x] Cálculos reutilizáveis
- [x] Validações compartilhadas

---

# Fase 3 — Momentum

## Indicadores

- [x] RSI
- [x] MACD
- [x] Momentum
- [x] ROC
- [x] Stochastic

## Base matemática

- [x] Wilder Average
- [x] Price Changes
- [x] Previous Values
- [x] Rolling Max
- [x] Rolling Min

---

# Fase 4 — Trend

## Indicadores

- [ ] ATR
- [ ] DI+
- [ ] DI-
- [ ] ADX
- [ ] SuperTrend

## Base matemática

- [ ] True Range
- [ ] Directional Movement
- [ ] Directional Index
- [ ] Average True Range

---

# Fase 5 — Volume

## Indicadores

- [ ] VWAP
- [ ] VWMA
- [ ] On Balance Volume (OBV)
- [ ] Volume Financeiro
- [ ] Weis Wave

## Base matemática

- [ ] Volume acumulado
- [ ] Preço médio ponderado
- [ ] Acumulação de volume

---

# Fase 6 — Volatility

## Indicadores

- [ ] Bollinger Bands
- [ ] Keltner Channel
- [ ] Donchian Channel

## Base matemática

- [ ] Desvio padrão
- [ ] Bandas
- [ ] Canais

---

# Fase 7 — Strategies

## Estrutura

- [ ] Framework de estratégias
- [ ] Sinais de entrada
- [ ] Sinais de saída
- [ ] Gerenciamento de posição

## Estratégias

- [ ] Cruzamento de Médias
- [ ] Pullback
- [ ] Rompimento
- [ ] VWAP
- [ ] ADX
- [ ] Price Action
- [ ] Multi-Timeframe

---

# Fase 8 — Backtesting

## Motor

- [ ] Simulação candle a candle
- [ ] Long
- [ ] Short

## Operações

- [ ] Stop Loss
- [ ] Take Profit
- [ ] Break Even
- [ ] Trailing Stop

## Custos

- [ ] Slippage
- [ ] Comissão
- [ ] Emolumentos

---

# Fase 9 — Analytics

## Métricas

- [ ] Lucro Líquido
- [ ] Lucro Bruto
- [ ] Prejuízo Bruto
- [ ] Win Rate
- [ ] Loss Rate
- [ ] Profit Factor
- [ ] Payoff
- [ ] Drawdown
- [ ] Drawdown Máximo
- [ ] Sharpe
- [ ] Sortino
- [ ] Expectancy
- [ ] Média Gain
- [ ] Média Loss

---

# Fase 10 — Reports

## Exportação

- [ ] CSV
- [ ] Excel
- [ ] PDF
- [ ] HTML

## Relatórios

- [ ] Relatório resumido
- [ ] Relatório completo
- [ ] Comparação entre estratégias

---

# Fase 11 — Visualization

## Gráficos

- [ ] Equity Curve
- [ ] Drawdown
- [ ] Distribuição dos resultados
- [ ] Heatmaps
- [ ] Comparação entre estratégias

---

# Fase 12 — Release 1.0

A versão 1.0 será considerada concluída quando:

- [ ] Todas as fases anteriores estiverem concluídas.
- [ ] Todos os testes automatizados estiverem aprovados.
- [ ] Documentação completa.
- [ ] Ruff sem erros.
- [ ] APIs públicas estáveis.
- [ ] Publicação do projeto no GitHub.

---

# Critérios de Qualidade

Cada fase somente poderá ser considerada concluída quando:

- Código implementado.
- Testes automatizados aprovados.
- Ruff sem erros.
- Tipagem completa.
- Docstrings atualizadas.
- Documentação revisada.
- APIs públicas estáveis.

---

# Evolução

Este roadmap representa a visão planejada para a versão 1.0.

Novas funcionalidades poderão ser avaliadas durante o desenvolvimento, porém somente serão incorporadas à versão 1.0 caso estejam alinhadas ao documento **Product Vision**.

Caso contrário, serão planejadas para versões futuras.
