import pandas as pd
import pytest

from cli import (
    STRATEGIES,
    create_parser,
    get_strategy_parameters,
    run_strategy,
)


def test_backtest_command_parses_arguments():
    parser = create_parser()

    args = parser.parse_args(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "breakout",
            "--lookback",
            "20",
        ]
    )

    assert args.command == "backtest"
    assert args.file == "market.csv"
    assert args.strategy == "breakout"
    assert args.lookback == 20


def test_backtest_command_rejects_unknown_strategy():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "backtest",
                "--file",
                "market.csv",
                "--strategy",
                "unknown",
            ]
        )


def test_backtest_command_rejects_invalid_lookback():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "backtest",
                "--file",
                "market.csv",
                "--strategy",
                "breakout",
                "--lookback",
                "0",
            ]
        )


def test_run_strategy_executes_breakout():
    market_data = pd.DataFrame(
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
                13.0,
            ],
        }
    )

    result = run_strategy(
        market_data,
        strategy_name="breakout",
        lookback=2,
    )

    assert "signal" in result.columns
    assert result["signal"].tolist() == [
        0,
        0,
        1,
    ]


def test_run_strategy_executes_moving_average_crossover():
    market_data = pd.DataFrame(
        {
            "close": [
                10.0,
                10.0,
                10.0,
                20.0,
                20.0,
            ],
        }
    )

    result = run_strategy(
        market_data,
        strategy_name="moving_average_crossover",
        fast_period=2,
        slow_period=3,
    )

    assert "signal" in result.columns


def test_strategy_registry_contains_strategy_functions():
    assert callable(STRATEGIES["breakout"]["function"])

    assert callable(STRATEGIES["moving_average_crossover"]["function"])

    assert STRATEGIES["breakout"]["parameters"] == ("lookback",)

    assert STRATEGIES["moving_average_crossover"]["parameters"] == (
        "fast_period",
        "slow_period",
    )


def test_backtest_command_parses_moving_average_parameters():
    parser = create_parser()

    args = parser.parse_args(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "moving_average_crossover",
            "--fast-period",
            "9",
            "--slow-period",
            "21",
        ]
    )

    assert args.fast_period == 9
    assert args.slow_period == 21


def test_get_strategy_parameters_for_breakout():
    parser = create_parser()

    args = parser.parse_args(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "breakout",
            "--lookback",
            "30",
        ]
    )

    parameters = get_strategy_parameters(args)

    assert parameters == {
        "lookback": 30,
    }


def test_get_strategy_parameters_for_moving_average_crossover():
    parser = create_parser()

    args = parser.parse_args(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "moving_average_crossover",
            "--fast-period",
            "5",
            "--slow-period",
            "15",
        ]
    )

    parameters = get_strategy_parameters(args)

    assert parameters == {
        "fast_period": 5,
        "slow_period": 15,
    }


def test_run_backtest_command_returns_report(
    monkeypatch,
):
    import cli

    market_data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2026-01-02 09:00:00",
                    "2026-01-02 09:05:00",
                    "2026-01-02 09:10:00",
                ]
            ),
            "open": [
                9.0,
                10.0,
                11.0,
            ],
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
                13.0,
            ],
            "volume": [
                100,
                110,
                120,
            ],
        }
    )

    monkeypatch.setattr(
        cli,
        "load_data",
        lambda file_path, header=None: market_data,
    )

    monkeypatch.setattr(
        cli,
        "normalize",
        lambda data, source=None: data,
    )

    parser = create_parser()

    args = parser.parse_args(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "breakout",
            "--lookback",
            "2",
        ]
    )

    report = cli.run_backtest_command(args)

    assert isinstance(report, str)
    assert "WINQuantLab - Backtest Report" in report
    assert "Strategy: breakout" in report
    assert "Parameters: lookback=2" in report


def test_main_prints_backtest_report(
    monkeypatch,
    capsys,
):
    import cli

    monkeypatch.setattr(
        cli,
        "run_backtest_command",
        lambda args: "BACKTEST REPORT",
    )

    cli.main(
        [
            "backtest",
            "--file",
            "market.csv",
            "--strategy",
            "breakout",
            "--lookback",
            "20",
        ]
    )

    captured = capsys.readouterr()

    assert captured.out.strip() == ("BACKTEST REPORT")
