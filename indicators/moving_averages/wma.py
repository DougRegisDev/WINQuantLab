"""Implementação da Média Móvel Ponderada — WMA."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.moving_averages.calculations import calculate_wma


def wma(
    dataframe: pd.DataFrame,
    period: int = 9,
) -> pd.DataFrame:
    """
    Calcula a Média Móvel Ponderada dos preços de fechamento.

    Os valores mais recentes recebem pesos maiores.

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna numérica ``close``.

    period:
        Quantidade de períodos utilizada no cálculo.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame com a coluna ``wma_<periodo>``.

    Raises
    ------
    TypeError
        Quando o período não é inteiro ou a coluna ``close`` não é numérica.

    ValueError
        Quando o período é menor ou igual a zero ou a coluna ``close``
        não existe.
    """
    validate_indicator_input(
        dataframe,
        period,
    )

    result = dataframe.copy()

    result[f"wma_{period}"] = calculate_wma(
        result["close"],
        period,
    )

    return result
