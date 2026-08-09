"""Testes do Stochastic Oscillator."""

from __future__ import annotations

import pandas as pd
import pytest

from indicators.momentum import stochastic


def test_stochastic_columns_are_created(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se as colunas %K e %D são criadas."""
    result = stochastic(
        market_data,
        k_period=14,
        d_period=3,
    )

    assert "stochastic_k_14" in result.columns
    assert "stochastic_d_14_3" in result.columns


def test_invalid_k_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica período inválido para %K."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        stochastic(
            market_data,
            k_period=0,
            d_period=3,
        )


def test_invalid_d_period(
    market_data: pd.DataFrame,
) -> None:
    """Verifica período inválido para %D."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        stochastic(
            market_data,
            k_period=14,
            d_period=0,
        )


def test_missing_high_column(
    market_data: pd.DataFrame,
) -> None:
    """Verifica ausência da coluna high."""
    dataframe = market_data.drop(
        columns=["high"],
    )

    with pytest.raises(
        ValueError,
        match="high",
    ):
        stochastic(dataframe)


def test_missing_low_column(
    market_data: pd.DataFrame,
) -> None:
    """Verifica ausência da coluna low."""
    dataframe = market_data.drop(
        columns=["low"],
    )

    with pytest.raises(
        ValueError,
        match="low",
    ):
        stochastic(dataframe)


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
        stochastic(dataframe)


def test_original_dataframe_is_not_modified(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""
    original_columns = market_data.columns.tolist()

    result = stochastic(
        market_data,
        k_period=14,
        d_period=3,
    )

    assert market_data.columns.tolist() == original_columns
    assert "stochastic_k_14" not in market_data.columns
    assert "stochastic_d_14_3" not in market_data.columns

    assert "stochastic_k_14" in result.columns
    assert "stochastic_d_14_3" in result.columns


def test_stochastic_values_between_zero_and_hundred(
    market_data: pd.DataFrame,
) -> None:
    """Verifica se %K e %D permanecem entre 0 e 100."""
    result = stochastic(
        market_data,
        k_period=14,
        d_period=3,
    )

    k_values = result["stochastic_k_14"].dropna()
    d_values = result["stochastic_d_14_3"].dropna()

    assert (k_values >= 0).all()
    assert (k_values <= 100).all()

    assert (d_values >= 0).all()
    assert (d_values <= 100).all()


def test_stochastic_values(
    market_data: pd.DataFrame,
) -> None:
    """Compara o Stochastic com uma referência independente."""
    k_period = 14
    d_period = 3

    result = stochastic(
        market_data,
        k_period=k_period,
        d_period=d_period,
    )

    highest_high = (
        market_data["high"]
        .rolling(
            window=k_period,
            min_periods=k_period,
        )
        .max()
    )

    lowest_low = (
        market_data["low"]
        .rolling(
            window=k_period,
            min_periods=k_period,
        )
        .min()
    )

    expected_k = (
        (
            market_data["close"]
            - lowest_low
        )
        / (
            highest_high
            - lowest_low
        )
    ) * 100

    expected_d = (
        expected_k
        .rolling(
            window=d_period,
            min_periods=d_period,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result["stochastic_k_14"],
        expected_k,
        check_names=False,
    )

    pd.testing.assert_series_equal(
        result["stochastic_d_14_3"],
        expected_d,
        check_names=False,
    )
