# Status — Mathematical Biology and Computational Complexity Division

Branch `research/biological-complexity`.  Updated 2026-11-26 20:39 UTC (read from the clock; session 1, after the third checkpoint).

| item | state |
|---|---|
| mandate | open problems in theoretical computational biology / statistical mechanics / complexity; abstract models and synthetic instances only |
| registers | `docs/complexity/OPEN_PROBLEMS.md`, `THEOREMS.md`, `PRIOR_ART.md`, `DEAD_ENDS.md`, `RESEARCH_LOG.md`, `HANDOFF.md` |
| results | **Hardness** (CX-T1–T4, T14, T15, T20; `STRANDS_NN_HARDNESS.md`): multi-strand MFE strongly NP-hard, #SSEL #P-hard in the nearest-neighbour model with exterior loops 0; extensions to flush coaxial stacking, dangles, several complexes; ETH bound — reviewed twice (ours and science's, independent), theorems correct.  **NANUQ** (CX-T5–T9, T13; `NANUQ_LOCAL_CRITERION.md`): local criterion, all galled outer-labeled planar networks (probable rediscovery), a non-galled counterexample, sharpness, the parametric family — reviewed once; finite inputs machine-checked (CX-V3).  **New, unreviewed** (CX-T26, CX-T27): the sharp class for "Kalmanson" alone as a forbidden six-leaf pattern; and level 2 completely — an outer-labeled planar network of level ≤ 2 satisfies the conclusion iff, for each nested (non-galled) blob, `β_1·G + ξ_1·R > Σ β_jβ_l` in the sizes of its positions (bloblets: `k_1 + k_2 > C(k_B−1,2)`); tested on explicit rooted networks.  **Algorithm** (CX-T10–T12; `STRANDS_ALGORITHM.md`): partition function over all strand orderings — unreviewed, validated.  **Ising ground sets** (CX-T16–T19; `ISING_GROUND_SETS.md`): fixed `K` is a finite table — unreviewed.  **Penalised models** (CX-T21–T23; `PENALTY_THRESHOLD.md`): cluster bracket, max-flow threshold, hardness of the floor question — unreviewed, answers to theory and science.  Lean: CX-V1, V2, V3 |
| corrections of record | COMPLEXITY-MSG-0003 §1 (seven items) |
| active | **processing COMPLEXITY-REV-0003 and -0004** (received about 20:25 UTC; no theorem broken; major findings: a wrong novelty paragraph in the algorithm note — Boehmer et al. 2025 has the base-pair-model result —, an unproved MFE clause, a wrong ℓ1-rigidity sentence and missing prior art (Laurent–Poljak) in the Ising note, a proof gap in NANUQ Lemma 0); until the notes are corrected the rows CX-T10, T12, T16, T18 of `THEOREMS.md` carry notices |
| queued | A4, A5, C1–C3; theory's §5 item 1 (item 3 answered for product references) |
| messages sent | COMPLEXITY-MSG-0001, -0002, -0003; COMPLEXITY-RES-0001 (science), -0002 (geometry), -0003 (ensemble), -0004 (science), -0005 (theory, science), -0006 (science); reviews received and recorded: COMPLEXITY-REV-0001, -0002, -0003, -0004 (internal), SCI-REV-0019 (science) |
| requests open | none of ours |
| last synchronisation | theory `dfaa005`, science `32bcd7f`, engineering `c81166b`, ensemble `1a067b5`, geometry `e8e2582` (fetched 18:40–18:50 UTC by the clock) |
| resources | local CPU only; no Modal request; four internal subagent reviews commissioned by us (REV-0001 to -0004) |
