"""Implementação da Hull Moving Average — HMA."""

from __future__ import annotations

from math import isqrt

import pandas as pd

from core.validations import validate_indicator_input
from indicators.moving_averages.calculations import calculate_wma


def hma(
    dataframe: pd.DataFrame,
    period: int = 9,
) -> pd.DataFrame:
    """
    Calcula a Hull Moving Average dos preços de fechamento.

    A HMA combina diferentes médias móveis ponderadas para reduzir
    o atraso e manter uma resposta rápida às variações de preço.

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna numérica ``close``.

    period:
        Quantidade de períodos utilizada no cálculo.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame com a coluna ``hma_<periodo>``.

    Raises
    ------
    TypeError
        Quando o período não é inteiro ou a coluna ``close`` não é numérica.

    ValueError
        Quando o período é menor que 2 ou a coluna ``close`` não existe.
    """
    validate_indicator_input(
        dataframe,
        period,
    )

    if period < 2:
        raise ValueError(
            "O período da HMA deve ser maior ou igual a 2.",
        )

    result = dataframe.copy()

    half_period = max(
        1,
        period // 2,
    )

    square_root_period = max(
        1,
        isqrt(period),
    )

    wma_half = calculate_wma(
        result["close"],
        half_period,
    )

    wma_full = calculate_wma(
        result["close"],
        period,
    )

    intermediate_series = (
        2 * wma_half
        - wma_full
    )

    result[f"hma_{period}"] = calculate_wma(
        intermediate_series,
        square_root_period,
    )

    return result
