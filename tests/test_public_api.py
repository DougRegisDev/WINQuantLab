import importlib.util
from importlib.metadata import version

import pytest

import winquantlab


def test_winquantlab_package_is_available():
    package = importlib.util.find_spec("winquantlab")

    assert package is not None


def test_load_data_is_available_from_public_api():
    try:
        from winquantlab import load_data
    except ImportError:
        pytest.fail("load_data is not available from the public API")

    assert callable(load_data)


def test_normalize_is_available_from_public_api():
    try:
        from winquantlab import normalize
    except ImportError:
        pytest.fail("normalize is not available from the public API")

    assert callable(normalize)


def test_moving_averages_are_available_from_public_api():
    try:
        from winquantlab import ema, hma, sma, wma
    except ImportError:
        pytest.fail("moving averages are not available from the public API")

    assert callable(sma)
    assert callable(ema)
    assert callable(wma)
    assert callable(hma)


def test_momentum_indicators_are_available_from_public_api():
    try:
        from winquantlab import macd, momentum, roc, rsi, stochastic
    except ImportError:
        pytest.fail("momentum indicators are not available from the public API")

    assert callable(rsi)
    assert callable(macd)
    assert callable(momentum)
    assert callable(roc)
    assert callable(stochastic)


def test_trend_indicators_are_available_from_public_api():
    try:
        from winquantlab import (
            adx,
            atr,
            di_minus,
            di_plus,
            parabolic_sar,
            supertrend,
        )
    except ImportError:
        pytest.fail("trend indicators are not available from the public API")

    assert callable(adx)
    assert callable(atr)
    assert callable(di_minus)
    assert callable(di_plus)
    assert callable(parabolic_sar)
    assert callable(supertrend)


def test_volume_indicators_are_available_from_public_api():
    try:
        from winquantlab import financial_volume, obv, vwap, weis_wave
    except ImportError:
        pytest.fail("volume indicators are not available from the public API")

    assert callable(financial_volume)
    assert callable(obv)
    assert callable(vwap)
    assert callable(weis_wave)


def test_strategies_are_available_from_public_api():
    try:
        from winquantlab import breakout, moving_average_crossover
    except ImportError:
        pytest.fail("strategies are not available from the public API")

    assert callable(breakout)
    assert callable(moving_average_crossover)


def test_backtesting_is_available_from_public_api():
    try:
        from winquantlab import backtest, run_sessions
    except ImportError:
        pytest.fail("backtesting is not available from the public API")

    assert callable(backtest)
    assert callable(run_sessions)


def test_text_report_is_available_from_public_api():
    try:
        from winquantlab import create_text_report
    except ImportError:
        pytest.fail("text report is not available from the public API")

    assert callable(create_text_report)


def test_public_version_matches_installed_package_version():
    installed_version = version("WINQuantLab")

    assert winquantlab.__version__ == installed_version
