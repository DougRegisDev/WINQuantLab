# WINQuantLab

> Construído para demonstrar como princípios de Engenharia de Software podem ser aplicados ao desenvolvimento de ferramentas quantitativas para o mercado financeiro.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-118%2B%20Passing-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

---

# Visão Geral

O **WINQuantLab** é um projeto Open Source criado com o objetivo de desenvolver uma biblioteca profissional para análise quantitativa do mercado financeiro.

Mais do que implementar indicadores técnicos, o projeto busca aplicar boas práticas de Engenharia de Software, utilizando arquitetura modular, testes automatizados, documentação técnica e código reutilizável.

O objetivo de longo prazo é construir uma plataforma completa para:

- Estudos quantitativos
- Market Structure
- Backtests
- Dashboards
- Estratégias de Trading
- Análise em tempo real

---

# Objetivos do Projeto

O WINQuantLab foi criado para demonstrar que projetos voltados ao mercado financeiro podem seguir os mesmos padrões de qualidade encontrados em aplicações corporativas.

O foco do projeto é unir:

- Engenharia de Software
- Mercado Financeiro
- Arquitetura de Software
- Boas práticas de desenvolvimento

---

# Principais Características

- Arquitetura modular
- Código reutilizável
- Clean Code
- Desenvolvimento orientado por testes (TDD)
- Testes automatizados
- Documentação técnica
- Fácil manutenção
- Preparado para expansão futura

---

# Indicadores Implementados

## Médias Móveis

- SMA
- EMA

---

## Momentum

- RSI

---

## Tendência

- ATR
- Directional Movement
- Directional Indicators (+DI / -DI)
- Directional Index (DX)
- ADX
- SuperTrend

---

# Arquitetura

```
WINQuantLab
│
├── config/
├── core/
├── data/
├── docs/
│
├── indicators/
│   ├── calculations.py
│   ├── moving_average/
│   ├── momentum/
│   └── trend/
│
├── reports/
├── strategies/
└── tests/
```

A arquitetura foi desenvolvida para minimizar duplicação de código e favorecer reutilização entre indicadores.

Grande parte dos cálculos matemáticos é compartilhada através de funções reutilizáveis.

---

# Princípios de Desenvolvimento

O projeto segue os seguintes princípios:

- Clean Code
- Arquitetura em Camadas
- Reutilização de Código
- Responsabilidade Única
- Testes Automatizados
- Refatoração Contínua
- Documentação antes da implementação

---

# Testes

Todo o desenvolvimento é realizado utilizando **Test-Driven Development (TDD)**.

Status atual:

- Mais de 118 testes automatizados
- Pytest
- Ruff
- Validação contínua durante o desenvolvimento

Executando os testes:

```bash
python -m pytest
```

Verificando qualidade do código:

```bash
python -m ruff check .
```

---

# Tecnologias

- Python
- Pandas
- Pytest
- Ruff
- Git
- GitHub

---

# Roadmap

## V1

- Loader de Dados
- Normalização
- Validação
- Médias Móveis
- Indicadores de Momentum
- Indicadores de Tendência

---

## V2

Market Structure

- Suportes e Resistências
- Swing High / Swing Low
- BOS
- CHoCH
- Classificação de Tendência
- Zonas de Oferta e Demanda

---

## V3

Análise em Tempo Real

- Dashboard
- Market Structure em tempo real
- Scanner de Estratégias
- Alertas

---

## V4

Backtesting

- Motor de Backtests
- Comparação de Estratégias
- Relatórios
- Métricas de Performance

---

# Filosofia

O WINQuantLab não nasceu apenas para calcular indicadores.

Ele foi criado para servir como uma plataforma de estudos de Engenharia de Software aplicada ao mercado financeiro.

Cada módulo do projeto é desenvolvido com foco em:

- Clareza
- Organização
- Testabilidade
- Reutilização
- Facilidade de manutenção

---

# Autor

## Douglas Betta Regis

Analista de Sistemas

Analista de Sistemas | Desenvolvedor Python | Engenharia de Software | Automação

LinkedIn

*(Adicionar após publicação)*

GitHub

https://github.com/DougRegisDev

---

# Licença

MIT License
