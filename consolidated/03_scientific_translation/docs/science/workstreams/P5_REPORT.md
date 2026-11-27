# Workstream P5 (science division) — the compact case: can a certified bound see the cancellation between self and cross terms of GBn2?

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Everything is in
`experiments/science/ws_P5/` (running notes: `NOTES.md`; logs: `logs/`; results: `out/`).
Written 2026-11-26, section by section while the work ran (02:17–03:53 UTC).

Labels: **[P]** proved here on paper (I say how it was checked numerically), **[M]** measured on
the named model by the named script (exact enumeration unless stated), **[N]** numerical
evidence only, **[C]** conjecture, **[H]** heuristic or physical reading, **[K]** known and cited
with the reading level.  Units: kcal/mol; `k_BT = 0.596161 kcal/mol` (300 K).  Every statement is
**model-relative**: it is about the finite function defined by OpenMM 8.6.1's GBn2 expression on
workstream P2's rigid synthetic peptides (Ace-X_n-NMe, ideal α-helix backbone `(−57°, −47°)`,
three-state grid per side-chain dihedral, P2's pruned product domain), exactly as workstream P3
set it up.  (For leucine and serine that product is the whole clash-free domain — coordinator's
note of 2026-11-26 at the head of `P3_REPORT.md`, read in commit `3959dce` — so the correction
about greedily pruned sub-products does not touch the instances used here.)  No sequence was
varied, designed or optimised.  Numbering of statements continues P3's (Propositions 1–6).

---

## 0. Verdict

1. **The route proposed in the brief is not alive.**  On every enumerated helix instance the
   object it would keep signed — for one atom, the sum over the atoms of a neutral or rigid
   group — is only 1.6–4.4 times smaller than the pair-by-pair sum of absolute values (the
   brief's criterion was 10–100), so a bound of that architecture, *even with exact constants*,
   stays 8–53 times above the true order-3–5 anchored constants for leucine (6–8 at order 6) and
   4.5–24 times for serine; the cancellation sits in sums that are signed on both sides at the
   scale of whole residues (residue × residue: within 1.6–6.9 of the truth), where there is no
   small parameter [M, exact enumeration of six instances, §1].
2. **P3's negative finding is now a theorem with numbers** [P + M, §2].  Born radii do not depend
   on the charges, so any bound that uses the charges only through `|q_p|` — every term-by-term
   bound, P3's included — must hold for every sign pattern; by exact evaluation of sign-reversed
   systems, every such bound of the order-`m` remainder exceeds the truth by at least 153, 23,
   16.5 (Leu₆), 72, 24, 38 (Leu₈) and 51, 34, 20 (Leu₁₂) at `m = 3, 4, 5` — but only 3.8 at `m = 6`
   (Leu₁₂) and 3.4–19 for serine, where the question stays open — and on an explicit family (`N`
   equidistant charges `±q` with one Born radius; `N = 4` is two crossed neutral dipoles, built
   with OpenMM's own integrals) by at least `N|Δb|/|Δχ| − (N − 1) ≈ N (B/r)²`, without bound.
3. **Keeping a signed sum at a reference does not rescue the route** [P, §3.2–3.3]: it costs the
   evaluations of the next order and still pays that order's sign-blind bound `m + 1` times
   (Proposition 11), so it is dominated by P3's recipe one order higher; and exactness inside a
   window fails because the many-body terms are long-ranged (the triples that span a
   sixteen-residue helix still carry certified bounds of 0.01–0.2 kcal/mol each).
4. **Nevertheless the compact case is certified at the sizes tested** [P3's Theorem 5 + M, §3.4]:
   P3's own pipeline at order 6 with the floor as a function (site penalties) — a combination
   P3 did not run — gives for Leu₁₂ and Leu₁₆ on the helix deterministic brackets of `ln Z` of
   0.32 and 0.52 nats (0.023 and 0.026 with 20 000 samples; sandwich verified at all 4 096 and
   65 536 states; the exact value 483.8466 reproduced), for Leu₂₀ (`1.05·10⁶` assignments, not
   enumerated) `ln Z ∈ [593.0653, 593.6992]` from 21 700 evaluations with no sampling and
   `[593.2964, 593.3144]` with 50 000 samples, and for **Leu₃₀ (`1.07·10⁹` assignments)
   `ln Z ∈ [866.6507, 867.3804]` from 174 437 evaluations with no sampling and `[866.9000, 866.9306]`
   with 20 000 samples** — all four brackets contain the coordinator's fitted-chain values
   593.3030 and 866.9139.
5. **What this is and is not.**  The certified bound of the tail is still two to three orders
   of magnitude above the truth (`Γ₆ = 8.0` against a remainder of 0.013 kcal/mol at Leu₁₆); by
   item 2 no analysis that ignores signs can bring it within a factor ten at orders 3–5, and
   at order 6 at most the slack of P3's inequalities (a factor 9 against the best pair-by-pair
   bound) is there to be recovered; the certificates work because this helix ensemble is nearly
   frozen (0.6–0.8 side chains off the anchor on average), so the answer to the brief's
   question is: *no bound of the natural kinds at the orders where it was asked — and a
   certificate all the same, for ensembles that stay near their anchor.*

---

## Notation used throughout

As in P3's report (§2.0).  `X = ∏_i X_i` the product domain of rotamers, `x⁰` an anchor (here
always `argmin E`, found by enumeration), `S(x) = {i : x_i ≠ x⁰_i}`; for a set `T` of sites
`Δ_T g(z; y_T)` the mixed difference, `c_T^anch(F) := sup{|Δ_T F(z; y_T)| : z ∈ X, z_T = x⁰_T, y_T ∈ X_T}`
the **anchored constant** of a function `F` (all contexts, all non-anchor states of `T`);
`d_T(x_T) := Δ_T g(x⁰; x_T)` the anchored terms, `I_M g := Σ_{|U| ≤ M} d_U`.  Atoms `p = 1 … N`
with charges `q_p`.

**The kernel matrix.**  With `b_p = 1/B_p` the inverse Born radius, `ℓ_p = ln B_p` and
`h(w; r) = (r² + e^w e^{−r² e^{−w}/4})^{−1/2}`, put

```
M_pq(x) := h(ℓ_p(x) + ℓ_q(x); r_pq(x))   (p ≠ q),        M_pp(x) := b_p(x)   ( = h(2ℓ_p; 0) ).
g(x) = −(κ/2) Σ_{p,q} q_p q_q M_pq(x)  =  Σ_{p,q} W_pq(x),      W_pq := −(κ/2) q_p q_q M_pq
```

(ordered pairs; the diagonal is P3's *self part*, the off-diagonal part its *cross part*).
**`M(x)` does not depend on the charges**: Born radii are functions of the geometry and of the
radius parameters only.  This is the one structural fact everything in §2 rests on.  My sum
`Σ_{p,q} W_pq` agrees with P3's evaluator `p3core.GBModel.energy` at every state of every
enumerated instance (largest deviation `1.2·10⁻¹¹` kcal/mol; asserted in every run).

---

## 1. What was measured (step 1 of the brief)

**Instances** (all of P3's enumerable helix instances named in the brief, plus Leu₁₂):
Ace-Leu_n-NMe, `n = 6, 8, 12`, τ = 0.60 (two admissible rotamers per site: 64, 256, 4 096
assignments; 126, 164, 240 atoms) and Ace-Ser_n-NMe, `n = 4, 5, 6`, τ = 0.70 (domains
`9·9·6·6 = 2 916`, `17 496`, `104 976`; 56, 67, 78 atoms), α-helix.  Anchor `x⁰ = argmin E`
(enumerated).  For every subset `T` of sites of order 3–5 (3–6 for Leu₁₂) the script
`s1_cancel.py` computes, **by exact enumeration of all states**, the anchored constants
`c_T^anch(F)` of the following pieces `F` of `g = Σ_{p,q} W_pq`, and sums them over the pieces:

| level | pieces `F` | what a bound of that architecture can see |
|---|---|---|
| **total** | `g` itself | everything: this is the truth, `c_T^anch(g)` |
| self, cross | `Σ_p W_pp`; `Σ_{p≠q} W_pq` | P3's split |
| group × all | `Σ_{p∈P} Σ_q W_pq` for each group `P` | all signs for one group |
| **group × group** | `Σ_{p∈P, q∈Q} W_pq` for each ordered pair of groups | signs on both sides of a group pair |
| atom × all | `Σ_q W_pq` for each atom `p` | all signs over the partners of one atom |
| **atom × group** | `Σ_{q∈Q} W_pq` for each atom `p` and group `Q` | **the brief's candidate: signed kernel sums over a neutral group, for one atom** |
| **pair by pair** | every `W_pq` separately | nothing: the least value any term-by-term bound can have (`PP_T` of §2.1) |
| P3 | — | P3's certified `ĉ_T` (`gfbound.GFBound.total(m, T)`), which summed over `T` is its `Γ_m` |

Each level is a sum of exact constants of pieces, hence (triangle inequality) an upper bound
of the truth and the *smallest value a bound can reach that treats the pieces of that level one
at a time*; the levels are nested (`total ≤ group × all ≤ group × group ≤ pair`, `total ≤ atom × all ≤
atom × group ≤ pair`), which the script asserts for every subset.  Four groupings:
**residue** (Ace, each residue, NMe — the only exactly neutral groups: every group has charge
0); **rigid** (per residue its fixed atoms N, H, CA, HA, CB, C, O and its moving side-chain
atoms — the rigid bodies of the rotamer model; they are *not* neutral: −0.184 e and +0.184 e
for leucine); **peptide** (planar units C, O of residue `i` with N, H of residue `i+1`; the rest of
the fixed atoms; the moving side chain); **united** (every heavy atom with its hydrogens,
carbonyl C and O merged; charges up to 0.32 e).  The rows "cross part regrouped" repeat the
group levels for the cross part alone (diagonal `p = q` removed), which is what the brief asked
for literally; with the self terms inside their groups the numbers are 0–35 % smaller.

**Table 1a — sums over all subsets of order `m` of exact anchored constants, kcal/mol**
(`out/tables.md`, block `step1_abs`; "cross regrouped" = cross part alone, signed inside the
groups named; the last column is the range of the true remainder over all states).

| instance (states) | m | subsets | self | cross | **total** | cross regrouped: residue × residue | rigid × rigid | atom × residue | atom × rigid | best pair-by-pair (cross part) | P3's bound (cross part) | P3's bound, all = `Γ_m` | true remainder `g − I_{m−1}g` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leu₆/H τ0.60 (64) | 3 | 20 | 0.597 | 0.684 | **0.268** | 1.91 | 2.27 | 8.69 | 9.96 | 36.3 | 131 | 132 | [−0.019, 0.057] |
| Leu₆/H τ0.60 (64) | 4 | 15 | 0.00696 | 0.0644 | **0.0607** | 0.163 | 0.203 | 0.746 | 0.825 | 2.32 | 12.8 | 12.9 | [−0.030, 0.004] |
| Leu₆/H τ0.60 (64) | 5 | 6 | 6.6·10⁻⁴ | 0.00434 | **0.00418** | 0.00935 | 0.0122 | 0.0341 | 0.0376 | 0.0971 | 0.775 | 0.776 | [−7.4·10⁻⁴, 0.0022] |
| Leu₈/H τ0.60 (256) | 3 | 56 | 1.26 | 1.75 | **1.23** | 5.27 | 6.49 | 25.2 | 28.9 | 104 | 354 | 357 | [−0.067, 0.25] |
| Leu₈/H τ0.60 (256) | 4 | 70 | 0.0161 | 0.291 | **0.286** | 0.697 | 0.884 | 3.08 | 3.43 | 10.1 | 49.2 | 49.3 | [−0.088, 0.012] |
| Leu₈/H τ0.60 (256) | 5 | 56 | 0.00298 | 0.0288 | **0.0292** | 0.0733 | 0.0915 | 0.256 | 0.281 | 0.710 | 4.97 | 4.98 | [−0.0024, 0.0029] |
| Leu₁₂/H τ0.60 (4 096) | 3 | 220 | 2.67 | 4.80 | **3.92** | 15.1 | 19.3 | 74.7 | 85.9 | 305 | 1 028 | 1 034 | [−0.12, 0.78] |
| Leu₁₂/H τ0.60 (4 096) | 4 | 495 | 0.0607 | 1.09 | **1.07** | 2.73 | 3.53 | 11.9 | 13.4 | 39.6 | 188 | 189 | [−0.17, 0.032] |
| Leu₁₂/H τ0.60 (4 096) | 5 | 792 | 0.0115 | 0.175 | **0.176** | 0.414 | 0.522 | 1.44 | 1.58 | 3.97 | 26.9 | 26.9 | [−0.016, 0.0085] |
| Leu₁₂/H τ0.60 (4 096) | 6 | 924 | 1.1·10⁻⁴ | 0.0220 | **0.0220** | 0.0467 | 0.0585 | 0.133 | 0.145 | 0.332 | 2.99 | 2.99 | [−4.2·10⁻⁴, 0.0092] |
| Ser₄/H τ0.70 (2 916) | 3 | 4 | 0.0107 | 0.0616 | **0.0709** | 0.121 | 0.162 | 0.317 | 0.362 | 0.779 | 4.00 | 4.13 | [−0.016, 0.047] |
| Ser₄/H τ0.70 (2 916) | 4 | 1 | 4.6·10⁻⁵ | 1.2·10⁻⁴ | **1.3·10⁻⁴** | 9.5·10⁻⁴ | 0.00131 | 0.00239 | 0.00289 | 0.00614 | 0.0388 | 0.0391 | [−7.9·10⁻⁵, 1.3·10⁻⁴] |
| Ser₅/H τ0.70 (17 496) | 3 | 10 | 0.0264 | 0.109 | **0.126** | 0.286 | 0.383 | 0.757 | 0.877 | 1.91 | 8.72 | 8.98 | [−0.042, 0.049] |
| Ser₅/H τ0.70 (17 496) | 4 | 5 | 3.4·10⁻⁴ | 0.00169 | **0.00179** | 0.00569 | 0.00868 | 0.0137 | 0.0166 | 0.0328 | 0.211 | 0.212 | [−0.0011, 2.2·10⁻⁴] |
| Ser₅/H τ0.70 (17 496) | 5 | 1 | 1.6·10⁻⁷ | 3.0·10⁻⁵ | **3.0·10⁻⁵** | 5.7·10⁻⁵ | 1.1·10⁻⁴ | 1.4·10⁻⁴ | 1.8·10⁻⁴ | 3.0·10⁻⁴ | 0.00238 | 0.00239 | [−3.0·10⁻⁵, 4.8·10⁻⁶] |
| Ser₆/H τ0.70 (104 976) | 3 | 20 | 0.0443 | 0.177 | **0.202** | 0.505 | 0.675 | 1.34 | 1.56 | 3.44 | 16.5 | 17.0 | [−0.066, 0.050] |
| Ser₆/H τ0.70 (104 976) | 4 | 15 | 8.1·10⁻⁴ | 0.00492 | **0.00514** | 0.0143 | 0.0207 | 0.0336 | 0.0402 | 0.0812 | 0.832 | 0.849 | [−0.0016, 5.6·10⁻⁴] |
| Ser₆/H τ0.70 (104 976) | 5 | 6 | 1.7·10⁻⁶ | 8.9·10⁻⁵ | **8.9·10⁻⁵** | 2.3·10⁻⁴ | 3.6·10⁻⁴ | 5.3·10⁻⁴ | 6.6·10⁻⁴ | 0.00123 | 0.0194 | 0.0196 | [−3.1·10⁻⁵, 4.2·10⁻⁵] |

My totals reproduce P3's Table 3.1 where both exist (Leu₆: 0.27 / 0.60 / 0.68, 0.061, 0.0042;
Leu₈: 1.23 / 1.26 / 1.75, 0.29, 0.029) and every `Γ_m` of P3's §3.3 (132, 12.9, 0.776; 357, 49.3,
4.98; 189, 26.9, 2.99; 4.13, 0.0391; 8.98, 0.212, 0.00239; 0.849) — an independent replication of
those entries with my own decomposition of `g`.

**Table 1b — the same as ratios to the truth (the column "total" of Table 1a), self terms kept
inside their groups, and the gains the brief asked about** (`out/tables.md`, block `step1_ratio`).

| instance | m | P3 `Γ_m` | best pair-by-pair | atom × united group | atom × residue | atom × all partners | united × united | rigid × rigid | residue × residue | residue × all | gain: pair-by-pair / (atom × residue) | gain: pair-by-pair / (residue × residue) | slack: P3 / best pair-by-pair |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leu₆/H | 3 | 492 | 139 | 53 | 31 | 20 | 21 | 6.0 | 4.7 | 2.3 | 4.4 | 30 | 3.5 |
| Leu₆/H | 4 | 212 | 39 | 18.2 | 12.2 | 8.3 | 8.2 | 3.2 | 2.5 | 1.6 | 3.2 | 15.2 | 5.5 |
| Leu₆/H | 5 | 186 | 23 | 11.5 | 8.0 | 5.8 | 5.4 | 2.8 | 2.1 | 1.3 | 2.9 | 11.3 | 7.9 |
| Leu₈/H | 3 | 289 | 86 | 34 | 20.0 | 13.0 | 13.1 | 4.1 | 3.1 | 1.7 | 4.3 | 28 | 3.4 |
| Leu₈/H | 4 | 172 | 35 | 16.2 | 10.7 | 7.2 | 7.2 | 3.0 | 2.4 | 1.5 | 3.3 | 14.9 | 4.9 |
| Leu₈/H | 5 | 170 | 24 | 12.4 | 8.7 | 6.0 | 5.8 | 3.0 | 2.4 | 1.5 | 2.8 | 10.2 | 7.0 |
| Leu₁₂/H | 3 | 264 | 79 | 32 | 18.7 | 12.0 | — | 4.1 | 3.0 | 1.7 | 4.2 | 26 | 3.3 |
| Leu₁₂/H | 4 | 177 | 37 | 17.1 | 11.2 | 7.4 | — | 3.3 | 2.5 | 1.5 | 3.3 | 14.8 | 4.7 |
| Leu₁₂/H | 5 | 153 | 23 | 11.6 | 8.1 | 5.4 | — | 2.9 | 2.3 | 1.5 | 2.8 | 9.9 | 6.7 |
| Leu₁₂/H | 6 | 136 | 15.1 | 8.1 | 6.0 | 4.0 | — | 2.7 | 2.1 | 1.4 | 2.5 | 7.1 | 9.0 |
| Ser₄/H | 3 | 58 | 11.4 | 5.5 | 4.5 | 3.4 | 2.6 | 2.0 | 1.6 | 1.2 | 2.5 | 7.1 | 5.1 |
| Ser₄/H | 4 | 297 | 47 | 24 | 18.0 | 10.0 | 12.6 | 9.7 | 6.9 | 3.1 | 2.6 | 6.9 | 6.3 |
| Ser₅/H | 3 | 71 | 15.6 | 7.6 | 6.0 | 4.3 | 3.6 | 2.7 | 2.1 | 1.4 | 2.6 | 7.3 | 4.5 |
| Ser₅/H | 4 | 118 | 18.6 | 10.0 | 7.6 | 4.9 | 5.6 | 4.6 | 3.1 | 1.8 | 2.4 | 5.9 | 6.4 |
| Ser₅/H | 5 | 80 | 10.1 | 6.4 | 4.7 | 3.0 | 4.2 | 3.7 | 1.9 | 1.3 | 2.1 | 5.3 | 7.9 |
| Ser₆/H | 3 | 84 | 17.5 | 8.6 | 6.6 | 4.5 | — | 3.1 | 2.4 | 1.4 | 2.6 | 7.3 | 4.8 |
| Ser₆/H | 4 | 165 | 16.0 | 8.6 | 6.5 | 4.1 | — | 3.9 | 2.8 | 1.6 | 2.5 | 5.8 | 10.3 |
| Ser₆/H | 5 | 221 | 13.9 | 8.1 | 6.0 | 3.6 | — | 4.0 | 2.5 | 1.5 | 2.3 | 5.5 | 15.9 |

("—": not computed, for memory, on the two largest instances.)

*Checks* (`out/tables.md`, block `step1_checks`).  Every number is from full enumeration:
129 804 states in all (64, 256, 4 096, 2 916, 17 496, 104 976).  For every subset the script
asserts the nesting of the levels and that P3's certified bound dominates the exact constants —
`ĉ_T^self ≥ c_T(self)`, `ĉ_T^cross ≥ c_T(cross)`, and, more strongly, P3's self and cross parts `≥` the
sums of the exact constants of the single terms: **121 780 inequality checks, 0 violations.**
The ratio P3's `ĉ_T` / exact `c_T^anch(g)`, subset by subset, ranges from 22 to 2 782; the ratio
`ĉ_T` / (sum of exact term constants `PP_T`) from 2.3 to 62.  (For Leu₁₂ at order 6, P3's bound
was computed only in its closed form `Γ₆`, not subset by subset.)

**Findings** [M].

1. **By the brief's own criterion the candidate route is not alive.**  The signed object of the
   candidate — the sum over the atoms of a group, for one atom — is **2.2–4.4 times** smaller
   than the pair-by-pair sum for the neutral residue groups (2.1–4.2 for the cross part alone,
   1.6–4.4 over all four groupings); the brief asked for 10–100.  Even an *exact* bound of that
   architecture would stay at **6–53 times the truth for leucine** (18–53 at order 3, 11–18 at
   order 4, 8–12 at order 5, 6–8 at order 6) **and 4.5–24 times for serine**.
2. **The cancellation is two-sided and lives at the scale of residues.**  Sums signed on both
   sides are 5–30 times smaller than pair-by-pair for residue × residue (2.7–23 for the rigid
   bodies) and within **1.6–6.9 of the truth**; keeping all signs for one whole residue, 1.2–3.1.
   The smaller the groups, the less they help: united atoms × united atoms are 2.6–21 times the
   truth.  The levels gain a factor 3–7 (partners of one atom), then 2–9 (atoms of a residue),
   then 1.2–3.1 (residues): there is no level at which the sum collapses, hence no small
   parameter to expand in.
3. **Self against cross**, the cancellation P3 described at zeroth order, matters at order 3 for
   leucine (self + cross = 1.9–4.8 times the total) and has disappeared from order 4 on: the
   self part is then at most 16 % of the total for leucine (35 % for serine) and the cross part
   alone equals the total within 8 %.  At the orders that matter the problem is entirely inside
   the cross part.
4. **P3's bound is 3.3–15.9 times the best possible pair-by-pair bound**, and the factor grows
   with the order (leucine: about 3.4, 5, 7, 9 at orders 3–6; serine up to 16).  The best
   pair-by-pair bound itself is 15–139 times the truth for leucine and 10–47 for serine.  So of
   P3's factor 136–492 (leucine) the larger part is intrinsic to treating pairs one at a time,
   and of its factor 58–297 for serine the two parts are comparable.
5. **With the order everything tightens, the truth fastest of all** (Leu₁₂, per order from 3 to
   6: truth ÷3.7, ÷6.1, ÷8.0; best pair-by-pair ÷7.8, ÷10.0, ÷12.0; P3 ÷5.5, ÷7.0, ÷9.0): the
   pair-by-pair optimum approaches the truth slowly (79, 37, 23, 15 times), P3's bound more
   slowly still (264, 177, 153, 136).

---

## 2. A lower bound for pair-by-pair bounds (step 2 of the brief)

### 2.1 Proposition 7 [P] — a bound that does not look at the signs of the charges must hold for every sign pattern

**Setting.**  Fix everything that determines the kernel matrix `M : X → Sym_N` (coordinates of
every (site, state), radius parameters, neck tables).  For a charge vector `c ∈ ℝ^N` let
`g_c := −(κ/2) cᵀ M c`; the function of the report is `g = g_q`.  For a sign pattern
`s ∈ {±1}^N` write `s∘q` for the charges `s_p q_p`: `g_{s∘q}` is the GBn2 energy *of the same
atoms at the same places with some charges reversed* — a legitimate member of the same model
class, with the same Born radii, the same descreening tables and the same derivative
enclosures.  Let `Φ` be any functional of a function on `X` that is to be bounded: e.g.
`Φ_T(g) = c_T^anch(g)` for one subset, `Φ(g) = Σ_{|T| = m} c_T^anch(g)`, or the sup-norm of the
remainder `Φ_m(g) = sup_x |g − I_{m−1} g|(x)`.

**Definition (sign-blind bound).**  A number `β` is a *sign-blind bound of `Φ`* if
`Φ(g_{s∘q}) ≤ β` for every `s ∈ {±1}^N` — i.e. if it is computed from the geometry, the radii and
the **magnitudes** `|q_p|` by an argument that is valid whatever the signs are.

**Definition (term-by-term bound).**  Numbers `B_pq ≥ 0` (`p ≤ q`) with
`(κ/2)·sup|Δ_T M_pp| ≤ B_pp` and `κ·sup|Δ_T M_pq| ≤ B_pq` (suprema over the base points and states
admitted in `Φ_T`), and the bound `β = Σ_{p ≤ q} |q_p q_q| B_pq`: every term of the bound bounds
the corresponding term of `g`.

*Claims.*
(a) *Every sign-blind bound satisfies `β ≥ SB(Φ) := max_s Φ(g_{s∘q})`, and `SB(Φ)` is itself a
sign-blind bound* — the least one.
(b) *Every term-by-term bound is sign-blind, and the least term-by-term bound of `Φ_T` is
`PP_T := Σ_p q_p² (κ/2) sup|Δ_T M_pp| + Σ_{p<q} |q_p q_q| κ sup|Δ_T M_pq|`, the sum of the exact
constants of the single terms.*  Hence `β^{tt}_T ≥ PP_T ≥ SB(Φ_T) ≥ c_T^anch(g)`.
(c) *P3's Theorem 3 is a term-by-term bound* (its `σ_p` carries `q_p²`, its `θ_pq` carries `|q_p q_q|`,
and each bounds its own term).  Hence P3's `ĉ_T ≥ PP_T ≥ SB(Φ_T)`, and its remainder constant
satisfies `Γ_m ≥ max_s sup_x |g_{s∘q} − I_{m−1} g_{s∘q}|(x)` for the same anchor.

*Proof.*  (a) is the definition, read at the maximising `s`.  (b) `Δ_T g_{s∘q} = −(κ/2) Σ_{p,q} s_p s_q q_p q_q Δ_T M_pq`
and the triangle inequality give `|Δ_T g_{s∘q}| ≤ PP_T ≤ β^{tt}_T` for every `s`; the least value of each
`B_pq` is the supremum it must dominate.  (c) by inspection of P3's Theorem 3 and Theorem 5:
neither the tables, nor the oscillations `δ`, nor the derivative enclosures depend on a charge,
and the validity of Theorem 5 does not depend on the choice of the anchor. ∎

*Why this is the right formalisation of "a bound that treats atom pairs one at a time".*  A
**rule** that assigns to every pair a number `B_pq` from the pair's own geometry and its own
radius ranges cannot depend on the sign of any charge.  If the rule is *sound* — if
`Σ |q_p q_q| B_pq` is a valid bound for every assignment of charges to the same atoms, which is
what a proof that never uses a sign establishes — then its output is a sign-blind bound in the
sense above.  (The form `Σ |q_p q_q| B_pq` alone means nothing: `B_pq := |Δ_T g| / Σ|q_p q_q|` has
that form.  What defines the class is that the same number is claimed for all sign patterns.)
The class is strictly larger than the term-by-term bounds: it contains, e.g., every bound through
a matrix norm that is invariant under `M ↦ D M D`, `D = diag(±1)` — the operator norm
`‖Δ_T M‖_op ‖q‖₂²`, any norm of the entrywise absolute values — and it contains `SB` itself.

*What the proposition does **not** cover:* any bound that uses a signed sum of charges —
group sums at a reference, exact evaluations, an expansion carried one order further.  For
those the evidence is §1 and §3.

### 2.2 Theorem 8 [P + M] — numbers on the enumerated helix instances

*For the six enumerated helix instances and the anchor `x⁰ = argmin E`, the script
`s2_signblind.py` exhibits sign patterns `s` for which the reversed-charge system `g_{s∘q}` has, by
exact enumeration of all states, the remainders and anchored constants of Table 2.  By
Proposition 7, **every sign-blind bound** of the quantity in question — every term-by-term
bound, P3's `Γ_m`, any bound through a sign-invariant matrix norm — **is at least the value
found**, hence exceeds the truth by at least the factor printed in bold.*  Three quantities:

* **(C) the remainder itself**, `sup_x |g − I_{m−1} g|(x)`: one pattern per order, found by a
  1-flip local search on the quadratic form `sᵀ D (M − I_{m−1}M)(x*) D s`, `D = diag|q|`, at up to
  three states `x*` (thirteen for Leu₁₂) from 32 starting patterns each, and then evaluated at
  *all* states;
* **(B) the sum of anchored constants** `Σ_{|T|=m} c_T^anch`: the best single pattern among those
  tried (the pattern of (C), and all charges positive);
* **(A) the sum of per-subset optima** `Σ_T max_s c_T^anch(g_{s∘q})`: a separate search for each
  subset.  (A) is the relevant lower bound for a bound that is built subset by subset, as P3's
  is; (B) and (C) hold for any sign-blind bound.  (A) `≥` (B) by definition.

**Table 2 — what every sign-blind bound must pay (kcal/mol; ratios in bold)** (`out/tables.md`,
block `step2`).  † : no per-subset search at that order (Leu₁₂, orders 5 and 6); the entry is the
best single pattern.

| instance | m | **remainder** `sup_x |g − I_{m−1}g|`: truth | all charges positive | sign pattern found | **(C) every sign-blind bound of the remainder / truth ≥** | P3's `Γ_m` | `Γ_m` / (pattern found) | **sums over subsets** `Σ_T c_T`: truth | (B) best single pattern | (A) `Σ_T` best pattern per subset | best pair-by-pair `Σ_T PP_T` | **(B) / truth ≥** | **(A) / truth ≥** | P3 / (A) ≤ | pair-by-pair / (A) ≤ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leu₆/H | 3 | 0.0569 | 3.60 | 8.68 | **153** | 132 | 15.2 | 0.268 | 11.3 | 21.2 | 37.3 | **42** | **79** | 6.2 | 1.8 |
| Leu₆/H | 4 | 0.0301 | 0.574 | 0.685 | **23** | 12.9 | 18.8 | 0.0607 | 0.780 | 1.41 | 2.34 | **12.8** | **23** | 9.1 | 1.7 |
| Leu₆/H | 5 | 0.00222 | 0.00458 | 0.0367 | **16.5** | 0.776 | 21 | 0.00418 | 0.0468 | 0.0701 | 0.0979 | **11.2** | **16.8** | 11.1 | 1.4 |
| Leu₈/H | 3 | 0.249 | 6.25 | 17.9 | **72** | 357 | 20.0 | 1.23 | 29.0 | 59.2 | 106 | **24** | **48** | 6.0 | 1.8 |
| Leu₈/H | 4 | 0.0882 | 1.80 | 2.10 | **24** | 49.3 | 23 | 0.286 | 2.83 | 6.06 | 10.1 | **9.9** | **21** | 8.1 | 1.7 |
| Leu₈/H | 5 | 0.00286 | 0.0182 | 0.108 | **38** | 4.98 | 46 | 0.0292 | 0.200 | 0.449 | 0.714 | **6.9** | **15.4** | 11.1 | 1.6 |
| Leu₁₂/H | 3 | 0.779 | 17.4 | 39.9 | **51** | 1 034 | 26 | 3.92 | 74.8 | 168 | 310 | **19.1** | **43** | 6.1 | 1.8 |
| Leu₁₂/H | 4 | 0.174 | 5.13 | 5.97 | **34** | 189 | 32 | 1.07 | 9.97 | 22.6 | 39.9 | **9.4** | **21** | 8.3 | 1.8 |
| Leu₁₂/H | 5 | 0.0158 | 0.0347 | 0.321 | **20** | 26.9 | 84 | 0.176 | 0.795 | 0.909 † | 3.99 | **4.5** | **5.2** † | 30 | 4.4 |
| Leu₁₂/H | 6 | 0.00919 | 0.00324 | 0.0347 | **3.8** | 2.99 | 86 | 0.0220 | 0.0780 | 0.0826 † | 0.332 | **3.5** | **3.8** † | 36 | 4.0 |
| Ser₄/H | 3 | 0.0468 | 0.198 | 0.201 | **4.3** | 4.13 | 21 | 0.0709 | 0.443 | 0.452 | 0.809 | **6.3** | **6.4** | 9.1 | 1.8 |
| Ser₄/H | 4 | 1.3·10⁻⁴ | 0.00139 | 0.00252 | **19.1** | 0.0391 | 15.5 | 1.3·10⁻⁴ | 0.00252 | 0.00252 | 0.00622 | **19.1** | **19.1** | 15.5 | 2.5 |
| Ser₅/H | 3 | 0.0491 | 0.245 | 0.268 | **5.5** | 8.98 | 33 | 0.126 | 1.05 | 1.12 | 1.97 | **8.3** | **8.9** | 8.0 | 1.8 |
| Ser₅/H | 4 | 0.00114 | 0.00382 | 0.00460 | **4.0** | 0.212 | 46 | 0.00179 | 0.00945 | 0.0142 | 0.0333 | **5.3** | **7.9** | 15.0 | 2.3 |
| Ser₅/H | 5 | 3.0·10⁻⁵ | 4.4·10⁻⁵ | 1.2·10⁻⁴ | **4.0** | 0.00239 | 19.7 | 3.0·10⁻⁵ | 1.2·10⁻⁴ | 1.2·10⁻⁴ | 3.0·10⁻⁴ | **4.0** | **4.0** | 19.7 | 2.5 |
| Ser₆/H | 3 | 0.0656 | 0.446 | 0.535 | **8.2** | 17.0 | 32 | 0.202 | 1.97 | 2.00 | 3.54 | **9.7** | **9.9** | 8.5 | 1.8 |
| Ser₆/H | 4 | 0.00163 | 0.00527 | 0.00976 | **6.0** | 0.849 | 87 | 0.00514 | 0.0241 | 0.0354 | 0.0825 | **4.7** | **6.9** | 24 | 2.3 |
| Ser₆/H | 5 | 4.2·10⁻⁵ | 1.3·10⁻⁴ | 1.4·10⁻⁴ | **3.4** | 0.0196 | 136 | 8.9·10⁻⁵ | 2.8·10⁻⁴ | 4.8·10⁻⁴ | 0.00123 | **3.2** | **5.4** | 41 | 2.6 |

*Checks.*  (i) Every "pattern found" is an exact evaluation at all states.  (ii) For every
subset the chain `truth ≤ (A) ≤ PP_T ≤ ĉ_T` (P3) and `c_T(g_{|q|}) ≤ ĉ_T` is asserted: 16 296 checks,
0 violations.  (iii) **A new test of P3's theorem**: being sign-blind, `Γ_m` must bound the
remainder of *every* sign-reversed system at *every* state.  Checked for the true signs, all
charges positive and the pattern found, at every state, order by order: **1 171 776 state checks,
0 violations**; the ratio `Γ_m / sup|remainder|` ranges from 15.2 (the pattern found for Leu₆ at
order 3) to 2 315 (the true charges, Leu₆, order 3).

*Reading.*
1. **At orders 3, 4, 5, for leucine on the helix, no sign-blind bound of the remainder is within
   a factor ten of the truth**: at least 153, 23, 16.5 (Leu₆), 72, 24, 38 (Leu₈), 51, 34, 20
   (Leu₁₂).  The same holds for any bound assembled subset by subset at orders 3 and 4 (column
   (A): 21–79) and, where the per-subset search was run, at order 5 (15–17).
2. **At order 6 the question is open.**  On Leu₁₂ the strongest pattern I found gives 3.8 (a
   second search with 13 starting states and 32 starts each found nothing better), while the
   best pair-by-pair bound is 15 times the sum of constants and 36 times the remainder: the
   least sign-blind bound lies in `[3.8, 36]` times the truth there.  The loss of the sign-blind
   class decreases with the order (Leu₁₂: 51, 34, 20, ≥ 3.8), as fewer and fewer terms are left
   to cancel.  P3's actual bound at order 6 is 325 times the true remainder.
3. **For serine on the helix the theorem excludes little** (3.4–19; making all charges positive
   already gives 1.5–11 times the true remainder and the search adds little: the true charges
   cancel only mildly there), while P3's bound is 15–136 times the pattern found: there the
   slack of the inequalities is the larger part.
4. **Term-by-term bounds are nearly optimal among sign-blind ones.**  Where the per-subset
   search was run, the pair-by-pair optimum is within a factor 1.4–2.6 of the lower bound (A):
   for nearly every subset there is a sign pattern that realises most of the sum of absolute
   values.  Refinements that stay sign-blind (operator norms, semidefinite relaxations) can gain
   at most this factor over the best pair-by-pair bound.
5. **P3's bound is 6–41 times the lower bound (A)** and 15–136 times the pattern found for the
   remainder: an order of magnitude of it is slack, the rest is the price of the class.

### 2.3 Theorem 9 [P; every claim checked numerically on the family] — an explicit family on which the loss is exact and grows with the number of partners in range

**The class.**  Call *GB-type* any function `g = −(κ/2) Σ_{p,q} q_p q_q M_pq(x)` on a finite product
domain with `M_pp = b_p(x) > 0`, `M_pq = h(−ln b_p(x) − ln b_q(x); r_pq)`, `r_pq > 0` symmetric.  P3's
functions are of this type with `b_p = b_p(I_p)`, `I_p` additive in the sites; P3's Theorem 3, and
every analysis that works from descreening tables and ranges, applies to arbitrary additive
tables and to an arbitrary symmetric array `r_pq` (it never uses that the `r_pq` are distances
between points of `ℝ³`).

**The family `𝔉_N(r)`.**  `N` even; charges `q_p = (−1)^p q₀`; all pair distances equal, `r_pq = r`;
one common inverse Born radius, `b_p(x) = b(x)` for all `p`, `b_min ≤ b ≤ b_max`.
`N = 2` is a bond.  `N = 4` is a regular tetrahedron of edge `r`: **two neutral dipoles of
length `r`, crossed at right angles, their midpoints `r/√2` apart**; in OpenMM's GBn2 the four
Born radii are equal whenever the four atoms have the same parameters and the rest of the
system is invariant under the tetrahedral group (built and checked in `s2_family.py`, part C:
uncharged shells as sites, the four descreening integrals agree to `4·10⁻¹⁵ nm⁻¹`).  `N > 4`
is not realisable by points of `ℝ³`; it is a member of the GB-type class.

Let `ψ(u) := (u + e^{−u/4})^{−1/2}`, so that `h = b ψ(r² b²)`, and `χ_r(b) := b − h = b (1 − ψ(r² b²))`.
For a set `T` of `m` sites write `Δ` for any mixed difference `Δ_T(·)(z; y_T)`.

*Claims.*
(i) For every sign pattern `s`, with `k := Σ_p s_p`:
`g_{s∘q} = −(κ/2) q₀² [N b + (k² − N) h] = −(κ/2) q₀² [k² b − (k² − N) χ_r(b)]`.
(ii) The truth (`k = 0`) is `Δ g = −(κ/2) q₀² N Δχ_r`; with all charges positive (`k = N`)
`Δ g_+ = −(κ/2) q₀² [N² Δb − N(N−1) Δχ_r]`.
(iii) Hence every sign-blind bound `β` of `|Δ_T g|` on this instance satisfies

```
β / |Δ_T g|  ≥  |N² Δb − N(N−1) Δχ_r| / (N |Δχ_r|)  ≥  N · |Δb| / |Δχ_r| − (N − 1).
```

(iv) `0 ≤ 1 − ψ(u) ≤ (3/8) u` for all `u ≥ 0`, so `0 ≤ χ_r(b) ≤ (3/8) r² b³`,
`|Δχ_r| ≤ 2^{m−1}·(3/8)·r² b_max³`, and

```
β / |Δ_T g|  ≥  (8/3)·2^{1−m}·N·|Δ_T b| / (r² b_max³) − (N − 1).
```

*For a fixed radius function with `Δ_T b ≠ 0` the factor grows linearly in `N` — the number of
partners of an atom inside the range of the kernel, i.e. like the square root of the number
`N(N−1)/2` of pairs — and like `(B/r)²` as the cluster shrinks inside the Born radius.*
(v) The least term-by-term bound is `PP = (κ/2) q₀² [N |Δb| + N(N−1) |Δh|]`: it has `N(N−1)/2`
pair terms and `N` self terms where the truth, `(κ/2) q₀² N |Δχ_r|`, is `N/2` times the response of one
bond.

*Proof.*  (i) `Σ_{p≠q} s_p s_q = k² − N`.  (ii) by (i).  (iii) Proposition 7(a) with `s ≡ +1`, then
`|a − c| ≥ |a| − |c|`.  (iv) `ψ ≤ 1` because `u + e^{−u/4} ≥ u + 1 − u/4 ≥ 1`.  For `u ≥ 8/3` the claim
`ψ(u) ≥ 1 − (3/8)u` is trivial (the right side is `≤ 0`).  For `0 ≤ u < 8/3` it is equivalent to
`(u + e^{−u/4})(1 − (3/8)u)² ≤ 1`; with `e^{−u/4} ≤ 1 − u/4 + u²/32` the left side is at most
`(1 + (3/4)u + u²/32)(1 − (3/4)u + (9/64)u²) = 1 − (25/64)u² + (21/256)u³ + (9/2048)u⁴`, which is `≤ 1`
iff `168u + 9u² ≤ 800`, true for `u ≤ 8/3` (`448 + 64 = 512`).  A mixed difference of order `m` of a
function with values in `[0, c]` is a sum of `2^{m−1}` values minus `2^{m−1}` values, hence at most
`2^{m−1} c` in modulus.  (v) by definition. ∎

*Remark (clusters that can be built) [P; checked in `s2_family.py`, part D].*  For any neutral
set of charges (`Σ q_p = 0`) at points `r_p` with a common inverse Born radius `b(x)`, using
`(3/8)u − (27/128)u² ≤ 1 − ψ(u) ≤ (3/8)u` and `Σ_{p≠q} q_p q_q |r_p − r_q|² = −2|μ|²`, `μ := Σ_p q_p r_p`:

```
g(x) = −(3κ/8) |μ|² b(x)³ + E(x),        |Δ_T E| ≤ (κ/2)·2^{m−1}·(27/128)·b_max⁵ · Σ_{p≠q} |q_p q_q| r_pq⁴,
```

while the all-positive pattern gives `|Δ_T g_+| ≥ (κ/2) [ (Σ|q_p|)² |Δ_T b| − 2^{m−1}(3/8) b_max³ Σ_{p≠q}|q_p q_q| r_pq² ]`.
So inside the Born radius the truth is the response of the *dipole moment* of the cluster — of
order `N` for incoherently oriented bonds, of order one for compensated ones — and every
sign-blind bound is of order `(Σ|q_p|)² ~ N²`.  (The lower inequality for `ψ`:
`ψ ≤ (1 + (3/4)u)^{−1/2} ≤ 1 − (3/8)u + (27/128)u²`, since `e^{−u/4} ≥ 1 − u/4` and
`(1+y)^{−1/2} ≤ 1 − y/2 + (3/8)y²` for `y ≥ 0`.)

*Honest limit of the family.*  It isolates one mechanism — a neutral cluster smaller than its
Born radius — and there the loss is unbounded.  In the peptide this mechanism is only part of
the story: the Born radii inside a group differ by a factor two and groups are as large as
the range of the kernel (§1).  The theorem shows that the class of sign-blind bounds has no
uniform constant; how much the class loses on the real instances is Theorem 8.

*Numerical check* (`s2_family.py`, 0.6 s; **6 811 checks, 0 violations**).  The radius function
is real: `b(I)` is the GBn2 rescaling of a backbone carbonyl carbon, `I = I₀ + Σ_{i∈T} a_i x_i` with
`I₀ = 11.52 nm⁻¹` and the one-site changes `a_i` (`−0.72 … +0.69 nm⁻¹`) read from the descreening
tables of that atom in Leu₈/H; `B = 0.34–0.47 nm`; `q₀ = 0.5 e`.

* (F1) the two inequalities for `ψ` on a grid of 600 001 points of `[0, 60]`: no violation.
* Part B, the equidistant family, `m = 3, 4, 5`, seven distances, `N = 2 … 64`: the closed form (i)
  against all `2^N` sign patterns for `N ≤ 8` (and (ii), (iii), (iv), (v) for all `N`); the maximum
  over sign patterns is attained by the formula's best `k`.  Ratio (best sign pattern)/truth:

| `r` (nm) | m | `N = 2` (a bond) | `N = 4` (two crossed dipoles) | `N = 16` | `N = 64` | bound (iii) for `N = 4` |
|---|---|---|---|---|---|---|
| 0.050 | 3 | 170 | 339 | 1 354 | 5 413 | 339 |
| 0.123 (a C=O bond) | 3 | 21.5 | 42.1 | 165 | 658 | 42.1 |
| 0.150 | 3 | 13.0 | 25.1 | 97 | 386 | 25.1 |
| 0.300 | 3 | 2.1 | 3.2 | 9.9 | 37 | 3.2 |
| 0.123 | 4 | 6.9 | 14.8 | 62 | 252 | 8.8 |
| 0.123 | 5 | 9.3 | 17.6 | 67.5 | 267 | 17.6 |

  The growth is linear in `N` and like `(B/r)²` as claimed; at `r` comparable to `B` the factor is
  of order one (and bound (iii) is then empty: it can be negative).  Over the 111 cases of part
  B in which bound (iii) is positive the ratio (exact factor)/(bound) lies between 1.0 (the
  bound is attained whenever `Δb` and `Δχ_r` have the sign relation of the reverse triangle
  inequality) and 15.8.
* Part C, the `N = 4` member **built with OpenMM's own descreening integrals** (P3's
  `GBModel._H`: a tetrahedron of four identical charged atoms, a static tetrahedrally symmetric
  bath of 38 uncharged atoms, and as sites five symmetric shells of uncharged atoms that move
  between two radii): the four descreening integrals agree to `4·10⁻¹⁵ nm⁻¹`, `B = 0.35–0.47 nm`, and
  at `r = 0.123 nm` the best sign pattern exceeds the truth by **44.6, 13.8, 25.8** for `m = 3, 4, 5`
  (bound (iii): 44.6, 7.8, 25.8).  The pair-by-pair optimum equals the best sign pattern in 11 of
  the 12 cases run.
* Part D, the Remark: 240 random neutral clusters (`N = 4 … 32`, radius 0.03–0.25 nm): the
  dipole formula with its error bound and the lower bound for all charges positive hold in all
  of them; (all positive)/truth is between 6 and `1.6·10⁴` in the sixteen cases printed.
* Part E, **the family the brief named — two neutral dipoles (bond 0.123 nm, ±0.5 e) at distance
  `R`** with a common Born radius, `m = 3`, best of the 16 sign patterns over the truth: parallel
  dipoles 16, 14, 21, 29, 25, 22 at `R = 0.2, 0.3, 0.5, 0.8, 1.2, 2.0 nm`; antiparallel 108, 3 851,
  35, 28, 24, 22.  For `R` beyond the range of the kernel the two dipoles decouple and the factor
  is that of one bond (21.5); inside the range it depends on the orientation and is unbounded
  where the true dipole–dipole response changes sign (`R ≈ 0.3 nm`, antiparallel).

### 2.4 Proposition 10 [P; checked at every state] — the remainder identity for an arbitrary down-closed family of evaluated subsets

(Not asked for by the brief; needed in §3.3, and a strict generalisation of P3's Proposition 1.)

*Let `𝒟` be a down-closed family of subsets of the sites (`∅ ∈ 𝒟`; subsets of members are
members), and `Thr(𝒟) := {T ∉ 𝒟 : T ∖ {min T} ∈ 𝒟}` its **threshold sets**.  For every function
`g`, anchor `x⁰` and state `x`, with `S = S(x)`,*

```
g(x) − Σ_{U ∈ 𝒟, U ⊆ S} d_U(x_U)  =  Σ_{T ∈ Thr(𝒟), T ⊆ S} Δ_T g(z^{T,x}; x_T),     z^{T,x}_i = x_i (i < min T),  x⁰_i (otherwise),
```

*hence `|g(x) − Σ_{U∈𝒟, U⊆S} d_U(x_U)| ≤ Σ_{T ∈ Thr(𝒟), T ⊆ S} c_T^anch`.*  For `𝒟 = {|U| < m}` the
threshold sets are the `m`-subsets and this is P3's Proposition 1.

*Proof.*  By the context expansion (P3, proof of Proposition 1, step (a)) `g(x) = Σ_{U ⊆ S} d_U(x_U)`,
so the left side is `Σ_{U ⊆ S, U ∉ 𝒟} d_U`.  Take `U ∉ 𝒟`, `U = {u_1 < … < u_s}`, and its suffixes
`U_j := {u_j, …, u_s}`, `U_{s+1} = ∅`.  The suffixes increase as `j` decreases, `∅ ∈ 𝒟`, `U_1 = U ∉ 𝒟`, and
`𝒟` is down-closed, so there is exactly one `j*` with `U_{j*} ∉ 𝒟` and `U_{j*+1} ∈ 𝒟`.  Put
`T(U) := U_{j*}`: it is a threshold set, and `U = T ∪ U′` with `U′ ⊆ V_T := {i ∈ S : i < min T}`.
Conversely, if `T ⊆ S` is a threshold set and `U′ ⊆ V_T`, then `U := T ∪ U′ ∉ 𝒟` (else `T ∈ 𝒟`), the
suffixes of `U` that lie inside `T` are the suffixes of `T`, and so `T(U) = T`.  Thus the sets
`U ⊆ S` outside `𝒟` are partitioned into the intervals `{T ∪ U′ : U′ ⊆ V_T}`, and
`Σ_{U′ ⊆ V_T} d_{T∪U′} = Δ_T g(z^{T,x}; x_T)` by the context expansion with base `x⁰` and `V = V_T`. ∎

*Checks* (`s3_locality.py`, part (a)).  Both sides of the identity were evaluated at every
state for seven to nine families each (all windows `w = 1 … n−1` with all pairs added; the balls
`|U| ≤ 2, 3, 4`; one mixed family) on a random function on a `3×2×4×2×3` grid, on GBn2 of Leu₆/H
(64 states) and of Ser₄/H (2 916 states): **22 140 (state, family) checks, largest deviation
`7·10⁻¹⁴` kcal/mol, 0 violations**.  The bound with exact anchored constants over the threshold
sets: 20 988 checks, 0 violations; bound / |left side| between 1.0 (attained) and `2·10⁵`.

---

## 3. The signed bound (step 3 of the brief): not started, and why

### 3.1 The decision

The brief made step 3 conditional on step 1: "if the group sums are already 10–100 times
smaller than the pair-by-pair sums of absolute values, the route is alive."  Measured (§1):
the object the candidate route keeps signed — for one atom, the sum over the atoms of a group —
is **1.6–4.4 times** smaller than the pair-by-pair sum; only sums that are signed on *both*
sides (residue × residue) are 5–30 times smaller.  I therefore did not build the bound of
step 3.  Two statements make the decision more than a judgement.

### 3.2 Proposition 11 [P; checked at every (T, y_T, context)] — a signed term at the reference buys nothing that the next order does not buy

*For every function `g` on `X`, anchor `x⁰`, subset `T` and state `y_T`:*

```
sup_z |Δ_T g(z; y_T)|   ≤   |d_T(y_T)|  +  Σ_{j ∉ T} c^anch_{T ∪ {j}},                                         (*)
Σ_{|T| = m} c_T^anch      ≤   Σ_{|T| = m} max_y |d_T(y)|  +  (m + 1) · Σ_{|T′| = m+1} c^anch_{T′}.                    (**)
```

*Proof.*  Fix `T`, `y_T` and regard `F(u) := Δ_T g((u, x⁰_T); y_T)` as a function of the other
sites.  P3's Proposition 1 at order 1 for `F` with anchor `x⁰_{−T}` gives
`F(u) − F(x⁰_{−T}) = Σ_{j ∈ S(u)} Δ_j F(·; u_j)`, and `Δ_j F = Δ_{T∪{j}} g` is a mixed difference of `g`
between anchor states and other states, in some context: `|Δ_j F| ≤ c^anch_{T∪{j}}`.  `F(x⁰_{−T}) = d_T(y_T)`.
Summing (*) over `T` counts every `(m+1)`-set `m + 1` times. ∎

*Reading.*  The first term of (*) is exactly what "keep the signed sum at a reference"
means: the exact, fully signed value of the mixed difference in the anchor context.  Getting
it for all `T` of order `m` costs the values of `g` on the Hamming ball of radius `m` — the
evaluations of P3's recipe at order `m + 1`.  (An analytic substitute — the signed leading
Taylor term at reference Born radii — needs no energy evaluation but the same number
`C(n,m)(k−1)^m` of signed `O(N²)` sums, and adds its own remainder.)  The second term is where
uniformity over contexts is paid, and it is paid at order `m + 1`, sign-blind, `m + 1` times.
With the same evaluations P3's recipe at order `m + 1` puts the `d_T` into the model exactly
and pays `Γ_{m+1}` once.  So a certificate "signed at the reference, term by term for the rest"
is dominated by the next order of the plain recipe.  Numbers [M, `s4_refbound.py`; kcal/mol]:

| instance | m | truth `Σ_T c_T^anch` | signed reference terms `Σ_T max|d_T|` | right side of (**) with exact constants | **certified version** `Σ_T max|d_T| + (m+1) Γ_{m+1}` | P3's `Γ_m` (no evaluation beyond the ball of radius `m−1`) | P3's `Γ_{m+1}` (same evaluations as the certified version) |
|---|---|---|---|---|---|---|---|
| Leu₆/H | 3 | 0.268 | 0.165 | 0.408 | **51.7** | 132 | 12.9 |
| Leu₆/H | 4 | 0.0607 | 0.0507 | 0.0716 | **3.93** | 12.9 | 0.776 |
| Leu₈/H | 3 | 1.23 | 0.749 | 1.89 | **198** | 357 | 49.3 |
| Leu₈/H | 4 | 0.286 | 0.236 | 0.381 | **25.1** | 49.3 | 4.98 |
| Ser₄/H | 3 | 0.0709 | 0.0706 | 0.0711 | **0.227** | 4.13 | 0.0391 |
| Ser₅/H | 3 | 0.126 | 0.122 | 0.130 | **0.972** | 8.98 | 0.212 |
| Ser₅/H | 4 | 0.00179 | 0.00172 | 0.00187 | **0.0137** | 0.212 | 0.00239 |
| Ser₆/H | 3 | 0.202 | 0.193 | 0.214 | **3.59** | 17.0 | 0.849 |
| Ser₆/H | 4 | 0.00514 | 0.00497 | 0.00542 | **0.103** | 0.849 | 0.0196 |

The inequalities (*) and (**) were checked for every `(T, y_T)` against the supremum over all
contexts on the five instances: **59 084 checks, 0 violations**, bound/exact between 1.0 and
`1.8·10³`.  With exact higher constants (**) is within a factor 1.0–1.5 of the truth — the signed
reference terms *are* most of the truth.  The certified version is 1.8–3.3 times better than
`Γ_m` for leucine (4.7–18 for serine) and 4–6 times *worse* than `Γ_{m+1}`, which costs the same
evaluations.

### 3.3 A route I tried and abandoned: exactness inside a window, bounds only for what is non-local

If cancellation can only be seen by evaluating, evaluate everything that is local, and bound
only non-local subsets, whose bounds carry the smallness of distant descreening.  Proposition 10
makes this precise: with `𝒟_w` = all pairs and all subsets of sequence diameter `≤ w`, the model
`Σ_{U ∈ 𝒟_w} d_U` is an exact banded function (transfer matrix over `k^w` states) and the tail is a
sum over threshold sets, every one of which contains two sites more than `w` apart.  It fails
on the numbers [M, `s3_locality.py`; exact constants by enumeration, P3's bound per subset]:

| triples whose first and last site are `≥ d` residues apart | Leu₁₂/H: number | exact `Σ c_T^anch` | P3's `Σ ĉ_T` | Leu₁₆/H: number | exact `Σ c_T^anch` | P3's `Σ ĉ_T` |
|---|---|---|---|---|---|---|
| all (`d = 2`) | 220 | 3.92 | 1 034 | 560 | 7.45 | 1 819 |
| `d = 5` | 168 | 2.57 | 456 | 484 | 5.32 | 910 |
| `d = 8` | 80 | 0.383 | 98.4 | 336 | 1.39 | 271 |
| `d = 9` | 52 | 0.250 | 30.9 | 280 | 1.02 | 123 |
| `d = 11` | 10 | 0.035 | 4.12 | 170 | 0.423 | 43.1 |
| `d = 13` | — | — | — | 76 | 0.117 | 7.79 |
| `d = 15` | — | — | — | 14 | 0.0147 | 0.832 |

(kcal/mol; fourth-order subsets of Leu₁₂/H with `d ≥ 9`: exact 0.165, P3 16.3.)  A window of nine
residues on a sixteen-residue helix still leaves 280 triples outside whose certified bounds
add up to 123 kcal/mol (their exact constants to 1.0 kcal/mol); the two most distant side
chains of the chain, 22 Å apart, still take part in triples with exact constants of up to
`5·10⁻³` kcal/mol and certified bounds of 0.01–0.2 kcal/mol each.  The many-body terms of GBn2 are
long-ranged in the sequence — the descreening integrals decay like `r⁻⁴`, not exponentially —
and with a sign-blind tail the window would have to be the whole chain.  Proposition 10 is
correct and unused.  (The sum over *all* triples reproduces P3's `Γ₃ = 1 819` kcal/mol and P2's
measured `Σ c_ijk = 7.4` kcal/mol for Leu₁₆/H.)

### 3.4 What I did instead: the existing recipe at order 6 with the floor as a function

*Why.*  §1, §2 and §3.2 close the routes by which a bound could see the cancellation at a
fixed order.  What is left is the *form* of the certificate.  P3 showed on extended backbones
that a floor which is a function — site penalties `γ_i` paid only where `x_i ≠ x⁰_i` — is cheaper
by orders of magnitude than the constant `Γ_m`, because the ensemble rarely leaves the
neighbourhood of the anchor.  Its negative statement for the helix (its N2: "the recipe fails at
every affordable order", `e^{βΓ₆} ≈ e^{13.5}` for Leu₁₆) is about the constant bound; with site
penalties it ran the helix only up to eight residues and order 5.  The combination "order 6 +
site penalties + helix" was not run.  I ran it — P3's pipeline unchanged
(`floor_p3copy.py` is a verbatim copy of `ws_P3/run_floor.py` with one added import that
redirects the cache; `diff` confirms it), so every guarantee below is **P3's Theorem 5**, with
its paper proofs, its code and its floating-point allowances; what is mine is the choice of
regime and the checks.

**Table 4 — P3's pipeline, Leu on the helix (τ 0.60, two rotamers per site), truncation order 6,
site penalties; band of the pairwise models `w = n − 1` (all pairs) up to twenty residues, `w = 20`
for Leu₃₀** (`run_floor_helix.sh`, `run_floor_L30.sh`; logs `logs/floor_L<n>_H_m6_siteres.log`):

| instance | assignments | ball of radius 5: evaluations of `g` (share of the domain) | `Γ₆` (kcal/mol); largest site penalty `γ_i` (`k_BT`) | **deterministic bracket of `ln Z(E)`** (no sampling) | width (nats) | exact `ln Z(E)` | sandwich `m₋ ≤ E ≤ m₊`: violations / states checked | cost number `Z(m₋)/Z(E) − 1` | **Hoeffding bracket, δ = 0.05** (samples) | width | Bennett bracket with certified `b`, `s²`: width | sites off the anchor (mean under `π_{m₋}`); distinct sampled states | wall time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leu₁₂/H | 4 096 | 1 586 (38.7 %) | 2.988; 0.56 | [374.2091, 374.5277] | 0.319 | 374.345343 | 0 / 4 096 | 0.200 | [374.3309, 374.3540] (20 000) | 0.0231 | 0.193 | 0.61; 10 | 27 s |
| Leu₁₆/H | 65 536 | 6 885 (10.5 %) | 8.032; 1.23 | [483.6408, 484.1640] | 0.523 | 483.846587 | 0 / 65 536 | 0.374 | [483.8328, 483.8592] (20 000) | 0.0264 | 0.473 | 0.69; 10 | 162 s |
| Leu₂₀/H | 1 048 576 | 21 700 (2.07 %) | 14.479; 1.80 | [593.0653, 593.6992] | 0.634 | not enumerated; coordinator's fitted chain: 593.3030 ± 0.0001 | not enumerable in one run; `E ≥ m₋` at all 50 000 samples | — | [593.2964, 593.3144] (50 000) | 0.0180 | 0.639 | 0.74; 21 | 252 s |
| **Leu₃₀/H** | **1 073 741 824** | 174 437 (0.0162 %) | 32.674; 2.67 | **[866.6507, 867.3804]** | 0.730 | not enumerable; coordinator's fitted chain: 866.9139 ± 0.00003 | not enumerable; `E ≥ m₋` at all 20 000 samples | — | **[866.9000, 866.9306]** (20 000) | 0.0306 | 0.865 | 0.79; 19 | 694 s + 1 280 s for the ball |

For comparison, P3's own run of Leu₁₂/H at the same order with the *constant* bound
(`ws_P3/out/floor_L12_H_t0.60_gbn2_m6.json`): cost number 151, deterministic bracket 10.0 nats,
Hoeffding bracket 11.7 nats, the same exact `ln Z = 374.3453434`.

*Checks of the sandwich by enumeration* (done by the pipeline itself): `m₋ ≤ E` and `E ≤ m₊` at
each of the 4 096 + 65 536 states — **139 264 state checks, 0 violations**.  Largest `E − m₋`:
5.12 and 12.00 kcal/mol, largest `m₊ − E`: 4.33 and 10.77, against the certified
`max(m₊ − m₋) = 9.45` and 22.77; smallest `E − m₋`: `10⁻⁷` (at the anchor).  The exact remainder
`g − I₅g` lies in `[−4.2·10⁻⁴, 9.2·10⁻³]` and `[−1.2·10⁻³, 1.34·10⁻²]` kcal/mol where the certificate
allows `Σ_{i∈S(x)} γ_i ≤ Γ₆ = 2.99` and 8.03.  The transfer-matrix `ln Z(m₋)` equals the enumerated
one to `2·10⁻¹³` and `6·10⁻¹³`; the exact `ln Z(E)` lies in the deterministic, the Hoeffding and
the Bennett bracket in both runs.

*Reading.*
1. **The helix is certified at twelve, sixteen, twenty and thirty residues.**  Where the domain
   can be enumerated the sandwich holds at every state and the exact `ln Z` lies in every
   bracket; at sixteen residues the pipeline's own enumeration gives `ln Z = 483.846587`, the
   coordinator's 483.8466 of addendum A17 (10), by different code.  At twenty residues
   (`1.05·10⁶` assignments, 2 % of them evaluated) and at **thirty residues (`1.07·10⁹`
   assignments, 0.016 % of them evaluated)** the deterministic brackets need no random number and
   contain the coordinator's uncertified fitted-chain values (593.3030; 866.9139); the sampled
   brackets, 0.018 and 0.031 nats wide, contain them too.  This is the step the brief called
   step 4 — one helix instance beyond enumeration against the fitted chain — reached without
   the signed bound of step 3.  The anchor is the certified minimiser in all four runs
   (`min m₋ ≤ min E ≤ E(x⁰)` with `E(x⁰) − min m₋ = 10⁻⁷` kcal/mol, the floating-point allowance of
   one evaluation).
2. **Nothing about the tail bound has improved.**  `Γ₆` is the same sign-blind number as in P3's
   table (2.99, 8.03 kcal/mol) — 325 and 600 times the true remainder (0.0092 and 0.0134
   kcal/mol).  The constant bound costs `e^{βΓ₆}` (P3's cost number 151 at twelve residues,
   `e^{13.5}` at sixteen); the same constants spread over the sites as penalties cost 0.20 and
   0.37, because the Gibbs measure keeps 0.6–0.7 side chains off the anchor on average and the
   20 000 samples visit ten distinct assignments.  This is P3's lesson "the certificate must be a
   function, not a constant", at the order and in the geometry where P3 had concluded the
   recipe fails.
3. **The deterministic bracket is half-informative, the sampled one sharp.**  At sixteen
   residues `ln Z + βE(x⁰) = 0.54`: the anchor carries 58 % of the weight.  The deterministic
   bracket (0.52 nats) is as wide as that whole contribution; the Hoeffding bracket (0.026 nats)
   is what makes the certificate useful, and it rests on exact sampling from `π_{m₋}` and the
   certified range of `E − m₋`.  The Bennett bracket with certified floor and variance is no
   better than the deterministic one here (`b_cert = 0.4–1.0`, `s²_cert = 0.4–1.8`): the certified
   variance pays for the looseness of `γ_i` quadratically, as P3 found.
4. **Cost.**  1 586, 6 885, 21 700 and 174 437 evaluations of `g` for the ball (39 %, 10.5 %,
   2.1 %, 0.016 % of the domain), plus the samples; under five minutes each up to twenty
   residues, 33 minutes in four runs at thirty (the ball of a 582-atom peptide is the cost).
   The ball grows like `n⁵/120`, the domain like `2ⁿ`.
5. **The growth is slow, and it is growth** [M; H for the extrapolation].  From 12 to 30
   residues the largest site penalty goes 0.56, 1.23, 1.80, 2.67 `k_BT`, the width of the
   deterministic bracket 0.32, 0.52, 0.63, 0.73 nats, that of the sampled bracket stays near
   0.02–0.03 nats, and the mean number of side chains off the anchor under `π_{m₋}` 0.61, 0.69,
   0.74, 0.79.  `Γ₆` grows by 1.8 kcal/mol per residue between twenty and thirty residues, which
   suggests that the penalty of an interior site of a long helix tends to about `3 k_BT` (the
   central sites of Leu₃₀ are at 2.6–2.7); the brackets widen far more slowly than these
   penalties alone would suggest — presumably the side chains that leave the anchor are mostly
   the cheap ones near the ends; I did not check.  I did not run longer chains.  See §4, item 5.

---

## 4. What this means for certifying a solvated side-chain free energy in a compact geometry

Model-relative throughout: GBn2 as OpenMM 8.6.1 defines it, on P2's rigid synthetic peptides
with an ideal helix and a rotamer grid.

1. **At a fixed order, the cancellation cannot be bought by analysis** [P + M].  Three natural
   kinds of bound were examined.  *Sign-blind* (uses `|q_p|` only — every term-by-term bound): at
   least 16–153 times the true remainder for leucine on the helix at orders 3–5 (Theorem 8; at
   order 6 only a factor 3.8 could be shown).  *Signed on one side* (the brief's candidate):
   even with exact constants 6–53 times the truth for leucine, 4.5–24 for serine (§1).  *Signed
   on both sides at a reference*: costs the evaluations of the next order and still pays that
   order's sign-blind bound `m + 1` times (Proposition 11).  For this energy function, in a
   compact geometry, **seeing the signs means evaluating**, and the cheapest organised way of
   evaluating is the one P3 already has: one more order of the anchored expansion.
2. **The cancellation is not of the kind a small parameter controls** [M, H].  The gains by level
   of grouping are 3–7 (partners of one atom), then 2–9 (atoms of one residue), then 1.2–3.1
   (residues): no level at which the sum collapses.  Groups are as large as the range of the
   kernel, Born radii inside a group differ by a factor two, and the rigid bodies of the rotamer
   model are not neutral.  The neutral-cluster mechanism of Theorem 9 is real — a carbonyl-sized
   cluster inside a Born radius of 0.35–0.47 nm loses a factor 14–45 to any sign-blind bound — but
   in the peptide it is one contribution among several.  [H: the gain from pair level to atom
   level, 4–7 for leucine, is what about thirty partners with incoherent signs would give.]
3. **How much is still to be had without signs** [M].  P3's bound is 3–16 times the best
   pair-by-pair bound, and 6–41 times the sign-blind lower bound of the same quantity; the
   factor grows with the order.  For serine on the helix this slack and the intrinsic loss are
   comparable (P3 58–300 times the truth, pair-by-pair optimum 10–47); for leucine at orders 3–5
   the intrinsic part is the larger.  At the order the helix needs the slack is the larger lever: for Leu₁₂ at order 6
   the best pair-by-pair bound is 0.33 kcal/mol where P3's is 2.99 (the truth: 0.022 for the sum
   of constants, 0.0092 for the remainder).  A sharper term-by-term bound could therefore gain up
   to an order of magnitude in the site penalties — worth having wherever the function floor of
   item 4 is not already enough.
4. **The helix is nevertheless certified at the sizes tested — by the form of the certificate,
   not by a better bound** [P3's Theorem 5 + M, §3.4].  With the floor as a function the cost is
   paid only where the ensemble goes, and leucine on this helix keeps well under one side chain
   off its anchor on average.  The certified tail bound stays two to three orders of magnitude
   above the truth; the certificate does not care.
5. **Where this stops** [H].  The cost number of a site-penalty floor is about
   `∏_i (1 + p_i (e^{βγ_i} − 1)) − 1`, `p_i` the probability that site `i` is off the anchor.  It is
   small when the ensemble is nearly frozen (here `Σ_i p_i ≈ 0.6–0.8` under `π_{m₋}`) or the
   penalties are below `k_BT` (here up to `2.7 k_BT` at thirty residues, growing with the
   length).  A compact ensemble with real side-chain entropy and the same sign-blind penalties
   would not be certified this way; and the ball of radius 5 has `C(n, ≤5)(k−1)^5` points — 2 % of
   the domain at twenty leucines and 0.016 % at thirty, but `(k−1)^5 = 32` times more for three
   rotamers per site.  For such
   ensembles the compact case is as open as the brief says, and by item 1 the only levers are
   the order, the slack of item 3 and the form of the penalties.
6. **For the open problem as the coordinator stated it** ("the price is small and the proof is
   missing"): for leucine on the helix up to the lengths run here a proof exists; it is two
   orders of magnitude wider than the fitted chain's uncertified remainder; and no analysis of
   the natural kinds will close that gap at fixed order.

---

## 5. Prior art, at the level reached

Reading levels: **[abstract]** = the record returned by the literature tool; **[search snippet]**
= the summary a web search returned, the source itself not opened; **[from memory — unverified]**.
**Nothing was read in full.**  P2's and P3's own searches (pairwise GB in protein design,
provable partition functions, anchored decompositions) were not repeated.

| # | tool, query | what came back | read |
|---|---|---|---|
| 1 | web search: `group-based cutoff neutral charge groups truncation electrostatics artifacts atom-based cutoff Steinbach Brooks spherical cutoff` | 10 links | snippets only |
| 2 | web search: `maximum of quadratic form over sign vectors Grothendieck inequality "cut norm" Alon Naor approximating` | 10 links | snippets only |
| 3 | Consensus: "generalized Born energy pairwise decomposition error cancellation between self energy and screened interaction terms protein design" | 3 papers | 3 abstracts |
| 4 | PubMed: `fluctuating dielectric boundary generalized Born protein design` | 2 hits (PMID 28749575, 41055950) | not opened |
| 5 | web search: `Still Tempczyk Hawley Hendrickson 1990 generalized Born f_GB formula dipole in sphere limit Onsager ...` | 10 links | snippets only |

**What these say.**
* *Keeping neutral groups together is a classical device for sums of Coulomb terms*
  **[K, search snippet]**: "charge-group" (group-based) truncation of electrostatics in molecular
  simulation, discussed by Steinbach & Brooks (*J. Comput. Chem.* 15, 1994; Crossref record
  `10.1002/jcc.540150702`), Ni & Baumketner (PMC3204157) and Kubincová, Riniker & Hünenberger
  (*Phys. Chem. Chem. Phys.* 2020, `d0cp03835k`); the snippets report both that it reduces cut-off
  artefacts and that it creates others for charged groups.  That literature concerns the
  *accuracy of a truncated sum*; nothing in the snippets concerns certified bounds, and my
  measurement (§1) is that for the Born-radius response of GBn2 one-sided group sums buy a
  factor 2–4 only.
* *The best sign-blind bound is a maximum of a quadratic form over sign vectors*
  **[K, search snippet]**: such maxima (`‖A‖_{∞→1}`, the cut norm) are MAX SNP-hard to compute
  and are approximated within a constant by a semidefinite programme through Grothendieck's
  inequality (Alon & Naor, "Approximating the cut-norm via Grothendieck's inequality"); for
  quadratic forms `sᵀAs` on general graphs the gap is logarithmic (Alon, Makarychev, Makarychev &
  Naor, "Quadratic forms on graphs").  I used neither result: a local search gives a certified
  *lower* bound of the maximum, which is all Theorem 8 needs, and the pair-by-pair optimum is an
  upper bound.
* *Pairwise treatments of GB in protein design* **[K, abstract]**: Gaillard & Simonson,
  *J. Comput. Chem.* (2014), "Pairwise decomposition of an MMGBSA energy function for
  computational protein design" (the many-body character of the GB term "is overcome using an
  effective dielectric environment"; the error of the decomposition is evaluated numerically);
  Gaillard, *J. Phys. Chem. B* (2025), "Improved physics-based single-position protein sequence
  redesign with a residue-pairwise generalized Born model" (a "fluctuating dielectric boundary"
  approach "allowing an exact decomposition of the GB term" — for *their* GB variant; I did not
  read how).  Sevim et al., bioRxiv (2026), report that the Coulomb interaction energy and the GB
  correction are almost perfectly collinear in MM-GBSA calculations of complexes (`R² ≥ 0.99`) —
  the zeroth-order face of the cancellation measured here at orders 3–5.  These works choose or
  assess approximations; none of the three abstracts states a bound.
* *The GB pair formula* **[K, search snippet]**: Still, Tempczyk, Hawley & Hendrickson, *J. Am.
  Chem. Soc.* 112 (1990) 6127; Onufriev & Sigalov (2011, PMC3100913) on gross errors of the
  canonical formula relative to the Poisson equation.  The small-cluster expansion
  `g ≈ −(3κ/8)|μ|²/B³` used in the Remark of §2.3 is derived there from the formula; I did not
  look for it in print.

**From memory, unverified:** that the triangle inequality loses correlations between terms is
the "dependency problem" of interval arithmetic; the notion closest to "sign-blind" in analysis
is unconditionality (bounds uniform over sign changes of the coefficients).

**How this report relates to it.**  Proposition 7 is elementary; its content is the observation
that the GB kernel matrix does not depend on the charges, which turns "treats pairs one at a
time" into a quantifier over sign patterns that can be evaluated on real instances.  I did
not find that formulation, the family of Theorem 9, or the numbers of Theorem 8 in the nine
records above.  **This is not a claim of novelty**: five queries, nothing read in full, in a
literature I did not survey.

---

## 6. Requests (no request is an authorisation to spend anything)

### To the theory division

**P5-T1 (the price of not looking at signs, as a formal statement).**
*Statement.*  Let `M : X → Sym_N` be a matrix-valued function on a finite set, `q ∈ ℝ^N`,
`g_c := −(κ/2) cᵀ M c`, and `Φ` a functional that is convex and even in `g` (a sup-norm of a linear
image of `g`: an anchored constant, a remainder).  Call `β` sign-blind if `Φ(g_{s∘q}) ≤ β` for all
`s ∈ {±1}^N`.  Then `β ≥ max_s Φ(g_{s∘q})` (Proposition 7), the maximum is a maximum of
`|sᵀ A s|` over sign vectors and matrices `A = D (LM)(x) D`, `D = diag|q|`, `L` the linear map; and on
the family of Theorem 9 `max_s Φ(g_{s∘q}) / Φ(g_q) ≥ N|Δb|/|Δχ_r| − (N−1)`.
*Questions.*  (i) Is there a matching *upper* statement that is computable: by Grothendieck-type
inequalities the semidefinite relaxation of `max_s |sᵀAs|` is within a constant (bilinear case) or
`O(log N)` (quadratic forms) of the maximum — so is "the best sign-blind bound of one subset" =
"an SDP value, up to `log N`", and can such a value be summed over all subsets of a given order in
closed form as P3's Proposition 4 does for the term-by-term bound?  (ii) Does your
query-complexity theory have a statement for the class `{g_{s∘q} : s ∈ {±1}^N}` — kernel known,
signs of the coefficients not — which is the class a sign-blind analysis implicitly certifies?
*Validation case.*  Leu₈/H, `m = 4`: truth `sup|g − I₃g| = 0.0882`, a sign pattern with `2.10`, best
pair-by-pair sum `10.1`, P3's `Γ₄ = 49.3` kcal/mol (`out/s2_L8_H_0.60.json`).
*Stopping condition.*  A proved two-sided bracket of the least sign-blind bound in terms of a
polynomially computable quantity, or a reason there is none.

**P5-T2 (two lemmas for the remainder calculus).**  (a) Proposition 10: for a down-closed family
`𝒟`, `g − Σ_{U∈𝒟, U⊆S(x)} d_U = Σ_{T ∈ Thr(𝒟), T ⊆ S(x)} Δ_T g(z^{T,x}; x_T)`, `Thr(𝒟) = {T ∉ 𝒟 : T∖{min T} ∈ 𝒟}` —
the generalisation of P3's Proposition 1 (your `higherOrder_remainder`) from "all subsets of order
`< m`" to any family, e.g. different orders for near and far sites, or a different family for each
block of the energy.  (b) Proposition 11: `sup_z |Δ_T g(z; y_T)| ≤ |d_T(y_T)| + Σ_{j∉T} c^anch_{T∪{j}}`.
Both are three-line consequences of the context expansion and small formalisation targets.
*Validation.*  `s3_locality.py` (22 140 checks), `s4_refbound.py`.  *Stopping condition.*  Lean
statements next to `higherOrder_remainder`.

**P5-T3 (the cost of a floor that is a function, on a nearly frozen ensemble).**  The helix
results of §3.4 are an instance of P3's request P3-T2: the cost number is
`𝔼_{π_E} e^{β(E − m₋)} − 1` and with site penalties it is about `∏_i (1 + p_i (e^{βγ_i} − 1)) − 1`, `p_i` the
probability that site `i` is off the anchor.  *Question.*  For a floor of the form
`model − Σ_i γ_i [x_i ≠ x⁰_i]`, state the certificate cost in terms of the law of `S(x)` under `π_E`, and
the optimal allocation of a given family of subset bounds `ĉ_T` to sites or pairs (your Theorem
11.18a) *for that law* — the uniform `1/m` allocation P3 uses ignores that interior sites of a
helix are off the anchor more or less often than terminal ones.  *Validation case.*  Leu₁₆/H,
`m = 6`: `γ_i ∈ [0.21, 0.73]` kcal/mol, exact cost number 0.374, deterministic bracket 0.523 nats.

### To the engineering division

**P5-E1 (specification: the pair-by-pair optimum and the sign-blind lower bound at 16 residues).**
*Motivation.*  §1–§2 measure, up to 12 residues, how much of P3's bound is slack of its
inequalities (recoverable without signs) and how much is intrinsic.  At 16 residues the kernel
array has `65 536 × 316² = 6.5·10⁹` entries and my numpy implementation is too slow.
*Formulation.*  For Leu₁₆/H (τ 0.60, anchor all-ones in P3's domain indexing) and every subset
`T` of order 3–6: `PP_T = Σ_{p≤q} sup |Δ_T W_pq|` (anchored, all contexts), `c_T^anch(g)`, and
`c_T^anch(g_{|q|})`.  *Inputs.*  `p3core.GBModel('L16', 'H', tau=0.60)`; the definitions of
`p5lib.kernel_rows`, `anch_consts`.  *Outputs.*  The three sums per order.  *Validation.*  Leu₈/H:
`Σ_T PP_T = 105.8, 10.12, 0.7140`, `Σ_T c_T = 1.2328, 0.28632, 0.029192` kcal/mol at orders 3, 4, 5.
*Stopping condition.*  Orders 3–6 done, or 4 CPU-hours.  *Resources.*  A compiled loop over
pairs with a Gray-code walk over the `2^16` states; about `6.5·10⁹` kernel evaluations.

**P5-E2 (specification: the function floor at order 7).**  *Motivation.*  §3.4: at order 6 the
site penalties reach `2.7 k_BT` at thirty residues and the deterministic bracket is 0.73 nats
wide; one more order would divide the penalties by 5–8.  *Needs.*  Enclosure tables of order 7
(`encl.EnvelopeSup(K=7)`; P3's tables stop at 6) and the ball of radius 6 (`C(30, ≤6) = 768 212`
evaluations of a 582-atom energy for Leu₃₀; mine took 7 ms each).  *Validation.*  Leu₁₆/H and
Leu₃₀/H at order 6 (Table 4).  *Stopping condition.*  A deterministic bracket below 0.1 nats for
Leu₃₀/H, or a cost estimate showing it is out of reach.

---

## 7. The three most promising next steps

1. **Find where the function floor stops, on an ensemble that is compact and not frozen.**
   §3.4 works because leucine on the helix keeps 0.6–0.8 sites off the anchor.  The decisive
   test is a compact geometry with real side-chain entropy: P2's patterned sequence on the helix
   (where P3's certificate failed at order 4), serine or valine on the helix with a finer grid,
   several anchors.  The quantity to watch is `Σ_i p_i (e^{βγ_i} − 1)`.  If it fails there, the
   compact case is open again, and then only an order more (request P5-E2) or a smaller `γ` can
   help.
2. **Recover the slack inside the sign-blind class.**  P3's bound is 3–16 times the
   pair-by-pair optimum and the factor grows with the order (§1): at the order the helix needs,
   an order of magnitude of `γ_i` is slack of inequalities, not cancellation.  First a breakdown
   of `ĉ_T` against the exact term constants by type of pair (fixed–fixed, fixed–side chain, side
   chain–side chain; P3's sharpness test suggests the host step, which bounds a difference of two
   host states by a sum), then a sharper treatment of that step.  The ceiling of this route is
   Theorem 8: at orders 3–5 no sign-blind bound comes closer than a factor 16–153 to the truth
   for leucine on the helix; at order 6 the ceiling is not known (between 3.8 and 36 on Leu₁₂),
   and that is the order at which this route could pay.
3. **A formal home for "certification is evaluation".**  Propositions 7, 10 and 11 say that at a
   fixed order every certificate built from reference values and sign-blind tails pays the
   sign-blind price of the tail.  A theorem of the theory division's kind — a lower bound on the
   number of evaluations needed to certify the remainder of a GB-type function within a factor
   `c`, in terms of how fast the sign-blind optimum decays with the order — would turn the
   measurements of this report into a statement about all such certificates (request P5-T1).

---

## 8. How to re-run

Everything runs from `experiments/science/ws_P5/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`
(the wrappers set them) and `python3 -B`.  The scripts import workstream P3's modules
(`p3core`, `encl`, `gfbound`, `pwmodel`) and through them P2's (`fbmodel`, `scbuild`) and P's
read-only; `p5lib.py` redirects P3's enclosure cache to `ws_P5/cache/` (27 tables copied from
`ws_P3/cache/`; if they are deleted they are rebuilt there in about four minutes), so nothing
is written outside `ws_P5/`.  A log is complete when its last line is `DONE in … s` (my scripts)
or `[…s] -> out/floor_….json` (the copy of P3's pipeline).  Wall times are from a machine
shared with other jobs.

| what | one command | log(s) in `logs/` | run time (s) |
|---|---|---|---|
| step 1, Leu₆, Leu₈, Ser₄, Ser₅ (§1) | `./run_s1_small.sh` | `s1_L6_H_0.60.log`, `s1_L8_H_0.60.log`, `s1_S4_H_0.70.log`, `s1_S5_H_0.70.log` | 1.8, 12.6, 5.6, 110.0 |
| step 1, Ser₆ (two halves in parallel, then the merge) | `./run_s1_S6.sh` | `s1_S6_H_0.70_rows0-39.log`, `s1_S6_H_0.70_rows39-78.log`, `s1_S6_H_0.70.log` | 445.7, 446.3, 81.6 |
| step 1, Leu₁₂, orders 3–6 (two runs) | `./run_s1_L12.sh` | `s1_L12_H_0.60_rows0-240.log`, `s1_L12_H_0.60.log` | 509.3, 215.3 |
| step 2, the five instances of orders 3–5 (§2.2; needs the `s1` JSON files) | `./run_s2_all.sh` | `s2_L6_H_0.60.log`, `s2_L8_H_0.60.log`, `s2_S4_H_0.70.log`, `s2_S5_H_0.70.log`, `s2_S6_H_0.70.log` | 5.3, 43.3, 2.7, 43.6, 322.8 |
| step 2, Leu₁₂, orders 3–6 | `python3 -B s2_signblind.py L12 H 0.60 6 --lsmax 4 --nrand 4 --ncand 6 --nrandrem 30` | `s2_L12_H_0.60.log` | 296.6 |
| Theorem 9, the family (§2.3) | `python3 -B s2_family.py` | `s2_family.log` | 0.6 |
| Proposition 10 and the locality table (§2.4, §3.3) | `python3 -B s3_locality.py` | `s3_locality.log` | 391.7 |
| Proposition 11 (§3.2; needs the `s1` JSON files) | `python3 -B s4_refbound.py` | `s4_refbound.log` | 62.4 |
| P3's pipeline on the helix, order 6, site penalties (§3.4) | `./run_floor_helix.sh L12 6 --N 20000`; `./run_floor_helix.sh L16 6 --N 20000`; `./run_floor_helix.sh L20 6 --N 50000 --noenum` | `floor_L12_H_m6_siteres.log`, `floor_L16_H_m6_siteres.log`, `floor_L20_H_m6_siteres.log` | 27, 162, 252 |
| the same for Leu₃₀ (ball in two checkpointed halves, merge, pipeline) | `./run_floor_L30.sh` | `ball_L30_H_M5_part0.log`, `ball_L30_H_M5_part1.log`, `ball_L30_H_M5_merge.log`, `floor_L30_H_m6_siteres.log` | 552.9, 716.2, 10.4, 694 |
| tables of this report | `python3 -B mk_tables.py` | `out/tables.md` | < 1 |

(`./run_rest.sh` runs the first, sixth, eighth and fourth line in that order.)  Results:
`out/s1_*.json`, `out/s2_*.json`, `out/s2_family.json`, `out/s3_locality.json`, `out/s4_refbound.json`,
`out/floor_*.json`, `out/tables.md`.  **Not cited, superseded:**
`logs/SUPERSEDED_floor_L30_H_m6_siteres_killed.log` (a first Leu₃₀ run that would have exceeded
twenty minutes, killed after two); the files `logs/run_*.out`, `logs/*.err` are captures of
wrapper output, not logs of runs; earlier versions of the `s1`, `s2` and `s2_family` logs were
overwritten by the final runs listed above (§11).  Two runs were killed and are not in the
table: `s1_cancel.py L12 H 0.60 6` in one piece (it was about to pass twenty minutes) and the
first Leu₃₀ pipeline run.

---

## 9. What I did not settle

1. **Whether some other sign-aware bound exists.**  Proposition 7 excludes sign-blind bounds,
   §1 the one-sided group sums, Proposition 11 the signed reference term.  A bound that uses the
   signs *and* is uniform over contexts by some other mechanism (positivity of the GB kernel, a
   convex relaxation over the product domain, a low-rank factorisation of the kernel) is not
   excluded; I have no candidate, and every one I sketched reduced to "exact at reference
   points plus a sign-blind top order" (notes, 02:38–02:56).
2. **The least sign-blind bound itself** — only bracketed, see §2.2.  In particular for **serine
   on the helix** the question "is a sign-blind bound within a factor ten possible?" is open:
   the patterns found give 3.4–19, the pair-by-pair optimum 10–47.
3. **How far the function floor goes.**  §3.4 has four chain lengths, one side chain, one order,
   one anchor.  The growth of the site penalties with the length, the order-7 tables, more
   mobile side chains in a compact geometry, charged side chains: not run.
4. **Leu₂₀ and Leu₃₀ exactly.**  Their brackets contain the coordinator's fitted-chain values;
   neither was enumerated (Leu₂₀ would take about 40 CPU-minutes with P3's pipeline).
5. **Which step of P3's Theorem 3 carries its slack** (a factor 3–16 against the pair-by-pair
   optimum, growing with the order): not broken down by type of atom pair.
6. **Step 1 on other backbones.**  The measurement was made on the helix only; on the strand and
   on PPII P3's bound is already within reach of the recipe, and I did not repeat it there.
7. **Class constants** (all pairs of states) as opposed to anchored ones; several anchors.

---

## 10. What I did not check

* **No proof was machine-checked.**  Propositions 7, 10, 11 and Theorem 9 are paper proofs,
  checked numerically as stated at each of them.  The certificates of §3.4 are **P3's
  Theorem 5**, with P3's paper proofs, P3's code (a verbatim copy) and P3's floating-point
  allowances; I did not re-derive or review them.  Their sandwich was verified state by state
  only where the domain could be enumerated (Leu₁₂: 4 096 states; Leu₁₆: 65 536 states).  For
  Leu₂₀ and Leu₃₀ the only checks are `E ≥ m₋` at the sampled states and the agreement with the
  coordinator's uncertified fitted-chain values.
* **The sign patterns are from a local search**, not from an exhaustive one: every number called
  a lower bound is an exact evaluation, but the least sign-blind bound itself is only
  bracketed (between that and the pair-by-pair optimum, a factor 1.4–2.6).
* **Double precision.**  Mixed differences of order 5–6 are alternating sums of up to 64 values
  of size `10²` kcal/mol: absolute rounding about `10⁻¹¹`; the smallest total in a table is
  `3·10⁻⁵` kcal/mol (the smallest entry of any kind `1.6·10⁻⁷`).  No interval arithmetic was used
  for the *exact* constants (they are measurements, not certificates).
* **One anchor** (`argmin E`), one clash threshold per side chain (P3's), **the helix only**,
  **homopeptides only** (P2's patterned sequence was not run), Leu and Ser only.
* **The coordinator's reference values** (483.8466; 593.3030; 866.9139) were taken from
  addendum A17 (10) and not recomputed, except the first, which the pipeline reproduces by
  enumeration (483.846587).
* **Prior art** at snippet and abstract level only; two PubMed hits not opened.
* **Independence and exactness of the samples** behind every bracket with a `δ`: as in P3.
* **Physical meaning.**  Nothing here bears on whether GBn2 describes water, or on any real
  peptide.

---

## 11. My own errors

1. **A time stamp in my notes was a guess.**  The heading of the second block of `NOTES.md`
   first read "02:20–03:05"; the clock said 02:38.  Corrected in the notes, with the correction
   visible.  All later time stamps are from `date`.
2. **A bookkeeping bug in `s2_signblind.py`.**  The per-subset lower bound `LS_T` did not include
   the sign pattern found for the remainder, so for Ser₄ at order 4 the line "one pattern for all
   `T`" (`2.52·10⁻³`) exceeded "best pattern per `T`" (`2.19·10⁻³`) — impossible for a maximum.
   Seen in the first output, fixed (`LS_T` is now the maximum over every pattern tried), all five
   instances re-run.  It only made lower bounds smaller than they could be.
3. **I conflated two different lower bounds.**  My first reading was "every sign-blind bound is at
   least `Σ_T` (best pattern per `T`)".  That holds for bounds built subset by subset (P3's `Γ_m`
   is), not for an arbitrary sign-blind bound of the sum, which only has to dominate the best
   *single* pattern.  The tables now carry three lower bounds, (A), (B), (C), and the headline
   uses (C), the remainder itself.
4. **The first step-1 runs lacked a row the brief asked for** ("the cross part regrouped by
   groups": my first version regrouped self and cross together).  Added (`agx`, `ggx`), all
   instances re-run; the first logs were overwritten and are not cited.
5. **The first geometric realisation of the family (part C of `s2_family.py`) was not
   representative**: four atoms and distant shells have Born radii of 0.17–0.20 nm, so `r/B` was
   not small and the ratios were 2–19.  A static symmetric bath of 38 uncharged atoms gives
   `B = 0.35–0.47 nm`, the range of the real peptide; the first output is superseded.
6. **A sign error in the draft of Theorem 9(ii)** (`+` for `−` in the truth), corrected before any
   number depended on it; and a leftover dead block in `p5lib.anchored_interp`, removed before
   first use.
7. **I once waited with a foreground `sleep 100`** instead of the notification of the background
   job.  Harmless, noted.
8. **Two runs of mine were heading past the twenty-minute limit and had to be killed**: step 1 on
   Leu₁₂ in one piece (P3's bound subset by subset costs 0.6 s per subset at order 6; I had not
   estimated it and the loop printed no progress) and the first Leu₃₀ pipeline run (I had
   assumed 492 atoms; it has 582, and its ball alone takes 21 minutes).  Both were re-done as
   checkpointed pieces (`run_s1_L12.sh`, `run_floor_L30.sh`, `ball_precompute.py`); the killed
   logs are not cited.  While testing the fix I overwrote the Leu₆ result with a reduced one and
   had to re-run the small instances.
9. **Numbers written into the draft before the script that produces them existed.**  The verdict
   first said "4.5–8.6 for serine" and "8–34 for leucine" for the one-sided sums (from a few rows
   I had in mind); the ranges computed by `mk_tables.py` over all rows and groupings are 4.5–24
   and 6–53.  A check count ("27 114") was a wrong sum of mine; the logs give 16 296.  Every range
   in the final text is from the block `ranges` of `out/tables.md` or from a log.
10. **The first sign search on Leu₁₂ was too weak to be trusted at order 6** (three starting
    states, six starts).  I re-ran it with thirteen states and 32 starts; it found the same
    patterns, so the weak value at order 6 (3.8) stands as what I could show, not as what is
    true.

---

## Coordinator's note (2026-11-26, before publication as SCI-MSG-0024)

1. **Read in full by the coordinator.**  **Re-derived:** Proposition 7 (elementary; its content is
   that the kernel matrix does not depend on the charges — true of the Born radii of this model
   by construction); Theorem 9 (i)–(iv), including the arithmetic of the polynomial inequality
   (`1 − (25/64)u² + (21/256)u³ + (9/2048)u⁴`, and `168u + 9u² ≤ 800` on `[0, 8/3]`); Proposition 10 (the
   partition of the subsets outside a down-closed family by their shortest suffix outside it);
   Proposition 11.
2. **One slip, in Theorem 9(i):** "`k := Σ_p s_p`" must read `k := Σ_p s_p(−1)^p` — the sum of the
   signs of the charges *after* the reversal (the true charges alternate, so the truth is `k = 0`
   and "all charges positive" is `k = N`, as (ii) says).  With that reading (i)–(v) are as written.
3. **Recomputed with independent lines** (`experiments/science/pi_inference/p5_adoption_check.py`,
   7 s): for Leu₆ on the helix the kernel matrices from workstream P3's *table-free* path (the
   tables are what the workstream used), my own inclusion–exclusion for the anchored
   interpolation, and my own sign search (1-flip ascent on the quadratic form of the remainder
   at each state, then exact evaluation at all states).  True remainder `0.056866, 0.030119,
   0.002221` kcal/mol and all-charges-positive `3.600712, 0.573930, 0.004578` at orders 3, 4, 5 — the
   workstream's values to `10⁻⁹`; **my search finds remainders `8.6845, 0.6848, 0.0367`, the
   workstream's values, hence the same factors 152.7, 22.7, 16.5** (its patterns are not stored;
   mine were found independently — any pattern is a valid witness).  **The Leu₁₂ certificate
   rebuilt through a different driver** (workstream P6's `make_models`, site form, order 6, band
   11): `ln Z(m₋) = 374.5276673543`, `ln Z(m₊) = 374.2090967932`, exact `ln Z(E) = 374.345343432`, the
   sandwich at all 4 096 states, cost number `0.200003` — identical to the workstream's run of
   P3's pipeline.
4. **Checked by `diff`:** `ws_P5/floor_p3copy.py` is `ws_P3/run_floor.py` plus four lines (a comment
   and `import p5lib`).
5. **Two wordings.**  (a) "The anchor is the certified minimiser" (§3.4, reading 1): what is
   certified is the minimum *value* — `min E ∈ [E(x⁰) − 10⁻⁷, E(x⁰)]` kcal/mol — not that the
   minimiser is unique.  (b) "The helix is certified" means these instances: leucine, two
   rotamers per site, an ensemble with 0.6–0.8 side chains off the anchor; the report says so in
   §0 item 5 and §4 item 5, and the message keeps the qualification in its title.
6. **Prior art (§5).**  Verified by the coordinator at abstract level through PubMed: Gaillard &
   Simonson, *J. Comput. Chem.* 35 (2014) 1371–1387, doi:10.1002/jcc.23637; Gaillard, *J. Phys.
   Chem. B* 129 (2025) 10699–10710, doi:10.1021/acs.jpcb.5c03662 — both as quoted; and, found in
   the same search, Gaillard & Simonson, *J. Chem. Theory Comput.* 13 (2017) 4932–4943,
   doi:10.1021/acs.jctc.7b00202 (the GB term "is affected by pairwise decomposition errors when
   all positions are designed together").  Not verified by the coordinator: the bioRxiv record
   (Sevim et al.) and the web-search snippets (charge groups; cut norm).
7. **Not re-run by the coordinator:** the sign searches for Leu₈, Leu₁₂ and serine; `s2_family.py`;
   `s3_locality.py`; `s4_refbound.py`; the certificates for Leu₁₆, Leu₂₀, Leu₃₀.  The last two
   contain the coordinator's fitted-chain values of addendum A17 (10) (`593.3030 ± 0.0001`,
   `866.9139 ± 0.00003`), which were computed before this workstream existed: an independent check
   of the *value*, not of the certificate.
