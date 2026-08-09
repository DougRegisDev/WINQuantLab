"""Implementação do indicador Rate of Change (ROC)."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.momentum.calculations import (
    calculate_previous_values,
)


def roc(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """
    Calcula o indicador Rate of Change (ROC).

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna ``close``.

    period:
        Quantidade de períodos utilizada na comparação.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame contendo a coluna
        ``roc_<period>``.

    Raises
    ------
    TypeError
        Quando o período não é inteiro ou a coluna ``close``
        não é numérica.

    ValueError
        Quando o período é menor ou igual a zero ou a coluna
        ``close`` não existe.
    """
    validate_indicator_input(
        dataframe,
        period,
    )

    result = dataframe.copy()

    previous = calculate_previous_values(
        result["close"],
        period,
    )

    result[f"roc_{period}"] = (
        (
            result["close"]
            / previous
        )
        - 1
    ) * 100

    return result
