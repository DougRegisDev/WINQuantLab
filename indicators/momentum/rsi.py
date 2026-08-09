"""Implementação do Relative Strength Index — RSI."""

from __future__ import annotations

import numpy as np
import pandas as pd

from core.validations import validate_indicator_input
from indicators.calculations import calculate_wilder_average
from indicators.momentum.calculations import (
    calculate_price_changes,
    separate_gains_and_losses,
)


def rsi(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    """
    Calcula o Relative Strength Index dos preços de fechamento.

    Parameters
    ----------
    dataframe:
        DataFrame contendo a coluna numérica ``close``.

    period:
        Quantidade de períodos utilizada no cálculo.
        O valor padrão é 14.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame com a coluna ``rsi_<periodo>``.

    Raises
    ------
    TypeError
        Quando o período não é inteiro ou a coluna ``close`` não é numérica.

    ValueError
        Quando o período é menor ou igual a zero ou a coluna ``close``
        não existe.
    """
    validate_indicator_input(
        dataframe,
        period,
    )

    result = dataframe.copy()

    changes = calculate_price_changes(
        result["close"],
    )

    gains, losses = separate_gains_and_losses(
        changes,
    )

    average_gain = calculate_wilder_average(
        gains,
        period,
    )

    average_loss = calculate_wilder_average(
        losses,
        period,
    )

    relative_strength = average_gain / average_loss

    rsi_values = 100 - (
        100 / (1 + relative_strength)
    )

    rsi_values = rsi_values.mask(
        (average_loss == 0) & (average_gain > 0),
        100.0,
    )

    rsi_values = rsi_values.mask(
        (average_gain == 0) & (average_loss > 0),
        0.0,
    )

    rsi_values = rsi_values.mask(
        (average_gain == 0) & (average_loss == 0),
        np.nan,
    )

    result[f"rsi_{period}"] = rsi_values

    return result
