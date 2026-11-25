# R5 — Referee report on theory report §11.16 ("Without a hint: Monte Carlo is optimal among non-adaptive algorithms")

Reviewed at commit `36ec238`: `docs/THEORY_REPORT.md` §11.16 (Lemma 11.43, Theorems 11.44–11.45,
Proposition 11.46, table, heuristic paragraph), row G18, §12 item 2(d); `proofs/Frontiers/NonAdaptive.lean`;
witnesses `cube_nonadaptive_witness`, `tail_lemma_witness`; harness XIII.1–XIII.4; benchmark B12 and its
stored output; README ("Since the last review"); `docs/RESEARCH_LOG.md` (Cycle 10).  While I worked, other
processes changed the working tree (§11.17, `LinearClass.lean`, the harness after XIII, counts in the log);
`git diff HEAD` shows no change in any file or passage listed above.  Everything below is my own work in
`<session scratch>/referee5/` (scripts at
the top level, logs in `out/`, Lean scratch file in `lean/`); nothing in the repository was modified, and
I did not run `lake build`, the audit script or the author's harness.

## 0. Summary

**No lemma, theorem or proposition of §11.16 is false as stated.**  Lemma 11.43, Theorem 11.44(a,b,c),
Theorem 11.45(a,b,c) and the bracket of Proposition 11.46 are correct (11.43(b) needs `D ≠ X`); I re-derived
each with its constants, checked the combinatorial core exhaustively (all `2³² − 2` proper non-empty
subsets of the 5-cube), reproduced every quoted number with independent code, and compared each Lean
statement with the prose.

What is wrong is in the remarks and summaries: scope, labelling and attribution — the kinds of defect
earlier referees found:

1. **Bounded accuracies are not covered (MAJOR).**  Theorem 11.44 certifies *nothing* below the accuracy
   `ln 2 + ln(1 + min_{r≥1} Γ_n(r)) + ln(1/δ₂) ≈ ln(2(1 + 4eᵘ(eᵘ−1))) + ln(1/δ₂)` (`2.36, 3.67, 5.94 + ln(1/δ₂)`
   for `u = ½, 1, 2`), and just above it gives an exponent strictly larger than `KL(p_u‖½)`.  So "their
   sample size is now a theorem on the class and replaces the Chebyshev bound" is true only for
   accuracies `ε → ∞`; for bounded `ε` Chebyshev (`ln cosh u`) remains the only hint-free upper bound
   proved in the report, and "the non-adaptive exponent is exact" is proved for extensive accuracies only.
   The gap closes with a second use of Harper's theorem (Appendix B: `Γ` replaced by a `Γ'` that tends to
   `0` exponentially below `p_u`; then the exponent `KL(p_u‖½)` holds for every fixed `ε > 0`, without
   recentring) — my derivation, tested numerically, not refereed by anyone else.
2. **Prior art is missing (MAJOR).**  Mathé–Novak, *Simple Monte Carlo and the Metropolis algorithm*
   (J. Complexity 2007), prove a lower bound for all **non-adaptive** methods on a class of log-Lipschitz
   (log-concave) densities by the same construction in a neighbouring setting — cones `exp(−α‖y − y_i‖)`
   with hidden centres, pairs that differ only on a ball around the centre, Bakhvalov averaging — and
   remark that an adaptive method identifies the centre at once.  G18's "the matching non-adaptive lower bound was not found" is
   not tenable as written.  The exact exponent on the cube, for `ln Z`, with the matching class-wide upper
   bound, I did not find anywhere.
3. **Machine-checked status is overstated (MAJOR, labelling).**  Lean contains part (a) of the tail lemma,
   the abstract packing bound, and its cube instance *conditional* on two finite sums.  Not
   machine-checked: Lemma 11.43(b) (not only Harper's theorem, also its reduction), the closed forms `D_R`
   and `|B(R−1)|`, every asymptotic statement, hence the sentence "the non-adaptive exponent is exactly
   `θ_na`", which stands under a header tagged **[V]**.
4. Minor: `D ≠ X` and the form of Harper's theorem needed in 11.43(b); the doubling algorithm of 11.46
   needs a union bound over stages and a convention at `r̂ = 0`, and proves "no hint is needed" only for
   `ε > 2`; the adaptive-stopping remark is a sketch whose conclusion (worst case over cones, constant
   `(1−2δ)²/2`) is not stated; Proposition 11.46 has no harness test; "the same samples" are two
   independent samples; small mismatches listed in §2.

Two things the section could claim and does not: (i) the bound of Theorem 11.45(b) provably fails on
cones for adaptive algorithms that are correct on the **whole** class (`n + 3` evaluations, Appendix D);
(ii) at extensive accuracy the two sides appear to differ by a bounded factor, not only by `e^{o(n)}`
(numerically `R* − r = 12` both at `n = 1600` and at `n = 6400`, `u = 1`; `5` and `6` for `u = 2`).

## 1. Verdict per statement

| statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|
| L 11.43(a): `w(z) ≤ t ⇒ w(x) ≤ t e^{β d(z,x)}`; `Σw ≤ Σ min(w,t) + t Σ_D (e^{β dist(Dᶜ,x)} − 1)` | **yes**, also for asymmetric `d`, orientation as written | re-derived; Lean statements read, type-checked (`#check`, axioms standard); 21 714 threshold checks, `n ≤ 8` | one line | elementary | needs `Dᶜ ≠ ∅`; `t > 0` is automatic; Lean needs no envelope axiom |
| L 11.43(b): `|D| ≤ |B(r)| ⇒ Σ_D (e^{u dist(x,Dᶜ)} − 1) ≤ 2ⁿ(e^{Δ_r} − 1)` | **yes** for `D ≠ X` | re-derived in complement form (Appendix A); **exhaustive for `n ≤ 5`**; adversarial `n ≤ 8` | short | routine corollary of Harper; distance functions as extremal Lipschitz functions are classical (cf. Dzindzalieta 2013) | proof sketch needs the nested/strict form of Harper, or complements; not machine-checked |
| "equality for balls", "truncated cones attain equality" | yes (balls with `r < n`; thresholds at level values) | algebra; 3 154 tight cases found numerically | — | — | not tight when `|D|` is not a ball size: the exact extremum is the complement of an initial segment of the simplicial order (verified `n ≤ 5`) |
| T 11.44(a): lower tail `e^{−K/8}`, upper tail `δ₂` | **yes** | re-derived (Chernoff `P(S ≤ (1−η)μ) ≤ e^{−η²μ/2}`, `η = ½`, `μ ≥ K`; Markov); simulation with `K = 2, 4, 8` | routine | not found in this form | deterministic step tight at the cone up to `e^{1.0–1.9}` (`u = 1`, `r/n ≥ 0.385`) |
| T 11.44(b): recentred estimate | **yes** | re-derived; end-to-end simulation (coverage ≥ 0.988 against 0.90 required) | routine | — | **void** for `ε < ln(2(1+min Γ)) + ln(1/δ₂)`, never usable for `ε < ln(2/δ₂)` |
| T 11.44(c): `n⁻¹ ln Γ_n(ρn) → KL(ρ‖p_u)` on `[p_u, ½]`, `→ 0` below | **yes** | analytic; numerics `n = 10³, 10⁴, 10⁵`, `u = ½, 1, 2`, nine values of `ρ` | Stirling | — | below `p_u`: `Γ_n(ρn) → (eᵘ−1)/(a(1−aeᵘ))`, `a = ρ/(1−ρ)`, a constant `≥ 4eᵘ(eᵘ−1)`; at `p_u`: `Γ` grows like a power of `n` (about `√n`); above `½`: exponent `uρ − Λ₁` |
| T 11.44(c): `e^{nθ_na(ε₁)+o(n)}` samples suffice, `0 < ε₁ < ln cosh(u/2)` | **yes**, for fixed `ε₁ > 0` | re-derived | — | apparently new | fails to say anything for bounded `ε` (M1) |
| "the cone is the worst member"; "their sample size is now a theorem on the class and replaces the Chebyshev bound" | **partly** | numerics at the cone (§3, item 3); table of M1 | — | — | exponent-level and for `ε → ∞` only; overstated for bounded `ε` (M1).  The attribution to Chatterjee–Diaconis is accurate |
| T 11.45(a): non-adaptive packing bound | **yes**; Lean = prose | proof read line by line; scratch re-proof with a weaker hypothesis type-checks | short | known method (Bakhvalov averaging over hidden bumps) | `hna` quantifies over all functions; class members suffice |
| T 11.45(b): cones against flattened cones | **yes** | Lean read; closed form `D_R`, difference set, admissibility, ball count by brute force (`n ≤ 10`, 2 874 cases) | short | construction of Mathé–Novak 2007 moved to the cube and to `ln Z` | Lean statement is conditional on two finite sums; closed forms are paper |
| T 11.45(c): `n⁻¹D_{ρn} → KL(ρ‖p_u)`; "exponent exactly `θ_na`" | **yes**, for extensive accuracies, fixed `δ < ½`, same convention on both sides | analytic; numerics to `n = 10⁵`; finite-`n` sandwich recomputed | — | apparently new | tagged [V], is [P] + [K] (M3) |
| "the pairs of (b) do not bind adaptive algorithms" | **yes**, and more is true | brute force (`n ≤ 8`); Lean scratch `adaptive_escapes_packing` | — | observation of Mathé–Novak (Remark after Thm 3) | on cones a class-correct adaptive algorithm needs `n + 3` evaluations (Appendix D) |
| adaptive-stopping remark **[P]** | correct in the form of Appendix C | full proof written out | short | — | sketch gives one step; conclusion and constant missing |
| P 11.46: bracket with `K = 24 ln(4/δ)` | **yes** (needs `M ≥ 2K`) | re-derived: failure bounds `e^{−K/4}, e^{−K/6}, e^{−K/16}, e^{−K/24}`, sum `≤ 0.34 δ`; exact binomial tails; simulation | routine | sample splitting + truncation are standard | no harness or benchmark test exists |
| P 11.46: zero residual, `M ≥ 2K·2ⁿ/|B(k*(ε−2)−1)|`, `ε > 2` | **yes**, except the edge case `k*(ε−2) = 0` | algebra (`ln(3/2) + ln(1+e^{ε−2}) ≤ ε` iff `ε ≥ 0.632`) | — | — | bracket is never narrower than `ln 3` |
| P 11.46: doubling algorithm correct on the class; cost claims | **gap** (union bound over stages); cost claims right at exponent level | re-derived: width `≤ ln 3 + ln(1 + 4Γ_n(r̂))` on the good event | — | — | fix in §2, m3 |
| Table; `θ_hint < θ_na`; common leading term; factor `→ 4`; `0.0291/0.1109`, `0.0077/0.0303`, `0.0973/0.3278`; `0.0293/0.0307/0.0283` at `n = 6400` | **all reproduced** | own code (`mpmath`, exact integers) | — | — | lower side uses `δ = 0.05`, upper side total failure `0.10` |
| heuristic paragraph | labelled as heuristic; nothing false found | read | — | — | "costs at most `e^{nθ_hint}`" rests on hand calculations with no artifact |

### 1b. Answers to the seven questions

**Q1 (Lemma 11.43).**  (a) Correct for asymmetric envelopes with the orientation written: admissibility
gives `g(z) − g(x) ≤ d(z,x)`, so `w(x)/w(z) ≤ e^{β d(z,x)}` with `z` outside `D` in the *first* argument;
`dist(Dᶜ, x) = min_{z∉D} d(z,x)` is the right quantity (the reversed orientation would be wrong).
`sum_le_truncated_add_tail` says what the prose says and slightly more: `ρ` is any function with
`d(z,x) ≤ ρ(x)` for *some* `z` of weight `≤ t`; `X` finite; `β ≥ 0`; no triangle inequality; if no point lies
above `t` both sides are equal, and if every point lies above `t` the hypothesis cannot be met (prose: the
right-hand side is `+∞`).  (b) Correct for `D ≠ X`.  Version of Harper used: *for every `m` the initial
segment `I_m` of the simplicial order minimises `|N(A)|` over `|A| = m`, and `N(I_m)` is an initial segment*;
corollary: `|A| ≥ |B(k)| ⇒ |N^t(A)| ≥ |B(k+t)|`.  The report's route (`N^{j−1}(D_j) ⊆ D`, "so
`|D_j| ≤ |B(r+1−j)|`") needs the **strict** statement `|S| > |B(k)| ⇒ |N^t(S)| > |B(k+t)|` for `k + t < n`; it is
true (an initial segment longer than `B(k)` contains a point of weight `k+1`, whose `t`-neighbourhood
reaches weight `k+t+1`) but does not follow from the ball corollary alone and fails at `k + t = n`.  The
complement form avoids both points: `D_j = X ∖ N^{j−1}(Dᶜ)`, `|Dᶜ| ≥ |B(n−r−1)|`, hence
`|D_j| ≤ 2ⁿ − |B(n−r+j−2)| = |B(r+1−j)|` (Appendix A).  When `|D|` is not a ball size the bound holds and is not
attained; the exact maximum of every `|D_j|` simultaneously is at the complement of an initial segment
(exhaustive, `n ≤ 5`).  "Equality for balls": yes for `r < n`.  "Truncated cones attain equality": yes when
the threshold is one of their level values.

**Q2 (Theorem 11.44).**  All constants re-derived (see table).  `t* = w_(m)`, `m = ⌈2ⁿK/M⌉`; ties are harmless
(`|{w > t*}| ≤ m − 1`, `P(w ≥ t*) ≥ K/M`); `r = 0` forces `D = ∅`.  The limit in (c) is right on `[p_u, ½]`,
below `p_u` (limit `0`, but `Γ_n(ρn)` itself tends to a constant `≥ 4eᵘ(eᵘ−1)`, not to `0`), at `p_u`
(`Γ` of order about `√n`) and at `½` (`ln cosh(u/2)`).
`M = e^{nθ_na+o(n)}` is right for every *fixed* `ε₁` in the range.  For `ε = o(n)`: the theorem gives
`KL(p_u‖½) + o(1)` if `ε → ∞`; for bounded `ε` it is void or strictly worse (M1).  "The cone is the worst
member" is justified only in the sense that the class-wide bound has the exponent of the cone
(numerically the deterministic step is attained by the cone up to a factor `e^{1.0–1.9}` for `u = 1`,
`r/n ≥ 0.385`); it is not proved as an extremal statement.  The attribution is accurate: Theorem 1.1 of
Chatterjee–Diaconis gives `n = exp(L ± t)`, `L = D(ν‖μ)`, with `I_n(1) = Â/A`, and
`D(π_cone‖uniform) = n KL(p_u‖½)`; but they obtain relative error `→ 0` at that sample size (times
`e^{O(√n)}`), and Theorem 11.44 guarantees no better than a factor `2(1 + Γ) ≥ 39` there (`u = 1`).

**Q3 (Theorem 11.45).**  (a) In Lean a deterministic non-adaptive algorithm is a `QueryAlgorithm` with
`queries g = Q` for **all** functions `g`; by `consistent` its output is then a function of `g|_Q`.  A
randomised one is a finite mixture; `E|Q|` counts distinct points; plain Monte Carlo on the cube is such a
mixture.  This is the standard notion (nodes independent of function values, random cardinality
allowed).  The hypothesis is stronger than needed — only `hna ω (g j)` is used
(`Referee5.nonadaptive_on_class` type-checks).  The bound does fail for adaptive algorithms, in three
senses of increasing strength: the abstract statement (a) without `hna` is false
(`Referee5.adaptive_escapes_packing`: three sensitive pairs, capacity 1, an exact algorithm with two
evaluations); on the family of cones and flattened cones `n + 2` evaluations suffice; and an adaptive
algorithm correct on the **whole** class makes `n + 3` evaluations on every cone (Appendix D).  Whether
the *worst case over instances* obeys the bound is the open problem.  (b) All verified.  (c) Yes: both
theorems use width `ε` and `(ε/2, δ)`-correctness; lower bound `(1−2δ)2ⁿ/|B(R*−1)|`, upper bound
`K·2ⁿ/|B(r)|` with `δ = e^{−K/8} + δ₂`.  The stopping remark is a sketch; Appendix C completes it.

**Q4 (Proposition 11.46).**  The three estimates and the bracket are right (table).  Zero residual: width
`ln(3/2) + ln(1 + e^{Δ_r̂})`, sample size as stated for `ε > 2`; against Theorem 11.25(c) the cost is larger
by a constant (at most `16·24 ln(4/δ)/ln(1/δ)` with doubling) and by `ε − 2` in place of `ε − 1` — a bounded
factor at extensive accuracy.  The doubling algorithm is *not* shown correct as written: with the same `K` at every stage the
failure probability is bounded only by (number of stages)·`δ`.  "Never more than the Monte Carlo cost up
to a polynomial factor" is justified at extensive accuracy (on the good event the width is at most
`ln 3 + ln(1 + 4Γ_n(r̂))`, which is below `ε` whenever the condition of Theorem 11.44 holds at the radius
`r̂` with `δ₂ ≤ 1/6`; the sample sizes at equal radius differ by the constant `2·24 ln(4/δ)/K`).

**Q5.**  Every number reproduced (§3, item 5).  Leading term and limit ratio 4 confirmed analytically and
numerically.

**Q6.**  §4.  The method of 11.45 is known; the hard family is Mathé–Novak's; the exponent on the cube
and Theorem 11.44 were not found; Lemma 11.43(b) is a routine corollary of Harper.

**Q7.**  §5.

## 2. Errors and gaps

No CRITICAL finding.

### MAJOR

**M1. Bounded accuracies: Theorem 11.44 is void there, and three sentences claim more than it gives.**
Location: remark after Theorem 11.44 ("so their sample size is now a theorem on the class and replaces
the Chebyshev bound `ln cosh u`"); opening paragraph ("This section proves that value on the whole
class"); research log, same sentence; G18 and §12 2(d) ("exactly … (`≈ u²/8` at `ε₁ → 0`)") which do not
say "for extensive accuracies"; section title.
Facts (own computation, `n = 4000`, `δ₂ = 0.05`; script `check_small_eps.py`):

| `u` | least `ln(2(1+Γ_n(r)))`, `r ≥ 1` | Thm 11.44 at `ε = 1` | at `ε = 7` | at `ε = 10` | Thm 11.45 lower bound at `ε = 1` | `KL(p_u‖½)` | `ln cosh u` |
|---|---|---|---|---|---|---|---|
| ½ | 2.356 | void | 0.0339 | 0.0239 | 0.0297 | 0.0303 | 0.1201 |
| 1 | 3.671 | void | 0.1647 | 0.1040 | 0.1094 | 0.1109 | 0.4338 |
| 2 | 5.935 | void | void | 0.3450 | 0.3252 | 0.3278 | 1.3250 |

("void": no radius `r ≥ 1` satisfies `ln(2(1+Γ_n(r))) + ln(1/δ₂) ≤ ε`, so the theorem asks for `M ≥ K·2ⁿ`.)
The stored benchmark shows the same thing: B12, `u = 1`, `n = 100`, `ε = 3.0`: `r0 = None`, `upper = 0.72491 > ln 2`.
Counter-statement: for `u = 1`, `δ₂ = 0.05`, every `n ≥ 100` and every `ε < 6.6`, Theorem 11.44 certifies no
sample size below `K·2ⁿ` (and for no `u`, `n` anything below `ε = ln(2/δ₂)`); whatever `δ₂ < ½` is chosen,
the void range reaches at least `ln 4 + ln(1 + min_r Γ_n(r)) ≈ 4.36` for `u = 1`.  The best hint-free bound
proved in the report at such accuracies is still Chebyshev's `(cosh u)ⁿ/(δ(1−e^{−ε/2})²)` of Theorem 11.25.
For `ε = 7`, the certified exponent `0.165` exceeds the lower bound `0.091` (`n = 4000`) and
`KL(p_u‖½) = 0.111`.
The cause is the step `E min(w,t*) ≥ t* K/M`, which ignores the mass below the threshold; as a result
`min_{r≥1} Γ_n(r)` does not tend to `0` but to `4eᵘ(eᵘ−1)` (`18.54, 18.67, 18.68` at `n = 10³, 10⁴, 10⁵` for `u = 1`).
The limit is approached **from below** (`17.51` at `n = 100`, `16.68` at `n = 50`), so "`Γ` stays above
`4eᵘ(eᵘ−1)`" is not a correct finite-`n` statement; "`Γ_n(r) ≥ c(u) > 0` for all `r ≥ 1`" is.
Fix (Appendix B): bound `E min(w,t*)` from below by Harper as well.  With
`Γ'_n(r) = Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1) / Σ_j C(n,j) e^{−u(j−r+1)₊}` one has `A ≤ (1+Γ'_n(r)) E min(w,t*)`,
`n⁻¹ ln Γ'_n(ρn) → −KL(ρ‖p_u)` below `p_u`, and `(1−η)/(1+Γ') ≤ Â/A ≤ 1 + η + Γ'/δ₃`.  Then the exponent
`KL(p_u‖½)` holds for every fixed `ε > 0` and matches Theorem 11.45 there.  Until something like this is
written and refereed: restrict the three sentences to "extensive accuracies (and `ε → ∞`)", and keep the
Chebyshev bound for bounded `ε`.

**M2. Missing prior art; G18 mis-states what was not found.**
Location: G18 ("its validity on a Lipschitz class and the matching non-adaptive lower bound were not
found"), §11.16 (no reference for the construction), §13.
P. Mathé, E. Novak, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 23 (2007)
(arXiv:math/0611285; I read §§1–4.1 and §5 in full).  Setting: `S(f,ρ) = ∫fρ/∫ρ` from oracle values of `f`
and of an unnormalised density `ρ`; they note the Boltzmann/partition-function reading.  Theorem 3: a
lower bound `2^{−d/2−3/2}(vol Ω/vol B^d)^{1/2} α^{d/2} (d!)^{−1/2} n^{−1/2}` for **every non-adaptive** Monte Carlo
method on log-concave densities with `|log ρ(x) − log ρ(y)| ≤ α‖x−y‖`, proved by Bakhvalov's averaging over
`ρ_i = c_i exp(−α‖y − y_i‖)` with `2n` hidden centres and integrands `±c̃_i 1_{B_i}` supported on a ball
around the centre.  Their remark after the theorem: "if `S_n` were adaptive, then by just one
appropriate function value `ρ(x)`, we could identify the index `i`".  Theorem 5: for an adaptive
Metropolis method (ball walk) the asymptotic error constant is polynomial in `d` and `α` (a
non-asymptotic bound is stated there as a belief, not proved).  Theorems 1–2: on the larger class
`sup ρ/inf ρ ≤ C`, simple Monte Carlo is optimal up to a constant among *all* methods, adaptive or not.
So the *method* of Theorem 11.45 (hidden cone centres; pairs that differ on a ball at the centre;
adaption defeats the construction) is in print for a neighbouring problem.  Not there: the cube, the
functional `ln Z`, a class without concavity, the exact exponent, the class-wide upper bound.  Fix: cite
it in §11.16, in G18 and in §13; replace "not found" by "method known (Mathé–Novak 2007); exponent on the
cube not found".  It also sharpens the open question: their adaptive upper bound uses log-concavity,
which the cube class lacks, and their Theorem 1 shows what happens when no structure is left.

**M3. What is machine-checked is less than the labels say.**
(i) Theorem 11.45 is tagged **[V]** as a whole.  [V] are: the conditional bound (a); in (b) the
admissibility of both functions, the identification of the difference set, and the bound *given* the
two hypotheses `hsens` (the drop of `ln Z`, as two raw sums over the cube) and `hB` (a bound on a
cardinality).  Not [V]: the closed form `D_R`, `|B(R−1)|`, the limit in (c), and the bold sentence "the
non-adaptive exponent … is exactly `θ_na(ε₁)`", whose upper half is Theorem 11.44 **[P + K]**.
(ii) Lemma 11.43 "[V; Harper's theorem K]" and README "machine-checked up to Harper's theorem": Lean has
part (a) only.  The reduction of (b) to Harper (erosions, layer-cake identity, the count for balls) is a
paper proof; the Lean header says so itself ("not formalised here").
(iii) Research log: "a machine-checked lower bound for non-adaptive algorithms with the same exponent";
§12 2(d): "optimal by a machine-checked lower bound".  The exponent is not machine-checked.
(iv) `cube_nonadaptive_witness` instantiates `ε = 0`, `R = c`, `B = 1`, where the conclusion
`(1−2δ)2ⁿ ≤ E|Q|` already holds for every algorithm by `cube_exact_randomized`; no machine-checked
instance separates non-adaptive from adaptive cost.  (The witness is legitimate as a proof that the two
instance hypotheses are satisfiable.)
Fix: tag 11.45 as "[V] (a), (b) given the two sums; [P] closed forms and (c)", 11.43 as "(a) [V]; (b) [P + K]",
and reword the three sentences; optionally add a witness with `R = 2c` (`B = n + 1`).

### MINOR

**m1. Lemma 11.43(b): hypothesis and proof.**  Add `D ≠ X` (otherwise `dist(x, Dᶜ)` is undefined).  The
inference "`N^{j−1}(D_j) ⊆ D`, so `|D_j| ≤ |B(r+1−j)|` by Harper" uses strictness; state the theorem in the
initial-segment form or use complements (Appendix A).  True as stated otherwise.

**m2. Theorem 11.44 statement.**  Say that (b) is empty unless `ε ≥ ln(2(1+Γ_n(r))) + ln(1/δ₂)`, and that
`Γ_n` is not monotone (`Γ_n(1) ≈ n(eᵘ−1)`; minimum near `ρ = a/(1+a)`, `a = e^{−u}/2`).  The benchmark's choice
"condition for all `r' ≤ r0`" is more conservative than the theorem requires; harmless.

**m3. Proposition 11.46.**  (i) Needs `M ≥ 2K`.  (ii) For `r̂ = 0` the set `{w > t̂}` is empty on the good
event and the term `t̂(e^{Δ_0} − 1)` must be dropped (as `Γ_n(0) = 0` in 11.44); as written, the claim
"narrower than `ε` once `M ≥ 2K·2ⁿ/|B(k*(ε−2)−1)|`" can fail when `k*(ε−2) = 0` (it does iff
`2^{−n}(eᵘ−1) > (2/3)e^ε − 2`, i.e. only for `eᵘ` of order `2ⁿ`); without the convention the algorithm of
the last sentence need not terminate on such classes.
(iii) *Doubling*: correctness "therefore" does not follow — the stopping stage is data-dependent, so a
union bound is needed: use `K_i = 24 ln(4·2^i/δ)` at stage `i` (or `24 ln(4(n+⌈log₂ 2K⌉+1)/δ)`); this costs a
factor `O(n)` at most and no exponent.  (iv) The bracket is never narrower than `ln 3 ≈ 1.10`, so the
algorithm never stops for `ε ≤ ln 3`; "no hint is needed at the zero residual" (title, README, G18, 2(d))
is proved for `ε > 2`, not for the bounded-accuracy and small-accuracy rows of Theorem 11.25(d).  With
`(1 ± η)` in place of `3/2` and `2` and `K ≍ η^{−2}` the restriction goes away, at the price of a factor
`ε^{−2}`.  (v) "From the same samples": the proposition draws **two independent** samples (the split is
used in the proof); say so in the title and in the README.  (vi) Neither the harness nor B12 tests the
proposition, contrary to the preamble of §11.16 ("the statements are checked by the harness").

**m4. Adaptive stopping (end of Theorem 11.45, table row 2).**  What the sketch proves, once completed
(Appendix C): for algorithms that evaluate a pre-drawn sequence and choose when to stop,
`max_s E τ(cone_s) ≥ E_s E τ(cone_s) ≥ (1−2δ)² 2ⁿ / (2|B(R−1)|)`.  State it: the constant is not `(1−2δ)`, and it
is a worst-case statement — the same class of algorithms costs `e^{nθ_hint}` at the zero residual
(Proposition 11.46).  The table entry "exact" is right in that sense only.

**m5. "The cone is the worst member of the class for uniform sampling."**  Not proved; replace by "the
bound has the exponent of the cone", or prove the two-sided version (Appendix B gives the fraction of
Gibbs mass in a super-level set within a factor `eᵘ` of the cone's).

**m6. Finite-`n` comparison.**  `0.0293` is computed with `δ = 0.05`, `0.0307` with total failure
probability `e^{−K/8} + δ₂ = 0.10` (harness XIII.4 and B12).  Effect `2·10⁻⁵`; say it or use `1 − 2·0.1`.

**m7. Title and "optimal".**  "Exponent-optimal" (as in the Lean header).  At laboratory sizes the two
theorems are far apart: `n = 200`, `u = 1`, `δ₁ = δ₂ = 0.05` (lower bound with `δ = 0.1`): `M = 2.9·10⁵`
against `82` at `ε = 12.0`; `M = 6.6·10¹²` against `3.2·10³` at `ε = 7.2` (just above the void threshold);
`n = 6400`, `ε₁ = ¼ ln cosh ½`: a factor `e^{8.7}`.  At fixed `ε₁` the factor seems to stay bounded as
`n → ∞` (`R* − r = 12` at `n = 1600` and at `n = 6400`; each level changes `ln Γ_n` and `D_R` by about
`ln[ρ(1−p_u)/((1−ρ)p_u)]`) — a stronger statement than "same exponent"; I did not prove it, but it should
be within reach and is worth making.

**m8. Stale text elsewhere in the report.**  Theorem 11.25 (end of (d)) still calls `e^{KL(π‖uniform)}` "a
heuristic here, not a theorem" and says the hint-free exponent "lies between `≈ u²/32` and `ln cosh u`";
§8 does not list Lemma 11.43(b), Theorem 11.44 and Proposition 11.46 among the unformalised statements.

**m9. Heuristic paragraph.**  Properly labelled.  "In every family we examined … costs at most `e^{nθ_hint}`"
has no script or note behind it in the repository; say "hand calculations, not recorded".

**m10. README wording.**  "Above any threshold, the Gibbs mass … is at most the excess of a dip on a
ball" omits the positive part and the factor `t`: `E(w − t)₊ ≤ t(e^{Δ_r} − 1)`.

**m11. Harness.**  XIII.1, XIII.3, XIII.4 and the deterministic half of XIII.2 test what the theorems
say and can fail (11 mutations are caught).  The simulation in XIII.2 has little power for the
probabilistic step: it uses `K = 8 ln 10` and counts the event `Â < A/(2(1+Γ))`, which is far rarer than
the bound `0.1` (in my simulations it never occurred, for any `K ≥ 2`), so the constant `1/8` is not
tested.  The Chernoff event itself (`Σ min(w(X_i),t*) <` half its mean) with `K = 2, 4, 8` has frequency
up to `0.21, 0.23, 0.05` (bounds `0.78, 0.61, 0.37`) — a usable test.  The limit of `Γ_n` is tested at three
`ρ > p_u` only (not below `p_u`, not at `½`).

## 3. Independent numerical checks

All scripts and outputs are in `scratchpad/referee5/` (`out/` holds the logs).  Own code throughout; the
author's scripts were read, not run.

1. `harper_exhaustive.c` — **every** proper non-empty subset `D` of the `n`-cube, `n = 3, 4, 5`
   (`4 294 967 294` sets for `n = 5`, 17 s): all erosions `|D_j|`; maximum over `|D| = m` for each `(m, j)`.
   Outcome: `|D_j| ≤ |B(r+1−j)|` with `r` the least radius with `|B(r)| ≥ |D|`, no violation; the maxima equal,
   for every `(m, j)` simultaneously, the values at the complement of the initial segment of the
   simplicial order.  This checks the deduction from Harper including non-ball sizes; it is not a check
   of Harper's theorem for `n ≥ 6`.
2. `check_tail_mc.py` — cubes `n = 3…8`, `u ∈ {0.3, 1, 2.5}`; cones, truncated, flattened and banded cones,
   extremal profiles `−u·dist(·, Dᶜ)` for final segments, random sets, unions of balls and co-subcubes,
   envelopes of random data, Lipschitz-regularised Cauchy noise.  21 714 threshold checks of Lemma 11.43
   (level values and midpoints; 3 154 with equality), 364 880 checks of `A ≤ (1+Γ_n(r)) E min(w,t*)` over
   all quantiles; a hill-climb in the Lipschitz class.  No violation.
3. `check_tail_mc2.py`, `check_cone_slack.py` — tightness of that inequality over `r ≥ 1` (the case
   `r = 0` is an identity): a hill-climb reaches ratios `0.12–0.64` (`n ≤ 7`); at the cone the loss is
   `eᵘ` for `r` well above `n/2`, and `e^{1.9}, e^{1.4}, e^{1.1}` at `r/n = 0.385, 0.45, 0.5` for `u = 1`
   (`n = 1000` and `n = 6400` alike; `e^{2.6}, e^{2.3}, e^{2.1}` for `u = 2`); near `p_u` it grows to `e^{4.7}`
   (`u = 1`, `n = 6400`), which is the defect M1.
4. `check_limits.py` — `Γ_n` and `D_R` in 60-digit arithmetic, `n = 10³, 10⁴, 10⁵`, `u = ½, 1, 2`,
   `ρ ∈ {0.02, p_u/2, 0.9p_u, p_u, (p_u+½)/2, 0.45, ½, 0.55, 0.7}`: limits as claimed; below `p_u` the
   predicted constants (e.g. `19.145` at `ρ = p_u/2`, `u = 1`); `min_{r≥1} Γ_n(r) → 4eᵘ(eᵘ−1)`.
5. `check_exponents.py`, `check_finite.py` — table and numbers: `θ_hint(0), θ_na(0)` =
   `0.007673/0.030300`, `0.029139/0.110944`, `0.097281/0.327813` (`u = ½, 1, 2`); ratio `3.9995` at `u = 0.05`;
   both exponents `/ 2((ln cosh(u/2) − ε₁)/u)² → 1`; identity `KL(ρ_hint‖p_u) = ε₁ + ln 2 − h(ρ_hint)` to
   `10⁻¹⁶`; `n = 6400`, `u = 1`: `R* = 2437`, `r = 2425`, `0.02933`, `0.03069`, limit `0.02830`; `u = 2`:
   `0.03182`, `0.03273`, `0.03106`.  The stored B12 output is reproduced digit for digit, including the
   certified lower ends `−5.146, −4.305, −3.955, −3.734` and `e^{4.9}, e^{9.3}, e^{33.2}`.
6. `check_small_eps.py` — table of M1.
7. `check_flatcone.py` — 2 874 cases, `n ≤ 10`: flattened cone Lipschitz, difference set = open ball,
   closed form of `D_R`, `D_1 = −ln(1 − (1−e^{−u})/(1+e^{−u})ⁿ)`, monotonicity in `R`.
8. `sim_mc.py` (`n = 40`, functions of the distance to a centre, exact binomial sampling; cone, cone on a
   flat background, flattened cone, spike; `u = 1, 4`): Theorem 11.44(a) with `K = 2, 4, 8`,
   `M = 200, 5·10³, 5·10⁴`: the certified lower end was never violated; the Chernoff event has frequency
   at most `0.374·e^{−K/8}`.  Proposition 11.46 with `K = 6, 12, 24`: failures only at the lower end
   (`Â/1.5 > A`), at most `2 %` at `K = 6`, none at `K = 12, 24`.
9. `sim_recentred.py` — Theorem 11.44(b) end to end (`n = 60, 200`; `u = 1, 2`; `ε` at 70 % and 85 % of the
   threshold; 17 instances; 600 repetitions): coverage `≥ 0.988` (required `0.90`).
10. `check_prop46_exact.py` — the two order-statistic estimates as exact binomial tails over
    `K ∈ [1, 150]`, `M/K ∈ [2, 10⁶]`: at most `0.26` and `0.52` of `e^{−K/6}`; sum of the four failure bounds
    `≤ 0.34 δ`.
11. `check_adaptive_cone.py` — the adaptive certificate of Appendix D on 12 672 cones (always certified,
    at most `n + 3` evaluations, exact `ln Z`), 22 176 flattened cones and 21 600 random members (never
    accepted unless the function is a cone).
12. `check_sharper.py`, `check_odds.py` — Appendix B: 185 544 quantile checks of `A ≤ (1+Γ') E min(w,t*)`
    (`n ≤ 8`), largest ratio `0.9745`; `n⁻¹ ln Γ'_n(ρn)` = `−0.165, −0.041, −0.007` at `ρ = 0.05, 0.15, 0.22`
    (`u = 1`, `n = 2000`; `−KL(ρ‖p_u) = −0.165, −0.041, −0.006`); 28 162 checks of the odds statement (iii).
13. `lean/R5Check.lean` (type-checked against the built library, no error): `#check` and `#print axioms`
    of the four cited declarations (standard axioms); `nonadaptive_on_class`;
    `adaptive_escapes_packing`.

## 4. Literature (search log)

Reading depth is stated for each item.  Seventeen web searches and ten page fetches, 2026-11-25.

* **Chatterjee, Diaconis**, *The sample size required in importance sampling*, Ann. Appl. Probab. 28
  (2018) 1099–1135.  Read: arXiv abstract page; Theorem 1.1 and the summary of §3 through an automatic
  reading of the ar5iv full text (first 100 000 characters).  Theorem 1.1 is as used in the report;
  §3 treats `Z(β)` of Gibbs measures.  Nothing on classes of functions.  Attribution accurate.
* **Mathé, Novak**, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 23 (2007),
  arXiv:math/0611285.  Read in full text (pdftotext of the arXiv PDF): §§1–4.1 and §5; §4.2 skimmed.
  See M2.  Closest prior art.
* **Dzindzalieta**, *Extremal Lipschitz functions in the deviation inequalities from the mean*,
  Electron. Commun. Probab. 18 (2013), arXiv:1205.6300.  Abstract only: the supremum of
  `μ{f − Ef ≥ x}` over Lipschitz `f` is attained on distance functions; exact solutions include the cube
  with Hamming distance.  Precedent for "cones are extremal"; not the functional of Lemma 11.43.
* **Harper 1966**: not read.  Statement taken from secondary sources: the introduction of
  Keevash–Long, *Stability for vertex isoperimetry in the cube* (ar5iv, automatic reading), and a
  search summary of *Uniqueness in Harper's vertex-isoperimetric theorem* (arXiv:1806.11061): initial
  segments of the simplicial order minimise the closed neighbourhood for every size.
* **Holzmüller, Bach**, JMLR 26 (2025), arXiv:2303.03237.  Automatic reading of the first half of the
  ar5iv text: stochastic points may be adaptive; "We leave a lower bound outside of the optimization
  regime as an open problem."  The sentence of §12 2(d) about it is accurate.
* **Krieg, Novak, Ullrich**, *On the power of adaption and randomization*, Forum Math. Sigma 13 (2025);
  **Heinrich**, *Randomized complexity of parametric integration and the role of adaption I*
  (arXiv:2306.13471; J. Complexity 2024).  Abstract pages.  Both concern **linear** problems on convex
  (symmetric) sets; `ln Z` is not linear, so neither Bakhvalov's "adaption does not help" nor these gaps
  apply.  **Novak**, *On the power of adaption*, J. Complexity 12 (1996): search summary only.
* **Cai, Scarlett**, *Kernelized normalizing constant estimation*, AAAI 2024, arXiv:2401.05716.  Abstract:
  lower and upper bounds for `∫e^{−λf}` over an RKHS ball, interpolating between quadrature and
  optimisation.  Related to §12 2(d); not cited in the report.
* Search summaries only: **Dagum–Karp–Luby–Ross**, SIAM J. Comput. 29 (2000) (stopping-rule Monte Carlo,
  optimal up to constants; relevant to the doubling algorithm and to adaptive stopping);
  **Kunsch–Novak–Rudolf**, J. Complexity 2019 (sample-size selection, varying cardinality);
  **Ionides**, J. Comput. Graph. Statist. 17 (2008) (truncated importance sampling);
  **Štefankovič–Vempala–Vigoda**, J. ACM 2009 (adaptive against non-adaptive cooling schedules for
  partition functions, a different oracle); **Ge–Lee–Lu**, STOC 2020; **Bobkov–Houdré–Tetali** 2006.
* Searches without a relevant hit: query complexity of the partition function of a Lipschitz function
  on the Hamming cube (adaptive / non-adaptive); `Σ exp(−f)` over the Boolean cube by value queries;
  Harper's theorem combined with Monte Carlo or importance sampling; worst case of importance sampling
  over log-Lipschitz classes (this one led to Mathé–Novak).

Assessment.  Lemma 11.43(a): elementary.  (b): routine corollary of a classical theorem.  Theorem 11.44:
not found; a routine combination (truncation at a quantile, isoperimetric tail bound, Chernoff, Markov).
Theorem 11.45(a): standard information-based-complexity argument; (b): known construction in a new
setting; (c) with 11.44, the exact non-adaptive exponent on the cube for `ln Z`: apparently new.
Proposition 11.46: standard tools; the observation about the zero residual is new within this framework.
Nothing is mis-attributed; one attribution is missing (M2).

## 5. Faithfulness of README, research log, G18, §12 2(d)

| place | sentence | verdict |
|---|---|---|
| README | "a tail lemma; machine-checked up to Harper's theorem" | overstated: part (a) only (M3) |
| README | "Above any threshold, the Gibbs mass … is at most the excess of a dip on a ball" | loose (m10) |
| README | "plain Monte Carlo is accurate on the whole class with the exponent `min{…}`" | true for extensive accuracies; not said (M1) |
| README | "no non-adaptive algorithm does better (machine-checked lower bound)" | bound correct; the machine-checked statement is conditional on two finite sums, the exponent is paper (M3) |
| README | "the same samples give a certified bracket that needs no hint at the zero residual" | two independent samples; proved for `ε > 2`; exponent-level (m3) |
| README | "Whether adaptive algorithms without a hint reach the hinted exponent is open" | accurate |
| log | "this turns the Chatterjee–Diaconis sample size at one instance into a theorem on the class and replaces the Chebyshev bound" | overstated for bounded `ε` (M1) |
| log | "a machine-checked lower bound for non-adaptive algorithms with the same exponent" | exponent not machine-checked (M3) |
| log | "a certified bracket from the same samples, which costs at the zero residual what the best hinted algorithm costs" | exponent-level, `ε > 2`; union bound missing (m3) |
| log | "the non-adaptive exponent is exact, and the open question … is reduced to adaptivity" | accurate for extensive accuracies |
| log | "A candidate adaptive algorithm (not a theorem) …" | labelled; not checkable |
| log | counts (43 files, 2835 declarations, 89 tests, 132 mutations) | consistent with the stored outputs at the commit; not re-run |
| G18 | "the exponent of non-adaptive algorithms is exactly `min{…}`" | add "at extensive accuracy" |
| G18 | status column "[V] …; Harper's theorem [K]; the probabilistic statements [P]" | the deterministic paper steps (11.43(b), closed forms, limits) are missing from the list (M3) |
| G18 | "the matching non-adaptive lower bound [was] not found" | wrong as to the method (M2) |
| §12 2(d) | "exactly `θ_na` (`≈ u²/8` at `ε₁ → 0`; plain Monte Carlo, optimal by a machine-checked lower bound)" | extensive accuracies; `ε₁ → 0` is a limit of exponents, not a statement at bounded `ε`; label (M1, M3) |
| §12 2(d) | "no hint is needed at the zero residual" | `ε > 2` (m3) |
| §12 2(d) | "the tail lemma holds on every subcube"; "the partition functions of the subcubes of a coordinate block form a Lipschitz landscape" | both true (checked by hand: `Z_y ≥ Z_{y'} e^{−u d(y,y')}`) |
| §12 2(d) | "the open lower bound of Holzmüller–Bach" | exists as described (their stochastic algorithms are adaptive) |
| blueprint | — | does not mention §11.16 at this commit |

## 6. Not checked

* Harper's theorem itself beyond `n = 5`; I used it as a known result and did not read Harper's paper.
* Theorems 11.22 and 11.25 were read and used as given (the lower bound at the zero residual for every
  algorithm; `k*`; the hedged spot-check); I did not re-derive them.
* `lake build`, the axiom audit and the author's harness and benchmark were not run; I read the code and
  the stored outputs and type-checked one scratch file against the existing build.
* The families "examined" in the heuristic paragraph and the multilevel scheme of the research log.
* Appendix B is my own derivation: checked numerically for `n ≤ 8` and asymptotically, by nobody else.
* Whether the hinted complexity at some instance other than the zero residual exceeds `θ_hint` (it would
  raise the lower end of the open bracket).  A quick packing estimate for plateaux `c·max(d(·,s) − R, 0)`
  gave nothing above `θ_hint`.
* Asymmetric envelopes numerically (part (a) is machine-checked for them); known parts `f ≠ 0`.
* Literature: only the items listed in §4, at the depth stated.

---

## Appendix A. Lemma 11.43(b) in complement form

Let `∅ ≠ D ≠ X`, `|D| ≤ |B(r)|`, `r ≤ n − 1`, `D_j = {x : dist(x, Dᶜ) ≥ j}`.  Then `D_j = X ∖ N^{j−1}(Dᶜ)`.  Since
`|Dᶜ| ≥ 2ⁿ − |B(r)| = |B(n−r−1)|`, Harper's theorem in its usual corollary form gives
`|N^{j−1}(Dᶜ)| ≥ |B(n−r+j−2)|`, so `|D_j| ≤ 2ⁿ − |B(n−r+j−2)| = |B(r+1−j)|` (zero for `j > r + 1`).  Then
`Σ_{x∈D}(e^{u dist(x,Dᶜ)} − 1) = Σ_{j≥1}(e^{uj} − e^{u(j−1)})|D_j| ≤ Σ_{j=1}^{r+1}(e^{uj} − e^{u(j−1)})|B(r+1−j)| = Σ_{i≤r} C(n,i)(e^{u(r+1−i)} − 1)`.
No strictness, no case distinction.

## Appendix B. A two-sided tail lemma, and Monte Carlo at every fixed accuracy (referee's suggestion)

*Lemma B.*  Let `g` be admissible on the cube, `t > 0`, `S = {w ≥ t}`, `|S| ≥ |B(k)|`.  Then
`2ⁿ E min(w,t) ≥ t·T_n(k)`, `T_n(k) = Σ_j C(n,j) e^{−u(j−k)₊}`.
*Proof.*  For `x ∉ S` and `y ∈ S` nearest to `x`, `w(x) ≥ w(y)e^{−u d(x,y)} ≥ t e^{−u dist(x,S)}`.  Hence
`Σ_x min(w,t) ≥ t Σ_x e^{−u dist(x,S)} = t[Σ_{i=0}^{n−1} |N^i(S)|(e^{−ui} − e^{−u(i+1)}) + 2ⁿe^{−un}]`, which is increasing
in every `|N^i(S)|`, and `|N^i(S)| ≥ |B(k+i)|` by Harper; for `S = B(k)` the value is `T_n(k)`.  ∎

*Proposition B.*  In the setting of Theorem 11.44 let
`Γ'_n(r) = Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1)/T_n(r−1)` for `r ≥ 1`, `Γ'_n(0) = 0`.  Then for every member of the class
`E(w − t*)₊ ≤ Γ'_n(r) E min(w,t*)`, so `A ≤ (1 + Γ'_n(r)) E min(w,t*)`; and for `0 < η < 1`, `δ₃ > 0`, outside an
event of probability `e^{−η²K/2} + e^{−η²K/3} + δ₃`,

    (1 − η)/(1 + Γ'_n(r))  ≤  Â/A  ≤  1 + η + Γ'_n(r)/δ₃.

*Proof.*  `|{w ≥ t*}| ≥ 2ⁿK/M > |B(r−1)|`, so Lemma B with `k = r − 1` gives `2ⁿE min(w,t*) ≥ t*T_n(r−1)`; Lemma
11.43 gives `2ⁿE(w − t*)₊ ≤ t* Σ_{j≤r} C(n,j)(e^{u(r+1−j)} − 1)`.  Write `Â = Â_trunc + Â_exc`.  The truncated part
is a mean of `[0, t*]`-valued variables whose normalised sum has mean `≥ K`: Chernoff on both sides.
`Â_exc ≥ 0` has mean `E(w − t*)₊ ≤ Γ' A`: Markov.  ∎

Since `T_n(r−1) ≥ |B(r−1)|`, `Γ' ≤ Γ`; and `n⁻¹ ln Γ'_n(ρn) → −KL(ρ‖p_u)` for `ρ < p_u`, `+KL(ρ‖p_u)` on `[p_u, ½]`
(numerator `e^{n h(ρ)}`, denominator `e^{n(uρ + ln(1+e^{−u}))}` below `p_u`).  Consequences: (i) for every fixed
`ε > 0` and `δ`, `e^{n KL(p_u‖½) + O(√n)}` samples suffice on the whole class, with the plain estimate `ln Â`;
with Theorem 11.45 (`|R* − p_u n| = O(√n)` at fixed `ε`) the non-adaptive exponent at every fixed accuracy is
`KL(p_u‖½)`; (ii) at extensive accuracy nothing changes; (iii) by the same two bounds, the Gibbs mass of
a super-level set `{w > t}` of size exactly `|B(r)|` has, for every member, odds at most `eᵘ` times the
odds of the ball `B(r)` under the cone — a precise form of "the cone is the worst member" (in 28 162
numerical cases, `n ≤ 8`, the odds never exceeded those of the cone itself, so the factor `eᵘ` may be an
artefact of the proof).  Numerical evidence: §3, item 12.  This appendix is my own derivation and has
not been checked by anyone else.

## Appendix C. Pre-drawn points with adaptive stopping

Model: for each seed `ω` a sequence `x_1, x_2, …` of distinct points fixed in advance, a stopping time
`τ_ω(g)` that depends on `g(x_1), …, g(x_k)` only, and an output that depends on the values seen.  Let
`ε < D_R`, `b = |B(R−1)|`, `T_ω(s) = min{i : d(x_i, s) < R}`.  If `τ_ω(cone_s) < T_ω(s)`, the run on the flattened
cone is identical, and the common output cannot be within `ε/2` of both values; so
`P_ω(τ_ω(cone_s) ≥ T_ω(s)) ≥ 1 − 2δ` for every `s` (this is `prob_query_ne_ge`).  For fixed `ω`, at most `m·b`
centres have `T_ω(s) ≤ m`.  With `s` uniform and independent of `ω`:
`P(τ(cone_s) > m) ≥ 1 − 2δ − mb/2ⁿ`, hence

    max_s E τ(cone_s)  ≥  E_s E τ(cone_s)  ≥  Σ_{m ≥ 0} (1 − 2δ − mb/2ⁿ)₊  ≥  (1 − 2δ)² 2ⁿ / (2b).

Same exponent as Theorem 11.45; the constant is `(1−2δ)²/2`, and the statement is about the worst cone.

## Appendix D. The bound fails on cones for adaptive algorithms correct on the whole class

Evaluate a point `x₀` and its `n` neighbours.  If every difference is `±c`, let `s` be the point that
differs from `x₀` exactly in the coordinates with difference `−c`; evaluate `g(s)` and `g(s̄)` (antipode).  If
`g(s̄) − g(s) = cn`, then for every member of the class `g(x) ≤ g(s) + c d(x,s)` and
`g(x) ≥ g(s̄) − c d(x,s̄) = g(s) + c d(x,s)`: `g` is the cone with apex `s`, and
`ln Z = −βg(s) + n ln(1 + e^{−u})` exactly.  Otherwise run any algorithm that is correct on the class.  This
algorithm is `(ε/2, δ)`-correct on the whole class for every `ε`, and on every cone it makes at most
`n + 3` evaluations, against `(1 − 2δ)2ⁿ/|B(R*−1)|` for non-adaptive ones (`e^{187.7}` at `n = 6400`, `u = 1`,
`ε₁ = ¼ ln cosh ½`).  (The two-point certificate is the remark M4 of the third referee, quoted after
Theorem 11.25.)  The cost of class-correct adaptive algorithms on flattened cones, and in the worst case,
is not settled by this.

Lean (`lean/R5Check.lean`): `adaptive_escapes_packing` — on four points, three pairs `(g_j, g'_j)` with
`|Φ(g'_j) − Φ(g_j)| = 1` and pairwise disjoint one-point difference sets, and a `QueryAlgorithm` (read a
pointer cell, then the cell it names) that returns `Φ` exactly on every function with at most two
evaluations; so `(1 − 2δ) Σ w ≤ |Q|·B` fails (`3 > 2`).  `nonadaptive_on_class` — the theorem of the
repository with `hna` required for class members only.

## Addendum. The working tree while this report was being finished (not part of the review)

The object of this report is commit `36ec238`.  Between 01:28 and 01:33 UTC the working tree changed in
files of my scope, apparently in response to a draft of this report: `NonAdaptive.lean` gained
`weight_ge_of_inside` and `sum_truncated_ge` (with a header that now lists what is not formalised), and the
harness gained checks of `Γ'`, of the Chernoff event with small `K`, of the `n + 3` certificate and a test
XIII.5 of the bracket.  What I did with them, and no more:

* Read the diff of `NonAdaptive.lean`; type-checked a scratch copy (`lean/NonAdaptive_worktree_copy.lean`):
  no error, no warning.  The two statements are the pointwise half and the summed form of the first
  inequality of Lemma B, with the right orientation for asymmetric envelopes (`d(x, y)`, `x` below the
  threshold, `y` at or above it).  The Harper step of Lemma B and of Lemma 11.43(b) remains on paper.
* Read (did not run) the new part of XIII.2.  Its description says that below `p_u` "`Γ` stays above
  `4eᵘ(eᵘ−1)`"; at finite `n` the minimum is slightly below that value (see M1), and the test passes only
  through its tolerance.
* §11.16 of the theory report was still unchanged at 01:33.  Any revised text of Theorem 11.44 (with
  `Γ'`), of Proposition 11.46 and of the labels needs a fresh look; I have not seen it.
