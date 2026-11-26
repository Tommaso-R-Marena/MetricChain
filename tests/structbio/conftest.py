"""Shared fixtures for the STRUCTBIO test suite.

The theory division's reference checker (`experiments/reference_checker.py`, used unmodified from
the branch point) is loaded as an external oracle: our certificates are converted to its JSON
format and must be judged by it exactly as by our own checker.
"""
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: long-running test (deselect with -m 'not slow')")


@pytest.fixture(scope="session")
def reference_checker():
    spec = importlib.util.spec_from_file_location(
        "metricchain_reference_checker", ROOT / "experiments" / "reference_checker.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
