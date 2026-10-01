"""Performance metrics for backtesting results."""


def calculate_total_pnl(trades: list[dict]) -> float:
    """Calculate the total PnL from a collection of trades."""
    return sum((trade["pnl"] for trade in trades), start=0.0)


def calculate_average_trade(trades: list[dict]) -> float:
    """Calculate the average PnL per trade."""
    if not trades:
        return 0.0

    total_pnl = calculate_total_pnl(trades)

    return total_pnl / len(trades)


def calculate_win_rate(trades: list[dict]) -> float:
    """Calculate the percentage of winning trades."""
    if not trades:
        return 0.0

    winning_trades = sum(1 for trade in trades if trade["pnl"] > 0)

    return winning_trades / len(trades) * 100


def calculate_gross_profit(trades: list[dict]) -> float:
    """Calculate the sum of PnL from winning trades."""
    return sum(
        (trade["pnl"] for trade in trades if trade["pnl"] > 0),
        start=0.0,
    )


def calculate_gross_loss(trades: list[dict]) -> float:
    """Calculate the sum of PnL from losing trades."""
    return sum(
        (trade["pnl"] for trade in trades if trade["pnl"] < 0),
        start=0.0,
    )


def calculate_profit_factor(trades: list[dict]) -> float | None:
    """Calculate the ratio between gross profit and gross loss."""
    gross_profit = calculate_gross_profit(trades)
    gross_loss = calculate_gross_loss(trades)

    if gross_profit == 0.0 and gross_loss == 0.0:
        return None

    if gross_loss == 0.0:
        return float("inf")

    return gross_profit / abs(gross_loss)
