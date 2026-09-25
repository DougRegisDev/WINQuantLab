import pandas as pd

from backtesting.pipeline import (
    create_period_summary,
    run_sessions,
    split_sessions,
)


def test_split_sessions_separates_market_data_by_date():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                ]
            ),
            "open": [100.0, 101.0, 200.0, 201.0],
            "high": [110.0, 111.0, 210.0, 211.0],
            "low": [90.0, 91.0, 190.0, 191.0],
            "close": [105.0, 106.0, 205.0, 206.0],
            "volume": [1000.0, 1100.0, 2000.0, 2100.0],
        }
    )

    sessions = split_sessions(market_data)

    assert len(sessions) == 2

    assert sessions[0]["session"].isoformat() == "2024-09-16"
    assert len(sessions[0]["data"]) == 2

    assert sessions[1]["session"].isoformat() == "2024-09-17"
    assert len(sessions[1]["data"]) == 2


def test_split_sessions_resets_each_session_index():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                ]
            ),
            "close": [100.0, 101.0, 200.0, 201.0],
        },
        index=[10, 11, 20, 21],
    )

    sessions = split_sessions(market_data)

    assert sessions[0]["data"].index.tolist() == [0, 1]
    assert sessions[1]["data"].index.tolist() == [0, 1]


def test_split_sessions_does_not_mutate_input_dataframe():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-17 09:00:00",
                ]
            ),
            "close": [100.0, 101.0, 200.0],
        },
        index=[10, 11, 20],
    )

    original = market_data.copy(deep=True)

    split_sessions(market_data)

    pd.testing.assert_frame_equal(
        market_data,
        original,
    )


def test_split_sessions_requires_datetime_column():
    market_data = pd.DataFrame(
        {
            "open": [100.0],
            "high": [110.0],
            "low": [90.0],
            "close": [105.0],
            "volume": [1000.0],
        }
    )

    try:
        split_sessions(market_data)
    except ValueError as error:
        assert str(error) == "The column 'datetime' was not found"
    else:
        raise AssertionError("ValueError was not raised")


def test_split_sessions_sorts_candles_by_datetime():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:10:00",
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                ]
            ),
            "close": [102.0, 100.0, 101.0],
        }
    )

    sessions = split_sessions(market_data)

    session_data = sessions[0]["data"]

    assert session_data["datetime"].tolist() == list(
        pd.to_datetime(
            [
                "2024-09-16 09:00:00",
                "2024-09-16 09:05:00",
                "2024-09-16 09:10:00",
            ]
        )
    )


def test_split_sessions_returns_empty_list_for_empty_dataframe():
    market_data = pd.DataFrame(
        {
            "datetime": pd.Series(
                [],
                dtype="datetime64[ns]",
            ),
            "open": pd.Series(dtype=float),
            "high": pd.Series(dtype=float),
            "low": pd.Series(dtype=float),
            "close": pd.Series(dtype=float),
            "volume": pd.Series(dtype=float),
        }
    )

    sessions = split_sessions(market_data)

    assert sessions == []


def test_run_sessions_executes_strategy_for_each_session():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                ]
            ),
            "open": [100.0, 101.0, 200.0, 201.0],
            "high": [110.0, 111.0, 210.0, 211.0],
            "low": [90.0, 91.0, 190.0, 191.0],
            "close": [105.0, 106.0, 205.0, 206.0],
            "volume": [1000.0, 1100.0, 2000.0, 2100.0],
        }
    )

    received_sessions = []

    def strategy(session_data):
        received_sessions.append(
            session_data.copy()
        )

        result = session_data.copy()
        result["signal"] = 0

        return result

    from backtesting.pipeline import run_sessions

    run_sessions(
        market_data,
        strategy,
    )

    assert len(received_sessions) == 2

    assert received_sessions[0]["datetime"].dt.date.nunique() == 1
    assert received_sessions[1]["datetime"].dt.date.nunique() == 1

    assert len(received_sessions[0]) == 2
    assert len(received_sessions[1]) == 2


def test_run_sessions_backtests_each_session_independently():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                    "2024-09-17 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                102.0,
                200.0,
                201.0,
                202.0,
            ],
            "high": [
                101.0,
                102.0,
                103.0,
                201.0,
                202.0,
                203.0,
            ],
            "low": [
                99.0,
                100.0,
                101.0,
                199.0,
                200.0,
                201.0,
            ],
            "close": [
                100.0,
                101.0,
                103.0,
                200.0,
                201.0,
                203.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                2000.0,
                2100.0,
                2200.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()
        result["signal"] = [1, 0, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    assert len(results) == 2

    assert len(results[0]["trades"]) == 1
    assert len(results[1]["trades"]) == 1

    assert results[0]["trades"][0]["entry_price"] == 101.0
    assert results[0]["trades"][0]["exit_price"] == 103.0

    assert results[1]["trades"][0]["entry_price"] == 201.0
    assert results[1]["trades"][0]["exit_price"] == 203.0


def test_run_sessions_preserves_session_without_trades():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                ]
            ),
            "open": [100.0, 101.0, 200.0, 201.0],
            "high": [110.0, 111.0, 210.0, 211.0],
            "low": [90.0, 91.0, 190.0, 191.0],
            "close": [105.0, 106.0, 205.0, 206.0],
            "volume": [1000.0, 1100.0, 2000.0, 2100.0],
        }
    )

    def strategy(session_data):
        result = session_data.copy()
        result["signal"] = 0

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    assert len(results) == 2

    assert results[0]["session"].isoformat() == "2024-09-16"
    assert results[0]["trades"] == []

    assert results[1]["session"].isoformat() == "2024-09-17"
    assert results[1]["trades"] == []


def test_run_sessions_associates_session_with_each_trade():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                    "2024-09-17 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                102.0,
                200.0,
                201.0,
                202.0,
            ],
            "high": [
                101.0,
                102.0,
                103.0,
                201.0,
                202.0,
                203.0,
            ],
            "low": [
                99.0,
                100.0,
                101.0,
                199.0,
                200.0,
                201.0,
            ],
            "close": [
                100.0,
                101.0,
                103.0,
                200.0,
                201.0,
                203.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                2000.0,
                2100.0,
                2200.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()
        result["signal"] = [1, 0, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    first_trade = results[0]["trades"][0]
    second_trade = results[1]["trades"][0]

    assert first_trade["session"].isoformat() == "2024-09-16"
    assert second_trade["session"].isoformat() == "2024-09-17"


def test_run_sessions_creates_basic_session_summary():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                    "2024-09-17 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                102.0,
                200.0,
                201.0,
                202.0,
            ],
            "high": [
                101.0,
                102.0,
                103.0,
                201.0,
                202.0,
                203.0,
            ],
            "low": [
                99.0,
                100.0,
                101.0,
                199.0,
                200.0,
                201.0,
            ],
            "close": [
                100.0,
                101.0,
                103.0,
                200.0,
                201.0,
                203.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                2000.0,
                2100.0,
                2200.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()

        if result["close"].iloc[0] < 150.0:
            result["signal"] = [1, 0, 0]
        else:
            result["signal"] = [0, 0, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    first_summary = results[0]["summary"]
    second_summary = results[1]["summary"]

    assert first_summary["session"].isoformat() == "2024-09-16"
    assert first_summary["candles"] == 3
    assert first_summary["trades"] == 1

    assert second_summary["session"].isoformat() == "2024-09-17"
    assert second_summary["candles"] == 3
    assert second_summary["trades"] == 0


def test_session_summary_counts_trade_directions_and_outcomes():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-16 09:15:00",
                    "2024-09-16 09:20:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                105.0,
                104.0,
                100.0,
            ],
            "high": [
                101.0,
                106.0,
                106.0,
                105.0,
                101.0,
            ],
            "low": [
                99.0,
                100.0,
                103.0,
                99.0,
                99.0,
            ],
            "close": [
                100.0,
                105.0,
                104.0,
                100.0,
                101.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                1300.0,
                1400.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()
        result["signal"] = [1, -1, 0, -1, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    summary = results[0]["summary"]

    assert summary["trades"] == 2
    assert summary["longs"] == 1
    assert summary["shorts"] == 1
    assert summary["wins"] == 1
    assert summary["losses"] == 1
    assert summary["evens"] == 0


def test_session_summary_calculates_total_pnl_points():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                    "2024-09-17 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                105.0,
                200.0,
                201.0,
                202.0,
            ],
            "high": [
                101.0,
                106.0,
                106.0,
                201.0,
                202.0,
                203.0,
            ],
            "low": [
                99.0,
                100.0,
                104.0,
                199.0,
                200.0,
                201.0,
            ],
            "close": [
                100.0,
                105.0,
                105.0,
                200.0,
                201.0,
                202.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                1300.0,
                1400.0,
                1500.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()

        if result["close"].iloc[0] < 150:
            result["signal"] = [1, -1, 0]
        else:
            result["signal"] = [0, 0, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    first_summary = results[0]["summary"]
    second_summary = results[1]["summary"]

    assert first_summary["pnl_points"] == 4.0
    assert second_summary["pnl_points"] == 0.0


def test_session_summary_calculates_total_mfe_and_mae_points():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                105.0,
            ],
            "high": [
                101.0,
                106.0,
                107.0,
            ],
            "low": [
                99.0,
                99.0,
                103.0,
            ],
            "close": [
                100.0,
                105.0,
                105.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()
        result["signal"] = [1, -1, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    summary = results[0]["summary"]

    assert summary["mfe_points"] == 5.0
    assert summary["mae_points"] == -2.0


def test_session_summary_calculates_average_mfe_and_mae_points():
    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2024-09-16 09:00:00",
                    "2024-09-16 09:05:00",
                    "2024-09-16 09:10:00",
                    "2024-09-17 09:00:00",
                    "2024-09-17 09:05:00",
                    "2024-09-17 09:10:00",
                ]
            ),
            "open": [
                100.0,
                101.0,
                105.0,
                200.0,
                201.0,
                202.0,
            ],
            "high": [
                101.0,
                106.0,
                107.0,
                201.0,
                202.0,
                203.0,
            ],
            "low": [
                99.0,
                99.0,
                103.0,
                199.0,
                200.0,
                201.0,
            ],
            "close": [
                100.0,
                105.0,
                105.0,
                200.0,
                201.0,
                202.0,
            ],
            "volume": [
                1000.0,
                1100.0,
                1200.0,
                1300.0,
                1400.0,
                1500.0,
            ],
        }
    )

    def strategy(session_data):
        result = session_data.copy()

        if result["close"].iloc[0] < 150:
            result["signal"] = [1, -1, 0]
        else:
            result["signal"] = [0, 0, 0]

        return result

    results = run_sessions(
        market_data,
        strategy,
    )

    first_summary = results[0]["summary"]
    second_summary = results[1]["summary"]

    assert first_summary["average_mfe_points"] == 5.0
    assert first_summary["average_mae_points"] == -2.0

    assert second_summary["average_mfe_points"] == 0.0
    assert second_summary["average_mae_points"] == 0.0


def test_create_period_summary_counts_sessions_and_trades():
    session_results = [
        {
            "summary": {
                "session": pd.Timestamp("2024-09-16").date(),
                "candles": 100,
                "trades": 2,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-17").date(),
                "candles": 110,
                "trades": 0,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-18").date(),
                "candles": 105,
                "trades": 3,
            }
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["sessions"] == 3
    assert summary["sessions_with_trades"] == 2
    assert summary["sessions_without_trades"] == 1
    assert summary["trades"] == 5


def test_create_period_summary_consolidates_session_activity():
    session_results = [
        {
            "summary": {
                "session": pd.Timestamp("2024-09-16").date(),
                "candles": 100,
                "trades": 3,
                "longs": 2,
                "shorts": 1,
                "wins": 2,
                "losses": 1,
                "evens": 0,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-17").date(),
                "candles": 110,
                "trades": 0,
                "longs": 0,
                "shorts": 0,
                "wins": 0,
                "losses": 0,
                "evens": 0,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-18").date(),
                "candles": 90,
                "trades": 2,
                "longs": 1,
                "shorts": 1,
                "wins": 0,
                "losses": 1,
                "evens": 1,
            }
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["candles"] == 300
    assert summary["longs"] == 3
    assert summary["shorts"] == 2
    assert summary["wins"] == 2
    assert summary["losses"] == 2
    assert summary["evens"] == 1


def test_create_period_summary_consolidates_pnl_points():
    session_results = [
        {
            "summary": {
                "session": pd.Timestamp("2024-09-16").date(),
                "candles": 100,
                "trades": 2,
                "pnl_points": 350.0,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-17").date(),
                "candles": 110,
                "trades": 0,
                "pnl_points": 0.0,
            }
        },
        {
            "summary": {
                "session": pd.Timestamp("2024-09-18").date(),
                "candles": 105,
                "trades": 3,
                "pnl_points": -150.0,
            }
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["pnl_points"] == 200.0


def test_create_period_summary_calculates_average_trade_excursions():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 400.0,
                    "mae_points": -100.0,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -200.0,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 0,
            },
            "trades": [],
        },
        {
            "summary": {
                "candles": 105,
                "trades": 1,
            },
            "trades": [
                {
                    "mfe_points": 600.0,
                    "mae_points": -300.0,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["average_mfe_points"] == 400.0
    assert summary["average_mae_points"] == -200.0


def test_create_period_summary_calculates_median_trade_excursions():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 100.0,
                    "mae_points": -50.0,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -100.0,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 300.0,
                    "mae_points": -150.0,
                },
                {
                    "mfe_points": 2000.0,
                    "mae_points": -500.0,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["median_mfe_points"] == 250.0
    assert summary["median_mae_points"] == -125.0


def test_create_period_summary_calculates_excursion_percentiles():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 100.0,
                    "mae_points": -400.0,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -300.0,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 3,
            },
            "trades": [
                {
                    "mfe_points": 300.0,
                    "mae_points": -200.0,
                },
                {
                    "mfe_points": 400.0,
                    "mae_points": -100.0,
                },
                {
                    "mfe_points": 500.0,
                    "mae_points": 0.0,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["mfe_p25"] == 200.0
    assert summary["mfe_p50"] == 300.0
    assert summary["mfe_p75"] == 400.0

    assert summary["mae_p25"] == -300.0
    assert summary["mae_p50"] == -200.0
    assert summary["mae_p75"] == -100.0


def test_create_period_summary_calculates_average_trade_duration():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 100.0,
                    "mae_points": -50.0,
                    "duration_candles": 10,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -100.0,
                    "duration_candles": 20,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 1,
            },
            "trades": [
                {
                    "mfe_points": 300.0,
                    "mae_points": -150.0,
                    "duration_candles": 30,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["average_duration_candles"] == 20.0


def test_create_period_summary_calculates_median_trade_duration():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 100.0,
                    "mae_points": -50.0,
                    "duration_candles": 5,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -100.0,
                    "duration_candles": 10,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 300.0,
                    "mae_points": -150.0,
                    "duration_candles": 20,
                },
                {
                    "mfe_points": 400.0,
                    "mae_points": -200.0,
                    "duration_candles": 100,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["median_duration_candles"] == 15.0


def test_create_period_summary_calculates_duration_percentiles():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 2,
            },
            "trades": [
                {
                    "mfe_points": 100.0,
                    "mae_points": -50.0,
                    "duration_candles": 10,
                },
                {
                    "mfe_points": 200.0,
                    "mae_points": -100.0,
                    "duration_candles": 20,
                },
            ],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 3,
            },
            "trades": [
                {
                    "mfe_points": 300.0,
                    "mae_points": -150.0,
                    "duration_candles": 30,
                },
                {
                    "mfe_points": 400.0,
                    "mae_points": -200.0,
                    "duration_candles": 40,
                },
                {
                    "mfe_points": 500.0,
                    "mae_points": -250.0,
                    "duration_candles": 50,
                },
            ],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["duration_p25"] == 20.0
    assert summary["duration_p50"] == 30.0
    assert summary["duration_p75"] == 40.0


def test_create_period_summary_returns_zero_statistics_without_trades():
    session_results = [
        {
            "summary": {
                "candles": 100,
                "trades": 0,
            },
            "trades": [],
        },
        {
            "summary": {
                "candles": 110,
                "trades": 0,
            },
            "trades": [],
        },
    ]

    summary = create_period_summary(
        session_results
    )

    assert summary["average_mfe_points"] == 0.0
    assert summary["average_mae_points"] == 0.0
    assert summary["median_mfe_points"] == 0.0
    assert summary["median_mae_points"] == 0.0

    assert summary["average_duration_candles"] == 0.0
    assert summary["median_duration_candles"] == 0.0

    assert summary["mfe_p25"] == 0.0
    assert summary["mfe_p50"] == 0.0
    assert summary["mfe_p75"] == 0.0

    assert summary["mae_p25"] == 0.0
    assert summary["mae_p50"] == 0.0
    assert summary["mae_p75"] == 0.0

    assert summary["duration_p25"] == 0.0
    assert summary["duration_p50"] == 0.0
    assert summary["duration_p75"] == 0.0
