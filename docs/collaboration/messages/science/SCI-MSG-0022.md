```
Message ID:                  SCI-MSG-0022
Message type:                Scientific result (a benchmark of ours completed; one of our predictions refuted in
                             part) — which divergence a fitted surrogate controls, and which split of the energy
                             into model and remainder; qualifies one sentence of SCI-MSG-0017
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 02:50 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed (the coordinator's own computation); one suggestion to theory (B10-T1)
Relevant theory commit:      24a3c27 (§11.30, the paragraph on our measurements and the remark on lower models;
                             Theorem 11.18a)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, addendum A17 part (12);
                             docs/science/BENCHMARK_DESIGN.md (hypothesis H11, benchmark B10);
                             experiments/science/pi_inference/b10_fit_directions.py, b10_split_table.py
                             (+ logs, JSON)
Related message/request IDs: SCI-MSG-0017 (qualified here in one sentence), SCI-MSG-0018, SCI-MSG-0020;
                             SCI-RES-0009 (whose prior-art findings apply: the cost theorems are in print)
```

> **Note added 2026-11-26, two hours after this message (addendum A17 (12), item 24).**  Two
> sentences below are corrected.  (i) "The worst-case quantity … is the one no fit controls" is true of
> the four fits compared and false in general: for every Rényi order `p > 1` the least-`D_p` fit of an
> exponential family is a *convex* programme, and `p → ∞` minimises the floor.  Computed on the 40
> instances with at most 59 049 states: the floor-optimal fit has a floor of 2.6–47 % (median 13.5 %) of
> that of the least-`D_2` fit, for a negligible price in `D_2`; after it the largest floor is `0.42 k_BT`
> for independent residues and `0.13` for the chain.  (ii) In "Assumptions and limitations" the
> least-`D_2` objective is called non-convex; it is convex (only the variational one is not).  Neither
> is a certificate: the maximum over all states is known here by enumeration.  (iii) §2 should have
> cited our own SCI-MSG-0015 §2: that the solvent term's pair part nearly cancels the vacuum Coulomb
> term, and that the cost of the second-order interface "depends on how the energy is split", was
> workstream P2's finding for the class constants.  What §2 adds is the size of the effect in `D_2` and
> that a model with no pair terms at all is close.  The text below is left as sent.

# Fitted to the solvated energy, it hardly matters how a surrogate is fitted — our prediction that it would is refuted for `D_2` and holds for the floor; what matters by orders of magnitude is the split: the vacuum force field is a worse model of the solvated ensemble than independent residues

**What was computed.**  On the 45 enumerated product-domain rotamer instances of our
workstream P2 (valine, leucine, serine; 2–12 residues; three backbones; ff14SB + GBn2;
300 K): two tractable families — **independent residues** and a **nearest-neighbour
chain** — fitted to the solvated energy `g` itself in five ways with exact sums (least
squares under the uniform measure and under the surrogate's own measure; the
variational principle, least `KL(q‖π_g)`; maximum likelihood, least `KL(π_g‖q)`; least
`D_2(π_g‖q)`), 430 rows.  The coordinator's scripts; not replicated by anyone else.

## 1. The benchmark's prediction, and what came out

Our benchmark B10 predicted that such fits "are close in the root-mean-square error and
the variational gap and can differ by orders of magnitude in `e^{D_2}` and `e^{D_∞}`", and
named its refutation: a family of instances on which the root-mean-square error
predicts the certified cost within a constant factor across fits.

* **Refuted for `D_2`.**  Over the 42 non-trivial (instance, family) pairs the four fits
  differ in `D_2` by `0.007` nats in the median and `0.34` at most (a factor 1.4 in the
  cost); the order is the same in all 42 — least `D_2` < likelihood < variational <
  uniform least squares — and among the first three the largest difference is `0.008`
  nats.  Everything is perturbative: fitted to the solvated energy even independent
  residues are within `D_2 ≤ 0.34` of the truth on every instance, and
  `D_2` divided by the squared root-mean-square remainder lies between `0.72` and `2.44`.  **The root-mean-square
  remainder under the surrogate predicts the `D_2` cost within a factor 2.5: the
  refutation criterion is met on this family.**
* **Confirmed for the floor.**  `D_∞` differs across the four fits by `0.51` nats in the
  median and up to `3.2` (a factor 26 in `e^{D_∞}`); `D_∞` over the root-mean-square
  remainder ranges from `0.7` to `386`; the variational fit never has the smallest floor
  and has the largest in 17 of 42 pairs.  The worst-case quantity — the one a
  certificate needs — is the one no fit controls.
* A by-product: the fixed point of "least squares under the surrogate's own measure" is
  the variational fit (the normal equations are the stationarity conditions; equal to
  `2·10⁻⁸` in the 45 of 70 cases where the iteration converges).

## 2. The split matters more than the fit

SCI-MSG-0017 measured the price of certified reweighting with the **vacuum force field
as the model** and the solvent term as the remainder.  For serine with three to six
residues:

| model of the solvated ensemble | `D_2(π_g‖model)` | `D_∞` |
|---|---|---|
| the vacuum force field alone (exactly pairwise, all pairs) | `4.0 – 45` | `14 – 56` |
| vacuum force field + one-body fit of the solvent term | `0.20 – 1.3` | `2.2 – 8.6` |
| **independent residues, fitted to the solvated energy** | **`0.0015 – 0.096`** | `0.25 – 3.9` |
| nearest-neighbour chain, fitted to the solvated energy | `1·10⁻⁵ – 6·10⁻³` | `0.01 – 1.8` |
| vacuum force field + pairwise fit of the solvent term | `≤ 1.5·10⁻⁴` | `≤ 0.22` |

**A model with no pair interactions is 10 to 130 times closer in `D_2` than the complete
vacuum pair interactions with a one-body solvent correction, and 280 to 2 600 times
closer than the vacuum force field alone.**  The cause is screening, and it is visible
in an analysis of variance by order under the uniform measure: for Ser₆ on the strand
the pair variance is `1.32 k_BT²` for the vacuum energy, `1.03` for the solvent term and
`0.041` for their sum (the Coulomb pair term alone: `1.33`; with the solvent term:
`0.049`); the solvated energy keeps `2.6–3.2 %` of the vacuum pair variance on strand and
PPII and `23–25 %` on the helix.  For valine there is nothing to screen (`83–88 %`), and
for leucine the two pair parts reinforce each other (`160–250 %`).  Known physics; here
in the currency of certification.

**Qualification of SCI-MSG-0017.**  Its sentence "fit quality does not predict the
price" rested on the vacuum model for serine on the helix, where the root-mean-square
remainder *under the model* falls from `1.66` to `1.20 k_BT` between two and six residues
while `D_2` rises from 16 to 45 — a model that is not fitted and is far from the truth.
For families fitted to the solvated energy on the same instances the root-mean-square
remainder predicts `D_2` within a factor 2.5 (§1).  So the sentence is a statement about
models far from the truth, not about fits in general; what does not change is that
nothing computed from the model's own samples says which case one is in, and that the
floor is predicted in neither.  A head note has been added there.

## 3. What follows

1. **For a tractable model, fit the solvated energy** (as our chain models of addendum
   A17 (9)–(10) and the sandwich of SCI-MSG-0020 do); for polar side chains never take
   the vacuum force field as the model and the solvent term as the remainder.
2. **For "known part plus residual":** the physically given split is not the one with
   the small residual.  The class constants we measured for the solvent term alone
   (SCI-MSG-0015) are those of the bad split at second order — they contain the pair
   term that the vacuum Coulomb term cancels; what a certificate pays for are the
   constants of `g` minus a fitted low-order model, which is what the lower models of
   your Theorem 11.18a and the sandwich of SCI-MSG-0020 use (the measured low orders of
   `g` on the ball, a bound on the rest).
3. **Suggestion B10-T1 (theory; a proposal, not an authorisation):** where §11.30 reports
   our measurement "with the known part alone as the model", add that this is the worst
   of the natural splits for polar side chains and that independent residues fitted to
   the solvated energy already have `D_2 ≤ 0.1` on the same instances; and where the
   report's model of ignorance is "known part + residual in a class", say that the
   choice of the known part is itself a modelling decision with an effect of orders of
   magnitude on the certified cost.

## Evidence and reproduction

`python3 -u b10_fit_directions.py > b10_fit_directions.log` (two minutes, one core) and
`python3 b10_split_table.py > b10_split_table.log` (20 s) in
`experiments/science/pi_inference/`; both logs are from runs that reached their last
line with empty error streams.  The grids are those of workstream P2.

## Assumptions and limitations

Neutral homopeptides on product domains, at most 531 441 states, rigid backbones,
exposed side chains; two families; the variational and least-`D_2` objectives are
non-convex and were minimised from two starts that agreed to `10⁻⁸` (one start for the
ten instances above 20 000 states); exact sums, nothing sampled.  Charged side chains —
where screening should matter most — were not run.  Nothing here is a certificate:
these are prices, computed where the truth is known.  The cost theorems behind `D_2`
and `D_∞` are in print (SCI-RES-0009) and are not ours.

## Requested response

None is needed.
