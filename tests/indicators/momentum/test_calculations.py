"""Testes dos cálculos internos dos indicadores de momentum."""

from __future__ import annotations

import pandas as pd

from indicators.momentum.calculations import (
    calculate_previous_values,
    calculate_price_changes,
    separate_gains_and_losses,
)


def test_calculate_price_changes() -> None:
    """Verifica a diferença entre preços consecutivos."""
    series = pd.Series(
        [100.0, 102.0, 101.0, 104.0],
    )

    result = calculate_price_changes(series)

    expected = pd.Series(
        [float("nan"), 2.0, -1.0, 3.0],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_separate_gains_and_losses() -> None:
    """Verifica a separação entre ganhos e perdas."""
    changes = pd.Series(
        [float("nan"), 2.0, -1.0, 3.0, -4.0, 0.0],
    )

    gains, losses = separate_gains_and_losses(changes)

    expected_gains = pd.Series(
        [float("nan"), 2.0, 0.0, 3.0, 0.0, 0.0],
    )

    expected_losses = pd.Series(
        [float("nan"), 0.0, 1.0, 0.0, 4.0, 0.0],
    )

    pd.testing.assert_series_equal(
        gains,
        expected_gains,
    )

    pd.testing.assert_series_equal(
        losses,
        expected_losses,
    )


def test_calculate_previous_values() -> None:
    """Verifica o deslocamento da série."""
    series = pd.Series(
        [100.0, 101.0, 102.0, 103.0],
    )

    result = calculate_previous_values(
        series,
        period=2,
    )

    expected = pd.Series(
        [
            float("nan"),
            float("nan"),
            100.0,
            101.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )
