import pandas as pd
import pytest

from backtesting.engine import backtest


def test_backtest_returns_no_trades_when_there_are_no_signals():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                101.0,
                102.0,
            ],
            "high": [
                102.0,
                103.0,
                104.0,
            ],
            "low": [
                99.0,
                100.0,
                101.0,
            ],
            "close": [
                101.0,
                102.0,
                103.0,
            ],
            "signal": [
                0,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert result == []


def test_backtest_executes_long_on_next_candle_open():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                115.0,
            ],
            "high": [
                105.0,
                116.0,
                121.0,
            ],
            "low": [
                99.0,
                108.0,
                114.0,
            ],
            "close": [
                104.0,
                115.0,
                120.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "long"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0


def test_backtest_closes_long_on_last_candle():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                115.0,
            ],
            "high": [
                105.0,
                116.0,
                121.0,
            ],
            "low": [
                99.0,
                108.0,
                114.0,
            ],
            "close": [
                104.0,
                115.0,
                120.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert result[0]["exit_index"] == 2
    assert result[0]["exit_price"] == 120.0


def test_backtest_calculates_long_pnl_points():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                115.0,
            ],
            "high": [
                105.0,
                116.0,
                121.0,
            ],
            "low": [
                99.0,
                108.0,
                114.0,
            ],
            "close": [
                104.0,
                115.0,
                120.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert result[0]["quantity"] == 1
    assert result[0]["pnl_points"] == 10.0


def test_backtest_calculates_long_loss():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                105.0,
            ],
            "high": [
                105.0,
                112.0,
                107.0,
            ],
            "low": [
                99.0,
                104.0,
                98.0,
            ],
            "close": [
                104.0,
                105.0,
                100.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert result[0]["pnl_points"] == -10.0


def test_backtest_executes_short_on_next_candle_open():
    df = pd.DataFrame(
        {
            "open": [
                120.0,
                110.0,
                105.0,
            ],
            "high": [
                122.0,
                112.0,
                107.0,
            ],
            "low": [
                118.0,
                104.0,
                98.0,
            ],
            "close": [
                119.0,
                105.0,
                100.0,
            ],
            "signal": [
                -1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "short"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0


def test_backtest_calculates_short_pnl_points():
    df = pd.DataFrame(
        {
            "open": [
                120.0,
                110.0,
                105.0,
            ],
            "high": [
                122.0,
                112.0,
                107.0,
            ],
            "low": [
                118.0,
                104.0,
                98.0,
            ],
            "close": [
                119.0,
                105.0,
                100.0,
            ],
            "signal": [
                -1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert result[0]["quantity"] == 1
    assert result[0]["pnl_points"] == 10.0


def test_backtest_closes_long_on_opposite_signal():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
                125.0,
                130.0,
            ],
            "high": [
                105.0,
                115.0,
                125.0,
                130.0,
                135.0,
            ],
            "low": [
                99.0,
                108.0,
                118.0,
                123.0,
                128.0,
            ],
            "close": [
                104.0,
                114.0,
                124.0,
                129.0,
                134.0,
            ],
            "signal": [
                1,
                0,
                -1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "long"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0
    assert result[0]["exit_index"] == 3
    assert result[0]["exit_price"] == 125.0
    assert result[0]["pnl_points"] == 15.0


def test_backtest_closes_short_on_opposite_signal():
    df = pd.DataFrame(
        {
            "open": [
                130.0,
                120.0,
                110.0,
                105.0,
                100.0,
            ],
            "high": [
                132.0,
                122.0,
                112.0,
                107.0,
                102.0,
            ],
            "low": [
                128.0,
                118.0,
                108.0,
                103.0,
                98.0,
            ],
            "close": [
                129.0,
                119.0,
                109.0,
                104.0,
                99.0,
            ],
            "signal": [
                -1,
                0,
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "short"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 120.0
    assert result[0]["exit_index"] == 3
    assert result[0]["exit_price"] == 105.0
    assert result[0]["pnl_points"] == 15.0


def test_backtest_ignores_repeated_long_signal():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
                125.0,
            ],
            "high": [
                105.0,
                115.0,
                125.0,
                130.0,
            ],
            "low": [
                99.0,
                108.0,
                118.0,
                123.0,
            ],
            "close": [
                104.0,
                114.0,
                124.0,
                129.0,
            ],
            "signal": [
                1,
                1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "long"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0
    assert result[0]["quantity"] == 1


def test_backtest_ignores_repeated_short_signal():
    df = pd.DataFrame(
        {
            "open": [
                130.0,
                120.0,
                110.0,
                105.0,
            ],
            "high": [
                132.0,
                122.0,
                112.0,
                107.0,
            ],
            "low": [
                128.0,
                118.0,
                108.0,
                103.0,
            ],
            "close": [
                129.0,
                119.0,
                109.0,
                104.0,
            ],
            "signal": [
                -1,
                -1,
                0,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "short"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 120.0
    assert result[0]["quantity"] == 1


def test_backtest_executes_multiple_trades():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
                125.0,
                115.0,
                105.0,
                100.0,
            ],
            "high": [
                105.0,
                115.0,
                125.0,
                130.0,
                120.0,
                110.0,
                105.0,
            ],
            "low": [
                99.0,
                108.0,
                118.0,
                123.0,
                113.0,
                103.0,
                98.0,
            ],
            "close": [
                104.0,
                114.0,
                124.0,
                129.0,
                119.0,
                109.0,
                99.0,
            ],
            "signal": [
                1,
                0,
                -1,
                -1,
                0,
                1,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 2

    assert result[0]["direction"] == "long"
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0
    assert result[0]["exit_index"] == 3
    assert result[0]["exit_price"] == 125.0
    assert result[0]["pnl_points"] == 15.0

    assert result[1]["direction"] == "short"
    assert result[1]["entry_index"] == 4
    assert result[1]["entry_price"] == 115.0
    assert result[1]["exit_index"] == 6
    assert result[1]["exit_price"] == 100.0
    assert result[1]["pnl_points"] == 15.0


def test_backtest_ignores_signal_on_last_candle():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                98.0,
                103.0,
                108.0,
            ],
            "close": [
                104.0,
                109.0,
                114.0,
            ],
            "signal": [
                0,
                0,
                1,
            ],
        }
    )

    result = backtest(df)

    assert result == []


def test_backtest_handles_empty_dataframe():
    df = pd.DataFrame(
        {
            "open": [],
            "high": [],
            "low": [],
            "close": [],
            "signal": [],
        }
    )

    result = backtest(df)

    assert result == []


def test_backtest_raises_error_when_signal_is_missing():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                98.0,
                103.0,
                108.0,
            ],
            "close": [
                104.0,
                109.0,
                114.0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'signal' was not found",
    ):
        backtest(df)


def test_backtest_raises_error_when_open_is_missing():
    df = pd.DataFrame(
        {
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                98.0,
                103.0,
                108.0,
            ],
            "close": [
                104.0,
                109.0,
                114.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'open' was not found",
    ):
        backtest(df)


def test_backtest_raises_error_when_close_is_missing():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                98.0,
                103.0,
                108.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'close' was not found",
    ):
        backtest(df)


def test_backtest_does_not_modify_original_dataframe():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
            ],
            "close": [
                104.0,
                115.0,
                125.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        }
    )

    original_df = df.copy(deep=True)

    backtest(df)

    pd.testing.assert_frame_equal(
        df,
        original_df,
    )


def test_backtest_closes_new_position_on_last_candle():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "close": [
                102.0,
                108.0,
                115.0,
            ],
            "signal": [
                0,
                1,
                0,
            ],
        }
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["direction"] == "long"
    assert result[0]["entry_index"] == 2
    assert result[0]["entry_price"] == 110.0
    assert result[0]["exit_index"] == 2
    assert result[0]["exit_price"] == 115.0
    assert result[0]["pnl_points"] == 5.0


def test_backtest_does_not_trade_with_single_candle():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
            ],
            "close": [
                105.0,
            ],
            "signal": [
                1,
            ],
        }
    )

    result = backtest(df)

    assert result == []


def test_backtest_raises_error_when_signal_is_invalid():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "close": [
                104.0,
                109.0,
                114.0,
            ],
            "signal": [
                0,
                2,
                0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="signal must contain only -1, 0, or 1",
    ):
        backtest(df)


def test_backtest_raises_error_when_signal_is_nan():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                105.0,
                110.0,
            ],
            "close": [
                104.0,
                109.0,
                114.0,
            ],
            "signal": [
                0,
                float("nan"),
                0,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="signal must contain only -1, 0, or 1",
    ):
        backtest(df)


def test_backtest_works_with_custom_dataframe_index():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
            ],
            "close": [
                104.0,
                115.0,
                125.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        },
        index=[
            10,
            20,
            30,
        ],
    )

    result = backtest(df)

    assert len(result) == 1
    assert result[0]["entry_index"] == 1
    assert result[0]["entry_price"] == 110.0
    assert result[0]["exit_index"] == 2
    assert result[0]["exit_price"] == 125.0
    assert result[0]["pnl_points"] == 15.0


def test_backtest_preserves_entry_and_exit_time():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
            ],
            "close": [
                104.0,
                115.0,
                125.0,
            ],
            "signal": [
                1,
                0,
                0,
            ],
        },
        index=pd.to_datetime(
            [
                "2026-09-23 09:00:00",
                "2026-09-23 09:05:00",
                "2026-09-23 09:10:00",
            ]
        ),
    )

    result = backtest(df)

    assert result[0]["entry_index"] == 1
    assert result[0]["exit_index"] == 2

    assert result[0]["entry_time"] == pd.Timestamp(
        "2026-09-23 09:05:00"
    )
    assert result[0]["exit_time"] == pd.Timestamp(
        "2026-09-23 09:10:00"
    )


def test_backtest_preserves_exit_time_on_opposite_signal():
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                110.0,
                120.0,
                125.0,
            ],
            "close": [
                104.0,
                115.0,
                124.0,
                129.0,
            ],
            "signal": [
                1,
                0,
                -1,
                0,
            ],
        },
        index=pd.to_datetime(
            [
                "2026-09-23 09:00:00",
                "2026-09-23 09:05:00",
                "2026-09-23 09:10:00",
                "2026-09-23 09:15:00",
            ]
        ),
    )

    result = backtest(df)

    assert len(result) == 1

    assert result[0]["entry_index"] == 1
    assert result[0]["entry_time"] == pd.Timestamp(
        "2026-09-23 09:05:00"
    )

    assert result[0]["exit_index"] == 3
    assert result[0]["exit_time"] == pd.Timestamp(
        "2026-09-23 09:15:00"
    )

    assert result[0]["entry_price"] == 110.0
    assert result[0]["exit_price"] == 125.0
    assert result[0]["pnl_points"] == 15.0
