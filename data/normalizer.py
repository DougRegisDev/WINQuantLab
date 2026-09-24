"""
Normalização dos dados de mercado.
"""

from __future__ import annotations

import pandas as pd

from config.column_mapping import COLUMN_MAPPING
from data.schemas import OFFICIAL_COLUMNS

PROFIT_COLUMNS = {
    0: "ticker",
    1: "date",
    2: "time",
    3: "open",
    4: "high",
    5: "low",
    6: "close",
    7: "financial_volume",
    8: "volume",
}


def _normalize_source(
    market_data: pd.DataFrame,
    source: str | None,
) -> pd.DataFrame:
    """
    Normaliza o layout específico da fonte dos dados.
    """

    if source is None:
        return market_data

    if source == "profit":
        return market_data.rename(
            columns=PROFIT_COLUMNS
        )

    raise ValueError(
        f"Fonte de dados não suportada: {source}"
    )


def _normalize_columns(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Renomeia as colunas para o padrão oficial do projeto.
    """

    dataframe = market_data.rename(
        columns=COLUMN_MAPPING
    )

    return dataframe


def _create_datetime(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria a coluna datetime.
    """

    if (
        "date" in market_data.columns
        and "time" in market_data.columns
    ):
        market_data["datetime"] = pd.to_datetime(
            market_data["date"].astype(str)
            + " "
            + market_data["time"].astype(str),
            dayfirst=True,
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
    Ordena o DataFrame por datetime.
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
    """

    return market_data.reset_index(drop=True)


def _reorder_columns(
    market_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reorganiza as colunas na ordem oficial do projeto.
    """

    existing_columns = [
        column
        for column in OFFICIAL_COLUMNS
        if column in market_data.columns
    ]

    return market_data[existing_columns]


def normalize(
    market_data: pd.DataFrame,
    source: str | None = None,
) -> pd.DataFrame:
    """
    Normaliza um DataFrame para o padrão oficial do WINQuantLab.
    """

    dataframe = market_data.copy()

    dataframe = _normalize_source(
        dataframe,
        source,
    )
    dataframe = _normalize_columns(dataframe)
    dataframe = _create_datetime(dataframe)
    dataframe = _normalize_numeric_columns(dataframe)
    dataframe = _sort_dataframe(dataframe)
    dataframe = _reset_dataframe(dataframe)
    dataframe = _reorder_columns(dataframe)

    return dataframe
