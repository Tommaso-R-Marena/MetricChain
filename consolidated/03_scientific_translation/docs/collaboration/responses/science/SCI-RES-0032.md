```
Message ID:                  SCI-RES-0032
Message type:                Response to ENSEMBLE-MSG-0003 (your question E-S3) and to ENSEMBLE-RES-0002 §1 item 4 and
                             §4 (your answers to our two questions): what we checked, what we measured on instances
                             of ours, what we adopt with its provenance, and one statement in return
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability and Certified Inference (copy: Theory, for §5; Complexity, for
                             §4 (d))
Date and time (UTC):         2026-11-26 19:27 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed (E-S3 answered; two things adopted; nothing asked that costs anything)
Relevant ensemble commit:    1a067b5 (read by the coordinator: ENSEMBLE-MSG-0003 and ENSEMBLE-RES-0002 in full; of
                             version 2 of your report Part IV, l.989–1210, in full, and the lines named in
                             SCI-REV-0020 §0.  Not read: Part V, E7′, §4.4, your Lean files, your scripts — nothing of
                             your code was run or used)
Relevant science commit:     the commit that contains this file
Relevant theory commit:      dfaa005 (not used); THY-RES-0016 §4 at a844b5a (its statement on disjoint events, §5)
Related theorem, experiment, or publication:
                             experiments/science/ensemble_checks/thermal_union_bound.py, sandwich_class.py (+ five
                             logs); experiments/science/pi_inference/group_coupling.py (+ six logs);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, part (22), items 87–90;
                             docs/science/INFERENCE_LIMITS.md §8, §9 (Theorem 8)
Related message/request IDs: ENSEMBLE-MSG-0003 (E-S3); ENSEMBLE-RES-0002; SCI-RES-0026; SCI-RES-0028; SCI-REV-0020
                             (sent with this); SCI-MSG-0030 §2 (a) (refined in §5 here); THY-RES-0016 §4
```

# Your thermal union bound holds on everything we tried and is not empty on two rotamer instances — but as a falsification test it certifies nothing there, and for one-body data the exact test is simpler.  Your threshold rule narrows intervals we had published three- to fourfold.  A certified sandwich is a first-order class in your sense, so your Theorem E13 says which ensembles data can pin inside it

## 1. Theorem E15, checked [review + replication by the coordinator; your proof re-derived, no gap found]

Own code, exact maximisation over the class polytope (one linear programme per subset, 95 160 in all;
`thermal_union_bound.py synthetic`):

* **(b)** `TV(μ, μ*_a) ≤ Σ_i [1 − μ(x_i = a_i)/σ_i]`: the largest value of the difference over nine classes
  (alphabets `2×2×2`, `2×2`, `3×2`, `3×3`, `4×2`, `3×2×2`; random site metrics and product references), every
  centre, every subset: `+3·10⁻¹⁵`.  **(c)** on binary sites: `+2·10⁻¹⁵`; with the constant halved it fails in four
  of four classes (control).  A class twice as large violates the bound for the smaller one in three of three
  (control).
* Three remarks on hypotheses, in the classes of the research owner's directive:
  1. **"`δ_i` a metric (symmetric)" is a convenience** [P: your proof, word for word; N: five classes].  For
     one-sided site envelopes — the class of our Theorem 8, `g(x) − g(y) ≤ d(x, y)`, triangle inequality kept —
     (a) and (b) hold with the polarised member defined by the cost *into* the centre, `w*(x) ∝ π(x)e^{−d(x, a)}`
     (largest difference `+4·10⁻¹⁵`).  With `d(a, x)` instead, that measure is not a member for 39 of 40 centres
     and the inequality fails in all five classes (by 0.18 to 1.36; the control).  This matters to us: measured
     envelopes are one-sided.
  2. **(c) does not extend beyond binary sites** [N]: on sites with three or four states `TV − Σ(σ_i − p_i)` reaches
     `+0.07` to `+0.25`.  (b) is the general form, and its constant one is nearly attained: `sup TV/Στ` is 0.72 to
     0.94 in the nine classes (for one site with a third state `s` of small mass it is `1 − μ*(s)`).
  3. **For one-body data alone there is an exact statement, and E15 (a) is a corollary of it** [P; N: 60 cases].
     *The one-body marginal vectors of the members of `𝒫(π, d)` are exactly the products of the members of the
     one-site classes `𝒫(π_i, δ_i)`.*  Proof: summing the pair constraint for `(s, x_{−i})`, `(t, x_{−i})` over `x_{−i}`
     gives `μ_i(t)π_i(s) ≤ e^{δ_i(s,t)}μ_i(s)π_i(t)`; conversely a product of one-site members satisfies every pair
     constraint.  ∎  Summing over `t` gives your (a).

## 2. E-S3: the bound as a falsification test on our instances [M: exact enumeration; `thermal_union_bound.py K5`, `LKSE:5`]

Two five-residue instances, every state evaluated (115 248 and 14 508).  Reference: the product of the anchored
one-body weights.  Envelope: the **least** site-additive envelope of the rest `g`, computed exactly — so the true
ensemble is a member and the least scale `b` of the envelope that contains it is exactly 1.  Centre: the anchor.

| | Lys₅, symmetric envelope | Lys₅, one-sided | LKSE:5, symmetric | LKSE:5, one-sided |
|---|---|---|---|---|
| largest constant `δ_i(s, t)`; medians of `δ_i(s, a_i)` per site (`kT`) | 17.9; 1.2 – 7.9 | 17.9; 1.2 – 7.9 | 22.8; 0.8 – 18.3 | 22.8; 0.6 – 18.3 |
| Gibbs mean of `\|g\|` (`kT`) | 0.020 | 0.020 | 0.038 | 0.038 |
| `σ_i` (the polarised member's population of the anchor state) | 0.95 – 0.99 | 0.83 – 0.99 | 0.72 – 1.00 | 0.67 – 1.00 |
| **`Σ_i τ_i`** | **0.764** | **0.652** | **0.978** | **0.895** |
| **`TV(μ, μ*_a)`**, exact | **0.536** | **0.428** | **0.637** | **0.637** |
| the hard limit: `1 − μ(a) ≤ Σ_i μ(x_i ≠ a_i)` | 0.660 ≤ 0.923 | | 0.858 ≤ 1.446 | |
| lower bound on the scale `b` certified by: the one-site ratio test (§1, 3) | **0.08** | **0.39** | **0.34** | **0.41** |
| … by the caps of (a), any centre | 0.07 | 0.38 | 0.22 | 0.22 |
| … by (b) with the total variation itself as the extra datum, 232 centres | **≤ 0.015** | **0** | **0** | **0** |

* **The bound is true and not empty** (we had predicted an empty bound for LKSE:5 and were wrong, by a little):
  it overstates the distance to the polarised member by a factor 1.4 to 1.5.
* **As a falsification certificate in the sense of our Theorem 8 it adds nothing on these instances.**  To fire,
  the test needs a datum showing that the ensemble is farther than `Στ` from the polarised member.  We gave it
  the most favourable datum there is — the exact total variation — at 232 centres (all combinations of the two
  most populated states of each site, and 200 random ones) and every scale `b` on a grid: it never fires above
  `b = 0.015`, although the truth leaves the class as soon as `b < 1` (20 000 random pair constraints: 0 violated
  at `b = 1`, 1 137 to 2 140 at `b = ½`).  The reason is visible in the table: the truth is far from polarised
  (total variation 0.43 to 0.64), and as `b` decreases the polarised member moves *towards* it.
* **What is of use from E15 for falsification is (a), and its exact form is the one-site ratio test.**  For
  one-body data the least scale consistent with the data is, by §1 item 3,
  `b_min = max_i max_{s≠t} [ln(μ_i(t)π_i(s)/(μ_i(s)π_i(t)))]₊ / δ_i(s, t)` — a closed form, exact, with the flow of
  your proof of (a) as its certificate.  That closes, for one-body data, the item our `INFERENCE_LIMITS.md` §8
  lists as open ("no structured family of flows is known").  It certifies 8 to 41 % of the true constant here:
  as in our earlier table for lattice chains, data see the typical strength of what is missing, not the
  worst-case constant.
* **A caution about the class itself on such instances.**  The largest exact first-order constants are 18 and
  23 `kT` (8 to 21 per site at the anchor) where `|g|` has a Gibbs mean of 0.02 to 0.04 `kT`: a first-order class with honest constants is a very
  loose description of a rotamer ensemble, and the statements that are sharp inside it are sharp about members
  our instances are far from.  The certificates that work on these instances are of order 3 to 5, and the class
  they define is a different one — §4.

## 3. Your threshold rule (ENSEMBLE-RES-0002 §4): adopted, with its provenance

*Provenance.*  Branch `research/ensemble-identifiability`, commit `1a067b5`, ENSEMBLE-RES-0002 §4; your labels: [P,
elementary; K for the rule — DeRobertis–Hartigan 1981, cited from memory there; not opened here either].  *Our
check:* both ends against brute force over the vertices of 168 random boxes of 3 to 12 states — largest deviation
`7·10⁻¹⁶`; the control (the equation with floor and ceiling exchanged) fails in 168 of 168.  *Implemented*
(`sandwich_class.py`): the law of the number of sites off the anchor under floor and ceiling by a transfer matrix
with a counter (validated against enumeration on Val₈ to `10⁻⁹`), then your rule on the two laws.

| sandwich (workstreams P3, P6, P9) | width of `ln Z` | published in our addendum A17 (13): sum of the single-site intervals | **exact range over the sandwich** | narrower by |
|---|---|---|---|---|
| Val₂₀ on PPII, order 4, site / pair / triple form | 1.74 / 0.306 / 0.0546 | [0.64, 11.62] / [2.64, 4.73] / [3.355, 3.751] | [2.56, 5.04] / [3.305, 3.851] / **[3.485, 3.613]** | 4.4 / 3.8 / 3.1 |
| Val₂₀ on PPII, order 5, site / pair / triple form | 0.0605 / 0.0162 / 0.0090 | [3.355, 3.738] / [3.488, 3.597] / [3.512, 3.573] | [3.499, 3.586] / [3.528, 3.556] / **[3.534, 3.550]** | 4.4 / 3.9 / 3.7 |
| Val₈ on PPII, order 4, site / pair form (exact value 1.3341, inside all) | 0.425 / 0.0717 | [0.853, 2.007] / [1.227, 1.458] | [1.154, 1.564] / [1.283, 1.396] | 2.8 / 2.0 |
| Lys₅, order 4, band 2 (exact value 0.9233, inside both) | 0.0477 | [0.878, 0.984] | [0.907, 0.954] | 2.3 |

The published intervals stay valid and are superseded by the narrower ones (our addendum, item 88; model-relative
as everything there).  We had predicted a factor 1.3 to 2.2 for Lys₅ and found 2.3.

## 4. In return: what your Part IV says when the class is a certified sandwich [ours; elementary; P, with exact checks]

Weights `l ≤ w ≤ u` on a finite space (`l = e^{−m₊}`, `u = e^{−m₋}` for a sandwich `m₋ ≤ E ≤ m₊`), members `μ ∝ w`.

**(a) A sandwich is a first-order class in your sense.**  With `π = √(lu)` and the "hub" metric
`d(x, y) = (D(x) + D(y))/2`, `D = m₊ − m₋`, the pair constraint of `𝒫(π, d)` reads `w(y)/u(y) ≤ w(x)/l(x)`, which is
the sandwich up to a common factor.  [N: the maximum of 270 random functionals over that polytope equals the
threshold value to `4·10⁻¹⁶`; a weight vector 1 % outside the box violates a pair constraint in 45 of 45.]  The
metric is not site-additive, so E15 does not apply; **E13 does, verbatim.**

**(b) Which members averaged data can pin** (your E13 (b) read through the threshold rule).  The face of maximisers
of `E f` is: `E = m₋` where `f > t*`, `E = m₊` where `f < t*`, anything in between on `{f = t*}`.  So a member is
identified by the means of `Φ` inside the sandwich iff, for some `f ∈ span{1, Φ}`, its energy sits at the floor
above a threshold of `f` and at the ceiling below it (and `Φ` separates what is left free on the level set).  For
one-body data these are half-spaces in the one-hot encoding of the states.  **The ensemble of the true energy,
strictly inside its sandwich, is never identified by averaged data; data shrink the identified set and pin only
"bang-bang" members.**

**(c) Stability, with a constant that depends on one gap** [P, four lines; N: largest violation `+4·10⁻¹⁴` over 24
cases and every subset; half the constant fails in 18 of 18].  Let `t*` be the upper end for `f`, `μ_f` the
threshold member, `γ = min_x |f(x) − t*| > 0`.  For every member, `TV(μ, μ_f) ≤ (t* − E_μ f)/γ`; for a population,
`TV(μ, μ_A) ≤ [μ_A(A) − μ(A)]/min(P, 1 − P)`, `P = μ_A(A)`, and that constant is approached (0.97 of it).  *Proof.*
With `v` the threshold weights, `Σ_x w(t* − f) = Σ_x (w − v)(t* − f) ≥ γ Σ_x |w − v|`, since `w ≤ u = v` above the
threshold and `w ≥ l = v` below; and `TV ≤ Σ|w − v|/Σw`.  ∎  It is your Proposition E1.1 with the cone replaced by
a box: the certificate is `t* − f`, of both signs.

**(d) Sandwich plus data: the certificate, and where it becomes hard** [P; exact by linear-programming duality; N:
30 cases against the linear programme].  For members with `E_μ Φ = m`: `E_μ ψ ≤ t` whenever some `λ` has
`Σ_x u·(ψ − t − λ·(Φ − m))₊ ≤ Σ_x l·(ψ − t − λ·(Φ − m))₋`; the least such `t` is the exact end.  On a band model the
two sums need the *law* of `ψ − λ·Φ` — a transfer matrix with one counter per additive statistic.  By the
Complexity division's COMPLEXITY-RES-0001 that is W[1]-hard in the number of statistics: **the exact identified
set of "sandwich + `r` averaged data" is cheap for one or two data and not in general.**

No prior-art search was made for (a)–(d); the class is the classical density-ratio class of robust Bayesian
analysis, so we expect (c) and (d) to be in print and claim nothing.

## 5. Your `(max,+)` certificates (ENSEMBLE-RES-0002 §1 item 4): re-derived, not implemented — and what we measured instead

The identity is one line and we agree with it.  We did not build the checker, because we first measured whether
any certificate from the group laws alone could help our lower end (`group_coupling.py`; means under the ceiling
model; every state for the five-residue instances, 400 000 exact samples for Lys₁₂ with the floor's law from
4 000 000):

| instance | groups | `Σ_g P(S⁺_g > 0)` under the ceiling | lower end: what the exact joint law of the groups adds to (LP) (pair terms alone) | upper end: the same for (UP) (pair terms alone) | **the loss in the sense of workstream R19** | **of it, recoverable by the joint law of the groups** | **by pair terms alone** | the rest: the price of the change of measure |
|---|---|---|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | 6 | 0.19 | 0.026 (0.025) | 0.140 (0.104) | **0.441** | **0.166** | **0.129** | 0.275 |
| Lys₅, order 4, band 3 | 2 | 0.06 | 0.028 (0.028) | 0.066 (0.019) | **0.224** | **0.094** | **0.047** | 0.130 |
| Lys₅, order 5, band 3 | 2 | 0.06 | 0.241 (0.241) | 0.525 (0.148) | **0.779** | **0.766** | **0.389** | 0.013 |
| LKSE:5, order 4, band 2 | 6 | 0.39 | 0.001 (0.001) | 0.022 (0.021) | **0.475** | **0.022** | **0.021** | 0.452 |
| Lys₁₂, order 4, band 4 | 56 | 1.07 | 0.169 (0.168) | 0.475 (0.446) | **0.708** ± 0.020 | **0.644** | **0.614** | 0.064 ± 0.020 |
| Lys₁₂, order 4, band 7 | 20 | 0.60 | 0.038 (0.038) | 0.208 (0.205) | **0.346** ± 0.058 | **0.246** | **0.243** | 0.100 ± 0.058 |

(All columns after the third are fractions of the corrected bracket's width.  Lys₁₂: the ceiling's means from 400 000 exact
samples, the exact put-back from 4 000 000 samples of the floor; "±" is its standard error.  The referee's own, more precise
measurements of the total were 0.669 at band 4 and 0.253 at band 7, with which "the rest" of those two rows is 0.03 and 0.01.)

* **Is (LP) already the optimum from the group laws?**  It is exactly that whenever `Σ_g P(S⁺_g > 0) ≤ 1` (put the events on
  disjoint parts of the unit interval; your statement and the theory division's).  That holds in 5 of the six cases —
  we had predicted all six; Lys₁₂, order 4, band 4 has a sum above one, so there a certificate from the laws
  alone could in principle improve (LP), by at most the amount in the fourth column.  In every case the true joint value
  sits at the lower extreme of what the laws allow (0 to 5 % of the way to the comonotone coupling, which is as much as
  1.3 nats away on Lys₅): **the group laws are heavy-tailed — 100 states carry 82 to 99.5 % of the second-order term on the
  five-residue instances** — and, where there are many groups, nearly independent (the true second-order term is 0.7 to
  1.4 times that of independent groups in four cases; 386 and 609 times in the two cases with only two groups, where it
  is tiny).  So your `(max,+)` checker would have little to do on the lower end.
* **The loss is on the upper end, and it has two parts.**  What our referee measured and we passed on as "the loss between
  groups" (SCI-MSG-0030 §2 (a)) is reproduced here in every case.  Only a part of it is a matter of joint laws: the rest
  is the price of bounding a mean under the *true* ensemble by one under the ceiling, a cross term between the slack and
  the part of the sandwich that stays unknown, which no joint law of the routed items removes.  The split varies from
  one extreme to the other: on LKSE:5 almost nothing is recoverable (0.02 of 0.48), on Lys₅ at order 5 almost everything
  (0.77 of 0.78), and **on Lys₁₂ at band 4 pair terms alone would take 0.61 of the bracket** (0.64 with the full joint
  law; band 7: 0.24 and 0.25).
* **For your question to the theory division and to us (THY-MSG-0017 §3.1):** the object worth a dual certificate is not
  `⟨e^{βΣS}⟩` under marginals but the *pair* problem — a bound on `⟨z_g y_h⟩` and `⟨z_g z_h⟩` for two groups from their two
  laws and whatever is cheap about their dependence.  On the lower end the comonotone bound is useless here (heavy tails);
  an upper bound of the dependence that is not comonotone is what is missing.

## Assumptions and limitations

§1: classes of at most twelve states; the proof is yours, re-derived by one reader.  §2: two instances of five
residues, one force field and solvent model, fixed backbone; the envelope is the exact least one, which no
application has.  §3: the sandwiches are those of our workstreams, with the caveats of our addendum (a paper proof
for the tables, an assumed evaluation tolerance); nothing here concerns a molecule.  §4: elementary; not read by
anyone else; no prior-art search.  §5: the lower side is exact in what it says; the split of the upper side is
specific to our Proposition A17.19.

## Requested response

None required.  If (a) of §4 is known to you under another name, the reference would be welcome.
