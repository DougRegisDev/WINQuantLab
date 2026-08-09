"""Testes do indicador Rate of Change (ROC)."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.momentum import roc


def test_roc_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna do ROC é criada."""

    result = roc(
        market_data,
        period=14,
    )

    assert "roc_14" in result.columns


def test_invalid_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica períodos inválidos."""

    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        roc(
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
        roc(
            dataframe,
            period=14,
        )


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""

    original_columns = market_data.columns.tolist()

    result = roc(
        market_data,
        period=14,
    )

    assert market_data.columns.tolist() == original_columns

    assert "roc_14" not in market_data.columns

    assert "roc_14" in result.columns


def test_roc_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara o ROC com uma referência independente."""
    period = 14

    result = roc(
        market_data,
        period=period,
    )

    previous = market_data["close"].shift(period)

    expected = (
        (
            market_data["close"]
            / previous
        )
        - 1
    ) * 100

    pd.testing.assert_series_equal(
        result["roc_14"],
        expected,
        check_names=False,
    )
