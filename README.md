# WINQuantLab

> An open-source Python framework for quantitative market analysis, strategy research, and backtesting, built with software engineering best practices.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-313%20Passing-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

## Overview

WINQuantLab is an open-source Python project for quantitative market analysis, strategy research, and backtesting.

The project combines financial market analysis with software engineering practices such as modular architecture, Test-Driven Development (TDD), automated testing, reusable components, explicit architectural decisions, and technical documentation.

WINQuantLab is designed as an analytical framework rather than an automated trading system.

Its core principle is simple:

> **WINQuantLab measures. The user interprets.**

The framework analyzes what happened after a strategy generated a signal and while the resulting trade remained active. Decisions involving capital, risk, stop loss, take profit, position sizing, and execution policy remain outside the analytical core.

---

## Current Capabilities

WINQuantLab currently provides:

- Market data loading
- Data validation
- Data normalization
- Profit/Neologica CSV integration
- Technical indicators
- Quantitative strategies
- Signal generation
- Single-session backtesting engine
- Multi-session backtesting pipeline
- Trade excursion analysis
- Trade duration analysis
- Outcome-based analytics
- Period aggregation
- Text reports
- Command-line interface
- Public Python API
- Automated test suite

---

## Architecture

The main analytical pipeline follows this structure:

```text
Market Data
    |
    v
Loader
    |
    v
Normalizer
    |
    v
Session Split
    |
    v
Indicators
    |
    v
Strategies
    |
    v
Signals
    |
    v
Backtesting Engine
    |
    v
Session Results
    |
    v
Period Analytics
    |
    v
Reports
```

Responsibilities are intentionally separated.

Indicators calculate market information.

Strategies consume normalized market data and generate signals.

The backtesting engine executes those signals according to explicit execution rules.

The analytical pipeline aggregates trades and sessions.

Reports present the resulting measurements.

The `winquantlab` package acts as the public facade of the library, keeping the public API independent from the internal module organization.

---

## Project Structure

```text
WINQuantLab/
|
|-- backtesting/
|   |-- engine.py
|   `-- pipeline.py
|
|-- config/
|-- core/
|-- data/
|-- docs/
|
|-- indicators/
|   |-- calculations.py
|   |-- momentum/
|   |-- moving_averages/
|   |-- trend/
|   `-- volume/
|
|-- reports/
|   `-- text_report.py
|
|-- strategies/
|   |-- breakout.py
|   `-- moving_average_crossover.py
|
|-- tests/
|
|-- winquantlab/
|   `-- __init__.py
|
|-- cli.py
|-- pyproject.toml
|-- README.md
|-- README.pt-BR.md
|-- CHANGELOG.md
|-- CONTRIBUTING.md
`-- LICENSE
```

---

## Technical Indicators

### Moving Averages

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Weighted Moving Average (WMA)
- Hull Moving Average (HMA)

### Momentum

- Momentum
- Rate of Change (ROC)
- Relative Strength Index (RSI)
- Stochastic Oscillator
- MACD

### Trend

- Average True Range (ATR)
- Directional Indicator (+DI / -DI)
- Average Directional Index (ADX)
- Supertrend
- Parabolic SAR

### Volume

- Financial Volume
- On-Balance Volume (OBV)
- Volume Weighted Average Price (VWAP)
- Weis Wave Volume

---

## Strategies

### Moving Average Crossover

Generates trading events when a fast moving average crosses a slower moving average.

Main parameters:

```text
fast_period
slow_period
```

The fast period must be smaller than the slow period.

### Breakout

Generates signals when the closing price breaks the highest high or lowest low of the previous `lookback` candles.

Main parameter:

```text
lookback
```

The current candle is excluded from the breakout level calculation.

---

## Signal Model

Strategies generate events rather than persistent position states:

```text
 1 = buy event
 0 = no new event
-1 = sell event
```

Strategies do not execute trades.

Execution belongs to the backtesting layer.

---

## Backtesting Engine

The current engine uses explicit execution rules.

A signal generated at the close of candle `N` is executed at the open of candle `N+1`.

The engine currently supports:

- FLAT, LONG, and SHORT states
- One position at a time
- Fixed quantity of one unit
- No pyramiding
- Same-direction signal ignored while positioned
- Opposite signal closes the current position
- No automatic reversal
- Forced closing of an open position at the final candle
- Point-based P&L
- Trade duration measurement
- Maximum Favorable Excursion (MFE)
- Maximum Adverse Excursion (MAE)
- WIN / LOSS / EVEN classification

Financial risk management is intentionally outside the current engine.

The engine does not decide:

- Capital allocation
- Stop loss
- Take profit
- Position sizing
- Margin
- Monetary risk
- Brokerage costs
- Slippage

---

## Analytical Measurements

Each trade can contain analytical information including:

```text
direction
entry_index
entry_price
exit_index
exit_price
quantity
pnl_points
favorable_price
adverse_price
mfe_points
mae_points
mfe_index
mae_index
duration_candles
outcome
```

When a `DatetimeIndex` is available, entry and exit timestamps can also be recorded.

Period analytics include distributions such as:

- Average
- Median
- Minimum
- Maximum
- P25
- P50
- P75

Measurements can also be grouped by trade outcome:

```text
WIN
LOSS
EVEN
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DougRegisDev/WINQuantLab.git
cd WINQuantLab
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install WINQuantLab

For development:

```bash
python -m pip install -e ".[dev]"
```

The project declares its runtime dependencies through `pyproject.toml`.

---

## Public Python API

WINQuantLab provides a high-level public API through the `winquantlab` package.

```python
import winquantlab as wql

print(wql.__version__)
```

The public API exposes the main components of the framework without requiring users to depend on its internal module structure.

### Data

```python
from winquantlab import load_data, normalize
```

### Indicators

```python
from winquantlab import (
    adx,
    atr,
    di_minus,
    di_plus,
    ema,
    financial_volume,
    hma,
    macd,
    momentum,
    obv,
    parabolic_sar,
    roc,
    rsi,
    sma,
    stochastic,
    supertrend,
    vwap,
    weis_wave,
    wma,
)
```

### Strategies

```python
from winquantlab import breakout, moving_average_crossover
```

### Backtesting

```python
from winquantlab import backtest, run_sessions
```

### Reports

```python
from winquantlab import create_text_report
```

### Basic indicator example

```python
import winquantlab as wql

data = wql.load_data("market_data.csv")
data = wql.normalize(data)

data = wql.rsi(data)
data = wql.ema(data)

print(data.tail())
```

For headerless Profit/Neologica CSV exports, the data can be loaded and normalized explicitly:

```python
import winquantlab as wql

data = wql.load_data("market_data.csv", header=None)
data = wql.normalize(data, source="profit")
```

### Strategy and single-session backtest

```python
import winquantlab as wql

signals = wql.breakout(data, lookback=20)
trades = wql.backtest(signals)

print(trades)
```

### Multi-session backtest

`run_sessions()` receives normalized market data and a strategy callable.

Strategies with custom parameters can be configured with a small wrapper:

```python
import winquantlab as wql


def breakout_20(data):
    return wql.breakout(data, lookback=20)


results = wql.run_sessions(data, breakout_20)
```

This facade-first design allows the internal architecture to evolve without requiring users to import implementation modules directly.

---

## Command-Line Interface

After installation, the CLI is available through:

```bash
winquantlab --help
```

The current CLI provides the `backtest` command.

### Breakout example

```bash
winquantlab backtest --file data/sample/market_data.csv --strategy breakout --lookback 20
```

### Moving Average Crossover example

```bash
winquantlab backtest --file data/sample/market_data.csv --strategy moving_average_crossover --fast-period 9 --slow-period 21
```

The current data integration is designed for headerless Profit/Neologica CSV exports normalized by WINQuantLab.

---

## Example Report

A backtest produces a text report containing information such as:

```text
WINQuantLab - Backtest Report
=============================

Strategy: breakout
Parameters: lookback=20

Period analyzed
---------------
Sessions: ...
Sessions with trades: ...
Sessions without trades: ...
Trades: ...

Results
-------
Wins: ...
Losses: ...
Even: ...

General excursion
-----------------
MFE average: ...
MFE median: ...
MFE P25/P50/P75: ...

MAE average: ...
MAE median: ...
MAE P25/P50/P75: ...

Duration
--------
Average: ...
Median: ...
P25/P50/P75: ...

By outcome
----------
                   WIN        LOSS        EVEN
...
```

The report is analytical. It does not provide trading recommendations or determine risk parameters.

---

## Testing

WINQuantLab is developed with Test-Driven Development (TDD).

Current status:

```text
313 automated tests passing
```

Run the complete test suite:

```bash
python -m pytest
```

Run static analysis:

```bash
python -m ruff check .
```

Check formatting:

```bash
python -m ruff format --check .
```

---

## Engineering Principles

The project emphasizes:

- Modular architecture
- Separation of responsibilities
- Test-Driven Development
- Automated testing
- Clean Code
- Reusable calculations
- Explicit validation
- Continuous refactoring
- Architecture Decision Records (ADRs)
- Technical documentation
- Incremental evolution

Features are introduced when there is a concrete architectural or analytical need rather than through premature abstraction.

---

## Architecture Decision Records

Important architectural decisions are documented under:

```text
docs/ADR/
```

The project currently includes seven ADRs covering:

- Project foundation
- Data normalization
- Indicator architecture
- Moving averages architecture
- Strategy architecture
- Backtesting architecture
- Backtest execution pipeline

These records document not only what was implemented, but also the reasoning and boundaries behind each subsystem.

---

## Documentation

Additional documentation is available in the `docs/` directory, including:

- Architecture
- Coding standards
- Project principles
- Glossary
- Roadmap
- Architecture Decision Records

---

## Project Status

| Component | Status |
|---|:---:|
| Data Pipeline | Implemented |
| Data Validation | Implemented |
| Data Normalization | Implemented |
| Technical Indicators | Implemented |
| Volume Indicators | Implemented |
| Strategy Layer | Implemented |
| Backtesting Engine | Implemented |
| Multi-Session Pipeline | Implemented |
| Trade Analytics | Implemented |
| Period Analytics | Implemented |
| Text Reports | Implemented |
| Command-Line Interface | Implemented |
| Public Python API | Implemented |
| Package Distribution | In progress |
| Interactive Interface | Planned |

---

## Roadmap

### Current 0.8.0 Stabilization

- Validate clean installation workflows
- Validate package build
- Refine package distribution
- Finalize release documentation
- Prepare the `0.8.0` release

### Future Evolution

Potential future work includes:

- Bollinger Bands
- Donchian Channel
- Pullback / Mean Reversion strategy
- Price Action research
- Parameter optimization
- Additional analytical reports
- Market structure research
- Strategy comparison tools
- Interactive visualization
- Graphical interface
- Extended data-source support

New functionality should preserve the separation between market analysis, strategy logic, execution simulation, and reporting.

---

## Philosophy

WINQuantLab is not intended to decide how much risk a trader should take.

Its role is to provide reproducible measurements that help researchers understand strategy behavior.

> **WINQuantLab measures. The user interprets.**

This principle keeps analytical evidence separate from financial decisions.

---

## Contributing

Contributions are welcome.

Before contributing, review:

```text
CONTRIBUTING.md
docs/coding_standards.md
docs/ADR/
```

Issues and Pull Requests can be used to propose improvements, fixes, tests, documentation, or new analytical components.

---

## About the Author

**Douglas Betta Regis**

Systems Analyst | Python Developer | Software Engineering | Automation

GitHub:
https://github.com/DougRegisDev

LinkedIn:
https://www.linkedin.com/in/douglas-betta-regis/

---

## License

This project is licensed under the MIT License.
