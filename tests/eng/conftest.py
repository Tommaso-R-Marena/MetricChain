"""Shared guard of the engineering test suite.

Every test must find, and leave, the floating-point unit in round-to-nearest.  A library that changes the rounding
mode of the process (the Parma Polyhedra Library does, on import) silently alters every later float computation in
the same interpreter -- numpy, the C kernels, even Python's parsing and printing of floats.  On 2026-11-26 that made
an unrelated test fail only when the whole suite ran in one session.
"""
import pytest


def _to_nearest() -> bool:
    one, tiny = 1.0, 2.0 ** -53
    return one + tiny == one and one - tiny / 2 == one


def pytest_collection_finish(session):
    if not _to_nearest():
        raise pytest.UsageError("an import during collection changed the floating-point rounding mode of the process")


@pytest.fixture(autouse=True)
def _rounding_mode_guard(request):
    assert _to_nearest(), f"rounding mode is not round-to-nearest before {request.node.nodeid}"
    yield
    assert _to_nearest(), f"{request.node.nodeid} left the floating-point unit in another rounding mode"
