from pathlib import Path

import pytest

from data.loader import load_data


def test_load_valid_csv():
    """
    Deve carregar um CSV válido.
    """

    file_path = Path("tests/fixtures/csv/exemplo.csv")

    market_data = load_data(file_path)

    assert not market_data.empty


def test_file_not_found():
    """
    Deve lançar erro quando o arquivo não existir.
    """

    file_path = Path("tests/fixtures/csv/arquivo_inexistente.csv")

    with pytest.raises(FileNotFoundError):
        load_data(file_path)
