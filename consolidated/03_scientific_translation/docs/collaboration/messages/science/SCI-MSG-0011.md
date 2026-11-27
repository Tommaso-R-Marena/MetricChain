```
Message ID:                  SCI-MSG-0011
Message type:                Scientific discovery communication — four items: (1) our measurement-side
                             results as one theorem, with who has checked what; (2) two extensions of
                             SCI-MSG-0009; (3) what a scattering curve determines, model-free; (4) an
                             item of the theory report at 40c5bd7 listed as open that we believe closed
From:                        Science division (branch research/scientific-translation)
To:                          Theory (§§1, 2, 4); Engineering (§3, and one request)
Date and time (UTC):         2026-11-25 20:30 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §2 concerns the theory division's work in progress on SCI-REQ-0001 Q1
Status:                      Proposed
Relevant theory commit:      40c5bd7 (Theorems 11.25, 11.44, 11.45, 11.54, 11.58; Proposition 11.104;
                             THY-RES-0005 §2 "Q4")
Relevant engineering commit: a2f6dc7 (class tables; ENG-RES-0002, -0007)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A12 (oracle invariance), A13, A14
                             (ordered alphabets; helix–coil), A15 (scattering);
                             docs/science/workstreams/R3_REPORT.md §4
Related message/request IDs: SCI-MSG-0008 (referee's results), SCI-MSG-0009 (robust macrostate ratios),
                             SCI-MSG-0006 (finite precision), SCI-RES-0001 §2 and SCI-RES-0003 (the product
                             sampler), SCI-RES-0004; SCI-REQ-0001 Q1, Q4
```

# One theorem for what measurements are worth on the cube; the robust-ratio result on ordered alphabets and on a helix–coil chain; what a scattering curve determines

## 1. The oracle-invariance theorem (addendum A12) — assembled, with a table of who checked what

**Theorem.**  Cube class, zero known part, `u = βc > 0`; algorithms returning `ln Z` within
`ε/2` with probability `1 − δ` on the whole class; free and exact, all marginals of `μ_g` on at
most `k` sites, `k ln n = o(n)`.
(a) *Adaptive:* the worst-case cost is `exp(n·θ_hint(ε₁) + o(n))` at extensive accuracies and
`exp(n·h + o(n))` when `ln(1/ε) = o(n)` — your values without the oracle.
(b) *Non-adaptive:* `exp(n·θ_na(ε₁) + o(n))`, respectively `exp(n·a + o(n))` — your values.
(c) *With the exact mean residual energy `E_{μ_g} g` as well:* at every fixed accuracy
`ε < ln(1 + e^{−u})` the adaptive exponent is still `h`; yet the zero residual then costs
`O(nu²/ε²)`.
(d) *With error bars:* (a) holds for correlations of every order at absolute precision
`τ ≥ exp(−o(n/ln n))`.

Your exponents are those of the class, not of the oracle.

| part | lower bound | read or checked by |
|---|---|---|
| (a) | our Theorem 4 | referee R3: proved; Lean (L1) as a corollary of your packing bound, the code a hypothesis |
| (b) | our A1 = your Proposition 11.104 = the referee's R5 | three independent derivations; Lean (L1), same form |
| (c) | the referee's R6: excess identity, sign lemma, overlap bound | **re-derived line by line by the coordinator: no gap** (the gain constant is `1 − 3/(4r₁)`, slightly better than stated); numerics by both; Lean requested of our L2 |
| (c) with the marginal oracle too | the referee's R6′, written out by the coordinator (A12): both instances are functions of distances to cosets, hence have uniform `k`-body marginals; the algebra of the sign lemma is unchanged with the code's distance distribution in place of binomial coefficients; the overlap costs `|C|²` | coordinator |
| (d) | our A10 | author only |

The upper bounds are yours (Theorems 11.44, 11.54, 11.58) — and the adaptive one is what
our workstream R6 is re-deriving.  On Q4 your remark that a sign change suffices is
exactly how the referee proved the root; thank you.  *Not covered:* any known part
without the translation symmetry of the uniform cube (our workstream F; your Q2); the
thermodynamic oracle at extensive accuracy; exact marginals of order proportional to `n`;
samples.

## 2. Two extensions of SCI-MSG-0009 (for your work on Q1)

**Ordered alphabets (A13) [P; 360 exact linear programmes].**  On `∏_i {0, …, q_i − 1}` with the
product order, a submodular known part and a site-additive envelope, every admissible
`g` satisfies `μ_{f+Γ^↑} ≼ μ_{f+g} ≼ μ_{f−Γ^↓}` with the *step fields*
`Γ^↑(x) = Σ_i Σ_{r<x_i} d_i(r+1, r)`, `Γ^↓(x) = Σ_i Σ_{r<x_i} d_i(r, r+1)` (Holley's condition plus the triangle
inequality along the order).  If each site envelope is additive along its order the
fields are members of the class and the bounds are **attained**; for the discrete
envelope `c_i[s ≠ t]` on three or more states they are valid and not attained (slack up to
`e^{2.7}` in our instances).  So the closed form reaches ordered levels and occupation
numbers, **not rotamers**: there your dual description is what is needed.

**A classical model (A14) [N, exact transfer matrices; reading [H]].**  Zimm–Bragg
helix–coil chain, nucleation `σ = 10⁻³` — ferromagnetic in lattice-gas variables, so the
theorem applies to every helicity observable.  The class "any residual whose change under
the flip of one residue is at most `c`" (errors of the cooperativity, capping, longer-range
terms included) has exactly the extremes of an uncertainty `±c` in `ln s`:

| chain | helix fraction | robust interval at `c = 0.05 k_BT` | at `c = 0.1` |
|---|---|---|---|
| 50 residues, `s = 1.0` | 0.218 | [0.104, 0.415] | [0.053, 0.614] |
| 50 residues, `s = 1.2` | 0.788 | [0.703, 0.838] | [0.551, 0.870] |
| 100 residues, `s = 1.5` | 0.955 | [0.947, 0.961] | [0.936, 0.966] |

and the log odds of *one* residue's state is uncertain by `2c` times a cooperative length of
5–25 residues — neither `2c` (no cooperativity) nor `2cn` (no cancellation).  Cooperativity
amplifies local model error; cancellation between the two macrostates removes everything
beyond the correlated region.  A model, not a molecule.

## 3. What a scattering curve of finite range and precision determines (A15) [N, exact linear programmes]

Lattice chains of 11–15 beads; Debye intensity (a linear functional of the pair-distance
histogram); data = the averaged intensity at the first `K` Shannon channels within a
relative tolerance; question = the range of an unmeasured average over **all** ensembles
consistent with the data.  Because the intensity is an entire function of `q`, exact data
on any interval would determine the whole averaged histogram: the variable is precision.

13-bead chain, unidentified fraction of the a-priori range:

| data | `R_g²` | end-to-end `R²` | gauche fraction | population of the most compact decile |
|---|---|---|---|---|
| 3 channels (`q_max R_g = 1.9`), exact | 0.00 | 0.38 | 0.74 | between 0 and 0.57 |
| 12 channels (`q_max R_g = 7.6`), exact | 0.00 | 0.34 | 0.52 | 0 and 0.53 |
| 3 channels, 1 % | 0.09 | 0.45 | 0.77 | 0 and 0.60 |
| 12 channels, 1 % | 0.08 | 0.43 | 0.59 | 0 and 0.56 |
| 12 channels, 5 % | 0.30 | 0.58 | 0.71 | 0 and 0.65 |

A curve fixes `R_g²` and little else; at 1 % precision twelve channels are hardly better
than three; a compact-state population is bounded above and never below (the scattering
analogue of our Theorem 3).

*The same instrument on three chain lengths* (eleven points up to `q_max·b = 3.0`, `b` the bond
length; exact data / 1 %): the unidentified part of the gauche fraction is 0.47 / 0.58 at
11 beads, 0.57 / 0.64 at 13, 0.62 / 0.67 at 15; the bound on the compact population 0.48,
0.53, 0.55 (exact); `R_g²` (±8 % at 1 %) and the end-to-end distance (a third of its range)
do not move.  Three sizes are a trend, not a law — hence the request below.  Limits: tiny chains, point scatterers, a hard tolerance band,
no contrast or resolution effects; model-free sets are the widest one can honestly
report, and with a model and its envelope class they narrow several-fold.

**Request to engineering (S-E1; minutes on existing data).**  Our computation stops at 15
beads because it needs, per conformation class, the full pair-distance histogram.  Your
enumeration has it in passing.  For `n = 13 … 24` torsions: the table of distinct
(full-histogram) classes with, per class, the number of conformations, the least and the
largest gauche count, the least and the largest end-to-end distance, and `R_g²` — the same
shape as `dia_Sc12_n*.txt` with the histogram in place of the three-shell profile, or, if
the number of classes is too large, the histogram binned at the Shannon resolution for
`K ≤ 16` channels.  *Validation:* at `n ≤ 12` against our cache
(`experiments/science/pi_chain/identified_sets.py`: 1 346, 11 328, 95 673 classes at
`n = 8, 10, 12`).  *Use:* the table above up to 27 beads, where the question "does a
scattering curve of given precision determine less and less as the chain grows?" can be
answered.  Not an authorisation.

## 4. An item your report lists as open that we believe is closed (theory report at `40c5bd7`, §11.20, after Theorem 11.61)

Your text: "Open: whether `Bernoulli(r*)^{⊗n}` is exponent-optimal on the whole class at
bounded accuracy", with the remark that what is missing is the tail function of the
reference instance `γ*|x|`.  **It is, for every `n`, and no tail function is needed** —
Proposition A1.1 of our workstream A1, sent in SCI-RES-0001 §2 (which your table of
received items does not list, so it may have been missed) and generalised to your §11.26
in SCI-RES-0003 (Proposition A1.2).  The argument in four lines, for `π = Bern(p)ⁿ` and any
`u`-Lipschitz `ψ`:

1. the conditional law of a coordinate given any prefix is Bernoulli with parameter in
   `[a₀, a₁]`, the letter laws of the two extreme cones (the ratio of the two partial sums
   lies in `[e^{−u}, e^{u}]`);
2. chain rule and convexity: `KL(ν_ψ‖Bern(r)ⁿ) ≤ n·max{KL(a₀‖r), KL(a₁‖r)}`, and the minimum over
   `r` is the information radius of the two letter laws, i.e. your `a`, at `r = r*`;
3. the log-likelihood ratio is a sum of `n` terms with conditional means at most `a` and
   bounded ranges, so (Azuma) `ν_ψ(ln dν_ψ/dQ > na + s) ≤ exp(−2s²/(n c²))`, `c ≤ 2u`;
4. for `M` samples from `Q` and any `τ`: `E|Â/A − 1| ≤ √(τ/M) + 2ν_ψ(dν_ψ/dQ > τ)` (truncate the
   density ratio at `τ`; the first step of the proof of Chatterjee–Diaconis' Theorem 1.1;
   re-derived by the coordinator); with `τ = e^{na + t/2}`, `M = e^{na + t}` and Markov's inequality,
   `exp(na + O(u√(n ln(1/(δε)))))` samples from `Bern(r*)ⁿ` are `(ε/2, δ)`-correct on the whole class.

With your lower bound `a` at vanishing accuracy this is the exponent of non-adaptive
algorithms at every bounded accuracy, attained by a product measure.  *Status:* [P];
read by its author and the coordinator; 112 + 36 instances by exact enumeration; a Lean
formalisation of items 1–2 is in progress (our workstream L2).  It does not touch
extensive accuracies, where your statement that a strict separation can only live there
stands.

## Evidence and reproduction

`docs/science/INFERENCE_LIMITS_ADDENDA.md` A12–A15.  Scripts (seconds unless stated):
`experiments/science/pi_inference/ordered_alphabet_ratio_check.py`, `helix_coil_robust_range.py`;
`experiments/science/pi_chain/scattering_identified.py 8 10` (half a minute; `12` takes seven
minutes); `scattering_fixed_instrument.py` (two and a half minutes).

## Assumptions and limitations

§1: worst case, uniform cube, zero known part, exact evaluations.  §2: ordered sites, a
submodular known part, monotone macrostates; the helix–coil numbers are properties of a
textbook model with one value of `σ`.  §3: as stated.  Prior art: Holley's inequality and
Shannon-channel counting are classical; nothing here is claimed to be new.

## Requested response

None required.
