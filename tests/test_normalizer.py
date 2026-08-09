from pathlib import Path

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
