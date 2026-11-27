"""Harness remark of SCI-REV-0007: the proposed change of harness test XVI.3 (HARNESS_PROPOSAL.md), applied to a COPY
of the harness and tested there.  Nothing is written to the repository.

  1. the four replacements of the proposal are applied to a copy of falsify_conjectures.py (argv[1]) in argv[2];
  2. the patched copy is run:  --only XVI.3 (quick and full),  --only XVI.4 (quick);
  3. every mutation of XVI.3 and XVI.4 of mutation_tests.py (argv[3]) is applied to the patched copy and run in quick
     mode, as the mutation runner does: caught = exit code 1 and no test ended in ERROR;
  4. for information (not part of the proposal): a Harper term with one shell too many (radius k + 1) is NOT caught by
     XVI.3 -- the certified fraction is below the true one by the factor 1 + eta, so on the landscapes of the test
     k + 1 is still at most the true radius; a test of the radius of the Harper term would need level sets with
     partial shells.

Usage: python3 h_proposal_test.py <falsify_conjectures.py> <work dir> <mutation_tests.py> [suffix of the output names]
       (in the repository:  python3 -B h_proposal_test.py ../../falsify_conjectures.py /tmp/h_proposal ../../mutation_tests.py ;
        20 s; the two harness files are only read, the patched copy and the mutants are written to the work dir)
"""
import sys, os, re, subprocess, difflib

src, work, mut_src = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
SUFFIX = sys.argv[4] if len(sys.argv) > 4 else ""
HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


EDITS = [
 # H1: keep the Markov-only value of the running bound (statistics only)
 ("                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term\n",
  "                ell_markov = max(ell, s * math.exp(-b) * pbar)                               # the bound without the Harper term (statistics only)\n"
  "                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term\n"),
 # H2: the record of a pass carries it, with the tail
 ("            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg)\n",
  "            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg, tail=tail, ell_out=ell,\n"
  "                       ell_markov=(ell_markov if pop else ell))\n"),
 # H3: the check of a run counts how often the Harper term is exercised
 ('        stats["populated" if lv["pop"] else "unpopulated"] += 1\n    stats["runs"] += 1\n    return None\n',
  '        stats["populated" if lv["pop"] else "unpopulated"] += 1\n'
  '    # how often the Harper term is exercised (a question of the Scientific Discovery Division, SCI-REV-0007): populated passes\n'
  '    # at which it raises the running bound, and runs whose closure it decides (the closing pass is populated and would fail\n'
  '    # the closure test with the bound without the Harper term)\n'
  '    seq, last = run["levels"] + [run["last"]], run["last"]\n'
  '    stats["harper_active"] = stats.get("harper_active", 0) + sum(1 for lv in seq if lv["pop"] and lv["ell_out"] > lv["ell_markov"])\n'
  '    stats["harper_decisive"] = stats.get("harper_decisive", 0) + int(last["pop"] and last["tail"] > theta * math.exp(b) * last["ell_markov"])\n'
  '    stats["runs"] += 1\n    return None\n'),
 # H4: a fixed sub-case that exercises it, and the power condition
 ('    if stats["populated"] == 0 or stats["unpopulated"] == 0 or stats["skipped"] > 0:\n'
  '        return False, dict(reason="the test has no power", **stats)\n    return True, stats\n\n\n@conjecture("XVI.4 Sample sizes',
  '    # (iii) a fixed sub-case in which the Harper term decides the closure (plateau of radius 4, then a cone of slope u): the\n'
  '    # closing pass is populated, its radius is at most r_dagger, and the closure test holds through the Harper term only --\n'
  '    # without that term the level is left and the check of the closing radius fails.  (3000 of 3000 runs over seeds and\n'
  '    # inner behaviours: experiments/coordinator_checks/nested_review_R6/h_subcase_robust.py)\n'
  '    n_o, u = 24, 0.5\n'
  '    f = u * np.maximum(np.arange(n_o + 1, dtype=float) - 4, 0.0)\n'
  '    vals, probs = np.exp(-f), np.array([math.comb(n_o, j) for j in range(n_o + 1)], dtype=float) / 2 ** n_o\n'
  '    decisive_before = stats.get("harper_decisive", 0)\n'
  '    for mode in (1, 2):\n'
  '        bad = one(vals, probs, 0.0, n_o, n_o + 2, u, dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0), mode, ("harper", mode))\n'
  '        if bad:\n'
  '            return False, bad\n'
  '    if stats.get("harper_decisive", 0) - decisive_before != 2:\n'
  '        return False, dict(reason="the fixed sub-case no longer exercises the Harper step", **stats)\n'
  '    if stats["populated"] == 0 or stats["unpopulated"] == 0 or stats["skipped"] > 0 or stats.get("harper_active", 0) == 0:\n'
  '        return False, dict(reason="the test has no power", **stats)\n    return True, stats\n\n\n@conjecture("XVI.4 Sample sizes'),
]
EXTRA_MUTATION = ("(for information, not proposed) Harper term with one shell too many (radius k + 1)",
                [("                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term",
                  "                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[min(k + 1, n_o)] / No)")], "XVI.3")


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    base = open(src, encoding="utf-8").read()
    patched = base
    for old, new in EDITS:
        assert patched.count(old) == 1, old[:80]
        patched = patched.replace(old, new)
    os.makedirs(work, exist_ok=True)
    ppath = os.path.join(work, "falsify_conjectures_proposed.py")
    open(ppath, "w", encoding="utf-8").write(patched)
    diff = "".join(difflib.unified_diff(base.splitlines(True), patched.splitlines(True), "experiments/falsify_conjectures.py", "experiments/falsify_conjectures.py (proposed)", n=2))
    open(outfile(f"h_proposal{SUFFIX}.diff"), "w", encoding="utf-8").write(diff)
    out(f"proposal applied to a copy: {len(EDITS)} replacements, diff of {len(diff.splitlines())} lines")
    ok = True
    for args in (["--only", "XVI.3", "--quick"], ["--only", "XVI.3"], ["--only", "XVI.4", "--quick"]):
        r = subprocess.run([sys.executable, "-B", ppath, *args], capture_output=True, text=True)
        for ln in r.stdout.strip().splitlines():
            if ln.startswith("["):
                tail = ln[ln.rfind("("):] if "(" in ln else ln
                out(f"  patched harness {' '.join(args)}: exit {r.returncode}; {ln[:36].strip()} ... {tail[:330]}")
        ok = ok and r.returncode == 0
    # the mutations of the runner, on the patched copy
    ns = {}
    mtext = open(mut_src, encoding="utf-8").read()
    start = mtext.index('MUTS["XVI"] = [')
    end = mtext.index("]\n", mtext.index("'XVI.3 M6")) + 2
    exec("MUTS = {}\n" + mtext[start:end], ns)
    muts = list(ns["MUTS"]["XVI"])
    for m in re.finditer(r"    \('(XVI\.4 M\d[^']*)',\n     \[\((.*?)\)\], 'XVI\.4'\),\n", mtext, re.S):
        muts.append(eval("(" + repr(m.group(1)) + ", [(" + m.group(2) + ")], 'XVI.4')"))
    caught = 0
    sel = [m for m in muts if m[2] in ("XVI.3", "XVI.4")]
    for (label, edits, only) in sel + [EXTRA_MUTATION]:
        info = label.startswith("(for information")
        s = patched
        stale = False
        for old, new in edits:
            if s.count(old) < 1:
                stale = True
            s = s.replace(old, new)
        mpath = os.path.join(work, "mutant.py")
        open(mpath, "w", encoding="utf-8").write(s)
        r = subprocess.run([sys.executable, "-B", mpath, "--only", only, "--quick"], capture_output=True, text=True)
        is_caught = (not stale) and r.returncode == 1 and "ERROR" not in r.stdout
        caught += is_caught and not info
        reason = ""
        for ln in r.stdout.splitlines():
            if "reason=" in ln:
                reason = ln[ln.index("reason="):][:150]
        out(f"  [{'caught' if is_caught else 'NOT CAUGHT' if not stale else 'STALE'}] {label}   {reason}")
        ok = ok and (is_caught or info)
    out(f"mutations caught on the patched copy: {caught} of {len(sel)}")
    out(f"proposal test passed: {ok}")
    open(outfile(f"h_proposal_test{SUFFIX}.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
