import pandas as pd


def sma(
    dataframe: pd.DataFrame,
    period: int = 9,
) -> pd.DataFrame:
    """
    Calcula a Média Móvel Simples (Simple Moving Average).

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame contendo a coluna 'close'.

    period : int
        Quantidade de períodos da média.

    Returns
    -------
    pd.DataFrame
        DataFrame com a coluna sma_<period>.
    """

    if period <= 0:
        raise ValueError(
            "O período deve ser maior que zero."
        )

    if "close" not in dataframe.columns:
        raise ValueError(
            "A coluna 'close' não foi encontrada."
        )

    dataframe[f"sma_{period}"] = (
        dataframe["close"]
        .rolling(window=period)
        .mean()
    )

    return dataframe
