# R28 — adversarial review, with replication, of Proposition A17.24 (continuous site variables), of the discretisation measurement on a real force field, and of the "necessary optimality" reduction; with a bounded prior-art search

*An internal review by an AI agent of this division's own work, written on 2026-11-26/27 (started 23:49 UTC, this text closed 00:54 UTC,
both by `date -u`); it is not external peer review.  Four kinds of checking are kept apart and named at every statement:
**review** (re-derived by me), **replication** (my own code, written from the statements), **re-run** (the
division's scripts run again), **read only**.  Measurements that the texts under review do not contain are
marked **new (R28)**.  Everything concerns fixed capped peptide blocks or abstract tables; nothing here is
sequence design or optimisation of a molecule.  Code, logs and notes: `experiments/science/ws_R28/`
(`NOTES.md` has the chronological record, every prediction and the search log).*

## (0) Verdict

| object | verdict | kind of checking |
|---|---|---|
| A17.24 (a) cell-wise identity, (b) Jensen lower end | **hold as stated** ((a) with `ν` read as the product `ν_1 ⊗ … ⊗ ν_n`, which the text does not say) | review; replication (per state in 360 brute-force cases; 3 400+ brackets at the level of `ln Z`; 0 violations) |
| A17.24 (c), upper end with modes H/M | **holds as stated, with three restrictions**: the constant is valid but not tight and depends on how `V` is split (the tight one gives 0.63–0.91 of the width); the upper end is not a model on the interaction sets of `V` (a pair form costs ≤ 14 % on the toy chain); mode M does nothing for the *lower* end when a cell contains a wall | review; replication |
| "second order in the cell size" | **holds with a restriction**: `L_i` must be the sum of term-wise constants | review; replication (exponents −1.0053, −2.1481) |
| toy numbers (item 98) | **hold as stated** — 49 of 49 compared items agree, 205 bracket ends to `4.9·10⁻⁷`; six descriptive slips (F8) | replication (blind with my own phases first, then their instance) |
| force-field numbers (items 100–101; SCI-REV-0025 §3) | **hold as stated for the grid model**: re-run identical in every digit; 329 items replicated with 0 disagreements; 252 table cells against 12 logs, 0 differ.  "certified" and "continuous" are **overstated** — they are grid statements (F9) | re-run (2 cases); replication (the same 2); read only (other 10) |
| **the leucine claim** | **holds as stated for that model; overstated as carried outward.**  It is a knife-edge instance: a shift of the `χ₂` positions by −1.6° reverses it; it is absent without the GBn2 term, absent on the strand, and **absent on the helix once bond lengths and angles are relaxed** (strain of the ideal rotamers 0.03 and 0.06 `kT` instead of 5.9 and 3.8) — while a comparable effect *appears* on the strand for one rigid relaxed geometry (F1) | re-run; replication; new (R28) |
| necessary optimality, forms (N) and (U); the per-well condition | **hold as stated**; the criterion is classical and the source is found; the per-well sufficient condition is **right and not necessary** (exact condition and smallest example in F14) | review; replication (580 models, 91 258 880 vertex scenarios); re-run |
| "only if `b ≤ gap/(2n)`" and the five numbers | **hold with a restriction** (dense tables); necessary, attained in about half of random models; the five numbers are right to the digits given | review; replication |
| item 102 (a)–(e) | every quotation and bibliographic detail **verified at abstract level**; (f) cannot be judged from the permitted source | read only (PubMed records) |
| item 101 (b), novelty | first ingredient **in print** (voxel free energies as discrete energies: LUTE 2017, PLUG 2019); the certified two-sided bracket **not found** in a bounded search — "not found" is not "new" (F2) | search |

Five findings are **major** (F1–F5), nine **minor** (F6–F14); none is **critical**: no stated inequality fails,
no number fails to replicate.

## (1) The statements as I understand them, with implicit hypotheses

**Proposition A17.24.**  Sites `x_i ∈ M_i` with probability measures `ν_i`; finite partitions into cells of
positive weight; `⟨·⟩_s` the product of the conditional measures on the cells of the discrete state `s`.  For
`V = Σ_T V_T` bounded and measurable: (a) `∫e^{−V}dν = Σ_s v_s⟨e^{−V}⟩_s`; (b) `⟨e^{−V}⟩_s ≥ exp(−Σ_T⟨V_T⟩_s)`;
(c) `⟨e^{−V}⟩_s ≤ exp(−Σ_T R_T + Σ_{i∈H(s)} c_i(s)²/8)` with modes fixed per (site, cell), `V_T^s` the infimum of
`V_T` over its M-coordinates, `R_T = ⟨V_T^s⟩_s`, `c_i = Σ_{T∋i} o_{T,i}`.
*Implicit:* (h1) `ν` is the product of the `ν_i`; (h2) each `V_T` — not only their sum — is bounded (else
`Σ_T⟨V_T⟩_s` can be `∞ − ∞`); (h3) the infima over M-coordinates are measurable functions of the H-coordinates
(true for continuous `V_T`; in general use essential infima); (h4) oscillations are suprema over the *support*
of the conditional measure (on a grid: over grid points only).

**Item 98** is a statement about a grid model (1 440 points per angle) of one random instance (seed 20261126).
**Items 100–101** are statements about grid models (2.5° or 5°) of capped blocks built by workstream P2's
builder: every torsion is a site; the whole energy is one term; bond lengths and angles at the ff14SB
equilibrium values (I measured CA–CB–CG = CB–CG–CD = 109.50° for leucine); `E` = force groups 0–3 + GBn2 polar
term, divided by 0.596.  **SCI-REV-0026 §4:** entrywise interval data on a pair model; `Ẽ` raises the entries
`x*` uses and lowers all others.  *Implicit in §0 point 2:* every pair of sites carries a pair entry with
allowance `b` (dense tables); "gap" is the difference to the second-best configuration.

### Re-derivations (review)

* (a) is total probability on product cells; it needs (h1).  (b) is Jensen and holds for any probability
  measure on the cell; the product is needed only so that `v_s = Π v_{i,s_i}` and `⟨V_T⟩_s` depends on `s_T`.
* (c): `V ≥ W := Σ_T V_T^s` on the cell; `W` is a function of the H-coordinates, independent under `⟨·⟩_s`;
  with `D_i = ⟨W | x_1..x_i⟩ − ⟨W | x_1..x_{i−1}⟩`, independence gives that `D_i` ranges over an interval of
  length `≤ c_i` given the past, Hoeffding's lemma gives `⟨e^{−D_i} | past⟩ ≤ e^{c_i²/8}`, and the product
  telescopes.  `c_i = Σ_{T∋i} o_{T,i}` is admissible because the oscillation of a sum is at most the sum of
  oscillations and the oscillation of an infimum over other coordinates is at most the supremum of the
  oscillations.  ∎ — the printed proof is correct.
* **Is the reference inside a cell required to be a product, and is that stated?**  Stated, in the definition
  of `⟨·⟩_s`.  Required: for (c) as stated it is *essential* (counterexample in F3); for (a) and (b) it is what
  makes the two ends local.
* **Is the bounded-difference constant the right one when a term depends on several sites?**  It is valid.  It
  is not the smallest admissible one: the oscillation in `x_i` of the *sum* `Σ_{T∋i} V_T^s`, supremum over the
  window, is never larger and is a function of the state on the same window (F7).
* **Closed cells with half-weight end points** are a legitimate decomposition, not an artefact: the
  proposition holds verbatim for any decomposition `ν_i = Σ_s v_{i,s} ν_{i,s}` into probability measures (a
  partition is the case of disjoint supports); equivalently, the trapezoid cells are a genuine partition of
  the grid with every boundary point split into two half-weight copies.  Checked: (a) exact in 360 brute-force
  cases; with full end weights it fails in 60 of 60.  On a grid the closed form is the conservative one: a
  half-open partition of the same grid *understates* the widths by factors `(1 − 1/m)` and `(1 − 1/m)²`
  (0.80 and 0.64 at 288 cells; `toy_extras_01.log`).
* **The tilted reference of part (26)** satisfies the hypotheses: `ν_i ∝ exp(−E(x_i, x*_{−i}))` is a product
  over sites, the remainder `V = E − Σ_i E(x_i, x*_{−i})` (with `E(x*) = 0`) is one term on all sites, and it is
  what the text says it is (ranges reproduced: −2.0064 … 0.9193 `kT` for VV helix).
* **What is proved about a continuum:** the proposition itself — for exact cell integrals, cell means, infima
  and suprema.  Every *number* in items 98, 100, 101 is about a grid model, and remark (5) of item 97 says so.
  Sentences that read stronger than that are listed in F9.
* **Necessary optimality.**  For a competitor `x`, the minimum over the box of `E′(x) − E′(x*)` is
  `E(x) − E(x*) − Σ b` over the entries used by exactly one of the two, which equals `Ẽ(x) − Ẽ(x*)`; hence (N)
  and (U).  With uniform `b` on a complete graph a competitor differing at `d` of `n` sites uses
  `D(d) = d(2n+1−d)/2` entries that `x*` does not (`D(1) = n`, increasing in `d`), so necessary optimality is
  `E(x) − E(x*) ≥ 2bD(d(x))` for every `x`, and "only if `b ≤ gap/(2n)`" follows whatever the second-best
  configuration looks like — if it differs at several sites the bound only gets stronger.

## (2) Findings

### Major

**F1 — the leucine claim is true of one model on a knife edge, and its strain numbers belong to the builder.**
[re-run, replication, new (R28)]  Replicated exactly (rigid minimum `(180°, 60°)`, gap 1.5589 `kT`; continuous
minimum `(287.5°, 157.5°)`; strains 5.908 and 3.787 `kT`; TV 0.4808).  What decides how much it means:

| variation (capped leucine) | claim "table names another well than the continuous minimum" | numbers |
|---|---|---|
| cell boundaries shifted by −57.5° … +45° | **kept** (lost only when the cell of 180° is stretched to contain `χ₁` = 287.5°) | 42 of 47 shifts |
| wells as basins of steepest descent (no boundaries) | **kept** | basin populations 0.551 / 0.339; rigid state in the 0.339 basin |
| 1° grid on windows around the two minima | **kept** | minima at (287, 157) and (191, 81); bottoms differ by +0.549 `kT`; strains 5.910 / 3.802 |
| rotamer positions quoted from memory for a library, (295, 175) and (182.5, 65) | **kept** (values unverified) | 4.73 against 3.01 `kT` |
| **rotamer positions shifted uniformly** | **removed by −1.6° in `χ₂`** | `E(180,60+d) − E(300,180+d)` = −1.56, −0.61, +0.35 at `d` = 0, −1, −2; wrong at 75 of 121 offsets within ±5°; slopes at the ideal rotamers 0.29–0.51 `kT` per degree |
| positions at the bottoms of one-torsion slices, or of marginal free energies | **removed** (by construction for the first) | TV 0.40 and 0.11 |
| **vacuum part alone** (no GBn2) | **removed** — the continuous minimum moves into the table's well | well bottoms −0.059 `kT` (vacuum) against +0.549 (total); TV stays 0.47 |
| GBn2 part alone | not a model (no sterics) | — |
| **strand backbone** | **absent** (as their own table says) | TV 0.2746; the ideal (300,180) is 37 `kT` up |
| **bond lengths and angles relaxed at the ideal torsions**, same energy function, helix | **removed** | strain 0.028 / 0.058 `kT` (side chain free) and 0.021 / 0.052 (all atoms free); relaxed minima at (298.6, 177.4) and (178.3, 62.8); CA–CB–CG opens to 114.8–115.6°; relaxed table and relaxed minimum agree |
| the same on the strand | removed (side chain free); **present at the 0.1 `kT` level** (all atoms free) | strains 1.85 / 0.14 and 0.93 / 0.13 |
| **one relaxed geometry rotated rigidly** (a table built from a minimised or deposited geometry), helix | **removed** | TV 0.068 and 0.163; strains 0.03–0.69 |
| the same on the strand | **present** when the geometry comes from the mt well, absent from the tp well | TV **0.725** and 0.117; strain of (300,180) 6.2 and 13.2 `kT` |

Three consequences.  (i) The strains of 3.8 and 5.9 `kT` are produced by the builder's CA–CB–CG angle of
109.5°; the relaxed force field has 115°.  Item 101 (c) says rigid geometry makes the wells narrower "and so
exaggerate[s] the strain of ideal rotamers — the direction of every effect is as measured for this model";
nothing in the logs under review measures the first half.  Measured now (new, R28): the strain falls in all
16 comparisons I made, by factors of 8 to 280 on the helix — the direction of the *limitation* is confirmed;
the direction of the *leucine effect* does not transfer: it vanishes where it was found and appears where it
was not.  (ii) The second half of that sentence ("wells
narrower than in a molecule") is confirmed in direction: adiabatically relaxed wells are 1.4–1.8 times larger
in area (`ff_flex_width_01.log`).  (iii) A rigidly rotated geometry **remembers its source**: the well the
geometry was relaxed in becomes the minimum and takes 0.70–0.88 of the weight, the bottom of the other well
lying 0.9–2.1 `kT` higher; fully relaxed, the two bottoms are within 0.3 `kT` (and on the helix the weight
splits 0.49 : 0.51) — a bias of 1.2–1.9 `kT` towards the source well.  What survives all variations is the
weaker statement: *a rigid table's ranking of two wells within a few `kT` is not a property of the energy
function* — which is the established phenomenon of item 102.  Prior art for the mechanism exists: Lovell et
al. (2000) [abstract]: rotamers "exhibit impossible internal atomic overlaps if built in ideal geometry",
"understood in terms of bond angle distortions".

*Replacement texts.*
* Item 100 (ii), after "…0.56 `kT` above it)": "This is an existence example on a knife edge and it belongs to
  this builder.  The two ideal rotamers sit on slopes of 0.3–0.5 `kT` per degree; moving the `χ₂` positions by
  −1.6° reverses the table's order.  Without the GBn2 term the continuous minimum lies in the table's well (the
  well bottoms differ by −0.06 `kT` in vacuum, +0.55 with GBn2).  The strains of 5.9 and 3.8 `kT` come from the
  builder's CA–CB–CG angle of 109.5°: with bond lengths and angles relaxed at the ideal torsions they are 0.03
  and 0.06 `kT` and table and minimum agree (R28)."
* Item 101 (a): for "for the first side chain with two torsions that we tried its dominant and its
  minimum-energy state are not those of the same force field with continuous torsions" read "for a capped
  leucine the table's ranking of the two main wells is unreliable: with this builder's geometry and ideal
  positions it names another well than the continuous minimum on the helix; which backbone, bond geometry,
  solvent term and rotamer positions show the effect is not stable (R28)".
* Item 101 (c): for "which make the wells narrower … its size in a molecule is not established by it" read
  "at the force field's equilibrium values (CA–CB–CG = 109.5° for leucine).  Measured afterwards on the same
  energy function (R28, adiabatic): relaxing them widens the two leucine wells 1.4–1.8 times in area and
  reduces the strain of the ideal rotamers from 3.8–5.9 `kT` to 0.03–0.06 on the helix (35.8 and 4.4 to
  0.9–1.8 and 0.13–0.14 on the strand); the leucine-on-helix effect does not survive, a comparable one appears
  on the strand for one rigid relaxed geometry.  Neither the direction nor the size of the leucine effect in a
  molecule is established".
* SCI-REV-0025 §3, point 1, add: "(After review R28: this example depends on the builder's bond angles, on the
  solvent term and, to within 1.6°, on the rotamer positions; with relaxed bond geometry it disappears on the
  helix and a similar one appears on the strand.  Read it as 'the identity of the table's minimum is not
  robust', not as 'ideal rotamers are strained by 4–6 `kT` in your model'.)"  The same caveat belongs with the
  bullet "Measurements" of SCI-MSG-0035 §2.
* SCI-REV-0026 F5: for "ideal rotamers are strained (ours, … 3.8 and 5.9 `kT` for one capped leucine)" read
  "ideal rotamers are strained when built on a bond geometry that is not the relaxed one (ours: 3.8 and 5.9
  `kT` for a capped leucine with equilibrium bond angles; 0.03–0.7 `kT` on a relaxed geometry rotated rigidly
  on a helix, 6–13 `kT` for the rotamer of the other well on a strand; your tables rotate the deposited
  geometry, so the number to measure is yours, and so is the bias towards the deposited rotamer — 1.2 to 1.9
  `kT` per leucine in our blocks)".

**F2 — the first ingredient of item 101 (b) is in print, and remark (6) of item 97 is incomplete.**  [search;
reading levels in §5]  Hallen, Jou and Donald (LUTE, 2017) write the continuous partition function as
`q = Σ_r ∫_{V(r)} exp(−E′/RT)`, define the "discrete free energy function" `E(r) = −RT ln ∫_{V(r)} exp(−E′/RT)`
and note that the K\* literature uses the voxel minimum instead [passage read, submitted manuscript, eq. 2–5];
Hallen (PLUG, 2019) reports designs "that account for continuous entropy" [abstract], with voxel free
energies from Monte Carlo integration represented by a *learned* pairwise matrix [preprint, through a tool
summary].  So "a rotamer state is a cell with its own free energy" and "a pair table for it" are established,
without certified error.  Not found in 6 web and 14 PubMed queries: cell *averages* of the coupling with a
Jensen lower end and a bounded-difference upper end.
*Replacement* (item 102, "What remains ours"): "…the construction of item 101 (b) *as a two-sided bracket*:
the discrete model with voxel free energies is LUTE's eq. (4)–(5) (Hallen, Jou, Donald 2017) and is used with
Monte Carlo voxel integrals in PLUG (Hallen 2019), both uncertified; a Jensen lower end with cell-averaged
couplings and a bounded-difference upper end was not found in a bounded search (R28: 6 web, 14 PubMed
queries) — class: at most a new combination of existing techniques."  Add to item 102: Lovell et al. (2000)
for the strain of rotamers in ideal bond geometry; Doig and Sternberg (1995), "Changes in vibrational entropy
appear to be negligible compared to the entropy change resulting from the loss of accessible rotamers", for
the term item 100 (i) calls vibrational.  In remark (6) of item 97, for "represent a voxel by its *minimised*
energy…" read "…in K\*; the same literature also defines the voxel free energy (LUTE, eq. 4) and computes it
by Monte Carlo (PLUG)".

**F3 — item 99 (ii): the class of "a product reference measure inside each cell" is wrong.**  [review;
replication]  The text says "needed only by the proof of (c)".  It is essential for (c) as stated.  *Smallest
counterexample:* one cell per site, `x_1 = x_2 ∈ {0, 1}` with probability ½ each (perfectly correlated),
`V = a(x_1 + x_2)`, so `c_1 = c_2 = a`: `ln⟨e^{−(V−⟨V⟩)}⟩ = ln cosh a`, which exceeds `Σc_i²/8 = a²/4` for every
`a ≤ 2` (0.4338 against 0.25 at `a = 1`); `(Σc_i)²/8 = a²/2` holds.  The same hypothesis is what makes
`v_s = Π_i v_{i,s_i}` and "every quantity with index `T` depends on `s_T` only" true.
*Replacement:* "*a product reference measure inside each cell* — essential for (c) as stated (two perfectly
correlated two-point coordinates violate `Σc_i²/8`); removal changes the constant to `(Σ_i c_i)²/8`; it is also
what makes the weights a product and the tables local in (a) and (b)."

**F4 — the upper end is not a model on the interaction sets of `V`; no pair-model upper end was tested.**
[review; replication]  The factor `exp(c_i(s)²/8)` couples all sites of all terms containing `i`: three sites on
a chain, a whole neighbourhood in a dense pair model.  The text says "a penalty on the union of the terms that
contain it", which is accurate, but remark (4) ("one more allowance table") and item 101 (b) are read by a
software author as "a pair table".  By Cauchy–Schwarz, for weights `w_{T,i} > 0` with `Σ_{T∋i} w_{T,i} = 1`,
`c_i² ≤ Σ_{T∋i} o_{T,i}²/w_{T,i}`, which gives tables `R_T − Σ_{i∈T∩H} o_{T,i}²/(8w_{T,i})` on the interaction sets of
`V`; with equal weights the price on the toy chain is a factor 1.000 (3 cells) to 1.138 (288 cells) in width
(`toy_pairwise_01.log`).  The force-field brackets of part (26) take the whole energy as one term and are full
tables over `kⁿ` states (`n ≤ 3`).
*Replacement* (item 97, after "inside a window of width `2w`)"): "The upper end is therefore not a model on the
interaction sets of `V`.  It becomes one by Cauchy–Schwarz with weights `w_{T,i}` summing to one at each site:
tables `R_T − Σ_{i∈T∩H} o_{T,i}²/(8w_{T,i})`; on the toy chain this costs at most 14 % in width (R28)."  Item 101
(b), add: "(as measured, both ends are full tables over all cell states of two or three torsions; a
pair-model upper end has not been put through a force field)".

**F5 — walls: mode M repairs the upper end only.**  [review; replication]  With a wall inside a cell the Jensen
end pays the cell *mean* of the wall.  On the toy chain, raising the bump from 0 to 20, 200, 2 000 `kT` moves
the Jensen end from 0.36 to 0.52, 1.11, 7.71 nats per angle below the exact value at three cells
(`toy_extras_01.log`); on leucine with the uniform reference the Jensen end is 13 700 nats below at three
cells (their log).  Item 101 (b) says of walls that "the mode M of item 97 will have to carry them"; item 99
(ii) says "bounded oscillation inside a cell — replaceable: mode M".
*Replacement:* item 101 (b): "…the remainder there will contain walls; mode M carries them in the upper end
only — the lower end averages a wall over the cell and needs smaller cells where walls are, or a reference
that excludes them".  Item 99 (ii): "*Bounded oscillation inside a cell* — replaceable for the upper end (mode
M); the lower end needs a finite cell mean."  Remark (3): add "(the lower end pays the cell mean of a wall in
either mode)".

### Minor

**F6 — statement hygiene** [review].  *Replacement* for the first sentence of item 97: "…with probability
measures `ν_i` and `ν = ν_1 ⊗ … ⊗ ν_n` … Let `V = Σ_T V_T(x_T)` with every `V_T` bounded and measurable and the
infima below measurable (e.g. `V_T` continuous) …"; and a remark: "the cells may be any decomposition
`ν_i = Σ_s v_{i,s} ν_{i,s}` into probability measures; the closed cells with half-weight end points of item 98
are one".

**F7 — remark (1) and the constant** [review; replication].  "If `V` changes by at most `L_i h`" does not bound
`c_i`, which is a sum of term-wise oscillations.  *Replacement:* "If every term `V_T` changes by at most
`L_{T,i}h` when `x_i` moves across a cell, … mode H of order `Σ_i(Σ_{T∋i} L_{T,i}h)²/8`.  The constant depends on how
`V` is split into terms; the oscillation of `Σ_{T∋i} V_T^s` in `x_i`, supremum over the window, is admissible,
never larger (0 of 94 770 entries) and gives 0.91, 0.79, 0.67, 0.63 of the all-H width at 3, 6, 12, 24 cells on
the toy chain."

**F8 — item 98, six slips of description; no number is wrong** [replication].
(1) The one-body terms are `1.5(1 + cos(3x + φ_i))` with random phases; the text omits `φ_i`.  With `φ = 0` the
wells are centred in the three cells and the mixed width at three cells is 1.07, not 1.29; every other entry
moves by under 2 % (`toy_phi0_01.log`).
(2) The "smooth wall … between neighbours" is one bump of width 0.6 rad at a random point of each pair's
torus, `W exp(−(2 − cos(x_i − a_i) − cos(x_{i+1} − b_i))/σ²)`; its largest slope is about 20 `kT` per radian for
`W = 20` — not a steric wall.  (3) "interpolated between 96 and 144": the width at 144 cells is `1.047·10⁻³`,
above the target; the script interpolates between 144 and 288 (147.3; the power law through 96 and 144 gives
147.2 by extrapolation).  (4) "width over `J²`: 0.027, 0.025, 0.021, 0.015" are *total* widths of eight angles
over `J²`, in a sentence about the width per angle (per angle: 0.0034, 0.0032, 0.0026, 0.0018).  (5) "4.7 times
larger" holds at 48 cells; the ratio is 2.2 at 3 cells and 4.95 at 144.  (6) "best choice of modes by a
threshold" is the best of nine thresholds; a local search over modes is better by up to 10 % (0.349 → 0.316
with the bump at 12 cells; 0.651 → 0.620 at 6 cells).
*Replacement fragments:* "one-body terms `1.5(1 + cos(3x + φ_i))` with random phases"; "optionally one smooth
bump of height `W` and width 0.6 rad at a random point of each neighbour pair's torus"; "(log–log interpolation
between 144 and 288 cells)"; "(total width of the eight angles over `J²`: …)"; "4.7 times larger at 48 cells
(2.2 at 3, 4.9 at 144)"; "best of nine thresholds on `c_i`".

**F9 — sentences stronger than "a grid model"** [review].  (1) Item 99 (i): "the best certified statement that
item 97 gives at three cells per angle" — it is the narrowest bracket obtained with one grouping of terms,
one reference and nine thresholds, for a grid.  *Replacement:* "the narrowest bracket we obtained from item
97 for the grid model".  (2) Item 100 (iv): "below the continuous `ln Z` by at most `1.2·10⁻⁵`" and item 101 (b) /
SCI-REV-0025 point 4: "a certified lower model of the continuous partition function".  The 2.5° and 5° grids
differ in `ln Z` by `5.4·10⁻⁵` for VV helix (up to `5.9·10⁻⁴` over the 2.5° cases) — forty times the Jensen gap
quoted — so for a continuum only the *direction* of the lower end is a theorem, and only once the one-residue
cell integrals and the cell averages are enclosed.  *Replacement:* "below the grid's `ln Z`"; "a lower model of
the grid's partition function (for the continuum: a theorem once the cell integrals and cell averages are
enclosed; here they are grid sums whose error exceeds the gaps quoted)".

**F10 — the assertions do not test the H-mode constants** [replication].  With every oscillation multiplied by
0.5 the all-H end still contains the exact value in 41 of 41 partitions (the exact value sits below 0.21 of
the bracket everywhere); multiplied by 0.3 it is excluded in 34 of 41, by 0.1 in 41 of 41.  "Asserted in all 41
partitions" therefore does not detect an oscillation too small by a factor of two; the agreement of two
independent implementations to `5·10⁻⁷` does.  *Replacement* (controls of item 98): add "the all-H end with
oscillations × 0.3 excludes the exact value in 34 of 41 partitions, × 0.5 in none — the bracket assertions do
not detect an oscillation that is too small by a factor of two".

**F11 — item 99 (ii), last class** [review; replication].  "With them free, the 'sites' are no longer
independent under any natural reference" is not so: in bond-angle-torsion coordinates the volume element is a
product, `b² sin θ` per atom (checked numerically: constant ratio to `2·10⁻⁹` over 200 geometries,
`bat_jacobian_01.log`; Chang, Potter, Gilson 2003 is the reference named by a search result, not opened).
*Replacement:* "*Fixed bond lengths, bond angles and backbone* — outside the statement as tested, not outside
its reach: in bond-angle-torsion coordinates the reference is a product, so a site may carry its side chain's
bond lengths and angles (higher-dimensional sites); a free backbone destroys the locality of the terms, not
the product reference."

**F12 — numbers in items 100 and SCI-REV-0025 §3** [read only against the logs].  All 252 table cells agree
with the logs; in the texts: (1) "off … by one to three nats per torsion": the range of the absolute offset
is 0.580–3.177 (leucine is 0.58–0.62) — *read* "0.6 to 3.2".  (2) SCI-REV-0025 point 3, "a vibrational term of
about 2 nats per torsion": the cell-minimised offsets are +1.18 … +2.28 (serine 1.18–1.21, leucine 1.76–1.77,
valine 1.89–2.28) — *read* "1.2 to 2.3".  (3) "kinder by a factor of about twenty": 15.5–43.8 for valine at 2.5°
(4.6 for serine, 127 for leucine).  (4) Item 100 (vi) cites the research log at "22:36"; the entry is headed
"22:35".  (5) The entry "+1.992" for VVV helix is a three-decimal rounding of a logged "1.9925"; its last digit
rests on digits that are not in the log (not re-run: 477 s).  "−0.580" for leucine is right (−0.579521).
(6) SCI-REV-0025 §3 introduces the measurement as "the side-chain torsions on a 2.5° grid"; two of the twelve
rows (the tripeptide) are on a 5° grid, as the table itself says.

**F13 — item 102** [read only, PubMed records].  (b) "using more rigid rotamers was never better than a
continuous-rotamer model" is verbatim but drops the abstract's qualifier "at computationally feasible
resolutions" — *restore it*.  (d) "not the search" is a gloss; with the softer repulsion the optimum does add
a point (77 % → 78 %), as SCI-REV-0026 §3 says — *read* "for the default terms … not the search".  (f) The
permitted source, SCI-REV-0026.md, contains no occurrence of "voxel", "THY-MSG-0020", "VoxelEnclosure" or
"VoxelBridge": the fairness of (f) cannot be judged from it.  Internally: "Mode M of item 97 (a cell
represented by its minimum and maximum)" — mode M is the minimum; the maximum belongs to the bracket of
remark (1).  *Read* "Mode M (a cell represented by its minimum) and the minima/maxima bracket of remark 1 are
instances of that enclosure".

**F14 — SCI-REV-0026 §0 point 2 and §4** [review; replication].
(1) "only if `b ≤ gap/(2n)`" assumes dense tables; on path graphs the exact radius exceeds `gap/(2n)` in 245 of
293 random models.  The exact radius is `b* = min_x (E(x) − E(x*))/(2·#{entries x uses and x* does not})`; on
complete graphs `b* ≤ gap/(2n)` in 392 of 392 models, with equality in 194.  (2) "That is above your rounding
unit": an upper bound on a radius being above something says nothing about the radius.  (3) "the minimiser of
the published integers and of nothing near them": `x*` does minimise every table within `b*`.
*Replacement:* "By §4, on dense tables `x*` minimises every table within `b` of yours, entry by entry, only if
`b ≤ gap/(2n)` — a competitor that differs at one site uses `n` other entries (in general: one plus the number
of pair tables at that site); the exact radius is the minimum over competitors of their gap divided by twice
the number of entries they do not share with `x*`, and can be smaller.  From your table: at most … kcal/mol
per entry.  These bounds are below everything else in the budget; whether the radius itself exceeds your
rounding unit is what (i) of §4 decides.  *The certified minimiser is certified for the published integers
and, at most, for tables this close to them.*"
(4) §4 (ii), "for a well we know only a sufficient condition (compare against `x*` alone)": right, and not
necessary — in 49 of 2 720 (site, well) cases the statement is true without it, never the converse.  *Smallest
example:* two sites with two states, `E(a,p) = 0`, `E(a,q) = 0.1`, `E(c,p) = E(c,q) = 5`, `b = 1` on all eight
entries: site 1 keeps `a` in all 256 vertex scenarios ((a,p) beats (c,p) by at least 1, (a,q) beats (c,q) by
at least 0.9) although `Ẽ(c,q) − Ẽ(a,p) = −1`, and `x* = (a,p)` itself is not necessarily optimal.  *Exact
condition:* every minimiser of every scenario has site `i` in the well iff no configuration outside the well
is *possibly optimal*, and `x` is possibly optimal iff it minimises the table with its own entries lowered and
all others raised (5 430 of 5 430 configurations agree with enumeration) — one minimisation per competitor,
not one in all.  *Replacement:* "…where comparing against `x*` alone is sufficient and not necessary; the exact
condition is that no configuration outside the well minimises the table in which its own entries are lowered
and all others raised".
(5) "the criterion is classical … both from memory, nothing opened": now opened (§5).  *Replacement:*
"*Novelty:* none — under interval costs the maximum regret of a solution is attained at the scenario with its
own costs at the upper and all others at the lower bounds, and a necessarily optimal solution is one of zero
maximum regret (Kasperski and Zieliński, survey, passage read); the same survey records that the optimum of
the midpoint scenario detects a necessarily optimal solution whenever one exists — so testing the minimiser
of the nominal table is enough (checked: 0 exceptions in 3 000 random models)."

## (3) Runs, with predictions and controls

Every script caps its address space at 3 GB and prints its peak memory in the last line (largest: 691 MB);
the division's scripts were run under `ulimit -v 3145728`.  One thread, at most two processes, longest run
279 s.  Every log named here reached its last line.  A prediction was written in `NOTES.md` before each run.

| run (log in `ws_R28/`) | kind | prediction → outcome | result; controls with their violations |
|---|---|---|---|
| `toy_selftest_02` | replication of (a)–(c) from the definitions | zero violations → met | 360 (model, mode) cases by brute force, closed and half-open cells: (a) 0 violations; (b), (c) per state: 0; transfer matrices = brute force to `4.6·10⁻¹³`.  Controls: oscillations × 0.3 → 176 models with a violated state; full end weights → (a) fails 60/60; correlated reference → (c) fails for `a ≤ 2` |
| `toy_stageA_seed28_01` | replication, blind (own phases, before their script was opened) | 7 predictions → all met | rows 1–2 within 2 %; exponents −1.0052, −2.1476; 146.1 cells; position 0.144–0.210; 611 brackets, 0 violated.  Controls: × 0.3 excludes at 6 of 8 `k`, × 0.1 at 8, × 0.5 at 0; minima as lower end fail 8/8 |
| `toy_stageB_01` | replication on their instance | 0 disagreements → met | 49 items (8 exact values, 41 rows), 0 disagreements; 205 ends to `4.9·10⁻⁷`; 2 409 brackets, 0 violated.  Controls: Jensen as upper end violated 41/41; minima as lower end 41/41; × 0.5: 0/41; × 0.3: 34/41; × 0.1: 41/41 |
| `toy_extras_02`, `toy_pairwise_01`, `toy_phi0_01` | replication (extensions) | met; one control of mine could not bite (§7) | closed/half-open ratios; tight constant 0.63–0.91; bumps 20–2 000 `kT`; pair form ≤ 1.138; `φ = 0` |
| `rerun_L_H_144_01`, `rerun_VV_H_144_01` | re-run | identical but for timings → met | `diff` against the committed logs: lines 1 and 45 only (run times) |
| `ff_grid_*` (3 grids, 3 windows) | replication of the energy grid | met, after my dihedral sign error (§7) | dihedrals as requested to `4·10⁻¹⁴`°; bond and angle energy constant; builder = fresh ff14SB + GBn2 system to `2·10⁻¹⁶`; my grid = their cache to `7·10⁻¹⁴`.  Controls: OBC2 in place of GBn2 differs by 1.1–2.0 kcal/mol; exchanged axes differ by 0.86 (VV) and `10⁹` (L) in relative terms |
| `ff_reduce_L_H_01`, `ff_reduce_VV_H_01` | replication of the reductions | 0 disagreements → met | 165 and 164 items, 0 disagreements; 432 brackets, 0 violated; valine tilted: `7.1788·10⁻⁷`, `1.8418·10⁻²`, `1.6602·10⁻⁵` per torsion; exhaustive search over the 64 mode assignments at three cells confirms `1.8418·10⁻²`.  Controls: separable energy → remainder `10⁻¹³`, gaps 0, populations factorise to `10⁻¹⁶` (real energy: 0.19 off); shuffled grid → 135/165 and 155/164 items disagree, inequalities still 0 violated; × 0.3 excludes 13/18 (VV), 0/18 (L: its all-H end is `4·10¹⁹`) |
| `ff_leucine_L_H_01`, `_L_E_01`, `ff_window_01` | new (R28) | vacuum prediction **missed**; others met | table of F1 |
| `ff_flex_H_01`, `_E_01`, `_H_map_01`, `ff_flex_width_01` | new (R28) | direction met; size far beyond my guess | table of F1.  Controls: all atoms frozen = builder energy (difference 0); restraint fidelity 0.04–0.11°; relaxation never raises the energy (0 of 16); perturbed restart within `10⁻³ kT` |
| `ff_relaxgeom_H_01`, `_E_01` | new (R28) | helix met; strand not predicted | table of F1.  Controls: Z-matrix extraction reproduces the builder to `4·10⁻¹⁵` Å and the original grid to `10⁻¹³`; builder geometry reproduces TV 0.4808, gap 1.559 |
| `check_tables_01` | read only | 0 differing cells → met | 252 cells; text numbers of F12 |
| `no_check_01` | replication | all met | 580 tiny models, 5 shapes: (N) 580/580, (U) 580/580.  Controls: four mutilated criteria disagree in 177, 159, 401, 181 models; per-well "sufficient but false": 0 |
| `rerun_necessary_optimality_01` | re-run | identical → met | `diff`: start time and run time only |
| `no_midpoint_01`, `bat_jacobian_01` | replication of two facts I quote | met | 0 exceptions in 3 000 models (control: another candidate fails in 751); Jacobian ratio constant to `2·10⁻⁹` (controls vary by 144 % and 308 %) |

The five derived numbers of SCI-REV-0026 §0, from the inputs in my brief: 0.0451/52 = `8.6731·10⁻⁴`;
0.0243/72 = `3.3750·10⁻⁴`; 0.1102/72 = `1.5306·10⁻³`; 0.0068/92 = `7.3913·10⁻⁵`; 0.0039/98 = `3.9796·10⁻⁵` — all as
claimed; `2⁻²¹ = 4.7684·10⁻⁷`; one-site allowances `2bn` = `2.48·10⁻⁵` … `6.20·10⁻⁵`, 0.52 … 1.3, 5.2 … 13 as claimed.
The gaps and site counts themselves were not checked (the other division's branch is not available to me).

## (4) The assumption table (Proposition A17.24 and its use)

| hypothesis | class | what happens without it |
|---|---|---|
| `ν` is a product over sites | **essential** for the statement as written (stated only implicitly) | (a) with `v_s = Πv_{i,s_i}` is false (two perfectly correlated binary coordinates, cells = points: the cell (0,1) has weight 0, not ¼); with `v_s = ν(C_s)` it is true and non-local |
| product of conditionals inside a cell | **removal makes (c) false** (F3: `ln cosh a > a²/4`); a **weaker bound survives**, `(Σc_i)²/8`; for (b): needed for locality only | — |
| cells that are products over sites | convenience for (a); the tables stop being local otherwise (as the text says) | — |
| cells form a partition | **replaceable by a weaker condition**: any decomposition of `ν_i` into probability measures (trapezoid cells; soft cells) | nothing |
| finitely many cells, each of positive weight | convenience (countably many; drop null cells) | nothing |
| `V` bounded | convenience for (a), (b) (integrability suffices; `+∞` allowed, the bound is then trivial); for (c) mode H needs a finite oscillation, mode M a finite infimum | a wall inside a cell: (c) survives through mode M, (b) becomes useless (F5) |
| each `V_T` bounded, infima measurable | technical; needed for the tables to exist | `∞ − ∞` in `Σ_T⟨V_T⟩_s` |
| modes fixed per (site, cell) | needed for "every quantity with index `T` depends on `s_T` only"; **replaceable** by modes per (term, coordinate, state of the term) — each term may minimise over a coordinate of its own choice, since an infimum of a sum is at least the sum of infima (not tested) | modes depending on the whole state: (c) true, tables non-local |
| the splitting `V = Σ_T V_T` | free; **changes the constants** of (c) (not of (b)) | — |
| term-wise constant `c_i = Σ_T o_{T,i}` | convenience; the window constant is tighter (F7) | — |
| one-body terms in `ν_i` (remark 2) | changes the constants: width 2.2–4.95 times larger without | — |
| a modulus of continuity of the unknown part (remark 4) | **essential** for any conclusion from finitely many evaluations beyond the a-priori bounds: a dip of depth `A` and width `ε` at an unevaluated point changes `Z` by up to `ε(e^A − 1)` and no evaluation sees it | false |
| fixed bond lengths, angles | not needed by the proposition (F11: product reference in bond-angle-torsion coordinates); **decisive for the measurement** (F1) | — |
| fixed backbone | needed for locality of the terms | terms depend on all backbone coordinates |
| the "continuum" is a grid (items 98, 100) | **essential gap** between the numbers and a certificate: grid maxima understate suprema, grid sums are not enclosures (remark 5 says so) | F9 |

## (5) Prior art, with the search log

Tools: the PubMed connector (records with abstracts), a web search tool, a page-fetching tool that returns a
model's summary of the page (or saves a PDF, which I then read with `pdftotext`).  Generic queries only.

**Reading levels.**  [P] passage read by me in the text; [A] abstract in the PubMed record; [T] the fetch
tool's summary of a full text, not read by me verbatim; [S] search-result snippet; [M] from memory.

| source | level | what it says that bears on the review |
|---|---|---|
| Georgiev, Lilien, Donald, *J. Comput. Chem.* 29 (2008) 1527, doi:10.1002/jcc.20909 | A | quotation of item 102 (a) verbatim |
| Gainza, Roberts, Donald, *PLoS Comput. Biol.* 8 (2012) e1002335, doi:10.1371/journal.pcbi.1002335 | A | the three quotations of (b) verbatim; one loses its qualifier (F13) |
| Petrella, Karplus, *J. Mol. Biol.* 312 (2001) 1161, doi:10.1006/jmbi.2001.4965 | A | (c) verbatim; also: on-rotamer conformations are minima of rigid-geometry maps "generally to within 10 degrees or less" |
| Yanover, Schueler-Furman, Weiss, *J. Comput. Biol.* 15 (2008) 899, doi:10.1089/cmb.2007.0158 | A | (d) verbatim, with 77 % → 78 % and "approximately 85% of the proteins" |
| Zhang, Liu, *PLoS Comput. Biol.* 2 (2006) e168, doi:10.1371/journal.pcbi.0020168; DuBay, Geissler, *J. Mol. Biol.* 391 (2009) 484, doi:10.1016/j.jmb.2009.05.068 | A | (e) as described |
| Hallen, Jou, Donald, LUTE, *J. Comput. Biol.* 24 (2017) 536, doi:10.1089/cmb.2016.0136 | A (record); **P** (submitted manuscript of 12 Aug 2016, eq. 2–5) | voxel free energy as the discrete energy; K\* uses the voxel minimum (F2) |
| Hallen, PLUG, *Proteins* 87 (2019) 62, doi:10.1002/prot.25623 | A; T (bioRxiv 10.1101/368522) | "designs that account for continuous entropy"; Monte Carlo voxel integrals; learned pairwise matrix; no bound |
| Jou, Holt, Lowegard, Donald, MARK\*, *J. Comput. Biol.* 27 (2020) 550, doi:10.1089/cmb.2019.0315 | A | K\* partition functions from "pairwise-minimized energy lower bounds" |
| Roberts, Donald, *Proteins* 83 (2015) 1151, doi:10.1002/prot.24808 | A | partitioned continuous rotamers tighten bounds on the minimum |
| Jumper, Freed, Sosnick, arXiv:1610.07277 | T | side-chain free energy as an integral over `χ`; coarse states; variational approximation, no bound |
| Koehl, Delarue, *J. Mol. Biol.* 239 (1994) 249, doi:10.1006/jmbi.1994.1366 | A | mean field over rotamers with an entropy estimate |
| Sciretti et al., *Proteins* 74 (2009) 176, doi:10.1002/prot.22145 | A | variational free energy over rotamer states by belief propagation (a design study; cited for that only) |
| Doig, Sternberg, *Protein Sci.* 4 (1995) 2247, doi:10.1002/pro.5560041101 | A | vibrational entropy changes "appear to be negligible" next to rotamer counting |
| Lovell, Word, Richardson, Richardson, *Proteins* 40 (2000) 389 | A | overlaps of rotamers "if built in ideal geometry"; "bond angle distortions" (F1) |
| Kasperski, Zieliński, "Robust discrete optimization under discrete and interval uncertainty — a survey" (author's PDF; the volume not verified) | **P** | worst-case scenario of a solution; necessarily optimal = zero maximum regret; midpoint scenario (F14) |
| Fortin, Kasperski, Zieliński, "Some methods for evaluating the optimality of elements in matroids with ill-known weights" (author's PDF; journal not verified) | **P** | possibly / necessarily optimal elements, Theorems 5 and 6; cites Yaman, Pinar, Karasan, *Oper. Res. Lett.* 29 (2001) 31 (reference list only) |
| A. Maurer, "Thermodynamics and concentration", arXiv:1205.1595; Chang, Potter, Gilson, *J. Phys. Chem. B* 107 (2003) 1048 | S | named by search results; not opened |
| leucine library values (−65, 175), (−177, 65); CA–CB–CG ≈ 116° in deposited leucines | M | used in one row of F1 and as context; unverified |

**Search log.**  PubMed: citation lookup of the six papers of item 102; then "continuous rotamers partition
function provable" (0); "continuous entropy voxel protein design side-chain" (0); "rotamer free energy integral
torsion side-chain entropy vibrational" (0); "continuous rotamers partition function" (2); "continuous entropy
protein design voxel" (0); "side-chain conformational entropy rotamer vibrational free energy" (1); "LUTE Local
Unpruned Tuple Expansion" (1); "Hallen MA[Author] AND (entropy OR "partition function" OR "free energy")" (4);
"minimization-aware recursive K\* partition function" (1); "BBK\* branch and bound over K\* partition function
bounds" (1); "self-consistent mean field side-chain conformational entropy rotamers" (3); "computational
protein design side-chain conformational entropy belief propagation free energy rotamers" (1); "penultimate
rotamer library" (5).  Web: (1) continuous rotamers voxel "free energy" integral over voxel partition function
provable bounds protein side chains "continuous entropy"; (2) Hallen "PLUG" "Pruning of Local Unrealistic
Geometries" "continuous entropy" LUTE voxel free energy bioRxiv; (3) "necessarily optimal" solution interval
costs combinatorial optimization criterion scenario "upper bounds" own elements "lower bounds" others
Kasperski Zieliński; (4) rigorous upper and lower bounds configuration integral partition function
discretization cells Jensen inequality lower bound "bounded differences" OR "Hoeffding" upper bound free
energy; (5) verified integration rigorous enclosure multidimensional integral Boltzmann factor partition
function interval arithmetic guaranteed error bound molecular; (6) Jacobian bond-angle-torsion internal
coordinates configuration integral "b^2 sin" product over atoms Jacobian determinant factorizes Cartesian to
BAT coordinates.
**Addresses opened:** https://ar5iv.arxiv.org/html/1610.07277 ; https://arxiv.org/abs/1806.06064 ;
https://donaldlab.cs.duke.edu/Supplementary/jcb16/lute/LUTE.submit.pdf ;
https://www.biorxiv.org/content/10.1101/368522.full ;
https://cs.pwr.edu.pl/zielinski/publications/papers/fss08.pdf ;
https://cs.pwr.edu.pl/zielinski/publications/papers/survey16.pdf .
**Not reached:** the full texts of the K\*, BBK\*, MARK\*, PLUG (journal), Gainza 2012 and Georgiev 2008 papers;
the statistical-mechanics literature on cell theories and variational coarse-graining beyond one query;
numerical analysis beyond one query; MathSciNet, zbMATH; any citation-graph search.  **"Not found" is not
"new".**

**Outcome.**  Item 100's phenomenon: established (as item 102 says).  The strain of rotamers in ideal bond
geometry: established (Lovell 2000 [A]).  Voxel free energies as discrete state energies: established (LUTE
[P], PLUG [A, T]), uncertified.  Jensen lower end and bounded-difference upper end: textbook ingredients; the
combination as a two-sided bracket of a side-chain integral was not found.  The necessary-optimality
criterion: classical, source read [P].

## (6) For a software author: what part (26) does and does not tell you about a rigid-rotamer table of a real protein

It tells you, with the literature (Georgiev 2008, Gainza 2012), that a certified minimum or free energy of a
rigid-rotamer table is a statement about the table.  It adds, for one force field on capped blocks, that the
free energy of a table differs from that of the continuous torsions by a per-torsion width term of 1.2–2.3
nats that moves by tenths of a nat with the context, and that minimising inside the cells repairs populations
(to 0.08) but not that term.  It does **not** tell you that ideal rotamers are strained by 4–6 `kT`: that
number belongs to side chains built with equilibrium bond angles (CA–CB–CG = 109.5°); on a relaxed geometry
the strain at the ideal leucine torsions is 0.03–0.06 `kT` on a helix.  It does not tell you *where* a table
fails: the example in our messages (leucine, helix) disappears with relaxed geometry, without the solvent term, or
when the `χ₂` positions move by 1.6°, and a larger one (total variation 0.73) appears on a strand for a relaxed
geometry taken from the other well.  What you can act on: (1) the identity of your table's minimum is not
robust wherever two wells of a residue lie within a few `kT` — test it by rebuilding the table from a second
bond geometry and from rotamer positions shifted by ±2°, and report the sites whose state survives; (2) a
table built by rigid rotation of the deposited geometry favours the deposited rotamer — by 1.2 to 1.9 `kT`
per leucine in our blocks — so measure that bias before comparing with deposited conformations; (3) the brackets
of Proposition A17.24 quoted for valine are grid-model numbers for two or three torsions with the whole
energy as one term: they are not yet a certificate for a continuum, and no pair-model upper end has been
tested; (4) no number here is about a protein.

## (7) What I did not check; my own errors; files

**Not checked.**  Parts (13)–(18) of the addenda (not opened, as instructed); parts (19)–(24) and item 94;
SCI-REV-0026 §§7–11 (the file was read to the end of §6 and afterwards only searched for words);
the ten force-field cases other than L helix and VV helix beyond a read-only comparison of texts and tables
with their logs (in particular all three-torsion and serine reductions); whether the logs' predictions
preceded the scripts (no timestamps available to me beyond the research log, lines 2924–2950 and 3024–3085,
which I read); the theory division's Lean files and THY-MSG-0020; the other division's branch — the gaps and
site counts of the five structures, and whether its tables are dense; the full text of any source (passages
of three were read by me; the rest at abstract level or through a tool's summary).  The relaxed-geometry measurements are adiabatic (no vibrational free energy of the relaxed
coordinates), for one residue type and one force field, with the map's mask taken from the rigid energies;
they bear on *direction*, not on a molecule.  The modes-per-term generalisation in §4 is not tested.  The
library values and the 116° marked [M] are unverified.

**My own errors** (all in `NOTES.md` where they happened).  (1) The brute-force reference of my first
self-test overflowed in `exp` (log `toy_selftest_01`, kept); fixed by working in logarithms.  (2) Three early
notes carried estimated times instead of clock readings; corrected, and every later time comes from `date -u`.
(3) My first dihedral function had the sign of the sine reversed (log `ff_grid_L_H_144_01`, kept, shows a
false "FAILED"); the grid was unaffected.  (4) One control of mine could not bite: "tight constant × 0.5 must
exclude the exact value" excluded nowhere; × 0.3 added (`toy_extras_02`).  (5) Two predictions missed: I
expected the vacuum part alone to keep the leucine claim (it removes it), and I suspected a double rounding
in "−0.580" (there is none).  (6) I did not predict the strand result of `ff_relaxgeom_E_01`; it changed my
conclusion from "an artefact of the geometry" to "a family in which the effect comes and goes".

**Tool actions declined:** none.

**Files** (all in `experiments/science/ws_R28/`): `NOTES.md`; `r28_common.py`; toy chain: `toy_lib.py`,
`toy_selftest.py`, `toy_run.py`, `toy_stageB.py`, `toy_extras.py`, `toy_pairwise.py`, `toy_phi0.py`; force field:
`ff_grid.py`, `ff_lib.py`, `ff_reduce.py`, `ff_leucine.py`, `ff_window.py`, `ff_flex.py`, `ff_flex_width.py`,
`ff_relaxgeom.py`, `check_tables.py`, `run_grids_02.sh`; necessary optimality: `no_check.py`,
`no_midpoint.py`; `bat_jacobian.py`; the logs named in §3 (two kept failing logs: `toy_selftest_01.log`,
`ff_grid_L_H_144_01.log`); data: `cc_cache/` (the re-run's cache), `grid_*.npz`, `win_*.npz`, `flexmap_*.npz`.
Nothing was written outside that directory and this report; no state-changing git command was run.
