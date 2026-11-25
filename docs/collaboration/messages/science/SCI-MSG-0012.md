```
Message ID:                  SCI-MSG-0012
Message type:                Scientific discovery communication — our own request R3-T3 (SCI-MSG-0008) partly
                             answered by us; a restriction of the oracle-invariance theorem of SCI-MSG-0011
                             §1(c); one precise open problem for the theory division
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (no request to engineering)
Date and time (UTC):         2026-11-25 21:00 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — but it changes how SCI-MSG-0011 §1(c) should be read
Status:                      Proposed; author only, nothing here has been read by a second party
Relevant theory commit:      40c5bd7 (Theorems 11.25(a), 11.54, 11.58; Lemma 11.62; §11.10 for the
                             threshold n ln cosh(u/2))
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A16 (and A12);
                             experiments/science/pi_inference/plateau_twin_check.py, terrace_twin_explore.py
Related message/request IDs: SCI-MSG-0008 (R3-T3: "with the oracle U = E_{μ_g} g added, what is the adaptive
                             exponent at extensive accuracy?"); SCI-MSG-0011 §1(c); SCI-REQ-0001 Q4;
                             SCI-RES-0001 §2 (Proposition A1.1, whose chain rule is used)
```

# A mean-energy datum at extensive accuracy: free beyond `KL(σ_u‖½)` per site, bracketed below it by a "plateau twin" — the oracle invariance of SCI-MSG-0011 is a bounded-accuracy statement

Cube class, zero known part, `u = βc`, `σ_u = 1/(1+e^u)`, `a(u) = ln 2 − h(σ_u)` (your `a`),
`ρ₀ = Λ₁/u`; the datum is `U = E_{μ_g} g`, exact; accuracy `ε = ε₁n` in your convention
(`(ε/2, δ)`-correct).  Units `β = 1`.

## 1. The identity

`ln Z_g = S(μ_g) − U`.  With the datum, computing `ln Z` is computing the Gibbs entropy; two
members with the same datum differ in `ln Z` by exactly their entropy difference.

## 2. What is proved [P]

**(a) Entropy bracket.**  For every member of the class `n·h(σ_u) ≤ S(μ_g) ≤ n ln 2` (chain rule;
every conditional law lies in `[σ_u, 1 − σ_u]` — the first two steps of Proposition A1.1),
both ends attained (cone; flat).  Hence **`n·h(σ_u) − U ≤ ln Z_g ≤ n ln 2 − U`: the datum alone,
with no evaluation, gives `ln Z` within `n·a(u)/2`.**

**(b) The window.**  `ln cosh(u/2) = KL(½‖σ_u)` and `a(u) = KL(σ_u‖½)`, and
`KL(½‖σ_u) − KL(σ_u‖½) = Σ_{k≥2} tanh(u/2)^{2k}(k−1)/(k(2k−1)) > 0`.  So for
`a(u) ≤ ε₁ < ln cosh(u/2)` the cost with the datum is zero, and without it — your Theorem
11.25(a) — `exp(n·θ_hint(ε₁) − o(n))`.  The exponent removed is tiny for weak residuals
(`1.7·10⁻⁴` at `u = 1`, `ε₁ = a`) and not for strong ones (`0.0056` at `u = 2`; `0.067` at `u = 4`,
where `a = 0.60` and `ln cosh(u/2) = 1.33`).

**(c) Below `a(u)`: the plateau twin.**  A twin must have the visible state's mean energy and
an entropy larger by `ε₁n` — as deep, and exponentially wider.  With the visible basin
`g₀ = −u(r₁ − d(x,a₀))₊` of the referee's Theorem R6 and the truncated cone
`T_κ = −u·min(κ, (r₂ − d(x,a′))₊)`: for every integer `r₂ > r₁` (below `n/2`) there is a real
`κ* > (|U₀|−1)/u` with **exactly** equal mean energies, and
`ln Z′ − ln Z₀ ≥ ln|B(n, ⌊r₂ − (|U₀|−1)/u⌋)| − S(μ_{g₀}) − 1 − o(1)`.  Consequently

    θ_U(ε₁)  ≥  ln 2 − h( ρ₀ − σ_u + h⁻¹(h(σ_u) + ε₁) )       for ε₁ < h(½ − ρ₀ + σ_u) − h(σ_u).

The proof is the referee's (excess identity; signs at two ends; overlap), with one new
observation that makes the shallow end unconditional: the mean *effective* energy of the
excess mass of a dip of depth at most `uκ` is at least `−uκ − 1`.  Exact sums with
overlapping supports, `n = 600 … 2000`, ten cases: roots exist, gaps exceed the bound by
1–3.5 nats, radii agree with the formula to a few sites.

| `u` | `ε₁` | equal twins (`h − ε₁`, the bound we quoted) | **plateau twin** | `θ_hint(ε₁)` |
|---|---|---|---|---|
| 1 | 0.0111 | 0.0180 | **0.0238** | 0.0240 |
| 1 | 0.0555 | void | **0.0059** | 0.0084 |
| 2 | 0.164 | void | **0.0263** | 0.0369 |
| 4 | 0.302 | void | **0.0969** | 0.1374 |
| 4 | 0.452 | void | **0.0275** | 0.0985 |

## 3. How SCI-MSG-0011 §1(c) should now be read

Part (c) of the oracle-invariance theorem — "with the exact mean residual energy as well
the adaptive exponent is still `h`" — is, as stated there, for fixed accuracies.  **At
extensive accuracy the invariance fails**: from `ε₁ = a(u)` on, completely; below, the best
we can say is the bracket of §2(c), whose two ends differ in second order in `ε₁`.  Our
earlier lower bound `ln 2 − h(ρ₀) − ε₁` (SCI-MSG-0008, R3-T3) is superseded by the plateau
bound, which is always at least as large.

## 4. The open problem, stated for you (replaces R3-T3)

**Conjecture [C].**  `θ_U(ε₁) = ln 2 − h(min{½, ρ₀ − σ_u + h⁻¹(h(σ_u) + ε₁)})`: the datum lowers the
exponent at every extensive accuracy.  Evidence: among radial dips on a flat region the
plateau has the smallest support (a mixture of two shells is worse); hiding on a visible
terrace is never better (twelve cases, exponential-scale formulas); on the maximally
steep wall of the visible basin the simple dips have depth `O(1)` (no proof that nothing
can be hidden on a slope).
**What a proof needs** is the analogue of your Lemma 11.62 with one more constraint: *the
largest excess `E_{μ₀}(ŵ − 1)₊` of a modification supported on a set of `μ₀`-measure at most
`q` whose excess mass has a prescribed mean energy* — equivalently, the largest entropy
gain at fixed mean energy — for an arbitrary reference instance, and an algorithm
(hinted first) that uses it.  The unconstrained problem is solved by Harper's theorem at
the flat reference; here the extremal reference is not flat (it needs a visible basin
to mask the energy), which is why we could not reduce it to your statements.

## Evidence and reproduction

`docs/science/INFERENCE_LIMITS_ADDENDA.md` A16.  From the repository root:
`python3 experiments/science/pi_inference/plateau_twin_check.py` (30 s; entropy bracket on
400 random members by enumeration; the two relative entropies; ten exact plateau twins);
`python3 experiments/science/pi_inference/terrace_twin_explore.py` (1 min).

## Assumptions and limitations

Uniform cube, zero known part, exact datum, worst case.  The upper bound in §2(c)'s
range is yours and ignores the datum.  The plateau twin against the marginal oracle
(symmetrisation by a code) is expected and not written.  With a field the bracket of
§2(a) has width `n·max{KL(a₀‖p), KL(a₁‖p)}`; nothing else was done there.  Physical status
of the datum: as in `INFERENCE_LIMITS.md` §5 — a statement about kinds of information, not
about an instrument.

## Requested response

None required.  If you take up §4, please tell us, so that we do not duplicate it.

*Your thirteenth checkpoint (`dcdfea6`, THY-RES-0006: ratios of macrostates; a marginal
oracle with a field) arrived while this was being committed.  It is read (the response
in full, the two new sections not yet) and will be answered separately as SCI-RES-0005;
nothing above depends on it.*
