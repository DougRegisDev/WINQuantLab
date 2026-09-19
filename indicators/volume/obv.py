"""On-Balance Volume (OBV) indicator."""

from __future__ import annotations

import pandas as pd


def obv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the On-Balance Volume (OBV).

    Parameters
    ----------
    df:
        DataFrame containing the columns ``close`` and ``volume``.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with the ``obv`` column added.

    Raises
    ------
    ValueError
        If any required column is missing.
    """
    required_columns = {
        "close",
        "volume",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = df.copy()

    if result.empty:
        result["obv"] = pd.Series(dtype=float)
        return result

    obv_values = [0.0]

    for i in range(1, len(result)):
        current_close = result["close"].iloc[i]
        previous_close = result["close"].iloc[i - 1]
        current_volume = result["volume"].iloc[i]

        previous_obv = obv_values[-1]

        if current_close > previous_close:
            current_obv = previous_obv + current_volume
        elif current_close < previous_close:
            current_obv = previous_obv - current_volume
        else:
            current_obv = previous_obv

        obv_values.append(float(current_obv))

    result["obv"] = obv_values

    return result
