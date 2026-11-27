### 4.5 Reading

**(i) Like for like — the form of the reference (T: equal shares on triples, band 7).**
Lys₁₂, order 5: 0.05669 (reference) → 0.0452 (stage 1) → **0.016** (stage 2), a
factor 3.5.  Lys₁₂, order 4: 1.413 → 0.3493 → **0.1115**, a
factor 13.  (LKSE)₃, order 5: 4.301 → 1.871 →
**0.1946**, a factor 22.  In the site and pair forms of stage 2:
0.1119 and 0.02058 (Lys₁₂, order 5; the reference has 0.4587 and 0.08487),
1.874 and 0.1853 (order 4; 10.56 and 3.096), 2.918 and
0.3009 ((LKSE)₃; the coordinator's log `occ_reduction_test_LKSEc12_H_m5_w7_SAb.log` has 22.58 and 10.83
for the reference; I did not re-run those two).  The three stopping
numbers of the brief — 0.0567, the order-4 number 1.4125, 4.30 — are beaten in the reference's
own form by factors 3.5, 13 and
22.

**(ii) The brief's first stage alone** (hosts resolved) is worth a factor 1.3 at
Lys₁₂ order 5 — the first-order regime, where the bracket follows the mean penalty and the
mean penalty moves by 23 % (§3.2) — and factors 4 at order 4 and
2.3 for (LKSE)₃, where the reference floor was delocalised (7.2 and
9.0 side chains off the anchor in its samples) and the stage-1 floor is not (1.3 for Lys₁₂).
**The dependence on the host's rotamer is weak, as §3.1 says; what stage 1 buys is the
threshold, not the slope.**

**(iii) With one sub-tuple per subset (form W)** the brackets are the penalty-free widths to
within a few per cent: Lys₁₂ order 5 **0.007233** `[517.125705, 517.132938]`
(reductions alone 0.007133); order 4 **0.007347** `[517.125649, 517.132996]`
(0.007132); (LKSE)₃ order 5 **0.01699** `[655.604050, 655.621038]`
(0.0167).  Against the three stopping numbers: factors 7.8,
192, 253.  The allocation alone — W with P8's
constants — gives 0.007286 at Lys₁₂ order 5 (constants small: enough), 0.7207 at
order 4 (floor delocalised: not enough) and 1.311 for (LKSE)₃; with the joint maxima
of stage 2 as *constants* 0.01024 at order 4 and 0.03933 for (LKSE)₃.
**Lys₁₂ is certified at order 4 — from 96 366 evaluations — 7.7 times
more tightly than the reference at order 5 with 1 621 056**; for comparison, the coordinator's
nested sampler on the order-4 reference sandwich reaches 0.0060 nats at probability 0.95 with
12 000 further evaluations (`[517.125561, 517.131531]`: its two-end form with empirical Bernstein;
0.032 as the theory division states the bound; addendum A17 (18) item 62) — the
deterministic bracket is 0.007347 with none, and the two intervals overlap.  **(LKSE)₃, the sequence that was "reachable by sampling and not
deterministically", is certified deterministically within 0.01699 nats**; the
coordinator's sampled interval (`[655.592089, 655.632643]`, 0.041 nats at probability 0.95, two-end
form with empirical Bernstein) contains my bracket.

**(iv) Where the predictions were wrong** (§4.1).  Wherever the floor stays at the anchor,
"penalty-free width + `2β⟨pen⟩` on the Gibbs sample" predicted the certified bracket within a
few per cent (every line of Lys₁₂ at order 5 within 3 %, of Ser₁₂ within 8 %; the stage-2 lines of
Lys₁₂ at order 4 and of (LKSE)₃ within a factor 1.6 — the equal-share forms 22–38 % below my guess, the window form within 2 % of it).  The two errors that matter are about
the floor: (a) I assumed that a delocalised reference floor stays delocalised under stage-1
tables (predicted 0.75 and 3.3 nats; found 0.3493 and 1.871); (b) I assumed that the
window form with P8's constants would be "first order plus a little" (Lys₁₂ order 4: predicted
0.02, found 0.7207, its floor at 6.6 side chains off the anchor; (LKSE)₃: predicted 0.15,
found 1.311, floor at 9.4).  In both cases the
number on the Gibbs sample was right about the sample and silent about the floor, as Lemma
A17.16 says it must be; I have no rule that says on which side of the threshold a set of
tables lies before the model is built (request P9-T2).

**(v) What the brackets now consist of.**  At the window form of stage 2 the penalties
contribute 0.007233 − 0.007133 and 0.007347 − 0.007132 nats for Lys₁₂ and
0.01699 − 0.0167 for (LKSE)₃: one to three per cent of the bracket.  The rest is
the reductions — the ten pairs of side chains beyond the band and the evaluated terms that
do not fit a window — which this workstream did not touch.
