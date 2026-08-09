from pathlib import Path

import pytest

from data.loader import load_data
from data.validator import validate_columns, validate_dataframe


def test_dataframe_is_not_empty():
    dataframe = load_data(
        Path("tests/fixtures/csv/exemplo.csv")
    )
    assert not dataframe.empty


def test_empty_dataframe():
    dataframe = load_data(
        Path("tests/fixtures/csv/vazio.csv")
    )
    with pytest.raises(ValueError):
        validate_dataframe(dataframe)


def test_missing_required_column():

    dataframe = load_data(
        Path("tests/fixtures/csv/missing_columns.csv")
    )

    with pytest.raises(ValueError):
        validate_columns(dataframe)
