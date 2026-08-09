"""Cálculos internos reutilizáveis das médias móveis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_wma(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula uma Média Móvel Ponderada sobre uma série numérica.

    Parameters
    ----------
    series:
        Série numérica usada no cálculo.

    period:
        Quantidade de períodos da média.

    Returns
    -------
    pd.Series
        Série contendo os valores da WMA.
    """
    weights = np.arange(
        1,
        period + 1,
        dtype=float,
    )

    return (
        series
        .rolling(
            window=period,
            min_periods=period,
        )
        .apply(
            lambda values: np.dot(values, weights) / weights.sum(),
            raw=True,
        )
    )
