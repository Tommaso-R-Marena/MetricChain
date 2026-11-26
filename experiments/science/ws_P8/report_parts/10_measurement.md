---

## 1. The measurement (step 1 of the brief)

**Instances.**  Helix: Ace-Lys_n-NMe, `n = 3, 4, 5` (τ = 0.70; 2 352, 16 464, 115 248 states; 78, 100,
122 atoms) and the patterned sequence LKSE:4, LKSE:5, LKSE:6 (LKSE, LKSEL, LKSELK; τ = 0.60; 7 254,
14 508, 217 152 states; 79, 98, 120 atoms).  Controls with neutral side chains (Ser₄, Ser₅, Ser₆,
Leu₆, Leu₈ on the helix — P5's instances, re-measured with my code) and three strand instances
(Lys₃, Lys₄, LKSE:5; 5 733, 74 529, 14 580 states) for contrast.  Anchor `x⁰ = argmin E` by enumeration, as in P5 (it coincides
with P3's coordinate-descent anchor wherever I compared).

**What is computed, all by exact enumeration of all states** (`p8_01_measure.py`; P5's definitions
and its `anch_walk` for the mixed differences).  `g = Σ_{p≤q} t_pq` with the pair terms
`t_pq = −κ q_p q_q M_pq` (`p < q`) and self terms `t_pp = −(κ/2) q_p² / B_p`; my sum equals P3's evaluator
at every state (largest deviation `5·10⁻¹²` kcal/mol, asserted).  For every subset `T` of order `3 … n`:

* **truth**: `c_T^anch(g)`, and the range of the true remainder `g − I_{m−1}g`;
* **all charges positive**: `c_T^anch(g_{|q|})`;
* **best pair-by-pair bound** `PP_T = Σ_{p≤q} c_T^anch(t_pq)` — the exact constant of *every* pair term,
  stored per `(T, p, q)`: the least value any term-by-term bound can have (P5's Proposition 7(b));
* **P3**: `ĉ_T` and `Γ_m`, decomposed by atom and atom pair;
* **the sign-blind lower bounds** of P5's Proposition 7 / Theorem 8 (`p8_02_signblind.py`): (A) per
  subset, the largest `|Δ_T g_s|` found over sign patterns `s`; (C) the largest remainder
  `sup_x |g_s − I_{m−1}g_s|` of a pattern found.  *How the search is done:* for the symmetric matrix
  of the mixed difference (at the context and states where the true, and where the all-positive,
  constant is attained) or of the remainder (at the four states with the largest true and the four
  with the largest all-positive remainder, and four random states with at least `m` changed
  sites), `|sᵀAs|` is maximised by 1-flip ascent in both signs of the objective, from the true
  signs, all-plus, the sign vectors of the six eigenvectors of largest `|eigenvalue|` and 24 random
  vectors, followed by best-improving 2-flips; the patterns found for the remainder are then
  evaluated at **all** states.  *How good it is:* every number is an exact evaluation, hence a
  valid lower bound of the least sign-blind bound; from above that bound is bracketed by `PP_T`.
  The bracket `PP/(A)` is 1.6–5.5 (table), so the least sign-blind bound is known within that
  factor; I did not try an exhaustive or semidefinite search.
* the new bounds S, SA (pair-wise) and Sb, SAb (block-wise) of §3.

<!--T:T1-->

<!--T:T1b-->

("—": not computed — see §7.  †: the block-wise variants were not run for that instance; the
pair-wise variant 'SA' is used in the ratio.)  The coordinator's quick table in the brief is reproduced where
both exist (Lys₄: `Γ₃ = 33.6`, 0.189, 178; 0.854, 0.0029, 290.  LKSE:5: 287, 0.475, 603; 29.2, 0.0505,
578; 1.53, 0.0044, 347), and so are P3's `Γ_m` (its §3.3: K, H: 13.6, 33.6, 0.854; LKSE, H: 125, 5.25,
29.1, 1.53, 143).

**Findings** [M].

1. **For lysine the price of not looking at signs is small.**  Every sign-blind bound of the
   remainder must be at least 4.6 (Lys₃), 6.8 and 6.6 (Lys₄, orders 3, 4), 5.8, 5.1 and 3.2 (Lys₅,
   orders 3, 4, 5) times the truth — against 16–153 for leucine at orders 3–5 (P5's Theorem 8);
   making all charges positive already gives 2.9–6.2 times the true sums.  A charged group has
   little to cancel.  For the patterned sequence the factor is larger, 14–37 (LKSE:4, LKSE:5): it
   contains both signs of charge and two apolar residues (LKSE:6: 13, 15, 16 at orders 3–5 and
   4.2 at order 6).
2. **P3's bound is far above that floor**: `Γ_m` is 21–490 times the largest remainder of a
   sign pattern found for lysine (25–40 for LKSE:4, LKSE:5; 58–470 for LKSE:6), and 7.7–89 times
   the best pair-by-pair bound for lysine, 5.8–117 for the patterned sequence (for Leu and Ser P5
   found 3.3–16), growing with the order and with the chain (Lys₅: 8.3, 37, 89; LKSE:6: 7.2, 23,
   53, 117).  For lysine, of P3's factor 97–1 580 over the truth only 3–7 is the price of the
   sign-blind class, 2.0–5.5 lies between the per-subset sign-blind floor (A) and the
   pair-by-pair optimum, and the rest — an order of magnitude at order 3, two at order 5 — is
   slack of P3's inequalities (table T1b).  §3.2 locates it.
3. **The truth falls fast with the order for lysine, slowly for the patterned sequence.**  Sums
   of exact anchored constants: Lys₅ 1.66, 0.0302, `3.6·10⁻⁴` kcal/mol at orders 3, 4, 5 (55- and
   83-fold; the largest remainder 38- and 69-fold) — as fast as serine (Ser₆: 39- and 58-fold in
   P5's Table 1a); LKSE:6: 2.80, 0.210, 0.0118, `4.1·10⁻⁴` (13-, 18-, 29-fold; the largest remainder
   14-, 11-, 14-fold), nearer to leucine (Leu₁₂: 3.7-, 6.1-, 8.0-fold).  P3's `Γ_m` falls 7.6- and
   36-fold for Lys₅ and 4.5-, 9.0-, 20-fold for LKSE:6.
4. **Per subset the truth is an order of magnitude larger for lysine than for serine** at the same
   place on the same helix: the one four-subset of four residues `2.9·10⁻³` against `1.3·10⁻⁴`
   kcal/mol (22 times); five residues, sums over the ten triples 1.66 against 0.126 (13), over
   the five four-subsets 0.0302 against 0.00179 (17), the five-subset `3.6·10⁻⁴` against `3.0·10⁻⁵`
   (12).

**By atom group (item (v) of the brief).**  Four classes: **bb** — every fixed atom (backbone,
Cβ, caps); **nsc** — the moving atoms of a neutral side chain (Leu, Ser); **chain** — the aliphatic
part of a charged side chain (Lys: Hβ, Cγ, Hγ, Cδ, Hδ, Cε, Hε; net charge +0.401 e; Glu: Hβ, Cγ, Hγ);
**head** — the charged group (Lys: Nζ, Hζ₁₋₃, +0.635 e; Glu: Cδ, Oε₁, Oε₂).  For each pair of
classes: the *signed share of the truth* — the value of `Δ_T` of that class pair's function at the
context and states where `|Δ_T g|` is largest, with the sign of `Δ_T g` (these shares add up to
`c_T(g)` exactly); the exact anchored constant of the class-pair function; the best pair-by-pair
bound, P3's bound and the new bounds restricted to the pairs of the class pair.  *Self against
cross:* the self terms are the rows "self:…", the cross terms the class pairs; for Lys₅ the
self part carries +18 %, −4.5 %, +0.1 % of the truth at orders 3, 4, 5 (almost all of it the head
groups') and 3.2 %, 3.3 %, 0.5 % of P3's bound — for lysine both the truth and the bound are
cross terms.

<!--T:T2|Lys₅,LKSE:5,LKSE:6-->

(Rows of Lys₅, LKSE:5 and LKSE:6; all fourteen instances: `experiments/science/ws_P8/out/tables.md`,
table T2.)

5. **For lysine the truth is the head groups, with one sign.**  On Lys₅ the class pairs that
   involve an ammonium group (head–head, chain–head, bb–head, and the head atoms' self terms)
   carry 96 %, 95 % and 101 % of the true constants at orders 3, 4, 5, head–head alone 42–45 %;
   backbone–backbone pairs carry about 1 %.  All large shares have the same sign: the sum of the
   absolute shares is 1.03–1.11 times the truth.  (Leucine, P5's Table 1a: for Leu₆ at order 3
   the self and the cross part are each more than twice the total — 0.60 and 0.68 against 0.27
   kcal/mol — and cancel.)
6. **P3's bound sits on the same pairs, and that is where its slack is**: head–head 40–45 %,
   bb–head 31–35 %, chain–head 16 % of `Γ_m` for Lys₅, with ratios to the best pair-by-pair bound
   of 12, 98, 313 (head–head), 9.5, 44, 104 (chain–head), 7.3, 28, 67 (bb–head) at orders 3, 4, 5,
   against 3.4, 4.0, 7.7 for backbone–backbone pairs.
7. **For the patterned sequence the truth is mostly backbone–neutral-side-chain and
   backbone–head, with cancellation** (LKSE:5, order 4: bb–nsc +64 %, bb–head +21 %, nsc–head
   +11 %; order 5: bb–nsc +109 %, bb–bb −21 %; LKSE:6: bb–nsc +24, +45, +83, +99 % at orders 3–6),
   and after the state-wise maximum the bound sits on the apolar part: bb–nsc 35–39 % and bb–bb
   22–33 % of the new bound on LKSE:5, 25–32 % and 21–40 % on LKSE:6.  What stops the patterned
   sequence is then leucine's problem (P5), not the charges.
8. **Controls and the strand** (tables T1, T1b).  *Neutral side chains, same code:* `Γ_m` over the
   pair-by-pair optimum is 4.6–22 for Ser₄–Ser₆ and 3.4–11 for Leu₆, Leu₈ (P5: 3.3–16); the
   state-wise maximum gains 1.7–3.5 for serine and 1.00–1.05 for leucine (two rotamers per
   site: nothing to resolve); the truth of Ser₆ falls 39-, 58-, 191-fold per order.  *Strand:*
   for lysine the truth is not smaller than on the helix — Lys₄: 0.518 and 0.0502 kcal/mol at
   orders 3, 4 against 0.232 and 0.0029 (on a strand the side chains `i` and `i+2` point to the
   same side [H]); Lys₃: 0.1408 against 0.1407, a coincidence to three digits, every other column
   differs — and 5–76 times smaller for LKSE:5 (0.225, 0.0108, `5.8·10⁻⁵` against 1.18, 0.108,
   0.0044).  There the price of the sign-blind class is 3.6–12 for lysine and 27–50 for LKSE:5,
   P3's bound is nearer to the pair-by-pair optimum (2.9–6.6; 3.9–34) and the state-wise
   maximum gains less (1.3–1.9; 1.7–6.0).
