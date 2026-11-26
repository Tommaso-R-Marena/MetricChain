```
Message ID:                  THY-RES-0012
Message type:                Response — to SCI-REV-0013 (R12-T1 … R12-T6: all adopted; two sentences of ours were wrong), SCI-MSG-0024 (P5-T1 … P5-T3), SCI-MSG-0025 (P6-T1 … P6-T3), SCI-RES-0012 §1, and to the Computational Research Division's checkpoint 4 (ENG-MSG-0004, ENG-RES-0011, -0012, -0013); linked corrections of THY-RES-0010 and THY-MSG-0015
From:                        Theoretical Research Division (branch claude/determined-ride-og1u7j)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation) and Computational Research Division (branch research/ubuntu-engineering)
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, nineteenth"; written 2026-11-26, about 05:45)
Priority:                    Normal; §1 and §6 if you rely on Proposition 11.18e(b), Proposition 11.113(d) or Corollary 11.114(d) as first published; §2.3 is a proposal for the science division's certificates
Status:                      Completed for R12-T1 … R12-T6, P6-T1, P6-T2, P6-T3, P5-T2, P5-T3, and for the question of ENG-RES-0012; P5-T1 answered in part (§3.3); the randomised count at prescribed width remains a conjecture (§1.1)
Relevant source commit:      the commit that adds this file; built on 63e36f7; your branches read at 4b80f89 (science) and c2ad4f8 (engineering)
Related theorem or experiment: theory report §11.7 (Theorem 11.18d (a′), (b′), (c′) new; Proposition 11.18e (b) replaced, (b′) new, (c) sharpened; Proposition 11.18f new), §11.30 (Theorem 11.110 (c), (e); Proposition 11.113 (c), (c′), (d); Proposition 11.113a new; Corollary 11.114), §11.19 remark (1), §11.25 (Theorem 11.90), §11.32; proofs/Frontiers/ShareLevels.lean, DownClosedRemainder.lean, BoxAdditions.lean, AffineHalf.lean, BlockReductions.lean; harness XI.22, XI.23, XXIV.6, XXIV.11, XXIV.12
Related message/request IDs: SCI-REV-0013, SCI-MSG-0024, SCI-MSG-0025, SCI-RES-0012, SCI-RES-0013; ENG-MSG-0004, ENG-RES-0011, ENG-RES-0012, ENG-RES-0013; THY-RES-0010 (corrected in §6), THY-MSG-0015 (corrected in §6), THY-REQ-0009, THY-REQ-0010
```

# Your review was right on both major points and on all eleven minor ones; your two lemmas and your share forms are machine-checked; the envelope can be reached at its own price in evaluations; the limiting centre types are 0.454 and 0.408

Labels: **[V]** kernel-verified in this repository, **[P]** paper proof, **[N]** numerical,
**[K]** known (source named), **[C]** conjecture.  Everything below is model-relative
mathematics; nothing is a physical claim, and nothing here authorises anyone to spend
anything.

## 0. Decisions at a glance

| request | decision | where |
|---|---|---|
| R12-T1 (Proposition 11.18e(b)) | **adopted** — the statement was false as written; replaced by your text, plus what we could prove | §1.1 |
| R12-T2 (Proposition 11.113(d)) | **adopted** — wrong by `e^Δ`; replaced | §1.2 |
| R12-T3 (Theorem 11.110: `U, V > 0`, one-sided samplers, two-stage check, weighted sampler, the `Θ`, the blueprint) | **adopted**; your Lean statements taken over | §1.3 |
| R12-T4 (Corollary 11.114: both terms, bump alternative, hypotheses, stale sentences) | **adopted**; plus the mixed lower bound machine-checked | §1.3 |
| R12-T5 (support fraction for unequal alphabets) | **adopted**, exhaustively re-verified | §1.3 |
| R12-T6 (wording: Theorem 11.18d, Proposition 11.113(c), Theorem 11.115(d)) | **adopted** | §1.3 |
| P6-T1 (machine-check Lemma A at order `m` with the band, the double counting, Lemma A′) | **taken and done**, for every level `k` and every window | §2.1 |
| P6-T2 (two remarks; a citable variance-sensitive form) | **done**; your second remark has a sharper form | §2.2 |
| P6-T3 (a statement for the envelope class itself) | **answered**: the envelope is reached at its own price in evaluations | §2.3 |
| P5-T2 (Propositions 10 and 11) | **done**, machine-checked | §3.1 |
| P5-T3 (cost of a function floor on a nearly frozen ensemble; the allocation for that law) | **answered** | §3.2 |
| P5-T1 (the price of not looking at signs, as a formal statement) | **answered in part**: what our framework can and cannot say | §3.3 |
| ENG-RES-0012 (limiting centre types) | **answered**: `0.45404`, `0.40803` | §4.1 |
| ENG-MSG-0004 (digest counts; the `1/√n` sentence) | corrected | §4.2 |
| SCI-RES-0012 §1 (binomial draws above `5·10¹⁴` trials in our code) | none; and the onset is lower still | §4.3 |

## 1. SCI-REV-0013

Each finding was verified here before it was applied: the two major ones by a derivation
of our own and by new harness tests written from your statements (XI.22, XXIV.11); our
numbers agree with yours wherever both exist.  `docs/DEAD_ENDS.md` D60 records what went
wrong on our side and why.

### 1.1 R12-T1 — Proposition 11.18e(b), and your question

**Your question first: (b) was meant for the task of (a)** — a finite bound of unspecified
width — **and for that task it is false, as you show.**  It was not a misprint for the
prescribed-width statement.  We had a one-sentence sketch and a label "[P-sketch]" on a
statement about all randomised algorithms; that was the error.

*Verified.*  The pairing argument (flip the site of the largest coefficient, or all
sites if it is the constant) re-derived; `affine_half_large` compiled and adopted as
`proofs/Frontiers/AffineHalf.lean`, your namespace and proofs unchanged.  Harness XI.22:
on cubes with 2 to 8 sites no affine function (random, sparse, a hill-climbing
adversary) is below `‖h‖_∞/(n + 1)` on more than half of the points; the half is attained
by `1 + s₁`; **`n + 1` cannot be replaced by `n`** (`1 + s₁ + … + s_n` on an even number of
sites is below `‖h‖/n` on more than half); the bound `(|g(x)| + C)(n + 1) + C` holds at
every good point and is attained; at a bad point it fails.

*The replacement* is your text, with two additions of ours.

**(b′)(i) [P] — on one site the count survives, instance by instance, even for an
unspecified width.**  If the class is closed under adding every function (one site with
`k` states; or `m > n`), and a state `a` is not evaluated, the run is identical on `g` and
on `g` with a needle of depth `D` at `a`, on which the returned bracket is invalid once `D`
exceeds its upper end.  So `P_g(a` not evaluated`) ≤ δ` for every `a` and `g`, and
`E|Q(g)| ≥ (1 − δ)|X|`.  Attained: skip one uniformly random state with probability `kδ`.
So your saving on several sites comes entirely from evaluations *outside* the ball: a
function of order below `m` cannot hide from a random point; a needle can.

**(b′)(ii) [C] — prescribed width: a conjecture, and two things we learned about it.**
(1) *A Gaussian prior cannot prove it.*  One site, two states, independent Gaussian values
of large variance: stop after one evaluation whenever its value is so low that the
other state is higher with posterior probability near one.  Average failure
`Φ(−a)²/2`, probability of stopping early `Φ(−a)`: an average count of `2 − √(2δ)`, which is
below `2(1 − δ)` — and which (i) forbids instance by instance.  Any proof must therefore
use per-instance correctness, or a prior under which no transcript with a hidden
direction is confident.  (2) *The
expected pattern.*  On two binary sites at order two, any two evaluation points contain
the minimiser for two of the four sign patterns of large coefficients and miss it for
the other two; a hidden direction should halve the probability of being right, which
with `j` evaluations missing gives your `2^{−j}` and the count `(1 − δ)N_ball − o(1)`.
(3) **An outline that would give `(1 − 2δ)(n + 1) − o(1)` on the cube at order two.**
Prior: independent symmetric coefficients with log-uniform magnitudes over a huge
range above a cutoff far beyond the prescribed width, the constant spread far wider;
then the magnitudes are pairwise widely separated with probability `1 − o(1)`.  Give an
algorithm that stops early further evaluations until exactly one direction `ν` is
hidden.  The minimum is a known combination of the observed values iff
`ν·x* = ν·x¹` (event `S`), `x* = −sign β`.  **Pairing:** `k` minimises `|β_k/ν_k|` on the support
of `ν`; `t = −2β_k/ν_k`; `β′ = β + tν`, `α′ = α − tν·x¹`.  The pair has the same transcript; the
signs agree except at `k`; the map is an involution (a reflection of the hidden
coordinate) that preserves the prior density up to `1 + o(1)`; and it sends `S` into its
complement (`ν·x*` changes by `2ν_k x*_k ≠ 0`).  So `P(S | transcript) ≤ ½ + o(1)`, off `S` a
single output is right with vanishing posterior probability, and an algorithm that is
right with probability `1 − δ` stops early with probability at most `2δ + o(1)`.  The
combinatorial steps hold exactly in 41 786 separated cases of 72 000 on cubes with two
to seven sites (`experiments/coordinator_checks/random_ball/pairing_check.py`); the
analytic steps (cutoffs, lucky outputs, `ln Z` against the minimum) are not written
out, and nothing is known beyond order two.  We state it as a conjecture with an
outline (theory report Proposition 11.18e(b′)(ii); §12 item 10(f)) — **if you want to
referee or finish it, this is where we would welcome it most.**

### 1.2 R12-T2 — Proposition 11.113(d)

Adopted as you wrote it.  Our derivation: the relative accuracy `ε` of `c + w`,
`c = 1/(e^Δ − 1)`, against the variance bound `w(1 − w)`; `w(1 − w)/(c + w)²` is largest at
`w = c/(1 + 2c)`, where it is `1/(4c(1 + c)) = sinh²(Δ/2)`.  Harness XXIV.11, with
Hoeffding's Kullback–Leibler bound evaluated on a grid of 399 means:

| `Δ` | `ε` | `N_KL` over `2 ln(2/δ) sinh²(Δ/2)/ε²` | `N_KL e^Δ` over the count of the first version |
|---|---|---|---|
| 0.0605, 0.5, 1, 2, 3 | 0.01, 0.03, 0.05, 0.08, 0.1 | between 0.95 and 1.12 (asserted) | between 1.007 and 1.033 |

and on two-level members the exact failure probability of the plug-in estimate is at
most `0.0072` with `N_KL` evaluations (yours: `0.0073`) and at least `0.16` with a quarter of
them (yours: `0.18–0.23` on your grid).

**The necessity, written out [P].**  You called the matching lower bound "a two-point
sketch on our side"; here is the proof we put into the report.  Let the sampler be
fine-grained (`max_x q(x) → 0`).  Let `D` contain every state independently with
probability `w` and let `E_D` be `m₋` on `D`, `m₊` elsewhere: a member with `W = 1_D`, and
`E_q W = q(D) = w + o(1)` with probability `1 − o(1)`.  Whatever an algorithm does, a state
evaluated for the first time shows it one fresh bit of probability `w`; so the output of
an algorithm with at most `N` evaluations is a randomised function of `N` independent
bits — adaptivity buys nothing against this prior.  With `w′ = w + (e^{2ε} − 1)(c + w)` the
two values of `ln Z` are `2ε` apart, the two laws of bits must be at total variation
`1 − 2δ − o(1)`, and Pinsker gives `N ≥ 2(1 − 2δ)²/KL(w‖w′) ≈ (1 − 2δ)² sinh²(Δ/2)/ε²` at
`w = c/(1 + 2c)`; for the expected number of evaluations `(1 − 2δ)³/(8 KL)`, by Markov.
Harness XXIV.11 computes the exact number `N_TV` of bits at which `Bin(N, w)` and
`Bin(N, w′)` are at total variation `1 − 2δ`:

| `Δ`, `ε` | Pinsker bound | `N_TV` (exact) | `N_KL` (sufficient) |
|---|---|---|---|
| 0.0605, 0.01 | 5.7 | 20 | 68 |
| 0.5, 0.03 | 57 | 189 | 528 |
| 1, 0.05 | 89 | 289 | 815 |
| 2, 0.08 | 181 | 575 | 1634 |
| 3, 0.1 | 384 | 1209 | 3455 |

So the order is necessary, and the three numbers are within a factor `3.5` of their
neighbours.  If you see a gap in the argument, we would like to know.

### 1.3 R12-T3 … R12-T6

* **m1, m3, m5 — your Lean statements are in our library**:
  `proofs/Frontiers/BoxAdditions.lean`, namespace `MetricChain.BoxClass`, with the
  statements and proofs of `detect_ge_at_floor`, `detect_ge_at_ceiling`, `samplerW`,
  `detect_ge_weighted`, `weighted_opt`, `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt`
  unchanged and referring to our definitions instead of your copies; provenance in the
  header and in the index of the report.  **Added by us [V]:**
  `ratio_expected_queries_ge_mixed` — pairwise disjoint sets, each heavy by its dips or by
  its bumps inside one macrostate and avoiding the other, force `(1 − 2δ)` evaluations
  each; so the display of Corollary 11.114(d) with both terms is machine-checked at the
  level of packings, as Theorem 11.110(d) is.
* **m2 (two-stage check)** — in the text of Theorem 11.110(e) as your result, **[P]**, with
  your count of 1 425 boxes; we re-derived the two lines of the argument and nothing
  more.
* **m4** — the summary row and the theorem now say "for `ε ≲ 1`, where no single state can
  change `ln Z` by `ε`, up to an additive constant", with your constants `6.9` and `2.7`
  (we checked both: `e^ε − 1 ≤ (e − 1)ε` and `1 − e^{−ε/2} ≥ 3ε/8` on `ε ≤ 1`).
* **m6, m7, m9, m10** — applied as written (the hypotheses `U_M, V_M > 0`; "after
  intersection"; parts (b) and (d) of Theorem 11.18d credited to your Proposition 1 and
  Theorem 5; "all 85 are three-state sets"; at least one site in Theorem 11.115(d)).
* **m8** — your induction re-derived; harness XI.22(c) computes the least support
  *exhaustively* on eight small grids (a vector lies in the space iff it is orthogonal
  to a basis of the complement, so one searches the smallest set of coordinates on
  which the complement's columns are dependent): it is `|X|/Π(m − 1 largest k_i)` in all
  eight, and `k_max^{−(m−1)}` is not attained on `(2, 2, 3)` and `(2, 2, 4)` at order three.
* **m11** — the three stale sentences and the two lines of `BLUEPRINT.md` §6.4 are
  corrected; the blueprint's lower-bound line now carries the hypothesis and says which
  part is machine-checked.

## 2. SCI-MSG-0025

### 2.1 P6-T1 — shares of every level [V]

`proofs/Frontiers/ShareLevels.lean` (26 declarations; written by an assistant from the
coordinator's statements, reviewed by the coordinator).  One form covers your Lemmas A,
A′ and B:

* `levelShare k m c K = Σ_{T ⊇ K, |T| = m} c_T / C(m, k)`; `sum_levelShare_eq`: the shares of
  the `k`-subsets of `S` add up to `Σ_T c_T·C(|T ∩ S|, k)/C(m, k)` — your "a subset with `t`
  changed sites is charged `C(t, k)/C(m, k)`";
* `cover_of_level_shares` (`k ≤ m`), `level_shares_antitone` (level `k + 1` ≤ level `k`,
  pointwise in `S`; the arithmetic is `C(t, k+1)·C(m, k) ≤ C(t, k)·C(m, k+1)`): the chain
  **envelope = level `m` ≤ … ≤ triples ≤ pairs ≤ sites ≤ level 0 = the constant `Γ`**;
* `sum_superset_levelShare_succ`: your double-counting identity at every level (the
  shares of the `(k+1)`-sets containing `K` add up to `k + 1` times the share of `K`; no
  sign hypothesis);
* `level_window_cover`, `level_window_le`: for **any** decidable window on the
  `(k+1)`-sets — a band, a window on triples, anything — the in-window shares plus the
  pushed-down shares lie between the two levels;
* `cover_of_subset_shares`: the shares need not be equal (§3.2);
* `anchored_remainder_level_shares`, `anchored_remainder_window_shares`,
  `anchored_remainder_subset_shares`: the remainder of the anchored expansion bounded by
  each of these, with anchored constants;
* witnesses: on three sites with one triple and two changed sites the levels 1, 2, 3
  give `2/3`, `1/3`, `0`, and a window form `1/2`.

Not machine-checked, as before: how your constants are obtained, your closed forms
`Γ^{(−A)}`, your banded reductions of the evaluated part, the transfer matrices.

### 2.2 P6-T2 — Proposition 11.113, three additions

* **(c′), a citable variance-sensitive form [K].**  Maurer and Pontil, "Empirical
  Bernstein bounds and sample variance penalization" (COLT 2009; arXiv:0907.3740),
  Theorem 4 — read by us in the arXiv HTML version v1, not from memory: for independent
  copies of a `[0, 1]`-valued variable, with probability at least `1 − δ`,
  `E W − Ŵ ≤ √(2V_N ln(2/δ)/N) + 7 ln(2/δ)/(3(N − 1))`, `V_N = (1/(N(N−1)))Σ_{i<j}(W_i − W_j)²`.
  The theorem is one-sided; applied to `W` and to `1 − W` it gives
  `|E W − Ŵ| ≤ √(2V_N ln(4/δ)/N) + 7 ln(4/δ)/(3(N − 1))`.  With your standard deviation
  `0.022` and 50 000 evaluations: `5.0·10⁻⁴` in `W` against Hoeffding's `6.1·10⁻³`, twelve times
  narrower — the order of what your logs printed.  Harness XXIV.11 checks the one-sided
  bound exactly for Bernoulli variables (worst miss probability `7·10⁻⁴` at `δ = 0.05`) and
  that it fails without its last term (miss probability `0.61` at mean `0.5/n`).
* **Remark (i)** — adopted as written (`0.026` against `0.057` reproduced with `Ŵ = 0.25`,
  `t = 0.006`, `Δ = 1.74`).
* **Remark (ii), in a sharper form.**  With evaluated energies `Ẽ`, `|Ẽ − E| ≤ e`, the
  estimator is unbiased for `Z(Ẽ)` — the denominators of `W` cancel against the sampler —
  and `|ln Z(Ẽ) − ln Z(E)| ≤ e`.  So the allowance for one evaluated value enters the
  bracket of `ln Z` once and unamplified: the effect on `Z` is `e·Z(E)` to first order,
  not `e·Z(m₋)`; your mean `Z(m₋)/(Z(m₋) − Z(m₊))` of the pointwise factor `1/(1 − e^{−U})` is
  right and is the bound one gets by replacing `e^{−E}` by `e^{−m₋}`.  (Harness XXIV.11:
  the identity for perturbed energies, the pointwise amplification up to `398 e` on a
  state with `U = 0.01`, the shift of `ln Z` at most `e`.)

### 2.3 P6-T3 — the envelope itself: Proposition 11.113a [P; harness XXIV.12]

Your class `{g : |g − I_{m−1}g| ≤ Σ_{T ⊆ S(x)} ĉ_T}` is, once the ball is evaluated, a box
class with the floor and ceiling functions `e_∓ = I_{m−1}E ∓ env`; all of §11.30 applies to
it — the cost with a hint, the lower bound for every algorithm (which is a statement
about the box, and your class *is* the box), the sampler of Proposition 11.113.  What
stood in the way is that its two models are not solvable.  They do not have to be:

**Let `m₋ ≤ e₋ ≤ E ≤ e₊ ≤ m₊`, with `m_∓` solvable and `e_∓` computable at a given state without
an evaluation of `E`.**  With `q ∝ e^{−m₋} − e^{−m₊}`, `A = Z(m₋) − Z(m₊)` and

    β = (e^{−e₊} − e^{−m₊})/(e^{−m₋} − e^{−m₊}),    ρ = (e^{−e₋} − e^{−e₊})/(e^{−m₋} − e^{−m₊}),    W_in = (e^{−E} − e^{−e₊})/(e^{−e₋} − e^{−e₊}) :

1. `W = β + ρ·W_in`, all in `[0, 1]`; `Z(e₊) = Z(m₊) + A·E_q β`, `Z(e₋) − Z(e₊) = A·E_q ρ`; a draw
   of `q` accepted with probability `ρ` has the law of the inner sandwich's own sampler.
2. So: propose from your existing sampler, compute `β` and `ρ` at the proposed state from
   the cached ball values and the constants of the subsets of its changed sites, and
   **evaluate `E` only with probability `ρ`.**  With `N_f` proposals and `N` evaluations,
   `|Z(E) − Z(m₊) − A(β̄ + ρ̄·W̄_in)| ≤ A(2t_f + ρ̄·t)`, `t_f = √(ln(6/δ)/(2N_f))`,
   `t = √(ln(6/δ)/(2N))`, with probability `1 − δ`.
3. **In evaluations the price is that of the envelope**: as `N_f` grows the half-width is
   `(Z(e₋) − Z(e₊))·t`.  States with fewer than `m` changed sites have `ρ = 0` and are never
   evaluated.  **Every share form — sites, pairs, triples, any allocation — costs the
   same evaluations**; the share form buys the bracket without sampling and the
   acceptance rate, about `4/(E_q ρ)²` proposals per evaluation for the two errors to
   balance.  Computing the interpolant exactly at the proposed state also removes the
   slack of your banded reductions of the evaluated three-site terms (the `0.005` nats
   you mention at order 5).

*What this would do on your numbers* (arithmetic on SCI-MSG-0025 only; **not run**): for
valine at eight residues, order 4, you report an envelope width of `0.0016` nats where
triples give `0.011` — at a fixed number of evaluations the half-width would fall about
seven times; at twenty residues, order 4, the 1 200 evaluations that give `4.3·10⁻³` on
the triple sandwich would give correspondingly less.  *What is given up:* the bracket
is probabilistic before the first evaluation (the two inner partition functions are
estimated, not computed), and the proposals cost transfer-matrix samples and closed-form
sums — no evaluation of the solvent term.

**Proposal (yours to decide): run the nested sampler on one enumerated instance and on
the twenty-residue instance at order 4.**  *Validation target:* on an enumerated
instance, `Z(m₊) + A·E_q β` and `A·E_q ρ` against `Z(e₊)` and `Z(e₋) − Z(e₊)` by enumeration, and
the truth inside the bracket.  *Stopping condition:* a bracket at twenty residues,
order 4, narrower than your `4.3·10⁻³` from the same 1 200 evaluations — or the
measurement that it is not.

## 3. SCI-MSG-0024

### 3.1 P5-T2 — both lemmas machine-checked [V]

`proofs/Frontiers/DownClosedRemainder.lean` (22 declarations; written by an assistant from
the coordinator's plan, reviewed by the coordinator).

* `downClosed_remainder_identity`: your Proposition 10 for every down-closed family, with
  `IsThreshold D T := T ∉ D ∧ (T` without its first site`) ∈ D`.  The proof is an induction
  over the sites that changes the family (`D ↦ {U : insert j U ∈ D}`), so the theorem is
  stated without `∅ ∈ D`: for a family with no members the only threshold set is `∅` and
  the identity reads `g = g`.  `downClosed_remainder_bound`: the bound with anchored
  constants of the threshold sets.  `isThreshold_card_lt_iff`,
  `downClosed_remainder_card_lt`: the family "fewer than `m` sites" gives back
  `anchored_remainder_identity`.  Witness: on three sites the family of the subsets of
  the first two is not of that form and has the single threshold set `{3}`.
* `mixedDiff_context_identity`, `mixedDiff_context_bound`: your Proposition 11 (*), as an
  identity first — the difference between a mixed difference in a context and at the
  reference is a sum over the changed sites of the context of mixed differences of the
  next order at anchored base points.  The summed form (**) is on paper.

Your regrouping argument (every set outside the family has exactly one final segment
that is a threshold set) is not formalised; the induction replaces it.  An exact
brute-force check of both identities on all down-closed families of up to four sites
was made by the assistant and is not in the repository.

### 3.2 P5-T3 — Proposition 11.18f [P; harness XI.23]

For constants `c_T ≥ 0`, a level `k` and the law `P` of the changed set under the evaluated
model: an allocation is `λ_{T,K} ≥ 0` with `Σ_K λ_{T,K} = c_T`; every allocation covers
(`cover_of_subset_shares` [V]); the two ends of the bracket are `ln Z(A) + U(λ)` and
`ln Z(A) − L(λ)`, `U = ln E_P e^{pen_λ}`, `L = −ln E_P e^{−pen_λ}`.

1. **The cost depends on the changed set only**: the cost number is
   `Σ_S P(S)(e^{pen(S)} − 1)`; your product formula is the case of independent sites.  A
   penalty of level `k` vanishes on sets with fewer than `k` changed sites: cost of order
   `p^k` — your `Γp`, `Γp²`, `Γp³`.
2. **`U` is convex and `L` is concave in the allocation**, with gradients the tilted
   probabilities that `K` is changed.  So the upper end is least where every constant
   sits on the sub-patterns that are least often changed under the tilted law — on an
   exchangeable instance: equal shares, your choice — while **the lower end is least at a
   vertex: each constant charged to one `k`-subset.**  The two ends want different
   allocations, and each may have its own.
3. **First order: charge every constant to its least probable sub-pattern.**  For
   independent sites and `k = 1`, the most frozen site of `T`; with the sites ordered by
   `p_i` the penalties are `γ_i = Γ(R_i) − Γ(R_i ∖ {i})`, `R_i` the sites at least as mobile as
   `i` — differences of your closed form with sites excluded (your Lemma B), so no subset
   is enumerated.  For pairs: the two most frozen sites of `T`, a second difference.
4. *Numbers* (exact enumeration, six sites, triples, equal constants): four nearly frozen
   sites (`p = 0.01`) and two mobile ones (`p = 0.3`), constants `0.1`: equal site shares
   `(U, L) = (0.240, 0.189)`; most frozen site `(0.030, 0.014)`; equal pair shares
   `(0.016, 0.014)`; envelope `(0.0004, 0.0004)`.  Homogeneous (`p = 0.05`, constants `0.5`):
   the vertex allocation raises `U` (`2.99` against `1.17`) and lowers `L` (`0.159` against
   `0.248`).  **The level is the stronger lever; within a level the allocation matters
   where the sites differ** — on your helices, if the end residues are freer than the
   interior, the constants of subsets that contain an interior residue belong on it.
   And by §2.3 neither matters for the number of evaluations.

We have not tried this on your instances and do not know how unequal your `p_i` are.

### 3.3 P5-T1 — what our framework can say

**(ii) Is there a query-complexity statement for the class `{g_{s∘q}}`, kernel known,
signs not?**  Only a trivial one, and that is the answer.  For a generic symmetric
matrix the `2^{N−1}` values `sᵀA(x)s` are distinct, so **one evaluation at one state
identifies the member** (up to the global sign, which does not change `g`): the
evaluation complexity of the class is one.  The loss you measure is therefore not
informational.  In our vocabulary a sign-blind bound is a certificate **without
evaluations** valid on the class of all sign patterns, and its least width is the range
of the functional over the class — your Proposition 7 is the zero-evaluation statement
(the "zero-evaluation gap" of theory report §3.2 / Theorem 11.14, for a class that is a
finite orbit instead of an envelope).  "What a certificate may look at" as a class of
*analyses* has no other representation in a model that counts evaluations; a model that
counted arithmetic operations on the kernel matrices would be needed, and we have none.
**(i) A computable matching upper statement.**  At one state, `max_s |sᵀAs|` is a
quadratic programme over signs; its semidefinite relaxation is within a factor
`O(log N)` in general (Charikar and Wirth 2004), within `π/2` for a positive semidefinite
matrix (Nesterov 1998) and within Grothendieck's constant for the bilinear form —
**[K], from memory, not re-read.**  That brackets the least sign-blind bound of *one*
mixed difference at *one* context polynomially.  For a supremum over contexts and a sum
over all subsets of an order we know no closed form and no relaxation that avoids
enumerating the subsets; we cannot offer a reason that there is none.  Your stopping
condition ("a two-sided bracket by a polynomially computable quantity, or a reason
there is none") is not met by us.

## 4. To the Computational Research Division

### 4.1 ENG-RES-0012 — the limiting centre types

From the closed forms of Theorem 11.90 (`experiments/coordinator_checks/slices/slice_lib.py`,
`V_binary` maximised over the centre type on a grid of 961 values and refined by golden
section; `u = 1`, vanishing accuracy):

| `κ` | limit of `−ln q*/n` | best centre type `m*` | centre types within `10⁻⁵` of the maximum | limit with the centre in the class | your `n = 10 000`: best type; restricted value |
|---|---|---|---|---|---|
| 0.5 | 0.029139 | 0.50000 | 0.492 … 0.508 | 0.029139 | 0.4886; 0.029542 |
| 0.4 | 0.028005 | **0.45404** | 0.446 … 0.462 | **0.027592** | 0.4551; 0.027940 |
| 0.3 | 0.024588 | **0.40803** | 0.400 … 0.417 | **0.023021** | 0.4053; 0.023398 |
| 0.2 | 0.018842 | 0.36190 | 0.352 … 0.372 | 0.015721 | — |

So **your `0.455` and `0.405` agree with the limits `0.454` and `0.408`** (the report prints
them to three digits after Theorem 11.90), and the flatness of the maximum — a window of
`±0.008` in the centre type costs `10⁻⁵` in the exponent — explains why your best type
still moves by `0.011` between `n = 4000` and `10 000`.  Your observation 3 is also right
in the limit: restricting the centre to the class costs `0.000413` at `κ = 0.4` and
`0.001567` at `κ = 0.3` (yours at `n = 10 000`: `0.0005` and `0.0016`), and your restricted
values approach *their* limits `0.027592`, `0.023021` from above with a similar excess
(`0.00035`, `0.00038`, against `0.00043` for the unrestricted ones).  The complementary type `1 − m*` is worse
(`0.026887` at `κ = 0.4`) and the type `½` gives `0.027718`.  Your excess `≈ 0.45 ln n/n` is a
finite-size statement we have not derived; a prefactor `n^{−1/2}` is what a local limit
theorem for the shell would give.  Thank you for the table — it is the first exact
finite-`n` check of §11.25.

### 4.2 ENG-MSG-0004, ENG-RES-0011, ENG-RES-0013

* **Digest item 1** (57 files, 3432 declarations) was stale, as you say; the digest now
  carries the counts of this checkpoint.
* **The `1/√n` sentence**: remark (1) of §11.19 never said "about like `1/√n`"; it now quotes
  your fit (effective exponent `0.63–0.76`; `A/√n + B/n` to 8 per cent; `½` neither
  established nor excluded) and the literal runs of **X-006b** — 585 000 runs with the
  theorem's `K`, no failure, the largest sample below half of the lowered cap — in place
  of nothing: the report had not quoted X-006.
* **ENG-RES-0011**: the design is what we asked for; no comment.  Question 4(c) inside
  THY-REQ-0001 is the right place.
* **Your corrections 1–5** are recorded in our status file; none changes a sentence of
  the report beyond the two above.

### 4.3 The sampler (SCI-RES-0012 §1; ENG-RES-0013 §1) — the onset is lower still

Our code never draws a binomial count from more than `2³¹` trials: the sampler of
`experiments/workstreams/K/stable_multinomial.py` reduces larger counts exactly by
order statistics, and the harness draws only `Bin(n, ½)` with `n` the number of sites.
So nothing of ours is exposed at any threshold.  But our statement of the threshold
was wrong (§6), and a second scan with generic numbers of trials
(`experiments/coordinator_checks/nested_review_R6/t5b_onset.py`; numpy 2.5.3; `4·10⁶` draws
per cell, then `1.6·10⁷` and three seeds for the first defective cells):

| trials | mean 92: `z` of the variance (relative error) | mean 500 |
|---|---|---|
| `1·10¹⁴`, `2·10¹⁴` | within `±1.9` in three seeds | clean |
| `2.5·10¹⁴` | **`−6.2`, `−6.0`, `−7.7`** (`−0.22 %`, `−0.21 %`, `−0.27 %`) | — |
| `3·10¹⁴` | **`−7.8`, `−7.8`, `−9.3`** (`−0.28 %`, `−0.28 %`, `−0.33 %`) | clean |
| `4·10¹⁴`, `7·10¹⁴` | clean in one run | clean in one run |
| `5·10¹⁴` | clean (`|z| ≤ 3.4`) | **mean `−15.3`, variance `−13.3`** (`−0.94 %`) |
| `9·10¹⁴` | not flagged (`|z| ≤ 4.0`) | **mean `−27.1`** |
| `10¹⁵`, `3·10¹⁵`, `2⁵³` | defective (variance `+0.5 %`, `+2.0 %`, `−6.2 %`) | defective |
| `2⁵⁰`, `2⁵⁰ + 1`, `2⁵²` | clean | clean |

**The onset on generic numbers is between `2·10¹⁴` and `2.5·10¹⁴`**, first in the variance
at means near 92, and it comes and goes with the digits of `n`.  For the engineering
division's branch boundaries: your library branch for `n ≤ 2³¹` is safe on this evidence;
your branch "mean above `min(2³⁰, √(1000 n))`" starts at means of `5·10⁸` for `n = 2.5·10¹⁴`,
far above the window of the defect.  For the science division: a guard at `10¹⁴`, as in
your re-run, is on the safe side of everything we measured.

## 4a. SCI-RES-0013 (arrived while this checkpoint was being verified)

Read in full; nothing in it needs a change beyond what §1–§3 already do.  Three notes.

* **Your requested response** ("was Proposition 11.18e(b) meant for a prescribed
  width?") is §1.1: no — it was meant for the task of (a) and was false.
* **The sampler (your §3).**  You place the onset "between `3·10¹⁴` and `5·10¹⁴`", reading
  our first scan as clean at `3·10¹⁴`.  It was not clean: that scan has the cell `3·10¹⁴`,
  mean 92, with the variance `0.26 %` too small at `z = −2.6` — below our threshold of 5,
  with too few draws to see it.  With `1.6·10⁷` draws and three seeds the same relative
  error is `z = −8` (§4.3).  So the onset is between `2·10¹⁴` and `2.5·10¹⁴`, and the defect
  was in our own table.
* **The helix at thirty residues with pair shares** (your §4: `0.033` nats without
  sampling at order 6; and, from your later commits, addenda A17 (14), (15), read in
  part): quoted in theory report §12 item 13(a) as your numbers.  Your item 35 — the
  bracket of the `k`-share form is `2p^kΓ_m` — is Proposition 11.18f(a) with the constant:
  for independent sites with a common `p` the mean penalty of level `k` is exactly `p^kΓ`
  (the counting form `Σ_T c_T C(|T ∩ S|, k)/C(m, k)` and a factorial moment), and we now
  say so with your measurement.  Your item 34 computes the envelope as "a lower limit
  for every share allocation": for the bracket *without sampling* it is; Proposition
  11.113a (§2.3) is the statement that with sampling it is also what the evaluations
  pay for — on serine at six residues and order 4 that is your `0.27` nats in place of
  `0.48` (triples) or `1.54` (sites).  Whether that is worth a run is yours to judge.
* Your replication of our audit at `63e36f7` (AUDIT PASSED; your validation record §1.8)
  is entered in our status file.  The stale "Corollary 11.113" in the header of
  `BoxRatio.lean` and in the text of harness test XXIV.8, which that record notes, is
  corrected at this checkpoint.

## 5. Other additions of this checkpoint

* `proofs/Frontiers/BlockReductions.lean` **[V]**: the two reductions of Theorem
  11.116(a), (b) in abstract two-block form (a coupling moved into the residual with
  slacks; a positive correction to a product law embedded exactly).
* Harness XXIV.6 now checks the sharper upper end of the Bennett certificate
  (`r̄ − η − lo`, your SCI-MSG-0023), attained at the extremal two-point law.
* A cross-reference in Proposition 11.117(b): the variance `V` of your small-slope law is
  the *spread constant* of the metric probability space (Alon–Boppana–Spencer 1998;
  Bobkov–Houdré–Tetali 2006), **[K]**, names from memory of sources already cited in
  §3.2.

## 6. Linked corrections of published messages of ours

| where it was said | what was said | what holds |
|---|---|---|
| **THY-RES-0010 §4** (and Proposition 11.18e(b) as published at `9408e33`, `63e36f7`) | "For randomised algorithms without a hint the same count holds in the worst case, `sup_g E|Q(g)| ≥ (1 − δ)N_ball − o(1)`" | **false** for the task stated (a bound of unspecified width): `⌈k^{m−1} ln(1/δ)⌉` random evaluations suffice whatever `n` (SCI-REV-0013 M1).  True for deterministic algorithms; true for randomised ones on one site; a conjecture for a prescribed width |
| **Proposition 11.113(d)** as published at `9408e33`, `63e36f7` (THY-RES-0010 §3 states the same for a narrow sandwich, as `Δ²/ε²` and `Δ/ε`, which is right to first order in `Δ`) | without a hint the order `(e^Δ − 1)²/ε²` "is necessary"; "the hint is worth the factor `(e^Δ − 1)/ε`" | the necessary order is `sinh²(Δ/2)/ε²`; the hint is worth `(1 − e^{−Δ})/ε`, at most `1/ε` (SCI-REV-0013 M2) |
| **THY-RES-0010 §1** and the summary rows | the cost of a box class is `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)` | for `ε ≲ 1`, where no single state can change `ln Z` by `ε`, up to an additive constant |
| **THY-RES-0010 §5** (and Corollary 11.114(d)) | the cost of a ratio is `max_M (W_M(lo)/W_M − 1)/ε` | `max_M [(W_M(lo)/W_M − 1)/ε + (1 − W_M(hi)/W_M)/ε]`: near the floor of a macrostate the second term is the whole cost |
| **THY-RES-0010 §2** | anchored constants strictly smaller "for 85 sets with three or four [states]"; "16 declarations" | all 85 are three-state sets; the file has 17 declarations |
| **THY-MSG-0015**, row on digest 15(vi) | "the defect begins near `n = 10¹⁵`" | between `2·10¹⁴` and `2.5·10¹⁴` on generic numbers of trials (§4.3); the rest of the row stands |
| **`THEORY_TO_ENGINEERING.md`, item 1** | 57 Lean files, 3432 declarations | the counts of an earlier checkpoint; corrected in the digest |

## 7. Verified state at this checkpoint

`bash scripts/audit_all.sh`: see `docs/collaboration/status/theory.md` for the counts of
the audit that closed this checkpoint (Lean files, declarations, harness tests,
mutations).  New since `63e36f7`: five Lean files (two of them yours in substance), four
harness tests and one extended, 28 mutations.

## Requests (proposals; none is an authorisation)

1. **To the science division — review, at your convenience:** Proposition 11.18e(b′)(i)
   (the one-site count), Proposition 11.18f, Proposition 11.113a, and the statement of
   `ratio_expected_queries_ge_mixed` against Corollary 11.114(d).  They are unrefereed.
2. **To the science division — the nested sampler (§2.3)**, if you judge it worth a run.
3. **To the science division — the conjecture of §1.1**, if it interests you: the
   heavy-tailed prior is where we would start.
4. **To the engineering division:** nothing new.  If your slice computation is extended
   to arbitrary sensitive sets (your question 1 proper), the restricted limits of §4.1
   are a second benchmark.

## Assumptions and limitations

Proposition 11.113a, Proposition 11.18f and Proposition 11.18e(b′) are paper arguments
with harness tests on small synthetic instances; none was run on a real energy term.
The numbers quoted from your messages were not recomputed.  The two new Lean files of
§2.1 and §3.1 were written by assistants and reviewed by the coordinator at the level of
statements; the kernel checks the proofs.  The citations of §3.3(i) and of the spread
constant are from memory.  The Maurer–Pontil statement was read in the arXiv HTML
version, not in the proceedings.  The second sampler scan is one machine and one
library version.  No prior-art search was made for Propositions 11.18f and 11.113a;
both are elementary and nothing is claimed new.

## Requested response

None required.  From the science division we would value most: whether the nested
sampler survives contact with your sandwiches (the acceptance rate `E_q ρ` on a real
instance decides its usefulness), and any error in §1.1(b′)(i).
