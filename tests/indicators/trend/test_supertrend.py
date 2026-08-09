"""Tests for the SuperTrend indicator."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.trend.supertrend import supertrend


def create_dataframe() -> pd.DataFrame:
    """Create a sample OHLC DataFrame."""
    return pd.DataFrame(
        {
            "open": [
                10.0,
                11.0,
                12.0,
                13.0,
                12.0,
                14.0,
                15.0,
                14.0,
            ],
            "high": [
                11.0,
                12.0,
                13.0,
                14.0,
                13.0,
                15.0,
                16.0,
                15.0,
            ],
            "low": [
                9.0,
                10.0,
                11.0,
                12.0,
                10.0,
                13.0,
                14.0,
                12.0,
            ],
            "close": [
                10.0,
                11.0,
                12.0,
                13.0,
                11.0,
                14.0,
                15.0,
                13.0,
            ],
        }
    )


def test_supertrend_creates_columns() -> None:
    """SuperTrend should create value and direction columns."""
    dataframe = create_dataframe()

    result = supertrend(
        dataframe,
        period=3,
        multiplier=2.0,
    )

    assert "supertrend_3_2" in result.columns
    assert "supertrend_direction_3_2" in result.columns


def test_supertrend_preserves_original_dataframe() -> None:
    """SuperTrend must not modify the original DataFrame."""
    dataframe = create_dataframe()
    original = dataframe.copy(deep=True)

    supertrend(
        dataframe,
        period=3,
        multiplier=2.0,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_supertrend_invalid_period() -> None:
    """SuperTrend should reject invalid periods."""
    dataframe = create_dataframe()

    with pytest.raises(ValueError):
        supertrend(
            dataframe,
            period=0,
            multiplier=2.0,
        )


def test_supertrend_invalid_multiplier() -> None:
    """SuperTrend should reject invalid multipliers."""
    dataframe = create_dataframe()

    with pytest.raises(ValueError):
        supertrend(
            dataframe,
            period=3,
            multiplier=0.0,
        )


def test_supertrend_missing_high_column() -> None:
    """SuperTrend requires the high column."""
    dataframe = create_dataframe().drop(
        columns=["high"],
    )

    with pytest.raises(ValueError):
        supertrend(dataframe)


def test_supertrend_missing_low_column() -> None:
    """SuperTrend requires the low column."""
    dataframe = create_dataframe().drop(
        columns=["low"],
    )

    with pytest.raises(ValueError):
        supertrend(dataframe)


def test_supertrend_missing_close_column() -> None:
    """SuperTrend requires the close column."""
    dataframe = create_dataframe().drop(
        columns=["close"],
    )

    with pytest.raises(ValueError):
        supertrend(dataframe)


def test_supertrend_direction_values() -> None:
    """SuperTrend direction should contain only -1 or 1."""
    dataframe = create_dataframe()

    result = supertrend(
        dataframe,
        period=3,
        multiplier=2.0,
    )

    direction = result[
        "supertrend_direction_3_2"
    ].dropna()

    assert direction.isin(
        [-1, 1],
    ).all()
