"""Cálculos compartilhados entre famílias de indicadores."""

from __future__ import annotations

import pandas as pd


def calculate_ema(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula uma Média Móvel Exponencial sobre uma série numérica.

    Parameters
    ----------
    series:
        Série numérica utilizada no cálculo.

    period:
        Quantidade de períodos da média exponencial.

    Returns
    -------
    pd.Series
        Série contendo os valores da EMA.
    """
    return (
        series
        .ewm(
            span=period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )


def calculate_rolling_max(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula o maior valor dentro de uma janela móvel.

    Parameters
    ----------
    series:
        Série numérica utilizada no cálculo.

    period:
        Quantidade de períodos da janela.

    Returns
    -------
    pd.Series
        Série contendo os maiores valores de cada janela.
    """
    return (
        series
        .rolling(
            window=period,
            min_periods=period,
        )
        .max()
    )


def calculate_rolling_min(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula o menor valor dentro de uma janela móvel.

    Parameters
    ----------
    series:
        Série numérica utilizada no cálculo.

    period:
        Quantidade de períodos da janela.

    Returns
    -------
    pd.Series
        Série contendo os menores valores de cada janela.
    """
    return (
        series
        .rolling(
            window=period,
            min_periods=period,
        )
        .min()
    )


def calculate_true_range(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
) -> pd.Series:
    """
    Calcula o True Range (TR).

    Parameters
    ----------
    high:
        Série de preços máximos.

    low:
        Série de preços mínimos.

    close:
        Série de preços de fechamento.

    Returns
    -------
    pd.Series
        Série contendo o True Range.
    """
    previous_close = close.shift(1)

    ranges = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    )

    return ranges.max(axis=1)


def calculate_wilder_average(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula a média suavizada de Wilder.

    Parameters
    ----------
    series:
        Série numérica que será suavizada.

    period:
        Quantidade de períodos utilizada na suavização.

    Returns
    -------
    pd.Series
        Série suavizada segundo o método de Wilder.
    """
    return (
        series
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )


def calculate_average_true_range(
    true_range: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calculate the Average True Range (ATR).

    Parameters
    ----------
    true_range:
        Series containing the True Range values.

    period:
        Number of periods used in the calculation.

    Returns
    -------
    pd.Series
        Series containing the Average True Range.
    """
    return calculate_wilder_average(
        series=true_range,
        period=period,
    )


def calculate_directional_movement(
    high: pd.Series,
    low: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """
    Calculate positive and negative Directional Movement.

    Parameters
    ----------
    high:
        High price series.

    low:
        Low price series.

    Returns
    -------
    tuple[pd.Series, pd.Series]
        Positive and negative Directional Movement series.
    """
    up_move = high.diff()
    down_move = -low.diff()

    positive_dm = up_move.where(
        (up_move > down_move) & (up_move > 0),
        0.0,
    )

    negative_dm = down_move.where(
        (down_move > up_move) & (down_move > 0),
        0.0,
    )

    return positive_dm, negative_dm


def calculate_directional_index(
    positive_di: pd.Series,
    negative_di: pd.Series,
) -> pd.Series:
    """
    Calculate the Directional Index (DX).

    Parameters
    ----------
    positive_di:
        Positive Directional Indicator series.

    negative_di:
        Negative Directional Indicator series.

    Returns
    -------
    pd.Series
        Series containing the Directional Index values.
    """
    denominator = positive_di + negative_di

    directional_difference = (
        positive_di - negative_di
    ).abs()

    return (
        directional_difference
        / denominator
    ) * 100
