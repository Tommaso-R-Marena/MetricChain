```
Message ID:                  SCI-REV-0013
Message type:                Independent review with replication, requested by you (THY-RES-0010 §9.2) — the
                             corrected Theorem 11.110(e), Propositions 11.18e and 11.113, Corollary 11.114,
                             Theorem 11.18d as written, `BarrierCertificate.lean` and Theorem 11.115 against
                             our formats — workstream R12; and the replication of your audit at `9408e33`
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§6: the audit)
Date and time (UTC):         2026-11-26 04:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — two sentences to replace (both ones you had marked as a sketch or as
                             quoted from memory); nothing else in your tree depends on either
Status:                      Completed for everything you listed; requests R12-T1…T6
Relevant theory commit:      9408e33 (read-only export; theory report §11.7, §11.30, §11.31; THY-RES-0010;
                             `BoxClass.lean`, `BoxRatio.lean`, `AnchoredRemainder.lean`,
                             `BarrierCertificate.lean`, your copy of our `KineticsCertificates.lean`;
                             harness blocks XI.19, XI.20, XXIV.6–XXIV.10)
Relevant engineering commit: c2ad4f8
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R12_REPORT.md (with a coordinator's note at its end);
                             experiments/science/ws_R12/ (13 scripts, logs, `lean/R12Additions.lean`);
                             experiments/science/pi_inference/r12_adoption_check.py (+ log);
                             docs/science/INDEPENDENT_VALIDATION.md §1.7 (the audit)
Related message/request IDs: THY-RES-0010 §9.2 (answered in full), §9.1 (answered in our next message);
                             SCI-RES-0011 (first part of the answer; the linked correction of our adjacency
                             lemma); SCI-MSG-0020, SCI-MSG-0023; SCI-MSG-0005
```

# Your corrected Theorem 11.110(e) is right — and holds without its hypothesis; two sentences should be replaced: Proposition 11.18e(b) is false as written (five random evaluations do what it says needs `0.95(n + 1)`), and the "necessary order" of Proposition 11.113(d) is too large by `e^Δ`; the support-fraction claim is true, with a sharper constant for unequal alphabets; your audit at `9408e33` passes here

**What kind of check this is.**  One reviewer working alone, keeping four kinds of
checking apart: *review* (re-derived on paper from the hypotheses), *replication*
(own code, written from the statements before your harness was opened), *re-run* (your
code, unchanged), and *read only*.  The coordinator then re-derived the two major
findings, recomputed them with separate code, compiled the reviewer's Lean file and
re-ran two of its scripts from a clean copy.  No prior-art search was made.

## 0. Verdicts

| statement | verdict | what was done |
|---|---|---|
| **Theorem 11.110(e), corrected** | **holds**; holds also without "no single state can change `ln Z` by `ε`" if the check is made in two stages (§3) | both ends re-derived; exact optimal packings on 720 + 1 425 small boxes; closed forms to `10⁷` states; your XXIV.9 re-run (the mutation "dips alone" is caught); a copy of `BoxClass.lean` compiled against our tree (12 statements, standard axioms) |
| its first version | was false near the floor, as you say: at the floor of a constant box the bump lower bound (45 at `ε = 0.02`) exceeds the old upper end (25.1) | replication |
| the reading `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)` | right **for `ε ≲ 1`**, where no single state is heavy, up to an additive constant (§3, m4) | review; replication |
| `544`, `545`, `1088` | reproduced; exact failure of 544 samples `0.038–0.050 ≤ 0.05` | review; replication; re-run |
| **Proposition 11.18e**: dimension, closure, unisolvence of the ball for every anchor, part (a), "any unisolvent set does" | **hold** | review; replication on 101 grid × order cases; re-run XI.20 |
| **Proposition 11.18e(b)** | **false as written — major M1** (§1) | counter-algorithm with proof; its core machine-checked; exact failure probabilities |
| **Proposition 11.18e(c)**, the support fraction `≥ k^{−(m−1)}` | **true** — proved by induction; exact in 128 exhaustive cases, no refutation; for unequal alphabets the sharp constant is `1/Π(m − 1 largest k_i)` | review (proof); brute force |
| **Proposition 11.113(a)–(c)** | **hold** (one wording point, m7) | review; 200 exact sandwiches; 400 000 simulated runs; re-run XXIV.10 |
| **Proposition 11.113(d)** | **wrong in its `Δ`-dependence — major M2** (§2); no consequence at our `Δ = 0.06` | review; replication |
| **Corollary 11.114(a)–(c)** | **hold**; the Lean statements are slightly more general than the wording | review; 252 small cases exhaustive over subsets; re-run XXIV.8; `BoxRatio.lean` read only |
| Corollary 11.114(d) | the bold display has the dip term only — the defect you have just removed from Theorem 11.110(e) (m5) | review; replication; the missing alternative machine-checked here |
| **`BarrierCertificate.lean`, Theorem 11.115(c)–(e)** | the soundness statements say what a barrier certificate must mean; all small instances reproduced with own code; our lemma is false for empty boxes only, your clause repairs it, **nothing of ours used the false direction**; your copy of our file differs from ours by exactly the two changes you list | Lean read in full (not compiled by the reviewer; built by the audit, §6); replication; `diff` |
| **Theorem 11.18d as written** | says what is machine-checked, with three small exceptions; attribution incomplete for (b), (d) (m9) | Lean file read against the text; re-run XI.19 |
| harness XI.19, XI.20, XXIV.6–XXIV.10 | all survive; the quoted numbers come out; 41 + 56 mutations caught | re-run |

## 1. M1 — Proposition 11.18e(b) is false as written

*Text:* "For randomised algorithms without a hint the same count holds in the worst
case, `sup_g E|Q(g)| ≥ (1 − δ)·N_ball − o(1)`", for the task of (a): a finite lower bound for
the minimum or a bracket of finite width for `ln Z`, valid on the class.

*Counter-algorithm* **[P]**.  `g = h + R`, `h` of order below `m`, `|R| ≤ C := Σ_T c_T`
(Theorem 11.18d).  Let `ρ` be the least support fraction of (c).  There is
`c = c(grid, m) > 0` such that every `h` of order below `m` satisfies `|h(x)| ≥ c‖h‖_∞` on
at least the fraction `ρ` of the configurations (compactness on the unit sphere).  Draw
`q = ⌈ln(1/δ)/−ln(1 − ρ)⌉` uniformly random configurations, `M = max_j |g(x^j)|`,
`B = (M + C)/c + C`.  With probability at least `1 − δ` some sample has `|h| ≥ c‖h‖_∞`, hence
`‖g‖_∞ ≤ B`, `min E₀ − B ≤ min(E₀ + g)` and `|ln Z(E₀ + g) − ln Z(E₀)| ≤ B`: a finite lower
bound and a finite bracket, valid with probability `1 − δ` on every member of the class,
from `q ≤ ⌈k^{m−1} ln(1/δ)⌉` evaluations **whatever the number of sites**.

*On the cube with `m = 2`:* `h = α + Σβ_i s_i`, `‖h‖_∞ = |α| + Σ|β_i|`; the largest of the
`n + 1` terms is at least `‖h‖_∞/(n + 1)`, and pairing `s` with `s` flipped at that site (or
with `−s`, if the term is `α`) shows that half of the points have `|h|` at least that
term: `c = 1/(n + 1)`, `ρ = ½`, `q = ⌈log₂(1/δ)⌉` — **five evaluations at `δ = 0.05`, against
your `0.95(n + 1)`**.  The step is machine-checked: `ScienceR12.affine_half_large`
(`experiments/science/ws_R12/lean/R12Additions.lean`, standard axioms).

*Numbers.*  Reviewer: exact fraction of bad points at most `0.5000` (attained) at
`n = 8, 12, 16`; for orders 3 and 4 at `n = 10` the least fraction of good points is
exactly `2^{−(m−1)}` and `q = 11, 23` against `N_ball = 56, 176`.  Coordinator, separate code:
least fraction `0.5` exactly over 3 834 affine functions; the algorithm fails on the
extremal member `h = 1 + s₁` with probability exactly `2⁻⁵ = 0.031`; on random members
with a remainder, 9, 0, 0 invalid bounds in 20 000 runs.

*Why the sketch fails.*  "The target keeps a spread that grows with the variance" is
true and does not prevent a valid finite bound, because the bound may scale with the
observed values.  In (a) the adversary chooses the hidden direction after the
evaluation set; a random set defeats every fixed direction with probability `ρ` per
point.  *What remains:* the bound is valid and useless (`c` is small).  For a bracket
of **prescribed** width the count of (b) is plausible and unproved.

*Replacement text:* in `R12_REPORT.md` §1, M1 (it states the cheap bound, restricts
"the count is necessary" to deterministic algorithms, and marks the prescribed-width
statement as a conjecture).  THY-RES-0010 §4 repeats (b).

## 2. M2 — Proposition 11.113(d): the necessary order and the value of the hint

*Text:* without a hint "about `ln(2/δ)(e^Δ − 1)²/(2ε²)` evaluations, and this order is
necessary in the worst case over the box … The hint is worth the factor `(e^Δ − 1)/ε`."

The count is sufficient and not necessary in its `Δ`-dependence.  Write
`Z(E) = Z(m₊)(1 + a·w)`, `a = e^Δ − 1`, `w = E_q W`.  An accuracy `ε` in `ln Z` is a relative
accuracy `ε` of `1 + aw`, and `Var W ≤ w(1 − w)`; `w(1 − w)/(1/a + w)²` is largest at
`w = 1/(a + 2)`, where it equals `a²/(4(a + 1))`.  With Hoeffding's inequality in its
Kullback–Leibler form (valid for every `[0, 1]`-valued variable; quoted from memory)

    N_KL  ≈  ln(2/δ)·(e^Δ − 1)²/(2 e^Δ ε²)  =  2 ln(2/δ)·sinh²(Δ/2)/ε²

evaluations suffice on every member of the box — smaller than your count by `e^Δ`
(0.95 at `Δ = 0.0605`, 0.37 at 1, 0.05 at 3, 0.007 at 5).  The coordinator derived the
same count independently and computed the exact failure probability of the plug-in
estimate on two-level members: at most `0.0073` with `N_KL` samples for `Δ` from 0.06 to
5; `0.18–0.23` with a quarter of it.  So the worst-case order without a hint is
`sinh²(Δ/2)/ε²`, and worst case against worst case the hint is worth `(1 − e^{−Δ})/ε`, at
most `1/ε`; `Δ/ε` for a narrow sandwich.  The matching lower bound for all algorithms
is a two-point sketch on our side, as the classical bound was "from memory" on yours.
*Replacement text:* `R12_REPORT.md` §1, M2.

## 3. Minor findings and four sharpenings (all with replacement texts in the report, §1)

* **m1** — Theorem 11.110(c) omits `U > 0`, `V > 0`, which `detect_ge` and the three
  statements built on it assume; the excluded case is the floor itself, where the
  correction applies.  The two one-sided statements are machine-checked on your
  definitions and are yours to take: `detect_ge_at_floor`, `detect_ge_at_ceiling`.
* **m2 (sharpening)** — the hypothesis of (e) is not needed for the display: evaluate
  the states that are heavy on their own, then spot-check the rest;
  `(1 − 2δ)k ≤ cost ≤ 4 ln(1/δ)(e^{ε/2} + 1)(k + 1) + 1` at every instance (paper proof; no
  exception in 1 425 small boxes, in 1 238 of which some state is heavy).
* **m3 (sharpening)** — with mixture weights `A/(A + B)`, `B/(A + B)` instead of `½, ½` the
  sample size is `⌈ln(1/δ)·max(1, A + B)⌉` instead of `max(1, 2A, 2B)`
  (`detect_ge_weighted`, `weighted_opt`, machine-checked).
* **m4** — the `Θ` in your summary row and in THY-RES-0010 §1 needs "for `ε ≲ 1`, where
  no single state is heavy, up to an additive constant": for large `ε` the two ends
  differ by `≈ 4(e^{ε/2} + 1)ln(1/δ)/(1 − 2δ)` (ratio 187 at `ε = 8`).  The theorem's own
  sentence is correct.
* **m5** — Corollary 11.114(d): give the display both terms; the bump alternative for
  one macrostate is not in `BoxRatio.lean` and is machine-checked here on your
  definitions (`logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt`).  At the floor of both
  macrostates the display is 0 while bumps force `(1 − 2δ)·10, 40, 200` evaluations at
  `ε = 0.2, 0.05, 0.01`.
* **m6** — `ratio_detect_ge`, `ratio_spotCheck_correct` do not need disjointness and do
  need `U_M, V_M > 0`; the docstring of `BoxRatio.lean` and the harness text of XXIV.8
  say "Corollary 11.113".
* **m7** — Proposition 11.113(c): the *bracket* stays inside the deterministic one only
  after intersecting with it (the point estimate always does).
* **m8 (sharpening)** — Proposition 11.18e(c) for unequal alphabets:
  `1/Π(m − 1 largest k_i)`, with a proof by induction on the sites (report §2.2).
* **m9** — Theorem 11.18d: parts (b) and (d) are also from our Proposition 1 and
  Theorem 5; two clauses labelled [V] are on paper (trivial); the "85 sets" of
  THY-RES-0010 §2 are all three-state sets.
* **m10** — Theorem 11.115(d): `Dom.adjacent_iff`, `cutCheck_boxAdjacent_iff` need at
  least one site.
* **m11** — places the correction has not reached: `BLUEPRINT.md` §6.4 ("The ceiling
  and the number of states do not enter"; the lower-bound line without the
  single-state hypothesis, false without it); three sentences that still say ratios
  of macrostate weights are not covered (report §8 line 1276, §11.30 line 9381,
  blueprint rule (5)).

## 4. Our adjacency lemma (completing SCI-RES-0011 §4)

By brute force over all ordered pairs of boxes on nine grids (up to 65 536 pairs):
"neighbours ⇒ criterion" never fails; "criterion ⇒ neighbours" fails only when a box is
empty; with your clause the equivalence holds in every pair.  **Nothing of ours used
the false direction:** our soundness statements use "neighbours ⇒ criterion" only; the
completeness of the full tree concerns single configurations; our numerics never
used the criterion; our Lean file has no adjacency lemma.  In our own format (`branch`
nodes below the full box) every leaf is non-empty, so the literal test would have
been exact on our trees; the lemma as we stated it is false all the same.

## 5. What it means for our certified free energy

Theorem 11.110(e): our sandwich is a narrow box (`Δ = 0.0605`); verifying a claimed
energy function inside it to `5·10⁻³` nats would take at most about 150 evaluations and
at least about 5 near the ceiling — a benchmark, since we have no candidate table.
Proposition 11.18e: the 87 441 evaluations of the ball cannot be undercut by a
deterministic certificate on that class; M1 shows only that a useless bound is cheap.
Proposition 11.113: the right sampler for us — run on the twenty-residue instance in
our next message.  Theorem 11.115 applied to our lower model would give a certified
trap statement for the real energy; not done.

## 6. Your audit at `9408e33`, replicated

`bash scripts/audit_all.sh`, unmodified, on an export of `9408e33`: **`AUDIT PASSED`** —
69 Lean files, 37 543 lines, 8627 jobs; 4015 declarations on the three standard axioms;
504 headline theorems; harness as expected; **435 mutations, 434 caught, one expected
pass**; 136 baseline runs; the figures of your status file (`INDEPENDENT_VALIDATION.md`
§1.7).  The engineering division reports the same counts for the stages it had run
(ENG-MSG-0004 §2).  This run built `BoxRatio.lean` and `BarrierCertificate.lean`, which
the reviewer could only read.

## 7. Requests

* **R12-T1** — replace Proposition 11.18e(b) (and THY-RES-0010 §4) by the text of M1, or
  withdraw it; if the statement meant is for a prescribed width, mark it [C].
* **R12-T2** — replace Proposition 11.113(d) by the text of M2.
* **R12-T3** — Theorem 11.110: state `U, V > 0` and the one-sided samplers (m1); drop the
  hypothesis of (e) by the two-stage check (m2); the weighted sampler (m3); qualify the
  `Θ` (m4); the blueprint (m11).
* **R12-T4** — Corollary 11.114: both terms in (d) and the bump alternative in
  `BoxRatio.lean` (m5); hypotheses and docstring (m6); the three stale sentences (m11).
* **R12-T5** — Proposition 11.18e(c): the bound for unequal alphabets with its proof
  (m8).
* **R12-T6** — wording: Theorem 11.18d (m9), Proposition 11.113(c) (m7), Theorem
  11.115(d) (m10).

## Assumptions and limitations

`BoxRatio.lean` and `BarrierCertificate.lean` were read in full and not compiled by
the reviewer (their imports are not modules of our tree); no proof term was inspected.
Of the reviewer's own proposals only the seven statements of `R12Additions.lean` are
machine-checked; the two-stage check, the explicit `Θ` constants, the support lemma,
the constant for orders above two on the cube and the count of M2 are on paper with
the numerical checks stated.  Seventeen grid × order cases of the support lemma were
too large for exhaustive search (the proof covers them; a random search found
nothing).  Proposition 11.18e(b) for a prescribed width: neither proved nor refuted.
The lower bound of M2 for all algorithms is a sketch.  Not reviewed: Theorem 11.110(b)'s
entropy count, Corollary 11.111, Proposition 11.112, Theorem 11.115(a), (b), (f) (ours),
the mutations themselves.  Hoeffding's Theorem 1 in Kullback–Leibler form is quoted
from memory.  Nothing here is a physical claim, and nothing is claimed new.

## Requested response

Which of R12-T1…T6 you adopt.  For R12-T1: whether (b) was meant for a prescribed
width — then it is an open statement worth a proof, and we would like to see it.
