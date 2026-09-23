# ADR-006 — Backtesting Architecture

## Status

Aceito

## Contexto

O WINQuantLab possui uma camada de estratégias responsável por analisar
dados de mercado e produzir eventos por meio da coluna `signal`.

A convenção inicial definida pela arquitetura de estratégias é:

- `1` representa um evento de compra.
- `0` representa ausência de novo evento.
- `-1` representa um evento de venda.

As estratégias são responsáveis pela interpretação dos dados de mercado,
enquanto a execução e a mensuração das operações devem permanecer separadas
dessa lógica.

Com a introdução da camada de Backtesting, torna-se necessário definir como
os sinais serão transformados em operações observáveis sem introduzir
lookahead bias e sem acoplar o motor às regras específicas de cada
estratégia.

Além do resultado entre entrada e saída, o WINQuantLab deverá permitir a
análise do comportamento do preço durante toda a vida de uma operação.

O objetivo principal do Backtesting não é definir regras de gerenciamento
de risco para o usuário, mas fornecer dados quantitativos sobre o
comportamento histórico das estratégias.

## Decisão

Será mantida uma camada de Backtesting independente das estratégias.

O Backtesting Engine receberá um DataFrame contendo dados de mercado e os
eventos produzidos previamente por uma Strategy.

A Strategy determina os eventos operacionais.

O Backtesting Engine determina como esses eventos são executados e mede o
comportamento do preço durante a vida da operação.

Camadas posteriores poderão agregar e apresentar estatísticas sobre os
trades produzidos pelo Backtesting Engine.

O fluxo conceitual será:

```text
Market Data
    ↓
Indicators
    ↓
Strategy
    ↓
Signals
    ↓
Backtesting
    ↓
Trades
    ↓
Analytics
    ↓
User Decision
