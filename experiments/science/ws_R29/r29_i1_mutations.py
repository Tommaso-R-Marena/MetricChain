#!/usr/bin/env python3
"""r29_i1_mutations.py [u J K]  --  mutation study of z6_certified_tops.py (Item 1 (iv) of the brief).

For every mutation (one small textual change of a COPY of the theory division's script; the original is only read):
  (1) the mutant is run as a program (through r29_wrap.py: 3 GB cap) and ITS OWN verdict is recorded: the last
      line "ALL CHECKS PASS" / "CHECK FAILED", or an assertion / exception of its own;
  (2) an instrumented copy of the same mutant (two logging statements, no other change) is checked by my
      independent exact checker (r29_i1_mutworker.py): certificate violations by kind, pairs that are truly
      invalid in 40-digit arithmetic, tops below the semi-analytic envelope top;
  (3) the tops are compared with those of the unmutated run.
A mutation is CAUGHT BY THE SCRIPT only if (1) is not "ALL CHECKS PASS".  The baseline M00 (no mutation) must pass
both; M20 (coarser but still outward intervals) is a specificity control: valid, and my checker must not flag it.
"""
import ast
import os
import re
import subprocess
import sys

import r29lib as R

R.cap_memory()

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z"
ORIG = open(os.path.join(EXPORT, "z6_certified_tops.py")).read()
MUTDIR = os.path.join(HERE, "mutants")
os.makedirs(MUTDIR, exist_ok=True)
u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
J = sys.argv[2] if len(sys.argv) > 2 else "6"
K = sys.argv[3] if len(sys.argv) > 3 else "400"

UP = "    return math.nextafter(float(x.b), INF)"
RET = "    return up(e), max(0.0, up(kl_iv(r, HALF)))"
E_LINE = "    e = kl_iv(r, PU)"
AL = "        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))))"
BE = "        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))))"
M_LOOP = "        while Fr(m) < mstar:\n            m = math.nextafter(m, INF)"
B_LOOP = "        while Fr(bL) < Fr(m) * C - 1:\n            bL = math.nextafter(bL, INF)"
MSTAR = "        mstar = max((1 - Vx) / (C - X) for X, Vx in vs[:-1])"
TOP_A = "    A = Fr(ABAR)"
TOP_F = "        if mid + ABAR * float(V.val(np.array([mid]))[0][0]) >= ABAR:"
TOP_V = "        if Fr(c) + A * V.val_exact(c) >= A:\n            return min(c, V.c)"

MUTS = [
    ("M00", "baseline: no mutation", []),
    # --- rounding directions of the certified pairs and of abar
    ("M01", "up(): nextafter towards -inf (every upper bound e', th, abar rounded the wrong way)", [(UP, "    return math.nextafter(float(x.b), -INF)")]),
    ("M02", "up(): lower end of the interval, x.a for x.b (outward rounding of the interval dropped)", [(UP, "    return math.nextafter(float(x.a), INF)")]),
    ("M03", "up(): no nextafter step (float() of the upper end only)", [(UP, "    return float(x.b)")]),
    ("M04", "pair: e' := dn(e) (the rate rounded down)", [(RET, "    return dn(e), max(0.0, up(kl_iv(r, HALF)))")]),
    ("M05", "pair: th := dn(KL(rho||1/2)) (theta rounded down)", [(RET, "    return up(e), max(0.0, dn(kl_iv(r, HALF)))")]),
    ("M06", "pair: midpoints of both intervals (no outward rounding)", [(RET, "    return float(e.mid), max(0.0, float(kl_iv(r, HALF).mid))")]),
    ("M32", "pair at rho = 1/2: e' := dn(eps*) (then theta_na(e') > 0 = th)", [("        return up(kl_iv(HALF, PU)), 0.0", "        return dn(kl_iv(HALF, PU)), 0.0")]),
    ("M19", "p_u replaced by a double (its interval dropped)", [("PU = 1 / (1 + iv.exp(U))", "PU = iv.mpf(float((1 / (1 + iv.exp(U))).mid))")]),
    ("M20", "interval precision 30 -> 12 digits (still outward: must stay valid)", [("iv.dps = 30", "iv.dps = 12")]),
    # --- interval evaluated at the wrong point / monotonicity used the wrong way
    ("M22", "theta bound evaluated at rho(1 + 1e-7) instead of rho", [(RET, "    return up(e), max(0.0, up(kl_iv(r * (1 + iv.mpf(10) ** -7), HALF)))")]),
    ("M23", "rate evaluated at rho(1 - 1e-7) instead of rho", [(E_LINE, "    e = kl_iv(r * (1 - iv.mpf(10) ** -7), PU)")]),
    ("M18", "the two divergences swapped (e' from KL(rho||1/2), th from KL(rho||p_u))", [(E_LINE, "    e = kl_iv(r, HALF)"), (RET, "    return up(e), max(0.0, up(kl_iv(r, PU)))")]),
    # --- rounding of the stored lines
    ("M07", "stored slope rounded UP (down -> upw)", [(AL, AL.replace("float(down(", "float(upw("))]),
    ("M08", "stored beta rounded DOWN (upw -> down)", [(BE, BE.replace("float(upw(", "float(down("))]),
    ("M09", "no rounding of the stored lines (n = 0 steps)", [("def down(x, n=4):", "def down(x, n=0):"), ("def upw(x, n=4):", "def upw(x, n=0):")]),
    ("M09b", "one nextafter step instead of four", [("def down(x, n=4):", "def down(x, n=1):"), ("def upw(x, n=4):", "def upw(x, n=1):")]),
    ("M09c", "two nextafter steps instead of four", [("def down(x, n=4):", "def down(x, n=2):"), ("def upw(x, n=4):", "def upw(x, n=2):")]),
    ("M21", "parent line multiplied by (1 + 1e-9) (not below V)", [("        a0 = float(V.al[i_]) if i_ >= 0 else 0.0", "        a0 = float(V.al[i_]) * (1 + 1e-9) if i_ >= 0 else 0.0")]),
    # --- the cap
    ("M10", "cap slope rounded DOWN", [(M_LOOP, "        while Fr(m) > mstar:\n            m = math.nextafter(m, -INF)")]),
    ("M11", "cap intercept rounded DOWN (line above 1 at c)", [(B_LOOP, "        while Fr(bL) > Fr(m) * C - 1:\n            bL = math.nextafter(bL, -INF)")]),
    ("M12", "cap loosened: tangent taken from (c(1 + 1e-6), 1), line still through (c, 1)", [(MSTAR, "        mstar = max((1 - Vx) / (C * Fr(1000001, 1000000) - X) for X, Vx in vs[:-1])")]),
    ("M13", "cap loosened: capped at 1.001 instead of 1", [("        bL = float(Fr(m) * C - 1)\n        while Fr(bL) < Fr(m) * C - 1:", "        bL = float(Fr(m) * C - Fr(1001, 1000))\n        while Fr(bL) < Fr(m) * C - Fr(1001, 1000):")]),
    ("M14", "cap slope: min over the vertices instead of max", [(MSTAR, MSTAR.replace("mstar = max(", "mstar = min("))]),
    # --- the top
    ("M15", "top verified with a LOWER bound of a (ALOW for ABAR)", [(TOP_A, "    A = Fr(ALOW)"), (TOP_F, TOP_F.replace("ABAR", "ALOW"))]),
    ("M16", "top: exact verification removed (float bisection accepted)", [(TOP_V, "        if True:\n            return min(c, V.c)")]),
    ("M17", "top: exact verification removed and the LOWER end of the bisection taken", [(TOP_V, "        if True:\n            return min(c, V.c)"), ("    c = hi\n", "    c = lo\n")]),
    ("M26", "val_exact computed in floating point", [("            w = Fr(float(a_)) * B - Fr(float(b_))", "            w = Fr(float(a_) * float(B) - float(b_))")]),
    # --- the hull and the selection
    ("M24", "hull: pop condition reversed", [("                if (b3 - b1) * (a2 - a1) <= (b2 - b1) * (a3 - a1):", "                if (b3 - b1) * (a2 - a1) >= (b2 - b1) * (a3 - a1):")]),
    ("M27", "selection: lines with nonpositive value at their sample point kept (harmless)", [("    good = (Fv > 0) & np.isfinite(Fv) & (Fv < 50.0)", "    good = np.isfinite(Fv) & (Fv < 50.0)")]),
    ("M28", "selection: sample points with V >= 1 kept (harmless)", [("    keep = s < 1.0", "    keep = s < 2.0")]),
]


def mutate(text, patches):
    for old, new in patches:
        if text.count(old) != 1:
            raise RuntimeError("patch does not apply exactly once: %r (%d)" % (old[:60], text.count(old)))
        text = text.replace(old, new)
    return text


def instrument(text):
    t = mutate(text, [('INF = float("inf")\n', 'INF = float("inf")\n_R29LOG = []\n')])
    lines = t.split("\n")
    out, n = [], 0
    for ln in lines:
        out.append(ln)
        if ln.strip().startswith("be_new.append("):
            out.append("        _R29LOG.append((al_new[-1], be_new[-1], r_, e_, th_, a0, b0))")
            n += 1
    if n != 1:
        raise RuntimeError("instrumentation point not found exactly once")
    return "\n".join(out)


def run(cmd, env=None, timeout=420):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, timeout=timeout, text=True)
        return p.stdout, p.returncode
    except subprocess.TimeoutExpired as ex:
        return (ex.stdout or "") + "\nR29: TIMEOUT", -9


env = dict(os.environ)
env["OMP_NUM_THREADS"] = "1"
env["PYTHONPATH"] = EXPORT + os.pathsep + HERE + os.pathsep + env.get("PYTHONPATH", "")
env["PYTHONDONTWRITEBYTECODE"] = "1"

print("# mutation study of z6_certified_tops.py: u = %s, J = %s, K = %s;  %d mutations + baseline" % (u_str, J, K, len(MUTS) - 1))
rows = []
base_tops = None
for mid, desc, patches in MUTS:
    text = mutate(ORIG, patches)
    head = "# MUTANT %s of z6_certified_tops.py, generated by workstream R29 (science division) for a mutation study.\n# NOT a file of the theory division.  Mutation: %s\n" % (mid, desc)
    plain = os.path.join(MUTDIR, "mut_%s.py" % mid)
    inst = os.path.join(MUTDIR, "inst_%s.py" % mid)
    open(plain, "w").write(head + text)
    open(inst, "w").write(head + instrument(text))
    out1, rc1 = run([sys.executable, "-B", os.path.join(HERE, "r29_wrap.py"), plain, u_str, J, K], env=env)
    if "ALL CHECKS PASS" in out1:
        own = "ALL CHECKS PASS"
    elif "CHECK FAILED" in out1:
        own = "CHECK FAILED"
    else:
        m = re.findall(r"R29-WRAP: target raised (\w+): ([^\n]*)", out1)
        own = ("exception %s: %s" % (m[0][0], m[0][1][:40])) if m else ("TIMEOUT" if "TIMEOUT" in out1 else "no verdict (rc %d)" % rc1)
    tops = [float(x.split("|")[1]) for x in out1.split("\n") if re.match(r"^\s*\d+ \|", x)]
    out2, rc2 = run([sys.executable, "-B", os.path.join(HERE, "r29_i1_mutworker.py"), inst, u_str, J, K], env=env)
    res = None
    for ln in out2.split("\n"):
        if ln.startswith("R29-MUT-RESULT "):
            res = ast.literal_eval(ln[len("R29-MUT-RESULT "):])
    if mid == "M00":
        base_tops = tops
    dtop = None
    wt = res["tops"] if res else []
    ref = base_tops if base_tops else []
    use = tops if tops else wt
    if ref and use:
        dtop = max(abs(x - y) / y for x, y in zip(use, ref))
    rows.append((mid, desc, own, res, dtop, len(tops)))
    open(os.path.join(MUTDIR, "out_main_%s.txt" % mid), "w").write(out1)
    open(os.path.join(MUTDIR, "out_worker_%s.txt" % mid), "w").write(out2)
    if res is None:
        print("%-5s %-88s | own: %-28s | worker: no result (rc %d)" % (mid, desc[:88], own, rc2), flush=True)
        continue
    kinds = ", ".join("%s %d" % (k, v) for k, v in sorted(res["kinds"].items())) or "-"
    print("%-5s %-88s | own: %-28s | checker violations %4d (%s)%s | truly invalid pairs %d of %d flagged | tops below envelope %d | max rel change of tops %s | levels %d"
          % (mid, desc[:88], own, res["viol"], kinds, ("; worker stopped: " + res["crashed"]) if res["crashed"] else "",
             res["pair_truly_invalid"], res["pair_flagged"], res["below_env"], ("%.1e" % dtop) if dtop is not None else "n/a", res["steps"]), flush=True)

print("#")
print("# SUMMARY (a mutation is 'caught by the script' only if its own run does not end with ALL CHECKS PASS)")
caught = [r for r in rows[1:] if r[2] != "ALL CHECKS PASS"]
notc = [r for r in rows[1:] if r[2] == "ALL CHECKS PASS"]
inv_not_caught = [r for r in notc if r[3] and (r[3]["viol"] > 0 or r[3]["below_env"] > 0 or r[3]["pair_truly_invalid"] > 0)]
harmless = [r for r in notc if r[3] and r[3]["viol"] == 0 and r[3]["below_env"] == 0 and r[3]["pair_truly_invalid"] == 0]
print("#   mutations: %d;  caught by the script itself: %d (%s)" % (len(rows) - 1, len(caught), ", ".join(r[0] for r in caught)))
print("#   NOT caught by the script but rejected by the independent checker: %d (%s)" % (len(inv_not_caught), ", ".join(r[0] for r in inv_not_caught)))
print("#   not caught and no violation found (equivalent or harmless mutants): %d (%s)" % (len(harmless), ", ".join(r[0] for r in harmless)))
b = rows[0]
print("#   baseline M00: own verdict %s; checker violations %d; tops below envelope %d" % (b[2], b[3]["viol"] if b[3] else -1, b[3]["below_env"] if b[3] else -1))
R.finish("r29_i1_mutations u=%s J=%s K=%s" % (u_str, J, K))
