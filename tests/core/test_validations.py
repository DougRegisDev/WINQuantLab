"""Testes das validações reutilizáveis."""

import pandas as pd
import pytest

from core.validations import (
    validate_indicator_input,
    validate_numeric_column,
    validate_period,
    validate_required_column,
)


@pytest.fixture
def valid_dataframe() -> pd.DataFrame:
    """Cria um DataFrame válido para os testes."""
    return pd.DataFrame(
        {
            "close": [100.0, 101.0, 102.0],
        },
    )


@pytest.mark.parametrize(
    "period",
    [1, 9, 20],
)
def test_validate_period_accepts_positive_integers(
    period: int,
) -> None:
    """Aceita períodos inteiros maiores que zero."""
    validate_period(period)


@pytest.mark.parametrize(
    "period",
    [0, -1, -20],
)
def test_validate_period_rejects_non_positive_values(
    period: int,
) -> None:
    """Rejeita períodos menores ou iguais a zero."""
    with pytest.raises(
        ValueError,
        match="maior que zero",
    ):
        validate_period(period)


@pytest.mark.parametrize(
    "period",
    [True, False, 9.5, "9", None],
)
def test_validate_period_rejects_non_integer_values(
    period: object,
) -> None:
    """Rejeita períodos que não sejam inteiros."""
    with pytest.raises(
        TypeError,
        match="número inteiro",
    ):
        validate_period(period)  # type: ignore[arg-type]


def test_validate_required_column_accepts_existing_column(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Aceita uma coluna existente."""
    validate_required_column(
        valid_dataframe,
        "close",
    )


def test_validate_required_column_rejects_missing_column(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Rejeita uma coluna inexistente."""
    with pytest.raises(
        ValueError,
        match="open",
    ):
        validate_required_column(
            valid_dataframe,
            "open",
        )


def test_validate_numeric_column_accepts_numeric_data(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Aceita uma coluna numérica."""
    validate_numeric_column(
        valid_dataframe,
        "close",
    )


def test_validate_numeric_column_rejects_text_data() -> None:
    """Rejeita uma coluna textual."""
    dataframe = pd.DataFrame(
        {
            "close": ["100", "101", "102"],
        },
    )

    with pytest.raises(
        TypeError,
        match="valores numéricos",
    ):
        validate_numeric_column(
            dataframe,
            "close",
        )


def test_validate_indicator_input_accepts_valid_data(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Aceita uma entrada completa e válida."""
    validate_indicator_input(
        valid_dataframe,
        period=9,
    )
