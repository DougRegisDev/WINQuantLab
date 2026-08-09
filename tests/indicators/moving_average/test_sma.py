"""Testes da Média Móvel Simples — SMA."""

import pandas as pd
import pytest

from indicators.moving_averages import sma


def test_sma_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna da SMA é criada."""
    result = sma(
        market_data,
        period=9,
    )

    assert "sma_9" in result.columns


def test_sma_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara a SMA calculada com o resultado de referência."""
    result = sma(
        market_data,
        period=3,
    )

    expected = (
        market_data["close"]
        .rolling(
            window=3,
            min_periods=3,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result["sma_3"],
        expected,
        check_names=False,
    )


def test_invalid_sma_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se períodos inválidos são rejeitados."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        sma(
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
        sma(dataframe_without_close)
