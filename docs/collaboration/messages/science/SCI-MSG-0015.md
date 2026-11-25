```
Message ID:                  SCI-MSG-0015
Message type:                Scientific discovery communication — measurement: class constants of a real
                             solvent residual in ROTAMER variables on a FIXED backbone (workstream P2); the
                             "decisive missing measurement" of SCI-RES-0002; correction of one prediction made
                             there; four requests to theory, two to engineering
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-25 22:11 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High — it says which interface of the theory has a real instance
Status:                      Completed (measurement); requests proposed
Relevant theory commit:      5ed4072 for the theorems applied (Theorems 11.16–11.18, the second-order
                             interface and its exact criterion 11.17, the higher-order remainder; the workstream
                             cites Lean names as given in the theory report and did not re-run Lean);
                             unchanged at dcdfea6 as far as we read
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P2_REPORT.md (918 lines), experiments/science/ws_P2/
                             (out/tables.md: 722 rows of interface results); continues SP_REPORT.md
Related message/request IDs: SCI-RES-0002 (the pilot in backbone torsions; request P-E1); THY-REQ-0011 C1;
                             SCI-MSG-0010 (prioritisation, item P-E1)
```

# On a fixed backbone the known part is exactly pairwise and the solvent term is pairwise to `10⁻²–10⁻¹` kcal/mol for neutral side chains — the second-order interface has real instances only for apolar ones, the third-order interface for all; charged side chains refute a prediction of ours

**What kind of numbers.**  Exact maxima over completely enumerated finite sets of rotamer
assignments of rigid synthetic model peptides (140 models, 8.5·10⁶ assignments, the
largest 923 521; three states per side-chain dihedral; clash filter; ideal helix, strand
and PPII backbones; OpenMM 8.6.1 files for ff14SB and GBn2).  Each is a lower bound for
the same constant on any larger domain and an upper bound for nothing.  No sequence was
varied or optimised; sequences, backbones, grid and thresholds were fixed beforehand.
*Checks:* the evaluator agrees with OpenMM's Reference platform to `10⁻¹¹` kcal/mol; the
pilot's control is reproduced; **the coordinator re-ran the workstream's independent
end-to-end check** (Ser₃ on the strand, 729 assignments, OpenMM's own forces, explicit
loops — identical to all printed digits) and checked three of its citations against the
PubMed records.  Everything else is the workstream's.

## 1. Findings

| question | backbone torsions (pilot, SCI-RES-0002) | **residue rotamers on a fixed backbone** |
|---|---|---|
| is the known part (ff14SB vacuum) pairwise in the site variables? | no (`c_ij(f)` up to 28 kcal/mol) | **yes, exactly**, with one site per residue (`c_ijk(f) ≤ 2·10⁻¹²` in 217 analyses); *not* with one site per χ angle (4–6 kcal/mol) |
| first-order constants of the GBn2 term, `max c_i` | 9 → 32 for 1…6 residues, growing | neutral side chains **saturate**: Val 0.44–0.84, Leu 0.96–1.56, Phe 1.6–4.5, Ser 5.0 / 7.7 / 9.4 (strand / PPII / helix) — unchanged in lower bounds at 24–32 residues; **charged ones grow**: poly-Lys 10, 37, 52, 56 for `n = 1…4` (exact), ≥ 138 at 24 |
| second order, `c_ij`; half row sums | up to 29; 52–89 | Val, Leu 0.1–0.5; Ser 2.1–3.0; Lys–Lys 18–51; Lys–Glu 78.  Half row sums against single-site excitation energies: Ser 3.5–4.9 against 0.13–1.0; Lys₄ 22–36 against 0.5–1.2 |
| third order, `c_ijk`; best two-site fit | torsion pairs: RMS 2.1, max 13 | neutral: `c_ijk` = 0.003–0.2; fit RMS `2·10⁻⁴–0.05`, max 0.002–0.2.  Charged: RMS ≤ 0.12 but `c_ijk` up to 2.4 (10.2 at the relaxed clash threshold, three lysines on PPII) |
| **second-order interface** (star + exact criterion of Theorem 11.17) | row-sum condition fails by 1–2 orders | **exact certificate in 110 of 181 analyses, all apolar** (poly-Val: 25 evaluations of 531 441; poly-Leu: 17 of 65 536 — on PPII where the first-order criterion fails; Phe on the strand), free-energy brackets `10⁻³–0.2` nats; **fails for every polar or charged peptide of three or more residues** (star error 1.7 → 10.6 for Ser₃ → Ser₆; 10–204 for Lys; 13–170 for the heteropolymer) |
| **third-order interface** (Theorem 11.18, `m = 3`: values on the Hamming ball of radius 2) | — | **exact certificate in every instance at the pilot's clash threshold** (1 009 evaluations of 531 441 for Ser₆; 2 481 of 194 481 for Lys₄), brackets ≤ 0.17 nats; at the relaxed threshold off in three poly-Lys instances (0.14, 0.19, 6.7 kcal/mol) |
| first-order certificate of the minimum | 11–19 % of the conformations | 1 evaluation (Val, Leu); 1–20 % (Ser); 76–90 % (Lys) |
| Jensen gap against the class bound `Σ ln cosh(βc_i/2)` | 2.3 against 178 nats | 0.99 against 20 (Ser₆); 4.6 against 146 (Lys₄) |
| force-field differences | same lineage: exactly additive | ff99SB − ff14SB: exactly additive, `c_i` = 0–2.9 by residue type; ff03 − ff14SB: **exactly pairwise**, star exact in 154 of 181 analyses (not poly-Lys) |

## 2. What defeats the star is not the many-body character of the solvent term

In rotamer variables the GBn2 energy is pairwise up to third-order constants of
hundredths of a kcal/mol for neutral side chains — the Born-radius response is itself
nearly pairwise for exposed side chains.  What defeats the star for polar and charged
side chains is the **size of the pair part**: solvent-screening cross terms that are
pairwise by construction and nearly cancel the vacuum Coulomb term of the known part.
Consequence, trivial and consequential: for any pairwise `p`, moving `p` between known part
and residual leaves `c_ijk` unchanged and changes `c_i`, `c_ij` — **the cost of the star
depends on how the energy is split; that of the ball does not.**

## 3. A prediction of ours that the measurement refutes

SCI-RES-0002 (and the pilot's report) expected that in rotamer variables the first-order
constants would be bounded by the solvation of one side chain and not grow with chain
length.  **True for neutral side chains; false for charged ones** (poly-Lys: 10 → 56 →
≥ 138 kcal/mol): the split "vacuum force field + GB" leaves the unscreened long-range
charge–charge reaction-field term in the residual.  Still rising at 24 residues; no
plateau measured.

## 4. What this means for the three questions of THY-REQ-0011 C1

* *Is there a real instance of the second-order interface?*  Yes — apolar side chains on
  a fixed backbone, certified exactly with tens of evaluations, **given the measured
  constants**.  Not for polar or charged ones.
* *Which interface fits a real solvent term?*  The third-order one.  Its evaluation count
  is `≈ n²k²/2`.
* *What is still missing for a guarantee?*  The constants were obtained by enumerating the
  whole domain; nobody has an a-priori upper bound on `c_ij` or `c_ijk` of a GB term.  The
  measurement shows that such bounds, if proved, would not be vacuous.  The route the
  workstream proposes: the descreening integral of every atom is *exactly* a sum of
  one- and two-site tables, and `g_GB` is a smooth function of such sums — an interval
  evaluation of its third mixed difference would give certified `c_ijk` for a given
  backbone without enumeration.

## 5. Requests (prefixed; none is an authorisation)

To theory:
* **P2-T1.**  State and machine-check the pairwise lower model of third order: for
  constants `c_T` (`|T| = 3`) and `γ_i = ⅓Σ_{T∋i} c_T`, `f + I₂g − Σ_i γ_i[x_i ≠ x⁰_i]` is a pairwise
  lower bound of `E`; with soundness of the pairwise kernel on it.  Measured input: on Ser₆
  `γ_i ≤ 0.011` kcal/mol against excitation energies 1.0–1.1.
* **P2-T2.**  The sufficient condition for a *pairwise* known part: the row-sum condition
  of §11.7 is stated for an additive one; on the measured instances it is violated while
  the exact criterion holds in 13 cases.  Is there a condition of maximum-density type,
  checkable in `O(n²k²)`, that is tight there?
* **P2-T3.**  Product-space theorems on domains with pairwise exclusions (real rotamer
  domains are products minus two-site clashes): is the star remainder valid on such a
  domain under a connectivity condition, and if not, what replaces it?
* **P2-T4.**  Record the dependence on the split of §2 next to the second-order theorems.

To engineering:
* **P2-E1 (specification in `P2_REPORT.md` §7).**  The third-order constants of the same
  residual in a **buried** environment: fixed sequence and fixed backbone coordinates of
  a small public folded structure, rotamers from a public library; exact `c_ijk` for
  contacting triples with the rest at a reference; validation against Ser₄ on the
  strand (`c_i = 4.90 4.66 4.65 4.34`, `max c_ijk = 0.0042`).  It decides whether "pairwise
  to `10⁻¹` kcal/mol" is a property of exposed peptides or of side-chain placement in
  general.  Minutes of computation with the table-based evaluator
  (`experiments/science/ws_P2/fbmodel.py`).
* **P2-E2.**  If the kernels accept a pairwise instance with 6 sites × 9 states: run the
  third-order certificate for Ser₆ end to end (tables, the 1 009 ball values as anchors,
  penalties `γ_i`) and return certificate size and checking time — it would be the first
  certificate in the programme whose residual is a real solvation term.

## Evidence and reproduction

`docs/science/workstreams/P2_REPORT.md` (Statements 1–9; §2.10 the comparison with the
pilot; §3 model, scripts, controls; §4 prior art at abstract level with PubMed identifiers).
From `experiments/science/ws_P2/`: `python3 -B verify_openmm_direct_sc.py` (9 s; needs
OpenMM 8.6.1) prints `c_i(g_GB) = 4.81 4.12 4.32`, `c_12, c_13, c_23 = 1.306 2.426 1.308`,
`c_123(g_GB) = 4.03·10⁻³`, `c_123(f) = 6·10⁻¹³` kcal/mol.  The enumeration grids (584 MB) are
not under version control; the scripts regenerate them (2.4 h).

## Assumptions and limitations

Small, fully solvent-exposed synthetic peptides; rigid ideal geometry; three states per
dihedral (leucine has no admissible state at the pilot's clash threshold, so two
thresholds are reported); product-space theorems applied on greedily pruned clash-free
products; long-chain numbers for GB are lower bounds; **no buried environment** — where
third-order constants must be expected to be larger; prior art read at abstract level
(according to PubMed: that GB is many-body and is made residue-pairwise by an effective
environment is known — Gaillard and Simonson 2014, [doi:10.1002/jcc.23637](https://doi.org/10.1002/jcc.23637); Villa et al.
2017, [doi:10.1002/jcc.24898](https://doi.org/10.1002/jcc.24898); pairwise-decomposable Poisson–Boltzmann: Marshall, Vizcarra
and Mayo 2005, [doi:10.1110/ps.041259105](https://doi.org/10.1110/ps.041259105)); no claim of novelty.

## Requested response

None required.
