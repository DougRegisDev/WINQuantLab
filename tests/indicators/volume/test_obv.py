import pandas as pd
import pytest

from indicators.volume.obv import obv


def test_obv_creates_column():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 10.5],
            "volume": [100, 200, 300],
        }
    )

    result = obv(df)

    assert "obv" in result.columns


def test_obv_calculates_expected_values():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 10.5, 10.5, 12.0],
            "volume": [100, 200, 300, 400, 500],
        }
    )

    result = obv(df)

    expected = pd.Series(
        [0.0, 200.0, -100.0, -100.0, 400.0],
        name="obv",
    )

    pd.testing.assert_series_equal(
        result["obv"],
        expected,
    )


def test_obv_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "close": pd.Series(dtype=float),
            "volume": pd.Series(dtype=float),
        }
    )

    result = obv(df)

    assert result.empty
    assert "obv" in result.columns


def test_obv_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "volume": [100, 200, 300],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        obv(df)


def test_obv_raises_error_when_volume_is_missing():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        obv(df)


def test_obv_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 10.5],
            "volume": [100, 200, 300],
        }
    )

    original = df.copy(deep=True)

    obv(df)

    pd.testing.assert_frame_equal(
        df,
        original,
    )


def test_obv_handles_single_row():
    df = pd.DataFrame(
        {
            "close": [10.0],
            "volume": [100],
        }
    )

    result = obv(df)

    expected = pd.Series(
        [0.0],
        name="obv",
    )

    pd.testing.assert_series_equal(
        result["obv"],
        expected,
    )
