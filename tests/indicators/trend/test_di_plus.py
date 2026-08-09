"""Tests for the Positive Directional Indicator (+DI)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.trend.di_plus import di_plus


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


def test_di_plus_creates_column() -> None:
    """DI+ should create the output column."""
    dataframe = create_dataframe()

    result = di_plus(
        dataframe,
        period=3,
    )

    assert "di_plus_3" in result.columns


def test_di_plus_preserves_original_dataframe() -> None:
    """DI+ must not modify the original DataFrame."""
    dataframe = create_dataframe()
    original = dataframe.copy(deep=True)

    di_plus(
        dataframe,
        period=3,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_di_plus_invalid_period() -> None:
    """DI+ should reject invalid periods."""
    dataframe = create_dataframe()

    with pytest.raises(ValueError):
        di_plus(
            dataframe,
            period=0,
        )


def test_di_plus_missing_high_column() -> None:
    """DI+ requires the high column."""
    dataframe = create_dataframe().drop(
        columns=["high"],
    )

    with pytest.raises(ValueError):
        di_plus(dataframe)


def test_di_plus_missing_low_column() -> None:
    """DI+ requires the low column."""
    dataframe = create_dataframe().drop(
        columns=["low"],
    )

    with pytest.raises(ValueError):
        di_plus(dataframe)


def test_di_plus_missing_close_column() -> None:
    """DI+ requires the close column."""
    dataframe = create_dataframe().drop(
        columns=["close"],
    )

    with pytest.raises(ValueError):
        di_plus(dataframe)
