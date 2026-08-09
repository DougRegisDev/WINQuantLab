"""Average Directional Index (ADX)."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import (
    calculate_average_true_range,
    calculate_directional_index,
    calculate_directional_movement,
    calculate_true_range,
    calculate_wilder_average,
)


def adx(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """
    Calculate the Average Directional Index (ADX).

    Parameters
    ----------
    dataframe:
        Input OHLC DataFrame.

    period:
        Number of periods used in the calculation.

    Returns
    -------
    pd.DataFrame
        Copy of the DataFrame containing the ``adx_<period>`` column.

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

    positive_dm, negative_dm = calculate_directional_movement(
        high=result["high"],
        low=result["low"],
    )

    true_range = calculate_true_range(
        high=result["high"],
        low=result["low"],
        close=result["close"],
    )

    smoothed_positive_dm = calculate_wilder_average(
        positive_dm,
        period,
    )

    smoothed_negative_dm = calculate_wilder_average(
        negative_dm,
        period,
    )

    average_true_range = calculate_average_true_range(
        true_range,
        period,
    )

    positive_di = (
        smoothed_positive_dm
        / average_true_range
    ) * 100

    negative_di = (
        smoothed_negative_dm
        / average_true_range
    ) * 100

    directional_index = calculate_directional_index(
        positive_di=positive_di,
        negative_di=negative_di,
    )

    result[f"adx_{period}"] = calculate_wilder_average(
        directional_index,
        period,
    )

    return result
