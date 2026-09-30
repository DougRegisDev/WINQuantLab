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


def test_public_version_matches_installed_package_version():
    installed_version = version("WINQuantLab")

    assert winquantlab.__version__ == installed_version
