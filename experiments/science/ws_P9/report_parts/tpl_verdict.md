1. **The first stage of the brief — the rotamers of the *host* side chains alone — is a weak
   dependence, and I can say why** [M, §3.1]: over the rotamers the ensemble visits, the resolved
   site penalty is 0.72–1.00 of the state-independent one; the anchor half of P3's host step,
   the blocks without a host in `T` and the *maximal* increments of the non-host sites do not
   move.  In certified nats (the reference's own form: triples, band 7, split around the
   anchor) it is still worth {K12_5_ref_T} → {K12_5_s1_T} for Lys₁₂ at order 5, and — because
   the reference floors were delocalised — {K12_4_ref_T} → {K12_4_s1_T} at order 4 and
   {LKSE_5_ref_T} → {LKSE_5_s1_T} for (LKSE)₃.
2. **The second stage is the lever** [P, §1; M]: with the non-host sites at their actual
   rotamers too — P3's theorem with the increments it is *stated* with; the maxima were only in
   the computable forms — the typical bound of a subset is 42–590 times below P8's constant
   in the three cases of the brief, and even its maximum over the states is 41–61 % of it
   (`βΓ = 18.2, 0.99, 26.1` where P8 has `34.0, 2.40, 42.8`: new *state-independent* constants).  The three brackets, like for like:
   **{K12_5_s2_T}** (was 0.0567), **{K12_4_s2_T}** (was 1.4125), **{LKSE_5_s2_T}** (was 4.30) nats.
3. **With every subset charged to one sub-tuple of its sites that fits a window** (an
   allocation in the sense of the theory division's Proposition 11.18f, here with
   state-resolved tables) the brackets are **{K12_5_s2_W}, {K12_4_s2_W}, {LKSE_5_s2_W} nats** —
   the penalty-free widths ({K12_5_zero}, {K12_4_zero}, {LKSE_5_zero}) plus one to three per cent:
   factors {R__K12_5_ref_T__K12_5_s2_W}, {R__K12_4_ref_T__K12_4_s2_W} and {R__LKSE_5_ref_T__LKSE_5_s2_W} against the three
   numbers of the brief.  The allocation alone, with P8's constants, gives {K12_5_sab_W},
   {K12_4_sab_W} and {LKSE_5_sab_W}: where the constants are large its floor delocalises.
4. **One order earlier.**  Lys₁₂ is certified from the order-4 ball (96 366 evaluations) within
   {K12_4_s2_W} nats, `[{K12_4_s2_W_lo}, {K12_4_s2_W_hi}]` — {R__K12_5_ref_T__K12_4_s2_W} times tighter than the
   reference at order 5 (1 621 056 evaluations).  **(LKSE)₃ — "reachable by sampling and not
   deterministically" — is certified deterministically**: `[{LKSE_5_s2_W_lo}, {LKSE_5_s2_W_hi}]` at order 5,
   inside the coordinator's sampled interval; and from its order-4 ball (181 268
   evaluations, where nobody had tried) within **{LKSE_4_s2_W} nats**, `[{LKSE_4_s2_W_lo}, {LKSE_4_s2_W_hi}]`.
   At order 3: {ORDER3}
5. **Statements** [P, §1]: Theorem R — `|g − I_{{m−1}}g|(x) ≤ Σ_{{T⊆S(x)}} Θ_T(x_T)`, block by block, with
   the hosts *and* the non-host sites of `T` at their actual states (P8's Theorem AH before its
   maximum; P3's Theorem 3 with actual increments); Proposition P — any allocation of
   `Θ_T(x_T)` to tables on sub-tuples by maxima over the *other* sites is a valid penalty, the
   state-dependent form of P3's site shares and P6's Lemmas A, A′.
6. **Validated by enumeration** [X, §2] on Lys₄, Lys₅, LKSE:5, every order, every state:
   {VAL_V1} block-level comparisons, {VAL_V2} whole-function checks, {VAL_V3} table checks,
   no violation; the resolved bound is attained within 0.3 %.  **Controls that fail as
   intended:** the minimum over the rotamers in place of the value, and the value at a wrong
   rotamer, fail at block level in every row and against every table form; against the
   whole function they fail only for stage 2 — for stage 1 that check has no power.
   Brackets on Lys₅ and LKSE:5: every sandwich at every state, exact `ln Z` inside.
7. **At twelve residues** [M, §3.4]: the resolved bound was checked at *every* state with
   exactly four side chains off the anchor (1 524 690 states of Lys₁₂, 3 290 515 of (LKSE)₃),
   at 20 000 random states with exactly five, and at 2 000–2 500 uniformly random states per
   case: no violation, both controls fail; my driver reproduces the coordinator's reference
   brackets digit for digit; the coordinator's sampled intervals are consistent with every
   bracket.
8. **Predictions** (written before the models, §4.1): within 3–8 % in the first-order cases
   (Lys₁₂ order 5, Ser₁₂), 20–40 % too high for the stage-2 rows in the equal-share forms elsewhere; about the floor
   itself wrong five times of nine — three times too pessimistic, twice too optimistic (by
   factors 36 and 9).
9. **Stretch** [M, §5.4]: {STRETCH_LINE}
10. **Limits.**  A draft: no proof refereed or machine-checked, one implementation of the
    stage-2 evaluation, no run by anyone else is cited; P3's enclosures inherited; and the
    brackets are now the *reductions* of the band (ten far pairs), which I did not touch.
