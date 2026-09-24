from pathlib import Path

import pandas as pd

from data.loader import load_data
from data.normalizer import normalize
from data.schemas import OFFICIAL_COLUMNS

dataframe = load_data(
    Path("tests/fixtures/csv/exemplo.csv")
)
dataframe = normalize(dataframe)
assert list(dataframe.columns) == OFFICIAL_COLUMNS


def test_columns_are_normalized():

    dataframe = load_data(
        Path("tests/fixtures/csv/exemplo.csv")
    )

    dataframe = normalize(dataframe)

    expected = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    assert list(dataframe.columns) == expected


def test_datetime_exists():

    dataframe = load_data(
        Path("tests/fixtures/csv/exemplo.csv")
    )

    dataframe = normalize(dataframe)

    assert "datetime" in dataframe.columns


def test_numeric_columns():

    dataframe = load_data(
        Path("tests/fixtures/csv/exemplo.csv")
    )

    dataframe = normalize(dataframe)

    assert dataframe["open"].dtype.kind in "fi"
    assert dataframe["high"].dtype.kind in "fi"
    assert dataframe["low"].dtype.kind in "fi"
    assert dataframe["close"].dtype.kind in "fi"


def test_normalize_profit_csv_without_header():
    """
    Deve reconhecer o layout sem cabeçalho exportado pelo Profit.
    """

    market_data = pd.DataFrame(
        [
            [
                "WINFUT",
                "16/09/2026",
                "18:20:00",
                187425.0,
                187600.0,
                187350.0,
                187600.0,
                1065619488.0,
                28412,
            ],
        ]
    )

    normalized = normalize(
        market_data,
        source="profit",
    )

    assert normalized.loc[0, "open"] == 187425.0
    assert normalized.loc[0, "high"] == 187600.0
    assert normalized.loc[0, "low"] == 187350.0
    assert normalized.loc[0, "close"] == 187600.0
    assert normalized.loc[0, "volume"] == 28412.0


def test_normalize_profit_uses_day_first_date():
    """
    Deve interpretar datas do Profit no formato dia/mês/ano.
    """

    market_data = pd.DataFrame(
        [
            [
                "WINFUT",
                "05/04/2026",
                "10:30:00",
                100.0,
                110.0,
                90.0,
                105.0,
                1000000.0,
                1000,
            ],
        ]
    )

    normalized = normalize(
        market_data,
        source="profit",
    )

    datetime_value = normalized.loc[0, "datetime"]

    assert datetime_value.year == 2026
    assert datetime_value.month == 4
    assert datetime_value.day == 5
    assert datetime_value.hour == 10
    assert datetime_value.minute == 30
