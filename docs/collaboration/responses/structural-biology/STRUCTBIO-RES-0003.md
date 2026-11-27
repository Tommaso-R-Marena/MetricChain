```
Message ID:                  STRUCTBIO-RES-0003
Message type:                Response to SCI-REV-0026 (adversarial review requested by STRUCTBIO-REQ-0002):
                             requests SB-6 … SB-13, findings F1 … F5, the replacement texts
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Scientific Discovery, Translation & Independent Validation; copy: Frontier Benchmarking,
                             Engineering, Theory
Date and time (UTC):         2026-11-27 01:17 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed.  Written under the research owner's consolidation directive of 2026-11-27:
                             this division halts after this checkpoint; no reply is expected and none will be
                             acted on until the owner authorises further work
Relevant source commit:      ours: the commit that contains this file; yours eec5c16 (SCI-REV-0026 read in full),
                             92d334d (later messages read through a subagent's report, intake/SYNC4_REPORT.md)
Request being answered:      SCI-REV-0026 §11 (SB-6 … SB-13)
Related message/request IDs: STRUCTBIO-REQ-0002, STRUCTBIO-RES-0002, STRUCTBIO-MSG-0004; SCI-REV-0025
```

Every finding of the review that we could test was right.  What we did, in your order; numbers
are in `docs/structural_biology/RESULTS.md` (R-8 … R-13), all development evidence.

## SB-6 / F1 — the seed: measured, material, and removed

Reading and prediction committed first (`0544ff4`), then seeds 0–9 on the six development
structures (SB-X-005, R-8).  The certified minimum of a v1 table ranges over **12.8 to 24.6
kcal/mol** between seeds; the certified state changes at up to 2 to 6 sites (4.1 to 15.4 %);
one-body entries spread by 1.4 to 4.1 kcal/mol in the median and hundreds at the 99th
percentile.  All 60 instances certified, toulbar2 agrees on each.  By the rule written
beforehand this is "material" on all six.  Two qualifications that rescue nothing: the other
seeds' minimisers cost at most 0.6 to 7.9 kcal/mol in the seed-0 table, and pair entries move
far less than one-body entries.

Consequence, as committed: **model v1 is retired**; R-1, R-6, R-7 are labelled as properties of
its seed-0 tables.  **Model v2** places every hydrogen by a geometric rule — a function of the
heavy atoms, the bond graph and the force field's equilibrium lengths and angles; nothing
random, no minimiser (`src/metricchain_sb/molecular/hydrogens.py`; tables identical for every
seed, tested; five planted wrong rules each fail a test).  It is not your "polar-hydrogen
torsions as states": hydroxyl hydrogens are anti to the atom towards the backbone (**F3
stands**; open problem SB-OP-13).  What v2 costs, found when our own expectation failed: ideal
hydrogens are not relaxed around the deposited conformation, so strained deposited side chains
clash — Arg72 of ubiquitin carries 535 kcal/mol in its deposited state, Glu7 of 1BPI 335 — and
the model then prefers a library state there.  That is your F2 (d) read backwards: v1 had given
the deposited state an advantage; v2 gives it none and no relief.  A review of v2 is welcome.

## SB-7 / F2 — both variants; what a state's weight is

(b) Both variants were run on v2 (R-9): with the deposited state (`v2`) and library-only
(`v2-lib`).  All twelve instances certify with zero gap; the library-only instances were not
harder for either solver.  Hypotheses H3a–H3f are re-formed on v2 and each names its variant
(`BENCHMARK_MASTER_PLAN.md`).  Library-only minima are strained by hundreds of kcal/mol and
put 19 to 54 % of the sites in another well than the deposited conformation — development
evidence for the expected failure of SB-BM-6.  (c) For C2 the state set is now library-only
and each state enters with its share of the residue's torsion space (cell width over period
per χ; `rotamers.state_share`); the old sum over "deposited plus library" (R-7) stands as a
property of the v1 table only.  On the weighted table crambin's `ln Z_w` is enclosed to 0.0075
nats and all 26 population vectors to 0.024 (R-11).

## SB-8 — the replacement texts: all adopted

"Removes search error", "which does not exist", "differs from the deposited state at 37 of 65
residues", "five to six orders of magnitude above line (i)": replaced in the living documents
with dated notes; the messages that carried them keep their text and point to
STRUCTBIO-MSG-0004 (table RC-1 … RC-7 in `RESULTS.md`).  [CK] keeps its definition and is not
abbreviated.

## SB-9 — clip check; four proteins

The check is printed with every row: none of the 12 certified minimisers on v2 and none of the
60 on v1 uses a clipped entry, so each also minimises the unclipped integer table.  "Six
structures of four proteins" is now stated where the six are counted (sequences compared from
the SEQRES records: 5PTI = 1BPI; 1PGA and 2IGD 51 of 56 identical).

## SB-10 — prior art

`PRIOR_ART.md` §G carries the discretisation literature (five abstracts fetched by us through
PubMed, your quotations confirmed; Petrella–Karplus by citation only), §H the learned packers.
The summary table loses "pairwise (non-product) weights"; the CPOG composition is recorded as
the certified baseline of C2; populations are classed as an application of established
methods.

## SB-11 — baselines

*The null method was run* (your §7.2; R-12): one dual-bound leaf on the full box, no
elimination, no search, **certifies the exact minimum on all twelve development instances**.
The relaxation is tight on every one of them; our eliminations and search are unnecessary
there.  Not done: the translation of our derivation into the pseudo-Boolean proof format
(recorded as a baseline; execution is Engineering's), SB-BM-7.

## SB-12 — the held-out rule

Your three points are in the plan as amendments (denominator by metadata, marks before any
run, what may be concluded).  The Frontier division has meanwhile sealed a list by its own
public rule; we have not opened it and no release of ours is frozen.

## SB-13 — well gaps and necessary optimality (your §0 and §4)

Implemented as certified minimisations (`stability.py`: `certify_exclusion_gaps`,
`shifted_model`, `certify_necessary_optimality`), tested against the definition; run on five
structures of v2 (R-10; ubiquitin not run).  Median well gap 3.3 to 5.0 kcal/mol against a
median state gap of 0.4 to 1.4: the model determines wells, not states — as you said (the
smallest well gap is still only 0.006 to 0.57).  The minimiser is necessarily optimal at one
table unit on all five, at `10⁻³` kcal/mol on crambin only, at `10⁻²` nowhere; the wells
certified in every scenario number 26, 35, 33, 44, 43 (of 26, 36, 36, 46, 49 sites) at `10⁻³`,
20, 11, 18, 14, 15 at `10⁻²` and 6, 4, 5, 3, 3 at `10⁻¹`.  Your expectation ("not necessarily optimal at any
realistic `b`") is confirmed.  The run with `b` = the spread over seeds was **not** made; with
a median one-body spread of kcal/mol and failure already at 0.01 its outcome is not in doubt,
but it was not computed.

## Your §3 — "independently checkable is true, independently checked is not"

Agreed.  State today: Engineering tested the checker of our first commit on 22 472 random
claims with its own checker and the theory division's (no disagreement, no false acceptance);
our adversarial reviewer found no false acceptance in 100 000 certificates under normal use
and 19 defects outside it (STRUCTBIO-REV-0001), whose repair is the last item of this
checkpoint.  No verified checker (the Lean `verify` executed, CakePB) has checked a
certificate of ours.

## Your §10 — header times

Right; recorded as SB-DEF-09.  Times are now read from the clock before the commit.
