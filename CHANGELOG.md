# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

O formato segue o padrão **Keep a Changelog** e utiliza **Versionamento Semântico (SemVer)**.

---

## [Não publicado]

### Alterado

- Iniciado o desenvolvimento da versão 0.9.0.

## [0.8.0] - 2026-09-30

### Adicionado

#### Backtesting Multi-Sessão

- Implementado pipeline de execução de backtests multi-sessão.
- Implementada separação automática dos dados por sessão.
- Implementada execução independente da estratégia e do backtesting por sessão.
- Implementada associação dos trades às respectivas sessões.
- Implementada preservação de sessões sem trades.
- Implementado resumo estatístico por sessão.
- Implementada consolidação dos resultados no resumo do período.
- Implementadas contagens de sessões, candles, trades, direções e resultados.
- Implementada consolidação do PnL em pontos.
- Implementado cálculo de MFE e MAE médios a partir dos trades individuais.
- Implementado cálculo de MFE e MAE medianos.
- Implementados percentis P25, P50 e P75 para MFE e MAE.
- Implementadas estatísticas de duração dos trades: média, mediana e percentis P25, P50 e P75.
- Implementados valores mínimo e máximo para as distribuições de MFE e MAE.
- Implementada segmentação por resultado dos trades, com contagem e médias de MFE, MAE e duração para `win`, `loss` e `even`.

#### Integração com Dados do Profit

- Implementada integração do pipeline de backtesting com arquivos CSV exportados pelo Profit.
- Integrado carregamento, normalização, estratégia e backtesting em um fluxo completo de execução.
- Validado o pipeline utilizando dados reais de mercado.

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

#### Estratégias

- Criada a camada inicial de estratégias.
- Implementada a estratégia Moving Average Crossover.
- Implementada a estratégia Breakout.
- Implementada composição interna dos indicadores necessários pelas estratégias.
- Definida convenção de sinais:
  - `1` para sinal de compra.
  - `0` para ausência de novo sinal.
  - `-1` para sinal de venda.
- Definido `signal` como evento e não como estado de posição.
- Preservado o DataFrame original durante a execução das estratégias.

#### Moving Average Crossover

- Implementado cálculo interno das médias móveis simples rápida e lenta.
- Implementada geração de sinal de compra no cruzamento da média rápida de baixo para cima da média lenta.
- Implementada geração de sinal de venda no cruzamento da média rápida de cima para baixo da média lenta.
- Evitada geração repetida de sinais enquanto as médias permanecem na mesma relação.
- Implementada validação de que `fast_period` deve ser menor que `slow_period`.
- Mantidas no indicador SMA as validações específicas dos períodos.
- Implementado comportamento para DataFrame vazio.
- Implementado tratamento da ausência da coluna obrigatória `close`.
- Impedida geração de sinais durante o período de aquecimento das médias.
- Preservado o DataFrame original por meio de cópia antes dos cálculos.

#### Breakout

- Implementada estratégia de rompimento baseada em máximas e mínimas anteriores.
- Implementado parâmetro configurável `lookback`.
- Implementado cálculo de `breakout_high` utilizando a maior máxima das N velas anteriores.
- Implementado cálculo de `breakout_low` utilizando a menor mínima das N velas anteriores.
- Excluída a vela atual do cálculo dos níveis de rompimento.
- Implementada confirmação de rompimento pelo preço de fechamento (`close`).
- Implementado sinal de compra (`1`) quando `close` rompe `breakout_high`.
- Implementado sinal de venda (`-1`) quando `close` rompe `breakout_low`.
- Mantido sinal neutro (`0`) quando não ocorre rompimento confirmado.
- Impedida geração de sinal quando o fechamento apenas toca o nível.
- Impedida geração de sinal quando apenas o pavio rompe o nível.
- Implementada validação de `lookback`.
- Implementadas validações das colunas obrigatórias `high`, `low` e `close`.
- Implementado tratamento para DataFrame vazio.
- Impedida geração de sinais durante o período de aquecimento.
- Preservado o DataFrame original por meio de cópia antes dos cálculos.

#### Backtesting Engine

- Criada a camada inicial de Backtesting.
- Implementado motor de execução por meio de `backtest()`.
- Implementada execução de sinais no `open` do candle seguinte.
- Implementados os estados operacionais FLAT, LONG e SHORT.
- Implementada abertura de posições LONG a partir de `signal = 1`.
- Implementada abertura de posições SHORT a partir de `signal = -1`.
- Implementado encerramento de posições LONG por sinal contrário.
- Implementado encerramento de posições SHORT por sinal contrário.
- Impedida reversão automática de posição.
- Impedida piramidação por sinais repetidos na mesma direção.
- Definida quantidade inicial fixa em `quantity = 1`.
- Implementado cálculo de resultado em pontos para operações LONG.
- Implementado cálculo de resultado em pontos para operações SHORT.
- Implementado suporte a múltiplos trades sequenciais.
- Implementado encerramento forçado de posições abertas no `close` do último candle.
- Impedida execução de sinais presentes no último candle quando não existe próximo `open`.
- Implementadas validações das colunas obrigatórias `open`, `high`, `low`, `close` e `signal`.
- Implementada validação dos valores permitidos para `signal`: `-1`, `0` e `1`.
- Implementada rejeição de valores `NaN` em `signal`.
- Implementado tratamento para DataFrame vazio e séries contendo apenas um candle.
- Preservado o DataFrame original durante a execução do backtest.
- Implementado suporte a índices personalizados sem alterar a indexação posicional dos trades.
- Implementada preservação de `entry_time` e `exit_time` quando utilizado `DatetimeIndex`.
- Implementado registro estruturado de `direction`, `entry_index`, `entry_price`, `exit_index`, `exit_price`, `quantity` e `pnl_points`.
- Implementado cálculo de Maximum Favorable Excursion (`mfe_points`) para LONG e SHORT.
- Implementado cálculo de Maximum Adverse Excursion (`mae_points`) para LONG e SHORT.
- Implementado registro de `favorable_price` e `adverse_price`.
- Implementado registro de `mfe_index` e `mae_index`, utilizando a primeira ocorrência quando o mesmo extremo se repete.
- Implementada janela de observação limitada ao período em que a posição esteve efetivamente ativa.
- Incluído o candle final nos cálculos de excursão quando ocorre fechamento forçado no último `close`.
- Excluído o candle de saída dos cálculos de excursão quando a posição é encerrada no próximo `open`.
- Implementada classificação de `outcome` em `win`, `loss` e `even`, determinada exclusivamente por `pnl_points`.
- Implementado `duration_candles` como quantidade de candles em que a posição permaneceu efetivamente ativa.

#### Analytics de Backtesting

- Implementado resumo consolidado de backtest por período.
- Implementada análise de duração dos trades.
- Implementadas distribuições estatísticas de MFE e MAE.
- Implementados valores mínimo, máximo, média, mediana e percentis.
- Implementada análise segmentada por `win`, `loss` e `even`.
- Implementada consolidação das métricas dos trades executados em múltiplas sessões.
- Refatorado o pipeline de analytics para simplificar a consolidação dos resultados.

#### Relatório Textual

- Criada a camada `reports`.
- Implementado relatório textual por meio de `create_text_report()`.
- Implementada apresentação das métricas consolidadas do backtest.
- Implementada apresentação das métricas de excursão, duração e resultado.
- Implementada formatação dos parâmetros utilizados na execução.
- Padronizada a formatação numérica das métricas do relatório.

#### Interface de Linha de Comando

- Implementada interface de linha de comando para execução de backtests.
- Adicionado comando `winquantlab backtest`.
- Implementado suporte à seleção de estratégia pela CLI.
- Implementado suporte aos parâmetros específicos das estratégias.
- Integrado o fluxo de carregamento, normalização, estratégia, backtesting e relatório.
- Configurado entry point `winquantlab`.

#### Packaging

- Configurado `pyproject.toml` como fonte de metadados do projeto.
- Definidas dependências de execução.
- Definidas dependências opcionais de desenvolvimento.
- Configurado setuptools para empacotamento do projeto.
- Configurada instalação editável para desenvolvimento.
- Configurado entry point da CLI.
- Preparada a versão de desenvolvimento `0.8.0.dev0`.

#### API Pública

- Criado o pacote de fachada `winquantlab`.
- Criada API pública estável para acesso às principais funcionalidades da biblioteca.
- Expostos `load_data` e `normalize`.
- Expostas as médias móveis SMA, EMA, WMA e HMA.
- Expostos RSI, MACD, Momentum, ROC e Stochastic.
- Expostos ADX, ATR, DI+, DI-, Parabolic SAR e SuperTrend.
- Expostos Volume Financeiro, OBV, VWAP e Weis Wave.
- Expostas as estratégias Breakout e Moving Average Crossover.
- Expostos `backtest()` e `run_sessions()`.
- Exposto `create_text_report()`.
- Implementado `__version__` utilizando os metadados instalados do pacote.
- Definido `__all__` como contrato explícito da API pública.
- Mantidos helpers e detalhes internos de implementação fora da fachada pública.

#### Testes

Adicionados e expandidos testes automatizados para indicadores, estratégias, backtesting, analytics, relatórios, CLI, packaging e API pública.

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

O Moving Average Crossover possui 12 testes cobrindo:

- Criação da coluna `signal`.
- Cálculo interno das médias móveis rápida e lenta.
- Geração de sinal de compra.
- Geração de sinal de venda.
- Sinal tratado como evento e não como posição.
- Preservação do DataFrame original.
- Rejeição de períodos iguais.
- Rejeição de `fast_period` maior que `slow_period`.
- Propagação de erro para período inválido do indicador.
- DataFrame vazio.
- Ausência da coluna `close`.
- Ausência de sinais durante o período de aquecimento.

O Breakout possui 17 testes cobrindo:

- Criação das colunas `breakout_high`, `breakout_low` e `signal`.
- Cálculo da máxima das velas anteriores.
- Cálculo da mínima das velas anteriores.
- Geração de sinal de compra.
- Geração de sinal de venda.
- Ausência de sinal quando o fechamento apenas toca o nível.
- Preservação do DataFrame original.
- Rejeição de `lookback` igual a zero.
- Rejeição de `lookback` negativo.
- Ausência da coluna `high`.
- Ausência da coluna `low`.
- Ausência da coluna `close`.
- Ausência de sinais durante o período de aquecimento.
- DataFrame vazio.
- Ausência de sinal quando apenas o pavio rompe os níveis.
- Ausência de sinal quando o fechamento permanece dentro da faixa.
- Aceitação de `lookback=1`.

O Backtesting Engine possui 49 testes cobrindo:

- Ausência de trades quando não existem sinais.
- Execução de LONG no `open` do candle seguinte.
- Encerramento de LONG no final da sessão.
- Cálculo de resultado positivo e negativo para LONG.
- Execução de SHORT no `open` do candle seguinte.
- Cálculo de resultado para SHORT.
- Encerramento de LONG por sinal contrário.
- Encerramento de SHORT por sinal contrário.
- Ausência de reversão automática.
- Rejeição de piramidação em LONG.
- Rejeição de piramidação em SHORT.
- Execução de múltiplos trades sequenciais.
- Ausência de execução para sinal no último candle.
- Tratamento de DataFrame vazio.
- Ausência da coluna `signal`.
- Ausência da coluna `open`.
- Ausência da coluna `close`.
- Preservação do DataFrame original.
- Encerramento de posição aberta no último candle.
- Comportamento com apenas um candle.
- Rejeição de valores inválidos em `signal`.
- Rejeição de `NaN` em `signal`.
- Suporte a índice personalizado.
- Preservação de `entry_time` e `exit_time` com `DatetimeIndex`.
- Preservação de `exit_time` em encerramento por sinal contrário.
- Validação das colunas obrigatórias `high` e `low`.
- Cálculo de MFE para operações LONG e SHORT.
- Cálculo de MAE para operações LONG e SHORT.
- Inclusão do último candle em MFE/MAE quando ocorre fechamento forçado.
- Registro de `favorable_price` e `adverse_price`.
- Registro de `mfe_index` e `mae_index`.
- Primeira ocorrência como convenção para extremos repetidos.
- Classificação de resultado como `win`, `loss` ou `even`.
- Independência entre `outcome` e as excursões MFE/MAE.
- Cálculo de `duration_candles` em saída por sinal contrário.
- Cálculo de `duration_candles` em fechamento forçado.

Estado atual da suíte:

- 313 testes automatizados.
- 313 testes aprovados.
- 0 falhas.

#### Arquitetura

- Expandida a família `indicators.trend`.
- Criada e expandida a família `indicators.volume`.
- Mantida a separação entre famílias de indicadores.
- Introduzido indicador com cálculo stateful/iterativo por meio do Parabolic SAR.
- Introduzido cálculo ponderado por volume por meio do VWAP.
- Introduzido cálculo de volume financeiro por candle.
- Introduzido indicador de volume acumulativo por meio do OBV.
- Introduzido indicador stateful de volume por ondas direcionais por meio do Weis Wave.
- Mantida a arquitetura modular dos indicadores.
- Preservada a compatibilidade com os componentes existentes do projeto.
- Introduzida a camada de estratégias.
- Definido contrato inicial para estratégias.
- Definida separação entre geração de sinais e gerenciamento de posições.
- Definida composição de indicadores pelas estratégias sem duplicação dos cálculos.
- Registrada a arquitetura de estratégias no ADR-005.
- Adiada a criação de abstrações como Strategy base ou Protocol até que múltiplas estratégias demonstrem necessidade concreta.
- Introduzida a camada de Backtesting.
- Implementado Backtesting Engine independente das Strategies.
- Definida execução de sinais no `open` do candle seguinte para evitar lookahead bias.
- Definida máquina de estados inicial com FLAT, LONG e SHORT.
- Mantida separação entre geração de sinais, execução de operações e análise de resultados.
- Definido `signal` como evento consumido pelo Backtesting Engine.
- Evoluído o contrato estruturado de trades com métricas analíticas de excursão, duração e resultado.
- Mantida indexação posicional para `entry_index` e `exit_index`.
- Adicionada preservação opcional de informação temporal por meio de `entry_time` e `exit_time`.
- Registrada a arquitetura de Backtesting no ADR-006.
- Refinado o ADR-006 com a filosofia de medição analítica de trajetória de preço.
- Formalizada a distinção entre resultado final (`outcome`) e excursões favorável/adversa.
- Formalizada a janela ativa utilizada por MFE, MAE e duração do trade.
- Formalizada a primeira ocorrência como convenção para índices de extremos repetidos.
- Registrado o pipeline de execução de backtests no ADR-007.
- Formalizada a separação entre dados, estratégias, sinais, backtesting e relatórios.
- Introduzida fachada `winquantlab` como contrato público da biblioteca.
- Mantida a organização modular interna desacoplada da API pública.
- Centralizada a versão do pacote nos metadados definidos em `pyproject.toml`.

#### Qualidade

- Parabolic SAR desenvolvido utilizando TDD.
- VWAP desenvolvido utilizando TDD.
- Volume Financeiro desenvolvido utilizando TDD.
- OBV desenvolvido utilizando TDD.
- Weis Wave desenvolvido utilizando TDD.
- Moving Average Crossover desenvolvido utilizando TDD.
- Breakout desenvolvido utilizando TDD.
- Backtesting Engine V1 e evolução analítica V2 desenvolvidos utilizando TDD.
- Pipeline multi-sessão e analytics cobertos por testes automatizados.
- Relatório textual, CLI, packaging e API pública validados por testes.
- Validações de entrada adicionadas.
- Casos de borda cobertos por testes automatizados.
- Preservação dos dados de entrada verificada por testes.
- Projeto validado com Ruff.
- Código padronizado com Ruff Formatter.
- Suíte completa executada após as implementações.
- 313 testes aprovados.
- Nenhuma regressão identificada nos testes existentes.

### Alterado

- Evoluído o projeto de uma coleção de componentes de análise técnica para um fluxo integrado de análise quantitativa.
- Expandido o backtesting com execução multi-sessão e analytics de período.
- Padronizada a interface de execução por meio da CLI.
- Padronizado o empacotamento e a instalação do projeto.
- Definida uma API pública de alto nível por meio do pacote `winquantlab`.
- Atualizada a documentação principal para refletir a arquitetura e as funcionalidades atuais.

### Planejado

#### Indicadores

- Bollinger Bands.
- Donchian Channel.

#### Estratégias

- Pullback / Mean Reversion.
- Price Action.

#### Backtesting

- Otimização de parâmetros.

#### Relatórios

- Evolução dos formatos de relatório e visualização dos resultados.

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