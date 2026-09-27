"""
Relatórios textuais de backtesting.
"""

from __future__ import annotations


def _format_parameters(
    strategy_parameters: dict,
) -> str:
    """
    Formata os parâmetros utilizados pela estratégia.
    """

    return ", ".join(
        f"{name}={value}"
        for name, value in strategy_parameters.items()
    )


def _format_outcome_row(
    label: str,
    values: dict,
) -> str:
    """
    Formata uma linha da tabela por resultado.
    """

    return (
        f"{label:<18}"
        f"{values.get('win', 0):>10}"
        f"{values.get('loss', 0):>10}"
        f"{values.get('even', 0):>10}"
    )


def create_text_report(
    summary: dict,
    strategy_name: str,
    strategy_parameters: dict,
) -> str:
    """
    Cria um relatório textual de backtesting.
    """

    parameters = _format_parameters(
        strategy_parameters
    )

    lines = [
        "WINQuantLab - Backtest Report",
        "=============================",
        "",
        f"Strategy: {strategy_name}",
        f"Parameters: {parameters}",
        "",
        "Period analyzed",
        "---------------",
        f"Sessions: {summary.get('sessions', 0)}",
        (
            "Sessions with trades: "
            f"{summary.get('sessions_with_trades', 0)}"
        ),
        (
            "Sessions without trades: "
            f"{summary.get('sessions_without_trades', 0)}"
        ),
        f"Trades: {summary.get('trades', 0)}",
        "",
        "Results",
        "-------",
        f"Wins: {summary.get('wins', 0)}",
        f"Losses: {summary.get('losses', 0)}",
        f"Even: {summary.get('evens', 0)}",
        "",
        "General excursion",
        "-----------------",
        (
            "MFE average: "
            f"{summary.get('average_mfe_points', 0.0)} pts"
        ),
        (
            "MFE median: "
            f"{summary.get('median_mfe_points', 0.0)} pts"
        ),
        (
            "MFE P25/P50/P75: "
            f"{summary.get('mfe_p25', 0.0)} / "
            f"{summary.get('mfe_p50', 0.0)} / "
            f"{summary.get('mfe_p75', 0.0)} pts"
        ),
        (
            "MFE min/max: "
            f"{summary.get('mfe_min', 0.0)} / "
            f"{summary.get('mfe_max', 0.0)} pts"
        ),
        "",
        (
            "MAE average: "
            f"{summary.get('average_mae_points', 0.0)} pts"
        ),
        (
            "MAE median: "
            f"{summary.get('median_mae_points', 0.0)} pts"
        ),
        (
            "MAE P25/P50/P75: "
            f"{summary.get('mae_p25', 0.0)} / "
            f"{summary.get('mae_p50', 0.0)} / "
            f"{summary.get('mae_p75', 0.0)} pts"
        ),
        (
            "MAE min/max: "
            f"{summary.get('mae_min', 0.0)} / "
            f"{summary.get('mae_max', 0.0)} pts"
        ),
        "",
        "Duration",
        "--------",
        (
            "Average: "
            f"{summary.get('average_duration_candles', 0.0)} "
            "candles"
        ),
        (
            "Median: "
            f"{summary.get('median_duration_candles', 0.0)} "
            "candles"
        ),
        (
            "P25/P50/P75: "
            f"{summary.get('duration_p25', 0.0)} / "
            f"{summary.get('duration_p50', 0.0)} / "
            f"{summary.get('duration_p75', 0.0)} candles"
        ),
        "",
        "By outcome",
        "----------",
        (
            f"{'':<18}"
            f"{'WIN':>10}"
            f"{'LOSS':>10}"
            f"{'EVEN':>10}"
        ),
        _format_outcome_row(
            "Trades",
            summary.get("outcome_trades", {}),
        ),
        _format_outcome_row(
            "MFE average",
            summary.get("outcome_average_mfe", {}),
        ),
        _format_outcome_row(
            "MAE average",
            summary.get("outcome_average_mae", {}),
        ),
        _format_outcome_row(
            "Duration average",
            summary.get(
                "outcome_average_duration",
                {},
            ),
        ),
    ]

    return "\n".join(lines)
