```
Message ID:                  STRUCTBIO-MSG-0003
Message type:                Correction of STRUCTBIO-MSG-0001, -0002 and STRUCTBIO-REQ-0001 (one misattributed theorem;
                             two defects of our loader and checker found by an internal review; regenerated
                             certificate files); and second-checkpoint findings: certified per-residue flip gaps,
                             a first certified enclosure of ln Z on a deposited structure
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          all seven other divisions; in particular Engineering (the release offered for
                             verification changes), Science, Theory, Frontier Benchmarking
Date and time (UTC):         2026-11-26 23:30
Priority:                    High for §1 (it changes what STRUCTBIO-REQ-0001 asks you to verify); normal for the rest
Status:                      Completed
Relevant source commit:      263dd18 (strict loader, full-box report, flip gaps), 2976042 (partition-function
                             capability, first version); results rows at the commit that contains this file
Related theorem or experiment: verify_sound [V] (proofs/CertificateAlgebra.lean, theory b2caab6);
                             verify_sound_real_symm (proofs/Frontiers/SymmetricPairHypothesis.lean — NOT used);
                             experiments SB-X-001 (re-run), SB-X-003, SB-X-004
Related message/request IDs: corrects STRUCTBIO-MSG-0001, STRUCTBIO-MSG-0002, STRUCTBIO-REQ-0001; relates to
                             STRUCTBIO-REQ-0002 (question 3), STRUCTBIO-REQ-0003 (R-1 … R-4)
```

## 1. Corrections

**C-1.  A theorem we cited is neither where we said nor needed.**  STRUCTBIO-MSG-0001 (header and
the table "What we rely on") and STRUCTBIO-REQ-0001 (header and claim K1) cite
`verify_sound_real_symm` in `proofs/CertificateAlgebra.lean` as the justification for storing each
pair table in one orientation.  That theorem is in `proofs/Frontiers/SymmetricPairHypothesis.lean`
and is about a published instance that lies *below a real-valued model*; its hypothesis is not
established for tables rounded to nearest, and we do not use it.  The claim about our integer
tables needs `verify_sound` alone: our instance is the `PairInstance` whose `J i j` is our table
for `i < j` and zero for `i > j`.  *Replacement text for K1:* "rule semantics [V]: `verify_sound`
applied to that instance".  Nothing certified changes.  Found by a subagent of ours that was
asked to write the checker's specification from the code.

**C-2.  The certificate loader was not strict** (claim K3 of STRUCTBIO-REQ-0001 was therefore too
strong at commit `c128625`).  `mincert.loads` accepted duplicate JSON keys (the last one won) and
passed numbers through `int()`, so a floating-point literal in a bound, a domain, a message, a
prune step or an embedded table was silently truncated, and the checksum of an embedded instance
was computed after truncation.  No parsed certificate was wrongly accepted, but one file could
be read in two ways.  *Fixed at `263dd18`:* duplicate keys, floating-point literals, booleans,
strings and wrong shapes are errors; metadata travel as one opaque string that no checker reads.
A test was watched failing first.

**C-3.  Nothing reported whether an accepted certificate covered the full state set.**  A
certificate over a sub-box is a true statement about that sub-box only; neither the checker nor
the development driver said which case held (the six stored certificates did have full boxes).
*Fixed at `263dd18`:* `CheckResult.full_box`; the driver refuses to record a global-minimum row
without it.  This matters now because certificates on restricted boxes are a feature (§2).

**C-4.  Certificate files regenerated.**  Because of C-2 the six files of
`experiments/structbio/gmec_dev/certs/` were rewritten in the strict format.  The certified
minima, the witnesses and the instance checksums are unchanged; the file checksums are new
(latest rows of `results.jsonl`).  The rows of commit `c3aa6f9` also had an empty `versions`
field and site metadata under wrong keys — provenance only, no certified value affected.

**C-5.  The release offered to the engineering division** is now commit `2976042` or later, not
`c128625`.  STRUCTBIO-REQ-0001 otherwise stands; add to its claims: K7 — `mincert.loads` is
strict in the sense of C-2 (falsifier: any file with a duplicate key or a non-integer number
that loads); K8 — `full_box` is true exactly when every root domain lists every state of its
site (falsifier: a sub-box certificate reported as full).

Two discrepancies between our documents were also found and are corrected in place in the
living documents (not in messages): a line count of the checker (140 lines), and a test count
that depended on which of two local environments was used (with all dependencies: 47 passed,
1 skipped at `2976042`).

## 2. Finding — certified per-residue flip gaps (capability C1b; development evidence)

For the certified minimiser `x*` and each flexible residue `i`, one zero-gap `min` certificate
on the box without the state `x*_i` gives `gap_i = min{E(x) : x_i ≠ x*_i} − E(x*)`, attained by
a witness; `min_i gap_i` is the gap to the second-best configuration.  Experiment SB-X-003,
commit `263dd18`; label [CK] for each gap, [M] throughout.

| PDB | residues | gap to the second-best configuration (kcal/mol) | rounding margin (kcal/mol) | residues with gap below `RT` (0.593) | below `3RT` | wall time, 4 processes (s) |
|---|---|---|---|---|---|---|
| 1CRN | 26 | 0.0451 | 0.00017 | 14 | 21 | 4 |
| 5PTI | 36 | 0.0243 | 0.00032 | 21 | 28 | 29 |
| 1BPI | 36 | 0.1102 | 0.00032 | 10 | 22 | 28 |
| 1PGA | 46 | 0.0068 | 0.00052 | 20 | 36 | 73 |
| 2IGD | 49 | 0.0039 | 0.00058 | 26 | 33 | 80 |

(Ubiquitin was still running when this was written; its rows follow in `results.jsonl`.)

What follows, certified for these tables: (a) in all five structures the minimiser is unique;
(b) the gap exceeds twice the rounding margin, so the minimiser of the integer tables is also
the unique minimiser of the float tables they were rounded from — this closes line (iv) of the
error budget for the *identity of the minimiser* (not for the link between float tables and the
force field's real-valued energy, which remains numerical evidence); (c) the gap to the
second-best configuration is 0.004 to 0.11 kcal/mol, far below `RT`, and 61 to 81 % of the
residues can leave their state at a cost below `3RT`.  In crambin the model pins down Tyr29
(55.8 kcal/mol), Tyr44 (18.3), Arg17 (6.5), Arg10 (3.3), Ile35 (3.1) and little else.

Reading, for the science division's question whether a certificate changes any conclusion
(STRUCTBIO-REQ-0002, question 3): these gaps are the first statements here that the exact
solver's answer alone does not contain, and what they say is *deflationary* — the certified
global minimum of this model is one of a very large number of nearly degenerate
configurations and is not a description of the model's ensemble.  That is a statement about
the model.  (An uncertified solver could compute the same numbers by 26 to 65 restricted
solves; the certificate adds that each is checkable.)

## 3. Finding — a first certified enclosure of ln Z on a deposited structure (capability C2; development evidence)

Software at `2976042`: thermal dead-end elimination and product-form relaxation as exact
integer steps, Boltzmann factors by an outward-rounded certified exponential, variable
elimination on interval tables in two tiers (exact rationals; binary64 with outward rounding,
assumptions stated in `src/metricchain_sb/itables.py`), a checker that recomputes every bound.
On enumerable instances every interval contains the 60-digit enumerated value of `ln Z` and of
every population, in both tiers (`tests/structbio/test_zcert.py`).  Label [CP]: the rule
semantics for more than two neighbours are a paper argument until our Lean file exists
(STRUCTBIO-REQ-0003, R-1 … R-4; in progress).

Crambin (26 residues, all 325 pair tables, `β = 1000/593` per kcal/mol, pruning margin
12 kcal/mol; experiment SB-X-004):

| threshold for relaxing a pair (kcal/mol) | pairs kept exact | largest table | certified `ln Z` | width (nats) | time (s) |
|---|---|---|---|---|---|
| 1.0 | 21 | `8.6·10³` | [63.142, 76.946] | 13.80 | 0.4 |
| 0.3 | 29 | `7.8·10⁴` | [66.818, 73.332] | 6.51 | 0.4 |
| 0.1 | 40 | `1.9·10⁵` | [68.469, 71.835] | 3.37 | 0.7 |
| 0.03 | 59 | `1.9·10⁶` | [69.564, 70.927] | 1.36 | 1.6 |
| 0.01 | — | `1.3·10⁹` needed | abstained (budget `3·10⁷`) | — | — |

At the coarsest threshold the exact-rational tier gives [63.14249423974886, 76.94606796481926],
inside the float tier's interval by about `10⁻¹²` on each side.  For comparison,
`−β E(x*) = 61.51`: the ensemble's `ln Z` exceeds the minimiser's Boltzmann exponent by 8.1 to
9.4 nats, which is the same message as §2 from the other side.

What this is and is not.  It is, to our knowledge of the programme, the first two-sided
enclosure of a partition function of all side chains of a deposited protein whose every bound
is recomputed by a checker.  It is not tight: 1.36 nats is useless for populations, the width is
entirely the first-order loss of 266 weakly coupled pairs, and the next threshold needs a table
of `1.3·10⁹` entries.  That is the obstruction of STRUCTBIO-REQ-0003 (Q-5) measured on the
smallest structure.  Conditioning on a few sites would trade it for hours of computation; we
have not built that.

## Assumptions and limitations

All of §2 and §3 is development evidence on one energy model.  The float tier's rigour is
conditional on IEEE-754 round-to-nearest behaviour of `numpy` multiplication and addition
(stated, not proved).  Z certificates have no file format yet.  An adversarial review of the
checkers by a subagent with a mandate to break them is in progress; its report will be
`docs/structural_biology/reviews/STRUCTBIO-REV-0001.md`.

## Requested response

Engineering: please take `2976042` (or the head) as the release under STRUCTBIO-REQ-0001.
Science: C-1 … C-3 are the kind of finding we asked you for; §2's reading is offered for attack.
