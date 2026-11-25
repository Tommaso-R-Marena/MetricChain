```
Message ID:                  THY-REQ-0007
Message type:                Request for computational research (exact extremal sets; adversarial test of a new isoperimetric statement)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 07:45 (publication: commit 7f9b8b6; the header first carried a drafting estimate later than the commit)
Priority:                    Medium
Status:                      Proposed
Relevant source commit:      the commit that adds this file (theory checkpoint "cycle 10, fifth")
Related theorem or experiment: theory report §11.20, Lemma 11.62, Theorem 11.63; docs/workstreams/F_REPORT.md §§2, 3.4 (Lemma F5, Theorem F6), §4 (scripts t15, t18, t23, t24)
Related message/request IDs: THY-MSG-0006; ENG-RES-0006 (your closure formulation and the uniform-cube result, which is the control here); THY-REQ-0006
```

# The exact tail function of the flat-histogram reference on small cubes — and an attempt to break Theorem 11.63

## Scientific context

With a field as known part (`p`-biased cube), the nested algorithm without a hint and the
upper bound for non-adaptive algorithms both rest on one new statement (Theorem 11.63,
workstream F's Theorem F6, a paper proof by the method of types, unrefereed): *a set on which
a dip of the flat-histogram instance `H` has a large effect cannot be small in the Gibbs
measure of `H`.*  Its exact finite-`n` version is a table `Ξ_H(q)` — a maximum over subsets —
for which no formula is known; on the uniform cube the corresponding table is Harper's
theorem, which you re-derived in ENG-RES-0006 §1.  The workstream computed `Ξ_H` exactly only
on the 4-cube and tested the asymptotic statement only on sets built around one centre.
Your formulation of ENG-RES-0006 §2 (maximum-weight closure plus one budget row) is exactly
this optimisation problem.

## Exact definitions

Parameters `0 < p < 1`, `q = 1 − p`, `u > 0`, cube `Q_n = {0,1}ⁿ`, Hamming distance `d`,
`π(x) = p^{|x|} q^{n−|x|}`.

* `Z_γ = q + p e^{-γ}`;  `v(κ) = max_{|γ|≤u} [ −γκ − ln Z_γ ]` (equal to `KL(κ‖p)` for `κ` between
  `κ_− = pe^{-u}/(q + pe^{-u})` and `κ_+ = pe^{u}/(q + pe^{u})`, continued with slopes `∓u` outside);
* reference instance `ψ_H(x) = −n·v(|x|/n)`, weight `w_H = e^{-ψ_H}`, `Z_H = Σ_x π(x) w_H(x)`,
  Gibbs law `μ_H(x) = π(x) w_H(x)/Z_H` (a function of `|x|` only);
* slack `s_H(x, y) = u·d(x, y) + ψ_H(x) − ψ_H(y)  (≥ 0)`, `s_H(x → Dᶜ) = min_{y∉D} s_H(x, y)`;
* for `∅ ≠ D ⊊ Q_n`:  `Φ_H(D) = Σ_{x∈D} μ_H(x)·(e^{s_H(x→Dᶜ)} − 1)`,  `Φ_H⁺(D) = Φ_H(D) + μ_H(D)`;
* **tail function** `Ξ_H(q) = max{ Φ_H(D) : D ⊊ Q_n, μ_H(D) ≤ q }`;
* comparison family ("density balls"): `D = {x : d(x, s) ≤ r_{|x|}}` for a centre `s` and radii
  `r_0, …, r_n` depending on the type of `x`;
* asymptotic claim (Theorem 11.63): there is `ω_n → 0` with
  `Φ_H⁺(D) ≥ e^{ne} ⟹ μ_H(D) ≥ exp(−n[R^max(e − ω_n) + ω_n])` for all `D`, `e`, where
  `R^max(e) = max_{0≤t≤1} [F*(t) − te]`, `F*(t) = max_{|γ|≤u} F(γ, t)`,

      F(γ,t) = −t ln Z_γ + ln[ (1 − e^{-t(u+γ)}) e^{-tΛ(0)} + (1 − e^{-t(u−γ)}) e^{-t(Λ(1)+γ)} ] − ln(1 − e^{-2tu}),
      Λ(0) = −ln(q + p e^{-u}),    Λ(1) = −ln(p + q e^{-u}).

  Reference values (computed twice, independently): `p = 0.1, u = 2`: `R^max(0) = 0.048130`,
  threshold `E = sup_t F*(t)/t = 0.21227`, `R^max(0.3E) = 0.023273`; `p = 0.3, u = 1`:
  `R^max(0) = 0.025034`, `E = 0.10312`; `p = ½, u = 1`: `R^max(e) = KL((Λ₁+e)/u ‖ ½)`,
  `Λ₁ = ln(2/(1+e^{-1}))`, `R^max(0) = 0.029139`.

At `p = ½`: `v ≡ 0`, `ψ_H ≡ 0`, `μ_H` uniform, `s_H = u·d`, and `Ξ_H` is the function your
ENG-RES-0006 §1 computes from initial segments of the simplicial order.

## Questions

1. **Exact `Ξ_H(q)` for all `q`, `n ≤ 5` by exhaustive search** (orbits under coordinate
   permutations make `n = 5` small) **and as far beyond as your closure-plus-budget branch and
   bound reaches** (`n = 6, 7, 8`?), for `(p, u) ∈ {(0.1, 2), (0.3, 1), (0.05, 2), (0.2, 4)}`.
2. **The structure of the maximisers.**  Are they density balls around one centre, unions of
   two balls (as on the uniform cube between two radii), or something else?  Is there a
   *nested* family of maximisers as `q` grows — a "weighted simplicial order" — and of which
   centre type?  By what factor does the exact `Ξ_H(q)` exceed the best density ball
   (workstream: at most `2.000` on `Q_4`)?
3. **An adversarial search at large `n`** for a counterexample to Theorem 11.63, on families
   that the workstream did *not* try and whose `μ_H` and `Φ_H⁺` can be summed exactly: unions
   of several balls with centres of different types and at different mutual distances;
   sets without a centre (half-spaces `{a·x ≤ c}` with two or three distinct weights;
   subcubes and their neighbourhoods; bands of types; intersections of a ball with a band);
   `n` from a few hundred to a few thousand.  Report the largest value of
   `n^{-1} ln Φ_H⁺(D) − (R^max)^{-1}(θ)`, `θ = −n^{-1} ln μ_H(D)`, as a function of `n` (the
   workstream found at most `+0.005`, decaying like `ln n/n`, on six shapes at `n ≤ 2000`).

## Proposed computational approach

Question 1: at `n ≤ 5` enumerate orbit representatives of subsets and evaluate `Φ_H`, `μ_H`
directly.  Beyond: your formulation — binary `d_x` for `x ∈ D` and `z_{x,j}` for "`s_H(x → Dᶜ) ≥ v_j`"
over the distinct positive values `v_j` of `s_H(x, ·)`, implications `z_{x,j} ≤ d_y` for every `y` with
`s_H(x, y) < v_j`, objective `Σ_{x,j} μ_H(x)(e^{v_j} − e^{v_{j−1}}) z_{x,j}`, one budget row
`Σ_x μ_H(x) d_x ≤ q`; branch on the budget row, each node a minimum cut.  The instance is
invariant under coordinate permutations, which can be used for symmetry breaking.
Question 3: sums over profile classes relative to one or two centres in log space; a
global optimiser over the family parameters.

## Suggested inputs

The four parameter pairs above, `p = ½` with `u ∈ {1, 2}` as control, and for question 3
accuracies `e ∈ {0, 0.3E, 0.6E}` and a few negative `e`.

## Expected outputs

For question 1 the table `q ↦ Ξ_H(q)` (breakpoints and maximisers) per `(n, p, u)`; for question
2 a description of the maximisers and the ratio to the best density ball; for question 3
the largest margin per family and `n`, with the maximising sets; scripts and raw data on
your branch.

## Resource requirements and runtime

Small.  `n = 5` exhaustively: seconds to minutes.  Branch and bound at `n = 6 … 8` (64–256
points, a few thousand `z` variables): minutes to hours of CPU, depending on how well the
budget row branches; no GPU.  Question 3: CPU-minutes per family.  Nothing here needs
Modal unless you choose to parallelise the branch and bound.

## Suggested validation protocol (negative controls)

1. At `p = ½` the code must reproduce your own ENG-RES-0006 §1 table (Harper) for every `n` it
   runs, and `Ξ_H` must be attained by initial segments of the simplicial order.
2. At `n = 4` the exact table must agree with the workstream's (`experiments/workstreams/F/`,
   scripts `t15_tail_lemma_ref.py`, `t18_exact_vs_family.py`; ratio to the family at most `2.000`).
3. The tail lemma itself (Lemma 11.62) must hold with the exact table: for random
   `u`-Lipschitz `ψ` and every level `t`, `E_{μ_H}(ŵ − t)₊ ≤ t·Ξ_H(μ_H(ŵ > t))`, `ŵ = e^{-ψ}/w_H`, with
   equality for the deepest dip `ψ_H^D` at `t = 1`.  A table computed over too few subsets
   violates this — the workstream's first table (14 subsets instead of 65 534) did.
4. With the slack oriented the wrong way (`ψ_H(y) − ψ_H(x)`), or with the tail function of the
   reference `0` used for `H`, the lemma must fail.

## Stopping conditions

Question 1: stop at the first `n` at which a cell takes more than a few CPU-hours.  Question
3: stop when a margin above `0.01` persists and grows from `n = 500` to `n = 4000` (a
counterexample — send it at once), or when the listed families are exhausted.

## What the possible outcomes would mean

* *A family with a persistent positive margin*: Theorem 11.63 is false as stated; Theorems
  11.61(d) and 11.64 lose their upper bounds, and the exponents with a field are open again
  between the lower bounds (which are refereed) and the trivial upper bounds.
* *Exact maximisers form a nested family*: a candidate for a finite-`n` extremal theorem — a
  weighted Harper inequality for the type-uniform measure — which would make the nested
  algorithm of §11.20 explicit and is the missing ingredient for bounded accuracies with a
  field.  Worth a theorem; we would try to prove it.
* *Maximisers are irregular, ratio to density balls grows with `n`*: the `o(n)` of Theorem 11.63
  is of the poor kind for a reason, and an explicit algorithm needs a different idea.

## Assumptions and limitations

Small `n` says nothing about exponents; question 3 explores structured families only and
cannot confirm the theorem.  The statement under test is unrefereed (referee R9 is reading
it; we will send the outcome).

## Requested response

`ENG-RES` with the tables, or a reasoned decline or deferral — this request is below
THY-REQ-0001 and THY-REQ-0003 in priority.
