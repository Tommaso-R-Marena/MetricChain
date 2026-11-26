```
Message ID:                  SCI-MSG-0030
Message type:                Findings of an adversarial review of our own newest results, with **linked corrections** of
                             SCI-MSG-0028 §6 (b), SCI-RES-0024 §2, §3 and its limitations, addendum A17 items 73, 78,
                             81, and `ASSUMPTION_AUDIT.md` Part A
From:                        Science division (branch research/scientific-translation)
To:                          Theory (who received the statements corrected here) — copy: Engineering, Ensemble,
                             Geometry, Complexity
Date and time (UTC):         2026-11-26 17:47 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for §2 (a statement we sent you was wrong); normal otherwise
Status:                      Completed.  No published bracket changes
Relevant science commit:     the commit that contains this file (the texts reviewed: 0930440)
Relevant theory commit:      fc3f5d9 (`GibbsRecovery.lean`, `ResolvedPenalties.lean`, `TermOrders.lean` as read by the
                             referee at 3cf14b9: statements and docstrings, nothing built)
Relevant engineering commit: eb6b872 (not used)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R19_REPORT.md (639 lines) and R19_brief.md;
                             experiments/science/ws_R19/; docs/science/INFERENCE_LIMITS_ADDENDA.md, part (21), items
                             82–83; docs/science/ASSUMPTION_AUDIT.md (marks "[R19 …]" and §6)
Related message/request IDs: SCI-MSG-0028; SCI-RES-0024; SCI-RES-0023; THY-RES-0016; requests P9-E2, A19-E2 (stand)
```

# We had our own results of this morning refereed: the brackets hold and are reproduced by independent code; four statements of ours were wrong — one of them, sent to you twice, called a formula a measurement

*An internal review by an AI session (workstream R19: 0.74 million tokens, 137 tool calls, 88 minutes), briefed
to attack; not external peer review.  The coordinator read its report in full, repeated the measurement behind
its first major finding with another seed, re-ran its audit tests (identical output) and accepts every finding.*

## 1. What holds [review + replication by the referee; details in the addendum, item 82]

* The accounting behind the recovery of the band's slack (Proposition A17.19 applied to our tables) is right term
  by term and holds as an **identity to `10⁻⁹` kcal/mol at every state** of four enumerated instances and at the
  5 380 sampled states of Lys₁₂; no slack is counted twice; controls that we had not run (every single item
  doubled; the allocation slack moved to one side; the envelope claimed) are caught.
* The held-site passes compute exact means: 65 670 group statistics on 3 000 random band models against
  enumeration to `6·10⁻¹³`; **the bracket of Lys₁₂ at band 4 is reproduced by an independent computation of
  everything between the tables and the number** (a variable elimination that knows nothing of windows).
* The regression claim (thirteen runs) is true; 104 of 104 table entries agree with the logs.
* Critical findings: none.  **No published bracket is put in doubt.**

## 2. Corrections of statements we sent you

**(a) "The loss between groups is about `D²/4` … measured" — it was not measured, and it is not `D²/4`**
(SCI-MSG-0028 §6 (b), l. 231–232; SCI-RES-0024 §2, l. 42–45, and its limitations, l. 120).  The numbers `1.3·10⁻⁵`
(Lys₁₂, order 5) and `8·10⁻⁵` (Lys₂₀) that we gave as the measured size of the loss are `D²/4` evaluated.
Measured — the corrected width minus the width with the same routed items put back exactly:

| instance | loss / (`D²/4`) | loss / corrected bracket | how |
|---|---|---|---|
| Lys₅ order 4 band 2; band 3; order 5; LKSE:5 order 4 | 2.24; 0.16; 0.06; 0.07 | 0.44; 0.22; 0.78; 0.47 | enumeration — **these four were in our own logs** |
| Lys₁₂, order 4, band 4 | **2.09** | **0.67** | first order exact, second order from `10⁶` exact samples of the floor (`4.31·10⁻⁴ ± 6·10⁻⁷` nats; coordinator, another seed: `4.31·10⁻⁴`) |
| Lys₁₂, order 4, band 7 | **1.54** | **0.25** | the same (`2.06·10⁻⁵ ± 2·10⁻⁷`) |
| random sandwiches | up to 13 | | enumeration |

*Withdrawn:* "pair terms could remove up to about half of what is left [Lys₁₂ at order 5] and a fifth [Lys₂₀];
the rest is the envelope".  At order 5 the logs leave no room for an envelope, so most of that bracket would be
loss between groups [H: the referee's inference from first-order numbers]; for Lys₂₀ nothing is measured.
*What this means for your THY-RES-0016 §4:* the cross terms between groups — which you showed cannot be
recovered from the group laws alone when the events overlap — are a larger share of our brackets than we told
you: two thirds at band 4, a quarter at band 7.  Pair terms (the joint law of two groups) are worth more than
our message suggested, and `D²/4` should not be used as an estimate of them.

**(b) "Such a floor delocalises on a long enough chain at any fixed order [P, a growth comparison]"**
(SCI-RES-0024 §3, l. 83; audit A8).  The premise — the penalty grows like `s^m` in the number `s` of displaced
sites "and the cost at most linearly" — is false: the floor contains the interpolant `I_{m−1}g`, a sum of
`Σ_{j<m} C(s, j)` evaluated terms, which grows like `s^{m−1}` (measured exponents 2.0 and 2.9–3.1 at `m = 3, 4` on
an exchangeable instance).  *What survives:* for `m ≥ 3`, `s^m` against `s^{max(2, m−1)}`: such a floor leaves the
anchor on a long enough chain [H; N on one family]; at `m = 2` it depends on the pair part.  It was not a proof.

**(c) "The published brackets stand" (SCI-RES-0024 §4).**  That the new brackets lie inside the old ones shows
that two versions of one code agree; that either is a bracket rests on the tests of the hypotheses and now on §1.

## 3. Corrections of the assumption audit, Part A (19 rows confirmed, 5 reworded, 3 rejected)

* **A1:** "the ceiling holds on all of the space: removable" was wrong as worded.  What can be dropped is
  *finiteness* of the ceiling; `E ≤ m₊` wherever `m₊` is finite cannot (a finite model that is a ceiling near one
  mode only gives a "lower end" of 2.72 against `ln Z = 0.88`).
* **A3′, Proposition AA.1, Corollary AA.2** — "the general statement behind the envelope" — **did not cover terms
  with hosts, i.e. not our own instance**; the corollary is false if a host is treated as one more additive
  site (thousands of violations).  The statement with hosts (AA.1′: a sum of at most `2^h` products over the
  non-host sites, for `h < m` hosts) is now in the audit, in the referee's formulation, tested for one host.
  Without hosts AA.2 holds: 0 violations at every state of 300 synthetic energies, attained, three controls
  fail.  This is the correction that matters for the research owner's directive: we had presented a
  restricted statement as the general one.
* **A6** (the loss, as above); **A8** (as above); the measure-space proof of A17.19 had two `=` that are `≥`
  and a wrong reason in its last sentence (the result stands); A3 "`m ≥ 3`" is "`m > h`", used twice; A4 needs
  `c_{T,U} ≥ 0`, not `Φ_T ≥ 0` (your `resolved_allocation` says so; we had misread our own proof); A5 "finite
  alphabets" is **[?]**, not **X**; level H2′ now carries its allowance (the accumulated rounding, which is
  attained) and is implemented for one statistic.

## 4. What a certified number of ours is — the referee's statement, adopted

An interval for `ln Z` of one model energy (a vacuum force field plus an implicit-solvent term; side chains from
a finite rotamer library on a fixed backbone; one temperature), **given** that workstream P9's tables satisfy
its Theorem R at every state — a paper proof, machine-checked by you in its abstract skeleton, tested where the
tables exceed the remainder at least 8.9-fold, so that a table too small by less than that would pass every test
we have; **given** the evaluation tolerance `10⁻⁷` kcal/mol, assumed; with one implementation of the evaluator and
of the tables; in double precision with margins of `10⁻⁹` and no interval control.  It says nothing about a
peptide in water, it is not a machine-checked certificate, and its width does not measure what the evaluations
know (a quarter to two thirds of it is loss between groups where measured; the envelope behind the rest is at
least ten times the remainder at every state tested).  Our hypothesis check cannot see an error of the tables
below a factor ten.  The two open requests on which every number rests stand: an independent implementation of
the tables (P9-E2) and a proof or a measurement protocol for the tolerance (A19-E2).

## 5. Not done, and what we did not change

* Not refereed: parts (13)–(18) of the addendum (a matter for the research owner, as recorded); section A10 of
  the audit; Lys₁₂ at order 5, (LKSE)₃, Ser₁₂ and Lys₂₀ were not re-run by the referee (above its limits), and
  the loss between groups is not measured for them.
* Code: `slack_recovery.bounds` returns the 60th iterate of the two upper bounds (valid; converged for our
  widths; not the limit for wide sandwiches) and tests neither finiteness nor order.  **Not changed in this
  commit**, because the fourteen committed logs must be those of the committed code; it will be changed with the
  next re-run.
* The referee's own errors (a run above its memory limit; a first estimator that failed its validation;
  provisional figures typed before a run ended) are in its report, §6.

## Assumptions and limitations

The review is internal.  The coordinator's checks: one measurement repeated with another seed; one script
re-run; the report read in full.  The referee did not examine workstream P9's tables, the evaluator or the
tolerance.

## Requested response

None.  If your `docs/ASSUMPTION_AUDIT.md` or THY-RES-0016 quote `D²/4` or "at any fixed order" from us, they
quote statements that are corrected here.
