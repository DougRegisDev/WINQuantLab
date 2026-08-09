"""Implementação da Média Móvel Exponencial — EMA."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import calculate_ema


def ema(
    dataframe: pd.DataFrame,
    period: int = 9,
) -> pd.DataFrame:
    """
    Calcula a Média Móvel Exponencial dos preços de fechamento.

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna numérica ``close``.

    period:
        Quantidade de períodos utilizada no cálculo.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame com a coluna ``ema_<periodo>``.

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

    result[f"ema_{period}"] = calculate_ema(
        result["close"],
        period,
    )

    return result
