import pandas as pd
import pytest

from strategies.breakout import breakout


def test_breakout_creates_strategy_columns():
    df = pd.DataFrame(
        {
            "high": [10.0, 11.0, 12.0, 13.0],
            "low": [8.0, 9.0, 10.0, 11.0],
            "close": [9.0, 10.0, 11.0, 12.0],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert "breakout_high" in result.columns
    assert "breakout_low" in result.columns
    assert "signal" in result.columns


def test_breakout_calculates_high_from_previous_candles():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                12.0,
                11.0,
                15.0,
            ],
            "low": [
                8.0,
                9.0,
                9.0,
                10.0,
            ],
            "close": [
                9.0,
                11.0,
                10.0,
                14.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert pd.isna(result["breakout_high"].iloc[0])
    assert pd.isna(result["breakout_high"].iloc[1])
    assert pd.isna(result["breakout_high"].iloc[2])

    assert result["breakout_high"].iloc[3] == 12.0


def test_breakout_calculates_low_from_previous_candles():
    df = pd.DataFrame(
        {
            "high": [
                12.0,
                13.0,
                14.0,
                11.0,
            ],
            "low": [
                10.0,
                8.0,
                9.0,
                6.0,
            ],
            "close": [
                11.0,
                9.0,
                13.0,
                7.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert pd.isna(result["breakout_low"].iloc[0])
    assert pd.isna(result["breakout_low"].iloc[1])
    assert pd.isna(result["breakout_low"].iloc[2])

    assert result["breakout_low"].iloc[3] == 8.0


def test_breakout_generates_buy_signal():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
                14.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
                11.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
                13.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["signal"].tolist() == [
        0,
        0,
        0,
        1,
    ]


def test_breakout_generates_sell_signal():
    df = pd.DataFrame(
        {
            "high": [
                12.0,
                13.0,
                14.0,
                11.0,
            ],
            "low": [
                10.0,
                9.0,
                8.0,
                6.0,
            ],
            "close": [
                11.0,
                10.0,
                9.0,
                7.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["signal"].tolist() == [
        0,
        0,
        0,
        -1,
    ]


def test_breakout_does_not_signal_when_close_equals_level():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                12.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
            ],
            "low": [
                8.0,
                9.0,
                8.0,
                8.0,
                7.0,
                6.0,
                6.0,
            ],
            "close": [
                9.0,
                11.0,
                10.0,
                12.0,
                9.0,
                8.0,
                6.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["signal"].iloc[3] == 0
    assert result["signal"].iloc[6] == 0


def test_breakout_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
                14.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
                11.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
                13.0,
            ],
        }
    )

    original = df.copy(deep=True)

    breakout(
        df,
        lookback=3,
    )

    pd.testing.assert_frame_equal(
        df,
        original,
    )


def test_breakout_raises_error_when_lookback_is_zero():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="lookback must be greater than zero",
    ):
        breakout(
            df,
            lookback=0,
        )


def test_breakout_raises_error_when_lookback_is_negative():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="lookback must be greater than zero",
    ):
        breakout(
            df,
            lookback=-1,
        )


def test_breakout_raises_error_when_high_is_missing():
    df = pd.DataFrame(
        {
            "low": [
                8.0,
                9.0,
                10.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'high' was not found",
    ):
        breakout(
            df,
            lookback=2,
        )


def test_breakout_raises_error_when_low_is_missing():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'low' was not found",
    ):
        breakout(
            df,
            lookback=2,
        )


def test_breakout_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'close' was not found",
    ):
        breakout(
            df,
            lookback=2,
        )
def test_breakout_does_not_signal_during_warmup():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["signal"].iloc[:3].tolist() == [
        0,
        0,
        0,
    ]

def test_breakout_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "high": pd.Series(dtype=float),
            "low": pd.Series(dtype=float),
            "close": pd.Series(dtype=float),
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result.empty
    assert "breakout_high" in result.columns
    assert "breakout_low" in result.columns
    assert "signal" in result.columns


def test_breakout_does_not_signal_when_only_wick_breaks_level():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                11.0,
                12.0,
                14.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
                7.0,
            ],
            "close": [
                9.0,
                10.0,
                11.0,
                10.0,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["breakout_high"].iloc[3] == 12.0
    assert result["breakout_low"].iloc[3] == 8.0
    assert result["signal"].iloc[3] == 0

def test_breakout_generates_no_signal_inside_range():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                12.0,
                11.0,
                11.5,
            ],
            "low": [
                8.0,
                9.0,
                8.5,
                9.0,
            ],
            "close": [
                9.0,
                11.0,
                10.0,
                10.5,
            ],
        }
    )

    result = breakout(
        df,
        lookback=3,
    )

    assert result["breakout_high"].iloc[3] == 12.0
    assert result["breakout_low"].iloc[3] == 8.0
    assert result["signal"].iloc[3] == 0


def test_breakout_accepts_lookback_of_one():
    df = pd.DataFrame(
        {
            "high": [
                10.0,
                12.0,
                13.0,
            ],
            "low": [
                8.0,
                9.0,
                10.0,
            ],
            "close": [
                9.0,
                11.0,
                12.5,
            ],
        }
    )

    result = breakout(
        df,
        lookback=1,
    )

    assert pd.isna(result["breakout_high"].iloc[0])
    assert pd.isna(result["breakout_low"].iloc[0])

    assert result["breakout_high"].iloc[1] == 10.0
    assert result["breakout_low"].iloc[1] == 8.0

    assert result["breakout_high"].iloc[2] == 12.0
    assert result["breakout_low"].iloc[2] == 9.0
