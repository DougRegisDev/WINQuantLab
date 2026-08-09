# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Architecture

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# 1. Objetivo

Este documento descreve a arquitetura do WINQuantLab.

Seu objetivo é documentar como a biblioteca está organizada, como seus módulos se relacionam e quais princípios arquiteturais orientam seu desenvolvimento.

A arquitetura foi projetada para facilitar manutenção, reutilização de código, escalabilidade e testes automatizados.

---

# 2. Visão Geral

O WINQuantLab foi desenvolvido utilizando arquitetura modular.

Cada módulo possui responsabilidades claramente definidas, reduzindo acoplamento e facilitando a evolução da biblioteca.

O fluxo principal da aplicação é composto pelas seguintes etapas:

```text
Mercado

↓

Dados

↓

Validação

↓

Normalização

↓

Indicadores

↓

Estratégias

↓

Backtesting

↓

Otimização

↓

Relatórios

↓

Análise
```

Cada etapa adiciona uma nova camada de informação sem modificar a responsabilidade da etapa anterior.

---

# 3. Arquitetura em Camadas

A arquitetura lógica da biblioteca está organizada nas seguintes camadas.

## Camada de Dados

Responsável pela importação, validação e normalização dos dados históricos.

Módulos:

- Loader
- Validator
- Normalizer

---

## Camada de Indicadores

Responsável pelo cálculo dos indicadores técnicos.

Os indicadores são organizados em famílias independentes.

Famílias previstas:

- Moving Average
- Momentum
- Trend
- Volume
- Volatility

---

## Camada de Estratégias

Responsável pela composição de indicadores para geração de regras de entrada e saída.

Nenhuma estratégia deverá implementar diretamente cálculos matemáticos já existentes nos indicadores.

---

## Camada de Backtesting

Responsável pela simulação das operações utilizando dados históricos.

Esta camada executará:

- entradas;
- saídas;
- stops;
- alvos;
- slippage;
- custos operacionais.

---

## Camada de Otimização

Responsável pela comparação automática de diferentes parâmetros.

Exemplos:

- Média de 20 versus 21 períodos.
- RSI de 9 versus 14 períodos.
- Comparação entre estratégias.

---

## Camada de Relatórios

Responsável pela geração de métricas e exportação dos resultados.

---

# 4. Estrutura do Projeto

```text
WINQuantLab
│
├── config/
│
├── core/
│
├── data/
│
├── indicators/
│   ├── moving_average/
│   ├── momentum/
│   ├── trend/
│   ├── volume/
│   ├── volatility/
│   └── calculations.py
│
├── strategies/
│
├── backtesting/
│
├── optimization/
│
├── reports/
│
├── visualization/
│
├── tests/
│
├── docs/
│
└── main.py
```

Esta estrutura representa a arquitetura prevista para a versão 1.0 da biblioteca.

---

# 5. Organização dos Indicadores

Cada família possui autonomia para implementar seus próprios cálculos auxiliares.

Exemplo:

```text
indicators/

    moving_average/
        calculations.py

    momentum/
        calculations.py
```

Caso um cálculo passe a ser utilizado por diferentes famílias, ele deverá ser promovido para:

```text
indicators/calculations.py
```

Essa organização evita duplicação de código e reduz dependências desnecessárias.

---

# 6. Hierarquia de Reutilização

Todo novo cálculo seguirá a seguinte hierarquia.

```text
Indicador

↓

Família

↓

Projeto
```

As regras são:

- um cálculo nasce no indicador que o utiliza;
- quando reutilizado pela mesma família, passa para `family/calculations.py`;
- quando reutilizado por diferentes famílias, passa para `indicators/calculations.py`.

Essa abordagem reduz refatorações prematuras e mantém o código organizado conforme sua evolução.

---

# 7. Fluxo de Desenvolvimento

Todo novo indicador deverá seguir o seguinte processo.

```text
Ideia

↓

Estudo da matemática

↓

Implementação dos cálculos reutilizáveis

↓

Testes dos cálculos

↓

Implementação do indicador

↓

Testes do indicador

↓

Refatoração (quando necessária)

↓

Documentação

↓

Git Commit
```

Nenhum indicador deverá ser considerado concluído antes de possuir testes automatizados.

---

# 8. Desenvolvimento Orientado por Testes

O WINQuantLab utiliza TDD como metodologia principal.

Cada funcionalidade deverá seguir o ciclo:

```text
RED

↓

GREEN

↓

REFACTOR
```

A implementação somente é considerada concluída após todos os testes serem aprovados.

---

# 9. Escalabilidade

A arquitetura foi projetada para permitir crescimento contínuo da biblioteca.

Novas famílias de indicadores poderão ser adicionadas sem alterar módulos já existentes.

Novas estratégias poderão reutilizar indicadores existentes.

Novos mecanismos de backtesting poderão reutilizar as estratégias.

Essa separação reduz acoplamento e facilita manutenção.

---

# 10. Dependências entre Módulos

A arquitetura segue o princípio de dependência unidirecional.

```text
Dados

↓

Indicadores

↓

Estratégias

↓

Backtesting

↓

Relatórios
```

Camadas superiores podem utilizar serviços das camadas inferiores.

O inverso não é permitido.

Exemplo:

- Estratégias utilizam indicadores.
- Indicadores não conhecem estratégias.

---

# 11. Convenções Arquiteturais

Durante todo o desenvolvimento da biblioteca deverão ser respeitados os seguintes princípios.

- Arquitetura antes da implementação.
- Separação de responsabilidades.
- Reutilização de cálculos matemáticos.
- Baixo acoplamento.
- Alta coesão.
- Desenvolvimento orientado por testes.
- Tipagem estática.
- Docstrings em módulos públicos.
- Refatoração apenas quando existir ganho arquitetural ou funcional.
- Código legível acima de código complexo.

---

# 12. Evolução da Arquitetura

A arquitetura deverá evoluir sem quebrar contratos públicos.

Mudanças estruturais relevantes deverão ser registradas por meio de ADRs (Architecture Decision Records).

A prioridade é preservar estabilidade, previsibilidade e reutilização dos componentes ao longo da evolução do projeto.
