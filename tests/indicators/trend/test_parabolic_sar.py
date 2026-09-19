import pandas as pd
import pytest

from indicators.trend.parabolic_sar import parabolic_sar


def test_parabolic_sar_creates_column():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12, 13, 14],
            "low": [8, 9, 10, 11, 12],
        }
    )

    result = parabolic_sar(df)

    assert "parabolic_sar" in result.columns


def test_parabolic_sar_returns_numeric_values():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12, 13, 14, 15],
            "low": [8, 9, 10, 11, 12, 13],
        }
    )

    result = parabolic_sar(df)

    assert result["parabolic_sar"].notna().any()


def test_parabolic_sar_stays_below_price_in_uptrend():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12, 13, 14, 15, 16],
            "low": [8, 9, 10, 11, 12, 13, 14],
        }
    )

    result = parabolic_sar(df)

    valid = result["parabolic_sar"].dropna()

    assert (valid <= df.loc[valid.index, "low"]).all()


def test_parabolic_sar_stays_above_price_in_downtrend():
    df = pd.DataFrame(
        {
            "high": [16, 15, 14, 13, 12, 11, 10],
            "low": [14, 13, 12, 11, 10, 9, 8],
        }
    )

    result = parabolic_sar(df)

    valid = result["parabolic_sar"].dropna()

    assert (valid >= df.loc[valid.index, "high"]).all()


def test_parabolic_sar_reverses_direction():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12, 13, 12, 11, 10],
            "low": [8, 9, 10, 11, 10, 9, 8],
        }
    )

    result = parabolic_sar(df)

    sar = result["parabolic_sar"]

    assert sar.iloc[-1] >= df["high"].iloc[-1]



def test_parabolic_sar_invalid_step():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12],
            "low": [8, 9, 10],
        }
    )

    with pytest.raises(ValueError):
        parabolic_sar(
            df,
            step=0,
        )


def test_parabolic_sar_invalid_max_step():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12],
            "low": [8, 9, 10],
        }
    )

    with pytest.raises(ValueError):
        parabolic_sar(
            df,
            max_step=0,
        )


def test_parabolic_sar_missing_high_column():
    df = pd.DataFrame(
        {
            "low": [8, 9, 10],
        }
    )

    with pytest.raises(ValueError):
        parabolic_sar(df)


def test_parabolic_sar_missing_low_column():
    df = pd.DataFrame(
        {
            "high": [10, 11, 12],
        }
    )

    with pytest.raises(ValueError):
        parabolic_sar(df)


def test_parabolic_sar_empty_dataframe():
    df = pd.DataFrame(
        {
            "high": pd.Series(dtype="float64"),
            "low": pd.Series(dtype="float64"),
        }
    )

    result = parabolic_sar(df)

    assert "parabolic_sar" in result.columns
    assert result.empty


def test_parabolic_sar_single_row():
    df = pd.DataFrame(
        {
            "high": [10.0],
            "low": [8.0],
        }
    )

    result = parabolic_sar(df)

    assert result["parabolic_sar"].iloc[0] == 8.0
