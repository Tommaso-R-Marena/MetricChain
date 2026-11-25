"""Modal job: exhaustive enumeration of self-avoiding diamond-lattice chains, split over prefixes.

Ephemeral app (``modal run`` only; nothing is deployed, no endpoint, no schedule, no volume).

    modal run modal_jobs/chain_enum_app.py --nmin 21 --nmax 24

For each chain length ``n`` the enumeration of ``src/metricchain_eng/chains/dia_enum.c`` is
split into ``--splits`` disjoint pieces (prefixes of ``--k`` torsions, round-robin), each piece
runs in its own single-core container, and the class tables are merged locally (counts added,
gmin/gmax by min/max, pattern bitmaps by OR) into

    experiments/eng/chain_cover/data/dia_Sc<cut>_n<n>.txt      (same format as a direct run)
    experiments/eng/chain_cover/data/dia_Sc<cut>_n<n>.meta.json (usage and pattern statistics)

Resource bounds (enforced by this file): 1 core and 512 MiB per container, at most
``MAX_CONTAINERS`` containers, ``TIMEOUT_S`` seconds per piece, no retries.  The worst case is
therefore ``splits * TIMEOUT_S`` core-seconds per chain length.
"""
from __future__ import annotations

import json
import sys
import time
import zlib
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
C_SOURCE = ROOT / "src" / "metricchain_eng" / "chains" / "dia_enum.c"

MAX_CONTAINERS = 50
TIMEOUT_S = 1800

app = modal.App("metricchain-eng-chain-enum")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("gcc", "libc6-dev")
    .add_local_file(C_SOURCE, "/opt/mc/dia_enum.c", copy=True)
    # no -march=native: the build host and the execution hosts may have different CPUs
    .run_commands("cc -O3 -o /opt/mc/dia_enum /opt/mc/dia_enum.c")
)


@app.function(image=image, cpu=1.0, memory=512, timeout=TIMEOUT_S, max_containers=MAX_CONTAINERS, retries=0)
def enum_split(n: int, s_cut: int, k: int, splits: int, w: int, want_bitmap: bool) -> dict:
    """Run one piece of the enumeration; returns the class table text and (optionally) the pattern bitmap."""
    import os
    import subprocess
    import tempfile

    t0 = time.time()
    cmd = ["/opt/mc/dia_enum", "-n", str(n), "-c", str(s_cut), "-k", str(k), "-W", str(splits), "-w", str(w)]
    bitmap = None
    with tempfile.TemporaryDirectory() as tmp:
        bpath = os.path.join(tmp, "patterns.bin")
        if want_bitmap:
            cmd += ["-b", bpath]
        out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
        if want_bitmap:
            with open(bpath, "rb") as f:
                bitmap = zlib.compress(f.read(), 6)
    return {"n": n, "w": w, "text": out, "bitmap": bitmap, "seconds": time.time() - t0}


@app.local_entrypoint()
def main(nmin: int = 21, nmax: int = 24, cut: int = 12, splits: int = 64, k: int = 8, bitmap: bool = True):
    sys.path.insert(0, str(ROOT / "src"))
    from metricchain_eng.chains.profile_cover import parse_enum_output

    data_dir = ROOT / "experiments" / "eng" / "chain_cover" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for n in range(nmin, nmax + 1):
        t0 = time.time()
        pieces = list(enum_split.starmap([(n, cut, k, splits, w, bitmap) for w in range(splits)]))
        wall = time.time() - t0
        tab = parse_enum_output("\n".join(p["text"] for p in pieces))
        lines = [f"# dia_enum n_torsions={n} n_beads={n + 3} s_cut={cut} mirror=1 split_k=0 split_W=1 split_w=0",
                 "# distances " + " ".join(str(d) for d in tab.distances),
                 f"# conformations={tab.n_conformations} classes={tab.n_classes}",
                 f"# merged from {splits} prefix splits (k={k}) of modal_jobs/chain_enum_app.py",
                 "# columns: pair counts at each distance | count | gmin | count_gmin | gmax"]
        for i in range(tab.n_classes):
            lines.append(" ".join(str(int(v)) for v in tab.hist[i])
                         + f" {int(tab.count[i])} {int(tab.gmin[i])} {int(tab.count_gmin[i])} {int(tab.gmax[i])}")
        (data_dir / f"dia_Sc{cut}_n{n}.txt").write_text("\n".join(lines) + "\n")
        meta = {"n_torsions": n, "s_cut": cut, "splits": splits, "split_k": k,
                "conformations": tab.n_conformations, "classes": tab.n_classes,
                "core_seconds": round(sum(p["seconds"] for p in pieces), 1),
                "max_piece_seconds": round(max(p["seconds"] for p in pieces), 1),
                "wall_seconds": round(wall, 1)}
        if bitmap:
            merged = bytearray(zlib.decompress(pieces[0]["bitmap"]))
            for p in pieces[1:]:
                b = zlib.decompress(p["bitmap"])
                merged = bytearray(x | y for x, y in zip(merged, b))
            total = 1 << n
            realised = sum(bin(byte).count("1") for byte in merged[: total // 8]) \
                + bin(merged[total // 8] & ((1 << (total % 8)) - 1)).count("1")
            meta["gauche_patterns_total"] = total
            meta["gauche_patterns_realised"] = realised
            (data_dir / f"dia_patterns_n{n}.bin").write_bytes(bytes(merged))
        (data_dir / f"dia_Sc{cut}_n{n}.meta.json").write_text(json.dumps(meta, indent=1) + "\n")
        print(json.dumps(meta), flush=True)
