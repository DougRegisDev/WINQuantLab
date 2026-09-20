import pandas as pd
import pytest

from strategies.moving_average_crossover import moving_average_crossover


def test_moving_average_crossover_creates_signal_column():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert "signal" in result.columns


def test_moving_average_crossover_calculates_moving_averages():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert "sma_2" in result.columns
    assert "sma_3" in result.columns


def test_moving_average_crossover_generates_buy_signal():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                9.0,
                8.0,
                9.0,
                10.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert result["signal"].tolist() == [
        0,
        0,
        0,
        0,
        1,
    ]


def test_moving_average_crossover_generates_sell_signal():
    df = pd.DataFrame(
        {
            "close": [
                8.0,
                9.0,
                10.0,
                9.0,
                8.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert result["signal"].tolist() == [
        0,
        0,
        0,
        0,
        -1,
    ]


def test_moving_average_crossover_signal_is_event_not_position():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                9.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert result["signal"].tolist() == [
        0,
        0,
        0,
        0,
        1,
        0,
        0,
    ]


def test_moving_average_crossover_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                9.0,
                8.0,
                9.0,
                10.0,
            ],
        }
    )

    original = df.copy(deep=True)

    moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    pd.testing.assert_frame_equal(
        df,
        original,
    )


def test_moving_average_crossover_raises_error_when_periods_are_equal():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="fast_period must be smaller than slow_period",
    ):
        moving_average_crossover(
            df,
            fast_period=3,
            slow_period=3,
        )


def test_moving_average_crossover_raises_error_when_fast_period_is_greater():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="fast_period must be smaller than slow_period",
    ):
        moving_average_crossover(
            df,
            fast_period=5,
            slow_period=3,
        )


def test_moving_average_crossover_propagates_invalid_period_error():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        moving_average_crossover(
            df,
            fast_period=0,
            slow_period=3,
        )


def test_moving_average_crossover_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "close": pd.Series(dtype=float),
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert result.empty
    assert "sma_2" in result.columns
    assert "sma_3" in result.columns
    assert "signal" in result.columns


def test_moving_average_crossover_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "volume": [
                100,
                200,
                300,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="A coluna 'close'",
    ):
        moving_average_crossover(
            df,
            fast_period=2,
            slow_period=3,
        )


def test_moving_average_crossover_does_not_signal_during_warmup():
    df = pd.DataFrame(
        {
            "close": [
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
            ],
        }
    )

    result = moving_average_crossover(
        df,
        fast_period=2,
        slow_period=3,
    )

    assert result["signal"].iloc[:3].tolist() == [
        0,
        0,
        0,
    ]
