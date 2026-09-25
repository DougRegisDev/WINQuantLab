# ADR-007 — Backtest Execution Pipeline

## Status

Accepted

## Context

O WINQuantLab possui componentes independentes para carregamento,
normalização, estratégias e backtesting.

O pipeline básico é:

Market Data
→ Loader
→ Normalizer
→ Strategy
→ Signals
→ Backtesting
→ Analysis

A integração com dados reais do Profit/Neologica demonstrou que esses
componentes já podem operar em conjunto.

Um arquivo real contendo dados de WINFUT entre 16/09/2024 e 16/09/2026
foi carregado e normalizado com sucesso.

O primeiro teste end-to-end foi realizado utilizando um único pregão,
16/09/2024, contendo 113 candles de 5 minutos.

A estratégia Breakout com lookback 20 produziu sinais reais que foram
processados pelo Backtesting V2.

Os trades resultantes tiveram PnL, MFE, MAE e duração auditados
diretamente contra os candles do mercado.

Essa integração revelou uma nova necessidade arquitetural.

Datasets reais podem conter múltiplos pregões, enquanto o mecanismo de
backtesting foi projetado para processar uma sessão de mercado por vez.

Executar diretamente um dataset contendo vários pregões permitiria que
uma posição permanecesse aberta artificialmente entre sessões.

Além disso, o objetivo do WINQuantLab não é apenas produzir trades, mas
permitir análise quantitativa do comportamento do preço após os sinais
de uma estratégia.

É necessário, portanto, definir uma camada responsável pela execução de
datasets multi-sessão e pela consolidação dos resultados.

---

## Decision

O WINQuantLab terá uma camada de execução responsável por coordenar o
pipeline completo de backtesting.

Essa camada ficará acima dos componentes existentes e não substituirá
suas responsabilidades individuais.

A arquitetura será:

Dataset
→ Loader
→ Normalizer
→ Session Split
→ Strategy
→ Signals
→ Backtesting
→ Session Results
→ Aggregate Analysis

---

## Multi-Session Datasets

O usuário poderá fornecer um dataset contendo múltiplas sessões de
mercado.

Por exemplo:

16/09/2024 → 16/09/2026

O usuário não precisará executar manualmente um backtest para cada dia.

Após a normalização, a camada de execução deverá identificar e separar
automaticamente as sessões presentes no dataset.

Cada sessão será processada independentemente.

Conceitualmente:

Dataset
→ Session 1
→ Session 2
→ Session 3
→ ...
→ Session N

Cada sessão será enviada individualmente para:

Strategy
→ Backtesting

---

## Session Isolation

Cada sessão começa sem posição aberta.

O estado inicial de cada sessão é:

FLAT

Uma posição nunca poderá atravessar artificialmente de uma sessão para
a próxima.

Caso uma posição permaneça aberta no final da sessão, o comportamento
definido pelo Backtesting continuará sendo aplicado:

a posição será encerrada no fechamento do último candle da sessão.

A próxima sessão começará novamente em estado FLAT.

Exemplo:

Session A
→ entrada LONG
→ nenhuma saída até o final
→ fechamento no último close
→ FLAT

Session B
→ começa FLAT

Essa regra preserva a independência entre pregões.

---

## Strategy Execution

A estratégia será executada separadamente para cada sessão.

A camada de execução fornecerá à estratégia somente os candles
pertencentes à sessão atual.

A estratégia continuará responsável exclusivamente por transformar
dados de mercado em eventos de sinal.

Ela não será responsável por:

- executar ordens;
- controlar posições;
- calcular PnL;
- calcular MFE;
- calcular MAE;
- controlar sessões;
- consolidar resultados.

Essas responsabilidades permanecem fora da camada de estratégia.

---

## Backtesting Responsibility

O mecanismo de backtesting continuará processando apenas uma sessão por
execução.

Ele não deverá conhecer:

- arquivos CSV;
- Profit/Neologica;
- datasets multi-sessão;
- relatórios globais;
- gerenciamento financeiro.

Seu contrato continuará sendo essencialmente:

DataFrame com OHLC + signal
→ trades

Essa decisão mantém o motor pequeno, previsível e testável.

---

## Result Hierarchy

Os resultados do pipeline serão organizados em três níveis.

### 1. Trade

O nível mais granular representa uma operação individual.

Cada trade preservará informações como:

- sessão;
- direção;
- índice de entrada;
- preço de entrada;
- índice de saída;
- preço de saída;
- quantidade;
- PnL em pontos;
- resultado;
- preço favorável;
- preço adverso;
- MFE em pontos;
- MAE em pontos;
- índice do MFE;
- índice do MAE;
- duração em candles.

Quando informações temporais estiverem disponíveis, poderão também ser
preservados os horários de entrada e saída.

A sessão deverá permanecer associada ao trade para permitir sua
identificação após a consolidação de múltiplos pregões.

---

### 2. Session Summary

Cada sessão deverá possuir um resumo próprio.

O resumo poderá incluir:

- data da sessão;
- quantidade de candles;
- quantidade total de trades;
- quantidade de trades LONG;
- quantidade de trades SHORT;
- trades positivos;
- trades negativos;
- trades zerados;
- PnL total em pontos;
- PnL médio por trade;
- MFE médio;
- MFE mediano;
- MAE médio;
- MAE mediano;
- duração média;
- duração mediana.

Sessões sem operações também deverão permanecer no resultado.

Exemplo:

Session
→ candles: 113
→ trades: 0
→ pnl_points: 0

Isso permite distinguir:

- sessões analisadas;
- sessões com operações;
- sessões sem operações.

---

### 3. Period Summary

Após o processamento de todas as sessões, os resultados serão
consolidados em um resumo do período completo.

O resumo global poderá incluir:

- início do período;
- fim do período;
- sessões analisadas;
- sessões com trades;
- sessões sem trades;
- candles analisados;
- trades totais;
- trades LONG;
- trades SHORT;
- trades positivos;
- trades negativos;
- trades zerados;
- PnL total em pontos;
- PnL médio;
- PnL mediano.

Também serão calculadas estatísticas de distribuição.

Para MFE:

- média;
- mediana;
- mínimo;
- máximo;
- percentis.

Para MAE:

- média;
- mediana;
- mínimo;
- máximo;
- percentis.

Para duração:

- média;
- mediana;
- mínimo;
- máximo;
- percentis.

Os percentis inicialmente relevantes poderão incluir:

- P25;
- P50;
- P75.

Novas estatísticas poderão ser adicionadas quando houver necessidade
analítica concreta.

---

## Outcome Segmentation

As estatísticas poderão ser segmentadas pelo resultado final dos trades.

Exemplo:

Trades positivos
→ quantidade
→ PnL médio
→ MFE médio
→ MFE mediano
→ MAE médio
→ MAE mediano

Trades negativos
→ quantidade
→ PnL médio
→ MFE médio
→ MFE mediano
→ MAE médio
→ MAE mediano

Essa segmentação permite estudar perguntas como:

- quanto trades vencedores normalmente andaram contra antes da saída;
- quanto trades perdedores chegaram a andar a favor antes da saída;
- qual foi a distribuição das excursões favoráveis;
- qual foi a distribuição das excursões adversas.

---

## Excursion Threshold Analysis

A camada analítica poderá calcular frequências de excursão.

Exemplos:

- quantidade de trades com MFE >= 100 pontos;
- quantidade de trades com MFE >= 200 pontos;
- quantidade de trades com MFE >= 300 pontos;
- percentual de trades que atingiram cada faixa;
- frequência dessas excursões entre trades positivos;
- frequência dessas excursões entre trades negativos.

O mesmo princípio poderá ser aplicado ao MAE.

Esses valores representam observações sobre o comportamento histórico
dos trades.

Eles não representam recomendações operacionais.

---

## Analytical Principle

O WINQuantLab é uma ferramenta de medição e análise.

Seu objetivo é responder:

"What happened with price after the strategy produced an entry and
while the trade remained active?"

O sistema deverá apresentar evidências quantitativas sobre o
comportamento observado após os sinais da estratégia.

Por exemplo:

- quanto o preço andou a favor;
- quanto o preço andou contra;
- quanto tempo a posição permaneceu ativa;
- como a operação terminou;
- com que frequência determinadas excursões ocorreram;
- como essas características se distribuem em grandes amostras.

O sistema não deverá transformar automaticamente essas observações em
decisões de trading.

---

## Risk Management Boundary

Decisões de gerenciamento de risco permanecem fora da responsabilidade
do WINQuantLab.

O sistema não deverá decidir ou recomendar automaticamente:

- stop loss;
- take profit;
- breakeven;
- trailing stop;
- tamanho de posição;
- número de contratos;
- capital necessário;
- risco financeiro por operação;
- risco percentual;
- gerenciamento de banca.

Por exemplo, o sistema poderá informar:

"42% dos trades que terminaram negativos apresentaram MFE >= 200
pontos."

Ele não deverá concluir:

"O stop deve ser movido para breakeven após 200 pontos."

A interpretação dessas evidências pertence ao usuário.

---

## Financial Layer

Uma camada financeira não faz parte desta decisão arquitetural.

O pipeline trabalhará prioritariamente com:

- preços;
- pontos;
- candles;
- frequência;
- duração;
- MFE;
- MAE;
- resultado da estratégia;
- distribuições estatísticas.

Não serão necessários neste estágio:

- saldo de conta;
- valor monetário do ponto;
- margem;
- custos operacionais;
- corretagem;
- tamanho de posição baseado em capital;
- retorno percentual sobre capital;
- Sharpe Ratio;
- métricas dependentes de gerenciamento financeiro.

Essas funcionalidades somente deverão ser consideradas no futuro caso
surja uma necessidade concreta.

---

## Separation of Responsibilities

A arquitetura resultante será:

Loader
→ lê os dados

Normalizer
→ transforma os dados para o schema do WINQuantLab

Execution Pipeline
→ identifica e separa sessões
→ coordena estratégia e backtesting

Strategy
→ produz sinais

Backtesting
→ executa os sinais de uma sessão
→ produz trades e medições

Analytics
→ resume trades
→ resume sessões
→ consolida o período completo
→ calcula distribuições e frequências

Essa separação evita que uma única camada concentre responsabilidades
não relacionadas.

---

## Initial Implementation Scope

A primeira implementação do pipeline deverá ser mínima.

Ela deverá priorizar:

1. receber dados normalizados;
2. separar os dados por sessão;
3. executar uma estratégia para cada sessão;
4. executar o backtesting para cada sessão;
5. associar cada trade à sessão correspondente;
6. preservar sessões sem trades;
7. consolidar os trades produzidos.

Os resumos estatísticos poderão ser implementados incrementalmente após
a execução multi-sessão estar corretamente testada.

Não será criada antecipadamente uma grande estrutura de relatórios.

---

## Testing Strategy

A implementação seguirá TDD.

Os primeiros testes deverão validar comportamento estrutural antes das
estatísticas avançadas.

Casos iniciais relevantes incluem:

- dataset contendo uma única sessão;
- dataset contendo múltiplas sessões;
- separação correta por data;
- cada sessão iniciando FLAT;
- posição não atravessando sessões;
- fechamento de posição no final da sessão;
- sessão sem sinais;
- sessão sem trades preservada;
- trades associados à sessão correta;
- dataset preservado sem mutação.

Somente após essas regras estarem estáveis deverão ser adicionados
testes para agregações e distribuições.

---

## Consequences

### Positive

- datasets de longos períodos podem ser analisados automaticamente;
- o usuário não precisa executar cada pregão manualmente;
- posições não atravessam sessões artificialmente;
- o backtester permanece simples;
- estratégias permanecem independentes da execução;
- trades individuais continuam auditáveis;
- análises diárias e globais podem coexistir;
- grandes amostras podem ser estudadas estatisticamente;
- gerenciamento de risco permanece uma decisão humana.

### Negative

- uma nova camada de coordenação será necessária;
- resultados multi-sessão exigirão estruturas adicionais;
- estatísticas agregadas aumentarão gradualmente a superfície de testes;
- diferentes mercados poderão futuramente exigir definições de sessão
  mais sofisticadas.

Essas consequências são aceitas em troca de uma arquitetura explícita e
testável.

---

## Deferred Decisions

Permanecem fora do escopo desta ADR:

- múltiplas posições simultâneas;
- pyramiding;
- reversão automática;
- múltiplos contratos;
- saídas parciais;
- stop loss automático;
- take profit automático;
- trailing stop;
- custos;
- slippage;
- margem;
- gerenciamento financeiro;
- otimização automática de parâmetros;
- recomendação automática de gerenciamento de risco;
- geração automática de regras de trading.

Também não será definida antecipadamente uma abstração complexa para
calendários ou sessões de diferentes bolsas.

Essas decisões serão tomadas somente quando casos reais exigirem.

---

## Final Principle

O pipeline de execução transforma um dataset multi-sessão em evidência
quantitativa organizada.

A hierarquia fundamental será:

Trade
→ Session
→ Period

O WINQuantLab mede.

O usuário interpreta.

O gerenciamento de risco permanece uma decisão humana.

---

## Implementation Status

A primeira etapa do pipeline multi-sessão foi implementada em
`backtesting/pipeline.py`.

O pipeline atualmente:

- recebe dados de mercado normalizados;
- separa automaticamente os dados por data de sessão;
- ordena os candles de cada sessão por `datetime`;
- reinicia o índice de cada sessão;
- executa a estratégia independentemente em cada sessão;
- executa o backtesting independentemente em cada sessão;
- associa cada trade à sessão correspondente;
- preserva sessões sem trades;
- produz resumos individuais por sessão;
- consolida os resultados no resumo do período.

O resumo de sessão atualmente inclui:

- quantidade de candles;
- quantidade de trades;
- trades LONG e SHORT;
- trades positivos, negativos e zerados;
- PnL total em pontos;
- MFE total;
- MAE total;
- MFE médio;
- MAE médio.

O resumo do período atualmente inclui:

- sessões analisadas;
- sessões com trades;
- sessões sem trades;
- candles analisados;
- trades totais;
- trades LONG e SHORT;
- trades positivos, negativos e zerados;
- PnL total em pontos;
- MFE médio;
- MAE médio;
- MFE mediano;
- MAE mediano;
- P25, P50 e P75 de MFE;
- P25, P50 e P75 de MAE.

As estatísticas do período são calculadas a partir dos trades individuais
consolidados, e não a partir de médias das sessões. Dessa forma, cada trade
possui o mesmo peso estatístico independentemente da quantidade de operações
existente em cada sessão.

Estatísticas adicionais previstas nesta ADR, como mínimo, máximo, duração,
segmentação por resultado e frequências de excursão, permanecem para
implementação incremental posterior.

A implementação continua seguindo o princípio:

O WINQuantLab mede.

O usuário interpreta.
