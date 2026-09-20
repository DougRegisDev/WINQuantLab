# ADR-005 — Strategy Architecture

## Status

Accepted

## Context

WINQuantLab separates market data processing, indicators, strategies,
backtesting, and reporting into independent layers.

With the introduction of the first trading strategy, a common contract
is required to define the responsibilities of the strategy layer.

A strategy may depend on one or more technical indicators, but it
should not reimplement indicator calculations or be responsible for
trade execution, position management, or performance calculation.

## Decision

Strategies receive a normalized market DataFrame as input.

Each strategy is responsible for orchestrating the indicators required
by its own trading logic by calling the existing implementations from
the `indicators` package.

Strategies must not duplicate indicator calculations.

The strategy returns a copy of the market DataFrame containing the
calculated data required by the strategy and a `signal` column.

The signal convention is:

- `1` — buy signal
- `0` — no new signal
- `-1` — sell signal

A signal represents an event, not a position.

For example, after a buy signal is generated, subsequent candles must
return `0` unless another signal event occurs. Maintaining an open
position is not the responsibility of the strategy layer.

Strategies must not modify the original DataFrame supplied by the
caller.

Strategy-specific parameter relationships are validated by the
strategy. Validation that belongs to an indicator remains the
responsibility of that indicator.

## Signal Timing

Strategies generate signals using only information available up to the
current candle.

A strategy does not execute trades.

Execution timing, including whether a signal generated at candle close
is executed at the next available price, belongs to the backtesting
layer.

This separation is intended to prevent strategy logic from being
coupled to execution assumptions and to reduce the risk of lookahead
bias.

## First Implementation

The first implementation of this contract is the Moving Average
Crossover strategy.

It uses two Simple Moving Averages:

- fast moving average
- slow moving average

A buy signal is generated only when the fast moving average crosses
from below or equal to above the slow moving average.

A sell signal is generated only when the fast moving average crosses
from above or equal to below the slow moving average.

Remaining above or below the slow moving average does not generate
additional signals.

The fast period must be smaller than the slow period.

## Consequences

This architecture keeps responsibilities separated:

```text
Market Data
    ↓
Indicators
    ↓
Strategies
    ↓
Signals
    ↓
Backtesting
    ↓
Reports
