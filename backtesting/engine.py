"""Backtesting engine."""

from __future__ import annotations

import pandas as pd


def _calculate_pnl_points(
    direction: str,
    entry_price: float,
    exit_price: float,
) -> float:
    """Calculate trade result in price points."""
    if direction == "long":
        return exit_price - entry_price

    return entry_price - exit_price


def _close_position(
    position: dict,
    exit_index: int,
    exit_price: float,
    df: pd.DataFrame,
) -> dict:
    """Close an open position and calculate its result."""
    position["exit_index"] = exit_index
    position["exit_price"] = exit_price

    if isinstance(df.index, pd.DatetimeIndex):
        position["exit_time"] = df.index[exit_index]

    position["pnl_points"] = _calculate_pnl_points(
        direction=position["direction"],
        entry_price=position["entry_price"],
        exit_price=exit_price,
    )

    return position


def backtest(df: pd.DataFrame) -> list:
    """
    Execute a backtest using strategy signals.

    Parameters
    ----------
    df:
        DataFrame containing market data and strategy signals.

    Returns
    -------
    list
        Completed trades generated during the backtest.

    Raises
    ------
    ValueError
        If a required column is missing.
        If signal contains a value other than -1, 0, or 1.
    """
    required_columns = (
        "open",
        "close",
        "signal",
    )

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"The column '{column}' was not found"
            )

    valid_signals = {-1, 0, 1}

    if not df["signal"].isin(valid_signals).all():
        raise ValueError(
            "signal must contain only -1, 0, or 1"
        )

    trades = []
    position = None

    for index in range(len(df) - 1):
        signal = df["signal"].iloc[index]
        next_index = index + 1

        if position is None and signal == 1:
            position = {
                "direction": "long",
                "entry_index": next_index,
                "entry_price": df["open"].iloc[next_index],
                "quantity": 1,
            }

            if isinstance(df.index, pd.DatetimeIndex):
                position["entry_time"] = df.index[next_index]

        elif position is None and signal == -1:
            position = {
                "direction": "short",
                "entry_index": next_index,
                "entry_price": df["open"].iloc[next_index],
                "quantity": 1,
            }

            if isinstance(df.index, pd.DatetimeIndex):
                position["entry_time"] = df.index[next_index]

        elif (
            position is not None
            and position["direction"] == "long"
            and signal == -1
        ):
            trade = _close_position(
                position=position,
                exit_index=next_index,
                exit_price=df["open"].iloc[next_index],
                df=df,
            )

            trades.append(trade)
            position = None

        elif (
            position is not None
            and position["direction"] == "short"
            and signal == 1
        ):
            trade = _close_position(
                position=position,
                exit_index=next_index,
                exit_price=df["open"].iloc[next_index],
                df=df,
            )

            trades.append(trade)
            position = None

    if position is not None:
        trade = _close_position(
            position=position,
            exit_index=len(df) - 1,
            exit_price=df["close"].iloc[-1],
            df=df,
        )

        trades.append(trade)

    return trades
