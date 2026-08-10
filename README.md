# WINQuantLab

> An open-source quantitative analysis library showcasing software engineering best practices for financial markets.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-126%20Passing-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

## Overview

WINQuantLab is an open-source Python library designed to build a professional quantitative analysis framework for financial markets.

Rather than focusing solely on implementing technical indicators, the project emphasizes software engineering principles such as modular architecture, code reuse, automated testing, maintainability, and technical documentation.

The project aims to evolve into a complete platform for quantitative research, market structure analysis, dashboards, and backtesting.

---

## Why WINQuantLab?

Most quantitative libraries focus only on calculations.

WINQuantLab focuses on building software that is:

- Modular
- Maintainable
- Testable
- Reusable
- Well documented
- Easy to extend

Every feature is designed with long-term evolution in mind.

---

## Engineering Principles

The project follows a software engineering approach based on:

- Layered Architecture
- Clean Code
- Test-Driven Development (TDD)
- Automated Testing
- Code Reusability
- Continuous Refactoring
- Technical Documentation

---

## Features

Current features include:

- Data loading
- Data validation
- Data normalization
- Moving averages
- Momentum indicators
- Trend indicators
- Shared mathematical calculation engine

Future versions will include:

- Market Structure
- Support & Resistance Zones
- Backtesting Engine
- Interactive Dashboard
- Real-Time Analysis

---

## Project Structure

```text
WINQuantLab
│
├── config/
├── core/
├── data/
├── docs/
├── indicators/
│   ├── calculations.py
│   ├── moving_average/
│   ├── momentum/
│   └── trend/
├── reports/
├── strategies/
├── tests/
│
├── README.md
├── README.pt-BR.md
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── CONTRIBUTING.md
```

---

## Current Indicators

### Moving Average

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)

### Momentum

- Relative Strength Index (RSI)

### Trend

- Average True Range (ATR)
- Directional Movement (+DM / -DM)
- Directional Indicator (+DI / -DI)
- Directional Index (DX)
- Average Directional Index (ADX)
- SuperTrend

---

## Current Project Status

| Module | Status |
|----------|:------:|
| Data Loader | ✅ |
| Validation | ✅ |
| Normalization | ✅ |
| Moving Average | ✅ |
| Momentum | ✅ |
| Trend | ✅ |
| Market Structure | 🔄 Planned |
| Dashboard | ⏳ Planned |
| Backtesting | ⏳ Planned |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/DougRegisDev/WINQuantLab.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -r requirements-dev.txt
```

---

## Testing

Run the automated tests:

```bash
python -m pytest
```

Run static analysis:

```bash
python -m ruff check .
```

Current project:

- 126 automated tests
- Test-Driven Development
- Continuous validation

---

## Roadmap

### Version 1

- Data Pipeline
- Technical Indicators
- Documentation

### Version 2

- Market Structure
- Supply & Demand
- BOS / CHoCH
- Swing Detection

### Version 3

- Dashboard
- Live Analysis
- Strategy Scanner

### Version 4

- Backtesting
- Reports
- Performance Metrics

---

## Documentation

Project documentation is available in the `/docs` directory.

It includes:

- Architecture
- Coding Standards
- ADRs
- Roadmap
- Project Principles

---

## Contributing

Contributions are welcome.

Feel free to open an Issue or submit a Pull Request.

---

## About the Author

**Douglas Betta Regis**

Systems Analyst • Python Developer • ServiceNow Developer

Passionate about Software Engineering, Automation and Quantitative Finance.

GitHub:
https://github.com/DougRegisDev

LinkedIn:
*(coming soon)*

---

## License

This project is licensed under the MIT License.
