"""Financial Volume indicator."""

from __future__ import annotations

import pandas as pd


def financial_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the financial volume.

    Parameters
    ----------
    df:
        DataFrame containing the columns ``close`` and ``volume``.

    Returns
    -------
    pd.DataFrame
        Copy of the original DataFrame with the
        ``financial_volume`` column added.

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

    result["financial_volume"] = (
        result["close"] * result["volume"]
    )

    return result
