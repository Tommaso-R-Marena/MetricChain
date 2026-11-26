## 3. The tables: what they look like

Scripts: `p9_03_tables.py` (the bounds `Θ¹_T`, `Θ²_T` of all subsets of a twelve-residue peptide,
reduced on the fly to the sums the forms need), `p9_04_gain.py` (ratios on two Gibbs samples;
no model is built).  The Gibbs samples are the coordinator's sampler with its seeds (4242, 777;
`p9_02_gibbs.py`); they reproduce the off-anchor frequencies of the coordinator's logs digit
for digit and are uncertified.

### 3.1 The bound of a subset as a function of the states of its sites [M]

`Γ_m` and its resolved counterparts, in `k_BT` (sums over all subsets; P8's two columns are
re-computed here in P8's code path and equal P8's stored per-subset values exactly —
relative deviation `0.0` in every run):

{GEN_CONSTANTS}

*Reading.*  **Stage 1 — the dependence on the host's rotamer is weak.**  Summed over the
subsets, the maximum and the minimum of `Θ¹_T` over the states of `T` differ by a factor 1.2–4:
the sum of the minima is 25–26 % of P8's constants for lysine, 62–66 % for the patterned sequence, 80 % for serine; the sum of its
medians 37 %, 69–73 %, 87 %; and its joint maximum is 97–99.9 % of 'SAb' (the block-wise
maxima nearly coincide).  The reason is in the formula: for a host `l ∈ T` the bound is
`W(x⁰_l) + W(x_l)` (P3's Remark L3) — the anchor half does not depend on `x`; the blocks without
a host in `T` do not either; and `W(b)` still carries the *maximal* increments of the non-host
sites, so it moves only through hulls and distances.  On Lys₄ the state-independent part is
36–43 % of the constant (`logs/probe_K4_H_0.70.log`).  This is the answer to the brief's
alternative stopping condition, *for the first stage as the brief defines it*.

**Stage 2 — the dependence on the rotamers of the non-host sites is strong, and grows with
the order.**  The typical (median) value of `Θ²_T` is 38, 146, 590 times below P8's constant
for Lys₁₂ at orders 3, 4, 5; 6, 14, 42 times for (LKSE)₃; 13 times for Ser₁₂; its minimum up
to five orders of magnitude below.  And **its maximum over the states — a state-independent
constant, `ĉ^{J,2}_T` of Corollary J — is 41–74 % of P8's**: `βΓ_m` falls from 34.0 to 18.2
(Lys₁₂, order 4), from 2.40 to 0.99 (order 5), from 42.8 to 26.1 ((LKSE)₃, order 5), without
any state dependence in the penalty.  The increments enter as products over the `m − 1` or
`m − 2` non-host sites of each term, and the rotamers the ensemble visits are mostly the ones
near the anchor, with small increments.

### 3.2 Site by site (question 3 of the brief) [M]

{GEN_GAIN}

*Reading.*  (i) *Maximum over `b`:* at most 1 in every row, as it must be; for stage 1 it is
0.84–1.00, for stage 2 0.28–0.67.  **It is not 1 for the worst rotamer, as the brief
expected, for two reasons:** subset by subset the maximum over `b` of `c_{T,i}(b)` *is* the joint
maximum `ĉ^J_T` (by construction), but different subsets have different worst rotamers of the
same site, so the maximum of the sum is below the sum of the maxima; and P8's constant, the
reference of the ratio, takes its maxima block by block, the table jointly.  (ii) *Boltzmann-typical value:* stage 1 0.72–1.00 of the
state-independent penalty — nearly nothing; stage 2 0.03–0.37 for lysine and 0.05–0.26 for
the patterned sequence (0.66 at its two-state leucine sites, which have nothing to resolve
in themselves and gain only through the other sites of their subsets).  (iii) For Lys₁₂ the
three N-terminal sites, which carry most of the off-anchor weight (each is off the anchor 23–40 % of the time), sit in **one**
alternative rotamer whose penalty is near the maximum (0.28–0.37 of 'SAb'); the nine frozen
sites visit rotamers at 0.03–0.17.  (iv) The gain grows with the size of the tuple that is
resolved: first-order numbers of forms S, B, T fall to 0.16–0.28, 0.07–0.20, 0.10–0.23 of
the state-independent ones, the window form to `4·10⁻⁴`–`0.04`, the envelope to
`5·10⁻⁵`–`0.03` (both samples; `0.015` at most on the check sample).

### 3.3 By rotamer [M]

{GEN_ROTAMERS}

### 3.4 The resolved bound at twelve residues, checked where it can be [M]

`p9_06_check12.py`.  (a) At a state with exactly `m` sites off the anchor the remainder **is**
the anchored term of order `m`, `g − I_{m−1}g = d_T(x_T)`, which the ball of radius `m` gives exactly;
so with P8's balls of radius 3 and 4 Theorem R can be tested at orders 3 and 4 at **every**
such state.  (c) At order 5 no ball of radius 5 exists; there 20 000 random states with
exactly five sites off the anchor were evaluated (one new evaluation each; the lower orders
from the ball of radius 4).  (b) Uniformly random states with `m … 12` sites off the anchor
(new evaluations of `g`; `I_{m−1}g` from the ball by my own formula, self-tested to `2.5·10⁻¹⁴`), as
the coordinator did for P8's constants.  Controls as in §2: W1 (the minimum of the table in
place of its value) and W2 (the table rolled by one rotamer along each axis).

{GEN_CHECK12}

No violation in any row.  Both controls fail in (a) and (c) in every row (`10²`–`2·10⁶`
violations), and fail weakly in (b) (1–11 violations): (a) and (c) are the checks with power.
The resolved bound is still 8–15 times the exact term at its tightest state and 200–400
times at the median state: the slack that is left is the sign-blind class and the suprema
over hulls, not the rotamers.
