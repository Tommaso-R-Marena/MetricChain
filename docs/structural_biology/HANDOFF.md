# Handoff of the Structural & Computational Biology division

*For a successor session or a human reader.  State at the **consolidation halt of 2026-11-27**
(owner's directive SB-D-3 in `OWNER_DIRECTIVES.md`).  The division is halted: **do not start
work without the research owner's explicit authorisation.**  The critical assessment is
`docs/collaboration/consolidation/structural-biology.md`; the evidence is `RESULTS.md`
(R-1 … R-13); this file is the map and the list of what was left unfinished.*

## What this division is

The seventh of eight divisions of the MetricChain programme (protocol:
`docs/collaboration/README.md`; mandate in the owner's words: `OWNER_DIRECTIVES.md`).  We write
only to `research/structural-biology`; we read the other branches and never merge them;
substantial computation is requested from the engineering division; no pull requests, releases
or publications without the owner's authorisation.

## What exists

| thing | where | state |
|---|---|---|
| exact pairwise model, instance files | `src/metricchain_sb/model.py`, `modelio.py` | tested |
| `min` certificates: format `structbio-mincert/1`, strict loader, converter to the theory division's `metricchain-cert/1` | `mincert.py` | tested; attacked by three reviews |
| independent exact checker (C1) | `mincheck.py` | rule semantics = theory kernel `verify` [V]; implementation tested, **not** formally verified |
| producer (dead-end elimination, MPLP dual bound, branch and bound; `eliminate=False` gives the null method) | `gmec.py` | untrusted by design; slow (Python loops) |
| certified gaps: leaving a state, leaving a rotamer well; optimality in every table within an entrywise error | `stability.py` | tested against the definition |
| certified exponential; interval tables (exact and outward-rounded float tiers) | `expo.py`, `itables.py` | tested; float tier under assumptions F1–F3 (stated, not proved) |
| Z certificates: format `structbio-zcert/1`, checker, producer with conditioning, state weights (C2) | `zcert.py`, `zcheck.py`, `partition.py` | tested against 60-digit enumeration in two tiers and 40 000 adversarial certificates |
| Lean: rule semantics of the Z checker (19 theorems) and our own axiom audit | `proofs/StructBio/FactorElimination.lean`, `AxiomAudit.lean` | builds; standard axioms only; not reviewed by the theory division |
| molecular layer: structure → rotamer model → tables; models `v1` (retired), `v2`, `v2-lib`; deterministic hydrogens; rotamer wells and torsion-space shares | `molecular/` | validated numerically against an independent OpenMM system; hydrogen rule tested against a force-field minimum |
| baseline | `baselines/toulbar2.py` | toulbar2 on the identical integer instance |
| experiments (drivers, rows, expectations written before runs) | `experiments/structbio/`: `gmec_dev` (SB-X-001), `gmec_synth` (-002), `flipgaps_dev` (-003, model v1), `lnz_dev` (-004), `seed_dev` (-005), `wellgaps_dev` (-006), `nullmethod_dev` (-007), `regime_dev` (-008) | rows in each `results.jsonl`; `min` certificates in `gmec_dev/certs/` (v1), `certs/v2/`, `certs/v2-lib/` |
| reviews | `docs/structural_biology/reviews/STRUCTBIO-REV-0001.md`; intake reports in `intake/` (first synchronisation; `SYNC4_REPORT.md`) | — |

## The scientific state in one paragraph

On six public structures (four proteins) the exact minimum of a fixed-backbone rotamer table
is certified in seconds and equals the optimum of toulbar2, which is 6 to 27 times faster; the
plain linear relaxation is tight on every one of these instances, so the certificate is in
substance an LP dual.  Certified margins show that the model holds rotamer wells by kcal/mol
and states by tenths, and that the minimiser does not survive a table error of 0.01 kcal/mol
per entry.  For crambin, `ln Z` and all rotamer populations are enclosed with a guarantee
(0.0075 nats; 0.024); for larger proteins this stops.  The first model had a seed worth 13 to
25 kcal/mol and was retired.  Every number is a property of a crude model (in vacuo, `ε = 4r`,
rigid ideal rotamers, hydrogens by rule); nothing has been compared with experiment and
nothing has been run on held-out structures.

## How to verify what we state

```
python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt
~/.venvs/structbio/bin/python -m pytest tests/structbio -q
~/.venvs/structbio/bin/python experiments/structbio/gmec_dev/run.py --check      # rebuilds 18 instances, re-checks the stored certificates (about 3 min)
python3 experiments/reference_checker.py --selftest --quick                       # the theory division's checker, unmodified
lake exe cache get && lake build proofs.StructBio.AxiomAudit                      # Lean 4.31.0, Mathlib v4.31.0; prints the axioms of our 19 theorems
```

Drivers take `--model v1|v2|v2-lib` (`gmec_dev/run.py`, `lnz_dev/run.py`, `wellgaps_dev/run.py`);
the rows of 2026-11-26 are on `v1`.  Every driver states its expectations in its docstring and
records the commit of the code in memory at process start.

## Rules a successor must keep

1. Development structures are a closed list (`BENCHMARK_MASTER_PLAN.md` rule 0.2); do not look
   at others; do not open the Frontier division's sealed list; do not choose a held-out list.
2. A certified number is published with its four-line error budget and its label; "[CK]"
   means rule semantics machine-checked and *our implementation tested* — never "formally
   verified software".
3. Test first, and watch every regression test fail against the defect it is for.
4. A correction is a new linked entry; nothing published is rewritten.
5. Expectations and decision rules are committed before a run; a message's header time is read
   from the clock before its commit.
6. No Modal, no paid service, no CASP17 reference data.

## Unfinished work, with what is needed to resume each item

1. **Checker repair after STRUCTBIO-REV-0001.**  In progress at this commit (a fixer subagent is repairing the 19 findings; 59 adversarial tests fail on purpose until its changes are reviewed and committed).  This item is rewritten in the final commit of the halt.
2. **Tighter population intervals (not started; specified here).**  Today
   `p_lo(a) = L_a / Z_hi`, `p_hi(a) = 1 − Σ_{b≠a} p_lo(b)`, so every state's interval has width
   about `1 − exp(−w)` (`w` = width of `ln Z`).  Better: let every node return, for each state
   `a` of the kept site `t` still present after its own steps, a lower end `L_a` and an upper
   end `H_a` of `Z_a = Σ_{x: x_t = a} w(x)`, and an upper bound `Rem` on the total weight of the
   kept states its own steps removed.  Leaf: ends of the final interval table over `t` times
   the node's factors from steps at other sites (lower: `Π exp(−β r_hi)`; upper:
   `Π exp(−β r_lo) · Π(1+ρ)`).  A prune of kept state `r` at step `k`: by the total rule on the
   box at that step `Z_r ≤ ρ_k · Z(box after the step)`, hence `Rem ≤ (Σ_k ρ_k) · F_all · Σ_a H_a`
   with `F_all` the product of all upper factors.  Branch on a site other than `t`:
   `L_a = Σ_children L_a` (children where `a` survives), `H_a = Σ_children (H_a, or the child's
   Rem where it removed a)`.  Top: `p(a) ∈ [L_a / (L_a + Σ_{b≠a} H_b + Rem),
   H_a / (H_a + Σ_{b≠a} L_b)]`; removed states: `p ≤ Rem / (Rem + Σ_b L_b)`.  Each step is an
   instance of a theorem of `FactorElimination.lean` on the box with `t` pinned, plus
   monotonicity of `x/(x+y)`.  Expected width about `2w·p(1−p)`.  Change is confined to
   `zcheck.evaluate` and the final assembly; test against enumeration with prunes on the kept
   site, relaxations and branches.
3. **A standalone format and semantics note** from which a second checker can be written
   (asked for by Engineering, ENG-RES-0018 §3): not written.  The specification of record is
   the docstrings of `mincert.py`, `mincheck.py`, `zcert.py`, `zcheck.py`, `itables.py`,
   `expo.py`, including the documented limits.
4. **Freeze record for held-out evaluation** (Frontier's sequence, FRONTIER-MSG-0002 §2): not
   issued.  It would name: a commit at or after this checkpoint, `MODELS["v2"]` and
   `MODELS["v2-lib"]` and `SCALE_BITS = 20` of `experiments/structbio/gmec_dev/run.py`, the
   library of `molecular/rotamers.py`, hypotheses H3a–H3f and H6-BM6 of
   `BENCHMARK_MASTER_PLAN.md`.  A held-out run must ship the integer instance with each
   certificate (`modelio.save_model`): bit-for-bit rebuilding has only been tested on one
   machine (SB-OP-15).
5. **Runs not made or not finished.**  SB-X-006 on ubiquitin
   (`wellgaps_dev/run.py 1UBQ --b-kcal 0.01 --time-limit 120`: about 260 certified
   minimisations of about 45 s); the gap rows of 2IGD (running at this commit); SB-X-004 at threshold 0.0001 on crambin
   (stopped by a command time limit); the necessary-optimality run with `b` = the spread over
   seeds (`seed_dev/1CRN_entry_spread.npz`; outcome not in doubt, not computed); SB-BM-7.
6. **Baselines not run.**  Pseudo-Boolean proof logging (VeriPB/CakePB) on an encoding and on
   a translation of our own derivation; exact SCIP with VIPR; toulbar2's `Z*ε`; the CPOG
   composition for `Z`; uncertified marginals against certified intervals.
7. **Producer speed** (the shortest path to useful performance): vectorise or compile the dual
   sweeps of `gmec._Dual` (a Python loop over pairs), start from the optimum toulbar2 returns
   (`certify_gmec(..., witness=x, eliminate=False, max_nodes=1)` is the null method, exact on
   12 of 12 development instances), avoid the `k_i² k_j` arrays of `dead_end_elimination` on
   large state sets.  Development instances for this: the ten public instances of the
   Frontier pilot (FRONTIER-REQ-0001), on which our producer abstained six times.
8. **Requests** STRUCTBIO-REQ-0001 and -REQ-0004 (Engineering) are unanswered and were written
   for model v1; re-issue for `v2`/`v2-lib` before anything is run.
9. **Not started:** capabilities C3 (ensemble identification) and C4 (geometric observability);
   the other divisions' interface documents are named in `intake/SYNC4_REPORT.md` §1.4–1.5.

## Open requests and where their answers are

| ours | to | state |
|---|---|---|
| STRUCTBIO-REQ-0001 | Engineering | unanswered; Engineering reviewed our first commit on its own initiative (ENG-RES-0018) |
| STRUCTBIO-REQ-0002 | Science | answered by SCI-REV-0026; our response STRUCTBIO-RES-0003 |
| STRUCTBIO-REQ-0003 | Theory, Complexity | Q-5 answered by COMPLEXITY-RES-0010; rules R-1 … R-4 closed by our own Lean file; Theory has not answered |
| STRUCTBIO-REQ-0004 | Engineering | unanswered |

Answers arrive only by fetching the other branches; there are no notifications, and under
SB-D-3 nothing is to be acted on without the owner's authorisation.

## Processes at the halt

At this commit: one fixer subagent (checker repair) and one local run (SB-X-006 on 2IGD) are still active.  This section is rewritten in the final commit of the halt.
