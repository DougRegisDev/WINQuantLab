"""Tests for the Average True Range (ATR)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.trend.atr import atr


def create_dataframe() -> pd.DataFrame:
    """Create a sample OHLC DataFrame."""
    return pd.DataFrame(
        {
            "open": [10.0, 11.0, 12.0, 13.0, 14.0],
            "high": [11.0, 12.0, 13.0, 14.0, 15.0],
            "low": [9.0, 10.0, 11.0, 12.0, 13.0],
            "close": [10.0, 11.0, 12.0, 13.0, 14.0],
        }
    )


def test_atr_creates_column() -> None:
    """ATR should create the output column."""
    dataframe = create_dataframe()

    result = atr(
        dataframe,
        period=3,
    )

    assert "atr_3" in result.columns


def test_atr_preserves_original_dataframe() -> None:
    """ATR must not modify the original DataFrame."""
    dataframe = create_dataframe()
    original = dataframe.copy(deep=True)

    atr(
        dataframe,
        period=3,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_atr_invalid_period() -> None:
    """ATR should reject invalid periods."""
    dataframe = create_dataframe()

    with pytest.raises(ValueError):
        atr(
            dataframe,
            period=0,
        )


def test_atr_missing_high_column() -> None:
    """ATR requires the high column."""
    dataframe = create_dataframe().drop(
        columns=["high"],
    )

    with pytest.raises(ValueError):
        atr(dataframe)


def test_atr_missing_low_column() -> None:
    """ATR requires the low column."""
    dataframe = create_dataframe().drop(
        columns=["low"],
    )

    with pytest.raises(ValueError):
        atr(dataframe)


def test_atr_missing_close_column() -> None:
    """ATR requires the close column."""
    dataframe = create_dataframe().drop(
        columns=["close"],
    )

    with pytest.raises(ValueError):
        atr(dataframe)
