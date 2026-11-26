*Reading.*  None of these orders had a certificate: P8's constants are `βΓ₄ = 296` for
(LKSE)₃ and `βΓ₃ = 375`, `1 660` for the two peptides (P8's code path, run here; P8 stored
constants from order 4 on), and with them the equal-share triple form has first-order
numbers of 2.7–52 nats and exponential estimates of 16–360 nats on the Gibbs sample
(`logs/gain_LKSEc12_H_0.60_m4_w7.log`, `gain_K12_H_0.70_m3_w7.log`, `gain_LKSEc12_H_0.60_m3_w7.log`; not
run as models).

**(LKSE)₃ at order 4 — 181 268 evaluations instead of 3 471 783 — is certified within
{LKSE_4_s2_W} nats**, `[{LKSE_4_s2_W_lo}, {LKSE_4_s2_W_hi}]` (reductions alone {LKSE_4_zero}; floor at
{LKSE_4_s2_W_floor} side chains off the anchor, the ensemble's own value).  The order-5 bracket lies
inside it, and both inside the coordinator's sampled interval.  **Here the second stage is
not an improvement but the difference between a certificate and none**: the same window form
gives {LKSE_4_s1_W} nats with stage-1 tables and {LKSE_4_cJ2_W} with the joint maxima of stage 2 as
constants — both floors delocalise — and the equal-share triple form of stage 2 gives
{LKSE_4_s2_T}.

**Lys₁₂ at order 3 — 3 841 evaluations — is certified within {K12_3_s2_W} nats**,
`[{K12_3_s2_W_lo}, {K12_3_s2_W_hi}]` (reductions alone {K12_3_zero}; floor at {K12_3_s2_W_floor} side chains
off the anchor); the triple form of stage 2 gives {K12_3_s2_T}, the window form {K12_3_s1_W} with
stage-1 tables and {K12_3_cJ2_W} with constants.  For comparison (the coordinator's numbers):
the reference certificate of this peptide is 1.41 nats at order 4 (96 366 evaluations) and
0.0567 at order 5 (1 621 056).  Workstream P8's first-order *estimates* for this order with **exact** state-independent
constants were 0.54 nats in the banded triple form and 0.024 with all triples charged in a
window (its §4.1, row "exact3", band 6, reductions not included); the resolved **bounds** are
certified at {K12_3_s2_T} and {K12_3_s2_W} in the corresponding forms — within a factor 1.5–3.5 of what
exact constants were estimated to give.

**(LKSE)₃ at order 3 — 6 083 evaluations —** {LKSE3_SENTENCE}

*Against the predictions* (3 and 4 of §4.1).  The two window-form brackets I hoped for came
out as predicted or better ((LKSE)₃ order 4: 0.02 predicted, {LKSE_4_s2_W} found; Lys₁₂ order 3:
0.12 predicted with an even chance of failure, {K12_3_s2_W} found); the equal-share triple form
at order 3 of Lys₁₂, which I had written off ("more than 2"), gives {K12_3_s2_T}.  Of the nine
predictions of this workstream that were about a floor I was too pessimistic three times
(T with stage-1 tables at Lys₁₂ order 4 and (LKSE)₃ order 5; T with stage-2 tables at Lys₁₂
order 3), too optimistic twice (the window form with P8's constants, twice), and right four
times, two of them with a stated risk of 40–50 % — I cannot predict it.
