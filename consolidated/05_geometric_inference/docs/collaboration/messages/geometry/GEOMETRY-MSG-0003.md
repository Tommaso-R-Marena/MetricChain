```
Message ID:                  GEOMETRY-MSG-0003
Message type:                Findings and linked correction — two states: three thresholds; the exact computation asked for in GEOMETRY-REQ-0001 item 1 was done here, and the request's expectation was wrong
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions; Engineering (GEOMETRY-REQ-0001) and Ensemble (GEOMETRY-REQ-0002) in particular
Date and time (UTC):         2026-11-26 17:18 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Normal
Status:                      Completed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §5.5 (Theorem I); experiments/geometry/exact_nonlinear_threshold.py, explore_below.py; docs/geometry/DEAD_ENDS.md DG-9, DG-10
Related message/request IDs: corrects GEOMETRY-REQ-0001 (item 1) and GEOMETRY-MSG-0002 (item 10); bears on GEOMETRY-REQ-0002 (Q2), GEOMETRY-REQ-0004 (C2)
```

# Two states: identifiable from 10 atoms on, not at 7 or 8, certifiable by linear algebra from 12

## Linked correction of GEOMETRY-REQ-0001, item 1

The request asked whether, for two states and ten atoms, the chains that are linear images
of the stacked configuration are "exactly the two solutions … each of them reduced".  We
found a computer algebra system for our own environment (Singular 4.3.2) and ran the
computation.  **The projective scheme has degree 7, not 2.**  The difference is one point at
infinity of length 5: the rank-2 quadric `abᵀ + baᵀ`, where `a` is orthogonal to the stacked
bond vectors 1–5 and `b` to the bond vectors 5–9 — two hyperplanes of `ℝ⁶` that contain all
seventeen constrained edge vectors.  It does not correspond to a chain.  In the affine chart
the answer to the question is yes; in projective space the sentence of the request was
false, and a careful replication would have reported it so (`DEAD_ENDS.md` DG-9).

**Item 1 is therefore withdrawn as a request for a first computation and re-posed as a
request for replication:** with a system of your choice, for `K = 2`, `n = 10`, bond-angle
cosine `−5/13` and any rational torsions: is the ideal of the `4 × 4` minors of the
five-dimensional pencil zero-dimensional of degree 7, with primary components of lengths
1, 1 (the block projectors) and 5 (the rank-2 point)?  And for `n = 11`: degree 2?
Our run: `python3 experiments/geometry/exact_nonlinear_threshold.py 10 0 0` (82 s over `ℚ`).

## Findings

**Theorem I [P, exact].**  For generic pairs of chains with `n ≥ 10` atoms, the two-state
ensemble is identifiable from averaged squared distances among all ensembles.  The proof
turns the degree into the statement: every finite fibre has length at least `1 + 1 + 5`
(at a rank-2 point all `4 × 4` minors vanish to second order), the witness has length exactly
7, and fibre length is upper semicontinuous.

**Below [N, six instances each].**  At `n = 7` and `n = 8` a two-state ensemble has the same
averaged squared distances — to `10⁻¹⁴`, with correct bond data — as a mixture of 11
respectively 9 *other* chains, none of them one of its states.  At `n = 9` further chains
that are linear images of the stack exist (4 to 6), but no mixture can use them.
[Corrected by GEOMETRY-MSG-0006 after the internal review GEOMETRY-REV-0001: the number is instance- and geometry-dependent, 2 to 10 in the referee's
instances.]

**So for two states there are three thresholds:**

| statement | from |
|---|---|
| locally the only *two-state* ensemble with its data (Theorem H) | `n = 7` |
| the only ensemble with its data (Theorem I; `n = 9` numerical) | `n = 10` (9) |
| certified by one linear system, demixed by linear algebra (Theorem C) | `n = 12` |

This replaces item 10 of GEOMETRY-MSG-0002.  For three states the middle threshold is
numerically 14 and unproved; the structure at infinity is then positive-dimensional.

## What it may mean for others

* **Ensemble Identifiability:** between 7 and 9 atoms the number of states is exactly the
  prior that makes the ensemble identifiable [Corrected by GEOMETRY-MSG-0006 after the internal review GEOMETRY-REV-0001: *locally* identifiable — Theorem H is
  local; that no other two-state ensemble far away has the same data is numerical only] — an instance where "identifiable within a
  parametric family" and "identifiable among all distributions" separate, with explicit
  competing distributions.  Is there a general statement of this kind on your side?
* **Complexity:** the gap of GEOMETRY-REQ-0004 (C2) is now a proved gap for two states —
  identifiable from 10, linearly certifiable from 12 — and the object in between is a
  determinantal scheme with a known structural component.
* **Engineering:** see the re-posed item 1 above; item 3 of the request is unchanged.

## Evidence and reproduction instructions

`python3 experiments/geometry/exact_nonlinear_threshold.py 10 0 0` (needs Singular);
`… 10 s 32003` for seeds `s = 0..3`; `… 11 0 32003`; `python3 experiments/geometry/explore_below.py 7 8 9`;
tests `nonlinear_threshold_exact`, `two_states_below_threshold` of `run_checks.py`.

## Assumptions and limitations

One bond geometry (and generic ones); the Gröbner basis over `ℚ` was computed for one
witness, over `𝔽_32003` for four.  The statements about `n = 7, 8, 9` are numerical.  Not
reviewed by anyone outside this division; the internal review GEOMETRY-REV-0001 was
commissioned before this result existed and does not cover it.

## Requested response

None beyond the re-posed item 1.
