"""P3: one-off helper that replaces the text placeholders of the report (kept for the record)."""
import os, sys
path = "/home/user/MetricChain/docs/science/workstreams/P3_REPORT.md"
t = open(path).read()
R = {}
R["⟨NVIOL⟩"] = "5 512 504"
R["⟨BIG⟩"] = ("Ace-Val₂₀-NMe on polyproline II, `3²⁰ = 3.49·10⁹` assignments: certified deterministic bracket `ln Z ∈ [518.2332, 518.2937]` from 87 441 "
              "evaluations, `[518.2598, 518.2648]` with 50 000 samples (δ = 0.05), and a certified global minimum")
R["⟨NVIOL-DETAIL⟩"] = ("160 enumerated runs, 5 512 504 state checks, **no violation**")
R["⟨VERDICT-NUMBERS⟩"] = (
    "For Ace-Val₂₀-NMe on polyproline II (`3²⁰ = 3.49·10⁹` assignments, far beyond enumeration): with `m = 4`, 9 921 evaluations of `g` certify "
    "`ln Z(E) ∈ [517.484, 519.220]` deterministically and, with 50 000 exact samples of `π_{m₋}`, `[518.2442, 518.2759]` at confidence 0.95; with `m = 5`, "
    "87 441 evaluations (`2.5·10⁻⁵` of the domain) certify `ln Z(E) ∈ [518.2332, 518.2937]` **with no sampling**, `[518.2598, 518.2648]` with the samples "
    "(Hoeffding), and `[518.2608, 518.2659]` by a Bennett bracket whose floor and variance are certified; all brackets intersect; the same models certify "
    "the global minimum, `min E = −306.56871 ± 10⁻⁵` kcal/mol at the anchor.  In 160 enumerated runs (5.5 million state checks) the sandwich `m₋ ≤ E ≤ m₊` "
    "was never violated and the true `ln Z` lay inside every bracket.")
R["⟨READ-3.4⟩"] = """(i) *Constant bound.*  The cost number is `e^{βΓ_m}` to within a few per cent, as the theory division's formula
says for the centre of a constant box.  `m = 3`: `10³–10¹²⁵` — nothing.  `m = 4`: Val 0.2–13 for 4–12 residues (growing like `e^{0.32 n}`: `10³` near
22 residues), Ser 0.01–0.07 on the strand and 0.07–3.2 on the helix, Phe 0.5–0.75, Lys₄ on the helix 3.2, Leu `3–10¹⁶`, the heteropolymer
`10⁴–10¹⁰⁵`.  `m = 5`: Val ≤ 0.05, Leu on strand and PPII 0.1–6.4 at 6–16 residues, Leu on the helix `3–10¹⁹`.
(ii) *Site penalties* — the floor as a function.  The cost number falls by orders of magnitude because the Gibbs measure rarely leaves the
neighbourhood of the anchor: Val₁₀ on the strand at `m = 4`, 6.3 → 0.022; Val₁₀ on PPII, 5.0 → 0.42; Lys₄ on the helix, 3.2 → 0.48; Leu₁₂ on PPII at
`m = 5`, 0.97 → 0.018.
(iii) *P2's Statement 5(d) with constants certified by analysis alone* (`m = 3`, site penalties, ball of radius 2).  It **works for serine on
the strand**: cost number 0.42, 1.13, 2.29 for 4, 5, 6 residues — at six residues 1 009 evaluations of 531 441, deterministic bracket 1.9 nats,
Hoeffding bracket 0.064 nats with 20 000 samples — and for a frozen ensemble (Leu₈ on the strand, 0.10).  It **fails for valine**: 0.48, 16,
`1.1·10³`, `9.6·10⁴` on the strand and 10.5, `1.5·10⁴`, `6.1·10⁷`, `2.8·10¹¹` on PPII for 4, 6, 8, 10 residues — a factor 8 to 60 per residue, faster
than the domain itself grows (a factor 3) — and for everything on the helix and everything charged (`10²–10⁸⁹`).
(iv) *Growth with length* (site penalties; fitted exponent of `1 + cost` per residue; extrapolations are [H]).  `m = 3`: Ser/E 0.42 per residue
(`10⁶` near 36 residues), Val/E 2.2, Val/PPII 4.1.  `m = 4`: Val/E 0.002, Ser/E 0.008, Val/PPII 0.035–0.06 (0.42 at 10 residues, 1.6 at 20 by
sampling; `10⁶` near 230 residues), Leu/PPII about 0.09, Ser/H about 0.16.  `m = 5`: Val/PPII 0.002 (0.032 at 20 residues), Leu/PPII 0.002.
(v) *When is the certificate cheaper than enumeration, and when impossible?*  Count `N_ball` plus the samples for a bracket of 0.1 nats at
`δ = 0.05` (Hoeffding: about `740 (1 + cost)²`).  With `m = 4` and site penalties this is below `k^n` from **4 residues on for Ser (k = 9) and
from 7 on for Val (k = 3)**; from there on the gap widens exponentially (Val₂₀: 9 921 + 50 000 evaluations against `3.5·10⁹`).  "Impossible"
(cost number above `10⁶`): with analysis-only constants from 6–11 residues on (never possible for Val on PPII beyond 4); with `m = 4` near
230 residues for Val on PPII [H], near 90 for Ser on the helix [H], at 5 for the heteropolymer [M]; with `m = 5` not within any length I can
extrapolate to for Val and Leu on extended backbones, and at 12 residues for Leu on the helix [M: `4·10¹⁹`].
(vi) *The same models certify the minimum* (`min m₋ ≤ min E ≤ E(x⁰)`).  With site penalties the minimum of `m₋` is attained at the anchor —
an exact certificate of `min E`, up to the floating-point allowance — in 5 of 21 runs at `m = 3` (Ser₄, Ser₅, Ser₆, Val₄ and Leu₈ on the strand:
these are certificates of the minimum by P2's Statement 5(d) with *no enumerated constant*), in 19 of 23 at `m = 4` (all Val and Ser instances
including the helix, Leu on strand and PPII, Lys₄ on the helix, Val₂₀ on PPII) and in 13 of 14 at `m = 5`; the exceptions are Phe₄/E
(0.04 kcal/mol), Leu₈ on the helix (12.8 at `m = 4`, 0.009 at `m = 5`) and the heteropolymer (3.4–21).  In all 160 enumerated runs the anchor
is the true minimiser."""
R["⟨BIG-3.5⟩"] = """**Instance.**  Ace-Val₂₀-NMe (a fixed synthetic homopeptide), backbone polyproline II `(−75°, +145°)`, grid R3, τ = 0.70:
332 atoms, 20 sites, 3 admissible rotamers at every site, `|X| = 3²⁰ = 3 486 784 401`.  (One GB evaluation costs 2–4 ms on the loaded machine:
enumeration would take 80–160 days.)  Chosen before any of its numbers were seen, because Val on PPII is the apolar ensemble with the most
entropy among those P2 enumerated (mean number of sites off the anchor: 3.6–4.3 here).
**What was done, in the order of the brief.**  (i) Certified constants: `Γ₄ = 2.82`, `Γ₅ = 0.0822` kcal/mol, site penalties `γ_i ≤ 0.175` and
`≤ 0.0055` (25–98 s).  (ii) The ball of radius 3 (9 921 states) or 4 (87 441 states; 447 s, cached for the other runs); banded lower and upper
models `m_∓` with band `w`; the pairs beyond the band are **not dropped**: `J_ij + d_ij` is split exactly into its column means plus a
remainder whose row minimum (maximum) goes into `m₋` (`m₊`) — so the far pairs sit in the certified remainder `u = β(m₊ − m₋)`.  Exact
`ln Z(m_∓)` and exact samples by transfer matrix over `w` sites (`3⁹` states for `w = 8`).  (iii) `N = 50 000` samples of `π_{m₋}`, `E` evaluated at
each (22 739–29 321 distinct states; `E ≥ m₋` held at every one).  (iv) Brackets valid at every `N` (§2.7, Proposition 6), `δ = 0.05`.
(v) Gibbs–Bogoliubov side."""
R["⟨READ-3.6⟩"] = """(i) *The request is met in full, without sampling and without enumeration:* a certified one-sided floor (`r ≥ 0` for
`m₋`; `r₀ ≥ −βρ_cert/2` for the midpoint model), a certified bound of the mean and of the variance (exact moments of the explicit function
`u`), and `W(b_cert, s²_cert)`.  (ii) *How far are the certified inputs from the enumerated ones?*  For the model `m₋` at `m ≥ 4`: `b_cert/b = 2.0`
throughout (because `𝔼u ≈ 2𝔼r`), `s²_cert/Var r = 4–13`, and **`W_cert` is 4–10 times the true gap `K`** (e.g. Val₁₀/PPII, `m = 5`:
`2.8·10⁻⁴` against `3.2·10⁻⁵` nats; Ser₅/E, `m = 5`: `2.7·10⁻⁷` against `6.8·10⁻⁸`).  For the midpoint model the true gap is `10⁻⁹–10⁻⁵` and
the certified `W` is `10⁻⁷–10⁻³`: looser relative to the truth (the certificate cannot see that `r₀` is almost constant) but small in
absolute terms.  (iii) *At 20 residues* (no enumeration possible): `m = 5`, band 8: **`b_cert = 0.061 k_BT`, `s²_cert = 4.8·10⁻³`,
`W = 2.4·10⁻³` nats** for `m₋` (midpoint model: `0.29`, `1.2·10⁻³`, `6.5·10⁻⁴`); the Bennett bracket with a Chebyshev mean on the certified variance is
`[518.2608, 518.2659]`, as narrow as Hoeffding's with the same samples, and it would be 0.02 nats wide with 5 000 samples.  With `m = 4`
the certified `b` and `s²` are 2.1 and 5.3 and the route is useless (W = 1.5 nats) although Hoeffding's bracket is 0.03 nats — the certified
variance pays for the looseness of `γ_i` quadratically.  With analysis-only constants (`m = 3`) it is useless everywhere except Ser on the
strand (Ser₆: `W_cert = 2.4` nats, true gap 0.29).
(iv) *The window.*  With band 2 (a next-nearest-neighbour chain; the pairs beyond the window are in `u`) the certified inputs at 20 residues
are `b = 0.21`, `s² = 0.049`, `W = 0.024` nats (midpoint: `W = 0.0072`); with band 1: 0.49, 0.25, 0.12 (0.040).  The enumerated statistics of my
midpoint model agree with the coordinator's ANOVA chain on the same peptides — Val₈/PPII: band 1 `b = 0.086`, `σ = 0.013` (ANOVA chain
`w = 1`: 0.127, 0.011); band 2: 0.053, 0.0087 (0.058, 0.0071); all pairs: 0.014, 0.0009 (0.012, 0.0018) — so a banded anchored model is, like
the ANOVA chain, essentially the whole ensemble, and it comes with a certificate.
(v) *Do the remainder statistics extrapolate?*  Yes, linearly in the chain length, for `r = β(E − m₋)` under `π_{m₋}` (Val on PPII, `m = 5`):

<!--T:extrap-->
(to be filled)
<!--/T:extrap-->

The linear extrapolation from the two longest enumerated chains predicts the sampled mean and the sampled minimum at 20 residues within
2–9 % and the variance within 7–26 % (the variance is slightly super-linear).  (vi) The full table (140 rows, both models, every run) is in
`out/report_tables.md`; in all 132 enumerated runs `b ≤ b_cert`, `Var r ≤ s²_cert`, `0 ≤ K ≤ W(b, Var r) ≤ W_cert` (asserted)."""
R["⟨READ-3.7⟩"] = """`Σ_i c_i²` of the *certified* oscillations is `10⁻⁶–0.06 (k_BT)²` for Ser on the strand at `m = 4, 5`, 0.002–0.025 for
Val₆–Val₁₀ at `m = 5` and **0.109 at 20 residues** (so `D₂ ≤ Σc_i²/2 ≤ 0.055` for a product reference: `e^{D₂} ≤ 1.06`), 1–29 for Leu at `m = 5`;
at `m = 4` it is 4–30 for Val₆–Val₁₀, 79 for Val₂₀, 33 for Lys₄, `10³` and more for Leu; at `m = 3` `10¹–10⁵`.  The *exact* oscillations of the
remainder are 200–1 000 times smaller than the certified ones (their squares sum to `10⁻¹²–10⁻²`).  Comparison of the two routes on the same
certified data: at `m = 5` both are cheap (floor: cost number 0.03 at 20 residues; moment: `e^{D₂} ≤ 1.06`); at `m = 4` the floor with site
penalties still works (cost number 1.6 at 20 residues) while the moment bound from worst-case oscillations does not (`D₂ ≤ 40`): the floor
is weighted by how often the measure actually leaves the anchor, the oscillation bound is not."""
R["⟨READ-3.8⟩"] = """(i) The whole pipeline runs unchanged for OBC2 and passes the same checks (9 runs, sandwich never violated).
(ii) OBC2's certified constants are **3–8 times smaller than GBn2's for apolar side chains** (Val₆/E: `Γ₃, Γ₄, Γ₅ = 4.49, 0.084, 0.00079` against
12.96, 0.432, 0.0066 kcal/mol; Leu₈/E: 40.8, 2.07, 0.067 against 95.4, 7.29, 0.313) and about equal for serine (Ser₄/E: 0.755, 0.0048 against
0.729, 0.0068).  (iii) *The neck correction is what makes GBn2's constants large* [N, an ablation that is not a model anyone uses:
`x05_neck.py`, GBn2 with `m0 := 0`]: without the neck term `Γ₃, Γ₄, Γ₅` fall by factors 10, 26, 74 for Val₆/E (1.24, 0.017, `9·10⁻⁵`), by 12, 27,
69 for Leu₈/E and by 6 and 12 for Ser₄/E; the largest change of `ln B` under a single rotamer flip at the anchor — the small parameter of
§2.8 — is 0.27 with the neck, 0.06 without, 0.15 for OBC2 (Val₆/E).  The neck integral is a sharply peaked function of the distance (width
about 1 Å), so a rotamer flip switches whole neck contributions on and off.  So yes: the size of every constant in this report depends on
the neck correction, by about an order of magnitude per order of the expansion; the *structure* of the analysis does not."""
missing = [k for k in R if k not in t]
for k, v in R.items():
    t = t.replace(k, v)
tmp = path + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, path)
print("replaced", len(R) - len(missing), "placeholders; missing:", missing)
