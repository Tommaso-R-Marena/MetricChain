1. **The first stage of the brief — the rotamers of the *host* side chains alone — is a weak
   dependence, and I can say why** [M, §3.1]: over the rotamers the ensemble visits, the resolved
   site penalty is 0.72–1.00 of the state-independent one; the anchor half of P3's host step,
   the blocks without a host in `T` and the *maximal* increments of the non-host sites do not
   move.  In certified nats (the reference's own form: triples, band 7, split around the
   anchor) it is still worth 0.05669 → 0.0452 for Lys₁₂ at order 5, and — because
   the reference floors were delocalised — 1.413 → 0.3493 at order 4 and
   4.301 → 1.871 for (LKSE)₃.
2. **The second stage is the lever** [P, §1; M]: with the non-host sites at their actual
   rotamers too — P3's theorem with the increments it is *stated* with; the maxima were only in
   the computable forms — the typical bound of a subset is 42–590 times below P8's constant
   in the three cases of the brief, and even its maximum over the states is 41–61 % of it
   (`βΓ = 18.2, 0.99, 26.1` where P8 has `34.0, 2.40, 42.8`: new *state-independent* constants).  The three brackets, like for like:
   **0.016** (was 0.0567), **0.1115** (was 1.4125), **0.1946** (was 4.30) nats.
3. **With every subset charged to one sub-tuple of its sites that fits a window** (an
   allocation in the sense of the theory division's Proposition 11.18f, here with
   state-resolved tables) the brackets are **0.007233, 0.007347, 0.01699 nats** —
   the penalty-free widths (0.007133, 0.007132, 0.0167) plus one to three per cent:
   factors 7.8, 192 and 253 against the three
   numbers of the brief.  The allocation alone, with P8's constants, gives 0.007286,
   0.7207 and 1.311: where the constants are large its floor delocalises.
4. **One order earlier.**  Lys₁₂ is certified from the order-4 ball (96 366 evaluations) within
   0.007347 nats, `[517.125649, 517.132996]` — 7.7 times tighter than the
   reference at order 5 (1 621 056 evaluations).  **(LKSE)₃ — "reachable by sampling and not
   deterministically" — is certified deterministically**: `[655.604050, 655.621038]` at order 5,
   inside the coordinator's sampled interval; and from its order-4 ball (181 268
   evaluations, where nobody had tried) within **0.0191 nats**, `[655.603013, 655.622116]`.
   At order 3: Lys₁₂ is still certified from its order-3 ball (3 841 evaluations) within 0.07686 nats, `[517.108870, 517.185731]`; (LKSE)₃ is not (658.9 nats: its floor delocalises completely).
5. **Statements** [P, §1]: Theorem R — `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x)} Θ_T(x_T)`, block by block, with
   the hosts *and* the non-host sites of `T` at their actual states (P8's Theorem AH before its
   maximum; P3's Theorem 3 with actual increments); Proposition P — any allocation of
   `Θ_T(x_T)` to tables on sub-tuples by maxima over the *other* sites is a valid penalty, the
   state-dependent form of P3's site shares and P6's Lemmas A, A′.
6. **Validated by enumeration** [X, §2] on Lys₄, Lys₅, LKSE:5, every order, every state:
   18 181 488 block-level comparisons, 844 392 whole-function checks, 13 510 272 table checks,
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
9. **Stretch** [M, §5.4]: with the resolved envelope and the window-form sandwich in the coordinator's nested sampler, the envelope's own bracket for (LKSE)₃ falls from 1.23 nats to 3.48e-06, and at probability 0.95 `ln Z` is known within **0.00017 nats as the theory division states the bound** (`[655.612610, 655.612778]`; 4.3e-05 in the two-end form with empirical Bernstein) from 400 000 proposals and 90 new evaluations — the coordinator's run with P8's constants: 0.188 and 0.041 in the same two forms, from 4 000 000 proposals and 12 000 evaluations.  From the order-4 ball alone: 0.00025 nats with 1200 evaluations.  One run per case, one seed; the Lys₁₂ run from the order-3 ball was not made (memory).
10. **Limits.**  A draft: no proof refereed or machine-checked, one implementation of the
    stage-2 evaluation, no run by anyone else is cited; P3's enclosures inherited; and the
    brackets are now the *reductions* of the band (ten far pairs), which I did not touch.
