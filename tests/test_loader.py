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

    file_path = Path(
        "tests/fixtures/csv/arquivo_inexistente.csv"
    )

    with pytest.raises(FileNotFoundError):
        load_data(file_path)


def test_load_csv_without_header(tmp_path):
    """
    Deve carregar todas as linhas de um CSV sem cabeçalho.
    """

    file_path = tmp_path / "sem_cabecalho.csv"

    file_path.write_text(
        "WINFUT;16/09/2026;18:20:00;187425,00\n"
        "WINFUT;16/09/2026;18:15:00;187325,00\n",
        encoding="utf-8",
    )

    market_data = load_data(
        file_path,
        header=None,
    )

    assert len(market_data) == 2
