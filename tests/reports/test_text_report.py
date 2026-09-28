from reports.text_report import create_text_report


def test_create_text_report_includes_strategy_information():
    summary = {}

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "WINQuantLab - Backtest Report" in report
    assert "Strategy: Breakout" in report
    assert "Parameters: lookback=20" in report


def test_create_text_report_includes_period_summary():
    summary = {
        "sessions": 250,
        "sessions_with_trades": 180,
        "sessions_without_trades": 70,
        "trades": 430,
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "Period analyzed" in report
    assert "Sessions: 250" in report
    assert "Sessions with trades: 180" in report
    assert "Sessions without trades: 70" in report
    assert "Trades: 430" in report


def test_create_text_report_includes_results():
    summary = {
        "wins": 210,
        "losses": 200,
        "evens": 20,
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "Results" in report
    assert "Wins: 210" in report
    assert "Losses: 200" in report
    assert "Even: 20" in report


def test_create_text_report_includes_mfe_statistics():
    summary = {
        "average_mfe_points": 315.4,
        "median_mfe_points": 260.0,
        "mfe_p25": 150.0,
        "mfe_p50": 260.0,
        "mfe_p75": 420.0,
        "mfe_min": 0.0,
        "mfe_max": 1350.0,
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "General excursion" in report
    assert "MFE average: 315.40 pts" in report
    assert "MFE median: 260.00 pts" in report
    assert (
        "MFE P25/P50/P75: "
        "150.00 / 260.00 / 420.00 pts"
        in report
    )
    assert "MFE min/max: 0.00 / 1350.00 pts" in report


def test_create_text_report_includes_mae_statistics():
    summary = {
        "average_mae_points": -185.7,
        "median_mae_points": -140.0,
        "mae_p25": -260.0,
        "mae_p50": -140.0,
        "mae_p75": -70.0,
        "mae_min": -1100.0,
        "mae_max": 0.0,
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "General excursion" in report
    assert "MAE average: -185.70 pts" in report
    assert "MAE median: -140.00 pts" in report
    assert (
        "MAE P25/P50/P75: "
        "-260.00 / -140.00 / -70.00 pts"
        in report
    )
    assert "MAE min/max: -1100.00 / 0.00 pts" in report


def test_create_text_report_includes_duration_statistics():
    summary = {
        "average_duration_candles": 18.4,
        "median_duration_candles": 14.0,
        "duration_p25": 7.0,
        "duration_p50": 14.0,
        "duration_p75": 25.0,
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "Duration" in report
    assert "Average: 18.40 candles" in report
    assert "Median: 14.00 candles" in report
    assert (
        "P25/P50/P75: "
        "7.00 / 14.00 / 25.00 candles"
        in report
    )


def test_create_text_report_includes_outcome_statistics():
    summary = {
        "outcome_trades": {
            "win": 210,
            "loss": 200,
            "even": 20,
        },
        "outcome_average_mfe": {
            "win": 420.5,
            "loss": 160.8,
            "even": 225.0,
        },
        "outcome_average_mae": {
            "win": -95.2,
            "loss": -285.7,
            "even": -140.0,
        },
        "outcome_average_duration": {
            "win": 16.3,
            "loss": 21.8,
            "even": 12.5,
        },
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "By outcome" in report

    assert "WIN" in report
    assert "LOSS" in report
    assert "EVEN" in report

    assert "Trades" in report
    assert "210" in report
    assert "200" in report
    assert "20" in report

    assert "MFE average" in report
    assert "420.50" in report
    assert "160.80" in report
    assert "225.00" in report

    assert "MAE average" in report
    assert "-95.20" in report
    assert "-285.70" in report
    assert "-140.00" in report

    assert "Duration average" in report
    assert "16.30" in report
    assert "21.80" in report
    assert "12.50" in report


def test_create_text_report_formats_decimal_values():
    summary = {
        "average_mfe_points": 640.1581546391752,
        "outcome_average_mfe": {
            "win": 1049.3084862385338,
            "loss": 302.40554079696375,
            "even": 583.8842857142778,
        },
    }

    report = create_text_report(
        summary,
        strategy_name="Breakout",
        strategy_parameters={
            "lookback": 20,
        },
    )

    assert "MFE average: 640.16 pts" in report

    assert "1049.31" in report
    assert "302.41" in report
    assert "583.88" in report
