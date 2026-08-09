"""Implementação do indicador Momentum."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.momentum.calculations import calculate_previous_values


def momentum(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """
    Calcula o indicador Momentum.

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna ``close``.

    period:
        Quantidade de períodos utilizada no cálculo.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame contendo a coluna
        ``momentum_<period>``.
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

    result[f"momentum_{period}"] = (
        result["close"]
        - previous
    )

    return result
