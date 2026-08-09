"""Validações reutilizáveis do WINQuantLab."""

from __future__ import annotations

from numbers import Integral

import pandas as pd


def validate_period(period: int) -> None:
    """
    Valida o período utilizado por indicadores técnicos.

    Parameters
    ----------
    period:
        Quantidade de períodos utilizada no cálculo.

    Raises
    ------
    TypeError
        Quando o período não é um número inteiro.

    ValueError
        Quando o período é menor ou igual a zero.
    """
    if isinstance(period, bool) or not isinstance(period, Integral):
        raise TypeError("O período deve ser um número inteiro.")

    if period <= 0:
        raise ValueError("O período deve ser maior que zero.")


def validate_required_column(
    dataframe: pd.DataFrame,
    column: str,
) -> None:
    """
    Verifica se uma coluna obrigatória existe no DataFrame.

    Parameters
    ----------
    dataframe:
        DataFrame que será validado.

    column:
        Nome da coluna obrigatória.

    Raises
    ------
    ValueError
        Quando a coluna não existe.
    """
    if column not in dataframe.columns:
        raise ValueError(
            f"A coluna '{column}' não foi encontrada.",
        )


def validate_numeric_column(
    dataframe: pd.DataFrame,
    column: str,
) -> None:
    """
    Verifica se uma coluna contém dados numéricos.

    Parameters
    ----------
    dataframe:
        DataFrame que será validado.

    column:
        Nome da coluna que deve ser numérica.

    Raises
    ------
    TypeError
        Quando a coluna não possui tipo numérico.
    """
    if not pd.api.types.is_numeric_dtype(dataframe[column]):
        raise TypeError(
            f"A coluna '{column}' deve conter valores numéricos.",
        )


def validate_indicator_input(
    dataframe: pd.DataFrame,
    period: int,
    column: str = "close",
) -> None:
    """
    Executa as validações comuns de um indicador técnico.

    Parameters
    ----------
    dataframe:
        DataFrame usado pelo indicador.

    period:
        Período utilizado no cálculo.

    column:
        Coluna numérica utilizada como fonte. O padrão é ``close``.
    """
    validate_period(period)
    validate_required_column(dataframe, column)
    validate_numeric_column(dataframe, column)
