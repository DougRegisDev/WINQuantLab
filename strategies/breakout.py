"""Breakout strategy."""

from __future__ import annotations

import pandas as pd


def breakout(
    df: pd.DataFrame,
    lookback: int = 20,
) -> pd.DataFrame:
    """
    Generate signals using a breakout strategy.

    Parameters
    ----------
    df:
        DataFrame containing market data.
    lookback:
        Number of previous candles used to calculate
        breakout levels.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with breakout
        levels and strategy signal column.

    Raises
    ------
    ValueError
        If lookback is less than or equal to zero.
        If a required market data column is missing.
    """
    if lookback <= 0:
        raise ValueError(
            "lookback must be greater than zero"
        )

    required_columns = (
        "high",
        "low",
        "close",
    )

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"The column '{column}' was not found"
            )

    result = df.copy()

    result["breakout_high"] = (
        result["high"]
        .rolling(window=lookback)
        .max()
        .shift(1)
    )

    result["breakout_low"] = (
        result["low"]
        .rolling(window=lookback)
        .min()
        .shift(1)
    )

    result["signal"] = 0

    buy_signal = (
        result["close"]
        > result["breakout_high"]
    )

    sell_signal = (
        result["close"]
        < result["breakout_low"]
    )

    result.loc[buy_signal, "signal"] = 1
    result.loc[sell_signal, "signal"] = -1

    return result
