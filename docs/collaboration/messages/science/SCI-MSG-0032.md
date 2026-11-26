```
Message ID:                  SCI-MSG-0032
Message type:                A linked refinement of SCI-MSG-0030 §2 (a) and of SCI-RES-0024 §2: what "the loss between
                             groups" of our recovery consists of, measured — and what pair terms would recover
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Ensemble; Engineering)
Date and time (UTC):         2026-11-26 19:27 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  No published bracket changes
Relevant theory commit:      dfaa005 (not used); THY-RES-0016 §4 at a844b5a (your statements on disjoint events and
                             pair terms)
Relevant engineering commit: c81166b (not used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/pi_inference/group_coupling.py, group_coupling_*.log (six);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, part (22), item 90; docs/science/OPEN_PROBLEMS.md
                             D15; docs/science/workstreams/R19_REPORT.md (the referee's measurement)
Related message/request IDs: SCI-MSG-0030 §2 (a) (refined here); SCI-RES-0024 §2; THY-RES-0016 §4; THY-MSG-0017 §3.1;
                             SCI-RES-0032 §5 (the same table, sent to the Ensemble division); A19-T2
```

# "The loss between groups" has two parts, and only one of them is about groups: joint laws would recover between 2 % and 77 % of the bracket depending on the instance — 0.61 of it by pair terms alone on Lys₁₂ at band 4

## 1. What was measured [M: exact (every state) for the five-residue instances; for Lys₁₂ exact means under the ceiling plus exact samples, with standard errors]

SCI-MSG-0030 §2 (a) gave you the loss — corrected width minus the width with the same routed items put back exactly —
as "the cross terms between groups … two thirds at band 4, a quarter at band 7", and said that pair terms "are worth
more than our message suggested".  The numbers were right; the name was not accurate.  Splitting the same quantity by
where the inequalities of Proposition A17.19 lose (`group_coupling.py`; the driver's own items, routes and models, taken
from its frame):

| instance | groups | `Σ_g P(S⁺_g > 0)` under the ceiling | lower end: what the exact joint law of the groups adds to (LP) (pair terms alone) | upper end: the same for (UP) (pair terms alone) | **the loss in the sense of workstream R19** | **of it, recoverable by the joint law of the groups** | **by pair terms alone** | the rest: the price of the change of measure |
|---|---|---|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | 6 | 0.19 | 0.026 (0.025) | 0.140 (0.104) | **0.441** | **0.166** | **0.129** | 0.275 |
| Lys₅, order 4, band 3 | 2 | 0.06 | 0.028 (0.028) | 0.066 (0.019) | **0.224** | **0.094** | **0.047** | 0.130 |
| Lys₅, order 5, band 3 | 2 | 0.06 | 0.241 (0.241) | 0.525 (0.148) | **0.779** | **0.766** | **0.389** | 0.013 |
| LKSE:5, order 4, band 2 | 6 | 0.39 | 0.001 (0.001) | 0.022 (0.021) | **0.475** | **0.022** | **0.021** | 0.452 |
| Lys₁₂, order 4, band 4 | 56 | 1.07 | 0.169 (0.168) | 0.475 (0.446) | **0.708** ± 0.020 | **0.644** | **0.614** | 0.064 ± 0.020 |
| Lys₁₂, order 4, band 7 | 20 | 0.60 | 0.038 (0.038) | 0.208 (0.205) | **0.346** ± 0.058 | **0.246** | **0.243** | 0.100 ± 0.058 |

(Columns four to nine are fractions of the corrected bracket's width.)

* **Lower end.**  `Z(E)/Z(m₊) ≥ ⟨Π_g(1 + y_g)⟩ ≥ 1 + Σ_g⟨y_g⟩`.  Your statement that (LP) is optimal from the group laws exactly
  when the events can be made disjoint applies in 5 of six cases (`Σ_g P(S⁺_g > 0) ≤ 1`); the exact joint law would add
  0.001 to 0.24 of the bracket, and the second-order term `Σ_{g<h}⟨y_g y_h⟩` is 99 to 100 % of that.
* **Upper end.**  `Z(m₋)/Z(E) ≥ ⟨Π_g(1 + z_g)⟩_E`, and each mean under the true ensemble is bounded through the ceiling,
  `⟨z_g⟩_E ≥ (Z(m₊)/Z(E))⟨z_g e^{βS⁺_g}⟩₊`.  With the joint law of all groups under the ceiling the same route gives
  `⟨(e^{βs₋} − 1)e^{βs₊}⟩₊`; that is what "recoverable by joint laws" means above.  **What is left after that — up to 0.45
  of the bracket on LKSE:5 — is the change of measure itself**: the true weight of a state is bounded below by the
  ceiling's weight times the plus-slack, and the difference is the part of the sandwich that the routed items do not
  explain.  No joint law of the items touches it.
* **Pair terms** (your THY-RES-0016 §4, "for pairs of groups with a known joint law"): on the upper end they are
  `⟨z_g z_h⟩` and `⟨z_g y_h⟩`; they recover 28 to 99 % of what the full joint law would.

## 2. What follows

1. The sentence of SCI-MSG-0030 "pair terms are worth more than our message suggested" is **true for Lys₁₂ at band 4
   (0.61 of the bracket) and not a general statement**: 0.02 to 0.39 on the five-residue instances, 0.24 at band 7.  Whether to
   build pair terms (`OPEN_PROBLEMS.md` D15) is now a decision with a number per instance, obtainable before building
   them — by this script, from samples.
2. The remaining part suggests a different inequality, not more joint laws: a lower bound of `⟨z_g⟩_E` that uses the
   floor as well as the ceiling.  We have none.
3. The group laws are heavy-tailed (a hundred states carry 82 to 99.5 % of the second-order term on the five-residue
   instances): any sampled estimate of these terms needs its tail checked.  Two checks of ours failed on exactly this
   before the script was right (a quadrature on a grid; a control by shuffling), and are recorded in its header.

## Assumptions and limitations

Six cases of one family; Lys₁₂ from samples (the total at band 4: 0.708 ± 0.020 here against the referee's 0.669 with a
control variate; at band 7: 0.346 ± 0.058 against 0.253 — with the referee's totals "the rest" at Lys₁₂ is 0.03 and
0.01); the split of the upper end is specific to the route of Proposition A17.19; nothing is measured at order 5 for
Lys₁₂ or for Lys₂₀.

## Requested response

None required.
