"""
Interface de linha de comando do WINQuantLab.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable

import pandas as pd

from backtesting.pipeline import (
    create_period_summary,
    run_sessions,
)
from data.loader import load_data
from data.normalizer import normalize
from reports.text_report import create_text_report
from strategies.breakout import breakout
from strategies.moving_average_crossover import (
    moving_average_crossover,
)

STRATEGIES: dict[
    str,
    dict[
        str,
        Callable[..., pd.DataFrame] | tuple[str, ...],
    ],
] = {
    "breakout": {
        "function": breakout,
        "parameters": (
            "lookback",
        ),
    },
    "moving_average_crossover": {
        "function": moving_average_crossover,
        "parameters": (
            "fast_period",
            "slow_period",
        ),
    },
}


def positive_integer(value: str) -> int:
    """
    Converte um argumento para inteiro positivo.
    """

    integer_value = int(value)

    if integer_value <= 0:
        raise argparse.ArgumentTypeError(
            "value must be greater than zero"
        )

    return integer_value


def get_strategy_parameters(
    args: argparse.Namespace,
) -> dict[str, int]:
    """
    Retorna apenas os parâmetros da estratégia escolhida.
    """

    strategy_config = STRATEGIES[
        args.strategy
    ]

    parameter_names = strategy_config[
        "parameters"
    ]

    return {
        parameter_name: getattr(
            args,
            parameter_name,
        )
        for parameter_name in parameter_names
    }


def run_strategy(
    market_data: pd.DataFrame,
    strategy_name: str,
    **parameters: int,
) -> pd.DataFrame:
    """
    Executa uma estratégia registrada.
    """

    try:
        strategy_config = STRATEGIES[
            strategy_name
        ]
    except KeyError as error:
        raise ValueError(
            f"Strategy not supported: {strategy_name}"
        ) from error

    strategy = strategy_config[
        "function"
    ]

    return strategy(
        market_data,
        **parameters,
    )


def run_backtest_command(
    args: argparse.Namespace,
) -> str:
    """
    Executa o fluxo completo de backtesting.
    """

    market_data = load_data(
        args.file,
        header=None,
    )

    market_data = normalize(
        market_data,
        source="profit",
    )

    strategy_parameters = (
        get_strategy_parameters(args)
    )

    def strategy(
        session_data: pd.DataFrame,
    ) -> pd.DataFrame:
        return run_strategy(
            session_data,
            strategy_name=args.strategy,
            **strategy_parameters,
        )

    session_results = run_sessions(
        market_data,
        strategy,
    )

    summary = create_period_summary(
        session_results
    )

    return create_text_report(
        summary,
        strategy_name=args.strategy,
        strategy_parameters=(
            strategy_parameters
        ),
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Cria o parser principal da CLI.
    """

    parser = argparse.ArgumentParser(
        prog="winquantlab",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    backtest_parser = subparsers.add_parser(
        "backtest",
    )

    backtest_parser.add_argument(
        "--file",
        required=True,
    )

    backtest_parser.add_argument(
        "--strategy",
        required=True,
        choices=sorted(STRATEGIES),
    )

    backtest_parser.add_argument(
        "--lookback",
        type=positive_integer,
        default=20,
    )

    backtest_parser.add_argument(
        "--fast-period",
        type=positive_integer,
        default=9,
    )

    backtest_parser.add_argument(
        "--slow-period",
        type=positive_integer,
        default=21,
    )

    return parser


def main(
    argv: list[str] | None = None,
) -> None:
    """
    Executa a interface de linha de comando.
    """

    parser = create_parser()

    args = parser.parse_args(
        argv
    )

    if args.command == "backtest":
        report = run_backtest_command(
            args
        )

        print(report)


if __name__ == "__main__":
    main()
