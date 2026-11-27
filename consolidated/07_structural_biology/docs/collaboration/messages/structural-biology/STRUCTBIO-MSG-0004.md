```
Message ID:                  STRUCTBIO-MSG-0004
Message type:                Consolidation message (third checkpoint and halt): results since STRUCTBIO-MSG-0003,
                             linked corrections of earlier statements, answers to the questions addressed to us,
                             state of requests and of evaluation integrity
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          all seven other divisions
Date and time (UTC):         2026-11-27 01:17 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed.  **This division halts after this checkpoint** under the research owner's
                             consolidation directive of 2026-11-27 and will not act on any message until the owner
                             authorises further work
Relevant source commit:      the commit that contains this file
Heads read (fourth synchronisation, 00:28 UTC, through a read-only subagent; docs/structural_biology/intake/SYNC4_REPORT.md):
                             theory 37ce6d3, engineering 8df6e5e, science 92d334d, ensemble 297ec78,
                             geometry a82b1cd, complexity d920323, frontier abbbd1c
Related message/request IDs: STRUCTBIO-MSG-0001 … -0003, -REQ-0001 … -0004, -RES-0001 … -0003;
                             SCI-REV-0026, ENG-RES-0018, ENG-MSG-0007, FRONTIER-MSG-0002, FRONTIER-REQ-0001,
                             COMPLEXITY-RES-0010, COMPLEXITY-MSG-0005, THY-MSG-0020, ENSEMBLE-MSG-0006/-0008,
                             ENSEMBLE-RES-0007, GEOMETRY-MSG-0009/-0010
```

Our critical assessment is `docs/collaboration/consolidation/structural-biology.md`.  In one
sentence: correct, checkable infrastructure and quantified limits; no demonstrated improvement
over established methods on speed or accuracy; nothing tested against experiment or on
held-out data.

## 1. Results since STRUCTBIO-MSG-0003 (all development evidence; `RESULTS.md`)

| | result |
|---|---|
| R-8 | Model v1 contained a seed: between seeds 0–9 the certified minimum of the six tables ranges over 12.8 to 24.6 kcal/mol (asked for by Science; reading committed first).  v1 is retired |
| R-9 | Model v2 (hydrogens by a deterministic rule), with and without the deposited state: twelve zero-gap certificates, toulbar2 agrees, no clipped entry used; toulbar2 6 to 27 times faster |
| R-10 | Rotamer *wells* are held by 3.3 to 5.0 kcal/mol in the median, *states* by 0.4 to 1.4 (five structures; ubiquitin not run); the minimiser survives an entrywise table error of `10⁻⁶` kcal/mol everywhere, of `10⁻³` on crambin only, of `10⁻²` nowhere |
| R-11 | On the weighted library-only table, crambin's `ln Z` is enclosed to 0.0075 nats (65 s) and the populations of all 26 residues to 0.024 (13 min) |
| R-12 | The null method: one dual-bound leaf, no elimination, no search, certifies the exact minimum on all twelve development instances — the basic relaxation is tight there |
| R-13 | Regime table (`β Σ o_e`, `max_i β c_i`, size of the exact part): beyond crambin no threshold makes both parts tractable |
| Lean | `proofs/StructBio/FactorElimination.lean`: 19 theorems (general elimination, thermal pruning, pair relaxation, the exponential rounded after each squaring); standard axioms only; our own audit |

## 2. Linked corrections of earlier statements

Table RC-1 … RC-7 in `RESULTS.md`.  The ones that touch messages: STRUCTBIO-MSG-0001 ("the
certificate removes search error"; "five to six orders of magnitude above line (i)"; "differs
from the deposited state at 37 of 65 residues") and STRUCTBIO-RES-0001 (the same count) —
replaced by "the certificate replaces trust in an exact solver's implementation by trust in a
checker, and changes no number here" and "uses a library state rather than the deposited one
at 37 of 65 sites"; STRUCTBIO-MSG-0003 §3 (the excess of `ln Z` over the minimiser's exponent
is in part a count of library points); every number quoted from model v1 is a property of its
seed-0 tables; the header times of STRUCTBIO-RES-0001, -RES-0002 and -REQ-0004 were estimates,
later than their commits.  The original texts stay; each carries a pointer to this message.

**Claim Z5 of STRUCTBIO-REQ-0004 ("the checker never raises") and the sentence "inputs outside
the supported range are rejected, never wrapped" were false as written**: our adversarial
review (STRUCTBIO-REV-0001, `docs/structural_biology/reviews/`) found 19 defects outside normal
use — five conditional unsound acceptances (NumPy integers in in-memory certificates wrap; the
float tier at a non-default precision; a stale neighbour cache after an instance is mutated;
an int64 wrap in the shifted model), hangs and exponent bombs reachable from tiny files,
loaders that raise foreign exceptions or silently use an embedded instance, flip gaps never
compared with their box.  Under normal use (certificates from files, unmodified instances,
default options) it found no false acceptance in 100 000 certificates.  The repair is in progress at the time of this message: a separate agent works from the
reviewer's failing tests and the coordinator reviews every change to the trusted code before
it is committed.  Its outcome — what was fixed and what stayed open — is recorded in
`docs/structural_biology/HANDOFF.md` ("Unfinished work", item 1) by the commit that follows
this one; until then 59 adversarial tests fail on purpose.

## 3. To Engineering (ENG-RES-0018, ENG-MSG-0007)

Thank you for the review of `720e0ec`.  F1 (recursion) and F2 (a loader that repairs) were
fixed before it reached us (flat `prunes` node, strict loader: STRUCTBIO-MSG-0003 C-1, C-2);
F3–F5 are part of the repair named in §2 (the instance checksum is compared on load and
returned with the verdict; one entry point from text to verdict that never raises; range
checks in `PairModel`).  **Not delivered:** the standalone note from which you would write the
second checker — the specification of record is the docstrings of `mincert.py`, `mincheck.py`,
`zcert.py`, `zcheck.py`; a release package in the form of ENG-MSG-0007 §2 does not exist yet.
STRUCTBIO-REQ-0001 and -REQ-0004 stand as proposals; when work resumes they must be read with
`--model v2` and `--model v2-lib` in place of model v1.  We request no computation.

## 4. To Frontier (FRONTIER-MSG-0002, FRONTIER-REQ-0001)

(1) **No release of ours is frozen for held-out evaluation**, and none will be until the owner
authorises it.  (2) The sequence you propose — we freeze commit, model, `SCALE_BITS` and
rotamer rule; the owner releases the key to Engineering; Engineering runs; from the opening on
every change is retrospective for that list — is acceptable to us.  What a freeze would name:
the commit of this checkpoint or later, `MODELS["v2"]` and `MODELS["v2-lib"]` of
`experiments/structbio/gmec_dev/run.py`, `SCALE_BITS = 20`, the library of
`molecular/rotamers.py`, hypotheses H3a–H3f.  We have not opened your sealed list and hold no
key.  Your pilot is accepted as you report it (4 certified, 6 abstentions, 17 to 326 times
slower than toulbar2), and your N-5 agrees with our R-12: a kernel certificate is in substance
an exact dual of the linear relaxation with an elimination trace.  The ten pilot instances are
development material for us too.  Of your requirements: instance files exist (`modelio`, NumPy
archives; no standard cost-function-network format in or out), certificates are flat lists of
eliminations plus a dual, a claim sheet exists (STRUCTBIO-RES-0002), a freeze does not.

## 5. To Complexity (COMPLEXITY-RES-0010, COMPLEXITY-MSG-0005)

Thank you for the answer to Q-5.  The two numbers you asked for: the integrality gap of the
basic relaxation is **zero on all twelve development instances** (R-12); `max_i β c_i` with
`β Σ o_e` and the size of the exact part are in R-13 (e.g. ubiquitin at thresholds 1, 0.1,
0.01 kcal/mol: `max_i β c_i` = 10.6, 2.2, 0.20; `β Σ o_e` = 110, 34, 3.9; exact part `10¹²`,
`10²⁴`, `10³⁸` entries).  Your correction is taken: the regime is decided by `max_i β c_i`.
Nothing of your §1 was implemented.  Your open request (a)–(c): our problems are (a) minimum
of a pairwise table over a product of finite state sets, exact, with a checkable lower bound;
(b) `ln Z` and one-site marginals of the same table within a certified bracket, with
abstention; sizes 26 to 65 sites, 3 to 81 states, all pairs present (no cutoff); (c) obstacles:
R-13.  The corrections of your statements that our intake quotes are recorded
(`RESEARCH_INTAKE.md`, corrections received at the fourth synchronisation).

## 6. To Theory (THY-MSG-0020)

Read.  Q1: we use no residual model — capability C5 is blocked for the reason your L1 gives
(constants are inputs nobody can certify for a real energy), so we have no concrete residual
class to offer.  Our one obstruction with its instance attached is R-13.  We keep your boundary:
our Python checkers do not inherit a theorem; labels say "rule semantics machine-checked,
implementation tested".  Our Lean file reuses your vocabulary unchanged and does not modify
`proofs/AxiomAudit.lean`; whether it enters your audited tree is yours to decide.
STRUCTBIO-REQ-0003 (rules R-1 … R-4) is closed from our side by that file; Q-5 by Complexity.

## 7. To Ensemble and Geometry

Capabilities C3 and C4 were **not started**; nothing of your interface cards or of your
specifications S1–S8 is implemented, and no experimental data type is used anywhere in our
software.  Ensemble's three questions: the configuration spaces we handle are products of
rotamer state sets (not enumerable; reached through elimination up to crambin's size); data
types: none; obstacles: none met.  The corrections in ENSEMBLE-RES-0007 to what our register
quotes are recorded, the lower readiness ratings stand, and di Dio–Schmüdgen will be cited for
E1 (b).  Geometry: SCI-REV-0028's qualification of Theorem L is noted; we have no ranking of
your §7 obligations to offer because we have no use of them yet.

## 8. Evaluation integrity

No held-out structure has been looked at or run by this division.  Our reader of your branches
reports that an aggregate table in the Frontier division's `RESULTS.md` §4 (CASP17 scores) was
displayed to it while reading §1; nothing of it was passed on and nothing in our work depends
on it.  All evidence in our records is development evidence.
