# Assumption register — capability C1 (certified GMEC)

Every assumption on which a C1 result (experiment SB-X-001, `experiments/structbio/gmec_dev/`)
rests, as of 2026-11-26 (software `c128625`, theory `b2caab6`). Kinds: **math** (mathematical),
**num** (numerical), **phys** (physical-model), **eng** (engineering). Status: **[V]** with the
Lean declaration (machine-checked by the theory division, not by us); **tested** (test named;
all in `tests/structbio/`); **[N]** numerical evidence; **assumed**. Module paths are under
`src/metricchain_sb/`. Nothing here is "proved by us".

## 1. The certified layer

| id | statement | enters | kind | status | if false | detection |
|---|---|---|---|---|---|---|
| SB-A-01 | The published instance (integer tables, `scale_bits`) *is* the model; every certified statement is about it ([M]) | `model.PairModel`; `run.py` step 2 | eng (definition) | assumed by definition | not falsifiable; the risk is misreading a statement about the tables as one about the force field or the protein | label [M] on every number; `PHYSICAL_APPLICABILITY.md` |
| SB-A-02 | One stored orientation per pair: `P_ij` for `i < j`, `J_ji = 0`; then `PairModel.energy_int` equals `PairInstance.energy` of the Lean kernel | `model.energy_int`; `mincheck.pair_rows`; `to_metricchain_cert1` | math | [V] `verify_sound` (`proofs/CertificateAlgebra.lean:308`) applies to that instance; the symmetrised reading is `verify_sound_real_symm` (`proofs/Frontiers/SymmetricPairHypothesis.lean:129`); tested: `test_energy_is_sum_of_unary_and_pair_tables`, reference-checker agreement | the bound would be about a different energy | differential tests against enumeration and the reference checker |
| SB-A-03 | numpy `int64` arithmetic in the checker is exact. Guard (`mincheck.py` lines 60–62): reject unless `max_abs_entry · 2**mb < 2**50`, `abs(L) < 2**62` and `(Δ + 3) · 2**50 < 2**62` (Δ = maximum degree, i.e. Δ ≤ 4092); a message with `abs(v) ≥ 2**50` is a rejection (line 79). Then every int64 intermediate is below `(Δ + 1) · 2**50` (unary side) or `3 · 2**50` (pair side) or `2 · 2**50` (prune differences), all `< 2**62`; per-site minima are summed as Python integers | `mincheck._check`, `leaf_ok`, `prune_ok` | num / eng | argued here from the code; tested in one case only: `test_checker_rejects_a_certificate_whose_tables_exceed_the_supported_range` | silent wrap-around could make an invalid certificate pass (unsound) | more hostile-input tests (gap, `VERIFICATION_REPORT.md` §5) |
| SB-A-04 | The checker implements the rule semantics of the kernel `verify` restricted to `leaf`, `branch`, `prune` | `mincheck.py` | eng | tested, not verified: `test_certificate_is_accepted_and_exact_on_small_instances`, `test_certificate_with_tolerance_brackets_the_minimum`, `test_checkers_agree_on_mutated_certificates_and_never_accept_a_false_bound` (49 accepted / 226 rejected by both, 13 malformed in our format) | an accepted false bound | SB-BM-1; an independent re-implementation from `VERIFICATION_REPORT.md` §2 |
| SB-A-05 | `to_metricchain_cert1` is exact: the reference checker accepts the converted document iff our checker accepts | `mincert.to_metricchain_cert1` | math / eng | tested (same tests as SB-A-04; `test_reference_checker_accepts_the_converted_certificate`, `test_raising_the_claimed_bound_by_one_unit_is_rejected_by_both_checkers`); argument in `VERIFICATION_REPORT.md` §2.7 | the external cross-check would not test what we claim | disagreement in the differential test |
| SB-A-06 | `model_sha256` identifies the instance: SHA-256 collision resistance [K]; canonical JSON of scale and tables; metadata excluded | `mincert.model_sha256`, `loads`; `modelio` | eng | tested: `test_checksum_changes_when_one_table_entry_changes`, `test_detached_certificate_needs_the_instance_with_the_recorded_checksum` | a certificate could be read against another instance; provenance (PDB id, parameters) is not covered by the checksum | none for collisions; provenance must be checked from `meta` and the row |
| SB-A-07 | The certificate file has one reading | `mincert.loads` | eng | **not met in general**: `loads` uses plain `json.loads` (duplicate keys: last wins) and converts with `int()` (a JSON float is truncated — in `lower_bound`, domains, messages, prune steps, and table entries of an embedded model, whose checksum is computed after truncation). The checker then decides about the object as parsed | the claim checked can differ from the claim a reader sees in the file (no unsound acceptance of the parsed object) | a strict loader as in the reference checker (`load_strict`); not yet written |
| SB-A-08 | For the reading "global minimum", the root domains are the full state sets | `run.py` (interpretation) | eng | assumed; not checked by `check_min_certificate` or `run.py --check`; verified by hand for the six stored certificates (2026-11-26) | a sub-box certificate is accepted (correctly) for a weaker proposition that the row would present as the GMEC | add a full-box check to `run.py` and the row |
| SB-A-09 | Python integers are arbitrary-precision; numpy 2.x raises `OverflowError` for Python integers outside int64 (observed with numpy 2.5.5) | `mincheck`, `model`, `mincert` | eng | assumed [K]; the overflow behaviour was observed once (`message_bits = 80` on zero tables is rejected) | silent conversion could change values | pinned numpy version |
| SB-A-10 | The Lean kernel, Lean 4 and Mathlib (axioms `propext`, `Classical.choice`, `Quot.sound`) are the trusted base of every [V] | all [V] statements | math | the theory division's [V]; the file builds here (Lean 4.31.0, Mathlib v4.31.0); the kernel has **not** been executed on our certificates (memory exhausted at 512 table entries, theory report) | a [V] statement could be false | outside this division |

## 2. From the force field to the integer tables

| id | statement | enters | kind | status | if false | detection |
|---|---|---|---|---|---|---|
| SB-A-11 | The float64 tables equal the stated energy function (ff14SB torsions, Lennard-Jones with 1–4 rules, Coulomb with `ε = 4r`) on the stated states | `molecular/tables.py` | num | [N]: differences agree with an independent OpenMM system to ≤ 3.6·10⁻¹¹ kcal/mol on low-energy configurations and ≤ 4.6·10⁻¹³ relative on random ones (`MOLECULAR_LAYER_REPORT.md` §3); tested: `test_decomposition_matches_openmm_crambin`, `test_decomposition_matches_openmm_ubiquitin` (slow); a wrong `ε0` or missing 1–4 term is detected | the certified minimum would be of a different model than described | SB-BM-4; an independent re-implementation (requested) |
| SB-A-12 | Omitted terms are constant: bonds and angles invariant under chi rotation; no torsion or exception couples moving atoms of two sites; `E_const := 0` | `tables.build_energy_tables` (raises on coupling), `reference.py` | math / num | code raises if coupling occurs; bonded spread ≤ 6.3·10⁻¹² kcal/mol [N]; `test_rotation_preserves_bonds_angles_and_hits_targets` | pairwise decomposition would be wrong | the OpenMM comparison |
| SB-A-13 | Rounding: each entry is the nearest multiple of `2**-20` kcal/mol (exact via `Fraction`, ties to even), so at most `2**-21` per entry and `(n + P) · 2**-21` per configuration (`1.0·10⁻³` kcal/mol for ubiquitin) | `PairModel.from_float` | num | by construction (code read); not separately tested | — (definition) | — |
| SB-A-14 | Clipping: entries are `min(entry, 1000)` kcal/mol from above only; no lower clip. Development entries lie in [−24.2, 1000] kcal/mol (observed 2026-11-26). Since clipping and nearest rounding are monotone, a lower bound for the clipped instance is a lower bound for the rounded unclipped tables; if `x*` uses no clipped entry it also minimises them — **not checked automatically** | `tables.build_energy_tables` | phys | tested: `test_table_api_and_clipping` | the minimiser of the clipped model might use a clipped (clashing) entry and differ from the unclipped one | check the witness's entries against `e_clip` (not done) |
| SB-A-15 | Hydrogen placement by `Modeller.addHydrogens` with Python `random` seeded by `seed = 0`, Reference platform; native-state H are minimised by OpenMM, library-state H are not | `prepare.py` lines 128–134 | eng / phys | tested: `test_preparation_is_reproducible_and_replaces_input_hydrogens` (same machine) | instances not reproducible (defect found before seeding, up to ~70 kcal/mol); bias between native and library states | `run.py --check` compares checksums; cross-machine reproducibility untested |
| SB-A-16 | Protonation at pH 7 and histidine tautomers chosen once by OpenMM's heuristic on the native structure; NH3+/COO− termini | `prepare.py` | phys | assumed; tautomers recorded in `meta` | a different charge state changes the model | none in the pipeline |
| SB-A-17 | First model, first alternate location; partial occupancies without altloc used as deposited | `prepare.py` (`openmm.app.PDBFile`) | phys | assumed; verified on 2IGD Glu20 (`MOLECULAR_LAYER_REPORT.md` §1.1) | another conformer of the deposited model would be the reference | none |
| SB-A-18 | Preparation fails closed (one chain; 20 standard residues; SEQRES length; chain breaks; heavy-atom set; heavy atoms unmoved) | `prepare.py` | eng | tested: `test_rejects_missing_heavy_atom_and_nonstandard_residue`, `test_pdbfixer_repair_only_behind_flag_and_recorded`, `test_native_state_reproduces_input_coordinates` | silently repaired structures | the tests |

## 3. The physical model

| id | statement | enters | kind | status | if false | detection |
|---|---|---|---|---|---|---|
| SB-A-19 | Fixed deposited backbone and fixed sequence | `tables.build_model` | phys | assumed | backbone relaxation changes every table | not detectable inside the model |
| SB-A-20 | Sites: residues with ≥ 1 chi, except PRO and disulfide-bonded CYS; termini are sites | `tables.build_model` | phys | tested: `test_flexible_site_selection_crambin` | different degrees of freedom | — |
| SB-A-21 | Rigid rotation about chi bonds with deposited bond lengths and angles; hydroxyl/amine H rotate rigidly with the last chi | `chi.rotate_about_axis`, `tables._make_site` | phys | tested: `test_rotation_preserves_bonds_angles_and_hits_targets`, `test_chi_atoms_are_bonded_chains_and_measure_like_independent_formula`, `test_dihedral_known_values` | geometry of states differs from intended | the tests |
| SB-A-22 | Rotamer rule: native state plus the idealised staggered library (`rotamers.py`), 4 to 82 states per site; no de-duplication | `rotamers.library_values` | phys (discretisation) | tested: `test_library_is_symmetry_aware`, `test_chi_table_covers_twenty_residue_types` | the minimum over this set is not the minimum over continuous torsions (never claimed) | discretisation term is unquantified |
| SB-A-23 | Energy: ff14SB parameters as assigned by OpenMM, in vacuo, distance-dependent dielectric `ε(r) = 4r`, no cutoff, no solvent | `tables.py` | phys | assumed; a model choice, not evidence | conclusions about the protein would not follow (they are not drawn) | none inside the model |
| SB-A-24 | toulbar2 is an untrusted oracle: agreement is an observation, not evidence of soundness | `baselines/toulbar2.py` | eng | 6/6 agreements in SB-X-001; `test_toulbar2_minimum_equals_exhaustive_enumeration` (skipped in the present venv: `pytoulbar2` not installed) | a shared modelling error is invisible to agreement | — |

## 4. Assumptions that C2 will add (planned design)

- **Thermal dead-end elimination:** each step's margin is exact on the integer instance, and the
  multiplier `1 + exp(−β·margin)` is enclosed from above.
- **Product-form relaxation:** for every relaxed pair, `J = f(a) + g(b) + R(a,b)` exactly, with
  `r_lo ≤ R ≤ r_hi` verified on the current box; `f, g` added exactly to one-body terms.
- **Certified exponential:** `exp_enclosure` and `Z_encloses_partitionFn` ([V], theory
  `b2caab6`) with outward rounding; `β` a stated rational.
- **Elimination:** exact on factor tables along the stated order; conditioning sites stated.
- **Float tier:** IEEE-754 binary64 with round-to-nearest for `+` and `×`, outward rounding after
  every multiplication and an a-priori error factor for every sum; no fused or extended-precision
  operations, no reordering by the compiler or library (not yet specified: the bound we intend to
  use for sums holds for every order of summation and every precision at least binary64, so
  reordering is harmless there; for products we round outward after each elementwise operation;
  to be written out and tested when C2 is implemented).
- **Abstention:** a memory budget per table; no interval is reported when it would be exceeded.
- **Kernel:** the elimination rules are not yet in the theory division's kernel; their soundness
  will rest on a statement still to be written and reviewed.
