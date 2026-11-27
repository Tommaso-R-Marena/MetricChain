# Physical applicability register

What the objects computed by this division's software stand for physically, how far each
guarantee reaches, and what is not claimed. Date 2026-11-26; software `c128625`; results of
SB-X-001 (`experiments/structbio/gmec_dev/results.jsonl`, development evidence only). The
science division's orientation SCI-MSG-0034 (science commit `4661a03` as read) is adopted where
stated. Every certified statement here is model-conditional ([M]); none is a statement about a
protein.

## 1. Dictionary

| object in the software | stands for | measured / certified / estimated | where the guarantee stops meaning anything |
|---|---|---|---|
| site `i` | one residue with ≥ 1 chi angle, not PRO, not disulfide-bonded CYS, on a fixed deposited backbone | defined | residues outside the site set are frozen at deposited coordinates; backbone motion is outside the model |
| state `a` of site `i` | a side-chain conformation: state 0 = deposited (prepared) coordinates; others = rigid chi rotations to idealised staggered values | defined | it is one point, not a region of torsion space; nothing is said between grid points |
| integer table entry | `2**-20`-kcal/mol rounding of a pairwise or one-body energy term of ff14SB torsions + Lennard-Jones + Coulomb with `ε = 4r`, in vacuo, clipped above at 1000 kcal/mol | the integers are exact by definition; their agreement with the float energy function is [N] | beyond the model: solvent, polarisation, protonation changes, backbone relaxation, the real-valued force field (not proved), nature (not addressed) |
| energy `E(x)` | model energy of a configuration *relative to an omitted constant* (`E_const := 0`: fixed-atom terms not computed) | exact rational for the instance | absolute values have no meaning; only differences between configurations of the same instance |
| box `∏ D_i` | the set of configurations the statement quantifies over | given in the certificate | a statement over a sub-box says nothing outside it (the GMEC reading needs the full state sets) |
| certified minimum `L` (with gap 0) | the lowest model energy over all configurations of the box | certified ([CK], [M]) | at the model; no statement about the force field's real-valued energy, about continuous torsions, or about the protein |
| certificate | a tree of dead-end eliminations, case splits and dual-bound leaves that an exact checker accepts | checked by `mincheck.py` | the checker implementation is tested, not formally verified; the Lean kernel was not run on it |
| witness `x*` | one configuration attaining `L`: the global-minimum-energy conformation (GMEC) of the model | its energy is evaluated exactly | not a predicted structure; uniqueness is not certified (ties are possible) |
| *planned:* Boltzmann weight | `exp(−β E)` of a state or pair term, enclosed by a certified exponential with outward rounding | to be certified (C2) | as for the tables, plus the choice of `β` |
| *planned:* partition function `Z`, free energy `−kT ln Z` | sum of weights over the discrete box | to be certified as an interval (C2) | `ln Z` of a discrete rotamer model on a fixed backbone; observable only in differences, and not a free energy of the protein |
| *planned:* population interval | probability of a rotamer state under the model's Boltzmann distribution | to be certified as an interval (C2) | not an experimental population; discretisation is unquantified |
| *planned:* flip gap `G_i` | model-energy cost of moving residue `i` out of its GMEC state | to be certified from below (C1b) | a margin within the model; only meaningful against a stated bound on model error, which nobody has |

## 2. Four-line error budget for the C1 results (from STRUCTBIO-MSG-0001)

| line | value | source |
|---|---|---|
| (i) certified width | 0 for all six structures, for the integer tables | SB-X-001 rows, `certified_gap_kcal = "0"` |
| (ii) discretisation | not bounded for our tables; the claim is about the discrete state set, not continuous torsions.  **Measured by the science division on capped blocks** (SCI-REV-0025 §3; ff14SB with a solvent term, ideal backbones, rigid geometry; [M], unrefereed, not our energy model): a rigid ideal-rotamer table puts `ln Z` off the continuous value by −3.2 to +2.0 nats per torsion, moves rotamer-well populations by up to 0.48 in total variation, and for one capped leucine puts the table's minimum in a different well from the continuous minimum | SCI-REV-0025 (science `2796bec`) |
| (iii) energy model | refits within one force-field lineage change single-residue terms by 1.1 to 4.4 `kT` (SCI-MSG-0034 §2.3); a vacuum model with `ε = 4r` is cruder than that | science division [M]; this division's model choice |
| (iv) evaluation and rounding | ≤ 4·10⁻¹¹ kcal/mol observed disagreement with OpenMM on low-energy configurations [N]; rounding moves a configuration's energy by at most `(n + n(n−1)/2)·2⁻²¹` kcal/mol (1.0·10⁻³ for ubiquitin) | `MOLECULAR_LAYER_REPORT.md` §3; `model.from_float` |

Line (iii) is at least three orders of magnitude above the rounding bound of line (iv) and ten
above its observed agreement; line (i) is zero.  The certificate replaces trust in an exact
solver's implementation by trust in a checker, and changes no number here.

*(Corrected 2026-11-27 after SCI-REV-0026 §1; RESULTS.md, correction RC-3.  The earlier text
read: "Line (iii) is five to six orders of magnitude above line (i): the certificate removes
search error from a model-relative statement and nothing else."  Line (i) is zero, so that was
not a comparison; and no search error was exhibited — an exact solver without certificate
returned the same optimum on every instance.)*

**Line (iii) has a further entry for model v1, measured 2026-11-27 (RESULTS R-8):** the seed of
the hydrogen placement.  Between seeds 0 and 9 the certified minimum of a v1 table ranges over
12.8 to 24.6 kcal/mol and up to 4 to 15 % of the sites change state.  Model v2 has no seed.

## 3. What the certified minimum says, and what it does not

| PDB | sites | sites whose GMEC state index ≠ 0 | model energy, deposited state (kcal/mol) | certified minimum (kcal/mol) | deposited − minimum |
|---|---|---|---|---|---|
| 1CRN | 26 | 8 | −34.161 | −36.476 | 2.32 |
| 5PTI | 36 | 16 | −98.169 | −130.228 | 32.06 |
| 1BPI | 36 | 10 | −114.262 | −138.260 | 24.00 |
| 1PGA | 46 | 26 | 24.063 | −13.875 | 37.94 |
| 2IGD | 49 | 14 | −26.552 | −38.124 | 11.57 |
| 1UBQ | 65 | 37 | 50.433 | −88.696 | 139.13 |

(Energies relative to the omitted constant; "state index ≠ 0" counts sites not in the
deposited state; a library state may coincide geometrically with the deposited one, since no
de-duplication is done.)

It says: within this model, no configuration of the discrete state set has lower energy than
the witness. It does not say that the deposited side chains are wrong, that the witness is
closer to nature, or that the model is good. On ubiquitin (model v1) the minimum uses a library state rather than the
deposited state at 37 of 65 sites (how many of these lie in another rotamer well was not
counted on v1; on v2 28 of 65 sites are in another well, RESULTS R-9) and lies 139 kcal/mol
below the deposited configuration; the molecular-layer report explains
the mechanism in this model (in vacuo with `ε0 = 4`, charged side chains collapse onto each
other, `MOLECULAR_LAYER_REPORT.md` §3). A further bias: hydrogens of the deposited state were
minimised by OpenMM and those of library states were not. These are properties of the model. A
comparison with deposited conformations (SB-BM-6) would test the energy model, not the
certificate.

## 4. The science division's limitations (SCI-MSG-0034 §2), applied to our model

| # | limitation (one line) | applies to our model as built? |
|---|---|---|
| 1 | Certificates are about the discrete model; discretisation is the largest unquantified term | Yes. C1 claims the minimum over a 60°-or-coarser grid plus the deposited state; no continuous claim; the term is unquantified |
| 2 | Fixed backbone, ideal geometry; pairwise only on a fixed backbone | Yes for the fixed backbone (deposited, not ideal); bond geometry is the deposited one, not ideal; our structures are proteins, not capped peptides, but nothing about backbone freedom is covered |
| 3 | Energy-model uncertainty is of order `kT` per residue; certificates resolve far finer | Yes, more strongly: our vacuum `ε = 4r` model is cruder than the refits the science division measured |
| 4 | No production force-field constant is certified except by evaluation; evaluator tolerance unproved | C1 needs no class constant; the tables are defined as the rounded values, and their agreement with OpenMM is [N] only. It is why C5 is blocked |
| 5 | Compactness and charge make the residual method expensive | The residual method is not used by C1. Charge does dominate our model's pathology (ubiquitin) and the C2 obstruction (long-range Coulomb weak pairs, ~113 nats first order) |
| 6 | `ln Z` is observable only in differences; kinetics on voxel graphs are not rates | Applies to C2 when built; for C1 absolute table energies are meaningless (constant omitted) |
| 7 | Averaged data identify little; worst cases are real | Not applicable to C1 (no observation model); applies to C3 and C4 |
| 8 | Query-complexity exponents are for idealised regimes, not cost predictions | Not used by this division's software; we make no cost prediction from them |

## 5. Theorems that cannot presently be translated into a useful biological computation

From `THEOREM_TO_SOFTWARE_REGISTER.md` Part B and `RESEARCH_INTAKE.md` §3.

| result | reason | what would change it |
|---|---|---|
| Residual kernel `verifyITop_sound`, `IProblem.consistent_iff_nonempty` [V] (C5) | no certified first-order constant exists for any real energy term | certified `c_i` for one real term, e.g. by interval evaluation of a force-field term |
| Share certificates and third-order models (`F/StateShares.lean`, `F/ThirdOrderModel.lean`) | their constants are exact maxima over enumerated domains, not certified constants; completeness fails on non-product domains | certified `c_ij` / `c_T` |
| Science P-series constants (P3, P8, P9) | paper proofs by one workstream; code not reviewed; evaluator tolerance unproved | independent review and an outward-rounded evaluator |
| Query-complexity and exponent theory | idealised classes, asymptotic, worse than plain Monte Carlo at simulable sizes | finite-size constants on a rotamer class |
| Voxel / continuous-rotamer enclosures | no interval evaluator of force-field terms exists; `d^{d/2}` cost | a verified interval evaluator for LJ/Coulomb over chi cells |
| Barrier and macro-ratio certificates | no JSON or reference-checker entry point; plans as large as the macrostates; not refereed | a schema, a checker, a size bound on realistic move graphs |
| Linear/profile kernel `verifyLTop_sound` | class too small, constants vacuous (`10^93`–`10^2697`) | a real feature map with small coefficient boxes |
| STRANDS, NANUQ | nucleic acids and phylogenetics | none expected |
| Ising ground-set theorems | ±1 spins on complete graphs; rotamers are q-ary on sparse graphs | a q-ary local-polytope analogue |
| Penalty-threshold bracket | product reference only; void on science's floors; unreviewed | review and a band-reference version |
| Ensemble positive theorems under exact observables | exact laws, generic conformers; no stability modulus under bands | a stability modulus; review of Part VI |
| Geometry Theorems A–G, I | exact, state-independent bond geometry; `κ` uncertified | certified `κ` and a perturbation theory for inexact geometry |

## 6. Claims this division will not make

Adopted from SCI-MSG-0034 §4 where applicable, and specific to our software:

- that a certified minimum is a predicted structure, or that the GMEC of our model is the
  side-chain arrangement of the protein;
- that a certified property of the integer tables is a certified property of the force field's
  real-valued energy (the step is [N] only) or of nature;
- that a certified free energy or population (when C2 exists) is that of a protein rather than
  of a rotamer model on a fixed backbone;
- that a constant measured on a grid or fitted on a sample is a bound;
- that a root-mean-square error of a surrogate certifies a free energy;
- that a certified barrier on a graph of rotamer labels is a barrier of the molecule;
- that agreement with averaged data establishes a structure, order or disorder;
- that anything here has been compared with a measurement — nothing has;
- that any of this is new: certified optimality with checkable proofs is established technology
  in neighbouring solver fields (`PRIOR_ART.md` §B), and no comparison with pseudo-Boolean proof
  logging has been run;
- that our producer is fast: toulbar2 is 7 to 25 times faster on every development structure;
- that development results predict held-out performance: no held-out result exists;
- that a correct implementation, a passing test suite or a machine-checked theorem makes a
  scientific conclusion — each verifies a statement about the model.

## Addendum, 2026-11-26 (after the science division's first review, SCI-REV-0025)

1. **Wording.**  What capability C1 returns is the **certified minimum of the table** — of the
   integer rotamer tables of a stated model.  "GMEC" and "global minimum" in earlier text of
   ours mean this and nothing more.
2. **The discretisation line is no longer "unknown".**  The science division's measurement
   (line (ii) above) says a rigid-rotamer table can place its minimum in the wrong well and
   misstate free energies by nats per torsion.  Our tables use the same ideal staggered values
   and no minimisation inside a cell, so the finding applies; two differences that we have not
   measured are that we rotate the deposited geometry and include the deposited state.
3. **What our own certified numbers add to that picture** (RESULTS R-6): in the tables
   themselves the minimum is nearly degenerate — second-best within 0.004 to 0.11 kcal/mol,
   61 to 81 % of residues able to change state below `3RT`.  A certified minimum of such a
   table is a weak description even of the table's own ensemble.
4. **A constructive direction named by the science division**: states that are cells carrying
   their own free energy, pair tables that are cell averages, and one allowance table in the
   certificate (its addendum A17 (26), item 101 (b); unrefereed; tested on valine pairs).  For
   us this would change the table builder and leave certificates and checkers as they are.
   Not started; recorded as open problem SB-OP-04.
