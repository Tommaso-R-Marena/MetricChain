# Architecture of the STRUCTBIO research software

Branch `research/structural-biology`; package `src/metricchain_sb/` (version string `0.1.0`).
Written 2026-11-26 from the code as committed at `aec72df` (software of every result:
`c128625`; the checker, format and model files are unchanged since). Line numbers refer to that
code. Uncommitted work in progress seen at the time of writing — a `domains` argument of
`certify_gmec` (certificates over a sub-box) and a new `stability.py` (C1b) — is not described. Companion documents:
`ASSUMPTION_REGISTER.md`, `PHYSICAL_APPLICABILITY.md`, `VERIFICATION_REPORT.md` (labels [CK],
[CP], [M], [H] are defined in §1 of the last).

## 1. The six layers of the founding directive §9

| layer | modules | role | trusted? |
|---|---|---|---|
| scientific model definitions | `molecular/prepare.py`, `chi.py`, `rotamers.py`, `tables.py` (definition in its docstring, lines 3–47); `model.py` (`PairModel`) | the physical model (structure, sites, states, energy) and the published integer instance | the instance is the object of every claim ([M]); its link to the energy function is [N] |
| computational methods | `molecular/tables.py` (table construction), `molecular/reference.py` (independent OpenMM check), `synthetic.py` (generators) | numerical work in float64 | no |
| certificate producers | `gmec.py` (`certify_gmec`) | dead-end elimination, MPLP dual, ICM, branch and bound | no |
| certificate checkers | `mincheck.py` (`check_min_certificate`), with `mincert.validate_structure`, `mincert.loads`, `model.py`, `modelio.load_model` | exact integer acceptance test | yes (small, tested, not formally verified) |
| benchmark orchestration | `experiments/structbio/gmec_dev/run.py`; `baselines/toulbar2.py` | build, solve, certify, check, record | no |
| result interpretation | `results.jsonl` rows; `PHYSICAL_APPLICABILITY.md`; STRUCTBIO-MSG-0001 | what a number means | documentation |

`mincheck.py` imports `mincert` (data class, `validate_structure`, `MalformedCertificate`) and
numpy, and nothing from `gmec.py`. `mincert.to_metricchain_cert1` is not on the acceptance path:
it exists to hand our certificates to the theory division's reference checker.

### 1.1 Trust boundary

```
 UNTRUSTED                               |  TRUSTED (exact integers)     |  EXTERNAL ORACLES
                                         |                               |  (cross-checks, untrusted)
 PDB file --> prepare.py --> tables.py   |                               |
  (sha256)    OpenMM, float64  float64   |                               |  OpenMM reference System
                      |        tables ---+--- [N] comparison ------------+->  (reference.py)
                      v                  |                               |
          PairModel.from_float(2**-20)   |                               |
                      |                  |                               |
                      v                  |                               |
          published instance  ===========+==> model.py / modelio.py      |
          (integer tables, sha256)       |        |                      |
                      |                  |        v                      |
                      v                  |   mincheck.py  --> accept/    |  toulbar2 (same integer
          gmec.py (float MPLP, DEE, B&B) |   (validate_structure,         |   instance; optimum
                      |                  |    magnitude guard,            |   only, no proof)
                      v                  |    leaf/branch/prune)  reject  |
          certificate (structbio-        |                               |  reference_checker.py
          mincert/1, integers) ==========+==>                            |  (metricchain-cert/1,
                      |                  |                               |   via to_metricchain_cert1)
                      +------------------+-------------------------------+->
```

Data crossing the boundary into the checker: the integer tables and `scale_bits` (embedded in
the certificate or from an `.npz` archive whose `model_sha256` must equal the one recorded),
`message_bits`, the root domains, the claimed `lower_bound` (integer), an optional witness, and
the tree of nodes. Data crossing back out: accept/reject, a reason string, the lower bound and,
if the witness lies in the root box, its exact energy and the certified gap (Fractions), and
node counts. Floating-point numbers never cross into the checker.

## 2. Data formats actually implemented

### 2.1 Instance archive (`modelio.py`)

`save_model` writes one `np.savez_compressed` archive with arrays: `scale_bits` (int64
scalar), `meta_json` (JSON string, `sort_keys=True`), `n` (int64), `pairs` (int64, shape
`P × 2`, sorted `(i, j)` with `i < j`), `u{i}` (int64 vector of length `k_i`), `p{i}_{j}`
(int64 matrix `k_i × k_j`). Object arrays (entries `≥ 2**62`) are refused (line 21).
`load_model` uses `allow_pickle=False` and rebuilds a `PairModel`, which re-validates shapes,
keys and integer type. Identity of an instance is `mincert.model_sha256`: SHA-256 of
`json.dumps({"scale_bits", "unary", "pair"}, sort_keys=True, separators=(",", ":"))` —
metadata excluded (`mincert.py` lines 332–336).

### 2.2 `structbio-mincert/1` (`mincert.dumps` / `loads`)

Top-level JSON object:

| field | content | units |
|---|---|---|
| `format` | `"structbio-mincert/1"` | — |
| `model` | optional (absent in a *detached* file): `scale_bits`, `unary` (list of integer lists), `pair` (`{"i,j": k_i × k_j integer lists}`, `i < j`), `meta` | table integers in `2**-scale_bits` energy units (kcal/mol for the molecular layer) |
| `model_sha256` | checksum of the instance (always present; `loads` refuses a mismatch) | — |
| `message_bits` | natural number `mb` | — |
| `domains` | `n` lists of states (root box) | state indices |
| `claim.lower_bound` | integer `L` | `2**-(scale_bits + mb)` |
| `claim.witness` | list of `n` states, or `null` | — |
| `certificate` | root node | — |
| `meta` | producer record: `producer`, `eps`, `bnb_nodes`, `seconds`, `message_bits`, `max_sweeps` | — |

Nodes: `{"node": "leaf", "m": {"i,j": [int × k_i]}}` — messages for ordered listed pairs, one
integer per state of site `i`, in `2**-(scale_bits + mb)`; omitted keys are zero vectors.
`{"node": "branch", "site": i, "children": {"a": node}}`. `{"node": "prunes", "steps":
[[site, remove, dominator], ...], "rest": node}` — a flat list for a chain of eliminations
(written by `_node_to_json`, lines 294–307); its `rest` must be a leaf or branch
(`_node_from_json` rejects a `prunes` directly below a `prunes`, line 324). In memory each step
is a separate `prune` node (`site`, `remove`, `dominator`, `rest`).

### 2.3 Exact conversion to `metricchain-cert/1` (`to_metricchain_cert1`, lines 179–269)

After `validate_structure`: alphabet `k = max_i k_i`; `h[i][a] = unary[i][a] / 2**scale_bits`
(padded states 0); `J["i,j"]` for every stored `i < j`, padded `k × k`, no `J["j,i"]` (the
reference checker's default 0); `lower_bound = L / 2**(scale_bits+mb)`; same domains and
witness. Each prune gets `ell[j] = min_{s∈D_j} (J_ij(r,s) − J_ij(t,s))` for every neighbour
`j`, on the domains current at that node. Each leaf gets `u_i = min_{a∈D_i} (h_i(a) + Σ_j
m_ij(a))`, `p_ij = p_ji = ½ min_{a∈D_i, b∈D_j} (J_ij(a,b) − m_ij(a) − m_ji(b))` and its messages
padded. These are the largest values the reference inequalities admit, so acceptance coincides
(argument: `VERIFICATION_REPORT.md` §2.7). Rationals are canonical (`_rat`). Chains of prunes are
followed iteratively; recursion happens only through branch nodes. An empty domain can arise only
below an invalid prune; the converter then writes 0 (`_min0`) and both checkers have already
rejected above it.

### 2.4 Result row of `run.py` (one JSON object per line of `results.jsonl`)

`experiment`, `split`, `pdb_id`, `commit` (`git rev-parse HEAD`, `+dirty` if `src` is
modified), `model_sha256`, `pdb_sha256`, `sites`, `states_min`, `states_max`, `states_total`,
`pairs`, `certificate_accepted`, `certified_lower_bound_kcal` (exact rational string),
`witness_energy_kcal`, `certified_gap_kcal`, `certified_lower_bound_float`,
`toulbar2_energy_kcal`, `agrees_with_toulbar2` (toulbar2's value equals the witness energy),
`native_state_energy_float` (all-zero configuration), `witness_sites_differing_from_native`
(state index ≠ 0), `seconds_build_tables`, `seconds_toulbar2`, `seconds_produce_certificate`,
`seconds_check_certificate`, `toulbar2_nodes`, `bnb_nodes`, `cert_leaves`, `cert_branches`,
`cert_prunes`, `cert_message_integers`, `cert_bytes`, `cert_sha256`, `platform`, `versions`.

Two recording defects (no effect on any certified value, since metadata is outside the
checksum): `versions` reads `tables.meta["versions"]`, a key that does not exist (the builder
writes `software`), so it is `null` in all six rows; the instance metadata copies site key
`resseq`, which does not exist (the builder writes `resnum`), so it is `None` for every site.

## 3. Capability C1 — certified GMEC of a pairwise integer-table model (implemented)

1. **Scientific purpose.** Remove search error from the statement "configuration `x*` has the
   lowest energy among all configurations of this discrete rotamer model", with a proof that a
   small independent program checks.
2. **Mathematical specification.** Instance: `n` sites, states `0..k_i−1`, integer tables
   `U_i`, `P_ij` (`i < j`), scale `s`; `E(x) = 2**-s (Σ_i U_i(x_i) + Σ_{(i,j)} P_ij(x_i,x_j))`.
   Output: `L`, `x*` and a certificate such that acceptance implies `L ≤ E(x)` for all `x` in
   the root box (`verify_sound`, [V]); with root box = all states and `E(x*) = L` the minimum is
   exact.
3. **Explicit assumptions.** `ASSUMPTION_REGISTER.md` (SB-A-01 … SB-A-24).
4. **Trusted-input specification.** The integer instance identified by `model_sha256` (from the
   `.npz` archive or embedded); a certificate file in `structbio-mincert/1`. Nothing produced by
   `gmec.py` is trusted. For a GMEC reading, the root domains must be the full state sets; neither
   the checker nor `run.py` checks this (the six stored certificates do have full domains,
   checked by hand on 2026-11-26).
5. **Documented output.** `CheckResult(accepted, reason, lower_bound, witness_energy,
   certified_gap, stats)`; the row of §2.4.
6. **Failure conditions (abstain or reject), from the code.**
   - Producer abstains: `CertificationBudgetExceeded` after `max_nodes` (default 100 000)
     branch-and-bound nodes or `time_limit` seconds (3 600 in `run.py`); `ValueError` when
     `max|entry| · 2**message_bits ≥ 2**50` or `eps < 0`.
   - Model layer refuses: `StructureRejected` (non-standard residue in ATOM or SEQRES, SEQRES
     length ≠ observed residues, C–N distance > 2.0 Å, missing or unexpected heavy atom,
     heavy atom moved by hydrogen placement, not exactly one chain of the given id, MANIFEST
     checksum mismatch); `ValueError` for an unexpected force set, a non-`NoCutoff`
     NonbondedForce, a chi bond on a ring, a torsion or exception coupling two sites' moving
     atoms, non-finite tables in `from_float`; `TypeError` for non-integer tables in
     `PairModel`; `ValueError` for an empty state set, a pair key not `0 ≤ i < j < n`, a
     duplicate pair, a wrong table shape.
   - Loader refuses (`MalformedCertificate`): unknown format; detached file without instance;
     checksum mismatch; `prunes` below `prunes`; unknown node kind.
   - Checker rejects: any `validate_structure` failure; the magnitude guard; a message with
     `|v| ≥ 2**50`; a leaf bound below `L`; a branch without a child for a current state; a
     prune with `t = r`, `t ∉ D_i` or negative margin; any exception or recursion error.
   - `run.py --check` fails a structure when the rebuilt instance checksum, the certificate file
     checksum, acceptance or the recorded lower bound differ.
7. **Reproducibility procedure.**
   `~/.venvs/structbio/bin/python -m pytest tests/structbio -q`;
   `~/.venvs/structbio/bin/python experiments/structbio/gmec_dev/run.py --check` (rebuilds the
   six instances, compares checksums, re-checks stored certificates); `run.py <PDB id>`
   regenerates everything and needs `pytoulbar2`. Dependencies: `requirements-structbio.txt`.
   Bit-for-bit reproduction has been observed on one machine only.
8. **Tests.** `tests/structbio/test_mincert.py` (11), `test_molecular.py` (16, one marked
   slow), `test_baselines.py` (2); inventory and counts in `VERIFICATION_REPORT.md` §4.
9. **Benchmark criteria.** SB-BM-1 (conformance: zero disagreements and zero unsound
   acceptances over ≥ 10⁴ mutated certificates), SB-BM-2 (synthetic scaling, H2a–H2c),
   SB-BM-3 (held-out structures, H3a–H3e), SB-BM-4 (table–energy link) in
   `BENCHMARK_MASTER_PLAN.md`. Only development evidence exists.
10. **Provenance.** PDB files with sha256 in `benchmarks/structbio/pdb/MANIFEST.json` and in each
    row; instance `model_sha256`; certificate `cert_sha256`; software commit `c128625`; theory
    kernel and reference checker at `b2caab6`; platform string. Library versions are recorded in
    the table metadata (`software`) but not in the rows (§2.4).

## 4. Planned, not implemented

### 4.1 C1b — certified flip gaps (implemented at commit `263dd18`: `src/metricchain_sb/stability.py`, `tests/structbio/test_stability.py`; the robustness radius is still planned)

For each site `i`, the flip gap `G_i = min{E(x) : x_i ≠ x*_i} − E(x*)` (minimum energy over
configurations in which residue `i` leaves its GMEC state, minus the GMEC energy), certified
from below; and the gap to the second-best configuration, which equals `min_i G_i`. One
realisation that reuses the C1 producer and checker unchanged is one `min` certificate per site
on the box with `D_i` = all states except `x*_i` (confirmed; this is what `stability.certify_flip_gaps` does). Purpose:
per-residue stability of the certified conformation, and robustness of the conclusion to
rounding and to bounded model error; the exact robustness statement is to be fixed against the
theory division's `robust_certified_iff`.

### 4.2 C2 — certified enclosures of `Z`, free energy, populations (planned, under construction)

A certificate is a list of exact energy-level steps followed by an exact elimination:
- thermal dead-end eliminations, each multiplying the upper bound by `1 + exp(−β·margin)`;
- product-form relaxations of weak pairs: `J = f(a) + g(b) + R(a,b)` with `r_lo ≤ R ≤ r_hi` on
  the box; `f, g` move into the one-body terms; the bound is multiplied by
  `[exp(−β r_hi), exp(−β r_lo)]`;
- Boltzmann weights enclosed by the certified exponential with outward rounding (theory
  `exp_enclosure`, `Z_encloses_partitionFn`);
- exact variable elimination on factor tables along a stated order, optionally conditioned on a
  few sites.

Two arithmetic tiers: exact rationals (small instances, ground truth) and float64 with outward
rounding after every multiplication and an a-priori error factor for every sum (rigorous under
the IEEE-754 round-to-nearest model for `+` and `×`). The software abstains when a table would
exceed a memory budget. Known obstruction (exploratory): on ubiquitin first-order relaxation
plus exact elimination certifies nothing useful — best order found has width 10 and a largest
table of about `10¹³` entries for pairs above 1 kcal/mol non-additive oscillation; the weaker
pairs carry about 113 nats of worst-case first-order uncertainty.

C3 (ensemble partial identification) and C4 (geometric observability) are later priorities;
C5 (residual-class certificates on real energy terms) is blocked: no certified constant exists
for any real energy term.

## 5. Dependencies and non-goals

Checker: CPython (3.13.18 used) and numpy (2.5.5). Molecular layer: OpenMM 8.6.1 (Reference
platform), optional pdbfixer 1.12.0. Baseline: pytoulbar2 1.4.0.3 (not installed in the
session venv at the time of writing; its two tests are skipped). Tests: pytest. Lean 4 /
Mathlib only to build the theory division's proofs; nothing of ours is written in Lean.

Non-goals: no services, endpoints, databases or deployment; no network access by the code; no
sequence design or mutation (the sequence is fixed); no claim about proteins. The kernel's
`sum` rule and the `split` layer are not implemented.
