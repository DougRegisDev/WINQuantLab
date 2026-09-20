# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

O formato segue o padrão **Keep a Changelog** e utiliza **Versionamento Semântico (SemVer)**.

---

## [Não publicado]

### Adicionado

#### Indicadores de Tendência

- Implementado Average True Range (ATR).
- Implementado Directional Indicator positivo (DI+).
- Implementado Directional Indicator negativo (DI-).
- Implementado Average Directional Index (ADX).
- Implementado SuperTrend.
- Implementado Parabolic SAR (PSAR).

#### Parabolic SAR

- Implementado cálculo iterativo do Parabolic SAR.
- Implementada identificação do estado inicial de tendência de alta ou baixa.
- Implementado acompanhamento de tendência utilizando Extreme Point (EP).
- Implementado Acceleration Factor (AF).
- Implementado incremento configurável do fator de aceleração por meio de `step`.
- Implementado limite máximo configurável por meio de `max_step`.
- Implementada detecção de reversão de tendência de alta para baixa.
- Implementada detecção de reversão de tendência de baixa para alta.
- Implementado tratamento para DataFrame vazio.
- Implementado tratamento para séries contendo apenas um registro.
- Implementadas validações das colunas obrigatórias `high` e `low`.
- Implementadas validações dos parâmetros `step` e `max_step`.

#### Indicadores de Volume

- Criada a família `indicators.volume`.
- Implementado Volume Weighted Average Price (VWAP).
- Implementado Volume Financeiro.
- Implementado On-Balance Volume (OBV).
- Implementado Weis Wave Volume.

#### VWAP

- Implementado cálculo do Typical Price utilizando `high`, `low` e `close`.
- Implementado cálculo de preço ponderado pelo volume.
- Implementado cálculo acumulado de preço × volume.
- Implementado cálculo acumulado de volume.
- Implementado cálculo do Volume Weighted Average Price (VWAP).
- Implementadas validações das colunas obrigatórias `high`, `low`, `close` e `volume`.
- Implementado tratamento para DataFrame vazio.
- Implementado comportamento para séries com volume acumulado igual a zero.
- Preservado o DataFrame original por meio de cópia antes do cálculo.

#### Volume Financeiro

- Implementado cálculo de Volume Financeiro utilizando `close × volume`.
- Criada a coluna `financial_volume`.
- Implementadas validações das colunas obrigatórias `close` e `volume`.
- Implementado tratamento para DataFrame vazio.
- Implementado comportamento para candles com volume igual a zero.
- Preservado o DataFrame original por meio de cópia antes do cálculo.

#### On-Balance Volume

- Implementado On-Balance Volume (OBV).
- Definido valor inicial do OBV como `0.0`.
- Implementado acréscimo do volume quando o fechamento atual é superior ao fechamento anterior.
- Implementada subtração do volume quando o fechamento atual é inferior ao fechamento anterior.
- Implementada manutenção do OBV quando os fechamentos atual e anterior são iguais.
- Implementadas validações das colunas obrigatórias `close` e `volume`.
- Implementado tratamento para DataFrame vazio.
- Implementado tratamento para séries contendo apenas um registro.
- Preservado o DataFrame original por meio de cópia antes do cálculo.

#### Weis Wave Volume

- Implementado cálculo acumulativo de volume por ondas direcionais.
- Implementada identificação de ondas de alta com direção `1`.
- Implementada identificação de ondas de baixa com direção `-1`.
- Definido estado inicial neutro com direção `0`.
- Implementado acúmulo de volume enquanto a direção da onda é mantida.
- Implementado reinício do volume acumulado quando ocorre mudança de direção.
- Implementada manutenção da direção vigente quando o fechamento permanece inalterado.
- Implementado acúmulo dos volumes iniciais enquanto a direção da primeira onda ainda não foi definida.
- Implementadas validações das colunas obrigatórias `close` e `volume`.
- Implementado tratamento para DataFrame vazio.
- Implementado tratamento para séries contendo apenas um registro.
- Preservado o DataFrame original por meio de cópia antes do cálculo.

#### Testes

Adicionados testes automatizados para os indicadores de tendência e volume.

O Parabolic SAR possui 11 testes cobrindo:

- Criação da coluna `parabolic_sar`.
- Geração de valores numéricos.
- Comportamento em tendência de alta.
- Comportamento em tendência de baixa.
- Reversão de tendência.
- Validação de `step`.
- Validação de `max_step`.
- Ausência da coluna `high`.
- Ausência da coluna `low`.
- DataFrame vazio.
- Série contendo apenas um registro.

O VWAP possui 9 testes cobrindo:

- Criação da coluna `vwap`.
- Cálculo dos valores esperados.
- Ausência da coluna `high`.
- Ausência da coluna `low`.
- Ausência da coluna `close`.
- Ausência da coluna `volume`.
- DataFrame vazio.
- Volume acumulado igual a zero.
- Preservação do DataFrame original.

O Volume Financeiro possui 7 testes cobrindo:

- Criação da coluna `financial_volume`.
- Cálculo dos valores esperados.
- Ausência da coluna `close`.
- Ausência da coluna `volume`.
- DataFrame vazio.
- Preservação do DataFrame original.
- Volume igual a zero.

O On-Balance Volume possui 7 testes cobrindo:

- Criação da coluna `obv`.
- Cálculo dos valores esperados.
- DataFrame vazio.
- Ausência da coluna `close`.
- Ausência da coluna `volume`.
- Preservação do DataFrame original.
- Série contendo apenas um registro.

O Weis Wave Volume possui 11 testes cobrindo:

- Criação das colunas `weis_wave_direction` e `weis_wave_volume`.
- Acúmulo de volume em ondas de alta.
- Acúmulo de volume em ondas de baixa.
- Reinício do volume após mudança de direção.
- Manutenção da direção quando o fechamento permanece igual.
- Acúmulo de volume durante o estado neutro inicial.
- DataFrame vazio.
- Ausência da coluna `close`.
- Ausência da coluna `volume`.
- Série contendo apenas um registro.
- Preservação do DataFrame original.

Estado atual da suíte:

- 171 testes automatizados.
- 171 testes aprovados.
- 0 falhas.

#### Arquitetura

- Expandida a família `indicators.trend`.
- Criada e expandida a família `indicators.volume`.
- Mantida a separação entre famílias de indicadores.
- Introduzido indicador com cálculo stateful/iterativo por meio do Parabolic SAR.
- Introduzido cálculo ponderado por volume por meio do VWAP.
- Introduzido cálculo de volume financeiro por candle.
- Introduzido indicador de volume acumulativo por meio do OBV.
- Mantida a arquitetura modular dos indicadores.
- Preservada a compatibilidade com os componentes existentes do projeto.
- Introduzido indicador stateful de volume por ondas direcionais por meio do Weis Wave

#### Qualidade

- Parabolic SAR desenvolvido utilizando TDD.
- VWAP desenvolvido utilizando TDD.
- Volume Financeiro desenvolvido utilizando TDD.
- OBV desenvolvido utilizando TDD.
- Weis Wave desenvolvido utilizando TDD.
- Validações de entrada adicionadas.
- Casos de borda cobertos por testes automatizados.
- Preservação dos dados de entrada verificada por testes.
- Projeto validado com Ruff.
- Suíte completa executada após as implementações.
- Nenhuma regressão identificada nos testes existentes.

### Planejado

#### Estratégias

- Cruzamento de Médias
- Pullback
- Rompimento
- Price Action

#### Backtesting

- Motor de backtesting.
- Otimização de parâmetros.
- Relatórios estatísticos.

---

## [0.7.0] - 2026-08-07

### Adicionado

#### Indicadores de Momentum

- Implementado Relative Strength Index (RSI).
- Implementado Moving Average Convergence Divergence (MACD).
- Implementado Momentum.
- Implementado Rate of Change (ROC).
- Implementado Stochastic Oscillator.

#### Cálculos Compartilhados

- Criada `calculate_ema()`.
- Criadas `calculate_rolling_max()`.
- Criadas `calculate_rolling_min()`.

#### Cálculos da Família Momentum

- Criada `calculate_price_changes()`.
- Criada `separate_gains_and_losses()`.
- Criada `calculate_wilder_average()`.
- Criada `calculate_previous_values()`.

#### Testes

Adicionados testes automatizados para:

- RSI
- MACD
- Momentum
- ROC
- Stochastic
- Shared Calculations
- Momentum Calculations

Total:

- 84 testes automatizados.
- 84 testes aprovados.
- 0 falhas.
- 0 testes ignorados.

#### Arquitetura

- Criada a família `momentum`.
- Separação entre cálculos compartilhados e cálculos específicos da família.
- Reutilização da EMA pelo MACD.
- Reutilização dos cálculos auxiliares pelo RSI.
- Reutilização de `calculate_previous_values()` pelo Momentum e ROC.
- Definida convenção única para nomenclatura das colunas dos indicadores.

#### Qualidade

- Padronização completa dos novos indicadores.
- Docstrings adicionadas em todos os módulos.
- Tipagem estática aplicada.
- Todos os indicadores desenvolvidos utilizando TDD.

### Alterado

#### Arquitetura

- Consolidação da estrutura hierárquica dos cálculos matemáticos.
- Evolução da organização modular dos indicadores.
- Definição da convenção de reutilização por famílias de indicadores.

### Corrigido

- Ajustes na implementação inicial do RSI.
- Ajustes de importação dos módulos.
- Correção da API pública da família Momentum.
- Correções nos testes automatizados.

### Status da Sprint 2

Epic 2 — Indicadores de Momentum

Concluído:

- ✔ RSI
- ✔ MACD
- ✔ Momentum
- ✔ ROC
- ✔ Stochastic

Estado do projeto:

- 84 testes
- 84 aprovados
- 0 falhas

---

## [0.6.0] - 2026-08-05

### Adicionado

#### Indicadores

- Implementada a Média Móvel Simples (SMA).
- Implementada a Média Móvel Exponencial (EMA).
- Implementada a Média Móvel Ponderada (WMA).
- Implementada a Hull Moving Average (HMA).

#### Arquitetura

- Criado o módulo `core.validations`.
- Criado o módulo `moving_averages.calculations`.
- Padronizada a API pública da família de médias móveis.
- Centralizadas as validações compartilhadas dos indicadores.
- Separado o algoritmo de cálculo da WMA para reutilização.

#### Testes

- Testes para Loader.
- Testes para Validator.
- Testes para Normalizer.
- Testes para Core Validations.
- Testes da SMA.
- Testes da EMA.
- Testes da WMA.
- Testes da HMA.

Total:

- 35 testes automatizados.
- 35 testes aprovados.

#### Qualidade

- Projeto padronizado com Ruff.
- Tipagem adicionada aos módulos.
- Docstrings padronizadas.
- Estrutura modular reorganizada.

#### Documentação

Atualizados:

- README
- CHANGELOG
- Architecture
- Roadmap
- ADRs
- Coding Standards
- Project Principles

### Alterado

#### Refatoração

- Removidas validações duplicadas dos indicadores.
- Criado `validate_indicator_input()`.
- Reutilização das validações entre SMA, EMA, WMA e HMA.
- Refatoração da WMA para utilização de algoritmo compartilhado.
- Organização definitiva da família `moving_averages`.

### Status da Sprint 1

Epic 1 — Fundação do projeto

Concluído:

- ✔ Loader
- ✔ Validator
- ✔ Normalizer
- ✔ Core Validations
- ✔ SMA
- ✔ EMA
- ✔ WMA
- ✔ HMA

Estado do projeto:

- 35 testes
- 35 aprovados
- 0 falhas

---

## [0.5.0]

### Adicionado

- Implementação da EMA.
- Primeiros indicadores técnicos.
- Estrutura inicial da biblioteca de indicadores.

---

## [0.4.0]

### Adicionado

- Implementação da SMA.
- Organização inicial da pasta `indicators`.
- Primeiros testes automatizados para indicadores.

---

## [0.3.0]

### Adicionado

- Normalizador de dados.
- Testes do Normalizer.

---

## [0.2.0]

### Adicionado

- Validator.
- Testes do Validator.

---

## [0.1.0]

### Adicionado

- Estrutura inicial do projeto.
- Loader CSV.
- Configurações iniciais.
- Testes do Loader.
- Documentação inicial.
