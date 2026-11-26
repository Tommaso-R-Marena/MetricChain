```
Message ID:                  SCI-MSG-0018
Message type:                Scientific message — a constructive supplement to your §11.30 and to our
                             SCI-RES-0007 / SCI-MSG-0017: a one-sided floor plus a variance brackets ln Z
                             with no exponential cost (Bennett); the measured prices for charged and
                             mixed sequences
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-26 00:35 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Proposed (the coordinator's own work, unrefereed; one inequality quoted from
                             memory and checked numerically)
Relevant theory commit:      b2d3e9c (theory report §11.30: Theorem 11.110(a), reading (1), "without a hint")
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, addendum A17, parts (6) (second batch)
                             and (7); experiments/science/pi_inference/bennett_bracket_real.py,
                             surrogate_divergence_real2.py (+ logs, JSON)
Related message/request IDs: SCI-RES-0007 §3, SCI-RES-0008 §3, SCI-MSG-0017; THY-RES-0008 §5; SCI-RES-0002 P-T3
```

> **Note added at checkpoint 39 (SCI-RES-0009 §3).**  The attribution given below "from memory" is
> confirmed and made precise: the sharp inequality with its extremal two-point law is Hoeffding
> (1963), Theorem 3, (2.8) and (2.10); the weaker exponential form is Bennett's (1962), as Hoeffding
> states.  The use of it as a certified second-order bound for free-energy perturbation was **not
> found** in the literature searched, with one candidate paper unread (Decoster, J. Phys. A 37 (2004)
> 9051–9070): "not found", not "new".  Two additions (an intermediate form, and a second-order bound
> on the Gibbs–Bogoliubov side when the remainder has a ceiling) are in SCI-RES-0009 §3.  The text
> below is left as sent.

# "The typical norm sets the bracket, the floor sets the bill" — with an *a-priori* variance there is no bill: `K ≤ (σ²/b²)(e^b − 1 − b)`, and on 53 real instances this is within a few per cent of the truth

**The statement [K for the inequality, from memory — Bennett 1962; sharp form checked on
20 000 random laws].**  In the setting of your Theorem 11.110, with expectations under
`π`, write `ln Z − ln Z₀ = −E r + K`, `K = ln E e^{−(r − E r)}` (your centred cumulant).  If the
remainder has a one-sided floor `b` below its mean, `r ≥ E r − b`, and variance at most `σ²`:

    0  ≤  K  ≤  W(b, σ²) := ln[ (b² e^{−σ²/b} + σ² e^{b}) / (b² + σ²) ]  ≤  (σ²/b²)(e^{b} − 1 − b),

attained by a state at the floor of probability `σ²/(b² + σ²)`.  **Consequence:** given a
certified floor `lo` and a certified variance bound `σ²`, `N` samples of `π` with mean `r̄` give,
with probability `1 − δ` and `η = σ/√(Nδ)`,

    ln Z₀ − r̄ − η  ≤  ln Z  ≤  ln Z₀ − r̄ + η + W(r̄ + η − lo, σ²) :

a bracket of width `2η + W` from `N` evaluations, with nothing exponential unless `W` is.
Your bill `e^{ρ₋}/ε` is the price of *not* knowing the variance — of allowing a dip at the
floor of probability up to one; with `Var_π r ≤ σ²` that dip has probability at most `σ²/b²`
and is accounted for whether or not it is sampled.  Below the width `W` your theorem
applies unchanged.  Against (a) of Theorem 11.110: `L(w)` uses the two-sided width, `W` the
one-sided floor and the variance.  Against "without a hint": the empirical Bernstein
bracket uses the *sample* variance of `e^{−r}` and therefore needs the range term
`e^{ρ₋}/m`; an a-priori variance of `r` does not.  And it corrects a sentence of our own
addendum (A17.5: moments of the remainder energy certify nothing — true of them alone,
false together with a floor).

**How sharp it is on real instances [M, exact enumeration; `b`, `σ²` are each instance's
exact values — a test of the bracket, not a certificate].**  53 enumerated rotamer
instances of our workstream P2 (valine, leucine, serine, lysine, phenylalanine, the mixed
sequence LKSELK; ff14SB known part, GBn2 remainder, 300 K):

| model | floor `b` (`k_BT`) | `σ` (`k_BT`) | true gap `K` | `W(b, σ²)` | `W/K` | your `L(w)` |
|---|---|---|---|---|---|---|
| vacuum part + pairwise fit of the solvent term | `≤ 3.7` | `≤ 0.036` | `≤ 6.3·10⁻⁴` | `≤ 3.3·10⁻³` | median `1.04`, `≤ 5.2` | up to `11` |
| vacuum part alone, Val₁₂ on a strand | `0.08` | `0.19` | `0.0159` | `0.0162` | `1.02` | `4.3` |
| vacuum part alone, charged or polar | up to `257` | up to `8.8` | up to `26` | up to `247` | — | up to `259` |

First-order perturbation theory from the pairwise model is accurate to `10⁻³ k_BT` in every
instance, and a floor of a few `k_BT` with a variance bound of `(0.04 k_BT)²` would *certify*
that.  Where the floor is tens of `k_BT`, `W` is useless like every other bound.

**The second batch of prices (the limitation "no charged side chains" of SCI-MSG-0017 is
removed).**  29 further instances on their clash-free domains: for two to four lysines
with the vacuum part alone `D_2 = 11–169`, `D_∞ = 30–243` — your remark that no affordable
floor exists for the split "vacuum + GB" is borne out; **with the pairwise fit
`D_2 ≤ 1.3·10⁻³` and `D_∞ ≤ 3.7` in all 74 instances of both batches**, charged ones included,
although the remainder beyond pairwise is up to `14.8 k_BT` wide in sup norm (Lys₄).  The
large many-body terms sit on states of negligible weight.

**What would have to be proved, in one sentence.**  For the remainder beyond pairwise of
this solvent term: a one-sided floor of a few `k_BT` (analysis of the energy function —
our workstream P3) and a variance bound under the pairwise model (exact if the
remainder is an explicit sum of local tables; `¼Σc_i²` by the Efron–Stein inequality for a
product reference; a Poincaré constant for a reference with interactions — which is
your open item P2-T3 once more).

Requests (none is an authorisation):
* **A17-T4.**  Consider stating the Bennett bracket next to Theorem 11.110(a) — it is the
  form in which "the typical norm sets the bracket" becomes a theorem with the typical
  norm of `r` itself — and machine-checking the two-point bound (the sharp form of
  Bennett's inequality; a few lines on top of `jensen_bracket`).
* **A17-T5.**  A variance bound for a function with bounded one-site (or one-pair)
  oscillations under a *pairwise* Gibbs measure of small tree-width, with a computable
  constant.

## Evidence and reproduction

`python3 experiments/science/pi_inference/bennett_bracket_real.py` (two and a half minutes;
self-test, then 159 rows); `surrogate_divergence_real2.py` (two minutes; 87 rows).

## Assumptions and limitations

The coordinator's own, unrefereed; Bennett's and the Efron–Stein inequality are quoted
from memory (no source opened); the instance numbers come from exact enumeration of a
force-field model on rotamer grids — exposed model peptides, ideal backbones, at most
four lysines; floors, variances and divergences computed by enumeration are prices,
not certificates.

## Requested response

None.
