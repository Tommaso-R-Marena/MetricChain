# Handoff of the Structural & Computational Biology division

*For a successor session or a human reader.  State at the second checkpoint, 2026-11-26.  The
recovery point with exact next steps is `RESEARCH_LOG.md`, "Resume here"; this file is the
map.*

## What this division is

The seventh of eight divisions of the MetricChain programme (table and protocol:
`docs/collaboration/README.md`).  Mandate, in the owner's words: `OWNER_DIRECTIVES.md`.  We
write only to `research/structural-biology`; we read the other branches and never merge them;
substantial computation is requested from the engineering division; no pull requests,
releases or publications without the owner's authorisation.

## What exists

| thing | where | state |
|---|---|---|
| exact pairwise model, instance files | `src/metricchain_sb/model.py`, `modelio.py` | tested |
| `min` certificates: format, converter to `metricchain-cert/1` | `mincert.py` | tested |
| independent checker | `mincheck.py` | tested against enumeration and the theory division's reference checker; not formally verified; reports whether the root box is full |
| certified flip gaps (C1b) | `stability.py` | tested; development results R-6 |
| certified exponential, interval tables | `expo.py`, `itables.py` | tested against 80-digit references; the float tier is rigorous under stated IEEE-754 assumptions |
| Z certificates, checker, producer (C2, first version) | `zcert.py`, `zcheck.py`, `partition.py` | tested against 60-digit enumeration in two tiers; no conditioning, no file format; rule semantics [P] beyond two neighbours |
| producer (dead-end elimination, MPLP dual bound, branch and bound) | `gmec.py` | untrusted by design; adequate on real structures, slow on frustrated synthetic ones |
| molecular layer (public structure → rotamer model → tables) | `molecular/` | validated numerically against an independent OpenMM system |
| baseline | `baselines/toulbar2.py` | toulbar2 on the identical integer instance |
| experiments | `experiments/structbio/gmec_dev/` (SB-X-001), `gmec_synth/` (SB-X-002, quick grid), `flipgaps_dev/` (SB-X-003), `lnz_dev/` (SB-X-004) | rows in each `results.jsonl`; `min` certificates in `gmec_dev/certs/` |
| documents | `docs/structural_biology/` | see the index in `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` |

## The one-paragraph scientific state

A certified global minimum of a fixed-backbone rotamer model is achievable on real structures
(six of six development structures, zero gap, seconds) and agrees with an established exact
solver, which is faster.  Certified flip gaps then show what that minimum is worth: it is
unique and survives rounding, and it is one of very many nearly degenerate configurations
(second-best within 0.004–0.11 kcal/mol).  A first checked enclosure of `ln Z` exists for
crambin (1.36 nats wide).  Certified partition functions on whole proteins are blocked at the size
of ubiquitin by dense weak couplings; the obstruction is measured and a precise question is
with the theory division.  Every number is model-conditional, and the model (in vacuo,
`ε = 4r`, rigid rotamers) is crude: it puts ubiquitin's side chains 139 kcal/mol below the
deposited conformation.

## How to verify what we state

```
python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt
~/.venvs/structbio/bin/python -m pytest tests/structbio -q
~/.venvs/structbio/bin/python experiments/structbio/gmec_dev/run.py --check
python3 experiments/reference_checker.py --selftest --quick        # the theory division's checker, unmodified
```

## Rules a successor must keep

1. Development structures are a closed list (`BENCHMARK_MASTER_PLAN.md` rule 0.2); do not look
   at others, and do not choose the held-out list.
2. A certified number is published with its four-line error budget and its label; "[CK]"
   means rule semantics machine-checked elsewhere and *our implementation tested* — never
   "formally verified software".
3. Test first, and watch every regression test fail against the defect it is for
   (`DEAD_ENDS.md` SB-DEF-04).
4. A correction is a new linked entry; nothing published is rewritten.
5. No Modal, no paid service, no CASP17 reference data.

## Open requests (ours)

STRUCTBIO-REQ-0001 (engineering), -0002 (science), -0003 (theory, complexity): all "proposed".
Answers arrive only by fetching the other branches; there are no notifications.
