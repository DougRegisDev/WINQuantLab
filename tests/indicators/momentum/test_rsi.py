"""Testes do Relative Strength Index (RSI)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.momentum import rsi


def test_rsi_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna do RSI é criada."""

    result = rsi(
        market_data,
        period=14,
    )

    assert "rsi_14" in result.columns


def test_invalid_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se períodos inválidos são rejeitados."""

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        rsi(
            market_data,
            period=0,
        )


def test_missing_close_column(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a ausência da coluna close gera erro."""

    dataframe = market_data.drop(
        columns=["close"],
    )

    with pytest.raises(
        ValueError,
        match="close",
    ):
        rsi(
            dataframe,
            period=14,
        )


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""

    original_columns = market_data.columns.tolist()

    result = rsi(
        market_data,
        period=14,
    )

    assert market_data.columns.tolist() == original_columns

    assert "rsi_14" not in market_data.columns

    assert "rsi_14" in result.columns


def test_rsi_values_between_zero_and_hundred(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se os valores do RSI permanecem entre 0 e 100."""

    result = rsi(
        market_data,
        period=14,
    )

    values = result["rsi_14"].dropna()

    assert (values >= 0).all()

    assert (values <= 100).all()


def test_initial_values_are_nan(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se os primeiros valores são NaN."""

    result = rsi(
        market_data,
        period=14,
    )

    assert result["rsi_14"].iloc[:13].isna().all()


def test_rsi_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara o RSI calculado com uma referência independente."""
    period = 14

    result = rsi(
        market_data,
        period=period,
    )

    changes = market_data["close"].diff()

    gains = changes.clip(lower=0)

    losses = (
        changes
        .clip(upper=0)
        .abs()
    )

    average_gain = (
        gains
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    average_loss = (
        losses
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    relative_strength = average_gain / average_loss

    expected = 100 - (
        100 / (1 + relative_strength)
    )

    expected = expected.mask(
        (average_loss == 0) & (average_gain > 0),
        100.0,
    )

    expected = expected.mask(
        (average_gain == 0) & (average_loss > 0),
        0.0,
    )

    expected = expected.mask(
        (average_gain == 0) & (average_loss == 0),
        float("nan"),
    )

    pd.testing.assert_series_equal(
        result["rsi_14"],
        expected,
        check_names=False,
    )
