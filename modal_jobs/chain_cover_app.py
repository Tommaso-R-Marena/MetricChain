"""Modal job: covering numbers and entropy numbers of lattice-chain profile sets, one container per chain length.

Ephemeral app (``modal run`` only).  Runs ``metricchain_eng.chains.lattice_analysis.analyse_table``
-- the same function the local driver ``experiments/eng/chain_cover/run_lattice.py`` uses -- on the
class tables stored in ``experiments/eng/chain_cover/data/`` and merges the rows into
``experiments/eng/chain_cover/results/lattice_Sc<cut>.json``.

    modal run modal_jobs/chain_cover_app.py --nmin 1 --nmax 24

Resource bounds: 4 cores and 8 GiB per chain length, at most ``MAX_CONTAINERS`` containers,
``TIMEOUT_S`` seconds each, no retries.  Every integer programme has a time limit
(``--cover-time-limit`` per solver and setting, ``--net-time-limit`` per net); where a solver does not
prove optimality the result is the rigorous bracket [certified lower bound, verified cover].
"""
from __future__ import annotations

import sys
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
MAX_CONTAINERS = 24
TIMEOUT_S = 5400

app = modal.App("metricchain-eng-chain-cover")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("numpy==2.5.5", "scipy==1.18.1", "ortools==9.15.6755")
    .add_local_dir(ROOT / "src" / "metricchain_eng", "/root/src/metricchain_eng",
                   ignore=["**/__pycache__/**", "**/*.c"])
)


@app.function(image=image, cpu=4.0, memory=8192, timeout=TIMEOUT_S, max_containers=MAX_CONTAINERS, retries=0)
def analyse(table_text: str, solvers: str, net_time_limit: float, cover_time_limit: float,
            cpsat_max_centres: int) -> dict:
    sys.path.insert(0, "/root/src")
    from metricchain_eng.chains.lattice_analysis import analyse_table
    from metricchain_eng.chains.profile_cover import parse_enum_output

    return analyse_table(parse_enum_output(table_text), tuple(solvers.split(",")), exact_nets=True,
                         net_time_limit=net_time_limit, cover_time_limit=cover_time_limit,
                         cpsat_max_centres=cpsat_max_centres)


@app.local_entrypoint()
def main(nmin: int = 1, nmax: int = 24, cut: int = 12, solvers: str = "highs,cpsat", net_time_limit: float = 60.0,
         cover_time_limit: float = 300.0, cpsat_max_centres: int = 700):
    sys.path.insert(0, str(ROOT / "src"))
    from metricchain_eng.chains.lattice_analysis import format_row, merge_rows

    here = ROOT / "experiments" / "eng" / "chain_cover"
    texts = []
    for n in range(nmin, nmax + 1):
        path = here / "data" / f"dia_Sc{cut}_n{n}.txt"
        if path.exists():
            texts.append(path.read_text())
    out = here / "results" / f"lattice_Sc{cut}.json"
    out.parent.mkdir(exist_ok=True)
    kwargs = {"solvers": solvers, "net_time_limit": net_time_limit, "cover_time_limit": cover_time_limit,
              "cpsat_max_centres": cpsat_max_centres}
    for row in analyse.map(texts, kwargs=kwargs, order_outputs=False):
        merge_rows(out, [row], cut)          # written after every row, so a failure loses nothing
        print(format_row(row), flush=True)
