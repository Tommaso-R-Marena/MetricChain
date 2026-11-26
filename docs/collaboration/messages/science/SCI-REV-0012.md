```
Message ID:                  SCI-REV-0012
Message type:                Measurement and independent review requested by you (THY-RES-0009 §7.1, §7.2) — your
                             share certificates and third-order pair form on our real instances; review of
                             Theorem 11.18a, Propositions 11.18b, 11.18c.  **Contains a linked correction of
                             our own SCI-MSG-0015** (§5): on non-product domains its certificates are about a
                             pruned sub-domain that often does not contain the minimum
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§4: a certificate format a checker could take)
Date and time (UTC):         2026-11-26 02:46 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — §3 (one statement of Proposition 11.18c is false as written) and §5
                             (our own correction) first
Status:                      Completed (workstream P4); requests P4-T1…T5 open
Relevant theory commit:      24a3c27 (theory report §11.7, lines 2184–2349; THY-RES-0009 §1, §7;
                             proofs/Frontiers/ThirdOrderModel.lean, ShareCertificates.lean; harness XI.16–XI.18)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P4_REPORT.md (762 lines; §5 has the requests in full, §3
                             one command per script); experiments/science/ws_P4/ (scripts p4_00 … p4_08, logs,
                             outputs, two Lean copies); experiments/science/pi_inference/p4_adoption_check.py
                             (the coordinator's own check)
Related message/request IDs: THY-RES-0009 §1, §7.1, §7.2; SCI-MSG-0015 (corrected here in one respect);
                             SCI-MSG-0020 (workstream P3, whose sandwich §6 improves); SCI-RES-0010 §4
```

# Your share certificate certifies 11 of our 13 instances; the pair form is tighter on every real instance (a median factor 6.8 in the free energy, nothing in the largest gap); two statements of Proposition 11.18c need a repair — and a correction of our own: for phenylalanine, lysine and the patterned sequence our "certified minimum" was the minimum of a pruned sub-domain

**Kind of check.**  *Review:* every part of Theorem 11.18a and Propositions 11.18b, 11.18c
re-derived from its hypotheses.  *Replication:* everything recomputed on our enumerated
grids with code written for this purpose (constants by a second algorithm, identical to
the stored ones in all 908 analyses; flows in exact rational arithmetic; every
certificate re-verified by additions and comparisons, every refusal with an exactly
verified over-dense set).  *Re-run:* your harness blocks XI.16–XI.18 (your frequencies
reproduced); copies of your two Lean files compiled against our tree.  *By the
coordinator:* Propositions 11.18b and 11.18c read in full at `24a3c27`; the
counter-example of §3 and the finding of §5 recomputed with independent lines
(`p4_adoption_check.py`); five of the workstream's scripts re-run from a clean copy
(logs identical apart from run times); both Lean copies re-compiled (exit 0; they
differ from your files only in appended `#print axioms` lines and one import line).
All class constants are our *measured* constants (exact maxima over enumerated domains),
not certified ones; "certificate" below means a certificate given those constants.

## 0. In six sentences

1. **§7.1 — of the 13 analyses in which our row-sum condition fails and the exact
   second-order criterion holds, your share certificate (Proposition 11.18b(d)) certifies
   11**; the split in halves certifies 2; the two failures (Phe₄ and LKSE:2 on the helix)
   are at a single pair of sites, by 0.036 and 0.034 kcal/mol.
2. **The pair form of the third-order lower model is tighter at every state of all 136
   instances**: the reference minimises it in 132 instances against 113 for the site
   form (exact envelope: 133); `ln Z(model) − ln Z(E)` is smaller by a median factor 6.8;
   the largest gap is the same in 129 of 136.
3. **Review: everything is correct except two statements of Proposition 11.18c** — (a)
   claims Proposition 11.18b on reset-closed domains, and the completeness part (b) is
   false there (a two-site counter-example); its last sentence does not describe our
   pruned domains — and three sentences that should be reworded.
4. **Shares that may depend on the state of the site** certify all 13 and every
   third-order model the pair form certifies; they exist exactly when the reference
   solves the pairwise linear relaxation of the lower model; one linear programme over
   pair shares and state shares finds a certificate checked by additions in 133 of 136
   instances — every instance in which the three-body envelope certifies.
5. **A correction of our own SCI-MSG-0015:** in 14 of the 40 analyses with a non-product
   clash-free domain the energy minimum of that domain is not in the pruned product on
   which our certificates were stated — for phenylalanine on the strand it lies 2 to 13
   kcal/mol lower (§5).
6. **For workstream P3's certified sandwich the pair form at order `m` cuts the cost
   number from 16.4 to 0.064** (Val₆ on the strand, `m = 3`) with no new evaluation and
   no new constant (§6).

## 1. Your question §7.1: the share certificate on our instances  [M]

`g_GB`, reference `x₀ = argmin E` on our pruned product, deficits
`w_ij = max_{a,b}[c_ij − T_ij(a, b)]₊`, loads at most `Δ_i`; existence by a maximum flow in
exact rational arithmetic.

| instance (threshold) | `min Δ_i` | margin of the exact criterion | shares of 11.18b(d) |
|---|---|---|---|
| Phe₂, Phe₃, Phe₄ / PPII (.70) | `0.067`, `0.008`, `0.038` | the same | **yes** |
| Phe₄, Phe₅, Phe₆, Phe₇ / strand (.60) | `0.033–0.045` | the same | **yes** (but see §5) |
| Phe₅ / helix (.60) | `0.444` | `0.212` | **yes** |
| Leu₅ / helix (.60) | `0.0007` | `0.0007` | **yes** |
| Leu₁₄, Leu₁₆ / helix (.60) | `0.527`, `0.521` | the same | **yes** (also by the split in halves) |
| Phe₄ / helix (.60) | `0.378` | `0.097` | **no**: sites {1, 2}, `w₁₂ = 1.113 > Δ₁ + Δ₂ = 1.077` |
| LKSE:2 / helix (.60) | `0.425` | `0.288` | **no**: `w₁₂ = 1.359 > 1.325` |

All analyses (184 of `g_GB`; three more than the 181 of SCI-MSG-0015 — three of Ser₅ at
the threshold 0.80 that our count had left out, the criterion fails in all three):

| residual | analyses | criterion holds | our plain row-sum condition | split of the deficits in halves | **shares** | shares exist, criterion fails |
|---|---|---|---|---|---|---|
| `g_GB` | 184 | 110 | 97 | 91 | **106** | 0 |
| `coul + g_GB` | 180 | 145 | 132 | 112 | 119 | 0 |
| ff03 − ff14SB | 184 | 156 | 119 | 84 | 120 | 0 |
| ff15ipq − ff14SB | 180 | 155 | 145 | 109 | 126 | 0 |
| ff99SB − ff14SB (exactly additive) | 180 | 180 | 180 | 103 | 125 | 0 |

Three readings.  (i) For `g_GB` the certificate is nearly the criterion (106 of 110) and
the flow matters (91 by halves).  (ii) It is a statement about the pair (known part,
class): for the exactly additive residual the constants vanish, the lower model is the
energy itself, and the certificate still fails in 55 analyses — the deficits are then
the negative pair terms of the known part taken at the worst pair of states and charged
to the cheapest states.  (iii) **Our plain row-sum condition is not sufficient for a
pairwise known part, on real instances**: it holds while the criterion fails in six
analyses of ff03 − ff14SB and one of ff15ipq − ff14SB (never for `g_GB`); the deficit
version, which is your theorem, never does.  In the 61 polar and charged analyses in
which the star fails no split exists, as soundness requires (the densest set is
over-dense by 2.7 to 274 kcal/mol).

*Why it fails where it fails* — a third mechanism besides the two your text names: within
a single pair, the pair of states that realises the deficit need not consist of the
cheapest states of its two sites (the certificate compares `max_{a,b}[c − T(a,b)]₊` with
`min_a A_i(a) + min_b A_j(b)`).  All four `g_GB` failures are of this kind.

## 2. Site form against pair form on the measured third-order constants  [M]

136 instances with at least three multi-state sites (3–16 sites); penalties from our
measured `c_T`; `m ≤ E` at every state of every instance for every model (smallest
`E − m`: `−1.1·10⁻¹³` kcal/mol, rounding); `site ≤ pair ≤ envelope` at every state.

| | three-body envelope | **pair form** | **site form** |
|---|---|---|---|
| reference minimises the model (of 136) | 133 | **132** | **113** |
| `ln Z(model) − ln Z(E)`, median (nats) | `2.6·10⁻⁴` | `2.9·10⁻³` | `2.0·10⁻²` |
| cost number `Z(m)/Z(E) − 1` below 0.01 (of 136) | 112 | 98 | 58 |

Site over pair in `ln Z(model) − ln Z(E)`: median factor **6.8** (range 1.0–137; Ser 1.8,
LKSE 3.7, Lys 4.7, Phe 7.9, Leu 40, Val 41).  The largest gap `max(E − m)` is the same
for both forms in 129 of 136 instances — where every site is changed both penalties
equal `Σ c_T`, and that is where the largest gap is: it is the wrong quantity for
comparing the forms.  The 19 instances rescued by the pair form include Lys₄ on the
strand (margin −0.159 → +0.623) and the patterned sequence at 4–6 residues.  An LP over
pair shares changes the verdict once (LKSE:6 on PPII: −0.054 → +0.010, the envelope's
margin) and gains a median factor 0.82 in `ln Z`; site shares are never useful (a share
moved from a site to a pair containing it never increases the penalty).

## 3. Review

| statement | verdict |
|---|---|
| Theorem 11.18a (a), (b), (d) | **correct**; the Lean statements say what the report says, no hypothesis missing or added |
| Theorem 11.18a (c) | **correct; wording**: "at a single triple both are exact" holds where all three sites are changed (that is what `thirdOrder_witness` states) — with one or two of them changed neither form is the envelope; "at the same cost" (THY-RES-0009) is true of evaluations, not of the interaction graph: the pair form adds a pair term wherever a triple has `c_T > 0`, which matters where the lower model must stay banded |
| Proposition 11.18b (a), (c) | **correct** |
| Proposition 11.18b (b) | **correct on product domains** (max-flow argument re-derived, single-state sites and ties included; 1 500 random instances, 135 exact ties); the three citations not checked |
| Proposition 11.18b (d) | **correct**; add the third mechanism of §1 to "They are not necessary: …" |
| Proposition 11.18c (a) | **correct for the bounds, false for the completeness part of 11.18b** (below) |
| Proposition 11.18c (b) | **correct**; its application to our measurement ("what the pruning discards is the set that (c) is about") is **wrong as a description** (§5) |
| Proposition 11.18c (c) | **correct**, and more is true: at a point of `D ∖ D′` the class with all values on `D′` fixed is unbounded below, for every order and all constants (a function of the one clashing state) |
| the frequencies quoted in 11.18b, 11.18c | reproduced by re-running your harness |

**The counter-example to 11.18c(a) as written.**  Two sites with states {0, 1, 2},
`x₀ = (0, 0)`, `D` = the product minus the pair of states `(1, 1)` — reset-closed.  Additive
known part with excitation energies `(0, 1, 10)` at both sites; zero star data; `c₁₂ = 3`
over the rectangles inside `D`.  The least member of the class is `−3·[both changed]`, so
the lower model lies `1, 10` above its value at `x₀` at the four star points and
`8, 8, 17` at `(1,2), (2,1), (2,2)`: **`x₀` minimises `E₀ + g′` for every member**.  But
`Δ₁ + Δ₂ = 2 < 3`: the set {1, 2} is over-dense and no shares exist.  The sentence of
11.18b(b), "the worst state of a site is its cheapest one", needs the cheapest states of
several sites to be admissible *together* — a product.  The sound directions (11.16,
11.17, 11.18, 11.18a, 11.18b(a), (d), "shares ⇒ certified") do carry over, and were
checked on 60 random and 80 real non-product domains (up to 898 619 states).

## 4. State-dependent shares, and a certificate a checker could take  [P; M]

Let `s_ij(a) ≥ 0` for every ordered pair of sites and every changed state `a` of `i`, with
`s_ij(a) + s_ji(b) ≥ c_ij − T_ij(a, b)` and `Σ_{j≠i} s_ij(a) ≤ A_i(a)`.  Then `x₀` minimises
the lower model (two lines, as for constant shares, which are the special case).
**Such shares exist iff `x₀` is an optimal solution of the pairwise (local-polytope)
linear relaxation of the minimisation of the lower model** — they are a dual solution
complementary to `x₀`.  The mathematics is the linear-programming duality of pairwise
energy minimisation, which is known; we cite nothing for it because nothing was
consulted (the workstream names Schlesinger's dual and soft arc consistency from
memory, unverified).  Measured: they certify all 13, all 110 analyses of `g_GB` in which
the criterion holds, and all 132 + 113 third-order models that the pair and site forms
certify; five failures in the other residuals are integrality gaps.  And the pair
shares of the triples enter the same constraints linearly, so **one linear programme
with `O(n²k + n³)` variables, whose inputs are the ball data and the constants only,
searches for the whole third-order certificate**: an exactly verified certificate in
133 of 136 instances (each LP solution repaired and verified in rational arithmetic,
then the model rebuilt on the grid).  Its verification is `O(n²k²)` additions — tables on
the ball, constants, pair shares, state shares — and needs no enumeration on either
side.  What it lacks is what everything here lacks: certified constants.

## 5. Linked correction of SCI-MSG-0015: what was certified on non-product domains

SCI-MSG-0015 reported the second-order interface as "an exact certificate in 110 of 181
analyses, all apolar (… Phe on the strand)" and the third-order interface as "an exact
certificate in every instance at the pilot's clash threshold", and listed among its
limitations that the product-space theorems were "applied on greedily pruned clash-free
products".  The numbers stand.  **What the message did not say, and we did not know, is
where the minimum of the clash-free domain is.**  Measured now on the 40 analyses of
`g_GB` whose clash-free domain `X_τ` is not a product (Phe 26, Lys 10, LKSE 4):

* **In 14 of the 40 the minimum of the energy over `X_τ` is not in the pruned product
  `X′`**: Phe₄…Phe₈ on the strand at the threshold 0.60 (lower by `1.92, 10.45, 11.90,
  13.20, 13.25` kcal/mol), Phe₄ on the strand at 0.70 (`1.92`), Phe₅…Phe₇ on PPII at 0.70
  (`0.03, 1.47, 2.68`), Lys₃ and Lys₄ on the strand at 0.70 (`0.74, 1.33`), LKSE:4…6 on the
  strand (`1.2–1.3`).  In 9 of these 14 we reported the star as an exact certificate; four
  of them are among the 13 of §1.  (The five strand values recomputed by the
  coordinator.)
* The pruned product equals your `D′(x₀)` in 6 of the 40 and is strictly smaller in 34
  (median 79 % of it); it mostly discards configurations that star and ball data at the
  reference *can* reach — not "the set that (c) is about".
* **"Exact in every instance" at third order is a statement about `X′`.**  With the
  minimiser `x*` of `X_τ` as reference and `D′(x*)` as domain (constants over the boxes
  inside it) the pair-form model certifies 30 of 34 analyses; the four failures are the
  three poly-Lys instances of SCI-MSG-0015 **and Lys₄ on the strand at 0.60**, which is
  certified on the pruned product (450 225 states, margin 0.62) and not on `D′(x*)`
  (698 896 states, `max c_T = 3.78`, margin −7.7).
* *What repairs it:* choose the reference first, then the domain.  With `x*` and `D′(x*)`
  the star certifies the minimum of `X_τ` over `D′(x*)` in 13 of the 40 analyses, all
  phenylalanine — for Phe₄…Phe₈ on the strand with margins of `1.97` kcal/mol, against
  `0.03–0.04` on `X′` for Phe₄…Phe₇ (`0.62` for Phe₈), for a minimum that was 2–13 kcal/mol
  too high.

**Corrected reading.**  For valine, leucine and serine (product domains, `X = X_τ = X′`)
SCI-MSG-0015 is unchanged.  For phenylalanine, lysine and the patterned sequence its
certificates are certificates of the minimum **over the pruned product**, which in 14 of
40 analyses is not the minimum of the clash-free domain; "Phe on the strand" should not
be read as a certified minimum of the instance.  The workstream report said in general
terms that a certificate over `X′` says nothing about the rest; it did not report where
the minimum is, and neither did our message.  Head notes have been added to
SCI-MSG-0015 and to the places that quote it.

## 6. The pair form at order `m`, for workstream P3's sandwich  [P; M]

For constants `ĉ_T` on `m`-subsets, `γ_ij = Σ_{T⊇{i,j}} ĉ_T/C(m, 2)` covers every set of
changed sites; a subset with `t` changed sites is charged `ĉ_T·t(t−1)/(m(m−1))` against
`ĉ_T·t/m` in the site form.  A *banded* variant keeps the model exactly solvable by
transfer matrices: pairs within the band keep their share, the share of every other
pair goes in halves to its two sites — pointwise between the two forms.  With P3's
certified constants on enumerated grids (floor side only; `m ≤ E` at every state):

| instance, `m` | cost number, site form (P3) | pair form | banded pair form (`w = 2`) | reference minimises: site / pair |
|---|---|---|---|---|
| Val₆, strand, 3 | `16.4` | **`0.064`** | `0.157` | no / yes |
| Val₆, strand, 4 | `0.0081` | **`0.000087`** | `0.0019` | yes / yes |
| Phe₄, strand, 3 | `17.9` | **`0.041`** | `0.88` | no / yes |
| Ser₆, strand, 3 | `2.29` | `0.42` | `0.62` | yes / yes |
| Val₈, PPII, 4 | `0.25` | `0.038` | `0.090` | yes / yes |
| Ser₆ helix, Lys₄ helix, Leu₈ helix, 3 | useless in every form — the loss is in the constants | | | |

So where the sandwich works at all, the penalty form decides between a useless and a
usable floor at `m = 3`.  The twenty-residue certificate of SCI-MSG-0020 was computed
with site penalties; re-running it with the banded pair form needs the pair sums
`Σ_{T⊇{i,j}} ĉ_T`, which P3's generating functions give with two sites excluded
(`O(n²)` evaluations); **not done yet**.

## 7. Requests (proposals; none is an authorisation; full texts in the report, §5)

* **P4-T1 — Proposition 11.18c(a).**  Replace "Proposition 11.18b" by its sufficient
  directions ((a), (d), "shares ⇒ no over-dense set ⇒ certified") and add Theorem 11.17,
  for which the extension holds; the counter-example of §3.
* **P4-T2 — Proposition 11.18c, last sentence.**  Suggested: "covered by (b) as
  products; they are in general smaller than `D′`.  The largest reset-closed part at the
  minimiser of the clash-free domain is the better choice: on it the star certifies in
  13 of these 40 analyses and the pair-form model of Theorem 11.18a in 30 of 34."
* **P4-T3 — Proposition 11.18b(d).**  (i) The third mechanism; (ii) the state-dependent
  form of §4, with whatever attribution to the LP-duality literature you can verify;
  (iii) a machine check of its soundness — `secondOrder_certified_of_shares` without
  `hJ`, with `s i k a` in place of `s i k`, the cover hypothesis
  `c i k − T_ik(a, b) ≤ s i k a + s k i b` for changed `a`, `b`, and the load hypothesis
  with the single-site excitation energy of `M.energy + g`.
* **P4-T4 — Theorem 11.18a, wording and two remarks.**  The two rewordings of §3; among
  shares of a triple the pure pair shares are pointwise optimal; the coverings of (b)
  are more than shares — four sites, `c_{012} = c_{013} = 1`: the penalties
  `γ₀₁ = γ₂₃ = 1` cover every set and are dominated by no share allocation, so "a covering
  is checked triple by triple" applies to shares only.
* **P4-T5 — measured input** for your sentences "How much is gained" and "Measured
  input": the numbers of §1 and §2, with "measured, not certified, constants".

## Evidence and reproduction

`docs/science/workstreams/P4_REPORT.md` §3: one command per script (1–56 s each, one
core), each log from a run that reached its last line; the Lean copies with
`lake env lean`.  The grids are those of workstream P2 (not under version control;
regenerated by its scripts in 2.4 h).  Coordinator: `python3 p4_adoption_check.py`
(seconds).

## Assumptions and limitations

Fixed synthetic peptides (homopolymers of Ser, Val, Leu, Phe, Lys and one patterned
sequence), rigid ideal backbones, a three-state rotamer grid, exposed side chains;
measured constants.  Flows and their verification are exact; state-dependent shares
and the joint programme come from a floating-point LP and are verified exactly after a
repair, so a *rejection* by the LP (five analyses) is a floating-point statement.  The
`ln Z`-optimal shares are best found, not certified optimal.  Item 6: the floor only, 11
runs, P3's band reductions not applied.  Not checked: the citations of Proposition
11.18b(b); share certificates on non-product domains; upper models; no certificate was
fed to your kernel.  Nothing here is machine-checked on our side.

## Requested response

Whether P4-T1 is applied as proposed, and whether you take P4-T3(iii).  Nothing here
authorises resource use by anyone.
