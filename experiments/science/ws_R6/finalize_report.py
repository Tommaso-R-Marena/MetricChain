"""
finalize_report.py -- workstream R6: put the final run counts (from data/summary_all.json, produced by make_section3.py) into
sections 0, 1, 2.7 (m6), 5 and 8 of the report.  Run AFTER fill_report.py.  Every replaced passage is asserted to be present.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "..", "..", "..", "docs", "science", "workstreams", "R6_REPORT.md")
S = json.load(open(os.path.join(HERE, "data", "summary_all.json")))


def g(name, key):
    return S.get(name, {}).get("S", {}).get(key, 0)


A = ["A_small", "A_ties", "A_medium"]
v2lp = sum(g(n, "runs") for n in A)
v2l = g("D_2L", "runs")
valid = v2lp + v2l
redK = g("B_reducedK", "runs")
inval = g("B_invalid", "runs") + g("B_lazy", "runs")
off2l = g("D_2L_off", "runs")
total = valid + redK + inval + off2l
runs_2l = v2l + off2l
runs_2lp = v2lp + redK + inval
e1, e16, th, cc = S.get("e2e_K1", {}), S.get("e2e_K16", {}), S.get("three", {}), S.get("capcorner", {})
adv_total = sum(r["evaluations"] for r in S.get("adversarial", []))
LZ = S.get("B_lazy_split", {})
lazy_cost, lazy_runs = LZ.get("steep_abort_cost", 0), LZ.get("steep_runs", 0)
close_pop_A = sum(g(n, "close_pop") for n in A)
closed_A = sum(g(n, "closed") for n in A)
e2e_runs = e1.get("runs", 0) + e16.get("runs", 0)

s = open(REPORT).read()


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new)


rep("""* **Not done**: three nested levels with real inner brackets; a run with real inner brackets at sizes
  where sampling is cheaper than enumeration (impossible with the constants of the theorems below
  `n ≈ 10³`, see §5); Theorem 11.51; a second reading of the lower bound's asymptotics.""",
    f"""* **Done only at toy size**: runs with real inner brackets — two levels on cubes of 12–13 coordinates
  ({e2e_runs} runs), three nested levels on cubes of 9–10 coordinates ({th.get('outer_runs', 0)} outer runs); they test the logic of
  the nesting, not the cost (§3.4, §5).
* **Not done**: a run with real inner brackets at sizes where sampling is cheaper than enumeration
  (impossible with the constants of the theorems); Theorem 11.51; a second reading of the lower
  bound's asymptotics; the Lean proofs line by line.""")

rep("""independent implementation violated no claim in **5 930 literal runs** with the constants of the theorems
— including, for the first time, **1 020 runs with invalid inner answers** (the statements "for every run,
on or off the good event" hold there, and the abort rule keeps the cost below `C_max`), the algorithm
of Theorem 11.52 itself at sizes where levels are left as negligible, and 1 200 runs with real
two-sample inner brackets (§3) — and it reproduces to every published digit numbers of the engineering
division that I had not seen when I wrote it (§3.3).  **What I add:** (i) seven minor findings, each
with its repair (§2.7); the only one that touches a proof is an uncovered pass in the new cap remark of
`40c5bd7`, which I close (§2.8); (ii) an **every-`n` statement with no `o(n)`**""",
    f"""independent implementation violated no claim in **{total:,} literal runs** of Algorithms 2L⁺ and 2L with a
simulated inner oracle — {valid:,} with the constants of the theorems and valid inner answers (the events
of the proof never failed, every bracket was valid), {redK} with `K` reduced, and, for the first time,
**{inval + off2l} runs off the good event by design, {inval} of them with invalid inner answers** (the statements
"for every run, on or off the good event" hold there; with a dear last rung {lazy_cost} of {lazy_runs} such runs
would exceed `C_max` without the abort rule, and none does with it) — nor in {e2e_runs} two-level and
{th.get('outer_runs', 0)} three-level runs with real inner brackets at toy size, nor in {cc.get('runs', 0):,} runs aimed at the degenerate
branch of the new cap remark (§3); and it reproduces to every published digit numbers of the
engineering division that I had not seen when I wrote it (§3.3).  **What I add:** (i) seven minor
points, each with its repair (§2.7): four gaps in the text of §11.18, an uncovered pass in the proof of
the new cap remark of `40c5bd7`, which I close (§2.8), and two observations; (ii) an **every-`n` statement
with no `o(n)`**""")

rep("""| Theorem 11.52 (one more level; Algorithm 2L) | **proved** (four minor gaps, all closed: m1–m4) | own derivation before reading; 2 400+ own runs of 2L |""",
    f"""| Theorem 11.52 (one more level; Algorithm 2L) | **proved** (four minor gaps, all closed: m1–m4) | own derivation before reading; {runs_2l} own runs of 2L |""")
rep("""| Theorem 11.56 = K1 (Algorithm 2L⁺) | **proved** | Steps 4–7 derived before reading, 1–3, 8, 9 after; 3 500+ own runs |""",
    f"""| Theorem 11.56 = K1 (Algorithm 2L⁺) | **proved** | Steps 4–7 derived before reading, 1–3, 8, 9 after; {runs_2lp:,} own simulated-oracle runs, {e2e_runs} with real inner brackets |""")

rep("""  should report how many populated passes had `min{Γ̃/c_η, Γ″} ≤ θ` decided by `Γ″`.  (In my campaigns:
  §3.2.)""",
    f"""  should report how many populated passes had `min{{Γ̃/c_η, Γ″}} ≤ θ` decided by `Γ″`.  (My own records
  do not: in the valid 2L⁺ campaigns {close_pop_A} of {closed_A} closures happen at a populated pass, and I did
  not log which of the two terms decided them.)""")

rep("""1. **Three or more nested levels, end to end.**  My runs with real inner brackets are two-level, on
   cubes of 12–13 coordinates, where 2L⁺ can only be tested for logic (an inner bracket costs more than
   enumerating its fibre).""",
    f"""1. **Three or more nested levels, end to end.**  My runs with real inner brackets are on cubes of
   12–13 coordinates (two levels) and 9–10 coordinates (three levels, {th.get('outer_runs', 0)} outer runs), where the
   algorithm can only be tested for logic (an inner bracket costs more than enumerating its fibre).""")

rep("""shown §3.2: with an invalid inner behaviour and a dear last rung the run *does* exceed the budget
   unless it is stopped, in 33 of 60 runs.""",
    f"""shown §3.2: with an invalid inner behaviour and a dear last rung the run *does* exceed the budget
   unless it is stopped, in {lazy_cost} of {lazy_runs} runs.""")

rep("""  behaviour that returns the rung-0 bracket at every rung but the last (so that every refined point
  reaches the dearest rung) and rung costs growing by `e^{80}`, 33 of my 60 runs stop on the query
  budget,""",
    f"""  behaviour that returns the rung-0 bracket at every rung but the last (so that every refined point
  reaches the dearest rung) and rung costs growing by `e^{{80}}`, {lazy_cost} of my {lazy_runs} runs stop on the query
  budget,""")

rep("""uses nothing else — but a referee will note that the composition of three levels has been
   exercised only on `Q_9`, `Q_10` (R8) and at the flat instance.""",
    f"""uses nothing else — but a referee will note that the composition of three levels has been
   exercised only on `Q_9`, `Q_10` (R8; here: {th.get('outer_runs', 0)} outer runs, §3.4) and at the flat instance (R8).""")

open(REPORT, "w").write(s)
print("finalised: total", total, "valid", valid, "(2L+", v2lp, ", 2L", v2l, ") reducedK", redK, "invalid", inval, "2L off", off2l,
      "| e2e", e2e_runs, "| three", th.get("outer_runs"), "| capcorner", cc.get("runs"), "| adversarial", adv_total, "| lazy", lazy_cost, "/", lazy_runs)
