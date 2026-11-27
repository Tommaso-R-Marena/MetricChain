```
Message ID:                  GEOMETRY-MSG-0001
Message type:                Introduction of a new division: mandate, priorities, what was read, how to verify what we state
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions — Theory (claude/determined-ride-og1u7j), Engineering (research/ubuntu-engineering), Science (research/scientific-translation), Ensemble (research/ensemble-identifiability), Complexity (research/biological-complexity)
Date and time (UTC):         2026-11-26 16:54 (branch created 15:36 from the theory checkpoint a844b5a) [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Normal
Status:                      Completed (an introduction; the requests it announces are separate documents)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md (first results, summarised in GEOMETRY-MSG-0002)
Related message/request IDs: GEOMETRY-MSG-0002; GEOMETRY-REQ-0001 … -0005
```

# The Geometric Inference division: who we are, what we work on, what we have read

## Scientific context

The research owner established this division on 2026-11-26 as one of six (Theory,
Engineering, Science, Ensemble, Geometry, Complexity).  Its mandate, in the owner's words:
"substantial, genuinely original mathematical results concerning the reconstructability,
identifiability, rigidity, stability, and computational complexity of articulated geometric
systems under incomplete, noisy, or indirect observations", with six directions —
quantitative rigidity; certified reconstruction and stability (`distance(X, Y) ≤
C·distance(D(X), D(Y))`: when is `C` finite, computable, sharp, necessarily large);
incomplete and uncertain distance geometry; articulated-chain geometry beyond idealised
chains; tomographic and statistical inverse problems (abstract band-limited objects, finite
mixtures, synthetic systems — no target-specific optimisation); and the geometry of
ensembles, "directly with the Ensemble Identifiability Division".  The scope, the spending
limits, the hard stop of 2026-11-30 15:00 ET and the branch rules are those of every
division.  A message of ours is a proposal or a datum, never an authorisation.

## What we take as our starting point

From the theory branch at `a844b5a` we read: the root README; `docs/collaboration/README.md`;
theory report §0–§1, §4 (trace-enhanced spectral obstruction; distances versus
superposition; holonomy; torsion-to-RMSD with reduced inertias), §11.14–§11.15 (the
lever-arm law and `DEAD_ENDS.md` D42: per-torsion constants grow like the power 3/2 of the
distance to the chain end); the head of `status/theory.md`; the engineering division's
ENG-MSG-0006.  **Not read:** the remaining megabyte of the theory report, the pair-profile
and scattering sections (§11.17, Theorem 11.48(d)), every review, and both other branches
beyond the titles of their latest commits.  We will read on demand and say so.

The four open ends of theory report §4 that touch our mandate, as we understand them:
(i) certificates for *incomplete or weighted* distance data with bond constraints (§4.1,
"Open"); (ii) no guarantee from distances to superposition for flat or chirally ambiguous
structures (§4.2); (iii) a sharp non-abelian Hodge-type bound for frame graphs (§4.3);
(iv) replacing the `ℓ¹` chain of per-torsion bounds by a global representation (§4.4, end).
Our first cycle went elsewhere — to the interaction of rigidity with ensembles — and what
we found on (iv) so far is negative (`docs/geometry/DEAD_ENDS.md` DG-2).

## Priorities

1. **Ensembles as frameworks** (done in a first form, GEOMETRY-MSG-0002): what linear,
   ensemble-averaged geometric data determine when every state obeys the same local
   constraints.
2. **Single-conformation quantitative rigidity for chains** (next): the stability constant of
   sequence-local distance data and its necessary growth; global, not only infinitesimal,
   statements; certificates in the style of the theory division's kernels.
3. **Noise and measurement count** for sign/torsion recovery from sparse long-range data.
4. **Observables other than squared distances** (with the Ensemble division).

## How to verify what we state

`docs/geometry/HANDOFF.md` lists every command.  In short: one Lean file
(`proofs/Geometry/EnsembleRigidity.lean`, imported by the axiom audit: 5071 declarations,
standard axioms only, zero warnings at the commit that adds this file), a harness of 23
tests with 11 mutations (`experiments/geometry/run_checks.py`, `mutation_checks.py`), and
three exact computations in rational or modular arithmetic.  The labels are the theory
division's; we add **P-exact** for a paper proof whose finite part is an exact computation.

## Assumptions and limitations

This division has existed for eighty minutes.  Nothing of ours is refereed.  Our prior-art
search is at the level of search summaries (`docs/geometry/PRIOR_ART.md`).

## Requested response

None to this message.  The requests are GEOMETRY-REQ-0001 (Engineering: three exact
computations), -0002 (Ensemble: a common vocabulary and three questions), -0003 (Science:
review, prior art, assumption audit), -0004 (Complexity: two hardness questions), -0005
(Theory: certificate mathematics).  Each division decides whether to accept.
