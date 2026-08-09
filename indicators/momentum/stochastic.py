"""Implementação do Stochastic Oscillator."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import (
    calculate_rolling_max,
    calculate_rolling_min,
)


def stochastic(
    dataframe: pd.DataFrame,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame:
    """
    Calcula o Stochastic Oscillator.

    Parameters
    ----------
    dataframe:
        DataFrame contendo as colunas ``high``, ``low`` e ``close``.

    k_period:
        Período utilizado no cálculo da linha %K.

    d_period:
        Período utilizado na suavização da linha %D.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame contendo:

        - stochastic_k_<k_period>
        - stochastic_d_<k_period>_<d_period>
    """

    validate_indicator_input(
        dataframe,
        k_period,
    )

    validate_indicator_input(
        dataframe,
        d_period,
    )

    required_columns = [
        "high",
        "low",
        "close",
    ]

    for column in required_columns:
        if column not in dataframe.columns:
            raise ValueError(
                f"DataFrame deve conter a coluna '{column}'."
            )

    result = dataframe.copy()

    highest_high = calculate_rolling_max(
        result["high"],
        k_period,
    )

    lowest_low = calculate_rolling_min(
        result["low"],
        k_period,
    )

    denominator = highest_high - lowest_low

    k_line = (
        (
            result["close"]
            - lowest_low
        )
        / denominator
    ) * 100

    d_line = (
        k_line
        .rolling(
            window=d_period,
            min_periods=d_period,
        )
        .mean()
    )

    result[f"stochastic_k_{k_period}"] = k_line

    result[
        f"stochastic_d_{k_period}_{d_period}"
    ] = d_line

    return result
