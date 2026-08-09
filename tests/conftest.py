"""Fixtures compartilhadas dos testes do WINQuantLab."""

from pathlib import Path

import pandas as pd
import pytest

from data.loader import load_data
from data.normalizer import normalize


@pytest.fixture
def market_data() -> pd.DataFrame:
    """
    Carrega e normaliza os dados usados nos testes de indicadores.

    Returns
    -------
    pd.DataFrame
        DataFrame normalizado contendo os dados de mercado.
    """
    dataframe = load_data(
        Path("tests/data/market_data.csv"),
    )

    return normalize(dataframe)
