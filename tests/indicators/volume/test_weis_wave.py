import pandas as pd
import pytest

from indicators.volume.weis_wave import weis_wave


def test_weis_wave_creates_columns():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
            "volume": [100, 200, 300],
        }
    )

    result = weis_wave(df)

    assert "weis_wave_direction" in result.columns
    assert "weis_wave_volume" in result.columns


def test_weis_wave_accumulates_volume_in_up_wave():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0, 13.0],
            "volume": [100, 200, 300, 400],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0, 1, 1, 1],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0, 300.0, 600.0, 1000.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_accumulates_volume_in_down_wave():
    df = pd.DataFrame(
        {
            "close": [13.0, 12.0, 11.0, 10.0],
            "volume": [100, 200, 300, 400],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0, -1, -1, -1],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0, 300.0, 600.0, 1000.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_resets_volume_on_direction_change():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0, 11.0, 10.0, 11.0],
            "volume": [100, 200, 300, 400, 500, 600],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0, 1, 1, -1, -1, 1],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0, 300.0, 600.0, 400.0, 900.0, 600.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_keeps_direction_when_close_is_equal():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 11.0, 12.0],
            "volume": [100, 200, 300, 400],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0, 1, 1, 1],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0, 300.0, 600.0, 1000.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_accumulates_initial_neutral_volume():
    df = pd.DataFrame(
        {
            "close": [10.0, 10.0, 10.0, 11.0],
            "volume": [100, 200, 300, 400],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0, 0, 0, 1],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0, 300.0, 600.0, 1000.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "close": pd.Series(dtype=float),
            "volume": pd.Series(dtype=float),
        }
    )

    result = weis_wave(df)

    assert result.empty
    assert "weis_wave_direction" in result.columns
    assert "weis_wave_volume" in result.columns


def test_weis_wave_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "volume": [100, 200, 300],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        weis_wave(df)


def test_weis_wave_raises_error_when_volume_is_missing():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        weis_wave(df)


def test_weis_wave_handles_single_row():
    df = pd.DataFrame(
        {
            "close": [10.0],
            "volume": [100],
        }
    )

    result = weis_wave(df)

    expected_direction = pd.Series(
        [0],
        name="weis_wave_direction",
    )

    expected_volume = pd.Series(
        [100.0],
        name="weis_wave_volume",
    )

    pd.testing.assert_series_equal(
        result["weis_wave_direction"],
        expected_direction,
    )

    pd.testing.assert_series_equal(
        result["weis_wave_volume"],
        expected_volume,
    )


def test_weis_wave_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "close": [10.0, 11.0, 12.0, 11.0],
            "volume": [100, 200, 300, 400],
        }
    )

    original = df.copy(deep=True)

    weis_wave(df)

    pd.testing.assert_frame_equal(
        df,
        original,
    )
