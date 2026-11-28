#!/usr/bin/env python3
"""z6_pipeline_mutations.py [u] [levels] [K]  --  what is evidence for the certified tops, and what is not.

Finding F1 of the science division's review SCI-REV-0030 (workstream R29): the last line of
`z6_certified_tops.py` ("ALL CHECKS PASS") tests only that the tops are nonincreasing and above h; it
cannot fail for the errors a certificate must exclude.  The validity of a run is established by the
independent exact checker `review_a6/a6_02_verify_z6_output.py` (written by the referee of the
addendum; shares no code with the script).  This file measures both statements:

  for each textual mutation of z6_certified_tops.py (a copy in a scratch directory; the repository
  file is never modified), run  (i) the mutant's own main(), and  (ii) the independent checker on the
  mutant's output, and record the two verdicts.

A mutation that breaks the certificate must be REJECTED by (ii).  The run fails (exit code 1) if the
unmutated script is not accepted by both, or if a certificate-breaking mutation is accepted by (ii).

Default instance: u = 1, 6 levels, K = 300 sample points (about 25 s per mutant).
Output: out_z6_pipeline_mutations.txt
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
J = sys.argv[2] if len(sys.argv) > 2 else "6"
K = sys.argv[3] if len(sys.argv) > 3 else "300"
src = open(os.path.join(HERE, "z6_certified_tops.py")).read()

# (label, [(old, new)], breaks the certificate?)
MUTS = [
    ("M00 baseline (no mutation)", [], False),
    ("M01 up() rounds towards minus infinity",
     [("    return math.nextafter(float(x.b), INF)", "    return math.nextafter(float(x.a), -INF)")], True),
    ("M04 the rate e' rounded down",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return dn(e), max(0.0, up(kl_iv(r, HALF)))")], True),
    ("M05 the bound of theta rounded down",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return up(e), max(0.0, dn(kl_iv(r, HALF)))")], True),
    ("M18 the two divergences exchanged",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return max(1e-300, up(kl_iv(r, HALF))), up(e)")], True),
    ("M22 theta bounded at rho (1 + 1e-7)",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))",
       "    return up(e), max(0.0, up(kl_iv(r * (1 + iv.mpf(10) ** -7), HALF)))")], True),
    ("M07 the slope of a stored line rounded up",
     [("        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))))",
       "        al_new.append(float(upw(np.float64((1.0 + th_ * a0) / e_))))")], True),
    ("M08 the intercept of a stored line rounded down",
     [("        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))))",
       "        be_new.append(float(down(np.float64(th_ * (1.0 + b0) / e_))))")], True),
    ("M21 the parent line steeper by 1e-9",
     [("        a0 = float(V.al[i_]) if i_ >= 0 else 0.0", "        a0 = float(V.al[i_]) * (1 + 1e-9) if i_ >= 0 else 0.0")], True),
    ("M10 the slope of the cap line too small by 1e-6",
     [("        bL = float(Fr(m) * C - 1)", "        m = m * (1 - 1e-6)\n        bL = float(Fr(m) * C - 1)")], True),
    ("M15 the top accepted with a lower bound of a",
     [("    A = Fr(ABAR)\n    C = Fr(V.c)", "    A = Fr(ALOW) * (1 - Fr(1, 10 ** 6))\n    C = Fr(V.c)")], True),
]

TMP = tempfile.mkdtemp(prefix="z6-pipeline-")
bad = 0
print("# z6_pipeline_mutations.py  u = %s, %s levels, K = %s" % (u_str, J, K))
print("# columns: mutation | verdict of the mutant's own last line | verdict of the independent checker | as required?")
for k, (label, reps, breaks) in enumerate(MUTS):
    text = src
    stale = False
    for old, new in reps:
        if text.count(old) != 1:
            stale = True
        text = text.replace(old, new)
    d = os.path.join(TMP, "m%02d" % k, "Z")
    os.makedirs(os.path.join(d, "review_a6"))
    open(os.path.join(d, "z6_certified_tops.py"), "w").write(text)
    for f in ("a6_02_verify_z6_output.py", "a6exact.py", "a6lib.py"):
        shutil.copy(os.path.join(HERE, "review_a6", f), os.path.join(d, "review_a6", f))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1")
    r1 = subprocess.run([sys.executable, "-B", os.path.join(d, "z6_certified_tops.py"), u_str, J, K, "nocompare"],
                        capture_output=True, text=True, env=env, timeout=1200)
    own = (r1.stdout.strip().splitlines() or ["(no output)"])[-1] if r1.returncode == 0 else "CRASH: " + (r1.stderr.strip().splitlines() or ["?"])[-1][:60]
    r2 = subprocess.run([sys.executable, "-B", os.path.join(d, "review_a6", "a6_02_verify_z6_output.py"), u_str, J, K, "nocontrols"],
                        capture_output=True, text=True, env=env, timeout=1200)
    lines2 = r2.stdout.strip().splitlines()
    chk = lines2[-1] if (r2.returncode == 0 and lines2) else "CRASH: " + (r2.stderr.strip().splitlines() or ["?"])[-1][:60]
    accepted = chk.startswith("ALL CHECKS PASS")
    ok = (not stale) and ((accepted and own.startswith("ALL CHECKS PASS")) if not breaks else (not accepted))
    bad += not ok
    print("%-52s | %-28s | %-34s | %s" % (label, own[:28], ("accepted" if accepted else "REJECTED: " + chk[:24]), "yes" if ok else ("STALE PATTERN" if stale else "NO")), flush=True)
shutil.rmtree(TMP, ignore_errors=True)
n_break = sum(1 for m in MUTS if m[2])
print()
print("%d certificate-breaking mutations; the independent checker must reject every one of them: %s" % (n_break, "it does" if bad == 0 else "%d rows not as required" % bad))
sys.exit(1 if bad else 0)
