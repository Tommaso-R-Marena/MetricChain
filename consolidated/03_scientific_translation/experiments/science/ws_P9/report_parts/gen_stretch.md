The brief: for (LKSE)₃ the sampler's cost is the envelope's own bracket, 1.23 nats with P8's
constants; the fully resolved `Σ_{T⊆S(x)} Θ²_T(x_T)` is a valid envelope (Theorem R); estimate
its cost per proposal first.

**Cost, estimated before anything was built** (`NOTES.md`, 11:26; a scratch timing, not a cited
log).  The envelope is a sum of 792 table look-ups: 36 microseconds per state at uniformly
random states — 14 s for 400 000 proposals.  What costs is the proposals themselves: with an
outer bracket `D` the rejection step keeps a fraction `1 − e^{−D}` of the exact draws of the
floor, so the tighter the outer sandwich, the more draws a proposal costs (24 million draws
for 400 000 proposals at `D = 0.017`).

**Driver.**  `p9_07_nested.py` calls the coordinator's `nested_sampler.main()` unchanged, with the
outer sandwich of the window form of stage 2 and an envelope object that reads the stored
tables `Θ²_T` (`p9_03_tables.py --keeptabs`); the inner sandwich, its clipping and its
allowances are the coordinator's.  The envelope object reproduces the envelope accumulated
by the table run at the 960 Gibbs states to `3·10⁻²⁰` kcal/mol (from the same scratch run as
the timing: recorded in `NOTES.md`, not a cited log).

**(A) (LKSE)₃, order 5** (`logs/nested_LKSEc12_H_m5_w7.log`; 471 s, peak RSS 2736 MB).
Outer sandwich `[655.604050, 655.621038]`, `D = 0.01699` — the bracket of §4.3 rebuilt by this
driver.  400 000 proposals from 23 718 047 exact draws of the floor
(45 685 distinct states).  **The resolved envelope's own bracket, estimated from the
proposals: 3.48e-06 nats** (P8's constants: 1.23); mean `ρ = 0.000205`:
90 proposals accepted for evaluation, 90 evaluated; evaluated energy outside
the inner sandwich at 0, outside the outer at 0; clipping active at
0 proposals, inconsistent at 0.  With probability at least 0.95, given the two
sandwiches:

| bound | interval for `ln Z` | width (nats) |
|---|---|---|
| as stated by the theory division (Hoeffding) | `[655.612610, 655.612778]` | 0.00017 |
| two-end form (Hoeffding) | `[655.612652, 655.612736]` | 8.5e-05 |
| as stated, empirical Bernstein | `[655.612672, 655.612716]` | 4.4e-05 |
| **two-end form, empirical Bernstein** | `[655.612673, 655.612715]` | **4.3e-05** |

*Against what I had written before the run* (`NOTES.md`, 11:26): width about `1.7·10⁻⁴` "as stated"
— found 0.00017; "fewer than ten evaluations" — found 90.  That guess was wrong twice
over: my own rule `ρ ≈ (envelope bracket)/D` with my own input (`10⁻⁶/0.017`) gives 24 of 400 000,
not "fewer than ten" (a slip of arithmetic); and the envelope's bracket under the proposals is
3.48e-06, two to three times its first-order numbers on the two Gibbs samples of the true
ensemble (`1.2·10⁻⁶` and `1.6·10⁻⁶`, §3.2) — the rule itself holds (mean `ρ = 0.000205` is
3.48e-06`/D`).  How much of that factor is the inner sandwich's own allowances and how much
the different distribution of the proposals I did not separate.  *Against the coordinator's run for this `ln Z`* with
P8's constants (`pi_inference/nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`; theirs: 4 000 000
proposals, 12 000 evaluations): 0.188 nats as stated (Hoeffding) and 0.041 in the two-end form
with empirical Bernstein (`[655.592089, 655.632643]`, the interval quoted in addendum A17 (18)) —
here 0.00017 and 4.3e-05 in the same two forms, from a tenth of the proposals and
90 evaluations; their two-end interval contains 6 of the 6 intervals the
driver prints for my run (four of them are in the table).  The plain sampler with the same
90 evaluations (printed by the coordinator's driver) is 29–151 times wider.  What limits the result
now is the number of proposals, and each proposal costs `1/(1 − e^{−D})` = 59 exact draws of the
floor: 363 of the 471 seconds (request P9-E5).

**(B) (LKSE)₃ from the ORDER-4 ball** (181 268 evaluations; `logs/nested_LKSEc12_H_m4_w7.log`;
323 s, peak RSS 1512 MB).  Outer sandwich `[655.603013, 655.622116]`,
`D = 0.0191` (the bracket of §5.2); 400 000 proposals from 21 195 687 draws;
envelope bracket estimated from the proposals: 0.000727 nats; mean `ρ = 0.0381`:
15158 proposals accepted for evaluation, 1200 evaluated; evaluated energy
outside the inner sandwich at 0, outside the outer at 0; clipping
active at 0, inconsistent at 0.  With probability at least 0.95: as stated
(Hoeffding) `[655.612562, 655.612814]`, width **0.00025**; two-end, empirical
Bernstein `[655.612657, 655.612719]`, width 6.2e-05.  *Reading.*  What I had written before the run (`NOTES.md`, 11:47): "2–3·10⁻⁴ as stated, up to 1 200
evaluations" — found 0.00025 with 1200 (the cap I had set: 15158 proposals were
accepted for evaluation and the driver evaluates the first 1200; 1072 distinct states).
*The two runs against each other:* the interval from the order-4 ball contains the interval of the
same kind from the order-5 ball in 6 of the 6 forms the driver prints; 6 of the
6 order-4 intervals lie inside the deterministic bracket of order 5, and 6
inside the coordinator's two-end interval.  At this order the envelope is no longer negligible
(its own bracket 0.000727 nats; mean `ρ = 0.0381`): the evaluations carry 26 % of the
half-width "as stated", and the plain sampler with the same 1200 evaluations is
5.9–17 times wider (order 5: 29–151 times).  In evaluations of the
model function: 181 268 + 1200 here, 3 471 783 + 90 in run (A), 3 471 783 + 12 000 in the
coordinator's run.

**(C) Lys₁₂ from the order-3 ball: not run.**  The deterministic bracket there is 0.077 nats
(§5.2) and the resolved envelope is not small (first-order number 0.053 on the Gibbs sample),
so a sampler would have something to do: with 12 000 evaluations I expect about `2·10⁻³` nats
"as stated" from 3 841 + 12 000 evaluations in all (written at 11:47, before any sampler run).
I did not run it because the band-7 model of Lys₁₂ together with the sampler's stored
messages peaks near 2.9 GB (the coordinator's own Lys₁₂ sampler log: 2 877 MB), too close to
the 3 GB limit of this workstream.  It is one command (`p9_07_nested.py K12 H 3 7 W window --N 12000
--Nf 400000`) for whoever may use the memory.
