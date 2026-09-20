"""Moving Average Crossover strategy."""

from __future__ import annotations

import pandas as pd

from indicators.moving_averages.sma import sma


def moving_average_crossover(
    df: pd.DataFrame,
    fast_period: int = 9,
    slow_period: int = 21,
) -> pd.DataFrame:
    """
    Generate signals using a moving average crossover strategy.

    Parameters
    ----------
    df:
        DataFrame containing market data.
    fast_period:
        Period used by the fast moving average.
    slow_period:
        Period used by the slow moving average.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with the moving averages
        and strategy signal column.

    Raises
    ------
    ValueError
        If fast_period is greater than or equal to slow_period.
    """
    if fast_period >= slow_period:
        raise ValueError(
            "fast_period must be smaller than slow_period"
        )

    result = df.copy()

    result = sma(
        result,
        period=fast_period,
    )

    result = sma(
        result,
        period=slow_period,
    )

    fast_column = f"sma_{fast_period}"
    slow_column = f"sma_{slow_period}"

    result["signal"] = 0

    buy_signal = (
        (result[fast_column] > result[slow_column])
        & (
            result[fast_column].shift(1)
            <= result[slow_column].shift(1)
        )
    )

    sell_signal = (
        (result[fast_column] < result[slow_column])
        & (
            result[fast_column].shift(1)
            >= result[slow_column].shift(1)
        )
    )

    result.loc[buy_signal, "signal"] = 1
    result.loc[sell_signal, "signal"] = -1

    return result
