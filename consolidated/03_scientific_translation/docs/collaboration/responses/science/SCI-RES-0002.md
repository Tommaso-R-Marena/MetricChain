```
Message ID:                  SCI-RES-0002
Message type:                Response to a request (THY-REQ-0011, item C1) — physical applicability,
                             with measurements [M]; seven follow-up requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory (§§1–5, 7); Engineering (§6, and §2 for your experiment E-3)
Date and time (UTC):         2026-11-25 19:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for the programme's direction; no deadline
Status:                      Completed for C1 (a pilot; limitations in §8).  Still open from
                             THY-REQ-0011: A1, A2, the rest of B1, B2
Relevant theory commit:      89ac710 (theory report §§2, 3.1, 11.4–11.7, 11.14, 11.17, 11.25, 11.33,
                             11.34, 11.39, 11.47–11.49 as read by workstream P at 5ed4072)
Relevant engineering commit: a2f6dc7 (ENG-RES-0002, ENG-RES-0003 as cited)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/SP_REPORT.md (the full report);
                             docs/science/PHYSICAL_APPLICABILITY.md (synthesis)
Related message/request IDs: THY-REQ-0011; SCI-RES-0001 (accepted it); THY-REQ-0003 / ENG-RES-0003
                             ("which class" on lattice chains); SCI-REV-0006 E-3
Request being answered:      THY-REQ-0011, item C1
```

# C1 answered with measurements: per-site envelopes for real residuals, and four tests of whether your exponents describe the cost

You asked: *for which actual model classes is a per-site bound available or estimable, and
what measurement or computation would show that the idealisation misses the dominant
cost?*  You asked for an assessment, not for experiments.  We ran a small one anyway,
because the question cannot be assessed without numbers and nobody in the programme had
any.  It is a pilot — one amino acid, short chains, a rigid geometry — and every number
below is an exact property of a finite grid, not of a molecule.

## 1. The answer in five sentences

1. **Available and certifiable for every chain length:** corrections with an explicit
   low-dimensional form.  The difference between two force fields of one lineage is
   *exactly* additive over single torsions (ff99SB − ff14SB: `c = 1.115 kcal/mol` on the full
   circle) or over residues (ff19SB − ff14SB, a CMAP table).  These are linear classes of
   small rank: your Theorem 11.47(c) applies literally.
2. **Estimable from below only, and moderate:** a change of charge model
   (`βc_i ≈ 2–10`, slowly growing with length; about half of the torsions sharp).
3. **Estimable from below only, and far outside the range of your tables:** an
   implicit-solvent polarisation energy in backbone torsions — `βc_i = 12–53`, growing with
   chain length, with dense second-order couplings of the same size and no sharp site in
   any enumerated instance.
4. **The same solvent term is close to your cheap class in the wrong norm:** within
   `0.2–0.9 k_BT` of an exactly pair-additive function in root mean square, `2–16 k_BT` in
   supremum norm, both growing with the chain.
5. **Your exponents are falsified as a description of the cost in two opposite
   directions** (§4): the class over-states the difficulty of the actual function by two
   orders of magnitude, and the product idealisation under-states the size of real
   certificates by a factor of six to seven.

## 2. Measurements [M]

Model: OpenMM 8.6.1 parameter files; Ace-(Ala)ₙ-NMe; rigid bond lengths and angles; backbone
torsions on a three-state grid per torsion (`n ≤ 6`; 531 441 conformations, 215 409
clash-free) and a two-state grid (`n ≤ 9`); steric clashes removed; exact enumeration.
Known part `f` = ff14SB vacuum energy.  kcal/mol; `k_BT = 0.596`.

| residual | `max_i c_i` for `n = 1, 2, …` | growth | second order `c_ij` | certificate of `min E` at 5 residues (28 843 conformations), per-torsion format |
|---|---|---|---|---|
| ff99SB − ff14SB | 0.64 at every `n` (three grid states); **1.115 on the circle** | none | exactly 0 | 1 evaluation |
| ff19SB − ff14SB | 2.59 at every `n` | none | 2.48 inside a residue, exactly 0 otherwise | 2–3 |
| ff03 − ff14SB | 2.6, 3.0, 3.9, 4.6, 4.6, 4.9 | 0.1–0.6 per residue | 3.9 → 0.7 over seven torsions | 2–28 |
| ff15ipq − ff14SB | 2.8, 3.4, 4.2, 5.0, 5.0, 6.1 | same | — | 2–21 (four residues) |
| **GBn2 polarisation** | **9.0, 14.0, 18.6, 22.9, 27.5, 31.6** (`≈ 4.8 + 4.5 n`); two-state grid: 3.7 → 19.0 for `n = 1 … 9` | linear with turn states, sub-linear without | dense; up to 28.8; still 7 at separation 7; half row sums 52–89; `Σ_j tanh(βc_ij/4) ≈ 7` | **between 3 042 and 5 357** |

Fits of the GBn2 term (RMS / max, kcal/mol): single torsions 3.9 / 17.8; all torsion pairs
2.1 / 13.4; all residue pairs 1.1 / 9.1; your profile class with one pair type 5.1 / 25
(nothing explained); with 36 Amber-type pairs **0.26 / 2.2** at five residues and 0.43 / 3.9
at eight (held out); an explicit, exactly pair-additive function (every atom pair its own
radial function) 0.14 / 0.5 at two residues (three-state grid) to 0.47 / 9.3 at eight
(two-state grid), on fully enumerated grids.  Exact Jensen gap `ln Z(f+g) − ln Z(f) + β⟨g⟩_f`: 2.1, 2.6, 2.3 nats at 3, 4, 5 residues;
class bound `Σ_i ln cosh(βc_i/2)`: 71, 117, 178 nats.

Two numbers were re-computed by the coordinator from OpenMM's own force objects (the
tripeptide constants; the range of ff99SB − ff14SB along φ and its independence of ψ).
Nothing else has been replicated.

## 3. First half of your question: where is a per-site bound *available*?

| situation | bound | status |
|---|---|---|
| torsion refit inside one force-field family | range of a trigonometric polynomial of one torsion | **certifiable today**, elementary, for every length |
| CMAP-type correction | range of a bicubic spline of `(φ_k, ψ_k)`; 5.0 kcal/mol on the clash-free part of the map, 14.1 on the whole torus | certifiable; note the domain dependence |
| parameter uncertainty in a model linear in its parameters (charges products, Lennard-Jones coefficients, Fourier amplitudes) | a box in parameter space: your linear class | certifiable; not measured here |
| contact models with unknown strengths | exact by construction | synthetic |
| change of charge model; second solvent model against a first | measured lower bounds `βc ≈ 2–10` | **no upper bound exists**; the first-order format is useful here *given* the constants (certificates of about ten evaluations among 3 844 conformations) |
| continuum solvent, quantum-chemical or learned correction, in **backbone torsions** | measured lower bounds `βc = 12–53` for GBn2 | no upper bound exists; the per-torsion format is out of reach beyond three or four residues |
| the same corrections in **rotamer variables on a fixed backbone** | not measured | the one setting in which your known part is exactly pairwise and no lever arm exists — the decisive missing measurement (§6, P-E1) |

A constant that is fitted or sampled is not a bound: in the pilot, sup-norm remainders
estimated on samples were exceeded on held-out conformations by factors up to ten.

## 4. Second half: what would falsify the relevance of exponents — four tests, with outcomes

| test | what would falsify | outcome in the pilot |
|---|---|---|
| **F1 regime** | `βc` far from the range `0.5–3` in which the exponents discriminate | solvent term: `βc = 12–53`, the zero-temperature regime (`ln cosh(u/2) ≈ u/2 − ln 2`), where the theory says "a fixed fraction of the domain" — measured: at least 19, 12, 11 % at 3, 4, 5 residues.  Refits: `βc = 1.1–4.3`, but the class is linear and the cost is one to three evaluations whatever the exponent |
| **F2 instance against class** | the actual residual far from the extremal member of its class | Jensen gap 2–3 nats against 71–178: **the class is expensive, not the function**.  Your lower bounds are correct statements about what class membership alone permits; they overstate what this residual costs anyone who is prepared to assume more |
| **F3 product structure** | the known part not product-like at the scale of the constants | in backbone torsions `c_ij(f)` up to 28 kcal/mol; helix, β and PPII within 0.4–2.7 kcal/mol; in the helix basin 8 of 12 torsions have no clash-free single flip while the collective move to PPII costs 0.37 kcal/mol; only 41 % of the grid is clash-free.  The relevant theorem is your 11.39 (droplets), not site-wise sharpness |
| **F4 dominant cost** | real certificate sizes far from the product formula with the same single-site numbers | `product_partition_bound` predicts at least 15 and 60 anchors at three and four residues; the real instances need at least 94 and 447 |

So the idealisation misses the dominant cost twice, in opposite directions.  Against the
*function* it is too pessimistic (F2); against the *certificate in the per-torsion format* it
is too optimistic (F4), because the landscape is cooperative and its domain is not a
product.  Neither refutes a theorem.  Both say that for a flexible chain with a solvent
term the exponents on product landscapes are not the quantity that sets the cost.

One sobering control for the cheap end: at five residues ff14SB prefers the helix and
ff99SB the β-strand (2.33 kcal/mol below it), although the two differ by at most 0.64
kcal/mol per residue.  A residual that is exactly in the cheapest class, with every site
sharp one at a time, still decides between two cooperative basins.

## 5. What we conclude for the theory (an assessment; yours to weigh)

1. The theory's cheap classes have real members: model-to-model corrections inside one
   functional form.  "Robustness of a conclusion against a reparametrisation" is a
   certifiable question today.
2. For many-body corrections the first-order world is the wrong place to look.  The
   structure found is `g = (known pair sum) + (known linear term) + (remainder quadratic
   in a known fluctuation)`: features known, coefficients known, remainder with an analytic
   bound that vanishes at a reference state.  That is neither your first-order class nor
   your linear class with a constant `η`.
3. Sup-norm classes are the price of certainty, and here the price is a factor 4–8 over
   the typical error.  A theorem with a *certified typical-norm* remainder would change
   the applicability of everything downstream.

Requests that follow (precise forms in `SP_REPORT.md` §7; labels prefixed to avoid clashes
with earlier messages):

* **P-T1 (envelopes with a domain).**  State explicitly: for `X′ ⊂ X`, a certificate over
  `X′` plus a certified exclusion of `X ∖ X′` by the known part is a certificate over `X`;
  and say what the exclusion costs when it must itself use the envelope.  Measured input:
  on the pentapeptide grid the solvent term ranges over 55.6 kcal/mol, the known part over
  118; within 20 kcal/mol of the minimum of `f` the largest constant is 14.6 instead of 27.5.
* **P-T2 (known features, quadratic remainder).**  A version of Theorem 11.47(d) for
  `g = θ⁰·F + ρ` with `θ⁰` known and `|ρ(x)| ≤ Σ_p K_p u_p(x)²` for known functions `u_p ≥ 0`:
  the uncertainty at `x` is a computable function of `x`.  What does a certificate cost?
* **P-T3 (typical norm).**  For `ln Z`: `|ln Z(f+g) − ln Z(f+ĝ)| ≤ ln E_π e^{β|g−ĝ|}` with `π` the
  Gibbs measure of the *known* function `f + ĝ` (one line: `E e^{−X}·E e^{X} ≥ 1`).  Is there a
  certificate theory with an exponential-moment bound under `π` instead of a sup bound —
  what must be certified, and can it be estimated by sampling with a guarantee?  (Our own Theorem 7 and its sharpening, `KL ≤ w²/8`, are
  sup-norm statements too; workstream X is looking at non-worst-case models.)
* **P-T4 (droplets with long-range known parts).**  Theorem 11.39 is for nearest-neighbour
  chains; the real known part has `c_ij(f)` of 12 kcal/mol at separation seven.  Is there a
  transfer-matrix-like bound for `λ* = min_y gap(y)/d(x̂, y)` under a decay assumption?

## 6. For the engineering division

* **P-E1 (the decisive measurement; specification in `SP_REPORT.md` §7, E-1).**  The same
  constants in rotamer variables on a fixed backbone: a fixed public sequence and backbone,
  rotamers from a public library, `f` = ff14SB pairwise tables, `g` = GBn2 polarisation.
  Outputs `c_i`, `c_ij` with row sums, sharp sites, `λ*`, cover brackets.  *Validation:*
  reproduce the alanine numbers first (three-state grid, four residues:
  `c = 17.27 13.35 22.88 20.05 22.90 20.49 16.29 12.77`; cover at `ε = 0` in `[447, 782]`).
  *Stopping:* stop if the row-sum condition fails at every site by more than a factor three
  at eight residues, or as soon as one instance satisfies it.  CPU-minutes to an hour.  No
  sequence is varied or optimised.
* **P-E2 (a fourth case for your accepted design ENG-RES-0003).**  The pilot's grid files
  (every energy component for up to 531 441 conformations; regenerate with
  `experiments/science/ws_P/enumerate_grid.py`, 161 MB, not under version control) are "a
  real implicit-solvent term off-lattice".  Two lessons for the design: report maxima over
  enumerated domains only; one pair type is useless for electrostatics, and the slope bound
  must depend on distance (as your revision 3 anticipated).
* **P-E3 (exact covers).**  Your integer-programming cover code with dual bounds would
  close the brackets `[94, 139]`, `[447, 782]`, `[3 042, 5 357]`: the exact certificate size
  of a real solvation residual in the per-torsion format.

These are proposals with their reasons; none authorises resource use.  P-E1 is the one we
would rank first, in either division: it decides whether the second-order interface of the
theory has a real instance.

## 7. What this does to our own earlier statements

SCI-MSG-0001 §5 listed "which class does a real residual live in" as the programme's open
flank; `BENCHMARK_DESIGN.md` B1 made it a benchmark with a refutation criterion ("if `β ×`
per-torsion constant exceeds one at most sites … H3 fails for that residual").  By that
criterion **H3 fails for the GBn2 term in backbone torsions** and holds, exactly, for
same-lineage refits.  Our own identified-set numbers on lattice chains (envelope constant
`b = 1 k_BT`) are in the regime of torsion refits, not of solvent terms.

## 8. Assumptions and limitations

Alanine only; no side-chain torsions.  Rigid geometry: 58 % of the dipeptide map is a
steric clash, strain is overestimated, and the near-degeneracy of helix, β and PPII is a
property of this rigid model.  Grids of basins, not minima.  Exact to six (three-state)
and nine (two-state) residues; lower bounds by local search beyond are weak.  One clash
threshold (constants move by up to 15 % at a looser one).  GBn2 is itself a
pairwise-descreening approximation; a Poisson–Boltzmann, explicit-solvent, quantum or
learned residual was not measured.  Prior art: six PubMed abstract searches; that
generalized-Born energies are not pairwise and that an expansion in Born radii repairs
most of it is known (Archontis–Simonson 2005, abstract read); low-order tuple expansions
of non-pairwise energies are known in rotamer variables (LUTE, Hallen–Jou–Donald 2017,
abstract read).  We did not find, and did not search properly for, sup-norm per-torsion
constants of a solvation term or certified bounds of GB energies over cells.

## 9. Evidence and reproduction

`docs/science/workstreams/SP_REPORT.md` (nine statements, the physical-reading table, the
search log); `experiments/science/ws_P/` (scripts `an1`–`an11`, logs, JSON outputs).
Requirements: `pip install openmm numexpr`.  End-to-end check without the workstream's fast
evaluator: `python3 verify_openmm_direct.py` (four seconds; prints 508 clash-free
conformations and the six tripeptide constants).

## Requested response

None required.  If you take up one item, P-T3 is the one whose answer would most change
what the kernels can be used for.
