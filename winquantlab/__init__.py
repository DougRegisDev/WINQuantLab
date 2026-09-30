"""Public API for WINQuantLab."""

from importlib.metadata import version

from backtesting.engine import backtest
from backtesting.pipeline import run_sessions
from data.loader import load_data
from data.normalizer import normalize
from indicators.momentum import macd, momentum, roc, rsi, stochastic
from indicators.moving_averages import ema, hma, sma, wma
from indicators.trend import adx, atr, di_minus, di_plus, supertrend
from indicators.trend.parabolic_sar import parabolic_sar
from indicators.volume.financial_volume import financial_volume
from indicators.volume.obv import obv
from indicators.volume.vwap import vwap
from indicators.volume.weis_wave import weis_wave
from reports.text_report import create_text_report
from strategies.breakout import breakout
from strategies.moving_average_crossover import moving_average_crossover

__version__ = version("WINQuantLab")

__all__ = [
    "__version__",
    "load_data",
    "normalize",
    "sma",
    "ema",
    "wma",
    "hma",
    "rsi",
    "macd",
    "momentum",
    "roc",
    "stochastic",
    "adx",
    "atr",
    "di_minus",
    "di_plus",
    "parabolic_sar",
    "supertrend",
    "financial_volume",
    "obv",
    "vwap",
    "weis_wave",
    "breakout",
    "moving_average_crossover",
    "backtest",
    "run_sessions",
    "create_text_report",
]
