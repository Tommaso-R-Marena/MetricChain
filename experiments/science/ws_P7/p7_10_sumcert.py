"""
P7 items 3 and 5: a TRIPLET certificate written with the rules the theory division's min kernel already has
(`sum`, `branch`, `leaf`), and fed to their `verify`.

A certificate with triplet constraints (p7_03b_multi.py) is: messages m, and for every triple T and each of its
pairs a table lam_{T,pq}; all terms of
    U_i  = min_a [H_i(a) + sum_j m_ij(a)],   R_ij = min [J_ij - m_ij - m_ji - sum_T lam_{T,ij}],   Q_T = min [lam_pq + lam_pr + lam_qr]
are >= 0 (= 0 at the reference).  In the kernel's algebra this is

    sum I_T1 (I - I_T1)  0 0  (branch p1 [leaf, ..., leaf])  ( sum I_T2 (I - I_T1 - I_T2) 0 0 (branch p2 [...]) ( leaf u p m ) )

where I_T is the instance whose only non-zero tables are the three pair tables lam_{T,..} (so that I_T plus the
remainder is TERMWISE EQUAL to I: the hypothesis `SumOK`), the minimum 0 of the three-site instance I_T is
certified by one branching on a site p of T with, in each leaf, the exact dynamic-programming messages of the
remaining edge (this is the construction of the theory division's own `triangleCert`), and the remainder is
certified by ONE leaf: the messages of the triplet certificate.  No new rule is needed.

For each gap analysis: the first set of triples certified by p7_03b; everything in integers (units 2^-40);
every leaf is re-checked here by p7lib.leaf_bound on its own sub-instance; then lean/P7S_<label>.lean is written
and `lake env lean` evaluates  verify cert inst dom 0  (expected true),  verify cert inst dom (1/2^40)  (false).

usage: python3 -B p7_10_sumcert.py [--run] > logs/p7_10_sumcert.log   (writes out/p7_10_sumcert.json; last line "DONE p7_10_sumcert")
"""
import sys, os, json, time, re, subprocess
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

RUN = "--run" in sys.argv
ROOT = os.path.normpath(os.path.join(L7.HERE, "..", "..", ".."))
t00 = time.time()
print(f"p7_10_sumcert  started {L7.now()}")
CH = 128


class IntInst:
    """a pairwise integer instance (tables H, J for i < j) with the interface p7lib.leaf_bound needs."""
    class _PM:
        def ok(self, i, j):
            return None

    def __init__(self, H, J):
        self.H = H; self.J = J; self.n = len(H); self.pm = IntInst._PM()


def arr(name, vals, typ):
    out = []
    parts = [vals[c:c + CH] for c in range(0, len(vals), CH)] or [[]]
    if len(parts) == 1:
        return f"def {name} : Array {typ} := #[" + ", ".join(str(int(v)) for v in parts[0]) + "]\n"
    for q, part in enumerate(parts):
        out.append(f"def {name}_{q} : Array {typ} := #[" + ", ".join(str(int(v)) for v in part) + "]\n")
    out.append(f"def {name} : Array {typ} := " + " ++ ".join(f"{name}_{q}" for q in range(len(parts))) + "\n")
    return "".join(out)


five = {(f"{g['family']}{g['nres']}/{g['bb']}", g["tau"]): g for g in json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]}
multi = json.load(open(os.path.join(L7.HERE, "out", "p7_03b_multi.json")))
chosen = {}
for r in multi:
    if r["certified"] and (r["instance"], r["tau"]) not in chosen:
        chosen[(r["instance"], r["tau"])] = [tuple(T) for T in r["triples"]]
results = []
SEEN = {}
for key, Ts in chosen.items():
    g = five[key]
    lab = re.sub(r"[^A-Za-z0-9]", "_", f"{g['family']}{g['nres']}_{g['bb']}_tau{g['tau']}_{g['split'].split('-')[0]}")
    inst = L4.load_instance(g["tag"], float(g["tau"]))
    Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
    pm = PM.from_grid(Lmod, x0); ipm = IPM(pm); D = pm.full_domain()
    n = pm.n; shape = pm.shape; k = max(shape)
    res = L7.multi_triple_lp(pm, Ts)
    mI, lamI = L7.multi_triple_to_int(ipm, D, res["s"], res["lam"], Ts)
    LB, U, R, Q = L7.multi_triple_bound(ipm, D, mI, lamI, Ts)
    assert LB == 0 and all(u == 0 for u in U) and all(v == 0 for v in R.values()) and all(v == 0 for v in Q.values())
    zeroH = [np.zeros(kk, dtype=np.int64) for kk in shape]

    def zeroJ():
        return {(i, j): np.zeros((shape[i], shape[j]), dtype=np.int64) for i in range(n) for j in range(i + 1, n)}
    # ---- the triple instances and their certificates (branch on the site of T with the fewest states)
    parts = []
    Jrem = {kk: v.copy() for kk, v in ipm.J.items()}
    nleaf_chk = 0
    for T in Ts:
        JT = zeroJ()
        for pq in L7._pairs_of(T):
            JT[pq] = lamI[(T, pq)].copy()
            Jrem[pq] = Jrem[pq] - lamI[(T, pq)]
        IT = IntInst(zeroH, JT)
        p_ = min(T, key=lambda i: shape[i])
        q_, r_ = [i for i in T if i != p_]

        def tab(x, y):                                            # (k_x, k_y) table of the pair {x, y} of I_T
            return JT[(x, y)] if x < y else JT[(y, x)].T
        leaves = []
        for a in range(shape[p_]):
            m = L7.zero_messages(pm)
            m[(q_, p_)] = tab(p_, q_)[a, :].copy()                # pair (p, q) moved into the one-site term of q
            m[(r_, p_)] = tab(p_, r_)[a, :].copy()                # pair (p, r) moved into the one-site term of r
            m[(q_, r_)] = -tab(p_, q_)[a, :]                      # the one-site term of q moved into the pair (q, r)
            psi = (tab(q_, r_) + tab(p_, q_)[a, :][:, None]).min(axis=0)
            m[(r_, q_)] = psi.copy()                              # dynamic-programming message of the edge q - r
            Dl = L7.fix(D, p_, a)
            lb, Ul, Pl = L7.leaf_bound(IT, Dl, m)
            assert lb >= 0, "a dynamic-programming leaf of a triple instance fails"
            nleaf_chk += 1
            leaves.append(dict(m=m, U=Ul, P=Pl, state=a))
        parts.append(dict(T=T, J=JT, branch=p_, leaves=leaves))
    Irem = IntInst(ipm.H, Jrem)
    lbR, UR, PR = L7.leaf_bound(Irem, D, mI)
    assert lbR == 0, "the remainder leaf fails"
    nleaf_chk += 1
    # exact check of the termwise identity  I = sum_T I_T + remainder
    for kk in ipm.J:
        tot = Jrem[kk].copy()
        for prt in parts:
            tot = tot + prt["J"][kk]
        assert np.array_equal(tot, ipm.J[kk])
    print(f"\n{key[0]} tau {key[1]} split {g['split']}: triples {Ts}; LP slack t = {res['t']:.6f}; integer certificate: all U, R, Q are 0; "
          f"{sum(len(p['leaves']) for p in parts)} dynamic-programming leaves + 1 remainder leaf re-checked in integers ({nleaf_chk} leaves)")
    # ---- Lean
    den = 2 ** L7.SCALE
    Hoff = []; Hdat = []
    for i in range(n):
        Hoff.append(len(Hdat)); Hdat += [int(v) for v in ipm.H[i]]
    Joff = [0] * (n * n); pos = 0
    for i in range(n):
        for j in range(i + 1, n):
            Joff[i * n + j] = pos; pos += shape[i] * shape[j]

    def jflat(Jd):
        out = []
        for i in range(n):
            for j in range(i + 1, n):
                out += [int(v) for v in Jd[(i, j)].ravel()]
        return out
    Moff = [0] * (n * n); mpos = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                Moff[i * n + j] = mpos; mpos += shape[i]

    def mflat(m):
        out = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    out += [int(v) for v in m[(i, j)]]
        return out

    def pflat(P):
        out = [0] * (n * n)
        for (i, j), v in P.items():
            out[i * n + j] = int(v); out[j * n + i] = int(v)
        return out
    Lz = ["import proofs.CertificateAlgebra\n", f"""/-!
Workstream P7 of the science division: a TRIPLET certificate for {key[0]}, tau {key[1]}, split {g['split']}
(X' with {list(shape)} states per site), triples {Ts}, written with the rules `sum`, `branch`, `leaf` of the
theory division's `Cert` by experiments/science/ws_P7/p7_10_sumcert.py.  `verify` is THEIR function, evaluated
with `#eval`.  Nothing in this file is a theorem.
-/
open MetricChain
namespace P7S.{lab}

def den : ℚ := {den}
"""]
    Lz.append(arr("shp", list(shape), "Nat")); Lz.append(arr("Hoff", Hoff, "Nat")); Lz.append(arr("Hdat", Hdat, "Int"))
    Lz.append(arr("Joff", Joff, "Nat")); Lz.append(arr("Jdat", jflat(ipm.J), "Int")); Lz.append(arr("Moff", Moff, "Nat"))
    Lz.append(f"""
def jtab (dat : Array Int) (i j : Fin {n}) (a b : Fin {k}) : ℚ :=
  if i.val < j.val then ((dat.getD (Joff.getD (i.val * {n} + j.val) 0 + a.val * shp.getD j.val 0 + b.val) 0 : Int) : ℚ) / den else 0
def mkLeaf (U P M : Array Int) : Cert {n} {k} := .leaf (fun i => ((U.getD i.val 0 : Int) : ℚ) / den)
  (fun i j => ((P.getD (i.val * {n} + j.val) 0 : Int) : ℚ) / (2 * den))
  (fun i j a => ((M.getD (Moff.getD (i.val * {n} + j.val) 0 + a.val) 0 : Int) : ℚ) / den)

/-- the published instance -/
def inst : PairInstance {n} {k} where
  h := fun i a => ((Hdat.getD (Hoff.getD i.val 0 + a.val) 0 : Int) : ℚ) / den
  J := jtab Jdat
def dom : Dom {n} {k} := fun i => (List.finRange {k}).filter (fun a => decide (a.val < shp.getD i.val 0))
""")
    prev = "inst"
    for q, prt in enumerate(parts):
        Lz.append(arr(f"T{q}dat", jflat(prt["J"]), "Int"))
        Lz.append(f"""/-- the instance of triple {prt['T']}: three pair tables, nothing else -/
def instT{q} : PairInstance {n} {k} where
  h := fun _ _ => 0
  J := jtab T{q}dat
/-- what is left of the instance after the triples 0 .. {q} -/
def instR{q} : PairInstance {n} {k} where
  h := {prev}.h
  J := fun i j a b => {prev}.J i j a b - instT{q}.J i j a b
""")
        names = []
        for lf in prt["leaves"]:
            nm = f"T{q}_{lf['state']}"
            Lz.append(arr(f"U_{nm}", lf["U"], "Int")); Lz.append(arr(f"P_{nm}", pflat(lf["P"]), "Int")); Lz.append(arr(f"M_{nm}", mflat(lf["m"]), "Int"))
            names.append(f"mkLeaf U_{nm} P_{nm} M_{nm}")
        s = ""
        for a, nm in enumerate(names[:-1]):
            s += f"if a.val = {a} then {nm} else "
        s += names[-1]
        Lz.append(f"def certT{q} : Cert {n} {k} := .branch {prt['branch']} (fun a => {s})\n")
        prev = f"instR{q}"
    Lz.append(arr("U_R", UR, "Int")); Lz.append(arr("P_R", pflat(PR), "Int")); Lz.append(arr("M_R", mflat(mI), "Int"))
    term = "(mkLeaf U_R P_R M_R)"
    for q in reversed(range(len(parts))):
        term = f"(.sum instT{q} instR{q} 0 0 certT{q} {term})"
    Lz.append(f"""
/-- the triplet certificate: `sum`, `branch`, `leaf` -/
def cert : Cert {n} {k} := {term}

#eval verify cert inst dom 0              -- expected: true
#eval verify cert inst dom (1 / den)      -- expected: false
#eval verify (mkLeaf U_R P_R M_R) inst dom 0   -- expected: false (the remainder leaf alone, on the whole instance)
#eval cert.size

end P7S.{lab}
""")
    fname = os.path.join(L7.HERE, "lean", f"P7S_{lab}.lean")
    open(fname, "w").write("".join(Lz))
    row = dict(instance=key[0], tau=key[1], split=g["split"], triples=[list(T) for T in Ts], t=res["t"], file=f"lean/P7S_{lab}.lean", bytes=os.path.getsize(fname),
               dp_leaves=sum(len(p["leaves"]) for p in parts), sum_nodes=len(parts))
    print(f"   wrote lean/P7S_{lab}.lean ({row['bytes']} bytes): {len(parts)} `sum` node(s), {row['dp_leaves']} leaves under `branch`, 1 remainder leaf")
    sig = (tuple(shape), tuple(int(v) for h in ipm.H for v in h), tuple(int(v) for kk in sorted(ipm.J) for v in ipm.J[kk].ravel()))
    if RUN and sig in SEEN:
        row.update(skipped=f"the published instance is identical to that of {SEEN[sig]} (same X'): Lean run not repeated", as_expected=None)
        print(f"   Lean run not repeated: the published instance is identical to that of {SEEN[sig]}", flush=True)
    elif RUN:
        SEEN[sig] = f"{key[0]} tau {key[1]}"
        # one Lean process at a time, under `ulimit -v` 16 GB and a cap of 1.5 GB anonymous memory, and only
        # if at least 9 GB of memory are available (agreed with the coordinator after the incident of 05:26 UTC)
        import run_capped
        env = dict(os.environ)
        env["PATH"] = os.path.expanduser("~/.lean/lean-4.31.0-linux/bin") + ":" + env["PATH"]

        def avail_mb():
            for ln in open("/proc/meminfo"):
                if ln.startswith("MemAvailable:"):
                    return int(ln.split()[1]) / 1024.0
        waited = 0
        while avail_mb() < 9000 and waited < 180:
            time.sleep(5); waited += 5
        av = avail_mb()
        if av < 9000:
            row.update(skipped=f"MemAvailable {av:.0f} MB < 9000 MB after waiting {waited} s", as_expected=None)
            print(f"   SKIPPED the Lean run: MemAvailable {av:.0f} MB < 9000 MB", flush=True)
        else:
            pr = run_capped.run(["lake", "env", "lean", fname], cap_mb=1500, timeout_s=600, vlimit_mb=16000, cwd=ROOT, env=env)
            dt = pr["seconds"]
            mem = run_capped.summary(pr, 1500, 16000)
            open(os.path.join(L7.HERE, "logs", f"p7_10_lean_{lab}.log"), "w").write(
                f"$ cd {ROOT} && (ulimit -v 16384000; lake env lean {fname})   [through run_capped.py; MemAvailable before: {av:.0f} MB]\n" + pr["stdout"]
                + ("\n[stderr]\n" + pr["stderr"] if pr["stderr"].strip() else "") + f"\n{mem}\nexit {pr['returncode']}  ({dt:.1f}s)\n")
            lines = [ln.strip() for ln in pr["stdout"].strip().splitlines() if ln.strip()]
            ok = pr["returncode"] == 0 and lines[:3] == ["true", "false", "false"]
            row.update(exit=pr["returncode"], seconds=dt, output=lines[:6], as_expected=ok, peak_anon_mb=pr["peak_anon_mb"], peak_file_mb=pr["peak_file_mb"],
                       vmpeak_mb=pr["vmpeak_mb"], mem_available_before_mb=av)
            print(f"   lake env lean (MemAvailable before {av:.0f} MB): exit {pr['returncode']}, {dt:.1f}s, output {lines[:6]} -> {'AS EXPECTED (true, false, false)' if ok else 'UNEXPECTED'}", flush=True)
            print(f"   {mem}", flush=True)
    results.append(row)
json.dump(results, open(os.path.join(L7.HERE, "out", "p7_10_sumcert.json"), "w"), indent=1)
if RUN:
    print(f"\n{sum(bool(r['as_expected']) for r in results)} of {sum('exit' in r for r in results)} Lean runs: the triplet certificate in the form sum/branch/leaf is accepted by the theory division's `verify` (#eval); "
          f"{sum('skipped' in r for r in results)} not run (see above)")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_10_sumcert.json   finished {L7.now()}")
print("DONE p7_10_sumcert")
