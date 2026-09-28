# WINQuantLab

> Framework open source em Python para análise quantitativa de mercado, pesquisa de estratégias e backtesting, desenvolvido com boas práticas de Engenharia de Software.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-302%20Passing-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

---

## Visão Geral

O WINQuantLab é um projeto open source em Python para análise quantitativa de mercado, pesquisa de estratégias e backtesting.

O projeto combina análise de mercado financeiro com práticas de Engenharia de Software, como arquitetura modular, Test-Driven Development (TDD), testes automatizados, componentes reutilizáveis, decisões arquiteturais explícitas e documentação técnica.

O WINQuantLab foi projetado como um framework analítico, e não como um sistema automatizado de negociação.

Seu princípio central é simples:

> **O WINQuantLab mede. O usuário interpreta.**

O framework analisa o que aconteceu após uma estratégia gerar um sinal e enquanto a operação resultante permaneceu ativa. Decisões envolvendo capital, risco, stop loss, take profit, dimensionamento de posição e política de execução permanecem fora do núcleo analítico.

---

## Capacidades Atuais

Atualmente, o WINQuantLab oferece:

- Carregamento de dados de mercado
- Validação de dados
- Normalização de dados
- Integração com CSV do Profit/Neologica
- Indicadores técnicos
- Estratégias quantitativas
- Geração de sinais
- Motor de backtesting para uma sessão
- Pipeline de backtesting multi-sessão
- Análise de excursão das operações
- Análise de duração das operações
- Análises por resultado
- Agregação por período
- Relatórios em texto
- Interface de linha de comando
- Suíte automatizada de testes

---

## Arquitetura

O pipeline analítico principal segue esta estrutura:

```text
Dados de Mercado
    |
    v
Loader
    |
    v
Normalizer
    |
    v
Separação por Sessão
    |
    v
Indicadores
    |
    v
Estratégias
    |
    v
Sinais
    |
    v
Motor de Backtesting
    |
    v
Resultados por Sessão
    |
    v
Análise do Período
    |
    v
Relatórios
```

As responsabilidades são separadas de forma intencional.

Os indicadores calculam informações de mercado.

As estratégias recebem dados normalizados e geram sinais.

O motor de backtesting executa esses sinais de acordo com regras explícitas de execução.

O pipeline analítico agrega operações e sessões.

Os relatórios apresentam as medições resultantes.

---

## Estrutura do Projeto

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
|-- cli.py
|-- pyproject.toml
|-- README.md
|-- README.pt-BR.md
|-- CHANGELOG.md
|-- CONTRIBUTING.md
`-- LICENSE
```

---

## Indicadores Técnicos

### Médias Móveis

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

### Tendência

- Average True Range (ATR)
- Directional Indicator (+DI / -DI)
- Average Directional Index (ADX)
- Supertrend
- Parabolic SAR

### Volume

- Volume Financeiro
- On-Balance Volume (OBV)
- Volume Weighted Average Price (VWAP)
- Weis Wave Volume

---

## Estratégias

### Moving Average Crossover

Gera eventos de negociação quando uma média móvel rápida cruza uma média móvel mais lenta.

Principais parâmetros:

```text
fast_period
slow_period
```

O período rápido deve ser menor que o período lento.

### Breakout

Gera sinais quando o preço de fechamento rompe a máxima mais alta ou a mínima mais baixa dos `lookback` candles anteriores.

Parâmetro principal:

```text
lookback
```

O candle atual é excluído do cálculo do nível de rompimento.

---

## Modelo de Sinais

As estratégias geram eventos, e não estados persistentes de posição:

```text
 1 = evento de compra
 0 = nenhum novo evento
-1 = evento de venda
```

As estratégias não executam operações.

A execução pertence à camada de backtesting.

---

## Motor de Backtesting

O motor atual utiliza regras explícitas de execução.

Um sinal gerado no fechamento do candle `N` é executado na abertura do candle `N+1`.

Atualmente, o motor suporta:

- Estados FLAT, LONG e SHORT
- Uma posição por vez
- Quantidade fixa de uma unidade
- Sem piramidagem
- Sinal na mesma direção ignorado enquanto existe posição
- Sinal oposto encerra a posição atual
- Sem reversão automática
- Encerramento forçado de posição aberta no último candle
- P&L em pontos
- Medição da duração da operação
- Maximum Favorable Excursion (MFE)
- Maximum Adverse Excursion (MAE)
- Classificação WIN / LOSS / EVEN

A gestão financeira de risco permanece intencionalmente fora do motor atual.

O motor não decide:

- Alocação de capital
- Stop loss
- Take profit
- Dimensionamento de posição
- Margem
- Risco monetário
- Custos de corretagem
- Slippage

---

## Medições Analíticas

Cada operação pode conter informações analíticas como:

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

Quando um `DatetimeIndex` está disponível, os horários de entrada e saída também podem ser registrados.

As análises do período incluem distribuições como:

- Média
- Mediana
- Mínimo
- Máximo
- P25
- P50
- P75

As medições também podem ser agrupadas pelo resultado da operação:

```text
WIN
LOSS
EVEN
```

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/DougRegisDev/WINQuantLab.git
cd WINQuantLab
```

### 2. Crie um ambiente virtual

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

### 3. Instale o WINQuantLab

Para desenvolvimento:

```bash
python -m pip install -e ".[dev]"
```

As dependências necessárias para execução são declaradas no `pyproject.toml`.

---

## Interface de Linha de Comando

Após a instalação, a CLI fica disponível através de:

```bash
winquantlab --help
```

Atualmente, a CLI disponibiliza o comando `backtest`.

### Exemplo com Breakout

```bash
winquantlab backtest --file data/sample/market_data.csv --strategy breakout --lookback 20
```

### Exemplo com Moving Average Crossover

```bash
winquantlab backtest --file data/sample/market_data.csv --strategy moving_average_crossover --fast-period 9 --slow-period 21
```

A integração de dados atual foi projetada para arquivos CSV sem cabeçalho exportados pelo Profit/Neologica e normalizados pelo WINQuantLab.

---

## Exemplo de Relatório

Um backtest produz um relatório em texto contendo informações como:

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

O relatório é analítico. Ele não fornece recomendações de negociação nem determina parâmetros de risco.

---

## Testes

O WINQuantLab é desenvolvido utilizando Test-Driven Development (TDD).

Status atual:

```text
302 testes automatizados passando
```

Execute toda a suíte de testes:

```bash
python -m pytest
```

Execute a análise estática:

```bash
python -m ruff check .
```

Verifique a formatação:

```bash
python -m ruff format --check .
```

---

## Princípios de Engenharia

O projeto enfatiza:

- Arquitetura modular
- Separação de responsabilidades
- Test-Driven Development
- Testes automatizados
- Clean Code
- Cálculos reutilizáveis
- Validação explícita
- Refatoração contínua
- Architecture Decision Records (ADRs)
- Documentação técnica
- Evolução incremental

Novas funcionalidades são introduzidas quando existe uma necessidade arquitetural ou analítica concreta, evitando abstrações prematuras.

---

## Architecture Decision Records

As principais decisões arquiteturais são documentadas em:

```text
docs/ADR/
```

Atualmente, o projeto possui decisões relacionadas a temas como:

- Arquitetura de dados
- Arquitetura dos indicadores
- Arquitetura das estratégias
- Arquitetura de backtesting
- Pipeline de execução de backtests

Esses registros documentam não apenas o que foi implementado, mas também o raciocínio e os limites definidos para cada subsistema.

---

## Documentação

Documentação adicional está disponível no diretório `docs/`, incluindo:

- Arquitetura
- Padrões de código
- Princípios do projeto
- Glossário
- Roadmap
- Architecture Decision Records

---

## Status do Projeto

| Componente | Status |
|---|:---:|
| Pipeline de Dados | Implementado |
| Validação de Dados | Implementado |
| Normalização de Dados | Implementado |
| Indicadores Técnicos | Implementado |
| Indicadores de Volume | Implementado |
| Camada de Estratégias | Implementado |
| Motor de Backtesting | Implementado |
| Pipeline Multi-Sessão | Implementado |
| Análise de Operações | Implementado |
| Análise por Período | Implementado |
| Relatórios em Texto | Implementado |
| Interface de Linha de Comando | Implementado |
| Estabilização da API Pública | Em andamento |
| Interface Interativa | Planejado |

---

## Roadmap

### Estabilização Atual da V1

- Estabilizar a API pública
- Melhorar a documentação de instalação e uso
- Adicionar exemplos reproduzíveis
- Validar instalação em ambiente limpo
- Refinar a distribuição do pacote

### Evolução Futura

Possíveis evoluções incluem:

- Novas estratégias
- Novos relatórios analíticos
- Estudos de Market Structure
- Ferramentas de comparação de estratégias
- Visualização interativa
- Interface gráfica
- Suporte ampliado a fontes de dados

Novas funcionalidades devem preservar a separação entre análise de mercado, lógica das estratégias, simulação de execução e apresentação dos resultados.

---

## Filosofia

O WINQuantLab não tem como objetivo decidir quanto risco um trader deve assumir.

Seu papel é fornecer medições reproduzíveis que ajudem pesquisadores a compreender o comportamento das estratégias.

> **O WINQuantLab mede. O usuário interpreta.**

Esse princípio mantém as evidências analíticas separadas das decisões financeiras.

---

## Contribuindo

Contribuições são bem-vindas.

Antes de contribuir, consulte:

```text
CONTRIBUTING.md
docs/coding_standards.md
docs/ADR/
```

Issues e Pull Requests podem ser utilizados para propor melhorias, correções, testes, documentação ou novos componentes analíticos.

---

## Autor

**Douglas Betta Regis**

Analista de Sistemas | Desenvolvedor Python | Engenharia de Software | Automação

GitHub:
https://github.com/DougRegisDev

LinkedIn:
https://www.linkedin.com/in/douglas-betta-regis/

---

## Licença

Este projeto é licenciado sob a MIT License.
