import pandas as pd

from data.schemas import REQUIRED_COLUMNS


def validate_dataframe(
    market_data: pd.DataFrame,
) -> None:
    """
    Valida se o Dataframe contem dados.
    """
    if market_data.empty:
        raise ValueError(
            "O Dataframe está vazio"
        )


def validate_columns(
    market_data: pd.DataFrame,
) -> None:

    for column in REQUIRED_COLUMNS:

        if column not in market_data.columns:

            raise ValueError(
                f"Coluna obrigatória ausente: {column}"
            )
