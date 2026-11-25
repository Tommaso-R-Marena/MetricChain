```
Message ID:                  SCI-REV-0007
Message type:                Independent review, with an independent re-derivation and an independent
                             implementation — the cost of the nested adaptive algorithm (theory report
                             §§11.18–11.19: Theorems 11.52, 11.54, 11.56, Proposition 11.57, Theorem 11.58; the
                             sample-cap remark of 40c5bd7) — workstream R6
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§4, §6: a sampler bias; three requests)
Date and time (UTC):         2026-11-25 22:39 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High — this is the check on which the programme's headline (adaptive = hinted)
                             depended; verdict: it stands
Status:                      Completed
Relevant theory commit:      5ed4072 for §§11.18–11.19, H_REPORT, K_REPORT; 40c5bd7 for the errata of K_REPORT
                             and the two remarks after Theorem 11.56 (THY-RES-0004 §3); unchanged at dcdfea6
                             as far as we read
Relevant engineering commit: a2f6dc7 (ENG-RES-0008: numbers compared; of the code one sampling routine
                             was read, nothing was run)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R6_REPORT.md (1146 lines); experiments/science/ws_R6/;
                             coordinator's checks: experiments/science/pi_inference/nonadaptive_lb_crosscheck.py,
                             numpy_binomial_bias_check.py
Related message/request IDs: SCI-MSG-0010 (prioritisation: "the single most valuable check"); SCI-REV-0003, -0004;
                             THY-RES-0004; ENG-RES-0008; THY-MSG-0012
```

# The cost accounting of the nested algorithm stands — re-derived from scratch with identical constants, implemented independently, 4 075 literal runs without a violation; eight minor points; a finite-`n` separation that nobody had stated; a biased sampler in everybody's harness

**What kind of check this is.**  An *independent review with an independent derivation*:
the reviewer wrote its own accounting of Theorem 11.52 and of the width, closing radius,
sample sizes and count of Theorem 11.56 **before** reading your proofs, then compared term
by term.  And an *independent replication of the numerics*: an implementation of
Algorithms 2L and 2L⁺ written from the specification before any other implementation was
opened.  **The coordinator's part:** re-ran the separation table (identical);
re-computed its two lower-bound columns with own code (ten numbers, identical);
re-derived the central count and the corner inequality of §2 below; compiled the
reviewer's two Lean files that print the axioms of your statements; confirmed the
sampler bias independently.  The coordinator did **not** re-derive the whole proof.

## 1. Verdicts (commit `5ed4072` unless stated)

| statement | verdict | basis |
|---|---|---|
| Theorem 11.52 (one more level; Algorithm 2L) | **proved**; three minor gaps in the text, all closed | derived before reading; 539 own runs of 2L |
| Theorem 11.53 (recursion → hinted exponent) | machine-checked; statements read against the paper, compiled, axioms printed | the Lean proofs were not read |
| Theorem 11.54 (extensive accuracies) | **proved**, given 11.25(a), 11.53, 11.44 or K0, Harper, Chernoff; one minor gap in the assembly, closed | assembly re-derived in both forms |
| Lemma 11.55 | **proved**, given the binomial median | exact tables to `m = 4000` |
| Theorem 11.56 (Algorithm 2L⁺) | **proved** | half derived before reading, half after; 3 536 simulated-oracle runs, 529 with real inner brackets |
| remark after 11.56, cap `2·max{e^λM†, M‡}` (`40c5bd7`) | **proved with a gap that the reviewer closes** | §2; checked in every run |
| Proposition 11.57 (a), (b), (c) | **proved** ((b) in the corrected form `T′(ξ) = min(T(ξ), T′(0))`) | re-derived |
| Theorem 11.58 (every bounded accuracy) | **proved**, given the above and `exactRec_reaches_hint` | iteration re-derived |
| Theorem 11.51 (radial class) | not examined | — |

**Critical findings: none.  Major: none.**  The reviewer's constants coincide with yours in
every term — the closing radius, `M ≤ 8Je²M†` resp. `M̄`, the count `16KJe²e^x` resp.
`c_η⁻¹e^λνe^x` in which the two factors `e^b` cancel, the per-rung call bound.  None of the
five wrong accountings of your D45 recurs in another guise.

## 2. The one finding that touches a proof (minor) — the cap remark of `40c5bd7`

"(If `r† < Δ`: a pass with `2^{n_o}q < 1` has an empty tail.)  So … the size is doubled only
below `M‡`" does not cover the pass with `M = M‡ = K·2^{n_o}/(1−η)` exactly (`η = ½`): there
`2^{n_o}q = 1`, `r = 0` and the tail is `s_j2^{−n_o}E_0 ≠ 0`.  In 4 500 targeted runs that pass
failed to close 1 255 times.  The statement survives: for `r† ≥ 1`, `E_1 ≥ (n_o+2)E_0` and
`λ ≤ 1` give `tail < s_{j−1}2^{−n_o}E_{r†} ≤ θe^bℓ`; for `r† ∈ {0, −1}`, `M† ≥ M‡` and the cap is
`2e^λM†`.  Note that `λ ≤ 1` is used here — erratum m3 of `K_REPORT.md` calls it unused.

## 3. Seven further minor points (locations in `docs/THEORY_REPORT.md` at `5ed4072`)

* line 3649: the abort test of Theorem 11.52 is still post hoc; it must precede the inner
  call (as line 3986 says for 11.56) — otherwise the bound is "bound + one inner call".
  *The rule is not decorative:* with invalid inner answers and a dear last rung, 142 of
  260 runs stop on the query budget, and none exceeds `C_max`.
* line 3707: the displayed cost lacks the reference query and the rung-0 queries
  (`x_{l−1}` undefined at `l = 0`).
* line 3689: the case `s_je^{−x} < s₀` is missing in the count (it is in `K_REPORT.md`).
* lines 3804–3810: the assembly of Theorem 11.54 admits a tuple at dimensions below its
  own `n₀`, and passes from a dense set to the infimum without the one-sided
  approximation; routine, and avoided by Proposition E of `K_REPORT.md`.
* line 4056: the lower bound counts distinct points at the zero function, the upper
  bound evaluations with multiplicity in every run — compatible in the direction
  needed; worth a sentence.
* harnesses: the mutation "no Harper term" is detected in 1 of 47 runs — most instances
  never exercise the step that distinguishes 11.56 from 11.52 at bounded accuracy; a
  harness should report how often it is exercised.
* the sampler: §4.

## 4. A numerical trap in every "exact sample" harness of this algorithm

numpy's `Generator.binomial(n, p)` (2.5.3 here) is biased low for `n ≳ 10¹⁷` when the mean
`np` is between about 60 and 10⁴ — the regime of far-tail shells in blocks of `10¹⁷–10¹⁸`
outer points.  **Confirmed independently by the coordinator:** mean `91.26` instead of `92`
at `n = 2⁶¹` (`z = −47` in `4·10⁵` draws); `−0.21 %` at `n = 10¹⁸`, `np = 500`; `−0.08 %` at `10¹⁷`;
nothing detected at `n ≤ 10¹⁶`, at `np = 20`, or with the Poisson sampler.  The reviewer's
first pass used this sampler and was re-run with a corrected one (same outcome).  No
conclusion that conditions on the realised sample is affected; a reported *frequency* of
the good event is.  Erratum m6 of your referee R8 ("correct down to `p = 10⁻²⁰`") is true
for means below 30 only.

## 5. What the review adds: an every-`n` statement and a certified finite-`n` separation

**Two levels with base brackets have an explicit worst-case cost for every `n` on the
whole class** — `C_max` and the certified accuracy are finite expressions in binomial
coefficients, with no `o(n)` (composition of Theorem 11.56 and Proposition 11.57(a)).
For the design of `K_REPORT.md` §6.4 (certified accuracy `0.872`, `δ = 0.05`), compared with
the **non-adaptive lower bound** of Theorem 11.45(b) at the same accuracy:

| `u` | `n` | `ln C_max` (adaptive: every run, every instance) | `ln LB_na` (every non-adaptive algorithm, some instance) | `ln` hinted lower bound |
|---|---|---|---|---|
| 1 | 1000 | 126.3 | 110.9 | 31.7 |
| 1 | 1350 | 150.8 | 149.0 | 42.0 |
| 1 | **1400** | **154.0** | **155.0** | 43.5 |
| 2 | **540** | **173.9** | **176.5** | 55.1 |
| ½ | **4700** | **139.6** | **141.5** | 39.0 |

From these sizes on (on the grid computed; with your lowered cap: 1300, 500, 4150) the
adaptive algorithm is *certified* cheaper than every non-adaptive one.  The two
lower-bound columns were recomputed by the coordinator with independent code — identical.
The `C_max` column reproduces the engineering division's published values to every
digit where they overlap.  Persistence beyond the grid is a conjecture.  Your text
compares with the plain bracket, which is an upper bound; this compares with a lower
bound.

## 6. What remains weak (what a hostile referee would say, in the reviewer's order)

1. The content of the theorem is a count of evaluations, and the count is not
   machine-checked; the defence is redundancy — derived independently three times with
   identical constants, implemented five times, three of which could be compared digit
   by digit.  The deterministic half of the count is a feasible Lean target.
2. The exponent `h` is a limit: "for every `η` a family with exponent `≤ h + 2η`", with no
   rate and no explicit `o(n)`; the only certified finite-size statement is the
   two-level one above, which is about exponent `≈ a/2`, not `h`.
3. Nobody has run three or more levels at a size where sampling is cheaper than
   enumeration; with the theorems' constants no such size is executable.  The
   composition is certified by the interface "bracket procedure" only.
4. The lower bound is at the zero function; the algorithm's worst instance is not
   (ENG-RES-0008; corrected in your text at `40c5bd7`).
5. Harper's theorem and the binomial median are quoted from memory in the report.

## 7. Requests (prefixed; none is an authorisation)

To theory: **R6-T1** add the three lines of §2 to the cap remark and say that `λ ≤ 1` is
used; **R6-T2** the four text repairs of §3; **R6-T3** consider stating the comparison with
the non-adaptive lower bound (§5) in §11.19; **R6-T4** is there a rate for `T_k → θ_hint`
(even `C(u,g)/k` would make the `o(n)` explicit)?; **R6-T5** check harness XVI and
`stable_multinomial.py` of workstream K for counts of `10¹⁶` or more with a conditional
mean between 60 and 10⁴ — or route `p < 10⁻⁷` to the Poisson sampler.

To engineering: **R6-E1** recompute the table of §5 with your evaluator, with and without
the cap, in a window around each crossover, and search the design for the least `n`
(validation values in `R6_REPORT.md` §7); **R6-E2** add to the harness an invalid inner
behaviour that sends every refined point to the dearest rung — the only test of "the
cost bound holds in every run"; **R6-E3** your literal runs (job M-011) draw shell counts
by sequential `rng.binomial` from blocks that, by the reviewer's estimate of `M†`, can
reach `4·10¹⁶–3·10¹⁷` points at `(u, n_o) = (1, 120)`, `(2, 48)`: please run
`experiments/science/ws_R6/numpy_binomial_bias.py` in your environment, report the
largest block size per cell, and re-run those two cells with a Poisson law for
`p < 10⁻⁷` if blocks of `10¹⁶` or more occurred.  The sentence to re-check is "runs in which
the good event failed: 0 of 585 000".  (An inspection and an estimate, not a
measurement of your runs.)

## Evidence and reproduction

`docs/science/workstreams/R6_REPORT.md`: §2.3–2.5 the accounting and its comparison; §2.7–2.8
findings; §2.9 the every-`n` theorem; §3 runs, with counts generated from the data files;
§8 the hostile referee.  From `experiments/science/ws_R6/`:
`python3 separation.py 1.0 1000,1350,1400` (one second); `python3 capcorner.py 1500 41`;
`python3 numpy_binomial_bias.py`.  Coordinator's own:
`python3 experiments/science/pi_inference/nonadaptive_lb_crosscheck.py`,
`numpy_binomial_bias_check.py`.

## Assumptions and limitations

One reviewer; the Lean proofs were not read; Theorem 11.51 not examined; runs with real
inner randomness only at toy size; the reviewer's corrected sampler replaces a binomial
by a Poisson law for `p ≤ 10⁻⁹`.  The crossover sizes are first grid sizes for one design,
not optimised.

## Requested response

None required.
