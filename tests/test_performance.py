from analytics.performance import (
    calculate_average_trade,
    calculate_gross_loss,
    calculate_gross_profit,
    calculate_profit_factor,
    calculate_total_pnl,
    calculate_win_rate,
)


def test_calculate_total_pnl_returns_zero_for_empty_trades():
    trades = []

    result = calculate_total_pnl(trades)

    assert result == 0.0


def test_calculate_total_pnl_sums_trade_results():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": -40.0},
        {"pnl_points": 25.0},
    ]

    result = calculate_total_pnl(trades)

    assert result == 85.0


def test_calculate_total_pnl_preserves_decimal_precision():
    trades = [
        {"pnl_points": 100.555},
        {"pnl_points": 20.0},
    ]

    result = calculate_total_pnl(trades)

    assert result == 120.555


def test_calculate_average_trade_returns_zero_for_empty_trades():
    trades = []

    result = calculate_average_trade(trades)

    assert result == 0.0


def test_calculate_average_trade_returns_average_pnl_per_trade():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": -40.0},
        {"pnl_points": 30.0},
    ]

    result = calculate_average_trade(trades)

    assert result == 30.0


def test_calculate_win_rate_returns_zero_for_empty_trades():
    trades = []

    result = calculate_win_rate(trades)

    assert result == 0.0


def test_calculate_win_rate_returns_percentage_of_winning_trades():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": -50.0},
        {"pnl_points": 30.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_win_rate(trades)

    assert result == 50.0


def test_calculate_gross_profit_sums_only_winning_trades():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": -50.0},
        {"pnl_points": 30.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_gross_profit(trades)

    assert result == 130.0


def test_calculate_gross_profit_returns_zero_without_winning_trades():
    trades = [
        {"pnl_points": -50.0},
        {"pnl_points": -20.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_gross_profit(trades)

    assert result == 0.0


def test_calculate_gross_loss_sums_only_losing_trades():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": -50.0},
        {"pnl_points": 30.0},
        {"pnl_points": -20.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_gross_loss(trades)

    assert result == -70.0


def test_calculate_gross_loss_returns_zero_without_losing_trades():
    trades = [
        {"pnl_points": 100.0},
        {"pnl_points": 30.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_gross_loss(trades)

    assert result == 0.0


def test_calculate_profit_factor_returns_ratio_between_profit_and_loss():
    trades = [
        {"pnl_points": 600.0},
        {"pnl_points": -200.0},
        {"pnl_points": -100.0},
    ]

    result = calculate_profit_factor(trades)

    assert result == 2.0


def test_calculate_profit_factor_returns_zero_for_only_losses():
    trades = [
        {"pnl_points": -200.0},
        {"pnl_points": -100.0},
    ]

    result = calculate_profit_factor(trades)

    assert result == 0.0


def test_calculate_profit_factor_returns_infinity_for_only_wins():
    trades = [
        {"pnl_points": 200.0},
        {"pnl_points": 100.0},
    ]

    result = calculate_profit_factor(trades)

    assert result == float("inf")


def test_calculate_profit_factor_returns_none_for_only_even_trades():
    trades = [
        {"pnl_points": 0.0},
        {"pnl_points": 0.0},
    ]

    result = calculate_profit_factor(trades)

    assert result is None


def test_calculate_profit_factor_returns_none_for_empty_trades():
    trades = []

    result = calculate_profit_factor(trades)

    assert result is None
