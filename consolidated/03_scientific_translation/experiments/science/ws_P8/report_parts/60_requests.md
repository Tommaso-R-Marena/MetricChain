---

## 5. Requests (can be sent as they stand; no request is an authorisation to spend anything)

### To the engineering division / the coordinator's pipeline

**P8-E1 (independent re-run of the Lys₁₂ certificate with the new constants; the constants into the reach table).**
*Motivation.*  §4: fed with the state-wise constants, the pipeline's modules give for
Ace-Lys₁₂-NMe on the helix the brackets of table T10 (order 4: 2.81 nats; order 5: 0.45 nats with band 6 and 0.19 nats with band 7).
That run was made by the author of the constants with a driver of his own
(`ws_P8/p8_12_certificate.py`), which only imports the pipeline's modules; nobody else has re-run
it.  *Formulation.*  The coordinator's own driver (`pi_inference/serine_helix_reach.py`) with `ĉ_T`
taken from `ws_P8/out/g12b_K12_H_0.70_m5.npz` (array `Cb[:, 1]`, variant 'SAb', kcal/mol, one row per
subset in the order of `T`; anchor in `anchor`) instead of the closed-form sums; `S_i`, `G_ij`, `H_ijk`
are plain sums over the 792 subsets.  *Hypothesis used:* `|g − I₄g|(x) ≤ Σ_{T ⊆ S(x), |T| = 5} ĉ_T` —
Theorem AH of §3.3 (a paper proof; checked term by term and state by state on the enumerated
instances, §3.4, and against the exact anchored terms of all four-subsets at twelve residues, §2.3).
*Inputs.*  Ball of radius 4: 1 621 056 evaluations (cached with its states in
`ws_P8/cache/ball_K12_H_0.70_M4_*.npz`; half an hour on one core otherwise).  *Validation.*  The same
driver on the enumerated instances Lys₄ and Lys₅ (`ws_P8/p8_12_certificate.py … --enum`): sandwich
at every state, exact `ln Z` inside all brackets (table T10).  *Stopping condition.*  The
coordinator's driver reproduces the brackets of T10 to the digits printed, or a difference is
found and explained.  *Resources.*  About half a CPU-hour; 1.6 GB with band 6 and 2.3 GB with band 7 here.

**P8-E2 (the state-wise form inside the pipeline, and a hybrid for long chains).**
*Motivation.*  Every certificate so far uses `gfbound.GFBound`, whose merging of ingredients over
host rotamers costs a factor 20–170 for lysine and 6–30 for the patterned sequence (§3.5).
*Formulation.*  (i) For `n ≤ 12–16`: enumerate the subsets and call
`p8sr.BlockBound.total_T_blocks(m, T)['SAb']` (0.05–0.15 s per subset at 276 atoms; a subclass of P3's
`GFBound`, P3's files untouched).  (ii) For longer chains: `Σ_T ĉ^{AH}_T` in closed form
(`AHBound.total_ah`, P3's closed form with "X → A"), minus `ĉ^{AH}_T − ĉ^{SAb}_T` for the subsets inside a
window, enumerated — every subset keeps a valid constant.  *Validation.*  `ws_P8/out/g12*.npz` (the
four twelve-residue peptides, orders 4–6); the equality of variant 'P3' with `GFBound.total` and of
'Sb' with `termwise.TermBound` in anchored mode.  *Stopping condition.*  Leu₃₀ and Val₃₀ reproduced
with the closed form; one charged instance beyond twelve residues.

**P8-E3 (a latent memory leak in `ws_P5/p5lib.anch_walk`).**  The recursive closure `rec` uses the
base array `F` as a free variable and refers to itself, so every call leaves one full array in a
reference cycle until Python's cyclic collector runs (thresholds 2000/10/10 here).  In a loop over
atom rows this accumulated to 11.7 GB in my run (§7).  *Fix:* `gc.collect()` after the call (as in
`ws_P8/p8lib.py`), or pass `F.shape` into the closure instead of `F`.  *Validation.*
`ws_P8/x05_memdiag.py K4 H 0.70 12 old|new`: +13 MB per row against flat.

**P8-E4 (penalties resolved by rotamer state — specification of the next step).**
*Motivation.*  §2: on the true ensemble the exact remainder of Lys₁₂ is `10⁻⁵` kcal/mol at order 3,
while the new constants still cost 1.6–11 nats at order 4 (table T10): the constants are suprema over all
rotamers of the sites of `T`, and the ensemble visits few of them.  *Formulation.*  In the proof of
Theorem AH the host states of a term are those of the state `x` itself (`u_l = x_l`) before the
maximum over `u` is taken; so for a host `l` in `T` the bound may depend on `x_l`.  A site penalty
`γ_i(x_i)` or pair penalty `γ_ij(x_i, x_j)` that keeps this dependence for the pairs hosted at `i` (and
the maximum for the rest) is a table over rotamers and fits the band models as they are.
*Inputs.*  The per-state arrays already computed in `p8sr.SRBound._theta` (all pairs of host
states of a block).  *Outputs.*  Tables `γ_i(x_i)`, `γ_ij(x_i, x_j)`; the first-order bracket for Lys₁₂
at order 4.  *Validation.*  Lys₄, Lys₅ by enumeration: `|g − I_{m−1}g|(x) ≤ pen(x)` at every state.
*Stopping condition.*  A measured factor against the state-independent penalties, or a reason
why the dependence on `x_l` is weak.  *Resources.*  Minutes.  (Not done here.)

### To the theory division

**P8-T1 (the remainder identity with a term-dependent order).**  *Statement.*  Let `F = Σ_τ F_τ` on a
finite product, `x⁰` an anchor, and for each `τ` a total order `≺_τ` of the sites.  Then for every `x`
and `m ≥ 1`: `F(x) − I_{m−1}F(x) = Σ_τ Σ_{T ⊆ S(x), |T| = m} Δ_T F_τ(z^{T,x,τ}; x_T)`, `z^{T,x,τ}_i = x_i` if `i ≺_τ min_{≺_τ} T`
and `x⁰_i` otherwise.  If `≺_τ` puts a set `H_τ` of at most `m − 1` sites last, every site of `H_τ ∖ T` sits at
its anchor in all evaluations.  (Your `higherOrder_remainder` is the case of one order and of
class constants; P3's Proposition 1 the case of one order.)  *Use.*  Theorem AH of this report.
*Validation.*  `ws_P8/p8_10_order_identity.py` (62 400 checks of the identity, deviations at
rounding level).  *Stopping condition.*  A Lean statement next to `higherOrder_remainder`, or a
counterexample; and a referee's reading of the proof of Theorem AH as a whole (§3.3: one page).

**P8-T2 (what is the least sign-blind bound for a charged cluster?).**  P5's Theorem 9 shows that
the sign-blind class loses without bound on *neutral* clusters.  For lysine the measured loss is
3–7 (§1) and the pair-by-pair optimum is 2.6–5.5 above the largest remainder of a sign pattern
found.  *Question.*  For a
GB-type function whose charges are dominated by one sign inside the range of the kernel, is the
least sign-blind bound within a constant of the truth — i.e. is there a statement of the form
"`SB(Φ) ≤ C(Σ|q|/|Σq|)²·Φ(g)`" for clusters with a net charge?  *Validation case.*  Lys₅ on the
helix, `m = 4`, largest remainders: truth 0.0250, all charges positive 0.111, best pattern found
0.127 kcal/mol; sum over the five subsets of the pair-by-pair optima 0.545; of the new constants
1.24 (`ws_P8/out/sb_K5_H_0.70.json`, `ws_P8/logs/bc_K5_H_0.70.log`).
