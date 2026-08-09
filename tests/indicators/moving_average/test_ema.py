"""Testes da Média Móvel Exponencial — EMA."""

import pandas as pd
import pytest

from indicators.moving_averages import ema


def test_ema_column_is_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se a coluna da EMA é criada corretamente."""
    result = ema(
        market_data,
        period=9,
    )

    assert "ema_9" in result.columns


def test_ema_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara a EMA calculada com o resultado de referência do Pandas."""
    result = ema(
        market_data,
        period=3,
    )

    expected = (
        market_data["close"]
        .ewm(
            span=3,
            adjust=False,
            min_periods=3,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result["ema_3"],
        expected,
        check_names=False,
    )


def test_invalid_ema_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se períodos inválidos são rejeitados."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        ema(
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
        ema(dataframe_without_close)
