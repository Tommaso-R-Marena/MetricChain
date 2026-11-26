The brief: for (LKSE)₃ the sampler's cost is the envelope's own bracket, 1.23 nats with P8's
constants; the fully resolved `Σ_{{T⊆S(x)}} Θ²_T(x_T)` is a valid envelope (Theorem R); estimate
its cost per proposal first.

**Cost, estimated before anything was built** (`NOTES.md`, 11:26; a scratch timing, not a cited
log).  The envelope is a sum of 792 table look-ups: 36 microseconds per state at uniformly
random states — 14 s for 400 000 proposals.  What costs is the proposals themselves: with an
outer bracket `D` the rejection step keeps a fraction `1 − e^{{−D}}` of the exact draws of the
floor, so the tighter the outer sandwich, the more draws a proposal costs (24 million draws
for 400 000 proposals at `D = 0.017`).

**Driver.**  `p9_07_nested.py` calls the coordinator's `nested_sampler.main()` unchanged, with the
outer sandwich of the window form of stage 2 and an envelope object that reads the stored
tables `Θ²_T` (`p9_03_tables.py --keeptabs`); the inner sandwich, its clipping and its
allowances are the coordinator's.  The envelope object reproduces the envelope accumulated
by the table run at the 960 Gibbs states to `3·10⁻²⁰` kcal/mol (from the same scratch run as
the timing: recorded in `NOTES.md`, not a cited log).

**(A) (LKSE)₃, order 5** (`logs/nested_LKSEc12_H_m5_w7.log`; {NS_LKSE_5_secs} s, peak RSS {NS_LKSE_5_rssmb} MB).
Outer sandwich `[{NS_LKSE_5_lo}, {NS_LKSE_5_hi}]`, `D = {NS_LKSE_5_D}` — the bracket of §4.3 rebuilt by this
driver.  {NS_LKSE_5_Nf} proposals from {NS_LKSE_5_draws} exact draws of the floor
({NS_LKSE_5_distinct} distinct states).  **The resolved envelope's own bracket, estimated from the
proposals: {NS_LKSE_5_env} nats** (P8's constants: 1.23); mean `ρ = {NS_LKSE_5_rho}`:
{NS_LKSE_5_acc} proposals accepted for evaluation, {NS_LKSE_5_N} evaluated; evaluated energy outside
the inner sandwich at {NS_LKSE_5_viol_in}, outside the outer at {NS_LKSE_5_viol_out}; clipping active at
{NS_LKSE_5_clip} proposals, inconsistent at {NS_LKSE_5_bad}.  With probability at least 0.95, given the two
sandwiches:

| bound | interval for `ln Z` | width (nats) |
|---|---|---|
| as stated by the theory division (Hoeffding) | `[{NS_LKSE_5_thy_H_lo}, {NS_LKSE_5_thy_H_hi}]` | {NS_LKSE_5_thy_H_w} |
| two-end form (Hoeffding) | `[{NS_LKSE_5_two_H_lo}, {NS_LKSE_5_two_H_hi}]` | {NS_LKSE_5_two_H_w} |
| as stated, empirical Bernstein | `[{NS_LKSE_5_thy_EB_lo}, {NS_LKSE_5_thy_EB_hi}]` | {NS_LKSE_5_thy_EB_w} |
| **two-end form, empirical Bernstein** | `[{NS_LKSE_5_two_EB_lo}, {NS_LKSE_5_two_EB_hi}]` | **{NS_LKSE_5_two_EB_w}** |

{STRETCH_MORE}
