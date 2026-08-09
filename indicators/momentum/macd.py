"""Implementação do Moving Average Convergence Divergence (MACD)."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import calculate_ema


def macd(
    dataframe: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> pd.DataFrame:
    """
    Calcula o Moving Average Convergence Divergence (MACD).

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna ``close``.

    fast_period:
        Período da EMA rápida.

    slow_period:
        Período da EMA lenta.

    signal_period:
        Período da EMA da linha de sinal.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame contendo:

        - macd
        - macd_signal
        - macd_histogram
    """
    validate_indicator_input(
        dataframe,
        fast_period,
    )

    validate_indicator_input(
        dataframe,
        slow_period,
    )

    validate_indicator_input(
        dataframe,
        signal_period,
    )

    if fast_period >= slow_period:
        raise ValueError(
            "fast_period deve ser menor que slow_period."
        )

    result = dataframe.copy()

    ema_fast = calculate_ema(
        result["close"],
        fast_period,
    )

    ema_slow = calculate_ema(
        result["close"],
        slow_period,
    )

    macd_line = ema_fast - ema_slow

    signal_line = calculate_ema(
        macd_line,
        signal_period,
    )

    histogram = macd_line - signal_line

    result["macd"] = macd_line

    result["macd_signal"] = signal_line

    result["macd_histogram"] = histogram

    return result
