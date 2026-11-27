```
Message ID:                  ENG-RES-0007
Message type:                Response to a computational request (linked update of ENG-RES-0002)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         see the commit that adds this file (checkpoint 2 of the engineering branch)
Priority:                    High
Status:                      In progress (THY-REQ-0002 as a whole); the parts reported here are completed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517 (definitions); implementation: the commit that adds this file
Related theorem or experiment: theory report §11.17, Proposition 11.49(a); P_REPORT §§0, 3.3; engineering experiment X-002, X-004
Related message/request IDs: THY-REQ-0002; ENG-RES-0002 (updated in place by this checkpoint); ENG-REQ-0001
Request being answered:      THY-REQ-0002 (exact chain covering beyond twelve torsions)
```

# THY-REQ-0002, update: lattice covers complete to 24 torsions; the generic chain reproduced and extended

> **Linked correction (added at checkpoint 4; the text below is as published):** ENG-MSG-0004 §4, item 3 — the lower end of an open bracket is a
> certified bound *or, where larger, the solver's bound at its time limit*; the stored file does not say which, and the covers of the off-lattice
> chain are not stored.  No number changes.  And a restriction: no off-lattice computation at 13 torsions or beyond in floating point
> (SCI-REV-0008, finding M2; ENG-RES-0013 §5).

## 1. What changed in ENG-RES-0002 (so that nothing is rewritten silently)

ENG-RES-0002 was published at commit `206fd9e` with covers up to 19 torsions.  Its tables are
generated from the stored artifacts (`experiments/eng/chain_cover/make_tables.py`), and at this
checkpoint they were regenerated:

* cover table: rows `n = 20…24` added (job M-005); nothing in rows `n ≤ 19` changed;
* entropy table: rows `n = 20, 22, 24` added;
* single-flip table: unchanged;
* prose: the readings of §2 now quote the sequences through `n = 24`; "at most 7" for
  `L = 1/5` became "at most 8" (the entry 8 appears at `n = 22`); "quadratic" at fixed
  accuracy became "quadratic or slightly faster" (the bracket at 27 beads is `[80, 92]`,
  i.e. `0.110–0.126·N²`); the status table was brought up to date.  No finding was withdrawn.
* header times of all messages of checkpoint 1 were set to the publication time of that
  commit (some drafting times in the headers were later than the commit; the same
  correction you made at `b12a6c5`).
* ENG-REQ-0001: "still growing at 21 beads" became "27 beads" (one sentence; the request is
  otherwise as published).

## 2. Lattice chain, 19–24 torsions (question 1) — still no saturation

At extensive accuracy (`L = 1`), every value a solver-proved optimum unless bracketed:

| `n` | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|
| `N` (beads) | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
| `N^P_cov(ε = N/2)` | 10 | 11 | 12 | 13 | 13 | 13 | 14 | 15 |
| `N^P_cov(ε = N/4)` | 17 | 19 | 22 | 24 | 23 | 26 | [27, 29] | [28, 31] |

(Complete table in ENG-RES-0002 §2.  The dip 24 → 23 is the integer radius: `⌊23/4⌋ = 5`,
`24/4 = 6`.)  The growth continues at the same rate up to 27 beads — about one evaluation
per two torsions at `ε = N/2`, one per torsion at `ε = N/4`.  The stopping rule of the
request (constant over four consecutive sizes, or more than a day of compute) is not met:
enumeration of 24 torsions took two core-hours, and the limiting factor is now the integer
programmes at *fixed* accuracy, not the enumeration.  We stop extending the lattice here:
by the finite-size argument of ENG-RES-0002 §3 two or three more sizes would not change the
picture, and the informative next object is the limit shape (ENG-REQ-0001).

## 3. Generic (off-lattice) chain (questions 1 and 3) — replication and first extension

*Model* (`P_REPORT.md` §0, "gen"): bond length 1, bond angle 111°, torsions 180°/±60°, hard
core `s_pq ≥ 3` for `q − p ≥ 3`, cutoff `S_c = 16`, homopolymer, known part `#gauche`, zero
residual.  Implementation: `src/metricchain_eng/chains/generic_chain.py` (independent, from
the definition; internal coordinates; profile classes = equal sorted truncated squared
distances after rounding to 8 decimals; profile distance = `ℓ¹` distance of the sorted
truncated distances, Proposition 2 of the workstream report).

*Replication* **[R]**, all identical to `P_REPORT.md` §§0, 3.2, 3.3:

| check | published | obtained |
|---|---|---|
| 1–4 squared distances | 6.433 (`t`), 3.819 (`g`) | 6.433, 3.819 |
| conformations, `n = 5…10` | 99, 239, 577, 1 393, 3 363, 8 115 | identical |
| profile classes, `n = 5…10` | 30, 60, 136, 291, 639, 1 360 | identical |
| `N^P_cov`, `(L=1, ε=0)`, `n = 5…9` | 27, 48, 92, 137, 215 | identical |
| `N^P_cov`, `(L=1, ε=N/2)`, `n = 5…9` | 9, 15, 21, 34, 43 | identical |
| `N^P_cov`, `(L=1/5, ε=0)`, `n = 5…10` | 5, 5, 6, 9, 11, 13 | identical |
| conformations and classes, `n = 12` | 47 141 and 6 137 | identical |
| `N^P_cov`, `(L=1, ε=0)`, `n = 10` | bracket `[318, 319]` | **319** (optimality proved by the solver) |
| `N^P_cov`, `(L=1, ε=N/2)`, `n = 10` | bracket `[58, 62]` | **60** (optimality proved by the solver) |

*Results* **[X\*]** (floating-point cover relation with tolerance `10⁻⁹`; single numbers are
HiGHS-proved optima or certified, brackets are `[certified lower bound, verified cover]` with
90 s per integer programme for `n ≥ 10`; "nearest tie" is the smallest distance of an
off-diagonal comparison from equality, discussed below the table):

<!-- TABLE:generic -->
| `n` | `N` | conformations | classes | `L=1`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | `L=1/5`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | nearest tie |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 8 | 99 | 30 | 27 | 23 | 26 | 23 | 19 | 9 | 5 | 3 | 4 | 3 | 2 | 2 | 5.2e-04 |
| 6 | 9 | 239 | 60 | 48 | 43 | 46 | 43 | 29 | 15 | 5 | 4 | 5 | 4 | 3 | 2 | 2.7e-04 |
| 7 | 10 | 577 | 136 | 92 | 66 | 82 | 66 | 44 | 21 | 6 | 5 | 6 | 5 | 3 | 2 | 1.2e-04 |
| 8 | 11 | 1 393 | 291 | 137 | 97 | 115 | 94 | 59 | 34 | 9 | 6 | 7 | 5 | 4 | 3 | 1.8e-05 |
| 9 | 12 | 3 363 | 639 | 215 | 147 | 176 | 141 | 86 | 43 | 11 | 7 | 8 | 7 | 4 | 3 | 4.5e-06 |
| 10 | 13 | 8 115 | 1 360 | 319 | 223 | 255 | [209, 211] | [119, 123] | 60 | 13 | 8 | 10 | 8 | 5 | 3 | 3.2e-07 |
| 11 | 14 | 19 559 | 2 908 | [474, 484] | [339, 350] | [379, 392] | [308, 319] | [168, 179] | [85, 90] | 16 | 10 | 11 | 10 | 6 | 4 | 1.8e-15 |
| 12 | 15 | 47 141 | 6 137 | [757, 788] | [552, 595] | [605, 645] | [484, 526] | [251, 284] | [109, 136] | 21 | 13 | 15 | 11 | 6 | 4 | 2.9e-08 |
<!-- /TABLE:generic -->

*Is the floating-point cover relation trustworthy?*  (`results/generic_Sc16_ties.json`.)  The
rounding error of a profile distance is of order `10⁻¹³`.  For `n = 8, 9, 10, 12` no comparison
is closer to equality than `1.8·10⁻⁵`, `4.5·10⁻⁶`, `3.2·10⁻⁷`, `2.9·10⁻⁸` — five orders of magnitude
above the rounding error — so the relation does not depend on the tolerance.  At `n = 11`
there are **five exact ties** (to `6·10⁻¹⁴`), all at `L = 1`, `ε = N/2 = 7`: profile distances
that equal an integer, e.g. `12.999999999999998` against `gmin + ε = 13`.  They are counted as
covered (equality satisfies the cover condition); the bracket of that one cell is for this
reading.  Distinct classes are never closer than 0.035 to each other, so class identity
does not depend on the rounding to 8 decimals either.  (That sums of differences of
squared distances of this "generic" chain can be exact integers is itself a small
observation; we did not pursue it.)

Readings.

* **Off-lattice the growth at extensive accuracy is geometric at these sizes**, not linear:
  `ε = N/2`: 9, 15, 21, 34, 43, 60, then between 85 and 90, then between 109 and 136, for
  `n = 5…12` (a factor 1.3–1.7 per torsion, and the lower ends alone give 1.3–1.4 for the
  last two steps); `ε = N/4`: 19, 29, 44, 59, 86, then `[119, 123]`, `[168, 179]`, `[251, 284]`.
  This is the workstream's observation ("×1.5–1.9 per torsion" at `ε = 0`), now seen at
  extensive accuracy as well, two sizes further (`n = 11`: 19 559 conformations, 2 908
  classes — not in the workstream's tables), and with the columns `ε = 1, N/20, N/10, N/4`
  that were not there.
* **The contrast with the lattice is a feature count, not a geometry effect.**  On the
  lattice the profile has three degrees of freedom whatever the chain length; off-lattice
  the number of distinct distances below the cutoff grows with the chain, and with it the
  dimension of the set that must be covered.  That is the content of the workstream's
  "span cost ∝ features, first-order cost ∝ exp(features)", and these data are consistent
  with it at every accuracy in the table.
* With `L = 1/5` the numbers are small and grow by one to two evaluations per torsion at
  `ε = 0`.
* Hard-core decisions are not tolerance-dependent at these sizes: the closest accepted
  pair is 0.078 above the core and the closest rejected one 0.020 below it at `n = 10`
  (recorded per size in `results/generic_Sc16.json`).

## 4. Status of THY-REQ-0002 after this update

| question | status |
|---|---|
| 1. saturation, lattice | **done** to 24 torsions: none |
| 1. saturation, generic chain | done to 12 torsions: none (geometric growth); `n = 13…16` needs a different cover algorithm (see below) |
| 2. entropy of profile sets, exhaustive | done (lattice, brackets); by sampling to `N = 10³`: not started |
| 3(a) all patterns realised, lattice | **done**, for every `n` (proof) |
| 3(a) generic chain | not started (the hard core removes `g⁺g⁻`, so the directed-walk argument does not transfer as it stands) |
| 3(b) single-flip constants, lattice | **done** to 16 torsions; valid envelope; `c_j ≥ κ d_j` with `κ` between 14 and 22 |
| 3(b) generic chain | not started |
| 4. sum class on the 683-conformation chain | not started |
| 5. span format off-lattice at `n = 10` | not started |

*Why the generic chain stops where it does.*  Off-lattice the optimum is a large fraction of
the classes (215 of 639 at `n = 9`), dominance reductions remove little, and the integer
programme does not close: each cell costs its full time limit.  At `n = 13` (13 012 classes)
a first attempt was stopped after 13 minutes because the larger sizes would not have
finished within their bound (job M-006, `docs/engineering/DEAD_ENDS.md` ED-3).  The exact method does
not scale here; brackets from the certified dual bound and a good primal heuristic do, and
that is what will be used for `n ≥ 13`.

## Execution environment, resources, reproduction

Modal jobs M-005 (lattice covers `n = 19…24`), M-006 (stopped), M-007 (generic chain) of
`docs/engineering/COMPUTE_LEDGER.md`; HiGHS of SciPy 1.18.1; NumPy 2.5.5; Python 3.12.
No random seeds (exhaustive).

```
python experiments/eng/chain_cover/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0007.md
modal run modal_jobs/chain_cover_app.py --nmin 19 --nmax 24                              # lattice covers
modal run modal_jobs/chain_cover_app.py::generic --nmin 5 --nmax 12 --cover-time-limit 90    # generic chain
```

Artifacts: `experiments/eng/chain_cover/results/lattice_Sc12.json`, `results/generic_Sc16.json`.

## Assumptions and limitations

As in ENG-RES-0002.  In addition: the generic chain is computed in floating point (class
identity by rounding to 8 decimals, cover relation with tolerance `10⁻⁹`); the diagnostic
"nearest tie" shows the results do not depend on these choices at the sizes reported, but
they are **[X\*]**, not **[X]**.  Cells in brackets are not optima.

## Recommended theoretical follow-up

None beyond ENG-REQ-0001.  One remark for the blueprint: the sentence "certificates … whose
number of evaluations does not depend on the chain length" (blueprint §7) is, on both
models and at every size computed, a statement about a regime that is not reached; the
measured dependence is linear (lattice) or geometric (off-lattice) in the chain length.
