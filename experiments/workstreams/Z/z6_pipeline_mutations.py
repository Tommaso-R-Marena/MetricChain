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

Two kinds of mutation: "gross" ones make the output invalid by a margin far above rounding (relative 1e-9 or
more, or structurally) and must be rejected by (ii); "ulp" ones flip a rounding direction by a few units in the
last place — whether the output is then still a valid certificate depends on the instance, and the checker's
verdict is reported (if it accepts, it has exhibited a rational witness for every line: the output is valid).

A mutation that breaks the certificate must NOT be accepted by (ii): the checker must end with a
rejection.  (For an invalid line the checker searches long for a witness that does not exist; a run that
reaches the time limit is reported as "NO VERDICT" — it is not an acceptance, and it is counted as a
failure of this study, so that every row of the stored output is a real verdict.)  The run fails (exit
code 1) if the unmutated script is not accepted by both, or if a certificate-breaking mutation is not
rejected by (ii).

Default instance: u = 1, 4 levels, K = 40 sample points (the checker needs up to a few minutes on a mutant).
Output: out_z6_pipeline_mutations.txt
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
J = sys.argv[2] if len(sys.argv) > 2 else "4"
K = sys.argv[3] if len(sys.argv) > 3 else "40"
TLIM = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
src = open(os.path.join(HERE, "z6_certified_tops.py")).read()

# (label, [(old, new)], kind)   kind: "base" | "gross" (invalid by a margin far above rounding: must be
# rejected) | "ulp" (a rounding direction flipped: whether the OUTPUT is still a valid certificate depends on
# the instance, because the stored lines carry a margin of four units in the last place; the checker's
# verdict is reported, and either verdict is consistent with a sound pipeline)
MUTS = [
    ("M00 baseline (no mutation)", [], "base"),
    ("G01 up() rounds towards minus infinity (abar < a)",
     [("    return math.nextafter(float(x.b), INF)", "    return math.nextafter(float(x.a), -INF)")], "gross"),
    ("G02 the rate e' too small by 1e-6",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return dn(e) * (1 - 1e-6), max(0.0, up(kl_iv(r, HALF)))")], "gross"),
    ("G03 the bound of theta too small by 1e-6",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return up(e), max(0.0, dn(kl_iv(r, HALF)) * (1 - 1e-6))")], "gross"),
    ("G04 the two divergences exchanged",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return max(1e-300, up(kl_iv(r, HALF))), up(e)")], "gross"),
    ("G05 theta bounded at rho (1 + 1e-7)",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))",
       "    return up(e), max(0.0, up(kl_iv(r * (1 + iv.mpf(10) ** -7), HALF)))")], "gross"),
    ("G06 the slope of a stored line too large by 1e-6",
     [("        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))))",
       "        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))) * (1 + 1e-6))")], "gross"),
    ("G07 the intercept of a stored line too small by 1e-6",
     [("        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))))",
       "        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))) * (1 - 1e-6))")], "gross"),
    ("G08 the parent line steeper by 1e-9",
     [("        a0 = float(V.al[i_]) if i_ >= 0 else 0.0", "        a0 = float(V.al[i_]) * (1 + 1e-9) if i_ >= 0 else 0.0")], "gross"),
    ("G09 the slope of the cap line too small by 1e-6",
     [("        bL = float(Fr(m) * C - 1)", "        m = m * (1 - 1e-6)\n        bL = float(Fr(m) * C - 1)")], "gross"),
    ("G10 the top accepted with a (1 - 1e-6) in place of abar",
     [("    A = Fr(ABAR)\n    C = Fr(V.c)", "    A = Fr(ALOW) * (1 - Fr(1, 10 ** 6))\n    C = Fr(V.c)")], "gross"),
    ("U01 the rate e' rounded down (one unit in the last place)",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return dn(e), max(0.0, up(kl_iv(r, HALF)))")], "ulp"),
    ("U02 the bound of theta rounded down (one unit)",
     [("    return up(e), max(0.0, up(kl_iv(r, HALF)))", "    return up(e), max(0.0, dn(kl_iv(r, HALF)))")], "ulp"),
    ("U03 the slope of a stored line rounded up (four units)",
     [("        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))))",
       "        al_new.append(float(upw(np.float64((1.0 + th_ * a0) / e_))))")], "ulp"),
    ("U04 the intercept of a stored line rounded down (four units)",
     [("        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))))",
       "        be_new.append(float(down(np.float64(th_ * (1.0 + b0) / e_))))")], "ulp"),
]

TMP = tempfile.mkdtemp(prefix="z6-pipeline-")
bad = 0
SUMMARY = []
print("# z6_pipeline_mutations.py  u = %s, %s levels, K = %s" % (u_str, J, K))
print("# columns: mutation | verdict of the mutant's own last line | verdict of the independent checker | as required?")
for k, (label, reps, kind) in enumerate(MUTS):
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
    try:
        r1 = subprocess.run([sys.executable, "-B", os.path.join(d, "z6_certified_tops.py"), u_str, J, K, "nocompare"],
                            capture_output=True, text=True, env=env, timeout=TLIM)
        own = (r1.stdout.strip().splitlines() or ["(no output)"])[-1] if r1.returncode == 0 else "CRASH: " + (r1.stderr.strip().splitlines() or ["?"])[-1][:60]
    except subprocess.TimeoutExpired:
        own = "NO VERDICT (time limit)"
    try:
        r2 = subprocess.run([sys.executable, "-B", os.path.join(d, "review_a6", "a6_02_verify_z6_output.py"), u_str, J, K, "nocontrols"],
                            capture_output=True, text=True, env=env, timeout=TLIM)
        lines2 = r2.stdout.strip().splitlines()
        chk = lines2[-1] if (r2.returncode == 0 and lines2) else "CRASH: " + (r2.stderr.strip().splitlines() or ["?"])[-1][:60]
    except subprocess.TimeoutExpired:
        chk = "NO VERDICT (time limit %d s)" % TLIM
    accepted = chk.startswith("ALL CHECKS PASS")
    rejected = chk.startswith("FAILED") or chk.startswith("CRASH")
    if kind == "base":
        ok = accepted and own.startswith("ALL CHECKS PASS")
    elif kind == "gross":
        ok = rejected
    else:
        ok = accepted or rejected                      # a real verdict either way
    ok = ok and not stale
    SUMMARY.append((kind, own.startswith("ALL CHECKS PASS"), accepted, rejected))
    bad += not ok
    print("%-52s | %-28s | %-40s | %s" % (label, own[:28], ("accepted" if accepted else ("REJECTED: " if rejected else "") + chk[:30]), "yes" if ok else ("STALE PATTERN" if stale else "NO")), flush=True)
shutil.rmtree(TMP, ignore_errors=True)
gross = [t for t in SUMMARY if t[0] == "gross"]
ulp = [t for t in SUMMARY if t[0] == "ulp"]
print()
print("gross mutations: %d; the script's own last line still passes for %d of them; the independent checker rejects %d of them"
      % (len(gross), sum(1 for t in gross if t[1]), sum(1 for t in gross if t[3])))
print("rounding-direction mutations: %d; own last line passes for %d; the checker rejects %d and accepts %d (an accepted output IS a valid"
      " certificate: the stored lines carry a margin of four units in the last place)" % (len(ulp), sum(1 for t in ulp if t[1]), sum(1 for t in ulp if t[3]), sum(1 for t in ulp if t[2])))
print("STUDY AS REQUIRED" if bad == 0 else "%d ROWS NOT AS REQUIRED" % bad)
sys.exit(1 if bad else 0)
