"""Public API for WINQuantLab."""

from importlib.metadata import version

from data.loader import load_data

__version__ = version("WINQuantLab")

__all__ = [
    "__version__",
    "load_data",
]
