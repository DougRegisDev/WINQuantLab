"""Testes do indicador Momentum."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.momentum import momentum


def test_momentum_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna do Momentum é criada."""

    result = momentum(
        market_data,
        period=14,
    )

    assert "momentum_14" in result.columns


def test_invalid_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica períodos inválidos."""

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        momentum(
            market_data,
            period=0,
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
        momentum(
            dataframe,
            period=14,
        )


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""

    original_columns = market_data.columns.tolist()

    result = momentum(
        market_data,
        period=14,
    )

    assert market_data.columns.tolist() == original_columns

    assert "momentum_14" not in market_data.columns

    assert "momentum_14" in result.columns


def test_momentum_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara o Momentum com uma referência independente."""
    period = 14

    result = momentum(
        market_data,
        period=period,
    )

    previous = market_data["close"].shift(period)

    expected = market_data["close"] - previous

    pd.testing.assert_series_equal(
        result["momentum_14"],
        expected,
        check_names=False,
    )
