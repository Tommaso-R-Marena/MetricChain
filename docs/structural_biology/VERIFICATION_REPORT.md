# Verification report — `min` certificates (capability C1)

Date 2026-11-26. Software `c128625` (results `c3aa6f9`); theory kernel and reference checker at
`b2caab6`. All reviews named here are this division's own tests; none is an independent review.

## 1. Labels

- **[CK]** — a certificate accepted by an exact-arithmetic checker whose *rule semantics* are
  machine-checked in Lean (the declaration is named), the checker *implementation* being tested
  but not verified; the certificate file, its sha256 and the checker commit are named.
- **[CP]** — as [CK], but the rule semantics rest on a named paper proof, not on Lean.
- **[M]** — model-conditional: true of the published tables of rationals (the instance). The link
  between the instance and a physical energy function is stated separately and is never
  certified by this label.
- **[H]** — heuristic or uncertified estimate (floating-point solver, sampler, belief
  propagation, a solver's claim without certificate); never a certificate.

Combination with the other divisions' labels (`docs/collaboration/README.md`): [CK] cites a
[V] declaration of the theory division and never upgrades to [V]; a C1 number is always [CK]
*and* [M]; the instance–energy link is [N]; timings are [E] with the platform; toulbar2's
optimum is [H] for us. A [CK] result is an exact computation with certified optimality on the
integer instance and so meets the wording of the engineering division's [X]; we do not co-label:
[X] is that division's label for computations it has made or replicated, and ours becomes
[X]/[R] only when it has done so (coordinator, 2026-11-26). Independent re-runs by another division would be [R]. No
label of ours upgrades a mathematical statement, and none applies to nature.

## 2. Specification of the `min` certificate and its checker

Sufficient for re-implementation; checked line by line against `mincheck.py` and `mincert.py`.

### 2.1 Objects and units

- Instance: `n ≥ 0` sites; site `i` has states `0 … k_i − 1`, `k_i ≥ 1`; integer one-body
  tables `U_i(a)`; a set `Π` of listed pairs `(i, j)` with `i < j`, each with an integer table
  `P_ij(a, b)` of shape `k_i × k_j`; scale `s ≥ 0`. Energy
  `E(x) = 2^−s ( Σ_i U_i(x_i) + Σ_{(i,j)∈Π} P_ij(x_i, x_j) )` (exact rational; kcal/mol for the
  molecular layer). `N(i)` = sites `j` with `{i, j}` listed.
- Certificate: `mb ≥ 0` (message bits); unit `u = 2^−(s+mb)`. Scaled integer tables
  `H_i(a) = U_i(a)·2^mb`, `J_ij(a,b) = P_ij(a,b)·2^mb` for `(i,j) ∈ Π`, and the reading
  `J_ij(a,b) := J_ji(b,a)` for `i > j`. Claim: integer `L` (the bound is `L·u`), optional
  witness `w`. Root box `D⁰ = (D⁰_0, …, D⁰_{n−1})`. A tree of nodes.

### 2.2 Well-formedness (`validate_structure`, `mincert.py` lines 72–137)

Integers are Python/numpy integers that are not booleans. Reject unless:
1. `mb` is an integer `≥ 0`; `L` is an integer;
2. `D⁰` is a list of `n` non-empty lists of integers in `[0, k_i)` without repeats;
3. `w` is absent, or has length `n` with `w_i` an integer in `[0, k_i)`;
4. every node is a mapping whose `node` field is `leaf`, `branch` or `prune`, with no other
   fields than: leaf `{node, m}`; branch `{node, site, children}`; prune `{node, site, remove,
   dominator, rest}`;
5. leaf: `m` (default empty) maps keys `(i, j)` — integers, `0 ≤ i, j < n`, `i ≠ j`,
   `{min, max}` listed — to lists of exactly `k_i` integers;
6. branch: `site` an integer in `[0, n)`; `children` a mapping from integers in `[0, k_site)` to
   nodes (all children are validated, visited or not);
7. prune: `site` in `[0, n)`; `remove`, `dominator` integers in `[0, k_site)`; `rest` a node.

The instance itself is validated on construction (`PairModel.__post_init__`): integer tables,
`k_i ≥ 1`, keys `0 ≤ i < j < n`, no duplicate pair, shapes `k_i × k_j`.

### 2.3 Magnitude guard (`mincheck.py` lines 60–62, 79)

With `Δ = max_i |N(i)|` (0 if `n = 0`): reject if `max |U_i(a)|, |P_ij(a,b)| · 2^mb ≥ 2^50`, or
`|L| ≥ 2^62`, or `(Δ + 3)·2^50 ≥ 2^62`; reject a leaf with any message `|m| ≥ 2^50`. Under the
guard every fixed-width intermediate is below `2^62` (`ASSUMPTION_REGISTER.md` SB-A-03); sums
over sites and pairs are accumulated in arbitrary-precision integers. A re-implementation in
arbitrary precision needs no guard; it then accepts strictly more inputs than ours.

### 2.4 Node acceptance on the current box `D`

Missing messages are zero vectors.

- **leaf** — accept iff `L ≤ B`, where
  `B = Σ_i min_{a∈D_i} ( H_i(a) + Σ_{j∈N(i)} m_ij(a) ) + Σ_{(i,j)∈Π} min_{a∈D_i, b∈D_j} ( J_ij(a,b) − m_ij(a) − m_ji(b) )`.
- **branch** on site `i` — for every `a ∈ D_i` there must be a child for `a` (else reject);
  check that child on `D` with `D_i := {a}`. Children for states not in `D_i` are not checked.
- **prune** `(i, r, t)` — reject if `t = r` or `t ∉ D_i`; otherwise accept iff
  `H_i(r) − H_i(t) + Σ_{j∈N(i)} min_{s∈D_j} ( J_ij(r,s) − J_ij(t,s) ) ≥ 0`, and then check
  `rest` on `D` with `D_i := D_i ∖ {r}`. `r ∉ D_i` is allowed (the step is then a no-op), as in
  the kernel.

Domains stay non-empty at every visited node: the root is non-empty, a branch sets `D_i = {a}`,
and an accepted prune keeps `t ≠ r` in `D_i`.

### 2.5 Top-level acceptance (`check_min_certificate`)

Accept iff the certificate is well formed, the guard passes, and every visited node is
accepted (depth-first, stack-based; first failure rejects). Every exception, including a
recursion error, is a rejection; the function never raises.

### 2.6 What is reported

`accepted`, a reason, `lower_bound = L·u` (Fraction), node counts; if `w_i ∈ D⁰_i` for all `i`,
`witness_energy = E(w)` (exact) and `certified_gap = E(w) − L·u`. A witness outside the root box
is ignored. Acceptance does not depend on the witness.

The file loader (`mincert.loads`) additionally rejects an unknown `format`, a detached file
without an instance, an instance whose `model_sha256` differs from the recorded one, a `prunes`
node directly below a `prunes` node, and unknown node kinds. It expands each
`{"node": "prunes", "steps": [[i, r, t], …], "rest": …}` into nested prune nodes in list order.

### 2.7 Correspondence with the theory division's `verify` and reference checker

Lean (`proofs/CertificateAlgebra.lean`): `LeafOK` (line 127), `PruneOK` (141), `verify` (171),
`verify_sound` (308). Reference checker: `leaf_ok` (365), `prune_ok` (394), `verify_min` (414).

Our instance is the `PairInstance` with `k = max_i k_i`, `h_i(a) = U_i(a)·2^−s`,
`J_ij = P_ij·2^−s` for `(i, j) ∈ Π`, `J_ji = 0`, and zero on padded states (which lie in no
domain). Its energy, a sum over ordered pairs `i ≠ j`, equals `E`. All quantities below are
divided by `2^(s+mb)`, which preserves every inequality.

- **Leaf.** Lean stores `u`, `p`, `m` and requires `u_i ≤ h_i(a) + Σ_{j≠i} m_ij(a)` on `D_i`,
  `2p_ij ≤ J_ij(a,b) + J_ji(b,a) − m_ij(a) − m_ji(b)` on `D_i × D_j` for every ordered pair, and
  `L ≤ Σ u + Σ_{i≠j} p_ij`. We store only `m`. *If* our test passes, take
  `u_i = min_a(…)` and, for listed pairs, `p_ij = p_ji = ½ min_{a,b}(…)`, `p = 0` otherwise
  (unlisted pairs carry no message and zero tables, so `0 ≤ 0`); all three Lean conditions hold
  and `Σu + Σp = B ≥ L`. *Conversely*, any admissible `u_i` is at most our minimum, and because
  the pair expression is the same for `(i,j)` and `(j,i)`, `p_ij + p_ji` is at most our pair
  minimum; so `L ≤ Σu + Σp ≤ B`. Hence: some `u, p` satisfy `LeafOK` iff `L ≤ B`.
- **Prune.** Lean requires `t ∈ D_i`, `t ≠ r`, `ℓ_j ≤ link(i,r,t,j,s)` for all `j ≠ i`,
  `s ∈ D_j`, and `0 ≤ h_i(r) − h_i(t) + Σ_{j≠i} ℓ_j`. With one stored orientation,
  `link = J_ij(r,s) − J_ij(t,s)` (our `pair_rows` reads either orientation) and `link = 0` for
  non-neighbours. Some `ℓ` exists iff the margin with `ℓ_j = min_s link` is `≥ 0`, which is our
  test.
- **Branch.** Lean's children form a total function on `Fin k` and `verify` visits only
  `a ∈ D_i`; our partial map is completed by arbitrary children elsewhere. A missing child for
  some `a ∈ D_i` is a rejection in ours and in `verify_min`.
- **Sum.** Not implemented; a `sum` node is malformed for us.
- **Top level.** Lean `verify c I D L = true` implies `L ≤ E(x)` on `∏ D` (`verify_sound`, [V]).
  Our acceptance therefore implies the same proposition, *provided our implementation computes
  the test above* — tested, not verified. `to_metricchain_cert1` writes exactly the largest
  `u`, `p`, `ℓ` described here, so the reference checker judges the converted document as we
  judge the certificate. Observed: 288 mutated certificates; 275 converted and judged
  identically (49 accepted by both, 226 rejected by both); 13 malformed in our format (a state
  outside its site's own state set, expressible in the padded alphabet) and rejected by ours.

### 2.8 Discrepancies found while writing this specification

No discrepancy was found between the acceptance conditions of `mincheck.py`, the reference
checker's `min` semantics and Lean's `verify` on leaf, branch and prune. Found:

1. `mincert.py`'s docstring states the prune condition without `t ≠ r`; the code checks it.
2. `mincert.loads` is not strict: duplicate JSON keys are accepted (last wins), and values pass
   through `int()`, so a JSON float in `lower_bound`, a domain, a message, a prune step or an
   embedded table is truncated silently; the embedded instance's checksum is computed after
   truncation and then matches. The reference checker rejects duplicates and non-canonical
   numbers. This is not an unsound acceptance of the parsed object, but a file can have two
   readings.
3. Neither the checker nor `run.py` checks that the root box is the full state set; a
   certificate over a sub-box is accepted for that sub-box. The six stored certificates have full
   domains (checked 2026-11-26).
4. `verify_sound_real_symm` is in `proofs/Frontiers/SymmetricPairHypothesis.lean:129`, not in
   `CertificateAlgebra.lean` as some of our records say. For the [M] claim it is not needed:
   `verify_sound` applies to the instance with `J_ji = 0`. Its real-model hypothesis
   (instance ≤ real model on symmetrised sums) is not established for nearest rounding, so it is
   not a bridge to the float tables either.

**Coordinator's note, 2026-11-26 (after this section was drafted).**  Items 1–3 were fixed at
commit `263dd18`, each with a test that was watched failing first: the docstring states `t ≠ r`;
`mincert.loads` is strict (duplicate keys, floating-point literals, booleans, strings and wrong
shapes are `MalformedCertificate`; metadata travel as one opaque string and are never read by a
checker) — `test_loader_is_strict_so_that_a_file_has_one_reading`; `CheckResult.full_box` reports
whether the root box contains every state of every site, and the development driver refuses to
record a global-minimum row otherwise —
`test_check_result_says_whether_the_claim_covers_every_state_of_every_site`.  Item 4 is corrected
in our code comments and living documents and by the linked message STRUCTBIO-MSG-0003; published
messages are not rewritten.  The stored certificates were regenerated in the strict format (same
certified values; new file checksums in `results.jsonl`).

## 3. The certified results of SB-X-001 (founding directive §10)

- **Trusted inputs.** For each structure, the integer instance with the `model_sha256` of its row
  (rebuilt from the PDB file whose sha256 is in the row and in `MANIFEST.json`) and the detached
  certificate `experiments/structbio/gmec_dev/certs/<id>.mincert.json` with the row's
  `cert_sha256`.
- **Trusted code.** `src/metricchain_sb/mincheck.py` (140 lines, `wc -l`), `mincert.py` (374;
  used: `MinCertificate`, `validate_structure`, `loads` and its helpers, `model_sha256`),
  `model.py` (171) — 685 lines in total; `modelio.py` (44) when an instance is read from an
  archive (not used by `run.py`). Plus CPython 3.13.18 (`json`, `hashlib`, `fractions`) and
  numpy 2.5.5. Not trusted: `gmec.py`, the molecular layer, toulbar2, the converter.
- **Floating-point assumptions.** None in the checker. Floats are used in table construction
  (OpenMM, numpy), hydrogen placement (OpenMM minimiser), the input of `from_float`, the MPLP
  solver of the producer (messages are rounded to integers by `np.rint`; any rounding is sound),
  toulbar2, and the `*_float` fields of the row (display only).
- **Arithmetic guarantees.** Integer additions, subtractions, minima, comparisons; exact under
  the guard of §2.3.
- **Rounding assumptions.** The instance is defined as the nearest multiple of `2⁻²⁰` kcal/mol of
  each clipped float64 entry; nothing is certified about the unrounded numbers.
- **Discretisation assumptions.** The state set of `rotamers.py` plus the deposited state; no
  continuous claim.
- **Probability of failure.** None: deterministic.
- **Deterministic or probabilistic.** Deterministic (producer, checker, tables on one machine).
- **Exact proposition certified.** For the integer instance `I` with checksum `model_sha256`
  (`n` sites, tables in units of `2⁻²⁰` kcal/mol): for every `x ∈ ∏_i {0, …, k_i − 1}`,
  `E_I(x) ≥ L`, with `L` the row's `certified_lower_bound_kcal` (e.g. `−19124055/524288` for
  1CRN, `−93004435/1048576` for 1UBQ); and the witness `x*` has `E_I(x*) = L` (exact evaluation
  by the checker), so `x*` is a global minimiser of `I`. Labels [CK], [M].

## 4. Test inventory

Run on 2026-11-26: `/home/user/.venvs/structbio/bin/python -m pytest tests/structbio -q` →
**27 passed, 1 skipped in 30.4 s**. The skip is the whole of `test_baselines.py` (two
functions): `pytoulbar2` is not installed in this venv. With `-m "not slow"`: 26 passed, 1
skipped, 1 deselected (10.1 s). STRUCTBIO-REQ-0001 states "28 passed, 1 skipped (slow)"; that
was not reproduced here.

*Coordinator's note, 2026-11-26.*  The drafting agent ran a second virtual environment (`/home/user/.venvs/structbio`) that lacked `pytoulbar2`; the session's environment (`/root/.venvs/structbio`, created from `requirements-structbio.txt`) has it.  With every dependency installed the suite gives **33 passed, 1 skipped** (the skip is the slow ubiquitin table test) at commit `263dd18`, which also adds the tests of `test_stability.py` and three tests of `test_mincert.py`.  Both environments now hold the same packages.

`test_mincert.py`:
- `test_energy_is_sum_of_unary_and_pair_tables` — wrong energy assembly or pair orientation.
- `test_certificate_is_accepted_and_exact_on_small_instances` — producer/checker disagreeing with enumeration (24 instances).
- `test_certificate_with_tolerance_brackets_the_minimum` — a bound above the minimum, or a gap above `eps`.
- `test_reference_checker_accepts_the_converted_certificate` — conversion errors; semantic drift from the reference checker.
- `test_raising_the_claimed_bound_by_one_unit_is_rejected_by_both_checkers` — off-by-one leniency.
- `test_checkers_agree_on_mutated_certificates_and_never_accept_a_false_bound` — any disagreement or unsound acceptance on mutations.
- `test_checker_rejects_a_certificate_whose_tables_exceed_the_supported_range` — a missing magnitude guard (one case).
- `test_serialised_certificate_round_trips_and_is_judged_identically` — serialisation changing a verdict.
- `test_checksum_changes_when_one_table_entry_changes` — an insensitive checksum.
- `test_long_elimination_chains_serialise_convert_and_check_without_recursion` — defect 1 of §6 (recursion limit lowered to 250).
- `test_detached_certificate_needs_the_instance_with_the_recorded_checksum` — a detached file read against a wrong or missing instance; archive round trip.

`test_baselines.py` (skipped here):
- `test_toulbar2_minimum_equals_exhaustive_enumeration` — a wrong baseline encoding or offset.
- `test_contact_model_generator_is_deterministic_and_has_the_documented_structure` — a non-deterministic or misdescribed generator.

`test_molecular.py`:
- `test_chi_table_covers_twenty_residue_types` — missing or malformed chi definitions.
- `test_dihedral_known_values` — dihedral sign or convention errors.
- `test_chi_atoms_are_bonded_chains_and_measure_like_independent_formula` — wrong chi atoms or measurement.
- `test_library_is_symmetry_aware` — duplicate or symmetry-equivalent library values.
- `test_native_state_reproduces_input_coordinates` — preparation moving heavy atoms; state 0 not native.
- `test_rotation_preserves_bonds_angles_and_hits_targets` — non-rigid rotation; missed chi targets.
- `test_flexible_site_selection_crambin` — wrong site rule (CYX, PRO, GLY/ALA); wrong state counts.
- `test_rejects_missing_heavy_atom_and_nonstandard_residue` — preparation not failing closed.
- `test_pdbfixer_repair_only_behind_flag_and_recorded` — silent repair.
- `test_preparation_is_reproducible_and_replaces_input_hydrogens` — defect 3 of §6 (unseeded hydrogens).
- `test_table_api_and_clipping` — clipping or clip counts wrong.
- `test_save_load_roundtrip` — table file corruption.
- `test_max_states_per_site_keeps_native_and_lowest_self_energy` — wrong state truncation.
- `test_decomposition_matches_openmm_crambin` — tables not reproducing the independent OpenMM energy; bonded terms not constant.
- `test_reference_energy_is_deterministic` — non-deterministic reference evaluation.
- `test_decomposition_matches_openmm_ubiquitin` (slow) — as the crambin test, on 1UBQ.

## 5. Known gaps and what would close each

| gap | what would close it |
|---|---|
| the kernel's `sum` rule is not implemented | implement it in producer, format and checker, with conformance against `verify_min` |
| producer, formats and checker have one author | an independent checker from §2 (engineering, SB-BM-1) |
| few tests of robustness to hostile inputs; non-strict loader (§2.8 item 2) | a strict loader; adversarial cases of STRUCTBIO-REQ-0001 S3; ≥ 10⁴ mutations |
| full-box condition unchecked (§2.8 item 3) | check `domains` against all states in `run.py` and record it in the row |
| cross-machine reproducibility of instances untested | `run.py --check` on another machine (requested of engineering) |
| toulbar2 is 7–25× faster than our producer on every development structure | producer work; reported as is |
| no held-out result | SB-BM-3 with a list fixed and hashed by another division |
| no comparison with pseudo-Boolean proof logging | VeriPB/CakePB and exact SCIP/VIPR on the same instances (requested) |
| Lean kernel not executed on our certificates | a compiled or tabulated kernel evaluation, to be discussed with the theory division |
| `versions` and site `resseq` recorded as null (`ARCHITECTURE.md` §2.4) | read the existing `software` and `resnum` keys |

## 6. Defects found so far

1. Serialiser and converter recursed along prune chains and failed beyond 1 000 consecutive prune
   nodes — found on BPTI and ubiquitin; fixed by iterating along chains and the flat `prunes`
   node; regression test `test_long_elimination_chains_serialise_convert_and_check_without_recursion`.
2. The converter crashed (minimum of an empty set) below an invalid prune node — found by the
   differential mutation test; fixed (`_min0`).
3. OpenMM hydrogen placement was not reproducible until its random source was seeded (unary
   energies differed by up to ~70 kcal/mol between builds of 1CRN) — found by the molecular-layer
   engineer; fixed and tested.
4. The test suite masked defect 1: loading the reference checker raises Python's recursion limit
   globally (to 20 000); the regression test now lowers it explicitly.

## 7. What "formally verified" does and does not apply to

Formally verified, by the theory division in Lean 4 with Mathlib (labels [V], commit `b2caab6`):
the rule semantics — that `verify` accepting a certificate implies `L ≤ E(x)` on the box
(`verify_sound`) — and the theorems cited for C2. Not formally verified: our checker
`mincheck.py` and loader `mincert.py` (tested against enumeration and the reference checker
only), the converter, the producer, the table construction, the rounding of floats into the
instance, and the link between the instance and the force field or the protein. The Lean kernel
has not been executed on any of our certificates. No component of this division's software may
be described as formally verified.

## 8. Capability C2 (certified `ln Z` and populations) — verification state (coordinator, 2026-11-26, commit `b40f903`)

- **Exact proposition certified** (when `check_partition_certificate` accepts): for the integer
  instance with the recorded checksum, rational `β`, and root box `B`,
  `ln_z_lo ≤ ln Σ_{x∈B} exp(−β E(x)) ≤ ln_z_hi`; and, with a kept site `t`, for every state `a` of
  `t`, `population(a)` contains `Σ_{x∈B, x_t=a} exp(−βE(x)) / Σ_{x∈B} exp(−βE(x))`.
- **Deterministic**; no probability of failure.
- **Trusted inputs:** instance (checksum), `β`, root box.  **Trusted code:** `zcheck.py`,
  `zcert.py` (validation and parsing), `itables.py`, `expo.py`, `model.py`, CPython integers,
  and — for the float tier only — numpy's binary64 multiplication and addition.
- **Arithmetic and rounding:** steps in Python integers (exact); Boltzmann factors by
  `expo.exp_bounds_me` (integer arithmetic; lower values rounded down, upper values up after
  every squaring); elimination exact (tier `exact`) or outward-rounded binary64 (tier `float`,
  assumptions F1–F3 of `itables.py`: a product is moved one representable number outward; a
  sum of `m` terms is multiplied by `1 ∓ m·2⁻⁵²` and moved outward; values below `1e-300` are
  treated as 0 from below and `1e-300` from above); logarithms by `expo.log_bounds`, each bound
  certified through the exponential.
- **Rule semantics and their status:** `branch` — `WInstance.Z_branch` [V]; `prune` — the
  inequality inside `zprune_sound` [V], in energy form; elimination of a site with at most two
  neighbours — `Z_sumOut` [V]; with more neighbours, `relax`, and the rounded exponential —
  paper arguments of this division (STRUCTBIO-REQ-0003, R-1, R-3, R-4), unrefereed, with a Lean
  file in progress.  Hence label **[CP]**, not [CK].
- **Evidence for the implementation:** every interval contains the 60-digit enumerated `ln Z`
  and every enumerated population on all test instances, in both tiers, with and without
  relaxation, pruning and conditioning; the float tier's interval contains the exact tier's
  where both were run (crambin, coarsest threshold); a hand-written relaxation with arbitrary
  `f`, `g` cannot make the checker unsound (it recomputes the residual range).
- **Known gaps:** no independent implementation; assumptions F1–F3 are stated, not proved for
  this platform; the producer's heuristics are untuned; no baseline has been run; the adversarial
  review STRUCTBIO-REV-0001 covers this code and is recorded in `reviews/`.

## 9. Changes of 2026-11-27 (third checkpoint)

- **C2, rule semantics.**  §8 above was written when the general elimination, the relaxation
  and the rounded exponential rested on paper arguments.  They are now machine-checked in this
  division's `proofs/StructBio/FactorElimination.lean` (19 theorems; build "completed
  successfully (8567 jobs)"; our audit: only `propext`, `Classical.choice`, `Quot.sound`, 22
  declarations walked).  The label of C2 results changes from [CP] to **[CK]** — rule semantics
  [V], checker implementation tested — for the exact tier, and [CK] under F1–F3 for the float
  tier.  *Not* verified: the Python (its steps are instances of the theorems by reading; one
  author wrote producer and checker; no independent implementation exists yet —
  STRUCTBIO-REQ-0004 asks for one).
- **C1b extended** (`stability.py`): gaps for leaving a set of states (a rotamer well) and
  optimality in every table within an entrywise error `b`.  Each output is a `min` certificate
  on a restricted box or on the shifted table, checked by the same checker; exact proposition
  for the latter: if the certificate of the shifted model has minimum equal to the shifted
  energy of `x*`, then `x*` minimises every pairwise table whose entries lie within `b` of the
  model's (the science division's argument, SCI-REV-0026 §4; tested against the definition).
- **The model.**  v2 has no random element; its preparation is a function of the deposited
  heavy atoms (tested for two seeds bit for bit).  Trusted in addition for v2:
  `molecular/hydrogens.py` (geometry) — tested against a converged force-field minimisation of
  the hydrogens and by five planted wrong rules.
- **Provenance.**  Rows now record the commit of the code in memory at process start
  (SB-DEF-08).  Header times of messages are read from the clock (SB-DEF-09).
- **Internal adversarial review.**  STRUCTBIO-REV-0001 (a subagent with the mandate to break
  both checkers) — its findings and their handling are recorded in
  `docs/structural_biology/reviews/` and DEAD_ENDS when it reports.
