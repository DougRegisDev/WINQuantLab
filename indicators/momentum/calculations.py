"""Cálculos internos reutilizáveis dos indicadores de momentum."""

from __future__ import annotations

import pandas as pd


def calculate_price_changes(
    series: pd.Series,
) -> pd.Series:
    """
    Calcula a variação entre valores consecutivos.

    Parameters
    ----------
    series:
        Série numérica com preços de fechamento.

    Returns
    -------
    pd.Series
        Série contendo a diferença entre cada valor e o anterior.
    """
    return series.diff()


def separate_gains_and_losses(
    changes: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """
    Separa variações positivas e negativas em ganhos e perdas.

    Parameters
    ----------
    changes:
        Série contendo as variações entre preços consecutivos.

    Returns
    -------
    tuple[pd.Series, pd.Series]
        Duas séries:

        - ganhos positivos;
        - perdas convertidas para valores positivos.
    """
    gains = changes.clip(
        lower=0,
    )

    losses = (
        changes
        .clip(
            upper=0,
        )
        .abs()
    )

    return gains, losses


def calculate_previous_values(
    series: pd.Series,
    period: int,
) -> pd.Series:
    """
    Retorna a série deslocada em um número de períodos.

    Parameters
    ----------
    series:
        Série utilizada no cálculo.

    period:
        Quantidade de períodos para deslocamento.

    Returns
    -------
    pd.Series
        Série deslocada.
    """
    return series.shift(period)
