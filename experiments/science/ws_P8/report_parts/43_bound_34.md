### 3.4 Validation against exact constants [M]

Everything below is by **exact enumeration of all states** of the instance.  Scripts:
`p8_01_measure.py` (exact `c_T(t_pq)` for every subset and every atom pair, all contexts; exact
`sup_x |t_pq − I_{m−1}t_pq|` per pair), `p8_01b_restricted.py` (the same constants with the hosts
outside `T` at the anchor — the quantity Theorem AH is about), `p8_03_sr_validate.py` (pair-wise
variants), `p8_03b_statecheck.py` (every pair term at every state), `p8_03c_blockcheck.py` (block-wise
variants), `p8_02_signblind.py` (sign-flipped systems), `p8_10_order_identity.py` (step (a) of the
proof).  A "comparison" is one inequality bound ≥ exact; the tolerance is `10⁻¹²` kcal/mol
(`10⁻¹¹`–`10⁻⁹` in the state-level checks, where the exact side is an alternating sum of up to 64
energies).

<!--T:T5-->

*What each check can detect.*  C1, C2 and B1, B2 compare **term by term** (or block by block)
with exact constants — no cancellation between terms can hide a summand that is too small; the
smallest ratios, 1.0001 (self terms) and 1.010 (pair terms), show that the state-wise bound is
attained within 0.01 % and 1.0 % in the best case and never violated.  C4, C7 and B3 test
Theorem AH itself — the per-term ordering — on the exact remainder of every single term: C7 does
it **at every state** (for Lys₅: every one of the 7 503 terms at each of the 115 248 states at
orders 3, 4, 5 and three variants).  C5 and B4 are the inequality the certificate uses, at every
state, for the true charges, for all charges positive and for the sign patterns found in §1 (the
bounds are sign-blind, so they must hold for all of them).  C0 and B5 are consistency checks of
my evaluation against two independent code paths of workstream P3 (`gfbound` and `termwise`).
*The restriction matters:* the 'SA' summand is **below** the exact all-context constant of its
term in the number of cases shown (26 190 of 120 048 on Lys₅) — as the theory says, it bounds
only the constants with the hosts outside `T` at the anchor; against those it never fails.
*Step (a) of the proof* (P3's Proposition 1 for an arbitrary order of the sites) was checked
separately (`p8_10_order_identity.py`, log `p8_10_order_identity.log`): the identity
`F − I_{m−1}F = Σ_{T ⊆ S(x), |T| = m} Δ_T F(z^{T,x}; x_T)` on random functions on a 3×2×4×3×2 grid for 20 random
orders of the sites, `m = 1 … 5`, at every state (43 200 checks, largest deviation `7·10⁻¹⁵`); on
the GBn2 energy of Lys₄ for all 24 orders of its four sites, `m = 3, 4`, at 400 random states
(19 200 checks, `4.5·10⁻¹³` kcal/mol); and the combinatorial claim of step (b) — with the hosts
ordered last, a host outside `T` is never before `min T` — for 7 sites, five host sets and all `T`
of size 3, 4, 5 (328 cases, no exception).
