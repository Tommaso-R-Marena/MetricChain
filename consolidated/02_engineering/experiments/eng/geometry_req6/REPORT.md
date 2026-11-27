# GEOMETRY-REQ-0006 — a certified global maximum on the 4-torus and a certified 4D realisation (experiment X-019)

**Status of this report (Computational Research Division, 2026-11-27, written during the consolidation ordered by the
research owner).**  The work below was done by a subagent of this division from the text of GEOMETRY-REQ-0006; the
report under the line is its own, unedited except for one sentence about a scratch file.  **What the coordinator
checked:** the test file passes here (31 tests, 25 s); the three drivers were re-run and regenerate the stored records
identically apart from timings; the seven controls behave as stated.  **What the coordinator did not do:** read the
trusted core (956 lines: `gr6_model.py`, `gr6_kernel.py`, `gr6_qa_proof.py`, `gr6_qb_proof.py`) line by line, check
the pen-and-paper lemmas in its docstrings, or compare the model with the geometry division's own code.  Until
someone does, the statements are "certified by interval arithmetic in code reviewed by its author and by mutation
testing only" — a strong computation, not a refereed one.  The limits the subagent names in §6 stand, in particular:
the model identity with the requesters' convention is tested, not proved, at the bond angle of 111°; the couplings are
the request's rounded to six decimals.

---

# GEOMETRY-REQ-0006 — report of the certified computation (engineering subagent)

Decision: **accept; instance A is certified** (couplings rounded to six decimals, as the request allows). Both (Q-a) and (Q-b) are established by interval arithmetic. Nothing was committed; git was only read. All files are new and untracked, under `experiments/eng/geometry_req6/` and `tests/eng/test_geometry_req6.py`.

After the wind-down message I did only this: added one assertion block (18 lines) to the test file to close the gap exposed by a surviving mutant, ran the second half of the already-defined mutant list (10 runs), corrected three stale module names in docstrings, and re-ran the test file. No new search, proof attempt or subagent.

## 1. (Q-a) — what is rigorously established

**Statement certified.** With F = {(0,4),(0,5),(1,4),(1,6),(2,6)} and the exact rational couplings
c = (−317197, 185025, 307367, −150204, 115451)/10⁶,
H_c attains its maximum over T⁴ exactly at ±θ̂; every other θ is strictly below.

- θ̂ = (1.517383726589587796334153113297027340…, −1.046295577075061494192620663387382627…, 2.711958333973797896674444040453536009…, −1.674413477850529377051279150300093922…); each coordinate is enclosed to 10⁻³⁶ in the record.
- max H_c = 1.170178163968538342622515453407965250…(251).
- Hessian eigenvalues at θ̂ (enclosed): −1.09821, −0.31893, −0.25555, −0.020448.
- θ̂ and −θ̂ are certified distinct mod 2π.

**Two independent certificates of the same statement** (they share the local step and the loop, and differ in the bounding function):

| | Certificate D (direct, on T⁴, the structure the request proposed) | Certificate R (reduced to (θ₁,θ₂)) |
|---|---|---|
| Boxes examined | 20,298 | 686 |
| Excluded leaves | 18,980 | 490 |
| Unresolved at level 12 | 116 (58 near each of ±θ̂) | 18 (9 near each) |
| Exact tiling check | [−π,π]⁴ passed | [−π,π]² passed |
| Largest Hessian eigenvalue on B | ≤ −0.013893 | ≤ −0.013872 |
| Run time | 7.8–9.3 s | 0.16–0.19 s |

In D, B₊ = [1.51404,1.52017]×[−1.05078,−1.04157]×[2.70901,2.71515]×[−1.67817,−1.67051] and B₋ is its mirror. The "examined" count of D includes about 200 boxes re-examined when the loop resumes at levels 8 and 10.

**Which inequality establishes what.**
1. **Threshold.** L = lower end of the ball H(θ̃) at a dyadic point θ̃, so L ≤ max H.
2. **Exclusion.** H (and each Hessian entry) is multi-affine in the points (cos θ_k, sin θ_k). Each arc lies in a triangle (two end points and the tangent apex), so the supremum over a box is at most the maximum over the 81 vertex tuples. A box is excluded when that maximum is < L. For R, Cauchy–Schwarz gives H ≤ G(θ₁,θ₂) = A + |V| + |W|, valid because no monomial contains both θ₀ and θ₃ (checked on the support); G is separately convex, so 9 vertex pairs suffice.
3. **Local step.** On B the interval Hessian (vertex ranges, then Gershgorin after a similarity with an enclosed inverse) is negative definite, so H is strictly concave there. Krawczyk on a box of radius 2⁻⁸⁰ inside B gives a critical point, which is therefore unique in B and its strict maximiser. For R, additionally V, W ≠ 0 on B′ with their polar angles inside B₀, B₃.
4. **Mirror.** H is even: the forms have no monomial with an odd number of sines, by construction of the support. −θ̂₊ is certified to lie in B₋, so θ̂₋ = −θ̂₊.

**Kind of argument and assumptions.**
- Every inequality is a comparison of Arb balls or of their exact end points (python-flint 0.9.0, 192 bits), or exact `Fraction` arithmetic (grid, tiling, containment).
- Assumed: correctness of Arb/FLINT and of the python-flint wrappers. The tests check rounding directions of `lower`/`upper`, comparison semantics and the sin/cos enclosures against mpmath.
- Assumed: the pen-and-paper lemmas in the docstrings (vertex maximum, Cauchy–Schwarz, Krawczyk, Gershgorin).
- Floating point only proposes inputs (Newton starts, approximate eigenvectors, grouping of boxes); it concludes no inequality.
- The function certified is the transfer-matrix formula in `gr6_model.py`. Its equality with the requesters' NeRF convention is a derivation in the docstring, tested exactly in rational arithmetic (8 rational bond angles × 12 rational torsion points × 21 pairs) and to 50 digits at 111° on the 3⁴ interpolation grid. It is **not** machine-proved symbolically at 111°.

**"Second local maximum" (request's control), certified in this sense only:** H(θ) ≤ 1.154989405716968218293732063123715300…(301) for every θ whose (θ₁,θ₂) is not interior to the region N, with equality exactly at ±θ₂.
- θ₂ = (1.126613757241212…, −2.794492205891317…, −1.918843488000507…, 0.108426174220095…), a strict local maximiser (Hessian eigenvalues −0.689, −0.437, −0.285, −0.0578).
- N is 2,422 level-8 boxes of the (θ₁,θ₂)-plane, 3.70 % of its area: two neighbourhoods of ±(θ̂₁,θ̂₂), listed in the record.
- Certified margin: 0.015188758251570124….
- **Not** established: that the cylinders over N contain no local maximum other than ±θ̂.

## 2. (Q-b) — what is rigorously established

**Statement certified.** There is a configuration of 7 points in ℝ⁴ whose squared lengths on all 16 pairs of F ∪ E₀ equal those of X(θ) for every θ in the enclosure of θ̂, hence for X(θ̂) itself.
- Gauge: y₀ = 0, y₁ = (∗,0,0,0), y₂ = (∗,∗,0,0), y₃ = (∗,∗,∗,0); pins y₄[3] = 9/20 and y₅[3] = 3/4, exact.
- Coordinates enclosed to 7.7·10⁻⁴⁰.
- Singular values of the centred configuration: [0.2382559043018201, 0.2382559043018235], 0.83475795844492…, 1.60992800602802…, 2.88383706494395…; so σ₄ ≥ 0.23825590430182019 > 0 and the affine dimension is 4.
- On the five unconstrained pairs the squared distances differ from the chain's by certified amounts, e.g. −0.17446217… on (0,3).
- A second member of the family, proposed by the search (pins y₅[3] = −19/25, y₆[2] = 129/50), is certified too, with σ₄ ≥ 0.24527.

**Kind of argument.** Krawczyk in Arb on the 16 length equations in 16 unknowns, with the targets as interval parameters; then a Gershgorin enclosure of the 4×4 Gram matrix. Same assumptions as above.

## 3. Numerical evidence only (not part of any proof)
- With the unrounded couplings, H(θ*) = 1.1701814262 and the runner-up is 1.1549945; these match the request's 1.170181 and 1.154995.
- Stress at X(θ̂) in floats: the rigidity matrix has a one-dimensional left kernel; stress-matrix eigenvalues −1.6068, −0.8407, +0.1133 (indefinite); the rounded c is proportional to the stress on F to 2·10⁻¹⁶. Neither the uniqueness nor the signature is certified in intervals. The theorem does not need them, since (Q-b) gives non-universal rigidity directly.
- A 60⁴ floating-point grid shows no value above the certified maximum, and every point above the runner-up lies over N.
- The largest σ₄ on the two-parameter family is about 0.278; the length system is nearly singular there, so that member was not used.
- That the semidefinite controls admit no 4D realisation rests on float eigenvalues plus the universal-rigidity theorem. The code only shows that it does not certify one.

## 4. Controls (`results/controls.json`, all as expected)

| Control | Expected | Outcome |
|---|---|---|
| A1: runner-up claimed global | not certified | Not certified; 2,422 unresolved boxes away from the claim; a point with H ≥ 1.155141873 is exhibited |
| A2: couplings −c | not certified | Not certified; all 4,096 level-6 boxes unresolved |
| A3: (Q-a) on the semidefinite control | certified | Certified, 330 boxes, max 0.352978875717… |
| B1: (Q-b) on the same control | not certified | Search: 0 of 60 starts converge; Krawczyk fails at the flat realisation and with pins 9/20, 3/4 (least-squares residual 0.0094) |
| B2: instance A pinned flat | not certified | Krawczyk fails (singular Jacobian) |
| B3: six atoms, F = {03,14,25,05}, semidefinite | not certified | Search reaches only flat configurations (σ₄ ≈ 7·10⁻⁷) |
| B4: same graph, indefinite | certified | Certified, σ₄ ≥ 0.33 |

The semidefinite control is the same graph at θ ≈ (2.4644, −1.7802, 0.1149, −2.2217), with float stress eigenvalues 0.513, 0.560, 1.701.

On the reading of the request: for a semidefinite stress (Q-a) is true (universal rigidity plus the conic condition), so A3 certifying is the correct outcome. Only (Q-b) must fail there, and it does.

## 5. Discrepancies with the request's numbers
- Rounding c moves the maximiser by at most 3.8·10⁻⁵ per coordinate from θ*, the maximum by −3.3·10⁻⁶ and the runner-up by −5.1·10⁻⁶.
- The request's Hessian eigenvalues (−0.342, …, −0.0064) are ours (−1.098, …, −0.02045) divided by twice the largest stress eigenvalue; the two are consistent.
- The request's singular values (2.89, 1.61, 0.85, 0.15) belong to another member of the family.
- Cost: seconds, not hours. A float pilot on coarse levels predicted about 1,600–2,600 boxes per level (21,952 down to level 13).

## 6. Not done or not finished
- **No `--shard i --of N` or resumable driver.** It was unnecessary at about 10 s; to resume, wrap `gr6_qa_proof.branch_and_bound` over subsets of `root_boxes(3, 4)`.
- **Result files not regenerated after the last small edits** (rational bond-angle option in `gr6_model.Chain`, a `start` parameter in `gr6_controls.control_a1`, three docstring lines). The tests recompute with the final code and agree with the stored records.
- **D's 18,980 excluded boxes are not stored**, only counts and the tiling check. R's 490 are stored and re-verified box by box by a test.
- No symbolic proof of the model identity at 111° (see §1).
- No interval certificate of the stress signature, nor of the absence of other local maxima over N.
- No independent re-implementation in a second interval library; instance B and the fallback generator were not examined.
- Only my own test file was run, not the whole engineering suite. No response document was written.

## 7. Mutation results
- 18 hand-written mutants of the trusted code, applied one at a time to a scratch copy: **17 killed, 1 survived.**
- **Survivor #14** (transfer matrix A transposed, i.e. S → −S) is an equivalent mutant: conjugation by diag(1,−1,1) turns it into θ → −θ, and the forms are even, so the function is unchanged.
- **History of #8** (`H_upper` skipping the apex of the last arc): it survived the first run, because in the 30 random boxes of the comparison test the maximising vertex was never that apex. I added a 150-box comparison against the maximum over all 81 vertex tuples, with every apex exercised; on re-run it is killed.
- Mutants 0–7 were run against the test file before that addition, and 8–17 against the final file. The addition only adds assertions.
- Killed: hull apex on the circle; range max→min; Gershgorin radius dropped; Krawczyk always accepting; sin/cos swapped; G without |W|; a child box dropped; V1/V2 swapped; direction arc four times too small; coverage not required; definiteness tested on the wrong end; threshold raised; derivative sign; Jacobian of the length system; σ₄ > 0 not required; tiling volume unchecked.
- Not covered: rounding-direction slips (`lower` vs `upper`) change results at the 10⁻⁵⁷ level and cannot be detected numerically; they rest on code review. The list is ad hoc, not exhaustive.
- The mutation script was a scratch file outside the repository and is not kept; the list of mutants is the one above.

## 8. Commands and run times (from the repository root, venv active)
```
cd experiments/eng/geometry_req6
python run_qa.py            # ~15 s: R 0.2 s, D 8-9 s, float multistart 4.5 s, second maximum 0.7 s
python run_qb.py            # ~0.6 s
python run_qb.py --search   # ~1.5 s
python run_controls.py      # ~10 s
cd ../../.. && ulimit -v 3000000 && python -m pytest tests/eng/test_geometry_req6.py -q
```
- The test run: 31 passed in 25 s (19–47 s observed under varying machine load), peak RSS 231 MB.
- The drivers set RLIMIT_AS = 3·10⁹ themselves. The test file does not, so run it under `ulimit -v`.
- No absolute paths, user names or e-mail addresses in any file (grep checked).

## 9. Trusted and untrusted code
- **Trusted** (956 lines including proof docstrings): `gr6_model.py` (definition of H), `gr6_kernel.py` (points, hulls, ranges, Gershgorin, Krawczyk), `gr6_qa_proof.py` (all but the grouping heuristic `clusters`, whose output is re-checked exactly), `gr6_qb_proof.py`, and `dec_down`/`dec_up` in `gr6_common.py`.
- **Untrusted**: `gr6_search.py`, `gr6_records.py`, `gr6_controls.py` and the three `run_*.py` drivers.

Files are in `experiments/eng/geometry_req6/`:
- gr6_model.py
- gr6_kernel.py
- gr6_qa_proof.py
- gr6_qb_proof.py
- gr6_common.py
- gr6_search.py
- gr6_records.py
- gr6_controls.py
- run_qa.py
- run_qb.py
- run_controls.py
- results/qa_instance_A.json
- results/qb_instance_A.json
- results/qb_instance_A_search.json
- results/controls.json

The test file is `tests/eng/test_geometry_req6.py`.
