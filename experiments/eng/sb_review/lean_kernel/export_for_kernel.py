"""Write an instance and a "min" certificate of the structural-biology division as the token file that
``RunKernel.lean`` reads, so that the theory division's machine-checked kernel ``verify`` can be executed on them.

The tables come from a numpy archive (``export_tables.py``); the certificate is the detached ``structbio-mincert/1``
file, parsed by *our* strict parser (``check_files.parse_certificate``) -- the structural-biology division's loader
and its conversion ``to_metricchain_cert1`` are not used.

What the kernel is given, and why nothing here needs to be trusted for soundness: the kernel checks inequalities.
The bounds ``u_i``, ``p_ij`` of a leaf and ``l_j`` of an elimination, which the certificate format leaves to the
checker to recompute, are computed here as the minima the format prescribes and passed as *claims*; a wrong value
makes the kernel reject or proves a weaker statement, never a false one.  What must be right is the instance: the
digests printed by the Lean program (computed through the functions the kernel reads) are recomputed here from the
tables whose canonical checksum is the one the certificate names.

Scaling: the kernel instance holds the published integer tables unchanged.  Messages are integers in units of
``2^-message_bits`` of a table unit and the pair bounds are halved (the kernel states them per ordered pair), so every
rational is written as a numerator over ``den = 2^(message_bits + 1)``.

    python experiments/eng/sb_review/lean_kernel/export_for_kernel.py --tables X.npz --cert X.mincert.json --out X.tokens
        [--corrupt witness-entry | prune-order | bound]    # negative controls (see the code)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_files import load_tables, parse_certificate, tables_sha256  # noqa: E402

MODULUS = 2 ** 61 - 1


def digests(T: dict) -> tuple[int, int]:
    """The two digests of ``RunKernel.lean``, from the tables."""
    dh = 0
    for i, u in enumerate(T["unary"]):
        for a, v in enumerate(u.tolist()):
            dh = (dh + (i * 131 + a + 1) * int(v)) % MODULUS
    dj = 0
    for (i, j), t in T["pair"].items():
        rows, cols = t.shape
        w = ((i * 131 + j) * 131 + np.arange(rows, dtype=object)[:, None]) * 131 + np.arange(cols, dtype=object)[None, :] + 1
        dj = (dj + int((w * t.astype(object)).sum())) % MODULUS
    return dh, dj


def export(T: dict, C: dict, corrupt: str | None = None) -> tuple[list, dict]:
    unary = [u.astype(object) for u in T["unary"]]
    pair = {key: t.astype(object) for key, t in T["pair"].items()}
    n = len(unary)
    sizes = [len(u) for u in unary]
    k = max(sizes)
    mb = 2 ** C["message_bits"]
    den = 2 * mb
    nbrs = [[] for _ in range(n)]
    for (i, j) in pair:
        nbrs[i].append(j)
        nbrs[j].append(i)
    witness = list(C["witness"])
    lower = C["lower_bound"]                      # in units of 1/mb of a table unit
    info = dict(n=n, k=k, den=den, claimed_bound_num=2 * lower, corrupt=corrupt)

    if corrupt == "witness-entry":                # the table entry the witness uses at site 0 is lowered by one unit:
        unary[0] = unary[0].copy()                # the witness then has energy below the claimed bound, so an accepting
        unary[0][witness[0]] -= 1                 # kernel would be unsound
    elif corrupt == "bound":
        lower += 1                                # one unit of 1/mb above what the certificate claims

    def row(i, j, a):                             # J_ij(a, .) over all states of j, in table units
        return pair[(i, j)][a, :] if i < j else pair[(j, i)][:, a]

    out: list[int] = [n, k, den, 2 * lower]
    out += sizes
    for u in unary:
        out += [int(v) for v in u.tolist()]
    out.append(len(pair))
    for (i, j), t in pair.items():
        out += [i, j] + [int(v) for v in t.reshape(-1).tolist()]
    for d in C["domains"]:
        out += [len(d)] + [int(a) for a in d]
    out += [int(a) for a in witness]
    counts = dict(leaf=0, branch=0, prune=0)

    def emit(nd, D):
        """Preorder; ``D`` = current domains (lists).  Iteration over a prune chain, recursion over branches."""
        while True:
            if nd[0] == "prunes":
                steps = list(nd[1])
                if corrupt == "prune-order" and len(steps) >= 2 and counts["prune"] == 0:
                    steps = steps[::-1]           # the eliminations of the first chain in reverse order
                D = [list(d) for d in D]
                for (i, r, t) in steps:
                    counts["prune"] += 1
                    ell = [0] * n
                    for j in nbrs[i]:
                        ell[j] = int(min(row(i, j, r)[s] - row(i, j, t)[s] for s in D[j])) * den
                    out.extend([2, i, r, t] + ell)
                    D[i] = [a for a in D[i] if a != r]
                nd = nd[2]
                continue
            if nd[0] == "branch":
                counts["branch"] += 1
                i, ch = nd[1], nd[2]
                out.extend([1, i, len(ch)])
                for a in sorted(ch):
                    out.append(a)
                    D2 = [list(d) for d in D]
                    D2[i] = [a]
                    emit(ch[a], D2)
                return
            counts["leaf"] += 1
            m = {key: [int(v) for v in vec] for key, vec in nd[1].items()}        # units of 1/mb of a table unit
            u_num = []
            for i in range(n):
                best = None
                for a in D[i]:
                    v = int(unary[i][a]) * mb + sum(m[(i, j)][a] for j in range(n) if (i, j) in m)
                    best = v if best is None else min(best, v)
                u_num.append(best * 2)                                             # over den = 2 mb
            p_num = [0] * (n * n)
            for (i, j), t in pair.items():
                best = None
                mi, mj = m.get((i, j)), m.get((j, i))
                for a in D[i]:
                    for b in D[j]:
                        v = int(t[a, b]) * mb - (mi[a] if mi else 0) - (mj[b] if mj else 0)
                        best = v if best is None else min(best, v)
                p_num[i * n + j] = best                                            # p_ij = p_ji = best / (2 mb)
                p_num[j * n + i] = best
            out.append(0)
            out.extend(u_num)
            out.extend(p_num)
            out.append(len(m))
            for (i, j), vec in m.items():
                out.extend([i, j] + [2 * v for v in vec] + [0] * (k - len(vec)))
            return

    sys.setrecursionlimit(10000)
    emit(C["root"], [list(d) for d in C["domains"]])
    info.update(counts)
    return out, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--cert", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--corrupt", choices=["witness-entry", "prune-order", "bound"])
    args = ap.parse_args()
    T = load_tables(args.tables)
    C = parse_certificate(args.cert.read_text())
    sha = tables_sha256(T)
    if sha != C["model_sha256"]:
        raise SystemExit("the tables are not the instance the certificate names")
    toks, info = export(T, C, args.corrupt)
    args.out.write_text(" ".join(str(v) for v in toks) + "\n")
    dh, dj = digests(T)
    e = sum(int(T["unary"][i][a]) for i, a in enumerate(C["witness"])) + sum(int(t[C["witness"][i], C["witness"][j]]) for (i, j), t in T["pair"].items())
    info.update(tables_sha256=sha, digest_h=dh, digest_J=dj, witness_energy_table_units=e, tokens=len(toks),
                claimed_bound=f"{C['lower_bound']}/{2 ** C['message_bits']}")
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
