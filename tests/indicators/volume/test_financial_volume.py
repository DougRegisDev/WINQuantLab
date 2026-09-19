import pandas as pd
import pytest

from indicators.volume.financial_volume import financial_volume


def test_financial_volume_creates_column():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
            "volume": [100, 200, 300],
        }
    )

    result = financial_volume(df)

    assert "financial_volume" in result.columns


def test_financial_volume_calculates_expected_values():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
            "volume": [100, 200, 300],
        }
    )

    result = financial_volume(df)

    expected = pd.Series(
        [1000.0, 2200.0, 3600.0],
        name="financial_volume",
    )

    pd.testing.assert_series_equal(
        result["financial_volume"],
        expected,
    )


def test_financial_volume_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "volume": [100, 200, 300],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        financial_volume(df)


def test_financial_volume_raises_error_when_volume_is_missing():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        financial_volume(df)


def test_financial_volume_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "close": pd.Series(dtype=float),
            "volume": pd.Series(dtype=float),
        }
    )

    result = financial_volume(df)

    assert result.empty
    assert "financial_volume" in result.columns


def test_financial_volume_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
            "volume": [100, 200, 300],
        }
    )

    original = df.copy(deep=True)

    financial_volume(df)

    pd.testing.assert_frame_equal(
        df,
        original,
    )


def test_financial_volume_handles_zero_volume():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
            "volume": [100, 0, 300],
        }
    )

    result = financial_volume(df)

    expected = pd.Series(
        [1000.0, 0.0, 3600.0],
        name="financial_volume",
    )

    pd.testing.assert_series_equal(
        result["financial_volume"],
        expected,
    )
