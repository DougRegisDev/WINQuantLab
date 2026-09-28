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

    return ", ".join(f"{name}={value}" for name, value in strategy_parameters.items())


def _format_number(
    value: int | float,
) -> str:
    """
    Formata valores numéricos com duas casas decimais.
    """

    return f"{value:.2f}"


def _format_outcome_row(
    label: str,
    values: dict,
    decimal: bool = True,
) -> str:
    """
    Formata uma linha da tabela por resultado.
    """

    if decimal:
        win = _format_number(values.get("win", 0.0))
        loss = _format_number(values.get("loss", 0.0))
        even = _format_number(values.get("even", 0.0))
    else:
        win = str(values.get("win", 0))
        loss = str(values.get("loss", 0))
        even = str(values.get("even", 0))

    return f"{label:<18}{win:>12}{loss:>12}{even:>12}"


def create_text_report(
    summary: dict,
    strategy_name: str,
    strategy_parameters: dict,
) -> str:
    """
    Cria um relatório textual de backtesting.
    """

    parameters = _format_parameters(strategy_parameters)

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
        (f"Sessions with trades: {summary.get('sessions_with_trades', 0)}"),
        (f"Sessions without trades: {summary.get('sessions_without_trades', 0)}"),
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
        (f"MFE average: {_format_number(summary.get('average_mfe_points', 0.0))} pts"),
        (f"MFE median: {_format_number(summary.get('median_mfe_points', 0.0))} pts"),
        (
            "MFE P25/P50/P75: "
            f"{_format_number(summary.get('mfe_p25', 0.0))} / "
            f"{_format_number(summary.get('mfe_p50', 0.0))} / "
            f"{_format_number(summary.get('mfe_p75', 0.0))} pts"
        ),
        (
            "MFE min/max: "
            f"{_format_number(summary.get('mfe_min', 0.0))} / "
            f"{_format_number(summary.get('mfe_max', 0.0))} pts"
        ),
        "",
        (f"MAE average: {_format_number(summary.get('average_mae_points', 0.0))} pts"),
        (f"MAE median: {_format_number(summary.get('median_mae_points', 0.0))} pts"),
        (
            "MAE P25/P50/P75: "
            f"{_format_number(summary.get('mae_p25', 0.0))} / "
            f"{_format_number(summary.get('mae_p50', 0.0))} / "
            f"{_format_number(summary.get('mae_p75', 0.0))} pts"
        ),
        (
            "MAE min/max: "
            f"{_format_number(summary.get('mae_min', 0.0))} / "
            f"{_format_number(summary.get('mae_max', 0.0))} pts"
        ),
        "",
        "Duration",
        "--------",
        (
            "Average: "
            f"{_format_number(summary.get('average_duration_candles', 0.0))} "
            "candles"
        ),
        (
            "Median: "
            f"{_format_number(summary.get('median_duration_candles', 0.0))} "
            "candles"
        ),
        (
            "P25/P50/P75: "
            f"{_format_number(summary.get('duration_p25', 0.0))} / "
            f"{_format_number(summary.get('duration_p50', 0.0))} / "
            f"{_format_number(summary.get('duration_p75', 0.0))} candles"
        ),
        "",
        "By outcome",
        "----------",
        (f"{'':<18}{'WIN':>12}{'LOSS':>12}{'EVEN':>12}"),
        _format_outcome_row(
            "Trades",
            summary.get("outcome_trades", {}),
            decimal=False,
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
