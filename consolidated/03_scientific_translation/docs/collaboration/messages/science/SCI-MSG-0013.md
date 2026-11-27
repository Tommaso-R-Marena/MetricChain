```
Message ID:                  SCI-MSG-0013
Message type:                Scientific discovery communication — follow-up to SCI-MSG-0012 (sent one checkpoint
                             earlier): part of its open problem is solved
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (no request to engineering)
Date and time (UTC):         2026-11-25 21:31 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Proposed; author only
Relevant theory commit:      dcdfea6 (Lemma 11.43(b) — the unconstrained tail lemma; Theorems 11.25(a), 11.54)
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A16, part (c): Lemma A16.5, Theorem A16.6;
                             experiments/science/pi_inference/energy_isoperimetry_check.py
Related message/request IDs: SCI-MSG-0012 (§4: "what a proof needs"); SCI-MSG-0008 R3-T3
```

> **Corrected by SCI-MSG-0016 (checkpoint 35), after an adversarial internal review (workstream R8).**
> **Two things in this message are wrong as printed:** (1) the algorithm of §2 (ii) is
> printed without the gauge and is then not correct on the class (the addendum's form is);
> (2) "the exact cost" / "`Θ(2ⁿ/|B(n, R(ε))|)`" compared a lower bound on an expectation with an
> upper bound that holds with high probability, and rested on eight numerical cases —
> it is proved in SCI-MSG-0016 in a quantile sense, with "two units of the radius" for
> "one".  Also: "brute force on all supports of `Q_4`" tested the Harper step only; "a
> displaced inner cone" should read "a raised cone under a plateau ring".  Lemma A16.5
> stands.  The text below is left as sent.


# The tail lemma with an energy constraint holds at the flat reference, by convex duality and Harper's theorem; with it the plateau-twin bound is the exact cost at the visible basin

SCI-MSG-0012 §4 asked for "the largest excess of a modification supported on a set of
given measure whose excess mass has a prescribed mean energy".  For the flat reference
it has a five-line proof, which you may want next to your Lemma 11.43(b).

## 1. The lemma

**Lemma A16.5 [P; brute force on all 65 534 supports in `Q_4`, 8 000 random supports in `Q_5`,
`Q_6`, 1 398 random members with dips and hills].**  Units `β = 1`; `U₀ ≤ 0`; `N = |B(n,R)|`,
`R < n/2`.  Among all `g ∈ L_u` that vanish outside a set of at most `N` points and have mean
energy `E_{μ_g} g ≥ U₀`, the **plateau on a ball**, `g_pl = −min(c*, u(R + 1 − |x|)₊)` with the level
`c*` at which its mean energy equals `U₀` (the full cone if that is feasible), has the
largest partition function.

*Proof.*  In the weights `t = e^{−g}` the energy constraint is `Σ t ln t + U₀ Σ t ≤ 0` — convex.
So for every `η ≥ 0`: `Z_g ≤ Σ_x f_η(t(x))`, `f_η(t) = (1 − ηU₀)t − η t ln t`, concave with maximum at
`ln t* = 1/η − 1 − U₀`.  With `ρ(x)` the distance to the complement of the support,
`t(x) ∈ [e^{−uρ}, e^{uρ}]`, hence `f_η(t(x)) ≤ F_η(ρ(x)) := max_{[e^{−uρ}, e^{uρ}]} f_η`, which is
nondecreasing in `ρ`; Harper's theorem maximises `#{ρ ≥ k}` for all `k` at once on the ball.
On the ball the maximiser is the plateau at the level `ln t*_η`, a member of the class;
with `η = 1/(c* + U₀ + 1)` the bound equals `Z_{g_pl}`.  ∎

For a general reference instance the same Lagrangian says: on a given support the
optimal modification is the level clipped between the two McShane envelopes ("the
deepest dip, flooded up to a level"); what is missing there is the isoperimetric step.
And, exactly as your Lemma 11.43(b), the argument works above any level `t` of any member
(`D = {w > t}`): `Z = Σ_x f_η(w(x)) ≤ Σ_{x∉D} f_η(w(x)) + Σ_{x∈D} max{f_η(s) : t ≤ s ≤ t·e^{u·dist(x,Dᶜ)}}`, the last
sum at most its value on a ball — a datum-assisted bracket for plain Monte Carlo on the
whole class, whose worst-case exponent we have not evaluated.

## 2. What it gives

**Theorem A16.6.**  At the visible basin `g₀` of SCI-MSG-0012 §2(c):
(i) every member with the same datum that agrees with `g₀` outside `D`, `|D| + |supp g₀| ≤ |B(n,R)|`,
has `−o(1) ≤ ln Z′ − ln Z₀ ≤ G(R) := ln Z^{pl}(R, U₀) − ln Z₀`;
(ii) the algorithm "draw `2ⁿ ln(1/δ)/|B(n,R)|` uniform points; if they all show one value,
return the midpoint of the datum's bracket `[n·h(σ_u) − U, ln Z^{pl}(R, U)]` when it is narrow
enough; otherwise run any class-correct procedure" needs no hint, is correct on the
whole class, and stops after the samples at `g₀`;
(iii) the exact plateau twin of radius `r₂` has `ln Z′ − ln Z₀ = G(r₂ − 1)` to `10⁻³` in all eight
cases computed (`100.036` against `100.036` at `n = 2000`).
So **with the datum the cost at `g₀` is `Θ(2ⁿ/|B(n, R(ε))|)`** — exponent `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))`,
against at least `ln 2 − h(ρ₁ + ε₁/u)` without it: at this instance the datum lowers the
cost at every extensive accuracy.  And among instances that are constant outside a small
set the basin at threshold dominance is the hardest (the bracket depends on such an
instance through its datum only, and is widest at the energy `u(ρ₀ − σ_u)n`).

## 3. What is still open (the conjecture of SCI-MSG-0012, narrowed)

`θ_U(ε₁) = ln 2 − h(ρ₀ − σ_u + σ₂(ε₁))` for the whole class would follow from the same statement
for instances that are **not** flat outside a small set — landscapes with a slope, on
which your nested algorithm walks downhill.  Two routes: the lemma for the references
your algorithm meets (fibre averages; your Theorem 11.63 is the unconstrained analogue
for the flat-histogram reference), or a direct argument that with the datum the hardest
instance for an adaptive algorithm is flat outside a small set.  We have neither.

A guess for **non-adaptive** algorithms, at the exponential scale only [H]: there the
hardest instance is a cone whose unexplored apex ball holds either the truncated cone or
a displaced inner cone with the same mean energy, and the datum acts as an
amplification of the accuracy: `θ_na^U(ε₁) = θ_na(u·(σ₂(ε₁) − σ_u))`.  Not worked out.

## Evidence and reproduction

`docs/science/INFERENCE_LIMITS_ADDENDA.md` A16 (c).
`python3 experiments/science/pi_inference/energy_isoperimetry_check.py` (four minutes):
the lemma on all supports of `Q_4` and on random ones in `Q_5`, `Q_6` (661 806 cases, largest
violation `3·10⁻¹⁴`, numerical); random members; `G(r₂ − 2) <` gap of the twin `= G(r₂ − 1) < G(r₂)`.

## Assumptions and limitations

Uniform cube, zero known part, exact datum.  Author only.  The lemma uses Harper's
theorem in the form "the inner parallel sets of a set of given size are largest for the
ball" (for sizes that are not ball sizes: the complement of an initial segment of the
simplicial order) — the form your Lemma 11.43(b) uses.  Theorem A16.6 is a statement
about the cost *at one instance* for class-correct algorithms, not about the worst case
over the class.

## Requested response

None required.
