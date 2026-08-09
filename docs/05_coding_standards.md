# WINQuantLab

> Biblioteca Python para pesquisa quantitativa aplicada ao mercado financeiro.

---

# Documento

Coding Standards

Versão: 1.0

Status: Em desenvolvimento

Última atualização: 2026-08-07

---

# 1. Objetivo

Este documento define os padrões de código adotados pelo WINQuantLab.

Seu objetivo é garantir consistência, legibilidade, facilidade de manutenção e previsibilidade em todos os módulos da biblioteca.

Todas as novas implementações deverão seguir estes padrões.

---

# 2. Estilo de Código

O projeto utiliza:

- Python 3.13+
- PEP 8
- Ruff
- Tipagem estática
- Docstrings no padrão NumPy

Todo código deverá ser compatível com essas ferramentas.

---

# 3. Idioma

## Código

Todo o código deverá ser escrito em inglês.

Exemplos:

```python
close
high
low
volume

calculate_ema()

validate_indicator_input()
```

---

## Documentação

Toda a documentação oficial será escrita em português.

Arquivos em `docs/` deverão permanecer em português.

Docstrings permanecerão em inglês, seguindo o padrão NumPy.

---

# 4. Convenção de Nomes

## Arquivos

Utilizar apenas letras minúsculas e underscore.

Exemplos:

```
moving_average.py

stochastic.py

calculations.py
```

---

## Classes

Utilizar PascalCase.

Exemplo:

```python
IndicatorBase
```

---

## Funções

Utilizar snake_case.

Exemplo:

```python
calculate_ema()

calculate_previous_values()

validate_indicator_input()
```

---

## Variáveis

Utilizar nomes descritivos.

Preferir:

```python
highest_high

previous_close

price_changes
```

Evitar:

```python
x

y

tmp

var
```

---

## Constantes

Utilizar UPPER_CASE.

Exemplo:

```python
DEFAULT_PERIOD
```

---

# 5. Organização dos Arquivos

A ordem padrão deverá ser:

```python
"""Module docstring."""

from __future__ import annotations

Bibliotecas padrão

Bibliotecas externas

Bibliotecas internas

Constantes

Classes

Funções
```

---

# 6. Docstrings

Todas as funções públicas deverão possuir docstrings.

Formato:

```python
def ema(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the Exponential Moving Average.

    Parameters
    ----------
    dataframe:
        Input market data.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the EMA.
    """
```

Docstrings deverão seguir o padrão NumPy.

---

# 7. Tipagem

Todo código novo deverá possuir tipagem explícita.

Exemplo:

```python
def calculate_ema(
    series: pd.Series,
    period: int,
) -> pd.Series:
```

Evitar:

```python
def calculate_ema(series, period):
```

---

# 8. DataFrames

Funções que recebem DataFrames não deverão modificar o objeto original.

Sempre utilizar:

```python
result = dataframe.copy()
```

O DataFrame original deverá permanecer inalterado.

---

# 9. Colunas dos Indicadores

Toda coluna criada deverá possuir nome descritivo.

Exemplos:

```
ema_20

sma_9

rsi_14

macd_line_12_26

macd_signal_12_26_9

stochastic_k_14

stochastic_d_14_3
```

Evitar abreviações que dificultem a leitura.

---

# 10. Validações

Toda função pública deverá validar seus parâmetros.

Exemplos:

- período maior que zero;
- colunas obrigatórias;
- tipos esperados.

Sempre reutilizar validações existentes antes de criar novas.

---

# 11. Reutilização

Antes de implementar qualquer cálculo, verificar se ele já existe.

A hierarquia oficial é:

```
Indicador

↓

Família

↓

Projeto
```

Funções reutilizadas deverão ser movidas apenas quando houver necessidade comprovada.

---

# 12. Testes

Toda funcionalidade deverá possuir testes automatizados.

No mínimo deverão existir testes para:

- funcionamento;
- parâmetros inválidos;
- ausência de colunas;
- preservação do DataFrame;
- cálculo matemático.

---

# 13. Imports

Organizar imports na seguinte ordem:

```python
from __future__ import annotations

Bibliotecas padrão

Bibliotecas externas

Bibliotecas internas
```

Não utilizar imports desnecessários.

---

# 14. Comentários

Comentários deverão explicar decisões.

Não deverão explicar código óbvio.

Evitar:

```python
i += 1
# incrementa i
```

Preferir:

```python
# Wilder utiliza suavização exponencial própria,
# diferente da EMA tradicional.
```

---

# 15. Tratamento de Erros

Sempre utilizar exceções específicas.

Preferir:

```python
raise ValueError(
    "Period must be greater than zero."
)
```

Evitar mensagens genéricas.

---

# 16. Performance

Legibilidade possui prioridade.

Otimizações somente deverão ser realizadas quando existir evidência de ganho relevante.

Evitar complexidade desnecessária em nome de pequenas melhorias de desempenho.

---

# 17. Compatibilidade

Mudanças em APIs públicas deverão preservar compatibilidade sempre que possível.

Quando uma quebra for inevitável, ela deverá ser documentada.

---

# 18. Qualidade

Antes de concluir qualquer funcionalidade verificar:

- Ruff sem erros.
- Testes aprovados.
- Tipagem correta.
- Docstrings completas.
- Código legível.
- Sem duplicação desnecessária.
- Documentação atualizada.

---

# 19. Objetivo Final

O código do WINQuantLab deverá ser compreensível por qualquer desenvolvedor Python com conhecimentos intermediários.

A prioridade da biblioteca é produzir código confiável, organizado e fácil de evoluir ao longo do tempo.
