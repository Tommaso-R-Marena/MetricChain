Certified width of the bracket of `ln Z` in nats, helix, band 7, the coordinator's models; "→" reads: P8's state-independent constants → host rotamers resolved (stage 1, the brief's first stage) → all sites of `T` resolved (stage 2).

1. **Lys₁₂, order 5**, triple form (the reference's own form): **{K12_5_ref_T} → {K12_5_s1_T} → {K12_5_s2_T}**; window form of stage 2: **{K12_5_s2_W}**, `[{K12_5_s2_W_lo}, {K12_5_s2_W_hi}]`.
2. **Lys₁₂, order 4**, triple form: **{K12_4_ref_T} → {K12_4_s1_T} → {K12_4_s2_T}**; window form: **{K12_4_s2_W}**, `[{K12_4_s2_W_lo}, {K12_4_s2_W_hi}]` — from 96 366 evaluations, tighter than the reference at order 5.
3. **(LKSE)₃, order 5**, triple form: **{LKSE_5_ref_T} → {LKSE_5_s1_T} → {LKSE_5_s2_T}**; window form: **{LKSE_5_s2_W}**, `[{LKSE_5_s2_W_lo}, {LKSE_5_s2_W_hi}]` — deterministic, and inside the coordinator's sampled interval.
4. What is left is the band itself: the penalty-free widths are {K12_5_zero}, {K12_4_zero}, {LKSE_5_zero}; the window-form brackets are these plus one to three per cent.
5. The host rotamers alone are a weak dependence (site penalty 0.72–1.00 of the constant one at the visited rotamers); resolving the non-host sites too is the lever (typical subset bound 42–590 times below P8's constant).
6. One order earlier: (LKSE)₃ from its order-4 ball **{LKSE_4_s2_W}**; Lys₁₂ from its order-3 ball **{K12_3_s2_W}**; (LKSE)₃ at order 3: **no certificate** ({LKSE_3_s2_W} nats, the floor delocalises).
7. Proved [P]: Theorem R (the remainder bound with all sites of `T` at their actual states), Corollary J (smaller state-independent constants), Proposition P (tables by maxima over the other sites), Corollary S (the sandwich).
8. Validated [X] at every state of Lys₄, Lys₅, LKSE:5: {VAL_V1} block comparisons, {VAL_V2} whole-function checks, {VAL_V3} table checks, {ENUM_ROWS} enumerated sandwiches, no violation; the deliberately wrong tables fail.
9. Predictions written before the models: within 3–8 % in the first-order cases; about whether a floor delocalises, wrong five times of nine.
10. Stretch: the resolved envelope in the coordinator's nested sampler gives (LKSE)₃ within {NS_LKSE_5_thy_H_w} nats at probability 0.95 with {NS_LKSE_5_N} new evaluations.  **A draft: nothing refereed or machine-checked, stage 2 in one implementation, no run by anyone else cited.**
