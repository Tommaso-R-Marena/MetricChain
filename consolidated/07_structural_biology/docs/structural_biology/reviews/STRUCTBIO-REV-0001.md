# STRUCTBIO-REV-0001 — Adversarial review of the certificate checkers

| | |
|---|---|
| Id | STRUCTBIO-REV-0001 |
| Date | 2026-11-26 (concluded 2026-11-27 UTC) |
| Reviewed commit | `627a860e03aff0e0a8b1993550992c0f0cc2944c` (`git rev-parse HEAD` at the end; `src/` and `tests/` as in `7722963`, on which every test was run). The branch moved during the review (started at `29760422`); `mincheck`, `mincert`, `zcheck`, `zcert`, `itables`, `expo`, `model` are byte-identical from `b40f903` to this commit. |
| Scope | `src/metricchain_sb`: `mincheck`, `mincert` (format, loader, converter), `zcheck`, `zcert` (format, loader), `itables`, `expo`, `model`, `stability`; producers only where they touch a checker. |
| Mandate | Adversarial: break the checkers, do not confirm them. Internal AI review, **not** peer review. |

> **Disposition (added by the coordinator on 2026-11-27; the review below is unchanged).**  All 19 findings were
> addressed in commit `0e934eb`; finding 14 is the one whose test changed its contract.  What changed, the
> documented limits, the evidence and what stayed open: `docs/structural_biology/VERIFICATION_REPORT.md` §10 and
> `docs/structural_biology/HANDOFF.md` ("Unfinished work", item 1).  The repaired code has not been reviewed
> again by an independent reviewer.

Severity: **S1** a false statement accepted; **S2** exception or hang; **S3** one file two readings, silent truncation, strictness, claim weaker than it appears; **S4** documentation. Reproducers are in `tests/structbio/test_adversarial_*.py` (M = `…_mincheck.py`, F = `…_mincert_files.py`, Z = `…_zcheck.py`, E = `…_expo_model_stability.py`); tests for findings are left **failing**.

## Verdict

With certificates made of Python integers (everything a loader returns), an unmodified instance and default options, **no unsound acceptance was found** in either checker (campaigns below). Four unsound acceptances (and one false derived verdict) exist outside that envelope, and the Z checker can be stalled by a 300-byte file.

## Findings

### S1 — unsound acceptance (all conditional)

1. **NumPy `message_bits` bypasses the range guard of `mincheck`.** `validate_structure` admits `np.integer`; `2 ** np.int64(20)` is fixed-width, so the guard and the table scaling wrap. One-state model with energy −2⁴⁴: bound 0 accepted, `certified_gap` reported negative. In-memory only. `M::test_numpy_message_bits_must_not_bypass_the_magnitude_guard`
2. **NumPy integers in relax vectors wrap in `zcheck`.** `table - f - g` and `H += f` are computed in the width of `f`. With `np.int32` and entries of 1.5·10⁹ the accepted interval is [2.795, 2.795], ln Z = −1.5. In-memory only (the producer emits Python ints). `Z::test_numpy_integers_in_relax_vectors_must_not_wrap`
3. **Float tier is unsound for `exp_bits` ≈ 872–1001** (default 64 is safe; demonstrated at 980, 990). `FloatTables._ldexp_up` returns 1e-300 when the exponent is below −2000, valid only for mantissas below 2¹⁰⁰³. Accepted [−687.60, −687.31] for ln Z = −685.99; the population of the dominant state (0.80) is certified ≤ 0.25. `Z::test_float_tier_stays_sound_when_exp_bits_is_large`
4. **Both checkers trust a stale neighbour cache.** `PairModel` is mutable; after `model.pair[(0,1)] = t` the checkers read tables from `model.pair` and neighbours from `_neighbors`. Min: bound 1000 accepted, minimum 0. Z: [−50, −49] accepted, ln Z ≈ 2·10⁻²². Nothing in the repository mutates a model; a file round trip is safe. `M::…stale_neighbour_cache_of_the_instance`, `Z::test_z_checker_must_not_trust_a_stale_neighbour_cache_of_the_instance`
5. **`stability.shifted_model` wraps in int64** (new code, outside the original scope, seen briefly; entries and error bounds near 2⁶³; NumPy warns). An entry 2⁶³−1 raised by 2⁶³−1 becomes −2 and `certify_necessary_optimality` reports `holds = True`, with an accepted certificate, for an `x*` of energy 2⁶³−1 against 5. `E::test_shifted_model_does_not_wrap_at_the_edge_of_int64`

### S2 — exception or hang

6. **`zcheck` exponentiates step factors as exact rationals** (every node multiplies by `exp_bounds(a_lo)`, `exp_bounds(a_hi)`). A prune with margin m < 0 builds a rational of 1.44·e^(β|m|) bits: β|m| = 19 → 7.7 s, 189 MB; 21 → > 1.1 GB; 40 → 4·10¹⁶ bytes. A relax with `f = 10⁹` (β = 1) → > 20 s, 1.5 GB. A prune with a *large positive* margin (a clash, the safest prune) is quadratic: β·m = 10⁵ → 11 s, 3·10⁵ → > 30 s. A table entry 2⁶⁰⁰⁰⁰, `scale_bits = 10⁸`, or the exact tier at β = 10⁷ do not return within 20 s. Both tiers; reachable from `structbio-zcert/1` files. `Z::test_work_of_the_z_checker_is_not_exponential_in_the_numbers_of_a_step`, `Z::test_z_checker_returns_within_seconds_on_tiny_certificates`
7. **Exponent bombs in `mincheck`.** `2**message_bits` and `2**scale_bits` are computed before any range check: `message_bits = 10⁹` costs 4.9 s and 467 MB before the rejection (a 341-byte file suffices); with `scale_bits = 3·10⁸` the certificate is *accepted* after 3.4 s and 180 MB. `M::test_exponent_fields_of_a_small_file_do_not_make_the_checker_compute_astronomical_powers`
8. **Object graphs that are not trees hang `validate_structure`** (self-reference; 40 levels of shared children = 2⁴⁰ paths), both checkers, in-memory only. `M::test_checker_terminates_on_a_certificate_whose_tree_is_not_a_tree`, `Z::…[node that contains itself-exact]`
9. **Loaders raise other exceptions than `Malformed…`:** RecursionError for ≥ 1000 nested nodes or nested metadata text; ValueError for keys or numerals that pass `str.isdigit` but not `int` (`²`, `--3`) and for numerals beyond the interpreter's 4300-digit limit. `F::test_loader_reports_deep_nesting_as_a_malformed_certificate`, `F::test_loader_reports_non_ascii_digits_in_keys_as_a_malformed_certificate`, `Z::test_z_loader_reports_every_malformed_file_as_malformed_zcertificate`
10. **`to_metricchain_cert1` and `dumps` raise RecursionError on accepted certificates** (branches nested deeper than the recursion limit; the docstring bounds the nesting by the number of sites, true for the producer only). `M::test_converter_and_serialiser_work_on_every_certificate_that_the_checker_accepts`

### S3 — ambiguity, strictness, weaker claims

11. **`mincert.loads(text, model=X)` silently returns a certificate about the embedded instance.** A verifier holding X is told "accepted" about other tables. `F::test_loader_does_not_silently_replace_the_supplied_instance_by_an_embedded_one`
12. **The verdict on an honest Z certificate depends on options the file does not bind.** The producer stores its own interval as the claim; made exact / checked float: 12 of 12 rejected; `exp_bits` 48 or 96 instead of 64: about half rejected. `Z::test_a_certificate_made_in_one_tier_is_accepted_by_the_other_tier_and_by_other_precisions`
13. **Unknown fields are ignored** (min format: everywhere; Z format: inside nodes and steps; a Z node with both `branch` and `order` is read as a branch), and a `prunes` node may be followed by a `prunes` node with no steps. `F::test_loader_rejects_fields_and_encodings_outside_the_format`, `Z::test_z_loader_rejects_fields_outside_the_format`
14. **Equivalence with the reference checker stops at about 10⁴ consecutive prune nodes:** ours accepts, `json.dumps` cannot write the converted document and the reference checker answers "nested too deeply" (development certificates: 344–1280). `F::test_converted_document_can_be_judged_by_the_reference_checker_whenever_ours_accepts`
15. **A witness given as a dict yields the energy of no configuration** (0, gap 0; minimum 10). `M::test_witness_given_as_a_mapping_must_not_yield_the_energy_of_no_configuration`
16. **`PairModel` truncates silently** (7/2 → 3, 1.9 → 1 in object arrays; pair key `"01"` → (0, 1)). `E::test_pair_model_refuses_what_it_would_have_to_truncate`
17. **Negative state indices are read as "last state"** by `energy_int`, `certify_flip_gaps` (gap computed on the full box) and `shifted_model`. `E::test_negative_state_indices_are_refused`
18. **Flip gaps are not checked against their box.** Neither `stability` nor the driver compares the box of the returned certificate with `{x_i ≠ x*_i}`; with a producer that drops one state every existing check passes and the gap is 10 instead of 1. `second_best_gap` cannot detect an incomplete site list. The same applies to `certify_necessary_optimality` (shifted model not re-derived by a checker). `E::test_a_flip_gap_is_backed_by_a_certificate_on_the_flip_box` (failing), `E::test_second_best_gap_of_an_incomplete_list_of_sites_is_silently_too_large` (characterisation, passing)

### S4 — documentation

19. `expo`: "relative width about 2**-bits for bits <= 80" holds only for |q| ≲ 2¹⁴; measured 2⁻⁷⁴·⁵ at |q| = 10⁶, 2⁻⁴⁵ at 2⁶⁰, vacuous beyond 2¹⁰⁵, and "more bits only cost time" is contradicted by finding 3. `E::test_exp_bounds_width_is_two_to_minus_bits_as_documented`. Also contradicted by the findings above: `mincheck` "never wrapped" (1), `zcheck` "Steps: Python integers (exact)" (2) and "never raises … overflow is a rejection" (6), converter nesting bound (10).

## Attacks that failed

* **Min checker:** 60,000 random hand-built trees (random messages; valid, almost valid, repeated and out-of-domain prunes; dominators already removed; missing and extra children; sub-boxes): 25,819 acceptances, 6,807 tight; zero disagreements between the checker, an independent reading of the semantics, the reference checker on the converted document, and enumeration. Int64 edge: degree 4092 with entries and messages of 2⁵⁰−1 exact; one unit beyond rejected. 51 malformed in-memory objects rejected without exception.
* **Min files:** 168 mutations (types at every position, non-canonical keys, duplicate keys, non-integer literals, wrong or missing checksum, foreign instance for a detached file) all `MalformedCertificate`.
* **Z checker:** 40,000 random certificates × 2 tiers (entries to 2⁷⁰, β from 0 to weight spreads of e^±3000, prune/relax/branch trees, relax and prune on the kept site), truth by interval arithmetic at 160–2,560 digits: 31,889 (exact) and 29,683 (float) accepted results, all containing ln Z and every population; no invalid certificate accepted. The 339 results first tallied as "TOUCH" are not anomalies: the instance has equal weights (e.g. β = 0), the truth is rational and the bound equals it. With those compared exactly, a second campaign (25,097 certificates; 20,015 and 18,644 accepted) left nothing undecided and no miss. 38 invalid in-memory certificates × 2 tiers and 38 file mutations rejected.
* **`expo`:** 6,012 exp and 600 log enclosures (|q| ≤ 10⁶, 300-digit rationals, precisions 0–300 bits): no miss.
* **Float primitives:** 2,400 column sums (to 65,536 addends, adversarial), F2 as stated, 20,000 products, 9,066 conversions: no violation.

## Not examined; residual risks

The molecular layer, baselines, the Lean proofs and the reference checker itself; instances larger than 5 sites × 4 states (soundness evidence is by enumeration only); F1–F3 on other platforms or NumPy builds; time-of-check/time-of-use with exotic container subclasses; the producers' own int64 arithmetic; the new `stability` functions beyond findings 5, 17–18.

## Recommended fixes

1. Checkers: convert every certificate integer with `int()` (or admit `int` only) before arithmetic; derive neighbours from `model.pair`; freeze `PairModel`; Python integers in `stability._moved`.
2. `_ldexp_up`: test the value, not the exponent (or cap `exp_bits`).
3. `zcheck`: return `log_bounds(z) + a` at leaves and combine children in log space; bound `message_bits`, `scale_bits`, |β·entry| and reject negative-margin prunes beyond a threshold before computing.
4. Loaders: catch RecursionError and ValueError at the top; ASCII-only digit test; reject unknown fields; refuse `model=` together with an embedded instance.
5. Bind tier and `exp_bits` into the Z claim, or store a claim rounded outward.
6. Add a checker for flip-gap claims that recomputes the box.
