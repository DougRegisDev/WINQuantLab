"""Tests for the Average Directional Index (ADX)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.trend.adx import adx


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


def test_adx_creates_column() -> None:
    """ADX should create the output column."""
    dataframe = create_dataframe()

    result = adx(
        dataframe,
        period=3,
    )

    assert "adx_3" in result.columns


def test_adx_preserves_original_dataframe() -> None:
    """ADX must not modify the original DataFrame."""
    dataframe = create_dataframe()
    original = dataframe.copy(deep=True)

    adx(
        dataframe,
        period=3,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_adx_invalid_period() -> None:
    """ADX should reject invalid periods."""
    dataframe = create_dataframe()

    with pytest.raises(ValueError):
        adx(
            dataframe,
            period=0,
        )


def test_adx_missing_high_column() -> None:
    """ADX requires the high column."""
    dataframe = create_dataframe().drop(
        columns=["high"],
    )

    with pytest.raises(ValueError):
        adx(dataframe)


def test_adx_missing_low_column() -> None:
    """ADX requires the low column."""
    dataframe = create_dataframe().drop(
        columns=["low"],
    )

    with pytest.raises(ValueError):
        adx(dataframe)


def test_adx_missing_close_column() -> None:
    """ADX requires the close column."""
    dataframe = create_dataframe().drop(
        columns=["close"],
    )

    with pytest.raises(ValueError):
        adx(dataframe)


def test_adx_values() -> None:
    """Compare ADX values with an independent reference calculation."""
    period = 3

    dataframe = pd.DataFrame(
        {
            "open": [10.0, 11.0, 12.0, 11.0, 13.0, 14.0, 13.0],
            "high": [11.0, 13.0, 14.0, 13.0, 15.0, 16.0, 15.0],
            "low": [9.0, 10.0, 11.0, 9.0, 12.0, 13.0, 11.0],
            "close": [10.0, 12.0, 13.0, 10.0, 14.0, 15.0, 12.0],
        }
    )

    result = adx(
        dataframe,
        period=period,
    )

    up_move = dataframe["high"].diff()
    down_move = -dataframe["low"].diff()

    positive_dm = up_move.where(
        (up_move > down_move) & (up_move > 0),
        0.0,
    )

    negative_dm = down_move.where(
        (down_move > up_move) & (down_move > 0),
        0.0,
    )

    previous_close = dataframe["close"].shift(1)

    true_range = pd.concat(
        [
            dataframe["high"] - dataframe["low"],
            (dataframe["high"] - previous_close).abs(),
            (dataframe["low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    smoothed_positive_dm = (
        positive_dm
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    smoothed_negative_dm = (
        negative_dm
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    average_true_range = (
        true_range
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    positive_di = (
        smoothed_positive_dm
        / average_true_range
    ) * 100

    negative_di = (
        smoothed_negative_dm
        / average_true_range
    ) * 100

    directional_index = (
        (positive_di - negative_di).abs()
        / (positive_di + negative_di)
    ) * 100

    expected = (
        directional_index
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result["adx_3"],
        expected,
        check_names=False,
    )
