# Workstream P2 — the decisive measurement: class constants of a real residual in rotamer variables on a fixed backbone

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_P2/`; your report: `docs/science/workstreams/P2_REPORT.md`.
(Second wave.  You continue workstream P: read `docs/science/workstreams/SP_REPORT.md` — all of
§1, §2, §2.B, §3.1, §5, §6 — and `docs/science/PHYSICAL_APPLICABILITY.md` before anything else.
P's code is in `experiments/science/ws_P/`: `pepbuild.py` (internal-coordinate builder),
`fastff.py` (a numpy re-implementation of OpenMM's ff14SB and GBn2 energies that agrees
with OpenMM to `5·10⁻¹²` kcal/mol), `enumerate_grid.py`, the analysis scripts `an1`–`an11`.
You may import or copy them into your own directory; do not modify `ws_P/`.  OpenMM 8.6.1
and numexpr are installed.)

## Why this measurement decides something

The theory division's kernels need a **known part that is pairwise in the site
variables**, and their cheap classes need **small per-site constants** or **weak
second-order coupling**.  Workstream P measured a real implicit-solvent residual (GBn2
polarisation energy against ff14SB) in *backbone torsions* of alanine peptides and found
the opposite of what the theory needs: per-torsion constants of `12–53 k_BT` growing with
chain length, dense second-order couplings, no sharp site — and a known part that is not
pairwise in torsions at all.  But backbone torsions are the *wrong* variables: every atom
beyond a torsion moves with it (the lever arm).  **On a fixed backbone with side-chain
rotamers as site variables each atom depends on one site**, the molecular-mechanics energy
is exactly pairwise in the sites, and there is no lever arm.  That is the setting of
fixed-backbone side-chain placement, the one arena in which the theory's assumptions
could hold for a real molecule.  Nobody in the programme has measured the constants
there.  Our own ranking (`docs/science/PUBLICATION_OPPORTUNITIES.md` §4, item 2) puts this
measurement second among everything the three divisions could do next.

**Scope (hard).**  Fixed sequences, fixed backbones, no sequence is varied, compared or
optimised for any property; this is a measurement of a force-field term on synthetic
model peptides.  Use *generic* sequences stated in advance: homopolymers with rotatable
side chains (e.g. leucine, valine, serine, lysine, phenylalanine — whichever your builder
supports reliably) and **one** fixed heteropolymer made by repeating a stated pattern
(e.g. `L K S E`).  Backbones: ideal α-helix, ideal extended strand, ideal polyproline-II,
built with P's builder (no download is needed).  Do not go beyond this.

## The questions

1. **Is the known part pairwise?**  With the backbone fixed and all bond lengths and
   angles rigid, verify numerically that the ff14SB vacuum energy is a sum of one-site
   and two-site terms in the rotamer variables (all third-order mixed differences zero to
   rounding).  State which choice of "site" you use (one site per residue with all its χ
   angles; or one site per χ angle — in which case χ₂ moves with χ₁ and the energy is
   pairwise only per residue: say so).
2. **First-order constants** `c_i` of the GBn2 polarisation energy `g_GB` in rotamer
   variables, exactly on enumerable grids (three staggered states per χ; clash filter as
   in P, with the same threshold and a sensitivity check): as a function of chain length
   (as far as exact enumeration goes, then sampling with honest lower-bound labelling),
   of position, of residue type and of backbone conformation.  **Do they grow with chain
   length?**  P's prediction: no — they should be bounded by the solvation of one side
   chain.  Test it.
3. **Second-order constants** `c_ij(g_GB)`: size, decay with sequence separation and with
   spatial distance between the side chains; half row sums `½Σ_j c_ij` against the
   single-site excitation energies of the known part (the row-sum condition of theory
   report §11.7, Theorems 11.16–11.17: `grep -n 'Theorem 11.16\|Theorem 11.17\|11.7 ' docs/THEORY_REPORT.md`);
   the Dobrushin-type sums `Σ_j tanh(βc_ij/4)` (Theorem 11.33).  **Does any instance satisfy
   the hypotheses of the second-order interface?**  If one does, compute what the theorems
   then give for it (certificate size for the minimum; the free-energy bracket).
4. **Sharpness and certificates on the real instance**: number of sharp sites, the
   collective ratio `λ*`, smallest certificates of the minimum in the per-site format
   (forced points, volume bound, greedy cover — as in P's `an7_sharpness.py`), for
   `ε ∈ {0, k_BT, 2 kcal/mol}`.
5. **The typical-norm gap**: sup against RMS of single-site changes; the exact Jensen gap
   `ln Z(f+g) − ln Z(f) + β⟨g⟩_f` against the class bound `Σ_i ln cosh(βc_i/2)`; remainders of
   the best one-site and two-site fits of `g_GB` in rotamer variables, in RMS and in sup
   norm (sup norms over *enumerated* domains only).
6. **Same measurements for one force-field difference** (e.g. ff03 − ff14SB or
   ff15ipq − ff14SB) as a moderate residual, for comparison with P's Statement 4.
7. **Comparison table with P**: the same quantities in backbone-torsion variables (P's
   numbers) next to yours in rotamer variables.

## Controls and validation (do these first)

* Reproduce P's end-to-end check (`ws_P/verify_openmm_direct.py`: 508 clash-free
  conformations, `c_i = 16.09 12.41 18.63 16.43 15.14 11.19`).
* Validate your side-chain builder: bond lengths, angles, chirality, and energies
  against OpenMM's Reference platform on random rotamer states (P reached `5·10⁻¹²`).
* A synthetic residual that is exactly pairwise in your site variables must give
  `c_ijk = 0` and zero remainder of the two-site fit; a random residual must not.

## What would count as a result

* *"The second-order interface has a real instance"*: some chain, backbone and residue
  type for which the row-sum condition holds — then say exactly which theorem applies
  and what it certifies, with numbers.
* *"It does not, even here"*: constants and row sums with their dependence on length,
  showing by how much the hypotheses fail and why (long-range electrostatics? the
  many-body Born radii? clashes?).
* Either way: every number is an exact property of a finite grid of a rigid model —
  a lower bound for the continuous problem; say so wherever a number appears.

## Deliverable

`docs/science/workstreams/P2_REPORT.md` in the format of COMMON (verdicts; precise statements
with labels, **[M]** for measurements on the named model as in `SCIENCE_TO_ALL.md`; numerics
with sizes and how to re-run; prior art with reading levels — at least: what is known
about pairwise decomposability of generalized-Born energies in side-chain placement;
what you did not settle; next steps; requests).  Final message: at most 600 words.
