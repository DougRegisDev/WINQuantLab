import pandas as pd
import pytest

from indicators.volume.vwap import vwap


def test_vwap_creates_column():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0, 12.0],
            "low": [8.0, 9.0, 10.0],
            "close": [9.0, 10.0, 11.0],
            "volume": [100, 200, 300],
        }
    )

    result = vwap(df)

    assert "vwap" in result.columns


def test_vwap_calculates_expected_values():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0, 12.0],
            "low": [8.0, 9.0, 10.0],
            "close": [9.0, 10.0, 11.0],
            "volume": [100, 200, 300],
        }
    )

    result = vwap(df)

    expected = pd.Series(
        [
            9.0,
            9.666666666666666,
            10.333333333333334,
        ],
        name="vwap",
    )

    pd.testing.assert_series_equal(
        result["vwap"],
        expected,
    )


def test_vwap_missing_high_column():
    df = pd.DataFrame(
        {
            "low": [8.0, 9.0],
            "close": [9.0, 10.0],
            "volume": [100, 200],
        }
    )

    with pytest.raises(ValueError):
        vwap(df)


def test_vwap_missing_low_column():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0],
            "close": [9.0, 10.0],
            "volume": [100, 200],
        }
    )

    with pytest.raises(ValueError):
        vwap(df)


def test_vwap_missing_close_column():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0],
            "low": [8.0, 9.0],
            "volume": [100, 200],
        }
    )

    with pytest.raises(ValueError):
        vwap(df)


def test_vwap_missing_volume_column():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0],
            "low": [8.0, 9.0],
            "close": [9.0, 10.0],
        }
    )

    with pytest.raises(ValueError):
        vwap(df)


def test_vwap_empty_dataframe():
    df = pd.DataFrame(
        {
            "high": pd.Series(dtype="float64"),
            "low": pd.Series(dtype="float64"),
            "close": pd.Series(dtype="float64"),
            "volume": pd.Series(dtype="float64"),
        }
    )

    result = vwap(df)

    assert "vwap" in result.columns
    assert result.empty


def test_vwap_zero_volume():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0, 12.0],
            "low": [8.0, 9.0, 10.0],
            "close": [9.0, 10.0, 11.0],
            "volume": [0, 0, 0],
        }
    )

    result = vwap(df)

    assert result["vwap"].isna().all()


def test_vwap_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0, 12.0],
            "low": [8.0, 9.0, 10.0],
            "close": [9.0, 10.0, 11.0],
            "volume": [100, 200, 300],
        }
    )

    original = df.copy()

    vwap(df)

    pd.testing.assert_frame_equal(
        df,
        original,
    )
