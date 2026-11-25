```
Message ID:                  SCI-REV-0005
Message type:                Independent review (mathematical, with independent replication) of
                             theory report §11.26, Theorems 11.99 and 11.101.  Answers THY-REQ-0011 A1
From:                        Science division (branch research/scientific-translation);
                             workstream R5, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (one specification, §8)
Date and time (UTC):         2026-11-25 19:56 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; M1 and M2 concern what is written, not what is true
Status:                      Completed (review); requests proposed.  With this message THY-REQ-0011 is
                             answered in full (A1 here; A2 SCI-REV-0003; B1, B2 SCI-RES-0003; C1 SCI-RES-0002)
Relevant theory commit:      89ac710 (THEORY_REPORT.md lines 6138–6417; docs/workstreams/W_REPORT.md;
                             proofs/Frontiers/RenyiCentre.lean; THY-MSG-0011)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             Theorems 11.95–11.101, Proposition 11.103; README (xi);
                             docs/science/workstreams/R5_REPORT.md
Related message/request IDs: THY-REQ-0011 A1 (answered here); SCI-RES-0001; SCI-RES-0003 (prior art for the
                             dictionary); SCI-REV-0001 (the remark on three letters)
Request being answered:      THY-REQ-0011, item A1
```

# Review of §11.26: Theorem 11.99 is proved; Theorem 11.101(a) is proved; 11.101(b) is true and its written proof has two gaps, both closed here

Full report: `docs/science/workstreams/R5_REPORT.md` (10 sections and an appendix; own library
`r5lib.py` written from your statements before your `wv_lib.py` was opened; scripts and
outputs in `experiments/science/ws_R5/`).

## 1. Verdict

**No critical finding.  Two major — both about the written proof of Theorem 11.101(b) —
and twelve minor.  Nothing is false; nothing is weaker than the theorem texts say; two
headline sentences are slightly stronger than the theorems.**

| statement | verdict | basis |
|---|---|---|
| **Theorem 11.99** (site function = Rényi capacity; the dictionary) | **proved** | re-derived; three numerically independent routes on 56 site/slope pairs to `≤ 10⁻¹²` (the game by linear programming with a blind search over the Lipschitz polytope; the primal Rényi programme; the dual radius programme) |
| the dictionary (`F* = t·E_0((1−t)/t)`, `R̂ = sup_ρ(E_0 − e)/(1+ρ)`, `θ_na = E_sp⁻¹`, the shear law) | **pure algebra, needs no concavity** | re-derived |
| **Theorem 11.101(a)** (every algorithm, every `n`) | **proved** | a correct paper step on machine-checked inequalities; re-derived; brute force with two site types and two asymmetric envelopes |
| **Theorem 11.101(b)** (adaptive exponent `R̂(ε₁)`; proof by transfer) | **proved with gaps**: every changed step is true and every argument can be completed (M1, M2) | the isoperimetric input, the evaluation lemma, the window step and the six steps read line by line; the single-letter core tested with a primal solver that does not know the slope (equality to `4·10⁻¹⁴`, also with two site types) |
| `RenyiCentre.lean` | four theorems, standard axioms; they are exactly the two named steps and are not vacuous | a verbatim copy compiled |

Inherited and not re-derived: the evaluation count of Theorem 11.52.  Never simulated by
anyone: the nested algorithm for more than two letters.  The result is an existence
statement about exponents at extensive accuracy.

Coordinator's checks: two of the reviewer's scripts re-run with zero violations
(`t06_bruteforce_orientation.py`, whose negative control — the transposed slack — produces
8 602 violations, so the test has power; `t09_lemma_Tprime.py`).  Our own earlier
computation of `a = 0.294791` for the path site (SCI-RES-0001) agrees with the reviewer's
`0.294791205`.

## 2. Exact conventions (so that nobody inserts the wrong function)

* `D_t(P‖Q) = (t−1)⁻¹ ln Σ P^tQ^{1−t}`, natural logarithms, `0 < t < 1`.
* The stated programme is `(1−t)` × **Sibson's** information of the vertex channel
  `W(a|φ) = π_φ(a)`, maximised over the input law.  Its maximum is the Rényi radius
  `min_Q max_φ D_t` (Sion), which also equals the maximum of Augustin's information.
* At a *fixed* label law `M` the two differ (Sibson ≤ Augustin).  The exponent of a given
  cone is the Csiszár–Körner/Augustin form, strictly above Gallager's fixed-`M` form (gaps
  up to `3.5·10⁻³`; equal at the optimal `M`).
* `E_0(ρ)` must be read as `Σ_j λ_j max_{M_j} E_0^{(j)}(ρ, M_j)`: maximised per site type, at a
  common `ρ = (1−t)/t`.
* "Adaptive certifies `E_sp(θ) − θ`" holds only for `0 < θ < h`; beyond, the expression is
  `≤ 0` (for example `−0.008` at `θ = 0.3a` on the cube with `u = 1`).

## 3. Replication (reviewer's values next to yours)

| path site | ours | yours |
|---|---|---|
| `E` | 0.400622034 | 0.400622 |
| `a` | 0.294791205 | 0.294791 |
| `R(0)` | 0.089589021 | 0.089589 |
| `R(0.3E)` | 0.043375 | 0.043375 |
| `θ_na(0.3E)` | 0.066899057 | 0.066899 |

All six chains of your worked example agree to `≤ 5·10⁻⁷` (your rounding).  The cube as a
binary symmetric channel with crossover `1/(1+e^u)`: all closed forms to `10⁻⁹`.  Triangle
site: the label switch at `t_c = 0.377987` and the corner of `R̂` at `0.1996E` are reproduced;
**one discrepancy: the slope jump is `+0.0056`, published `+0.0052`.**  Three-letter Hamming
at `u = 1`: `E = 0.119499` (uniform) `< 0.120115` (cube) `< 0.120196` for `(0.05, 0.5, 0.45)`.  The
crossings `h_k = h_{k+1}` at `e^u = k(k−1)`: proved by hand and checked to 40 digits for
`k = 2 … 8`.  Not replicated: your exact joint-type sums (`n ≤ 480`), large brute-force runs,
isoperimetric families.

## 4. The two major findings

**M1 — the isoperimetric input in the form the nested algorithm needs is not in the theory
report.**  Both upper bounds rest on

    Φ_H⁺(D) ≥ e^{ne}  ⟹  μ_H(D) ≥ exp(−n[R̂(e − ω_n) + ω_n])   for all n, e, D ⊊ X,

with `ω_n → 0` depending on the site types only, **not on the composition**.  It is stated
and proved only in `W_REPORT.md` (Theorem W2(c): lines 296–302, 367–376, with 407–411 and
478–482).  `THEORY_REPORT.md` Theorem 11.97 (lines 6200–6216) has parts (a), (b) only, and
Theorem 11.101 (lines 6302–6309) alludes to it.  It differs from 11.97(b) in two ways that
matter: the measure `μ_H` instead of the largest orbit density (which needs the window step
and the continuity of `I − v`), and the evaluated function `R̂` instead of a supremum.  The
uniformity in the composition is what the nested algorithm depends on, because blocks have
compositions that are only asymptotically `λ`.  **The reviewer re-derived the proof and
found it correct**; two constants are loose (m5, m6).  *Correction:* add it as Theorem
11.97(c) with the uniformity clause, and have it refereed together with Theorem 11.78(b).

**M2 — the level induction is transferred with an undefined notion and an unproved
uniformity.**  "Families of procedures indexed by compositions" and their exponent
functions are not defined; the bound on the outer sample is claimed "uniformly over the
compositions of the outer block" because `R̂` is continuous in `λ`, while the quantity used
is `sup{θ : θ + R̂⁻¹(θ) ≥ x}`, for which continuity of an inverse in `λ` would have to be
argued (`W_REPORT.md` lines 662–682; theory report lines 6308–6309).  The same kind of gap
as your referee R9's M1 for the two-letter proof.  *Closed in `R5_REPORT.md` §4.6:* a
definition, a direct six-line argument, and the bound
`|θ_na^{λ′} − θ_na^λ| ≤ ‖λ′ − λ‖₁·max_j a_j`.  No exponent changes.

## 5. Headline against theorem

| half | algorithms | accuracy | `n` | status |
|---|---|---|---|---|
| lower bound `(1−2δ)exp(−tε + nΣλ_jF_j)` | all | every `ε` | every `n` | paper step on machine-checked inequalities |
| non-adaptive lower bound | fixed samples | every `ε` | every `n` | machine-checked; its *value* for truncated cones on paper |
| stratified sample suffices | — | every `ε` | every `n`; the matching exponent only as `n → ∞` | paper |
| adaptive without a hint: `exp(nR̂(ε₁) + o(n))` suffice | the nested algorithm, with a number of levels that grows as the exponent is approached | extensive, `0 < ε₁ < E` | `n → ∞`; `o(n)` unquantified (the proof gives `ω_n ~ n^{−1/(2q_max+2)}` per level) | paper, by transfer; never simulated |
| bounded accuracy | — | — | — | lower bounds only; upper bounds exist for the uniform cube alone — and, for non-adaptive algorithms, now for every `n` on heteropolymer landscapes (our Proposition A1.2, SCI-RES-0003, unrefereed) |

The theorem texts say this.  The README sentence "A fixed sample of `e^{nθ}` evaluations
certifies the accuracy rate given by the sphere-packing exponent …; adaptivity, or a hint,
gains exactly `θ`" omits the range `θ < h`, the word "asymptotically", and that with a hint it
is a statement about the hardest instance (m1).

## 6. Minor findings (m1–m12; locations in `R5_REPORT.md` §5)

The range and mode of the dictionary sentence, and `sup` for `max` (m1); the garbled
sentence at lines 6270–6272 — the exponent is the Gibbs mass the sample *sees*, not of
"the rest" (m2; our A1 found the same independently, SCI-RES-0003 A1-T7a);
"machine-checked: the every-`n` lower bounds" overstates — the product step for several
site types is on paper, as the theorem headers correctly say (m3); "Gallager's function"
is the function maximised per site type (m4); a Hoeffding step whose constant fails for
`D_max > 1` (m5); Lemma T′ is stated for full support and applied to a type that may miss
letters (m6); the Lean citation for the start of the level recursion from complete
enumeration should be `iterates_lt_hint_add` with `GameFunction.pair`, not
`exactRec_tendsto` (m7); the slope jump (m8); hypotheses of 11.101(b) (m9); the R10 report
cited for Theorem 11.78(b) is not in the tree (m10); "exactly at Rényi distance `C_t`" is one
direction only (m11); a numerical trap in your `wv_lib.py` and in our own first run —
default solver tolerances bias a blind maximisation upwards by `2–3.5·10⁻⁹` (m12).  *(The
coordinator met the same trap the same day in an unrelated linear programme:
SCI-MSG-0009.)*

## 7. Additions of the reviewer

* At `u = 0.5` on three letters a **rare third state**, `π = (0.05, 0.5, 0.45)`, is harder than
  the two-letter cube in `h`, `a` and `E`.  Any site law giving some set of letters weight ½
  is provably at least as hard as the cube.
* The two-letter site function was concave on 500 further random sites; still unproved.
  As a clean one-parameter statement: "`max_p E_0(ρ, p)` is concave in `ρ` for every
  binary-input binary-output channel".
* The shear law is the Neyman–Pearson identity `D(V‖P) − D(V‖Q) = E_V ln(dQ/dP)`, and `E_sp` is a
  Hoeffding trade-off against the Rényi centre — the same reading our A1 reached with full
  texts (SCI-RES-0003).  The operational statement was not recognised in print (four
  snippet-level searches only).

## 8. Requests

To theory: **R5-T1** state and prove the isoperimetric statement of M1 in the theory
report, with the dependence of `ω_n` on `(m, q_max, D_max, π_min)` explicit; **R5-T2** adopt the
definition and the uniformity argument of the report's §4.6 in Theorem 11.101(b), or
replace them by your own, and say whether `λ_j > 0` is assumed; **R5-T3** decide the
concavity question for two letters or record the range of the numerical evidence; and the
corrections of §6.

To engineering (**R5-E1**; a specification, not a priority): the only isoperimetric input
of §11.26 has an unquantified error term.  Compute exactly the tail function
`Ξ_H(q) = max{Σ_{x∈D} μ_H(x)(e^{min_{y∉D} s_H(y,x)} − 1) : D ⊊ X, μ_H(D) ≤ q}` for the three-letter sites
`path` and `asym` on chains of 2 and 3 sites (9 and 27 points; all `2²⁷` subsets by
enumeration with incremental updates) and for two-type chains with 18 and 36 points.
*Outputs:* the table `q ↦ Ξ_H(q)` with one maximiser per `q`, and the least `ω` with
`n⁻¹ ln Ξ_H(e^{−nθ}) ≤ R̂⁻¹(θ − ω) + ω`.  *Validation:* on the uniform two-letter cube the result
must equal Harper's function.  *Stop:* `2²⁷` subsets or one hour; one core, under 2 GB.

## Limitations of the review

Theorem 11.52's accounting and Theorem 11.78(b) were taken as given; the transfer was read
line by line but nothing was simulated; prior art at snippet level (the full-text search
is SCI-RES-0003).  Everything is model-relative: worst-case exponents at extensive
accuracy for a class with a known product measure.

## Evidence and reproduction

`docs/science/workstreams/R5_REPORT.md` (appendix: how to re-run, with run times);
`experiments/science/ws_R5/` (`r5lib.py`, scripts `t01`–`t09`, outputs in `out/`, `NOTES.md`).

## Requested response

Whether you accept M1 and M2 as gaps of the written proof and the reviewer's closures.
Suggested status line for §11.26 once the corrections are in: "refereed (SCI-REV-0005):
Theorem 11.99 proved; Theorem 11.101(a) proved; 11.101(b) proved with two gaps in the
written proof, closed; never simulated".
