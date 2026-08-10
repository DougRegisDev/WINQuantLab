"""Indicador Parabolic SAR."""

from __future__ import annotations

import pandas as pd


def parabolic_sar(
    df: pd.DataFrame,
    step: float = 0.02,
    max_step: float = 0.20,
) -> pd.DataFrame:
    """
    Calcula o Parabolic SAR.

    Parameters
    ----------
    df:
        DataFrame contendo as colunas ``high`` e ``low``.

    step:
        Incremento utilizado no fator de aceleração.

    max_step:
        Valor máximo permitido para o fator de aceleração.

    Returns
    -------
    pd.DataFrame
        Cópia do DataFrame original com a coluna
        ``parabolic_sar`` adicionada.

    Raises
    ------
    ValueError
        Se ``step`` ou ``max_step`` forem inválidos,
        ou se as colunas obrigatórias não existirem.
    """

    # Validação dos parâmetros
    if step <= 0:
        raise ValueError("step must be greater than zero")

    if max_step <= 0:
        raise ValueError("max_step must be greater than zero")

    # Validação das colunas obrigatórias
    required_columns = {"high", "low"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = df.copy()

    high = result["high"]
    low = result["low"]

    sar = pd.Series(
        index=result.index,
        dtype="float64",
    )

    # DataFrame vazio
    if result.empty:
        result["parabolic_sar"] = sar
        return result

    # Determina a tendência inicial
    if len(result) == 1:
        bullish = True
    else:
        bullish = high.iloc[1] >= high.iloc[0]

    acceleration_factor = step

    # Inicialização do SAR e do Extreme Point
    if bullish:
        extreme_point = high.iloc[0]
        sar.iloc[0] = low.iloc[0]
    else:
        extreme_point = low.iloc[0]
        sar.iloc[0] = high.iloc[0]

    # Cálculo iterativo do Parabolic SAR
    for position in range(1, len(result)):
        previous_sar = sar.iloc[position - 1]

        current_sar = (
            previous_sar
            + acceleration_factor
            * (extreme_point - previous_sar)
        )

        if bullish:
            current_sar = min(
                current_sar,
                low.iloc[position - 1],
            )

            if position >= 2:
                current_sar = min(
                    current_sar,
                    low.iloc[position - 2],
                )

            # Reversão de alta para baixa
            if low.iloc[position] < current_sar:
                bullish = False

                current_sar = extreme_point
                extreme_point = low.iloc[position]
                acceleration_factor = step

            # Novo extremo da tendência de alta
            elif high.iloc[position] > extreme_point:
                extreme_point = high.iloc[position]

                acceleration_factor = min(
                    acceleration_factor + step,
                    max_step,
                )

        else:
            current_sar = max(
                current_sar,
                high.iloc[position - 1],
            )

            if position >= 2:
                current_sar = max(
                    current_sar,
                    high.iloc[position - 2],
                )

            # Reversão de baixa para alta
            if high.iloc[position] > current_sar:
                bullish = True

                current_sar = extreme_point
                extreme_point = high.iloc[position]
                acceleration_factor = step

            # Novo extremo da tendência de baixa
            elif low.iloc[position] < extreme_point:
                extreme_point = low.iloc[position]

                acceleration_factor = min(
                    acceleration_factor + step,
                    max_step,
                )

        sar.iloc[position] = current_sar

    result["parabolic_sar"] = sar

    return result
