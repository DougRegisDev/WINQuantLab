# ADR-004 — Arquitetura da Família de Médias Móveis

## Status

Aceito.

---

## Data

05/08/2026

---

## Contexto

O WINQuantLab iniciou sua biblioteca de indicadores técnicos com a implementação da Média Móvel Simples (SMA).

Durante a evolução do projeto foram adicionadas outras médias móveis:

- SMA
- EMA
- WMA
- HMA

Inicialmente cada indicador possuía sua própria implementação e suas próprias validações.

Com o crescimento da biblioteca observou-se que diversos algoritmos compartilhavam responsabilidades semelhantes.

Exemplos:

- validação de período;
- validação da coluna `close`;
- validação de tipos numéricos;
- criação de novas colunas;
- reutilização do algoritmo da WMA.

Essas duplicações aumentariam significativamente conforme novos indicadores fossem adicionados ao projeto.

---

## Problema

Cada novo indicador repetia parte do código já existente.

Exemplo:

```
SMA
├── valida período
├── valida close
└── calcula

EMA
├── valida período
├── valida close
└── calcula

WMA
├── valida período
├── valida close
└── calcula
```

Além da duplicação de validações, a implementação da HMA exigiria executar o algoritmo da WMA diversas vezes.

Duplicar esse algoritmo criaria maior risco de inconsistências futuras.

---

## Decisão

Foram adotadas duas decisões arquiteturais.

### 1. Centralização das validações

Foi criado o módulo:

```
core/
└── validations.py
```

Esse módulo concentra todas as validações reutilizáveis dos indicadores.

Atualmente estão disponíveis:

- `validate_period()`
- `validate_required_column()`
- `validate_numeric_column()`
- `validate_indicator_input()`

Todos os indicadores utilizam essas funções antes do cálculo.

---

### 2. Separação dos algoritmos internos

Foi criado o módulo:

```
indicators/
└── moving_averages/
    └── calculations.py
```

Esse módulo contém algoritmos internos compartilhados pela família de médias móveis.

Atualmente:

```
calculate_wma()
```

é utilizado por:

- WMA
- HMA

Sem duplicação de código.

---

## Estrutura adotada

```
moving_averages/

├── calculations.py
├── sma.py
├── ema.py
├── wma.py
├── hma.py
└── __init__.py
```

Cada arquivo possui responsabilidade única.

---

## API Pública

A API pública permanece simples.

Exemplo:

```python
from indicators.moving_averages import (
    sma,
    ema,
    wma,
    hma,
)
```

Os algoritmos internos permanecem ocultos ao usuário.

---

## Benefícios

A arquitetura escolhida proporciona:

- redução de duplicação;
- menor acoplamento;
- maior reutilização;
- testes menores;
- manutenção simplificada;
- facilidade para inclusão de novos indicadores;
- melhor organização do projeto.

---

## Impacto Futuro

Essa arquitetura facilitará a implementação de:

- DEMA
- TEMA
- KAMA
- VIDYA
- ZLEMA
- HMA adaptativas

bem como outros indicadores que reutilizem algoritmos existentes.

---

## Alternativas Consideradas

### Duplicar os algoritmos

Cada indicador implementaria seu próprio cálculo.

Essa alternativa foi rejeitada devido ao aumento da duplicação e do custo de manutenção.

---

### Criar uma classe base

Foi considerada a criação de uma classe abstrata para todos os indicadores.

Exemplo:

```python
class Indicator:
    ...
```

Essa abordagem foi descartada neste momento.

As implementações atuais são compostas por funções puras e não necessitam manter estado interno.

Caso o projeto evolua para um motor de execução de indicadores, essa decisão poderá ser revisitada.

---

## Consequências

### Positivas

- Código mais limpo.
- Melhor reutilização.
- Menor acoplamento.
- Evolução simplificada.
- Estrutura preparada para expansão.

### Negativas

- Maior quantidade de arquivos.
- Necessidade de conhecer a organização interna da biblioteca.

Essas desvantagens foram consideradas aceitáveis.

---

## Conclusão

A família de médias móveis passa a utilizar módulos especializados para algoritmos compartilhados e validações reutilizáveis.

Essa decisão estabelece o padrão arquitetural para todas as próximas famílias de indicadores do WINQuantLab.
