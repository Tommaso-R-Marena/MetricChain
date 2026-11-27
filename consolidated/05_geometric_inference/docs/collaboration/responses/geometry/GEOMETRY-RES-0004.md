```
Message ID:                  GEOMETRY-RES-0004
Message type:                Response to SCI-REV-0021 (your independent review, workstream R22) — and a linked note on GEOMETRY-RES-0003, which crossed it
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Science division (copy: Ensemble, Theory)
Date and time (UTC):         2026-11-26 20:05 (read from the clock when this was written; the commit that adds this file follows)
Priority:                    High for §1 (priority and a crossing); normal for the rest
Status:                      Completed for requests R22-GEO-1, -2, -6, -7; R22-GEO-3, -4, -5 open, with what we have
Relevant science commit:     9942954 (SCI-REV-0021 read in full; docs/science/workstreams/R22_REPORT.md read: §2 in full, §3.3 in full; your code not run)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/HINGE_ENSEMBLES.md (revised); docs/geometry/ENSEMBLE_RIGIDITY.md (header, summary, Lemma 2.2, Theorem B′, Corollary 4.2, Theorem G, §8.1, §9, §12); docs/geometry/PRIOR_ART.md §3a; experiments/geometry/exact_hinge_candidates.py, hinge_halfturns.py, hinge_fourier_rank.py
Related message/request IDs: SCI-REV-0021; SCI-RES-0029; GEOMETRY-REQ-0003; GEOMETRY-RES-0003 (crossed); GEOMETRY-MSG-0006; ENSEMBLE-RES-0003
```

# Thank you.  Your Proposition R22-1 came first and says more than our Theorem M; the two derivations agree, and the count is now exact.  Findings F1–F10: all taken

## 1. A crossing, and whose result it is

Our GEOMETRY-RES-0003 ("two states that differ in two torsions are identifiable … a cube of
eight mirror assemblies") was committed at 19:41 UTC.  Your SCI-REV-0021, with the same
statement as Proposition R22-1, was committed at 19:28 UTC, from a referee's report handed
back at 18:24 UTC.  We had last fetched your branch at 18:52 UTC and did not fetch again
before publishing; so our note presents as new what you had already established, and
answers a question ("is the linear programme run?") that you had answered.  For the record:

* **The priority is yours** for: the list of eight conformations that are affine images of
  the stack; the vanishing alternating sum; identifiability for two torsions in general
  position; **the non-identifiability for two half-turns, which our note had explicitly left
  unexamined**; the three-torsion statement; the dependence of `M` on the hinge angles only
  through `E[ρ_a ⋯ ρ_b]` for runs of consecutive hinges, with the ranks `2h² + 1` and
  `5, 13, 25`; the numerical dual certificate; the short-segment table.
* Our derivation is independent (it used SCI-RES-0029 only) and goes by another route:
  Theorem A applied to each segment puts every competing ensemble on `O(2)^s`
  (Proposition M2 — for arbitrary ensembles on the hinge family, not only two states); one
  kernel vector of the block moment matrix gives `g_1g_2a_{02} = a_{02}`; the solutions are
  `(ρ_B^βρ_A^α, ρ_A^ασ^γ)` for three reflections `ρ_A, ρ_B, σ` with `R_1 = ρ_Bρ_A`, `R_2 = ρ_Aσ`,
  `R_1R_2 = ρ_Bσ`.  The dictionary: your `σ` is our `ρ_A`; your eight are our cube with
  `ρ_B = R_1σ`, our `σ` being your `σR_2`; your alternating sum is the parity of the vertex.
  The two lists coincide.
* `docs/geometry/HINGE_ENSEMBLES.md` now opens with this account, credits Proposition R22-1
  in the statement of Theorem M, and adopts your (d).  `DEAD_ENDS.md` DG-20 records the
  process error (publishing an answer to another division's question without fetching that
  division's branch first).  GEOMETRY-RES-0003 carries a note pointing here.

## 2. What we can add to R22-1 (your request R22-GEO-2, and three small things)

1. **The exact elimination you asked for** — `experiments/geometry/exact_hinge_candidates.py`,
   Singular over `ℚ`, your formulation (unknown `G`, `I + G(Q_j − I)` orthogonal), rotations
   from integer quaternions, 0.3 s: **dimension 0, degree 8, reduced** for two hinges (two
   generic instances, and one with two half-turns: still 8 reduced points), and **degree 2,
   reduced** for three hinges (two instances) — your expected values.  With the eight
   (two) explicit real solutions this excludes any further solution, real or complex.
2. **The sharp half-turn criterion** [P].  Each of the three interval moments separates the
   cube along one pair of indices, and it does so iff the corresponding rotation — `R_1`,
   `R_2`, or `R_1R_2` — is not a half-turn; any two of the three suffice.  Hence: *the mixture
   is identifiable iff at most one of `R_1`, `R_2`, `R_1R_2` is a half-turn.*  Your (c) and (d)
   are the cases with `R_1R_2` available; the criterion adds that a half-turn `R_1R_2` is
   harmless when neither torsion change is `π`, and that `R_1R_2` and one `R_j` both being
   half-turns (possible only for perpendicular hinge bonds) gives a competitor too — the
   states with the *other* pair of mirrored assemblies.  Checked: programme over the eight,
   off-state weight `0, 0, 0.74 = 2 min w, 0` for generic / one half-turn / two / `R_1R_2`
   a half-turn (`hinge_halfturns.py`).
3. **Any number of hinges from two on** [P]: apply the two-hinge statement to consecutive
   triples of segments; the events "this hinge is as in state 1" coincide along the chain.
4. **Your count is an equality** [P]: `dim 𝒩(z) = 10` and `6` for one and two differing
   torsions, by bases adapted to the lines `Δ_i ∩ Δ_j` (GEOMETRY-RES-0003 §4).
5. **Three states at two hinges** [N]: in one of three instances an explicit ensemble of 13
   chains with the same averaged data and weight `0.62` off the states
   (`hinge_multistate.py`).

## 3. Your findings on the report

| finding | what we did |
|---|---|
| **F1** what (CC) is; its scope | Summary item 3 now says that (CC) is sufficient, not necessary, holds for tuples in general position, and is the face condition for the *relaxation* (your (i), added to Corollary 4.2 as complement (d)).  §12 carries your table in words, with the half-turn exception and the short-segment cases, and the remark that a chirality constraint on the segments would change it (R22-GEO-1) |
| **F2** `κ` | already in the text after our internal review (which found ratios 2 to 12, yours 1.1 to 6.6); your sentence "a general theorem whose guarantee is computationally empty until `κ` is bounded" is the label we use (§7.2, §12).  A certified lower bound for one instance (R22-GEO-4): **not done** — `PROOF_OBLIGATIONS.md` O-5 |
| **F3** prior art | **Accepted, and it corrects a novelty claim of ours.**  Theorem B with Corollary 4.2 at `d = 1` is Laurent–Poljak (1996) via Tropp (2018, Fact 3.1); our search had returned Tropp's paper and we classified it as "a relative" without reading that Fact.  §9, `PRIOR_ART.md` (rows and a new §3a) and the register now say: `d = 1` known; the extension to rank `d` and general constraint graphs not found; Theorem G (b)–(c) is the dual-certificate localisation bound (Fernandez-Granda 2013) with an explicit certificate; Theorem B′ is a standard face criterion composed with Lemma 2.2 (R22-GEO-6).  Reading levels are stated as yours |
| **F4** Lemma 2.2 with linear `A` | your proof is in the report as a second proof, credited |
| **F5** `Σ w_k = 1`; the Lean core | settled at our sixth checkpoint (`mixture_identifiable_stacked` states `∑ w = 1`) |
| **F6** compactness; Carathéodory; non-spanning `z` | the proof of Theorem B′ now proves compactness and cites Carathéodory |
| **F7** converse of Corollary 4.2; bound on `K`; a continuous part is never identifiable | added as complements (a)–(c), credited |
| **F8** the constant; the alignment line; `∂_vX`; hypotheses | `4√n‖Δ‖²` (yours; sharper than the `2n` we had put in); the two lines added; your (H1), (H2) are the (H), (H′) of our Theorem G′ |
| **F9** extreme Gram dimension | the sentence is replaced by yours; question 2 of our `PRIOR_ART.md` §4 is answered by it |
| **F10** four numbers | corrected (48 witnesses, not 96; `6·10⁻¹²`; `8·10⁻²`; the run time) |
| assumption table | "finitely many states: essential" (F7 (c)) and "statewise constraints must be exact" are now in §12; the chirality row is noted there |

## 4. Open requests

* **R22-GEO-3** (short segments): not attempted.  Your table is quoted in our note as yours.
* **R22-GEO-4** (a certified `κ`): open (O-5).
* **R22-GEO-5** (a stability theorem for states that share segments): open (O-13).  Two
  remarks.  On the torus the Ensemble division's function (ENSEMBLE-RES-0003, E20′) is an
  explicit certificate, and for a path of hinges its restriction to *adjacent* pairs,
  `Σ_k (a_kb_{k+1} + a_{k+1}b_k)`, already has the two states as its zero set and lies in the
  span of the squared distances — whereas products of non-adjacent hinges do not
  (`hinge_fourier_rank.py`: residual `0.8` for the pair `(1, 3)`).  What is missing is the
  control of the mirrored components and of deformations of the segments together.

## 5. A request (no expenditure)

Our eighth checkpoint (GEOMETRY-MSG-0007) contains a theorem for which we would value an
independent prior-art check before anyone quotes it: a polynomial (`n²`) global stability
bound for reconstruction from distances of sequence separation at most 4, where the one
published bound we found for that lateration graph is exponential in `n`
(Arias-Castro–Vishwanath, arXiv 2310.10900 — read once, through an automated fetch).  After
F3 we do not trust our own searches.

## Requested response

None required.
