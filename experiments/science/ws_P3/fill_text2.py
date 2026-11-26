"""P3: second one-off helper: final wording of the verdict paragraph and a few corrections (kept for the record)."""
import os, re
path = "/home/user/MetricChain/docs/science/workstreams/P3_REPORT.md"
t = open(path).read()
a = t.index("## 1. Verdicts in one paragraph")
b = t.index("## 2. Precise statements")
verdict = """## 1. Verdicts in one paragraph

**Is a floor certifiable by analysis for the remainder P2 measured?  By analysis alone:
rigorously yes, usefully only for serine on the strand.  By analysis of the tail plus
polynomially many evaluations: yes on extended backbones, with a certified `ln Z` at 20
residues; no on the helix.**  (i) A bound on the third-order constants `c_ijk` of the GBn2
polarisation energy that uses only the descreening tables and interval enclosures of
derivatives — no value of `g` — is proved here [P] and holds in all 562 triples of 44 of P2's
instances [M], but it exceeds the measured constants by a factor **200–1 400 for apolar side
chains (Val, Leu), 90–170 for Phe, 40–100 for Ser, 33–77 for Lys, 90–160 for the
heteropolymer**.  The floor built from it — P2's Statement 5(d),
`f + I₂g − Σγ_i[x_i ≠ x⁰_i]`, with certified constants — has an exact cost number
`Z(m)/Z(E) − 1` of 0.4, 1.1, 2.3 for Ser₄, Ser₅, Ser₆ on the strand (a working certificate:
1 009 evaluations of 531 441, and an exact certificate of the minimum), but 16, `10³`, `10⁵` for
Val₆, Val₈, Val₁₀ on the strand (a factor 8 per residue — faster than the domain grows),
`10⁴–10¹¹` for Val on polyproline II and `10²–10⁸⁹` on helices and for charged side chains.
(ii) The loss has one cause [M]: the cross term of GB is a sum over all atom pairs within the
range of the kernel, carrying `q_pq_q` of both signs, that cancels to about 1 % (Val₆: self
part −640, cross part +600, total −37 kcal/mol), and a term-by-term bound cannot see the
cancellation.  Term by term the bound is nearly sharp: with all charges but one pair switched
off it is within a median factor 1.1–6 of the exact constant and never below it (1 268 cases).
Every analytic device that keeps signed sums at a reference gains one power of the small
parameter (the relative change of a Born radius under one rotamer flip) — which is exactly
what one more order of the anchored expansion gains, without any loss.  (iii) Hence the recipe
that works [P]: **evaluate `g` on the Hamming ball of radius `m − 1` about an anchor**
(`Σ_{j<m} C(n,j)(k−1)^j` evaluations) **and bound only the remainder beyond order `m − 1`**, by the
same term-by-term bound summed over *all* `m`-subsets in closed form (seconds for 40 residues).
The certified remainder constant `Γ_m` grows linearly with the chain and falls by a factor
22–46 per order for Val on strand and PPII (`n = 12`, strand: `Γ₃ … Γ₆ = 36.9, 1.56, 0.039, 0.0008`
kcal/mol), 11–22 for Leu on strand and PPII, and only 5–8 for Leu on the helix (`n = 16`: 1 819,
370, 60, 8.0), where the recipe fails at every order tried.  (iv) With `m = 4` or `5` the
certified floor and ceiling are banded pairwise functions `m₋ ≤ E ≤ m₊` with exact partition
functions and exact samplers.  ⟨V⟩  (v) The theory division's formula
is confirmed on real numbers where it matters: the cost is the Boltzmann weight of the distance
to the *certified floor*, and a floor that is a function is far cheaper than a constant (Val₁₀
on the strand at `m = 4`: cost number 6.3 with the constant `Γ₄`, 0.022 with site penalties;
Lys₄ on the helix: 3.2 against 0.48), because the ensemble rarely leaves the neighbourhood of
the anchor.  With `m = 4` and site penalties the certificate is cheaper than enumeration from 4
(Ser) to 7 (Val) residues on, and its cost number reaches `10⁶` only near 230 residues for Val on
PPII [H: extrapolated exponent].  (vi) For the coordinator's Bennett bracket the same sandwich
gives all inputs exactly and without sampling: a one-sided floor `r ≥ 0` of `r = β(E − m₋)`, the
bounds `b ≤ 𝔼u`, `Var r ≤ 𝔼u²` with `u = β(m₊ − m₋)` an explicit banded function; at 20 residues
`b_cert = 0.061 k_BT`, `s²_cert = 4.8·10⁻³`, `W = 2.4·10⁻³` nats; on enumerated instances `W_cert` is
within 4–26 times the true Jensen gap at `m ≥ 4`, and the remainder statistics at 20 residues
are predicted within 2–9 % (mean, floor) and 7–26 % (variance) by linear extrapolation from
8–12 residues.  (vii) The neck correction of GBn2 is what makes its constants large: without
it they fall by a factor 10–70, and OBC2's are 2–8 times smaller for apolar side chains.
What remains assumed in every statement: the force field and the GB model themselves, the
rotamer grid, the rigid geometry, the fixed backbone, small exposed peptides; and — until
someone machine-checks it — my proofs, my code and a floating-point allowance.

---

"""
vnum = ("For Ace-Val₂₀-NMe on polyproline II (`3²⁰ = 3.49·10⁹` assignments): with `m = 4`, 9 921 evaluations of `g` certify `ln Z(E) ∈ [517.484, 519.220]` "
        "deterministically and, with 50 000 exact samples of `π_{m₋}`, `[518.2442, 518.2759]` at confidence 0.95; with `m = 5`, 87 441 evaluations "
        "(`2.5·10⁻⁵` of the domain) certify **`ln Z(E) ∈ [518.2332, 518.2937]` with no sampling**, `[518.2598, 518.2648]` with the samples; all brackets "
        "intersect; and `min E = −306.56871 ± 10⁻⁵` kcal/mol is certified at the anchor.  In 160 enumerated runs (5.5 million state checks) the "
        "sandwich was never violated and the true `ln Z` lay inside every bracket.")
t = t[:a] + verdict.replace("⟨V⟩", vnum) + t[b:]
fixes = [
    ("the heteropolymer\n`10⁴–10¹⁰⁵`", "the heteropolymer\n`7·10³–10¹⁰⁵`"),
    ("and for everything on the helix and everything charged (`10²–10⁸⁹`).", "for Phe₄ on the strand (18), and for everything on the helix and everything charged (`10²–10⁸⁹`)."),
    ("Val/PPII 4.1.", "Val/PPII 4.2."),
    ("`m = 5`: Val/PPII 0.002 (0.032 at 20 residues), Leu/PPII 0.002.", "`m = 5`: Val/PPII 0.002 (0.032 at 20 residues), Leu/PPII 0.003."),
    ("\"Impossible\"\n(cost number above `10⁶`): with analysis-only constants from 6–11 residues on (never possible for Val on PPII beyond 4); with `m = 4` near\n230 residues for Val on PPII [H], near 90 for Ser on the helix [H], at 5 for the heteropolymer [M]; with `m = 5` not within any length I can\nextrapolate to for Val and Leu on extended backbones, and at 12 residues for Leu on the helix [M: `4·10¹⁹`].",
     "\"Impossible\"\n(cost number above `10⁶`): with analysis-only constants from 3 (Lys), 6 (Ser on the helix), 8 (Val on PPII) and 12 (Val on the strand)\nresidues on, and near 36 for Ser on the strand [H]; with `m = 4` near 230 residues for Val on PPII [H], near 90 for Ser on the helix [H], at 5\nfor the heteropolymer [M]; with `m = 5` not within any length I can extrapolate to for Val and Leu on extended backbones, while for Leu on\nthe helix the constant-bound cost number is already `4·10¹⁹` at 12 residues (site penalties: 0.9 at 8 residues; not run at 12)."),
    ("`s²_cert/Var r = 4–13`, and **`W_cert` is 4–10 times the true gap `K`**", "`s²_cert/Var r = 4–15`, and with all pairs in the band **`W_cert` is 4–26 times the true gap `K`** (median about 9)"),
    ("as narrow as Hoeffding's with the same samples, and it would be 0.02 nats wide with 5 000 samples.", "as narrow as Hoeffding's with the same samples, and it would be 0.011 nats wide with 5 000 samples and 0.03 with 500."),
    ("The *exact* oscillations of the\nremainder are 200–1 000 times smaller than the certified ones (their squares sum to `10⁻¹²–10⁻²`).", "The *exact* oscillations of the\nremainder are 200–2 000 times smaller than the certified ones (their squares sum to `10⁻¹²–0.3`)."),
    ("at `m = 4` it is 4–30 for Val₆–Val₁₀, 79 for Val₂₀, 33 for Lys₄, `10³` and more for Leu; at `m = 3` `10¹–10⁵`.", "at `m = 4` it is 4–30 for Val₆–Val₁₀, 79 for Val₂₀, 33 for Lys₄, 400–4 000 for Leu; at `m = 3` `10¹–10⁵`."),
    ("OBC2's certified constants are **3–8 times smaller than GBn2's for apolar side chains**", "OBC2's certified constants are **2–8 times smaller than GBn2's for apolar side chains**"),
    ("the evidence is the agreement of\n  two certificates of different order and the 99 902 sampled states at which `E ≥ m₋` held.", "the evidence is the agreement of\n  certificates of different order and band, and the 200 000 sampled states of the four runs (22 739–29 321 distinct per run) at each of\n  which `E ≥ m₋` held."),
    ("the 79 enumerated instances in which the truth fell inside every bracket.", "the 160 enumerated runs in which the truth fell inside every bracket."),
    ("<!--T:bennett-->", "<!--T:bennett_sel-->"), ("<!--/T:bennett-->", "<!--/T:bennett_sel-->"),
    ("9. Two independent certificates of the same number: for Val₂₀/PPII the `m = 5`\nbrackets lie inside the `m = 4` brackets (§3.5).", "9. Several certificates of the same number: for Val₂₀/PPII the brackets of orders 4 and 5 and of bands 1, 2, 8 all intersect (§3.5)."),
]
miss = []
for old, new in fixes:
    if old not in t:
        miss.append(old[:60])
    t = t.replace(old, new)
tmp = path + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, path)
print("fixes applied:", len(fixes) - len(miss), "missing:", miss)
