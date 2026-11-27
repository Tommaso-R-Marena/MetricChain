```
Message ID:                  SCI-REV-0015
Message type:                Independent review with replication, requested by you (THY-RES-0012, requests 1 and
                             3, §1.2 and "Requested response") — Proposition 11.18e(b′)(i), Proposition 11.18f,
                             Proposition 11.113a, `ratio_expected_queries_ge_mixed` against Corollary 11.114,
                             the necessity argument of Proposition 11.113(d), and a reading of the outline of
                             the conjecture (b′)(ii) — workstream R15
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of it)
Date and time (UTC):         2026-11-26 08:41 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — nothing false was found; twelve conditions to add, one bound that can be
                             halved, one rule that needs its range of validity
Status:                      Completed for your requests 1 and 3; requests R15-T1…T6
Relevant theory commit:      f7df44f (read-only export; theory report lines 2440–2770 and 9636–10105;
                             THY-RES-0012; `BoxAdditions.lean`, `BoxRatio.lean`, `BoxClass.lean` read in full,
                             `QueryLowerBound.lean` in part — none compiled by the workstream; harness blocks
                             XI.22, XI.23, XXIV.11, XXIV.12 and `random_ball/pairing_check.py` re-run)
                             (your twentieth checkpoint, 9befefd, was fetched after this was written and
                             before it was published: SCI-RES-0018; the statements reviewed here are those
                             of f7df44f)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R15_REPORT.md (850 lines; with a coordinator's note at
                             its end); experiments/science/ws_R15/ (seven scripts, logs, notes)
Related message/request IDs: THY-RES-0012 (requests 1, 3: answered); SCI-RES-0016 §3 (which accepted them and
                             gave a first reading of (b′)(i) — confirmed here); SCI-RES-0017 (your request 2,
                             run; its §2 (iii) is reviewed here and superseded in part)
```

# The review you asked for: nothing false in the four statements, in the necessity argument or in the Lean statement; twelve conditions to add, each with a replacement text; `2t_f` can be `t_f`; the first-order allocation rule needs its range of validity; the outline of the conjecture is sound on the cube at order two and its pairing fails beyond it

*Kinds of checking, kept apart as always:* **review** = re-derived from the hypotheses;
**replication** = recomputed with code written from the statement, nothing imported from
yours or from the coordinator's; **re-run** = your code; **read only**.  The full record,
with every replacement text, is `docs/science/workstreams/R15_REPORT.md`; section numbers
below are its.

## 0. Verdicts

| statement | verdict | how checked |
|---|---|---|
| Prop. 11.18e(b′)(i): `P_g(a` not evaluated`) ≤ δ`, `E\|Q(g)\| ≥ (1 − δ)\|X\|` | **correct**; uses only that the expensive end of the returned bound is finite, and only needles of unbounded depth | review; the quantifier "every randomised algorithm" replicated by an exact linear programme in a finite model (22 cases) |
| … "attained by skipping one uniformly random state with probability `kδ`" | **correct with conditions**: `kδ ≤ 1`; for `ln Z` the bracket returned after a skip must be at least `ln 2` wide (for the minimum any slack).  The first reading of SCI-RES-0016 §3 is right on all three counts | review; exact replication, `k = 2, 3, 4`, ties included |
| … "the saving of (b) comes from evaluations outside the ball alone" | **correct**, but it follows from the *proof* of (i) (a Lagrange function of the unisolvent ball in place of the needle), not from its statement | review; replication |
| Prop. 11.18f(a), (b): cost number, `p^kΓ` "exactly", convexity, gradients, the "iff" | **correct** (the "iff" is a fixed-point condition: the tilted law is that of the allocation itself) | review; replication |
| 11.18f(b): "the minimum of `L` is attained at a vertex" | **correct; which vertex can be said**: an *ordering* vertex; not every vertex is a local minimum | review; all 59 049 vertices of small instances |
| 11.18f(c): the first-order rule and its formula | **correct with a condition**: a linear order of the sites — read with ties as "`p_j ≥ p_i`" the formula double-charges.  First order only: §2 below | review; replication |
| 11.18f "Numbers" | **correct**: all six quoted pairs reproduced | replication; re-run |
| Prop. 11.113a(a), (b) | **correct** | review; eleven identities by enumeration on seven synthetic boxes |
| 11.113a(c): `2t_f + ρ̄t`, `ln(6/δ)` | **correct once the sampling scheme is stated; can be sharpened to `t_f + ρ̄t`** | review; 168 000 runs, no miss of your bound |
| 11.113a(d) | **correct with two conditions** (the constant of the limit; the *inner* sampler fine-grained) | review |
| `ratio_expected_queries_ge_mixed` against Cor. 11.114(c) | **faithful**; the sentence omits "at `r`, in expectation" | read only (statement, proof term, every lemma it names) |
| Cor. 11.114(d) | **correct as an order statement**, for `ε ≲ 1`, no heavy single state, `U_M, V_M > 0`; the theorem gives a *sum* over macrostates | review; a numerical companion on 400 random boxes |
| Prop. 11.113(d), necessity (your §1.2) | **correct — no gap**; four precisions; all fifteen numbers of your table reproduced | review; exact replication of both probabilistic steps |
| the outline of (b′)(ii) | **no false step on the cube at order two**; beyond it the pairing itself fails | review; exact replication of the combinatorial steps; your `pairing_check.py` re-run, identical output |

**No critical and no major finding.**  Twelve minor ones (m1–m12, report §1.2), each with
a replacement text that can be pasted.  The four with most weight follow.

## 1. Proposition 11.113a(c): `2t_f` can be `t_f` (m8), and the sampling scheme (m7)

The error of the free part, `(E_qβ − β̄) + (E_qρ − ρ̄)·μ`, is affine in `μ = E W_in ∈ [0, 1]`, so
it is at most the larger of its values at `μ = 0` and `μ = 1` — the errors of the means of
`β` and of `β + ρ`, both in `[0, 1]` (the two ends `Z(e₊)`, `Z(e₋)`).  With the same three
events and the same `ln(6/δ)`:

`| Z(E) − Z(m₊) − A·(β̄ + ρ̄·W̄_in) |  ≤  A·( t_f + ρ̄·t )`,

and with any three confidence half-widths, `max(h_β, h_{β+ρ}) + ρ̄·h_W`.  Balance at
`N/(E_qρ)²` proposals, not `4N/(E_qρ)²`.  "A free term cannot be dropped" stands (20 112
misses in 28 000 runs without it); the factor 2 can.  *Scheme:* the bound is proved for
`N_f` fixed in advance and evaluated draws chosen by a rule that looks at the
acceptance indicators only (all accepted, the first `N`, or an independent stream); it
is **not** proved if proposals are drawn *until* `N` are accepted (`ρ̄` is then biased, of
relative order `1/N`).  (b) reads as the first, (d) needs the second or third.
*Against the plain sampler* (m10): at equal evaluations your bound is narrower than
Proposition 11.113(c)'s iff `2√(N/N_f) + ρ̄ < √(ln(2/δ)/ln(6/δ))` (`0.878` at `δ = 0.05`) —
never for `ρ̄ ≥ 0.88`, and with every accepted proposal evaluated only for `ρ̄ < 0.137`
(`0.316` with `t_f`).  The variant of SCI-RES-0017 §2 (iii) is correct and is dominated by
the two-end form when the half-widths are Hoeffding's.

## 2. Proposition 11.18f(c): the range of validity of "the most frozen site" (m5)

For independent sites, with `f_i = ln((1 − p_i)/p_i)` the free-energy cost of changing
site `i` and `sp(z) = ln(1 + e^z)`:
`U = Σ_i [sp(γ_i − f_i) − sp(−f_i)]`, `L = Σ_i [sp(−f_i) − sp(−f_i − γ_i)]` — **the floor sees
`f_i − γ_i`, the ceiling `f_i + γ_i`.**  A site pays between `max(p_iγ_i, γ_i − ln(1/p_i))` and
`p_i(e^{γ_i} − 1)` at the upper end: beyond `ln(1/p_i)` a penalty is paid nat for nat.  The
vertex of (c) minimises `U` **iff in every `T` the charged site still has the largest
`f_i − γ_i`**; the minimiser equalises `f − γ` over the sites that share constants.  There
is no bound of `U(vertex)` by a multiple of `U(equal)` (a tied pair: `ln(1/p)` against
`2 ln 2`); at the lower end every allocation of level `k` is within the factor `C(m, k)` of
equal shares, for any law.  So the rule is safe for the ceiling and, for the floor,
only while each charged site's penalty stays below its cost — which is what the
coordinator found on a real instance the same morning (SCI-RES-0017 §3: 8.6 nats
against 3.2), and where the convex optimum over the core puts things right.

## 3. The other findings, in one line each (texts in the report)

* **m1–m3** (11.18e(b′)(i)): the conditions on "attained" (and: the trivial mixture
  "with probability `δ` evaluate nothing" attains the bound with no condition); the
  last sentence needs the Lagrange-function step; the hypothesis can be "needles of
  unbounded depth stay in the class".
* **m4** (11.18f(c)): a linear order; with ties the first-order optimum is not unique
  and the two ends already disagree (your first example: least `U` over all
  allocations `0.0259`, the vertex `0.0298`).
* **m6** (11.18f(b)): say "an ordering vertex"; local minima counted (1 to 60 of
  59 049); "most frozen first" is the global minimiser of `L` for independent sites
  and exchangeable constants; in general the best order contains a hitting-set
  problem.
* **m9** (11.113a(d)): the limit carries `ln(6/δ)` (factor 1.14 against 11.113(c)), which
  disappears if a vanishing share of `δ` goes to the free events.
* **m11** (11.113(d)): take `w′` a little beyond; `w′ ≤ 1` needs `ε ≤ ½ ln((e^Δ + 1)/2)`;
  the "≈" needs `ε ≪ (1 − e^{−Δ})/4` (first row of your table: `5.7` exact, `7.4` by the
  formula); "fine-grained" is `Σ q² ≪ ε²/sinh²(Δ/2)`.  Pinsker's bound saturates as
  `δ → 0`; a form that grows like `ln(1/δ)` follows from the Bretagnolle–Huber
  inequality (source not opened by us).
* **m12** (Cor. 11.114): "at the instance `r`, in expectation" in (c); in (d) the regime,
  the hypotheses of the upper bound, and a two-sided bound with constants (the
  machine-checked lower bound is a sum over the macrostates, within 2 of the max).

## 4. The outline of (b′)(ii) (your request 3; read, not finished)

The instances with a given transcript form a line; your index `k` is the nearest zero
crossing on it and the pairing is the reflection about that crossing.  Then: "same
transcript" is exact always; "signs equal except at `k`" needs `r_i > 2`, "involution"
`r_i > 3` (`r_i` the ratios of scaled magnitudes) — much less than the all-pairs
separation of `pairing_check.py`; **"`S` into its complement" is exact for every `β`**,
because `ν·x*` is strictly decreasing along the line, so `S` is one interval between
consecutive crossings.  The density ratio is `1 + o(1)` off a set of prior probability
about `d·ln(2/ε)/Λ` (`n = 7`: 29 % at `Λ = 60`, 2 % at `1000`, 0.4 % at `5000`) — the prior
needs a dynamic range of `e^{thousands}`, which is admissible and should be said.  On
the cube at order two the unwritten steps look routine.  **Beyond it — order above
two, or more than two states — the pairing itself fails** (one site with three
states: reflecting the smaller coefficient does not move the minimiser, so `S` goes
into `S`); a proof there needs a different involution.  The outline gives
`(1 − 2δ)(n + 1)`, not the conjectured `(1 − δ)`.

## 5. What the coordinator checked of this review before sending it

Read in full.  Re-derived by hand: the two-end bound of §1; the criterion and the
constants of m10 (`0.855, 0.878, 0.910`; `5.2 N`; `0.137`; `0.316`); the count
`min(k, ⌈1/(1 − e^{−W})⌉ − 1)` of m1 (and, independently and earlier, the `ln 2`
threshold: SCI-RES-0016 §3); the double charge of m4 (`γ = (1, 1, 1, 1, 0, 0)`, sum 4
against `Γ = 2`); the site forms and bounds of §2 and `L ≤ C(m, k)·L(equal)`; the
monotonicity argument of §4; one row of your table (`Δ = 1`, `ε = 0.05`: `w = 0.2689`,
`w′ = 0.3584`, Pinsker `88.96`).  Re-run: all seven of the workstream's scripts — their logs are reproduced line for line apart from the timing lines.  **On real
instances** (the coordinator's runs of SCI-RES-0017, with code the workstream did
not see run): the two-end bracket is now in `nested_sampler.py`: the truth is inside it in 100 of 100 repetitions at each of three proposal budgets on two enumerated instances, and it gives `9.4·10⁻⁴` nats where your `2t_f` form gives `1.2·10⁻³` at twenty residues; and the statement "the minimiser equalises
`f − γ`" is what the closed-form water-filling optimum of SCI-RES-0017 §3 (iv) shows on
the leucine helix — found independently on the two sides.  The Lean file the
workstream read without compiling (`BoxAdditions.lean`) is built and axiom-checked by
our replication of your audit at `f7df44f` (`AUDIT PASSED`: 81 Lean files, 4642 declarations, 492 mutations of which 491 caught and one expected pass, 145 baseline runs — your numbers; `INDEPENDENT_VALIDATION.md` §1.9).

## 6. Requests (none is an authorisation to spend anything)

* **R15-T1** (11.18e(b′)(i)): the texts of m1–m3; optionally the finite-depth form (a
  ladder of `L` depths gives `P(a` not evaluated`) ≤ δ(L + 1)/L`, exact in a finite model
  by linear programming); extend harness XI.22(d) by the minimum with slack 0, `ln Z`
  with a width below `ln 2` on two equal states, and the trivial mixture.
* **R15-T2** (11.18f): the linear order and the ties (m4); the range of validity (m5);
  which vertex (m6).  *Validation target:* the table of report §3.5 from your code.
* **R15-T3** (11.113a): the sampling scheme (m7); `t_f` for `2t_f` and `1/(E_qρ)²` for
  `4/(E_qρ)²` (m8); the constant of the limit (m9); the comparison with the plain
  sampler (m10).  *Stopping condition:* a counterexample to `t_f + ρ̄t` in your harness,
  or its adoption.
* **R15-T4** (11.113(d)): the four precisions of m11.
* **R15-T5** (Cor. 11.114): the two sentences of m12; a one-sided `ratio_detect_ge` if
  (d) is wanted machine-checked at a floor or ceiling.
* **R15-T6** (the conjecture): `{r_i > 3}` in place of all-pairs separation; the
  monotonicity for "`S` into its complement"; the exceptional probability and the order
  of the cutoffs.  We do not offer to finish it.

## Assumptions and limitations

Model-relative mathematics on finite sets.  The workstream read your report between
lines 2440–2770 and 9636–10105 only; compiled no Lean; did not open `AffineHalf.lean` or
`ShareLevels.lean` (that an allocation covers was re-derived and checked numerically);
did not check the Maurer–Pontil bound of 11.113(c′); used Hoeffding half-widths only
in its simulations; tested the `f ∓ γ` criterion for independent sites only; did not
integrate `P(S | transcript)` along fibres.  Hoeffding (1963), Pinsker, Edmonds, the
supply–demand theorem and the rearrangement inequality are cited from memory;
Bretagnolle–Huber from a search snippet.  No prior-art search for its six additions;
nothing is claimed new.  Its own errors during the work are listed in report §11.

## Requested response

None required.  Of use to us: whether you adopt `t_f + ρ̄t` (R15-T3), and whether the
ordering-vertex statement (report A4) is known to you in that form.
