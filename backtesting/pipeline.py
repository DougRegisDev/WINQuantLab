"""
Pipeline de execução de backtests multi-sessão.
"""

from __future__ import annotations

from collections.abc import Callable
from statistics import median

import pandas as pd

from backtesting.engine import backtest

OUTCOMES = ("win", "loss", "even")


def _validate_datetime_column(
    market_data: pd.DataFrame,
) -> None:
    """
    Valida a presença da coluna datetime.
    """

    if "datetime" not in market_data.columns:
        raise ValueError("The column 'datetime' was not found")


def split_sessions(
    market_data: pd.DataFrame,
) -> list[dict]:
    """
    Separa dados de mercado em sessões independentes por data.
    """

    _validate_datetime_column(market_data)

    sessions = []

    for session_date, session_data in market_data.groupby(
        market_data["datetime"].dt.date,
        sort=True,
    ):
        session_data = session_data.sort_values(by="datetime").reset_index(drop=True)

        sessions.append(
            {
                "session": session_date,
                "data": session_data,
            }
        )

    return sessions


def _create_session_summary(
    session_date,
    session_data: pd.DataFrame,
    trades: list[dict],
) -> dict:
    """
    Cria o resumo de uma sessão.
    """

    longs = sum(trade["direction"] == "long" for trade in trades)

    shorts = sum(trade["direction"] == "short" for trade in trades)

    wins = sum(trade["outcome"] == "win" for trade in trades)

    losses = sum(trade["outcome"] == "loss" for trade in trades)

    evens = sum(trade["outcome"] == "even" for trade in trades)

    pnl_points = sum(trade["pnl_points"] for trade in trades)

    mfe_points = sum(trade["mfe_points"] for trade in trades)

    mae_points = sum(trade["mae_points"] for trade in trades)

    if trades:
        average_mfe_points = mfe_points / len(trades)
        average_mae_points = mae_points / len(trades)
    else:
        average_mfe_points = 0.0
        average_mae_points = 0.0

    return {
        "session": session_date,
        "candles": len(session_data),
        "trades": len(trades),
        "longs": longs,
        "shorts": shorts,
        "wins": wins,
        "losses": losses,
        "evens": evens,
        "pnl_points": pnl_points,
        "mfe_points": mfe_points,
        "mae_points": mae_points,
        "average_mfe_points": average_mfe_points,
        "average_mae_points": average_mae_points,
    }


def _collect_period_trades(
    session_results: list[dict],
) -> list[dict]:
    """
    Consolida os trades de todas as sessões.
    """

    return [trade for result in session_results for trade in result.get("trades", [])]


def _calculate_distribution(
    values: list[float | int],
) -> dict:
    """
    Calcula estatísticas descritivas de uma distribuição.
    """

    if not values:
        return {
            "average": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "p25": 0.0,
            "p50": 0.0,
            "p75": 0.0,
        }

    series = pd.Series(
        values,
        dtype=float,
    )

    return {
        "average": sum(values) / len(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "p25": series.quantile(0.25),
        "p50": series.quantile(0.50),
        "p75": series.quantile(0.75),
    }


def _calculate_outcome_average(
    period_trades: list[dict],
    outcome: str,
    field: str,
) -> float:
    """
    Calcula a média de um campo para um resultado específico.
    """

    values = [
        trade[field]
        for trade in period_trades
        if (trade.get("outcome") == outcome and field in trade)
    ]

    if not values:
        return 0.0

    return sum(values) / len(values)


def _calculate_outcome_analytics(
    period_trades: list[dict],
) -> dict:
    """
    Calcula métricas segmentadas pelo resultado dos trades.
    """

    outcome_trades = {
        outcome: sum(trade.get("outcome") == outcome for trade in period_trades)
        for outcome in OUTCOMES
    }

    outcome_average_mfe = {
        outcome: _calculate_outcome_average(
            period_trades,
            outcome,
            "mfe_points",
        )
        for outcome in OUTCOMES
    }

    outcome_average_mae = {
        outcome: _calculate_outcome_average(
            period_trades,
            outcome,
            "mae_points",
        )
        for outcome in OUTCOMES
    }

    outcome_average_duration = {
        outcome: _calculate_outcome_average(
            period_trades,
            outcome,
            "duration_candles",
        )
        for outcome in OUTCOMES
    }

    return {
        "outcome_trades": outcome_trades,
        "outcome_average_mfe": outcome_average_mfe,
        "outcome_average_mae": outcome_average_mae,
        "outcome_average_duration": outcome_average_duration,
    }


def create_period_summary(
    session_results: list[dict],
) -> dict:
    """
    Consolida informações de múltiplas sessões.
    """

    sessions = len(session_results)

    sessions_with_trades = sum(
        result["summary"]["trades"] > 0 for result in session_results
    )

    sessions_without_trades = sessions - sessions_with_trades

    candles = sum(result["summary"]["candles"] for result in session_results)

    trades = sum(result["summary"]["trades"] for result in session_results)

    longs = sum(result["summary"].get("longs", 0) for result in session_results)

    shorts = sum(result["summary"].get("shorts", 0) for result in session_results)

    wins = sum(result["summary"].get("wins", 0) for result in session_results)

    losses = sum(result["summary"].get("losses", 0) for result in session_results)

    evens = sum(result["summary"].get("evens", 0) for result in session_results)

    pnl_points = sum(
        result["summary"].get("pnl_points", 0.0) for result in session_results
    )

    period_trades = _collect_period_trades(session_results)

    mfe_values = [trade["mfe_points"] for trade in period_trades]

    mae_values = [trade["mae_points"] for trade in period_trades]

    duration_values = [
        trade["duration_candles"]
        for trade in period_trades
        if "duration_candles" in trade
    ]

    mfe_statistics = _calculate_distribution(mfe_values)

    mae_statistics = _calculate_distribution(mae_values)

    duration_statistics = _calculate_distribution(duration_values)

    outcome_analytics = _calculate_outcome_analytics(period_trades)

    return {
        "sessions": sessions,
        "sessions_with_trades": sessions_with_trades,
        "sessions_without_trades": sessions_without_trades,
        "candles": candles,
        "trades": trades,
        "longs": longs,
        "shorts": shorts,
        "wins": wins,
        "losses": losses,
        "evens": evens,
        "pnl_points": pnl_points,
        **outcome_analytics,
        "average_mfe_points": mfe_statistics["average"],
        "average_mae_points": mae_statistics["average"],
        "median_mfe_points": mfe_statistics["median"],
        "median_mae_points": mae_statistics["median"],
        "mfe_min": mfe_statistics["min"],
        "mfe_max": mfe_statistics["max"],
        "mae_min": mae_statistics["min"],
        "mae_max": mae_statistics["max"],
        "average_duration_candles": duration_statistics["average"],
        "median_duration_candles": duration_statistics["median"],
        "mfe_p25": mfe_statistics["p25"],
        "mfe_p50": mfe_statistics["p50"],
        "mfe_p75": mfe_statistics["p75"],
        "mae_p25": mae_statistics["p25"],
        "mae_p50": mae_statistics["p50"],
        "mae_p75": mae_statistics["p75"],
        "duration_p25": duration_statistics["p25"],
        "duration_p50": duration_statistics["p50"],
        "duration_p75": duration_statistics["p75"],
    }


def run_sessions(
    market_data: pd.DataFrame,
    strategy: Callable[[pd.DataFrame], pd.DataFrame],
) -> list[dict]:
    """
    Executa estratégia e backtesting independentemente por sessão.
    """

    sessions = split_sessions(market_data)

    results = []

    for session in sessions:
        strategy_data = strategy(session["data"])

        trades = backtest(strategy_data)

        for trade in trades:
            trade["session"] = session["session"]

        summary = _create_session_summary(
            session["session"],
            strategy_data,
            trades,
        )

        results.append(
            {
                "session": session["session"],
                "data": strategy_data,
                "trades": trades,
                "summary": summary,
            }
        )

    return results
