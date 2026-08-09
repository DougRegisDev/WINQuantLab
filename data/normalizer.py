"""
Normalização dos dados de mercado
"""
from __future__ import annotations

import pandas as pd

from config.column_mapping import COLUMN_MAPPING
from data.schemas import OFFICIAL_COLUMNS


def _normalize_columns(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Renomeia as colunas para o padrão oficial do projeto.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_

    """
    dataframe = market_data.rename(columns=COLUMN_MAPPING)
    return dataframe


def _create_datetime(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria a coluna datetime
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    if "date" in market_data.columns and "time" in market_data.columns:
        market_data["datetime"] = pd.to_datetime(
            market_data["date"].astype(str)
            + " "
            + market_data["time"].astype(str)
        )
        market_data = market_data.drop(
            columns=["date", "time"]
        )
    return market_data


def _normalize_numeric_columns(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Converte colunas numéricas para float.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:

        if column in market_data.columns:

            market_data[column] = pd.to_numeric(
                market_data[column],
                errors="coerce",
            )

    return market_data


def _sort_dataframe(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ordena o DataFrame por dateline.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    if "datetime" in market_data.columns:
        market_data = market_data.sort_values(
            by="datetime"
        )
    return market_data


def _reset_dataframe(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reinicia o índice do DataFrame.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return market_data.reset_index(drop=True)


def _reorder_columns(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reorganiza as colunas na ordem oficial do projeto.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """

    existing_columns = [
        column
        for column in OFFICIAL_COLUMNS
        if column in market_data.columns
    ]

    return market_data[existing_columns]


def normalize(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normaliza um DataFrame para o padrão oficial do WINQuantLab.
    _summary_

    Args:
        market_data (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    dataframe = market_data.copy()
    dataframe = _normalize_columns(dataframe)
    dataframe = _create_datetime(dataframe)
    dataframe = _normalize_numeric_columns(dataframe)
    dataframe = _sort_dataframe(dataframe)
    dataframe = _reset_dataframe(dataframe)
    dataframe = _reorder_columns(dataframe)

    return dataframe
