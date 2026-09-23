# ADR-006 — Backtesting Architecture

## Status

Accepted

## Context

WINQuantLab separates strategy logic from trade execution and analysis.

Strategies receive normalized market data, use indicators when necessary,
and produce trading events through the `signal` column:

- `1` represents a buy event.
- `0` represents no new event.
- `-1` represents a sell event.

A strategy describes what happened according to its own rules. It must not
execute trades, calculate position state, or define risk management.

Backtesting must transform those events into trades without lookahead bias
and measure what happened to price while each trade was active.

The objective is analytical measurement, not automatic trading decisions.

The conceptual flow is:

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
Trades
    ↓
Analytics
    ↓
User Decision
```

## Decision

Backtesting will remain independent from strategy implementation.

The engine receives a DataFrame containing market data and strategy signals.

The engine is responsible for:

- executing strategy events according to defined execution rules;
- maintaining position state;
- creating completed trade records;
- calculating trade result;
- measuring price behavior while a trade is active.

The engine must not decide:

- whether a strategy is good or bad;
- where a stop loss should be placed;
- where a take profit should be placed;
- acceptable risk;
- position sizing;
- capital allocation.

Those decisions belong outside the analytical core.

## Signal execution

A signal identified at the close of candle `N` is executed at the `open`
of candle `N+1`.

```text
Candle N
signal
   ↓
Candle N+1
open
   ↓
execution
```

This prevents execution using information that was not available before the
signal candle closed.

A signal on the final candle cannot generate a new trade because no next
candle exists for execution.

## Position states

The initial engine supports:

```text
FLAT
LONG
SHORT
```

When FLAT:

- `signal = 1` opens LONG at the next candle open.
- `signal = -1` opens SHORT at the next candle open.
- `signal = 0` does nothing.

When LONG:

- `signal = 1` is ignored.
- `signal = 0` maintains the position.
- `signal = -1` closes LONG at the next candle open.

When SHORT:

- `signal = -1` is ignored.
- `signal = 0` maintains the position.
- `signal = 1` closes SHORT at the next candle open.

An opposite signal closes the current position but does not automatically
reverse it.

A new strategy event is required to open another position.

## Quantity

The initial engine uses:

```text
quantity = 1
```

Multiple positions and pyramiding are outside the initial scope.

## Trade result

Trade result is measured in price points.

For LONG:

```text
pnl_points = exit_price - entry_price
```

For SHORT:

```text
pnl_points = entry_price - exit_price
```

An open position remaining at the end of the available data is force-closed
using the `close` of the final candle.

## Analytical philosophy

The central analytical question is:

> What happened to price after the strategy generated an entry and while
> the resulting trade remained active?

The engine should measure historical behavior rather than prescribe trading
decisions.

For example:

```text
entry_price = 180000
favorable_price = 187500
adverse_price = 179800
exit_price = 180700

mfe_points = +7500
mae_points = -200
pnl_points = +700
```

These values describe what happened.

They do not imply that a stop should be 200 points or that a target should
be 7500 points.

## Maximum Favorable Excursion

Maximum Favorable Excursion (`MFE`) measures the greatest favorable movement
observed while a trade was active.

For LONG:

```text
mfe_points = highest high - entry_price
```

For SHORT:

```text
mfe_points = entry_price - lowest low
```

MFE is represented as a positive value or zero.

The corresponding extreme price is stored as:

```text
favorable_price
```

The candle where that extreme occurred may be stored as:

```text
mfe_index
```

## Maximum Adverse Excursion

Maximum Adverse Excursion (`MAE`) measures the greatest adverse movement
observed while a trade was active.

For LONG:

```text
mae_points = lowest low - entry_price
```

For SHORT:

```text
mae_points = entry_price - highest high
```

MAE is represented as a negative value or zero.

The corresponding extreme price is stored as:

```text
adverse_price
```

The candle where that extreme occurred may be stored as:

```text
mae_index
```

## Observation window

Excursions must only use market data from the period during which the
position was actually active.

If a signal occurs at candle `N` and the position opens at the `open` of
candle `N+1`, the `high` and `low` of candle `N` are not included.

The entry candle is included because the position becomes active at its
`open`.

Example:

```text
Candle 10    Candle 11    Candle 12    Candle 13    Candle 14    Candle 15
signal -1      OPEN                                      signal +1      OPEN
                 |<------------ active trade ------------->|          exit
```

For this trade:

- candle 10 is excluded;
- candles 11 through 14 are included;
- candle 15 `open` is the exit price;
- candle 15 `high` and `low` are excluded.

This is necessary because price movement occurring after the exit must not
affect MFE or MAE.

## Forced final close

When a position remains open until the final candle of the available data,
the engine closes it using that candle's `close`.

In this situation, the final candle's `high` and `low` are included in the
excursion calculation because the position remained active throughout that
candle until its close.

Therefore, the observation window differs depending on the exit type:

```text
normal next-open exit
→ exclude high/low of exit candle

forced final-close exit
→ include high/low of final candle
```

## OHLC limitation

OHLC data provides the open, high, low, and close of a candle but does not
necessarily reveal the sequence in which the high and low occurred.

If both a favorable and an adverse extreme occur inside the same candle,
WINQuantLab must not infer which occurred first.

Questions that depend on intrabar sequence require finer-grained market data.

## Trade outcome

Final trade outcome and price excursions represent different information.

Outcome is determined exclusively from `pnl_points`:

```text
pnl_points > 0  → win
pnl_points < 0  → loss
pnl_points == 0 → even
```

MFE and MAE must not determine whether a trade is classified as a win or
loss.

For example:

```text
mfe_points = +900
mae_points = -100
pnl_points = -50
outcome = loss
```

This trade moved significantly in the favorable direction but eventually
closed at a loss.

Another losing trade could behave very differently:

```text
mfe_points = +100
mae_points = -700
pnl_points = -600
outcome = loss
```

Both trades are losses, but their price behavior is substantially different.

Preserving this distinction is a primary analytical objective of
WINQuantLab.

## Trade record

The existing trade record contains:

```text
direction
entry_index
entry_price
exit_index
exit_price
quantity
pnl_points
```

When a `DatetimeIndex` is available, the engine may also preserve:

```text
entry_time
exit_time
```

The analytical evolution of the trade record may add:

```text
favorable_price
adverse_price
mfe_points
mae_points
mfe_index
mae_index
duration_candles
outcome
```

The DataFrame remains the source of the complete candle trajectory.

The trade record does not need to duplicate every candle between entry and
exit.

## Strategy exit semantics

The current strategies use opposite signals as exit events.

For example:

```text
SHORT
    ↓
signal = 1
    ↓
exit SHORT at next open
```

The architecture must not assume that all future strategies will use this
mechanism.

Future strategies may define explicit exit conditions independently from
entry signals.

Backtesting should execute those events without taking responsibility for
the strategy logic that produced them.

## Analytics

Aggregate statistics belong to an analytical layer built from completed
trade records.

Possible analyses include:

- total trades;
- winning trades;
- losing trades;
- even trades;
- average and median MFE;
- average and median MAE;
- MFE and MAE distributions;
- percentiles;
- trade duration;
- statistics separated by outcome;
- time-based behavior;
- comparison between strategies.

This makes analyses such as the following possible:

```text
Strategy X
500 trades

WIN
280 trades
average MFE: ...
average MAE: ...

LOSS
205 trades
average MFE: ...
average MAE: ...

EVEN
15 trades
```

The analytical layer reports evidence.

It does not automatically convert that evidence into stop, target, or risk
recommendations.

## Consequences

This architecture keeps responsibilities separated:

```text
Strategy
→ determines market events

Backtesting
→ executes events and measures individual trades

Analytics
→ aggregates historical behavior

User
→ makes trading and risk decisions
```

It also allows WINQuantLab to distinguish final result from the path taken
by price before the trade ended.

## Out of scope

The analytical core does not currently include:

- automatic stop-loss recommendations;
- automatic take-profit recommendations;
- automatic risk/reward selection;
- capital management;
- position sizing recommendations;
- pyramiding;
- multiple simultaneous positions;
- automatic reversal;
- partial exits;
- slippage;
- transaction costs;
- margin simulation.

These features should not be introduced merely to turn WINQuantLab into a
traditional order simulator.

## Future evolution

Possible future developments include:

- MFE and MAE;
- extreme candle identification;
- trade duration;
- outcome classification;
- aggregate trade statistics;
- percentiles and distributions;
- analysis by time;
- multiple trading sessions;
- explicit strategy exit events;
- trajectory analysis;
- sequence analysis when data granularity permits;
- reports;
- quantitative comparison between strategies.

New features should preserve the distinction between measurement and
decision-making.