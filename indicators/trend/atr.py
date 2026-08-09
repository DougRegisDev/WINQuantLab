"""Average True Range (ATR)."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import (
    calculate_average_true_range,
    calculate_true_range,
)


def atr(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """
    Calculate the Average True Range (ATR).

    Parameters
    ----------
    dataframe:
        Input OHLC DataFrame.

    period:
        ATR period.

    Returns
    -------
    pd.DataFrame
        Copy of the DataFrame containing the ``atr_<period>`` column.

    Raises
    ------
    TypeError
        If the period is not an integer or required price data is invalid.

    ValueError
        If the period is less than or equal to zero or a required
        OHLC column is missing.
    """
    validate_indicator_input(
        dataframe,
        period,
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

    true_range = calculate_true_range(
        high=result["high"],
        low=result["low"],
        close=result["close"],
    )

    result[f"atr_{period}"] = calculate_average_true_range(
        true_range=true_range,
        period=period,
    )

    return result
