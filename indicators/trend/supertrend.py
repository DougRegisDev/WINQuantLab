"""SuperTrend indicator."""

from __future__ import annotations

import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import (
    calculate_average_true_range,
    calculate_true_range,
)


def supertrend(
    dataframe: pd.DataFrame,
    period: int = 10,
    multiplier: float = 3.0,
) -> pd.DataFrame:
    """
    Calculate the SuperTrend indicator.

    Parameters
    ----------
    dataframe:
        Input OHLC DataFrame.

    period:
        ATR period.

    multiplier:
        ATR multiplier used to build the bands.

    Returns
    -------
    pd.DataFrame
        Copy of the DataFrame containing the SuperTrend columns.
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

    if multiplier <= 0:
        raise ValueError(
            "multiplier deve ser maior que zero."
        )

    result = dataframe.copy()

    true_range = calculate_true_range(
        high=result["high"],
        low=result["low"],
        close=result["close"],
    )

    average_true_range = calculate_average_true_range(
        true_range=true_range,
        period=period,
    )

    middle_price = (
        result["high"]
        + result["low"]
    ) / 2

    basic_upper_band = (
        middle_price
        + multiplier * average_true_range
    )

    basic_lower_band = (
        middle_price
        - multiplier * average_true_range
    )

    final_upper_band = pd.Series(
        index=result.index,
        dtype=float,
    )

    final_lower_band = pd.Series(
        index=result.index,
        dtype=float,
    )

    supertrend_line = pd.Series(
        index=result.index,
        dtype=float,
    )

    direction = pd.Series(
        index=result.index,
        dtype=float,
    )

    for position in range(len(result)):
        current_upper = basic_upper_band.iloc[position]
        current_lower = basic_lower_band.iloc[position]

        if pd.isna(current_upper) or pd.isna(current_lower):
            continue

        if (
            position == 0
            or pd.isna(final_upper_band.iloc[position - 1])
            or pd.isna(final_lower_band.iloc[position - 1])
        ):
            final_upper_band.iloc[position] = current_upper
            final_lower_band.iloc[position] = current_lower

            supertrend_line.iloc[position] = current_upper
            direction.iloc[position] = -1

            continue

        previous_close = result["close"].iloc[position - 1]

        previous_upper = final_upper_band.iloc[position - 1]
        previous_lower = final_lower_band.iloc[position - 1]

        if (
            current_upper < previous_upper
            or previous_close > previous_upper
        ):
            final_upper_band.iloc[position] = current_upper
        else:
            final_upper_band.iloc[position] = previous_upper

        if (
            current_lower > previous_lower
            or previous_close < previous_lower
        ):
            final_lower_band.iloc[position] = current_lower
        else:
            final_lower_band.iloc[position] = previous_lower

        previous_supertrend = supertrend_line.iloc[position - 1]
        current_close = result["close"].iloc[position]

        if previous_supertrend == previous_upper:
            if current_close <= final_upper_band.iloc[position]:
                supertrend_line.iloc[position] = (
                    final_upper_band.iloc[position]
                )

                direction.iloc[position] = -1

            else:
                supertrend_line.iloc[position] = (
                    final_lower_band.iloc[position]
                )

                direction.iloc[position] = 1

        elif previous_supertrend == previous_lower:
            if current_close >= final_lower_band.iloc[position]:
                supertrend_line.iloc[position] = (
                    final_lower_band.iloc[position]
                )

                direction.iloc[position] = 1

            else:
                supertrend_line.iloc[position] = (
                    final_upper_band.iloc[position]
                )

                direction.iloc[position] = -1

    multiplier_label = f"{multiplier:g}"

    result["basic_upper_band"] = basic_upper_band
    result["basic_lower_band"] = basic_lower_band

    result["final_upper_band"] = final_upper_band
    result["final_lower_band"] = final_lower_band

    result[
        f"supertrend_{period}_{multiplier_label}"
    ] = supertrend_line

    result[
        f"supertrend_direction_{period}_{multiplier_label}"
    ] = direction

    return result
