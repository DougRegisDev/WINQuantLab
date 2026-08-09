"""Testes da Hull Moving Average — HMA."""

from math import isqrt

import pandas as pd
import pytest

from indicators.moving_averages import hma
from indicators.moving_averages.calculations import calculate_wma


def test_hma_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna da HMA é criada."""
    result = hma(
        market_data,
        period=9,
    )

    assert "hma_9" in result.columns


def test_hma_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara a HMA calculada com um resultado de referência."""
    period = 9

    result = hma(
        market_data,
        period=period,
    )

    half_period = period // 2
    square_root_period = isqrt(period)

    wma_half = calculate_wma(
        market_data["close"],
        half_period,
    )

    wma_full = calculate_wma(
        market_data["close"],
        period,
    )

    intermediate_series = (
        2 * wma_half
        - wma_full
    )

    expected = calculate_wma(
        intermediate_series,
        square_root_period,
    )

    pd.testing.assert_series_equal(
        result["hma_9"],
        expected,
        check_names=False,
    )


def test_invalid_hma_period_zero(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o período zero é rejeitado."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        hma(
            market_data,
            period=0,
        )


def test_hma_period_one_is_rejected(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o período um é rejeitado pela HMA."""
    with pytest.raises(
        ValueError,
        match="maior ou igual a 2",
    ):
        hma(
            market_data,
            period=1,
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
        hma(dataframe_without_close)


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""
    original_columns = market_data.columns.tolist()

    result = hma(
        market_data,
        period=9,
    )

    assert market_data.columns.tolist() == original_columns
    assert "hma_9" not in market_data.columns
    assert "hma_9" in result.columns
