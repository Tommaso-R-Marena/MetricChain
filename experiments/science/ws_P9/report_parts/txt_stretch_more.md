*Against what I had written before the run* (`NOTES.md`, 11:26): width about `1.7·10⁻⁴` "as stated"
— found {NS_LKSE_5_thy_H_w}; "fewer than ten evaluations" — found {NS_LKSE_5_N}.  That guess was wrong twice
over: my own rule `ρ ≈ (envelope bracket)/D` with my own input (`10⁻⁶/0.017`) gives 24 of 400 000,
not "fewer than ten" (a slip of arithmetic); and the envelope's bracket under the proposals is
{NS_LKSE_5_env}, two to three times its first-order numbers on the two Gibbs samples of the true
ensemble (`1.2·10⁻⁶` and `1.6·10⁻⁶`, §3.2) — the rule itself holds (mean `ρ = {NS_LKSE_5_rho}` is
{NS_LKSE_5_env}`/D`).  How much of that factor is the inner sandwich's own allowances and how much
the different distribution of the proposals I did not separate.  *Against the coordinator's run for this `ln Z`* with
P8's constants (`pi_inference/nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`; theirs: 4 000 000
proposals, 12 000 evaluations): 0.188 nats as stated (Hoeffding) and 0.041 in the two-end form
with empirical Bernstein (`[655.592089, 655.632643]`, the interval quoted in addendum A17 (18)) —
here {NS_LKSE_5_thy_H_w} and {NS_LKSE_5_two_EB_w} in the same two forms, from a tenth of the proposals and
{NS_LKSE_5_N} evaluations; their two-end interval contains {NS_LKSE_5_inside_coord} of the {NS_LKSE_5_nkinds} intervals the
driver prints for my run (four of them are in the table).  The plain sampler with the same
{NS_LKSE_5_N} evaluations (printed by the coordinator's driver) is {NS_LKSE_5_plain_min}–{NS_LKSE_5_plain_max} times wider.  What limits the result
now is the number of proposals, and each proposal costs `1/(1 − e^{{−D}})` = 59 exact draws of the
floor: 363 of the {NS_LKSE_5_secs} seconds (request P9-E5).

**(B) (LKSE)₃ from the ORDER-4 ball** (181 268 evaluations; `logs/nested_LKSEc12_H_m4_w7.log`;
{NS_LKSE_4_secs} s, peak RSS {NS_LKSE_4_rssmb} MB).  Outer sandwich `[{NS_LKSE_4_lo}, {NS_LKSE_4_hi}]`,
`D = {NS_LKSE_4_D}` (the bracket of §5.2); {NS_LKSE_4_Nf} proposals from {NS_LKSE_4_draws} draws;
envelope bracket estimated from the proposals: {NS_LKSE_4_env} nats; mean `ρ = {NS_LKSE_4_rho}`:
{NS_LKSE_4_acc} proposals accepted for evaluation, {NS_LKSE_4_N} evaluated; evaluated energy
outside the inner sandwich at {NS_LKSE_4_viol_in}, outside the outer at {NS_LKSE_4_viol_out}; clipping
active at {NS_LKSE_4_clip}, inconsistent at {NS_LKSE_4_bad}.  With probability at least 0.95: as stated
(Hoeffding) `[{NS_LKSE_4_thy_H_lo}, {NS_LKSE_4_thy_H_hi}]`, width **{NS_LKSE_4_thy_H_w}**; two-end, empirical
Bernstein `[{NS_LKSE_4_two_EB_lo}, {NS_LKSE_4_two_EB_hi}]`, width {NS_LKSE_4_two_EB_w}.  {STRETCH_B_READING}

**(C) Lys₁₂ from the order-3 ball: not run.**  The deterministic bracket there is 0.077 nats
(§5.2) and the resolved envelope is not small (first-order number 0.053 on the Gibbs sample),
so a sampler would have something to do: with 12 000 evaluations I expect about `2·10⁻³` nats
"as stated" from 3 841 + 12 000 evaluations in all (written at 11:47, before any sampler run).
I did not run it because the band-7 model of Lys₁₂ together with the sampler's stored
messages peaks near 2.9 GB (the coordinator's own Lys₁₂ sampler log: 2 877 MB), too close to
the 3 GB limit of this workstream.  It is one command (`p9_07_nested.py K12 H 3 7 W window --N 12000
--Nf 400000`) for whoever may use the memory.
