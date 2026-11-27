### 4.5 Reading

**(i) Like for like — the form of the reference (T: equal shares on triples, band 7).**
Lys₁₂, order 5: {K12_5_ref_T} (reference) → {K12_5_s1_T} (stage 1) → **{K12_5_s2_T}** (stage 2), a
factor {R__K12_5_ref_T__K12_5_s2_T}.  Lys₁₂, order 4: {K12_4_ref_T} → {K12_4_s1_T} → **{K12_4_s2_T}**, a
factor {R__K12_4_ref_T__K12_4_s2_T}.  (LKSE)₃, order 5: {LKSE_5_ref_T} → {LKSE_5_s1_T} →
**{LKSE_5_s2_T}**, a factor {R__LKSE_5_ref_T__LKSE_5_s2_T}.  In the site and pair forms of stage 2:
{K12_5_s2_S} and {K12_5_s2_B} (Lys₁₂, order 5; the reference has {K12_5_ref_S} and {K12_5_ref_B}),
{K12_4_s2_S} and {K12_4_s2_B} (order 4; {K12_4_ref_S} and {K12_4_ref_B}), {LKSE_5_s2_S} and
{LKSE_5_s2_B} ((LKSE)₃; the coordinator's log `occ_reduction_test_LKSEc12_H_m5_w7_SAb.log` has 22.58 and 10.83
for the reference; I did not re-run those two).  The three stopping
numbers of the brief — 0.0567, the order-4 number 1.4125, 4.30 — are beaten in the reference's
own form by factors {R__K12_5_ref_T__K12_5_s2_T}, {R__K12_4_ref_T__K12_4_s2_T} and
{R__LKSE_5_ref_T__LKSE_5_s2_T}.

**(ii) The brief's first stage alone** (hosts resolved) is worth a factor {R__K12_5_ref_T__K12_5_s1_T} at
Lys₁₂ order 5 — the first-order regime, where the bracket follows the mean penalty and the
mean penalty moves by 23 % (§3.2) — and factors {R__K12_4_ref_T__K12_4_s1_T} at order 4 and
{R__LKSE_5_ref_T__LKSE_5_s1_T} for (LKSE)₃, where the reference floor was delocalised ({K12_4_ref_T_floor} and
{LKSE_5_ref_T_floor} side chains off the anchor in its samples) and the stage-1 floor is not ({K12_4_s1_T_floor} for Lys₁₂).
**The dependence on the host's rotamer is weak, as §3.1 says; what stage 1 buys is the
threshold, not the slope.**

**(iii) With one sub-tuple per subset (form W)** the brackets are the penalty-free widths to
within a few per cent: Lys₁₂ order 5 **{K12_5_s2_W}** `[{K12_5_s2_W_lo}, {K12_5_s2_W_hi}]`
(reductions alone {K12_5_zero}); order 4 **{K12_4_s2_W}** `[{K12_4_s2_W_lo}, {K12_4_s2_W_hi}]`
({K12_4_zero}); (LKSE)₃ order 5 **{LKSE_5_s2_W}** `[{LKSE_5_s2_W_lo}, {LKSE_5_s2_W_hi}]`
({LKSE_5_zero}).  Against the three stopping numbers: factors {R__K12_5_ref_T__K12_5_s2_W},
{R__K12_4_ref_T__K12_4_s2_W}, {R__LKSE_5_ref_T__LKSE_5_s2_W}.  The allocation alone — W with P8's
constants — gives {K12_5_sab_W} at Lys₁₂ order 5 (constants small: enough), {K12_4_sab_W} at
order 4 (floor delocalised: not enough) and {LKSE_5_sab_W} for (LKSE)₃; with the joint maxima
of stage 2 as *constants* {K12_4_cJ2_W} at order 4 and {LKSE_5_cJ2_W} for (LKSE)₃.
**Lys₁₂ is certified at order 4 — from 96 366 evaluations — {R__K12_5_ref_T__K12_4_s2_W} times
more tightly than the reference at order 5 with 1 621 056**; for comparison, the coordinator's
nested sampler on the order-4 reference sandwich reaches 0.0060 nats at probability 0.95 with
12 000 further evaluations (`[517.125561, 517.131531]`: its two-end form with empirical Bernstein;
0.032 as the theory division states the bound; addendum A17 (18) item 62) — the
deterministic bracket is {K12_4_s2_W} with none, and the two intervals overlap.  **(LKSE)₃, the sequence that was "reachable by sampling and not
deterministically", is certified deterministically within {LKSE_5_s2_W} nats**; the
coordinator's sampled interval (`[655.592089, 655.632643]`, 0.041 nats at probability 0.95, two-end
form with empirical Bernstein) contains my bracket.

**(iv) Where the predictions were wrong** (§4.1).  Wherever the floor stays at the anchor,
"penalty-free width + `2β⟨pen⟩` on the Gibbs sample" predicted the certified bracket within a
few per cent (every line of Lys₁₂ at order 5 within 3 %, of Ser₁₂ within 8 %; the stage-2 lines of
Lys₁₂ at order 4 and of (LKSE)₃ within a factor 1.6 — the equal-share forms 22–38 % below my guess, the window form within 2 % of it).  The two errors that matter are about
the floor: (a) I assumed that a delocalised reference floor stays delocalised under stage-1
tables (predicted 0.75 and 3.3 nats; found {K12_4_s1_T} and {LKSE_5_s1_T}); (b) I assumed that the
window form with P8's constants would be "first order plus a little" (Lys₁₂ order 4: predicted
0.02, found {K12_4_sab_W}, its floor at {K12_4_sab_W_floor} side chains off the anchor; (LKSE)₃: predicted 0.15,
found {LKSE_5_sab_W}, floor at {LKSE_5_sab_W_floor}).  In both cases the
number on the Gibbs sample was right about the sample and silent about the floor, as Lemma
A17.16 says it must be; I have no rule that says on which side of the threshold a set of
tables lies before the model is built (request P9-T2).

**(v) What the brackets now consist of.**  At the window form of stage 2 the penalties
contribute {K12_5_s2_W} − {K12_5_zero} and {K12_4_s2_W} − {K12_4_zero} nats for Lys₁₂ and
{LKSE_5_s2_W} − {LKSE_5_zero} for (LKSE)₃: one to three per cent of the bracket.  The rest is
the reductions — the ten pairs of side chains beyond the band and the evaluated terms that
do not fit a window — which this workstream did not touch.
