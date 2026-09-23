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
            "high": [
                105.0,
                116.0,
                126.0,
            ],
            "low": [
                99.0,
                109.0,
                119.0,
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
            "high": [
                103.0,
                109.0,
                116.0,
            ],
            "low": [
                99.0,
                104.0,
                109.0,
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
            "high": [
                106.0,
            ],
            "low": [
                99.0,
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
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                99.0,
                104.0,
                109.0,
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
            "high": [
                105.0,
                110.0,
                115.0,
            ],
            "low": [
                99.0,
                104.0,
                109.0,
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
            "high": [
                105.0,
                116.0,
                126.0,
            ],
            "low": [
                99.0,
                109.0,
                119.0,
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
            "high": [
                105.0,
                116.0,
                126.0,
            ],
            "low": [
                99.0,
                109.0,
                119.0,
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
            "high": [
                105.0,
                116.0,
                125.0,
                130.0,
            ],
            "low": [
                99.0,
                109.0,
                119.0,
                124.0,
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


def test_backtest_calculates_long_mfe_points():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 132],
            "low": [98, 108, 115, 125, 128],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_points"] == 30


def test_backtest_calculates_long_mae_points():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 132],
            "low": [98, 105, 115, 107, 90],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_points"] == -5


def test_backtest_calculates_short_mfe_points():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 115, 120],
            "high": [155, 145, 135, 125, 150],
            "low": [145, 125, 110, 105, 90],
            "close": [148, 130, 115, 120, 125],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_points"] == 35


def test_backtest_calculates_short_mae_points():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 145, 150],
            "high": [155, 145, 150, 160, 190],
            "low": [145, 125, 120, 130, 140],
            "close": [148, 130, 140, 150, 155],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_points"] == -20


def test_backtest_raises_error_when_high_is_missing():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120],
            "low": [98, 108, 115],
            "close": [103, 115, 118],
            "signal": [1, 0, 0],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'high' was not found",
    ):
        backtest(df)


def test_backtest_raises_error_when_low_is_missing():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120],
            "high": [105, 115, 125],
            "close": [103, 115, 118],
            "signal": [1, 0, 0],
        }
    )

    with pytest.raises(
        ValueError,
        match="The column 'low' was not found",
    ):
        backtest(df)


def test_backtest_includes_last_candle_in_long_mfe_on_forced_close():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 130],
            "high": [105, 115, 125, 160],
            "low": [98, 108, 115, 125],
            "close": [103, 115, 125, 140],
            "signal": [1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_points"] == 50


def test_backtest_includes_last_candle_in_long_mae_on_forced_close():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 115],
            "high": [105, 115, 125, 120],
            "low": [98, 108, 105, 80],
            "close": [103, 115, 110, 100],
            "signal": [1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_points"] == -30


def test_backtest_includes_last_candle_in_short_mfe_on_forced_close():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 120],
            "high": [155, 145, 135, 125],
            "low": [145, 135, 120, 90],
            "close": [148, 135, 125, 100],
            "signal": [-1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_points"] == 50


def test_backtest_includes_last_candle_in_short_mae_on_forced_close():
    df = pd.DataFrame(
        {
            "open": [150, 140, 145, 150],
            "high": [155, 145, 150, 180],
            "low": [145, 135, 130, 140],
            "close": [148, 140, 145, 170],
            "signal": [-1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_points"] == -40


def test_backtest_records_long_favorable_price():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 200],
            "low": [98, 108, 115, 125, 128],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["favorable_price"] == 140


def test_backtest_records_long_adverse_price():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 132],
            "low": [98, 105, 115, 107, 80],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["adverse_price"] == 105


def test_backtest_records_short_favorable_price():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 115, 120],
            "high": [155, 145, 135, 125, 150],
            "low": [145, 125, 110, 105, 80],
            "close": [148, 130, 115, 120, 125],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["favorable_price"] == 105


def test_backtest_records_short_adverse_price():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 145, 150],
            "high": [155, 145, 150, 160, 200],
            "low": [145, 125, 120, 130, 140],
            "close": [148, 130, 140, 150, 155],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["adverse_price"] == 160


def test_backtest_records_long_mfe_index():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 200],
            "low": [98, 108, 115, 125, 80],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_index"] == 2


def test_backtest_records_long_mae_index():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 135, 130],
            "high": [105, 125, 140, 138, 200],
            "low": [98, 105, 115, 107, 80],
            "close": [103, 120, 135, 130, 129],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_index"] == 1


def test_backtest_records_short_mfe_index():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 115, 120],
            "high": [155, 145, 135, 125, 150],
            "low": [145, 125, 110, 105, 80],
            "close": [148, 130, 115, 120, 125],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_index"] == 3


def test_backtest_records_short_mae_index():
    df = pd.DataFrame(
        {
            "open": [150, 140, 130, 145, 150],
            "high": [155, 145, 150, 160, 200],
            "low": [145, 125, 120, 130, 140],
            "close": [148, 130, 140, 150, 155],
            "signal": [-1, 0, 0, 1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mae_index"] == 3


def test_backtest_records_first_occurrence_of_long_mfe_index():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 130, 135],
            "high": [105, 140, 140, 135, 200],
            "low": [98, 108, 115, 125, 80],
            "close": [103, 120, 130, 132, 134],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["favorable_price"] == 140
    assert trades[0]["mfe_index"] == 1


def test_backtest_records_win_outcome():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120],
            "high": [105, 125, 135],
            "low": [98, 108, 115],
            "close": [103, 120, 130],
            "signal": [1, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["pnl_points"] == 20
    assert trades[0]["outcome"] == "win"


def test_backtest_records_loss_outcome_despite_favorable_excursion():
    df = pd.DataFrame(
        {
            "open": [100, 110, 130, 105],
            "high": [105, 135, 150, 110],
            "low": [98, 108, 125, 100],
            "close": [103, 130, 140, 105],
            "signal": [1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["mfe_points"] == 40
    assert trades[0]["pnl_points"] == -5
    assert trades[0]["outcome"] == "loss"


def test_backtest_records_even_outcome():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120],
            "high": [105, 125, 130],
            "low": [98, 105, 108],
            "close": [103, 120, 110],
            "signal": [1, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["pnl_points"] == 0
    assert trades[0]["outcome"] == "even"


def test_backtest_records_duration_candles_on_opposite_signal_exit():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 130, 125],
            "high": [105, 115, 125, 135, 130],
            "low": [98, 108, 118, 128, 120],
            "close": [103, 115, 125, 132, 123],
            "signal": [1, 0, 0, -1, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["entry_index"] == 1
    assert trades[0]["exit_index"] == 4
    assert trades[0]["duration_candles"] == 3


def test_backtest_records_duration_candles_on_forced_close():
    df = pd.DataFrame(
        {
            "open": [100, 110, 120, 130],
            "high": [105, 115, 125, 135],
            "low": [98, 108, 118, 128],
            "close": [103, 115, 125, 132],
            "signal": [1, 0, 0, 0],
        }
    )

    trades = backtest(df)

    assert trades[0]["entry_index"] == 1
    assert trades[0]["exit_index"] == 3
    assert trades[0]["duration_candles"] == 3
