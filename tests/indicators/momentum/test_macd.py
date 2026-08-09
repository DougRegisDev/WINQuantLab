"""Testes do Moving Average Convergence Divergence (MACD)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.momentum import macd


def test_macd_columns_are_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se as colunas do MACD são criadas."""

    result = macd(
        market_data,
    )

    expected_columns = [
        "macd",
        "macd_signal",
        "macd_histogram",
    ]

    for column in expected_columns:
        assert column in result.columns


def test_invalid_periods(
    market_data: pd.DataFrame,
) -> None:
    """Verifica períodos inválidos."""

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        macd(
            market_data,
            fast_period=0,
        )

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        macd(
            market_data,
            slow_period=0,
        )

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        macd(
            market_data,
            signal_period=0,
        )


def test_fast_period_must_be_smaller_than_slow(
    market_data: pd.DataFrame,
) -> None:
    """A média rápida deve possuir período menor."""

    with pytest.raises(
        ValueError,
        match="fast_period",
    ):
        macd(
            market_data,
            fast_period=30,
            slow_period=10,
        )


def test_missing_close_column(
    market_data: pd.DataFrame,
) -> None:
    """Verifica ausência da coluna close."""

    dataframe = market_data.drop(
        columns=["close"],
    )

    with pytest.raises(
        ValueError,
        match="close",
    ):
        macd(dataframe)


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece intacto."""

    original_columns = market_data.columns.tolist()

    result = macd(
        market_data,
    )

    assert market_data.columns.tolist() == original_columns

    assert "macd" not in market_data.columns

    assert "macd" in result.columns


def test_macd_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara os valores do MACD com uma referência independente."""

    fast_period = 12
    slow_period = 26
    signal_period = 9

    result = macd(
        market_data,
        fast_period=fast_period,
        slow_period=slow_period,
        signal_period=signal_period,
    )

    ema_fast = (
        market_data["close"]
        .ewm(
            span=fast_period,
            adjust=False,
            min_periods=fast_period,
        )
        .mean()
    )

    ema_slow = (
        market_data["close"]
        .ewm(
            span=slow_period,
            adjust=False,
            min_periods=slow_period,
        )
        .mean()
    )

    expected_macd = ema_fast - ema_slow

    expected_signal = (
        expected_macd
        .ewm(
            span=signal_period,
            adjust=False,
            min_periods=signal_period,
        )
        .mean()
    )

    expected_histogram = (
        expected_macd
        - expected_signal
    )

    pd.testing.assert_series_equal(
        result["macd"],
        expected_macd,
        check_names=False,
    )

    pd.testing.assert_series_equal(
        result["macd_signal"],
        expected_signal,
        check_names=False,
    )

    pd.testing.assert_series_equal(
        result["macd_histogram"],
        expected_histogram,
        check_names=False,
    )
