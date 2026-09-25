"""
Pipeline de execução de backtests multi-sessão.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from backtesting.engine import backtest


def _validate_datetime_column(
    market_data: pd.DataFrame,
) -> None:
    """
    Valida a presença da coluna datetime.
    """

    if "datetime" not in market_data.columns:
        raise ValueError(
            "The column 'datetime' was not found"
        )


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
        session_data = session_data.sort_values(
            by="datetime"
        ).reset_index(drop=True)

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

    longs = sum(
        trade["direction"] == "long"
        for trade in trades
    )

    shorts = sum(
        trade["direction"] == "short"
        for trade in trades
    )

    wins = sum(
        trade["outcome"] == "win"
        for trade in trades
    )

    losses = sum(
        trade["outcome"] == "loss"
        for trade in trades
    )

    evens = sum(
        trade["outcome"] == "even"
        for trade in trades
    )

    pnl_points = sum(
        trade["pnl_points"]
        for trade in trades
    )

    mfe_points = sum(
        trade["mfe_points"]
        for trade in trades
    )

    mae_points = sum(
        trade["mae_points"]
        for trade in trades
    )

    if trades:
        average_mfe_points = (
            mfe_points / len(trades)
        )
        average_mae_points = (
            mae_points / len(trades)
        )
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
        strategy_data = strategy(
            session["data"]
        )

        trades = backtest(
            strategy_data
        )

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
