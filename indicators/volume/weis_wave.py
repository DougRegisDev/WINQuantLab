"""Weis Wave Volume indicator."""

from __future__ import annotations

import pandas as pd


def weis_wave(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the Weis Wave Volume indicator.

    Parameters
    ----------
    df:
        DataFrame containing the columns ``close`` and ``volume``.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with the Weis Wave columns added.

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
        result["weis_wave_direction"] = pd.Series(dtype=int)
        result["weis_wave_volume"] = pd.Series(dtype=float)
        return result

    directions = [0]
    wave_volumes = [float(result["volume"].iloc[0])]

    wave_direction = 0

    for i in range(1, len(result)):
        current_close = result["close"].iloc[i]
        previous_close = result["close"].iloc[i - 1]
        current_volume = result["volume"].iloc[i]

        if current_close > previous_close:
            current_direction = 1
        elif current_close < previous_close:
            current_direction = -1
        else:
            current_direction = 0

        if current_direction == 0:
            directions.append(wave_direction)

            current_wave_volume = (
                wave_volumes[-1] + current_volume
            )

        elif wave_direction == 0:
            wave_direction = current_direction
            directions.append(wave_direction)

            current_wave_volume = (
                wave_volumes[-1] + current_volume
            )

        elif current_direction == wave_direction:
            directions.append(wave_direction)

            current_wave_volume = (
                wave_volumes[-1] + current_volume
            )

        else:
            wave_direction = current_direction
            directions.append(wave_direction)

            current_wave_volume = current_volume

        wave_volumes.append(float(current_wave_volume))

    result["weis_wave_direction"] = directions
    result["weis_wave_volume"] = wave_volumes

    return result
