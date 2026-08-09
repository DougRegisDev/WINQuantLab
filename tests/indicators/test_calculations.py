"""Testes dos cálculos compartilhados entre indicadores."""

from __future__ import annotations

import pandas as pd

from indicators.calculations import (
    calculate_average_true_range,
    calculate_directional_index,
    calculate_directional_movement,
    calculate_ema,
    calculate_rolling_max,
    calculate_rolling_min,
    calculate_true_range,
    calculate_wilder_average,
)


def test_calculate_ema() -> None:
    """Compara a EMA compartilhada com a referência do Pandas."""
    period = 3

    series = pd.Series(
        [100.0, 102.0, 101.0, 104.0, 103.0],
    )

    result = calculate_ema(
        series,
        period,
    )

    expected = (
        series
        .ewm(
            span=period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_ema_initial_values_are_nan() -> None:
    """Verifica os valores iniciais ausentes da EMA."""
    period = 3

    series = pd.Series(
        [100.0, 102.0, 101.0, 104.0, 103.0],
    )

    result = calculate_ema(
        series,
        period,
    )

    assert result.iloc[: period - 1].isna().all()
    assert pd.notna(result.iloc[period - 1])


def test_calculate_rolling_max() -> None:
    """Verifica o maior valor dentro de uma janela móvel."""
    series = pd.Series(
        [10.0, 12.0, 11.0, 15.0, 13.0],
    )

    result = calculate_rolling_max(
        series,
        period=3,
    )

    expected = pd.Series(
        [
            float("nan"),
            float("nan"),
            12.0,
            15.0,
            15.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_rolling_min() -> None:
    """Verifica o menor valor dentro de uma janela móvel."""
    series = pd.Series(
        [10.0, 12.0, 11.0, 15.0, 13.0],
    )

    result = calculate_rolling_min(
        series,
        period=3,
    )

    expected = pd.Series(
        [
            float("nan"),
            float("nan"),
            10.0,
            11.0,
            11.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_wilder_average() -> None:
    """Compara a suavização de Wilder com a referência do Pandas."""
    period = 3

    series = pd.Series(
        [1.0, 2.0, 3.0, 4.0, 5.0],
    )

    result = calculate_wilder_average(
        series,
        period,
    )

    expected = (
        series
        .ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period,
        )
        .mean()
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_wilder_average_initial_values_are_nan() -> None:
    """Verifica os valores iniciais ausentes da suavização de Wilder."""
    period = 3

    series = pd.Series(
        [1.0, 2.0, 3.0, 4.0, 5.0],
    )

    result = calculate_wilder_average(
        series,
        period,
    )

    assert result.iloc[: period - 1].isna().all()
    assert pd.notna(result.iloc[period - 1])


def test_calculate_true_range() -> None:
    """Verifica o cálculo do True Range."""
    high = pd.Series(
        [10.0, 12.0, 15.0],
    )

    low = pd.Series(
        [8.0, 10.0, 11.0],
    )

    close = pd.Series(
        [9.0, 11.0, 14.0],
    )

    result = calculate_true_range(
        high,
        low,
        close,
    )

    expected = pd.Series(
        [
            2.0,
            3.0,
            4.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_true_range_gap_up() -> None:
    """Verifica o True Range quando há gap de alta."""
    high = pd.Series(
        [10.0, 15.0],
    )

    low = pd.Series(
        [8.0, 14.0],
    )

    close = pd.Series(
        [9.0, 14.0],
    )

    result = calculate_true_range(
        high,
        low,
        close,
    )

    expected = pd.Series(
        [
            2.0,
            6.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_true_range_gap_down() -> None:
    """Verifica o True Range quando há gap de baixa."""
    high = pd.Series(
        [10.0, 6.0],
    )

    low = pd.Series(
        [8.0, 5.0],
    )

    close = pd.Series(
        [9.0, 5.5],
    )

    result = calculate_true_range(
        high,
        low,
        close,
    )

    expected = pd.Series(
        [
            2.0,
            4.0,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_average_true_range() -> None:
    """Verifica o cálculo do Average True Range."""
    period = 3

    true_range = pd.Series(
        [2.0, 3.0, 4.0, 5.0, 6.0],
    )

    result = calculate_average_true_range(
        true_range,
        period,
    )

    expected = calculate_wilder_average(
        true_range,
        period,
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )


def test_calculate_directional_movement_positive() -> None:
    """Verifica o cálculo do movimento direcional positivo."""
    high = pd.Series([10.0, 13.0])
    low = pd.Series([8.0, 9.0])

    positive_dm, negative_dm = calculate_directional_movement(
        high=high,
        low=low,
    )

    expected_positive = pd.Series(
        [0.0, 3.0],
    )

    expected_negative = pd.Series(
        [0.0, 0.0],
    )

    pd.testing.assert_series_equal(
        positive_dm,
        expected_positive,
    )

    pd.testing.assert_series_equal(
        negative_dm,
        expected_negative,
    )


def test_calculate_directional_movement_negative() -> None:
    """Verifica o cálculo do movimento direcional negativo."""
    high = pd.Series([10.0, 11.0])
    low = pd.Series([8.0, 5.0])

    positive_dm, negative_dm = calculate_directional_movement(
        high=high,
        low=low,
    )

    expected_positive = pd.Series(
        [0.0, 0.0],
    )

    expected_negative = pd.Series(
        [0.0, 3.0],
    )

    pd.testing.assert_series_equal(
        positive_dm,
        expected_positive,
    )

    pd.testing.assert_series_equal(
        negative_dm,
        expected_negative,
    )


def test_calculate_directional_movement_tie() -> None:
    """Verifica que um empate gera movimentos nulos."""
    high = pd.Series([10.0, 13.0])
    low = pd.Series([8.0, 5.0])

    positive_dm, negative_dm = calculate_directional_movement(
        high=high,
        low=low,
    )

    expected = pd.Series(
        [0.0, 0.0],
    )

    pd.testing.assert_series_equal(
        positive_dm,
        expected,
    )

    pd.testing.assert_series_equal(
        negative_dm,
        expected,
    )


def test_calculate_directional_movement_no_movement() -> None:
    """Verifica que movimentos não positivos geram séries nulas."""
    high = pd.Series([10.0, 9.0])
    low = pd.Series([8.0, 9.0])

    positive_dm, negative_dm = calculate_directional_movement(
        high=high,
        low=low,
    )

    expected = pd.Series(
        [0.0, 0.0],
    )

    pd.testing.assert_series_equal(
        positive_dm,
        expected,
    )

    pd.testing.assert_series_equal(
        negative_dm,
        expected,
    )


def test_calculate_directional_index() -> None:
    """Verifica o cálculo do Directional Index (DX)."""
    positive_di = pd.Series(
        [20.0, 40.0, 60.0],
    )

    negative_di = pd.Series(
        [10.0, 20.0, 30.0],
    )

    result = calculate_directional_index(
        positive_di=positive_di,
        negative_di=negative_di,
    )

    expected = pd.Series(
        [
            33.333333333333336,
            33.333333333333336,
            33.333333333333336,
        ],
    )

    pd.testing.assert_series_equal(
        result,
        expected,
    )
