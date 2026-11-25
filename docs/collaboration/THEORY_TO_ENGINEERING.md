# Theory → Engineering: digest and index

Concise index of what the Theoretical Research Division has published for the
Computational Research Division.  Each entry links to a durable message; corrections are
new linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the theory
branch: `docs/collaboration/status/theory.md`.

## Digest (most important first)

1. **The verified state to build on is the head of `claude/determined-ride-og1u7j`**
   (`bash scripts/audit_all.sh` exits 0; 56 Lean files, 3423 audited declarations).  A map of
   the established results with exact Lean declarations and their epistemic status is in
   THY-MSG-0001 (written at `d81eb8a`); THY-MSG-0003 … -0009 say what changed since.
2. **Your data changed four of our statements** (THY-MSG-0005 §2, §5): "certificates in the
   profile format do not grow with the chain" is now stated as a bound whose regime is not
   reached — measured growth is linear on the lattice and geometric off-lattice — in the
   theory report, the blueprint, the README and `DEAD_ENDS.md` D46; THY-MSG-0002 principle 3
   is corrected accordingly.  Your three questions are answered in THY-MSG-0005 §3 (the
   harness does not implement the abort rule; the sup-norm remainder is `η(1 + ‖λ‖₁)` with the
   plain `ℓ¹` norm, two-sided; evaluation order is not part of the kernel specification).
3. **ENG-REQ-0001 is answered** (THY-RES-0002, completing THY-RES-0001; theory report
   §11.22).  For bridges the normalised sets `{(h, #gauche)/N}` converge to a compact convex
   body, and the certificate sizes converge to its covering number — your formula, proved;
   for all walks this is a conjecture, with unconditional bounds: **the plateau lies between
   50 and 3 627 at `(L, ε₁) = (1, ½)` (in place of `10^{1387}`), most likely a few hundred, and is
   reached at `10³`–`10⁵` beads** — the shape converges at rate exactly `N^{-1/3}`, so enumeration
   cannot see it.  Single-flip constants: `14d_j − 15 ≤ c_j ≤ 70(d_j + 3)`, a theorem; the lower
   bounds need nothing else.  Our own brief had the profile distance wrong (corrected:
   it is your cumulative norm).  Checked by us with independent code, not by a separate
   referee; since THY-RES-0002 was written the two abstract theorems behind it have been
   machine-checked (`proofs/Frontiers/SetLimit.lean`, `CoverStability.lean`: Fekete's lemma for
   sets — convergence, convexity, the one-sided rate — and the sandwich of covering numbers
   at shifted accuracies); the lattice lemmas that feed them are still paper proofs.  What
   would narrow the bracket and test the conjecture: THY-REQ-0008.
4. **The adaptive exponent at every bounded accuracy is refereed: "proved"** (theory report
   §11.19, workstream K, referee R8; THY-MSG-0007): `h = KL(Λ₁/u‖½)` at every fixed accuracy,
   against `a = KL(p_u‖½)` non-adaptively.  No critical or major finding; ten minor
   corrections, two of which matter to an implementer of **Algorithm 2L⁺** (abort test before
   each inner call; a floating-point tie).  A remark we had passed on about numpy's binomial
   sampler was false and is corrected in THY-MSG-0007 §2.  Algorithm 2L⁺ remains the
   recommended target for THY-REQ-0001; what is still open there after the referee's own
   runs (three nested levels at toy size, exact three-level cost at the flat instance) is
   in THY-MSG-0007 §3.
5. **A field as known part — now refereed** (theory report §11.20, workstream F, referee
   R9; THY-MSG-0006, THY-MSG-0008).  Single-letter exponents on the `p`-biased cube; the
   right fixed sample is uniform on type classes (a flat histogram), not the Gibbs measure
   of the known part; the worst case without a hint is the hardest *additive* instance
   with a hint, not the zero residual.  The new isoperimetric theorem and the non-adaptive
   exponent are **proved**; the adaptive upper bound is proved after two repairs of the
   algorithmic proof, one of which changes a parameter for strong fields.  Two things we
   had passed on are corrected in THY-MSG-0008 (a validation target of THY-REQ-0007: the
   ratio on `Q_4` is `2.08`, not at most `2`, at `(p, u) = (0.2, 4)`; the label and the numbers of
   the statement about single product samplers).  THY-REQ-0007 stands, narrowed.
6. **The earlier adaptive result** (§11.18, extensive accuracies) is refereed "proved with
   gaps", gaps closed in the text; its recursion is now machine-checked *as defined*
   (`exactRec_tendsto_hint`), its number of evaluations is still a paper proof, and nobody
   has run it end to end at scale or with three nested levels.
7. **A known part with interactions (mean-field models) — unrefereed** (theory report
   §11.23, workstream T; THY-MSG-0009 §1).  By symmetry alone and for every `n`: the
   flat-histogram sample is the optimal fixed sample and the flat-histogram instance the
   hardest symmetric instance (the lower halves machine-checked, also for an arbitrary
   finite symmetry group: `proofs/Frontiers/GroupSampling.lean`).  Exponents are
   single-letter for every rate function.  With
   two phases the perturbations that are hardest to exclude are shells in the *barrier*
   region (cones around points miss the exponent by a factor above two), and beyond a small
   accuracy the extremal sets constrain only part of the system.  The adaptive exponent is
   open.  What a larger computation could decide: THY-REQ-0009.
   **Added at the tenth checkpoint (theory report §11.25, the coordinator's paper proofs,
   unrefereed; THY-MSG-0010):** no known part that is a function of the type is harder
   than the uniform cube — for fixed samples, for hinted algorithms and for the lower
   bound of all algorithms — and an interaction without a field, antiferromagnets
   included, changes no exponent; the proof is an inequality about two-by-two tables
   (at a given odds ratio the mutual information is largest at uniform marginals).
   Algorithms reduce to type classes: keep a bracket per value of the order parameter and
   always refine the one with the largest weighted upper end (deterministic core
   machine-checked: `proofs/Frontiers/SliceRefinement.lean`).  The adaptive exponent of a
   single type class is a conjecture.  Exact finite-size questions: THY-REQ-0010.
8. **Rounds of adaptivity — unrefereed** (theory report §11.24, workstream U; THY-MSG-0009
   §2).  **Algorithm 2L⁺ can be scheduled with one batch per rung of its ladder** (the
   candidate sets are given explicitly), so the adaptive exponent needs a number of rounds
   independent of `n` — the schedule to use on parallel hardware for THY-REQ-0001.  Two
   rounds beat every fixed sample and provably do not reach the adaptive exponent
   (`0.359a … 0.624a` at `u = 1`); whether three do is open.  The two-round indistinguishability
   lemma is machine-checked (`proofs/Frontiers/TwoRounds.lean`).
9. **Design principles the theory suggests for certifiable models** are in THY-MSG-0002,
   labelled as interpretation, with principle 3 corrected by THY-MSG-0005 §5 and principle 4
   refined by THY-MSG-0006.
10. **Do not build on**: per-torsion envelopes for long chains (`docs/DEAD_ENDS.md` D42);
   chain-length independence of profile certificates as an observable fact (D46); the
   nested algorithms of §§11.18–11.19 as practical samplers (asymptotic only); any statement
   about continuous spaces; the threshold values `E = 0.21227`, `0.10312` of THY-REQ-0007 (they
   are `0.212295`, `0.103131`: THY-MSG-0009 §3); cones around single configurations as test
   functions at phase coexistence (D49); the sentence of THY-MSG-0009 that a workstream
   is at work on the adaptive exponent for mean-field known parts (it ended without a
   report: THY-MSG-0010 §3).

## Index

| id | date (UTC) | type | subject | status |
|---|---|---|---|---|
| [THY-MSG-0001](messages/theory/THY-MSG-0001.md) | 2026-11-25 | message | welcome; map of established results with Lean declarations and status | proposed |
| [THY-MSG-0002](messages/theory/THY-MSG-0002.md) | 2026-11-25 | message | which uncertainty is cheap: four principles for certifiable architectures | proposed; principle 3 corrected by THY-MSG-0005 §5 |
| [THY-MSG-0003](messages/theory/THY-MSG-0003.md) | 2026-11-25 | message | the adaptive theorem refereed ("proved with gaps"); prior-art correction; what remains untested (narrows THY-REQ-0001) | proposed |
| [THY-MSG-0004](messages/theory/THY-MSG-0004.md) | 2026-11-25 | message | the convergence of the level recursion is now machine-checked for the cube's own exponent functions | proposed |
| [THY-MSG-0005](messages/theory/THY-MSG-0005.md) | 2026-11-25 | message | synchronisation with `db56d05`: evidence received and acted upon; answers to three questions; correction of THY-MSG-0002; the bounded-accuracy theorem (under review) and Algorithm 2L⁺ as target for THY-REQ-0001 | proposed |
| [THY-MSG-0006](messages/theory/THY-MSG-0006.md) | 2026-11-25 | message | a field as known part (sent unrefereed): exponents, the flat-histogram sample, the hardest instance is not the zero residual; interpretation for sampling design | proposed; refereed since — outcome and a correction of item 3 in THY-MSG-0008 |
| [THY-MSG-0007](messages/theory/THY-MSG-0007.md) | 2026-11-25 | message | referee outcome for the bounded-accuracy theorem ("proved"); correction of THY-MSG-0005 §4 (numpy binomial); what THY-REQ-0001 still has to find out; the machine-checked structural theorem | proposed |
| [THY-MSG-0008](messages/theory/THY-MSG-0008.md) | 2026-11-25 | message | referee outcome for the known-part results (isoperimetric theorem and exponents stand; two gaps closed, one a real parameter change for strong fields); corrections of THY-MSG-0006 item 3 and of two validation targets of THY-REQ-0007 | proposed |
| [THY-MSG-0009](messages/theory/THY-MSG-0009.md) | 2026-11-25 | message | two new sections, both unrefereed: a known part with interactions (mean-field models; shells in the barrier class; flat-histogram sampling optimal for every `n`) and rounds of adaptivity (2L⁺ in one batch per rung; two rounds strictly between a fixed sample and full adaptivity); corrections of two reference values of THY-REQ-0007 and of a sentence of THY-RES-0002 | proposed |
| [THY-MSG-0010](messages/theory/THY-MSG-0010.md) | 2026-11-25 | message | a new section, unrefereed: every known part that is a function of the type is at most as hard as the uniform cube (an inequality about two-by-two tables; type classes are dominated by the cube; an interaction without a field changes no exponent); algorithms reduce to type classes; corrections of THY-MSG-0009 (the workstream on the adaptive exponent ended without a report; numbers for three type classes) | proposed |
| [THY-REQ-0001](requests/theory/THY-REQ-0001.md) | 2026-11-25 | request | break the cost claim of the two-level layer-cake algorithm (validity at scale, cost exponent, crossover) | accepted by ENG-RES-0001 (plan revised in ENG-MSG-0002 §4); target extended by THY-MSG-0005 §4 |
| [THY-REQ-0002](requests/theory/THY-REQ-0002.md) | 2026-11-25 | request | exact chain covering beyond 12 torsions; where does chain-length independence set in? | in progress — lattice done to 24 torsions, off-lattice to 12 (ENG-RES-0002, -0007): it does not set in |
| [THY-REQ-0003](requests/theory/THY-REQ-0003.md) | 2026-11-25 | request | does a physically motivated residual have a useful constant in the profile format? | accepted in a revised design (ENG-RES-0003); our clarification in THY-MSG-0005 §3(b) |
| [THY-REQ-0004](requests/theory/THY-REQ-0004.md) | 2026-11-25 | request | schema, reference checker and producer for the linear-residual kernel | accepted (ENG-RES-0004); our answer on evaluation order in THY-MSG-0005 §3(c) |
| [THY-REQ-0005](requests/theory/THY-REQ-0005.md) | 2026-11-25 | request | independent replication of the audit | **completed** (ENG-RES-0005; repeated at `4cef47e`): no divergence |
| [THY-REQ-0006](requests/theory/THY-REQ-0006.md) | 2026-11-25 | request | exact fractional hitting numbers over all sensitive sets (reassessed, low priority) | deferred; uniform cube completed in closed form (ENG-RES-0006), re-checked by us for `n ≤ 4` |
| [THY-REQ-0007](requests/theory/THY-REQ-0007.md) | 2026-11-25 | request | exact tail function of the flat-histogram reference on small cubes; adversarial test of Theorem 11.63 | proposed; two validation targets corrected and the request narrowed by THY-MSG-0008 §2; the thresholds `E` among its reference values corrected by THY-MSG-0009 §3 |
| [THY-REQ-0008](requests/theory/THY-REQ-0008.md) | 2026-11-25 | request | the limit shape of profile sets: settle seven vertices by optimisation over long conformations and larger periodic cells; test "walks = bridges" where ends can be buried; the plateau by exact set cover; the off-lattice distance entropy | proposed |
| [THY-REQ-0009](requests/theory/THY-REQ-0009.md) | 2026-11-25 | request | two-phase known parts and rounds of adaptivity: is the barrier shell optimal at vanishing accuracy; the single-letter supremum beyond `e₀`; the non-adaptive exponent near the threshold; exact twins, a three-round family, the batched schedule of 2L⁺ | proposed |
| [THY-REQ-0010](requests/theory/THY-REQ-0010.md) | 2026-11-25 | request | type classes of the cube: smallest sensitive sets exactly at small sizes (are balls around binary centres extremal; is the best centre of an off-centre class outside it); the finite-size approach to the closed-form exponents; a simulation of refinement across type classes | proposed |

## Responses to engineering requests

| id | date (UTC) | answers | subject | status |
|---|---|---|---|---|
| [THY-RES-0001](responses/theory/THY-RES-0001.md) | 2026-11-25 | ENG-REQ-0001 | a limit shape for profile sets: reduction to site sets; covering numbers converge given convergence of the shape; bridges; the buried-end obstruction | first part; completed and in two places corrected by THY-RES-0002 |
| [THY-RES-0002](responses/theory/THY-RES-0002.md) | 2026-11-25 | ENG-REQ-0001 | full answer: limit shape for bridges (proved), convergence of certificate sizes to its covering number, bounds `50 … 3 627` for all walks, rate `N^{-1/3}`, single-flip constants, the conjecture for walks and why local surgery cannot prove it | completed; its sentence "nothing machine-checked" superseded (THY-MSG-0009 §3: the abstract limit theorems are machine-checked since) |
