# ADR-006 — Backtesting Architecture

## Status

Aceito

## Contexto

O WINQuantLab possui uma camada de estratégias responsável por analisar
dados de mercado e produzir eventos por meio da coluna `signal`.

A convenção definida pela arquitetura de estratégias é:

- `1` representa um evento de compra.
- `0` representa ausência de novo evento.
- `-1` representa um evento de venda.

As estratégias são responsáveis pela interpretação dos dados de mercado,
enquanto a execução das operações deve permanecer separada dessa lógica.

Com a introdução da camada de Backtesting, torna-se necessário definir como
os sinais serão transformados em operações simuladas sem introduzir
lookahead bias e sem acoplar o motor de execução às regras específicas de
cada estratégia.

## Decisão

Será criada uma camada de Backtesting independente das estratégias.

O Backtesting Engine receberá um DataFrame contendo dados de mercado e a
coluna `signal`, produzida previamente por uma Strategy.

### Execução dos sinais

Um sinal identificado no fechamento do candle `N` será executado na abertura
do candle `N+1`.

Exemplo:

```text
Candle N
close
signal = 1
    ↓
Candle N+1
open
    ↓
entrada LONG
