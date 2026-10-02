import pandas as pd

from analytics.performance import (
    calculate_average_trade,
    calculate_total_pnl,
    calculate_win_rate,
)
from backtesting.engine import backtest


def test_backtest_trades_are_compatible_with_performance_analytics():
    market_data = pd.DataFrame(
        {
            "open": [95.0, 100.0, 110.0],
            "high": [100.0, 108.0, 115.0],
            "low": [90.0, 98.0, 108.0],
            "close": [98.0, 105.0, 112.0],
            "signal": [1, -1, 0],
        }
    )

    trades = backtest(market_data)

    assert len(trades) == 1
    assert trades[0]["pnl_points"] == 10.0
    assert calculate_total_pnl(trades) == 10.0
    assert calculate_average_trade(trades) == 10.0
    assert calculate_win_rate(trades) == 100.0
