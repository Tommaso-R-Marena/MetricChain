"""
P7 item 5: feed the certificates to the theory division's min kernel.

For every certificate file out/p7_02_cert*.json this script writes lean/P7_<label>.lean, which
  * imports proofs.CertificateAlgebra (the theory division's file, identical in our tree and in the export
    at 63e36f7 by `cmp`; nothing is built: the compiled module already exists in our tree),
  * defines the published instance as a `PairInstance n k` (rational tables: integers / 2^40; each pair table
    stored in the orientation i < j; states beyond the alphabet of a site are outside the domain),
    the domain `Dom n k`, and the certificate as a term of THEIR type `Cert n k` built from `branch` and
    `leaf` only (u = U / 2^40, p i j = p j i = P2_ij / 2^41, m = messages / 2^40),
  * evaluates THEIR function with `#eval`:
        verify cert inst dom 0                 -- expected true
        verify cert inst dom (1 / 2^40)        -- expected false  (one unit above the minimum)
        verify leaf_0 inst dom 0               -- expected false  (one leaf alone on the whole domain)
        inst.energy ref                        -- expected 0      (the bound is attained at the reference)
With --run each file is passed to `lake env lean` (no `lake build`) and the output is written to
logs/p7_07_lean_<label>.log; the four results are compared with the expected ones.

usage: python3 -B p7_07_lean.py [--run] > logs/p7_07_lean.log    (last line "DONE p7_07_lean")
"""
import sys, os, json, glob, time, subprocess, re
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RUN = "--run" in sys.argv
t00 = time.time()
print(f"p7_07_lean  started {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
CH = 128


def arr(name, vals, typ):
    out = []
    parts = [vals[c:c + CH] for c in range(0, len(vals), CH)] or [[]]
    if len(parts) == 1:
        return f"def {name} : Array {typ} := #[" + ", ".join(str(v) for v in parts[0]) + "]\n"
    for q, part in enumerate(parts):
        out.append(f"def {name}_{q} : Array {typ} := #[" + ", ".join(str(v) for v in part) + "]\n")
    out.append(f"def {name} : Array {typ} := " + " ++ ".join(f"{name}_{q}" for q in range(len(parts))) + "\n")
    return "".join(out)


def tree_term(node, k):
    if "leaf" in node:
        return f"leaf_{node['leaf']}"
    ch = node["children"]
    keys = sorted(ch, key=int)
    s = ""
    for a in keys[:-1]:
        s += f"if a{node['site']}.val = {a} then {tree_term(ch[a], k)} else "
    s += tree_term(ch[keys[-1]], k)
    return f"(.branch {node['site']} (fun a{node['site']} => {s}))"


results = []
os.makedirs(os.path.join(HERE, "lean"), exist_ok=True)
for path in sorted(glob.glob(os.path.join(HERE, "out", "p7_02_cert*.json"))):
    c = json.load(open(path))
    base = os.path.basename(path)[len("p7_02_"):-len(".json")]
    lab = re.sub(r"[^A-Za-z0-9]", "_", base)
    shape = c["shape"]; n = len(shape); k = max(shape)
    den = 2 ** (-c["unit_log2"])
    Hoff = []; Hdat = []
    for i in range(n):
        Hoff.append(len(Hdat)); Hdat += c["H"][i]
    Joff = [0] * (n * n); Jdat = []
    for i in range(n):
        for j in range(i + 1, n):
            Joff[i * n + j] = len(Jdat)
            for row in c["J"][f"{i},{j}"]:
                Jdat += row
    Moff = [0] * (n * n); pos = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                Moff[i * n + j] = pos; pos += shape[i]
    L = []
    L.append("import proofs.CertificateAlgebra\n")
    L.append(f"""/-!
Workstream P7 of the science division: a certificate "shares at the leaves of a branching tree" for
  {c['instance']}, tau {c['tau']}, split {c['split']}, order {c['order']}, domain X' with {shape} states per site,
written by experiments/science/ws_P7/p7_07_lean.py from {os.path.basename(path)} ({c['variant']}).
Instance: P4's second-order lower model in difference form at the reference {c['ref']}, every table entry
rounded DOWN to a multiple of 2^-40 kcal/mol (a termwise lower instance; value 0 at the reference).
Certificate: a term of the theory division's `Cert` built from `branch` and `leaf` only
({c['n_leaf_certificates']} leaf certificates, depth {c['depth']}).  `verify` is THEIR function (proofs/CertificateAlgebra.lean),
evaluated here with `#eval` (Lean's evaluator, not kernel reduction).  Nothing in this file is a theorem.
-/
open MetricChain
namespace P7.{lab}

def den : ℚ := {den}
""")
    L.append(arr("shp", shape, "Nat"))
    L.append(arr("Hoff", Hoff, "Nat"))
    L.append(arr("Hdat", Hdat, "Int"))
    L.append(arr("Joff", Joff, "Nat"))
    L.append(arr("Jdat", Jdat, "Int"))
    L.append(arr("Moff", Moff, "Nat"))
    L.append(f"""
/-- the published instance: integers / 2^40; pair tables in the orientation i < j -/
def inst : PairInstance {n} {k} where
  h := fun i a => ((Hdat.getD (Hoff.getD i.val 0 + a.val) 0 : Int) : ℚ) / den
  J := fun i j a b => if i.val < j.val then
      ((Jdat.getD (Joff.getD (i.val * {n} + j.val) 0 + a.val * shp.getD j.val 0 + b.val) 0 : Int) : ℚ) / den else 0

/-- the domain X': the first `shp i` states of site `i` -/
def dom : Dom {n} {k} := fun i => (List.finRange {k}).filter (fun a => decide (a.val < shp.getD i.val 0))

/-- the reference configuration -/
def ref : Config {n} {k} := ![{", ".join(str(v) for v in c['ref'])}]
""")
    for l, leaf in enumerate(c["leaves"]):
        P = [0] * (n * n)
        for key, v in leaf["P2"].items():
            i, j = (int(x) for x in key.split(","))
            P[i * n + j] = v; P[j * n + i] = v
        M = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    M += leaf["m"][f"{i},{j}"]
        assert len(M) == pos
        L.append(arr(f"U_{l}", leaf["U"], "Int"))
        L.append(arr(f"P_{l}", P, "Int"))
        L.append(arr(f"M_{l}", M, "Int"))
        L.append(f"""def leaf_{l} : Cert {n} {k} := .leaf (fun i => ((U_{l}.getD i.val 0 : Int) : ℚ) / den)
  (fun i j => ((P_{l}.getD (i.val * {n} + j.val) 0 : Int) : ℚ) / (2 * den))
  (fun i j a => ((M_{l}.getD (Moff.getD (i.val * {n} + j.val) 0 + a.val) 0 : Int) : ℚ) / den)
""")
    L.append(f"""
/-- the certificate: `branch` and `leaf` only -/
def cert : Cert {n} {k} := {tree_term(c['tree'], k)}

#eval verify cert inst dom 0              -- expected: true
#eval verify cert inst dom (1 / den)      -- expected: false (one unit above the minimum)
#eval verify leaf_0 inst dom 0            -- expected: false (one leaf alone on the whole domain)
#eval inst.energy ref                     -- expected: 0
#eval cert.size                           -- nodes of the certificate

end P7.{lab}
""")
    fname = os.path.join(HERE, "lean", f"P7_{lab}.lean")
    open(fname, "w").write("".join(L))
    size = os.path.getsize(fname)
    row = dict(file=f"lean/P7_{lab}.lean", instance=c["instance"], tau=c["tau"], split=c["split"], variant=c["variant"], n=n, k=k,
               leaf_certificates=c["n_leaf_certificates"], depth=c["depth"], bytes=size)
    print(f"wrote lean/P7_{lab}.lean  ({size} bytes; PairInstance {n} {k}; {c['n_leaf_certificates']} leaves)", flush=True)
    if RUN:
        t0 = time.time()
        env = dict(os.environ)
        env["PATH"] = os.path.expanduser("~/.lean/lean-4.31.0-linux/bin") + ":" + env["PATH"]
        # NOTE: the cited log logs/p7_07_lean.log (run of 05:20 UTC) was produced with a plain subprocess call here.
        # After the memory incident of 05:26 UTC (NOTES.md) the launch was changed to run_capped (address space
        # 16 GB, anonymous memory capped at 1.5 GB, only with >= 9 GB available); this version has not been re-run.
        import run_capped
        av = next(int(ln.split()[1]) / 1024.0 for ln in open("/proc/meminfo") if ln.startswith("MemAvailable:"))
        if av < 9000:
            print(f"   SKIPPED the Lean run: MemAvailable {av:.0f} MB < 9000 MB", flush=True)
            row.update(skipped=True, as_expected=None)
            results.append(row)
            continue
        r_ = run_capped.run(["lake", "env", "lean", fname], cap_mb=1500, timeout_s=900, vlimit_mb=16000, cwd=ROOT, env=env)
        dt = r_["seconds"]
        logname = os.path.join(HERE, "logs", f"p7_07_lean_{lab}.log")
        open(logname, "w").write(f"$ cd {ROOT} && (ulimit -v 16384000; lake env lean {fname})   [through run_capped.py]\n" + r_["stdout"] + ("\n[stderr]\n" + r_["stderr"] if r_["stderr"].strip() else "")
                                 + f"\n{run_capped.summary(r_, 1500, 16000)}\nexit {r_['returncode']}  ({dt:.1f}s)\n")
        lines = [ln.strip() for ln in r_["stdout"].strip().splitlines() if ln.strip()]
        ok = (r_["returncode"] == 0 and len(lines) == 5 and lines[0] == "true" and lines[1] == "false" and lines[2] == "false" and lines[3] == "0")
        row.update(exit=r_["returncode"], seconds=dt, output=lines, as_expected=ok)
        print(f"   lake env lean: exit {r_['returncode']}, {dt:.1f}s, output {lines} -> {'AS EXPECTED (true, false, false, 0)' if ok else 'UNEXPECTED'}", flush=True)
    results.append(row)

json.dump(results, open(os.path.join(HERE, "out", "p7_07_lean.json"), "w"), indent=1)
if RUN:
    print(f"\n{sum(bool(r['as_expected']) for r in results)} of {len(results)} certificates: the theory division's `verify` (run by #eval) returns true for the bound 0, "
          f"false for the bound 2^-40, false for a single leaf, and the instance has the value 0 at the reference")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_07_lean.json")
print("DONE p7_07_lean")
