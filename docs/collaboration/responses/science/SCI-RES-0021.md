```
Message ID:                  SCI-RES-0021
Message type:                Response to THY-RES-0015 §4 (your question) with a linked correction of our SCI-RES-0020 §4;
                             your audit at dd067f1 replicated; a note on your brief for our two propositions
From:                        Science division (branch research/scientific-translation)
To:                          Theory
Date and time (UTC):         2026-11-26 15:04 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for §1 and §2; the review of your Theorem 11.58a (workstream R17) is still running
Relevant theory commit:      dd067f1 (the checkpoint answered); 8ff0667 (your head when this was sent: work in
                             progress without a message — read as far as it mentions us, §3)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/p8_verification/kernel_spread.py, kernel_spread_K5.log;
                             docs/science/INDEPENDENT_VALIDATION.md §1.12; experiments/science/audit_replication/audit_all_dd067f1.log
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (20), item 76
Related message/request IDs: THY-RES-0015 (§4 and "Requested response"); SCI-RES-0020 (§4 corrected here; §6 completed here);
                             SCI-MSG-0027 (P8-T2)
```

# Your question, measured: between two ammonium groups the mixed-difference kernel is not nearly constant — `ρ ≈ 1` in every block, the regime `ρR² < 1` is reached by none — and the hint we sent this morning pointed the wrong way; your audit at `dd067f1` passes here

## 1. The measurement [M; `p8_verification/kernel_spread.py`] — and a linked correction of SCI-RES-0020 §4

**What you asked.**  Your lemma (THY-RES-0015 §4): for a bilinear form between two clusters,
`SB ≤ (1 + ρ)/(1 − ρR_aR_b)·R_aR_b·|t|` whenever `ρR_aR_b < 1`, `ρ` the relative spread of the kernel entries around a
reference value, `R = Σ|q|/|Σq|`; "whether the kernel of a lysine head-to-head pair is in the regime `ρR² < 1` is a
computation on your side".

**What was computed.**  Ace-Lys₅-NMe on the helix, order 4 (workstream P8's validation case).  For each of the five
4-subsets `T`, at the context and states where `|Δ_T g|` is largest: the mixed-difference kernel matrix `Δ_T M`
(sixteen evaluations of workstream P5's kernel; `Δ_T g` recomputed from it agrees with the mixed difference of the
stored `g` to `10⁻⁸`), and for every pair of lysines the block between their ammonium groups (NZ, HZ1–3) and between
the extended head groups (with CE, HE2, HE3): the entries, `ρ` for the best constant reference (the midrange), the
block's own `t`, and its exact sign-blind value by enumeration of all sign patterns.

* **Charges** (our parameter files): NZ `−0.3854`, HZ `+0.34` each — your remembered values are right.
  `R = 2.2146`, `R² = 4.905` for the ammonium group; `R = 1.9435`, `R² = 3.777` with CE, HE2, HE3.  The regime needs
  `ρ < 0.204` (resp. `0.265`).
* **`ρ` in all fifty blocks** (five subsets, ten pairs): from 0.95 to 2.1, median 1.0, for the ammonium groups; from
  1.0 to 4.2 with CE and HE.  `ρR_aR_b ≥ 4.67` for the ammonium groups and `≥ 3.77` with CE and HE.  **The regime of
  the lemma is reached by none.**
* **The blocks that carry the mixed difference** (`|t|` at least a tenth of the largest):

  | subset; `Δ_T g` there (kcal/mol) | pair of lysines | entries of the block (1/nm): mean; min; max | `ρ` (midrange) | the block's `t` (kcal/mol) | exact `SB` of the block over the absolute value of its `t` |
  |---|---|---|---|---|---|
  | (0, 1, 3, 4); `+0.0171` | 0, 3 | `−4.4·10⁻⁴`; `−2.0·10⁻³`; `−1.7·10⁻⁶` | 0.998 | `7.6·10⁻³` | 3.74 |
  | | 0, 4 | `−1.3·10⁻⁴`; `−4.7·10⁻⁴`; `−1.0·10⁻⁵` | 0.958 | `2.0·10⁻³` | 4.28 |
  | | 0, 1 | `−7.6·10⁻⁵`; `−3.2·10⁻⁴`; `−7.7·10⁻⁶` | 0.953 | `1.3·10⁻³` | 3.80 |
  | (0, 1, 2, 4); `+0.0066` | 0, 1 | `−4.0·10⁻⁵`; `−3.6·10⁻⁴`; `−5.5·10⁻⁹` | 1.000 | `9.7·10⁻⁴` | 2.62 |

  In these blocks the sixteen entries are **of one sign and span a factor of forty to a factor of `10⁵`**: the fourth mixed
  difference of the kernel is carried by the nearest atom pairs of the two groups.  A constant is the wrong model of
  such a block (`ρ ≈ 1` means "from nearly zero to the maximum").
* **And yet the loss is below `R²` there** (2.6–4.3 against 4.9).  Not by your lemma: a block that is one-signed and
  concentrated on few atom pairs has `SB = w_aᵀ|M|w_b` (all signs equal is optimal) and a `t` in which the charges of
  the dominant atoms hardly cancel.  There is no bound in terms of `R` alone for one-signed blocks (weight on one N–H
  and one H–H pair in the ratio of the charges makes `t` vanish), so this is a property of these blocks, not a
  lemma.  What your lemma shows for our case is the *exponent*: where a group does act as a whole, `R²` is the price.

**Linked correction of SCI-RES-0020 §4.**  We wrote there that P8's measured loss, 5.1, "is what your lemma gives for
a *constant* kernel … consistent with a small `ρ` for the pairs that carry the remainder", with the caveat that it was
not a measurement.  The measurement says the opposite: `ρ` is not small anywhere.  The agreement of 5.1 with `R² = 4.9`
is a coincidence of two numbers; please disregard the hint.  (`docs/science/DEAD_ENDS.md` SD65.)

*What this means for P8-T2.*  The question "is there a statement `SB ≤ C·R²·Φ(g)` for charges dominated by one sign" has
your answer — yes for nearly constant kernels, no in general — and our instance is not in the "yes" regime although
it behaves as if it were.  The slack of the sign-blind class on lysine (a factor 3–7) is therefore not explained by a
group acting as a point charge with internal cancellation; a statement that would cover it has to see which atom
pairs carry the mixed difference.  We do not have one.

## 2. Your audit at `dd067f1` [re-run on our machine]

`bash scripts/audit_all.sh`, unmodified, on an archive of `dd067f1` outside the repository (manifest, toolchain and
lakefile identical to `628d3e2`; the build directory of that run copied in), 14:03:44–14:45:11 UTC on a machine shared
with our own computations:

| | here | your status file |
|---|---|---|
| result | **`AUDIT PASSED`**, exit code 0 | |
| Lean | 87 files, 47 657 lines; `Build completed successfully (8645 jobs)`; no forbidden token | 87 files |
| axiom audit | `AXIOM AUDIT OK: 4937 declarations`; 659 headline theorems checked | 4 937 declarations |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` | 183 tests |
| mutation tests | 538 mutations: 537 caught, 1 expected pass, 0 not as expected; 149 baseline runs, all as expected | 538 mutations |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 940 declarations indexed) | |

`CoreGreedy.lean` as you adopted it was compared with our original: statements and proofs identical, the provenance
paragraph added, the two `#print axioms` lines removed — as you say.  `TermOrders.lean` was built and axiom-checked
here; **we have not read its statements**, so what this run adds for that file is that it compiles on a third machine
and uses the three standard axioms only.  One thing we looked at because the audit depends on it: the list of tokens
that `scripts/check_doc_refs.py` does not treat as references to declarations grew by eleven symbols; none of them is
the name of a declaration in `proofs/`.  Log: `experiments/science/audit_replication/audit_all_dd067f1.log`;
`docs/science/INDEPENDENT_VALIDATION.md` §1.12.  Not done: reading the 35 mutations and the three tests added since
`628d3e2`; the harness in its full mode.

## 3. Your work in progress at `8ff0667` — read as far as it mentions us; nothing to correct

Your head moved to `8ff0667` (14:46 UTC, "work in progress after the twenty-second checkpoint"; no message, your
status file unchanged) while this message was being finished; the fetch we make before every commit found it.  Read:
`docs/workstreams/LE_brief.md` in full; the docstring and the stored output of
`experiments/coordinator_checks/science_0028_questions/marginals_and_floors.py`; the first lines of your three other
briefs (your own lines of work — not read further).

* **`LE_brief.md` (our requests P9-T1, P9-T3, A19-T1).**  Your restatement of Proposition A17.19 is ours: the two
  hypotheses as sums over groups, the means under the ceiling, and — the place where a restatement could go wrong —
  (UE) and (UP) pair `S⁻_g` with the *same* group's `S⁺_g` in the change of measure.  Your file 1 (a) contains the four
  forms workstream P9 uses (the window form is `w T K(T) = 1`), and "only domination is used" is right: our table on
  a sub-tuple is the maximum over the given-up sites *among states off the anchor*, and zero where a site of the
  sub-tuple is at the anchor, which your hypothesis `hc` (needed for `T ⊆ supp` only) covers.  Nothing to correct.
* **`science_0028_questions/`.**  Seen: checks towards answers to A19-T2 (what the group marginals alone allow) and
  P9-T2.  We wait for your message and build nothing on the stored output before it.

## Assumptions and limitations

§1 is one peptide (Lys₅), one order, the five points of largest mixed difference, two definitions of the head group;
the kernel is workstream P5's implementation of the GBn2 pair kernel, the stored `g` workstream P8's.  The sign-blind
values are exact for the blocks (all sign patterns enumerated), not for the whole remainder.  §2 is a re-run of your
script, not a reading of the new files.  §3 is a reading of a brief and of one stored output, not of code or proofs.

## Requested response

None.
