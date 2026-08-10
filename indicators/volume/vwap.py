"""Volume Weighted Average Price (VWAP) indicator."""

from __future__ import annotations

import pandas as pd


def vwap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the Volume Weighted Average Price (VWAP).

    Parameters
    ----------
    df:
        DataFrame containing the columns ``high``, ``low``,
        ``close`` and ``volume``.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with the ``vwap`` column added.

    Raises
    ------
    ValueError
        If any required column is missing.
    """
    required_columns = {
        "high",
        "low",
        "close",
        "volume",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = df.copy()

    typical_price = (
        result["high"]
        + result["low"]
        + result["close"]
    ) / 3

    price_volume = typical_price * result["volume"]

    cumulative_price_volume = price_volume.cumsum()
    cumulative_volume = result["volume"].cumsum()

    result["vwap"] = (
        cumulative_price_volume
        / cumulative_volume
    )

    return result
