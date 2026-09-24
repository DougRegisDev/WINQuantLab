from pathlib import Path

import pandas as pd

from config.csv_config import (
    DEFAULT_DECIMAL,
    DEFAULT_SEPARATOR,
)


def validate_file_exists(file_path: Path) -> None:
    """
    Verifica se o arquivo existe.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )


def read_csv(
    file_path: Path,
    header: int | None = 0,
) -> pd.DataFrame:
    """
    Lê um arquivo CSV utilizando a configuração padrão do projeto.
    """

    return pd.read_csv(
        file_path,
        sep=DEFAULT_SEPARATOR,
        decimal=DEFAULT_DECIMAL,
        header=header,
    )


def load_data(
    file_path: str | Path,
    header: int | None = 0,
) -> pd.DataFrame:
    """
    Carrega os dados do mercado.
    """

    path = Path(file_path)

    validate_file_exists(path)

    market_data = read_csv(
        path,
        header=header,
    )

    return market_data
