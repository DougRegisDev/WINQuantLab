"""Testes da Média Móvel Ponderada — WMA."""

import numpy as np
import pandas as pd
import pytest

from indicators.moving_averages import wma


def test_wma_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna da WMA é criada."""
    result = wma(
        market_data,
        period=9,
    )

    assert "wma_9" in result.columns


def test_wma_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara a WMA calculada com um resultado de referência."""
    period = 3

    result = wma(
        market_data,
        period=period,
    )

    weights = np.arange(
        1,
        period + 1,
        dtype=float,
    )

    expected = (
        market_data["close"]
        .rolling(
            window=period,
            min_periods=period,
        )
        .apply(
            lambda values: np.dot(values, weights) / weights.sum(),
            raw=True,
        )
    )

    pd.testing.assert_series_equal(
        result["wma_3"],
        expected,
        check_names=False,
    )


def test_invalid_wma_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se períodos inválidos são rejeitados."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        wma(
            market_data,
            period=0,
        )


def test_missing_close_column(
    market_data: pd.DataFrame,
) -> None:
    """Verifica o comportamento quando a coluna close não existe."""
    dataframe_without_close = market_data.drop(
        columns=["close"],
    )

    with pytest.raises(
        ValueError,
        match="close",
    ):
        wma(dataframe_without_close)


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""
    original_columns = market_data.columns.tolist()

    result = wma(
        market_data,
        period=3,
    )

    assert market_data.columns.tolist() == original_columns
    assert "wma_3" not in market_data.columns
    assert "wma_3" in result.columns
