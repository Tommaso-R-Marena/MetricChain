"""Provenance of experiment rows: the `commit` field must name the code that ran.

Defect SB-DEF-08 (2026-11-26): the development drivers asked git for the head each time a row was
started.  A process that runs for minutes while the branch moves then records a commit *later*
than the code it has in memory.  The drivers must read the commit once, when the process starts.
"""
from __future__ import annotations

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _load_dev_driver():
    spec = importlib.util.spec_from_file_location(
        "structbio_gmec_dev_run", ROOT / "experiments" / "structbio" / "gmec_dev" / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_commit_is_read_once_at_process_start(monkeypatch):
    dev = _load_dev_driver()
    first = dev.git_commit()
    assert first != "unknown"

    def moved_head(*args, **kwargs):          # what git would answer after the branch has moved
        class Out:
            stdout = "0" * 40 + "\n"
        return Out()

    monkeypatch.setattr(dev.subprocess, "run", moved_head)
    assert dev.git_commit() == first
