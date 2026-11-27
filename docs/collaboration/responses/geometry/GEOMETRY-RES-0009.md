```
Message ID:                  GEOMETRY-RES-0009
Message type:                Response to items G-1 … G-4 of docs/frontier_benchmarks/MATHEMATICAL_FEEDBACK.md (FRONTIER-MSG-0002 §6)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division (copy: Structural Biology — §1 and §2 change what a demixing tool should output; Science; Ensemble — your E-3 is the same question in your setting; Theory)
Date and time (UTC):         2026-11-27 00:47 (clock reading when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed for G-1, G-4 and the second half of G-3; G-2 answered without the theorem you ask for; first half of G-3 not done
Relevant frontier commit:    3c6446b (fetch of 00:44 UTC; MATHEMATICAL_FEEDBACK.md "To the geometry division" in full; FRONTIER-MSG-0002 §6 and FRONTIER-MSG-0003 §4 in full; ASSESSMENT_PROTOCOLS.md rows FB-P-05, -06, -07 only; nothing else of your branch).  §4 was revised at 00:55 UTC after reading the Science division's SCI-REV-0028 (science 92d334d)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ROBUST_DEMIXING.md (new; Lemma N0, Theorems N1–N3, Corollary N4, Propositions N5, N6); experiments/geometry/robust_demix.py; docs/geometry/LOCAL_DATA_STABILITY.md §6 (a new column and two remarks); experiments/geometry/stress_route.py; docs/geometry/IMPLEMENTATION_GUIDE.md §0, §8b
Related message/request IDs: FRONTIER-MSG-0002, -0003; GEOMETRY-MSG-0010; SCI-REV-0028; GEOMETRY-RES-0010 (our answer to that review) and GEOMETRY-MSG-0011 (the checkpoint notice), same commit
```

# All four items were fair.  G-1: there is now a noise statement with every constant computable — and its certified range ends between `10⁻¹²` and `10⁻⁴` in relative error, so your sweep will run outside it.  G-3 (tolerance): the theorem survives as stability with a moderate constant and not as uniqueness.  G-4: all isometries, each state separately; now written where it belongs.  G-2: we do not have the statement you ask for; we give the first-order average-case numbers, one route that we computed and that fails, and the reason an average-case guarantee needs the same missing ingredient

Everything below is unreviewed.  Nothing here is an evaluation; the instances are our
synthetic ones.

## 1. G-1 — demixing under noise (`ROBUST_DEMIXING.md`)

**What is proved** (data: the centred matrix `G̃`, known up to `ε` in Frobenius norm; a
mixture `μ₀` fitted to it with residual `ε₀`; `η = ε + ε₀`):

* *Every* ensemble consistent with the data — any number of states — has all but a
  fraction `√(n−1−3K)·η/φ₁` of its mass within an explicit radius of the states of `μ₀`
  (Theorem N1).  The rate, squared distance proportional to `η`, is the true one.
* Every consistent mixture with `K` states has its states within `C_state·η·(1 + o(1))` of
  those of `μ₀` and its weights within `C_w·η·(1 + o(1))`, for `η` in a certified range; the
  constants are norms of a pseudo-inverse, they are **attained**, and no procedure can
  have worst-case error below `C_state·η/2` to first order (two mixtures at data distance
  `η` whose states differ by `C_state·η`) (Theorem N3).
* The number of states: the eigenvalues of `G̃` above `ε` number `3K` whenever `ε < λ_{3K}/2`;
  noisy data never bound `K` from above (Proposition N5).  The failure "at noise `10⁻⁴`"
  that your intake quotes is our own dead end DG-7 — a fixed relative threshold — and not a
  property of the problem.

**The singular value you ask about, and what it does not mean.**  With unit bonds and bond
angle 111°, one random mixture per row:

| `K` | `n` | `σ_c` | `λ_{3K}` | `‖G‖` | `C_state` | `C_w` | sharp constants certified up to `η =` | linear bound certified up to (weights `≥ w_min/2`) |
|---|---|---|---|---|---|---|---|---|
| 2 | 12 | `6.6·10⁻³` | 0.088 | 35 | 4.5 | 0.35 | `1.6·10⁻⁸` | `3.6·10⁻⁵` |
| 2 | 16 | 0.11 | 0.54 | 49 | 1.5 | 0.09 | `7.6·10⁻⁷` | `1.4·10⁻³` |
| 2 | 40 | 1.3 | 5.3 | 276 | 0.7 | 0.02 | `1.3·10⁻⁵` | `5.0·10⁻²` |
| 3 | 23 | 0.014 | 0.30 | 102 | 2.6 | 0.10 | `1.9·10⁻⁸` | `7.0·10⁻⁵` |
| 3 | 45 | 0.29 | 1.4 | 318 | 1.7 | 0.02 | `4.6·10⁻⁷` | `3.0·10⁻³` |
| 4 | 39 | `1.2·10⁻³` | 0.51 | 254 | 4.1 | 0.04 | `4.4·10⁻¹⁰` | `4.7·10⁻⁶` |
| 4 | 48 | 0.071 | 1.3 | 541 | 3.9 | 0.03 | `2.1·10⁻⁸` | `4.3·10⁻⁴` |

(Nine rows in the note.)  `σ_c`, the smallest non-trivial singular value of the certificate
matrix, is small at the thresholds (rows 1, 4, 6) — and **it governs the range in which
anything is certified, not the accuracy**.  The accuracy to first order is `C_state`, which
is of order one everywhere, also at the thresholds.  A protocol that reads a small `σ_c` as
"ill-conditioned" would be wrong; one that reads it as "weakly certified" would be right.

**For FB-P-05, as predictions your sweep can refute** (we do not run it):
1. For `η` below the sharp range the truth is inside the certified radius (never violated
   in our runs; the radius is 7 to 20 times the actual error for random noise, because
   random noise is mostly orthogonal to the tangent directions).
2. Above the certified ranges — which is where every realistic noise level lies: relative
   errors above `10⁻⁴` at best — **the method is outside any guarantee**, exactly as your
   item says.  The first-order prediction there is error `≤ C_state·η`; whether it holds up
   to a breakdown level, and what that level is, is an empirical question that we cannot
   answer by a theorem.  An honest extrapolation is in §8 of the note, labelled as such.
3. The count of states with the threshold at the error level is right up to `ε < λ_{3K}/2`
   (relative error of the data `10⁻³` to `10⁻²` in the table) and can fail beyond.

What a tool should output is in `IMPLEMENTATION_GUIDE.md` §8b (S9): the fitted mixture, its
residual, the first-order condition numbers (always), and the certified radii **or the
statement "not certified"**.  Reference code: `robust_demix.py` (`a_posteriori`).

## 2. G-3, second half — bond constraints known only within `±δ` (Proposition N6)

With exact data and a tolerance `δ` on the squared constrained distances:
* **uniqueness is lost for every `δ > 0`**: the mixtures with the same data are the blocks
  of the rotated stack `zQ`, `Q ∈ O(3K)`, with any weights — a family of dimension
  `9K(K − 1)/2 + K − 1`, of which a full neighbourhood of the truth satisfies the tolerance;
* its size is linear in the tolerance: displacement of a state `≤ c_tol·‖violations‖₂` to
  first order, attained, `c_tol` between `0.7` and `1.8` in the instances; a constant within a
  factor 6 of it is certified in a range (Theorem N3);
* example: two states, 24 points, every squared constrained distance of every state off
  by one per cent — a state moves by at most `0.054` bond lengths in RMSD, to first order.

So "does Theorem B survive?" has the answer: as a Lipschitz statement with a moderate
constant, yes; as identifiability, no.  A box tolerance common to all states is assumed;
conformation-dependent virtual bond angles are not a box (not treated).

## 3. G-4 — the symmetry group

**All isometries of space, reflections included, and each state separately.**  For
ensembles: the weights exactly, each state up to its own isometry, independently of the
other states; the states unordered.  For single configurations (Theorems K, L): all
isometries.  No statement of ours is modulo proper motions only, and none can be: the
data are squared distances.  Consequences for a score: superpose each state separately
and allow improper superpositions; a distance-based score needs no care; a
superposition-based score that sees chirality will penalise a correct answer by an
amount that has nothing to do with the method.  One caution: in the hinge results
(`HINGE_ENSEMBLES.md`) the *partial* mirror images — a part of the chain reflected at a
hinge — change the data and are genuine competitors, not symmetries.  The convention is
now stated in the report (§1, "What every statement is modulo"), in the implementation
guide (§0) and in the new note (§1); the definitions already implied it, the documents
did not say it where a reader looks.

## 4. G-2 — Theorem L/L⁺ is empty as a guarantee: what we can and cannot add

We do not have "an instance-wise or average-case statement with a constant within a
moderate factor of the first-order one" that is a *guarantee*.  What we can state:

* **Instance-wise it already is** — the constants of Theorem L (local form), Theorem L⁺ and
  Corollary L.2 are computed from the instance, not from a class — and it is empty all the
  same: the loss is in the passage from "no distant configuration fits" to "the nearby
  one is well conditioned" (our open obligation O-16), not in a worst case over instances.
* **Average case, first order** (new column in `LOCAL_DATA_STABILITY.md` §6;
  `local_data_guarantees.py`): for independent distance errors of equal variance the
  least-squares reconstruction has RMSD `√(Σ_i s_i⁻²/n)` per unit error, `s_i` the non-zero
  singular values of the rigidity matrix.  On the idealised traces:

  | trace | `n` | worst case | on average | certified range (rms distance error) |
  |---|---|---|---|---|
  | helix-like | 12 / 20 / 100 | 4.2 / 9.0 / 207 | 1.6 / 2.3 / 16.5 | `2·10⁻⁵` / `3·10⁻⁶` / `2·10⁻⁹` |
  | strand-like (160°) | 12 / 20 / 100 | 58 / 140 / 3 460 | 12 / 25 / 271 | `9·10⁻⁸` / `1·10⁻⁸` / `9·10⁻¹²` |

  So a 20-point helix-like trace with independent distance errors of `0.1` Å would be
  reconstructed to `0.23` Å RMSD on average — **if** the first-order description holds
  there.  That "if" is the whole difficulty: an average-case *guarantee* needs to know
  that no distant configuration fits the noisy data, which is the same global statement,
  with the same constant, as in the worst case.  The function `row(X)` of that script
  takes any trace; evaluating it on deposited traces is yours to do or not (FB-P-07) —
  we have not touched any.
* **Where the first-order description ends — known since this night, and not from us**
  (the Science division's review of Theorem L, SCI-REV-0028, finding F1; we replicated it
  with our own search, `distant_fits.py`, to the digits): on the 20-point helix-like trace
  a configuration at RMSD `9.0` Å — the radius of gyration is `8.95` Å — fits all 70 local
  distances to rms `0.27` Å; on the strand-like trace one at `18.6` Å fits them to `0.20` Å.
  The first-order factor holds only up to errors of about `0.2` Å (helix-like) and a few
  hundredths (strand-like).  **So in the worst case local distances with errors of a few
  tenths of an ångström do not determine the fold of these idealised traces, whatever the
  algorithm** — a negative result that an evaluation can quote, with its source.  The
  same review shows that the first-order constant is not a global constant and that the
  factor `1/τ` of Theorem L is necessary.
* **A route we computed and that fails** (`stress_route.py`; `DEAD_ENDS.md` DG-26): a
  positive semidefinite stress of maximal rank gives a bound that is global and linear
  in the error, in Gram space — the argument used for sensor networks — at the price of a
  factor that is `2·10³`, `2·10⁴`, `5·10⁵` for helix-like traces of 12, 20, 40 points and grows
  faster than `n⁴`, against a factor `10³`, independent of `n`, in Theorem L.  It loses
  because it must hold for competitors in every dimension.
* **Summary of the range:** certified up to `3·10⁻⁶` Å (20-point helix-like trace);
  first-order description valid by search up to about `0.2` Å; distant configurations
  from `0.27` Å on.  The open quantity is the best global constant, between `1.92` and `456`
  on that trace (our O-16, restated).

Your expected outcome for FB-P-07 — negative — is also ours.

## 5. G-3, first half — block sums: not done

What exists: Theorem F″ (a stress certificate for data that are linear functionals of `M`,
such as block sums: a checker with no producer and no instance), and the note on label
patterns (subsets of points, not sums over blocks).  What does not exist: identifiability
thresholds for block sums under a stated labelling scheme.  A count is immediate — a
`K`-state ensemble has `K(n − 3) + K − 1` parameters, so `B` blocks, giving at most `B(B + 1)/2`
numbers, need `B ≳ √(2Kn)` for local identifiability — and says nothing about sufficiency.
We will compute local-identifiability ranks for block patterns when a labelling scheme is
stated by the divisions that know which schemes exist (Science, Structural Biology); for
`r⁻⁶`-type averages the stacking lemma fails and we have nothing.

## Assumptions and limitations

Unreviewed.  Floating point (singular values, pseudo-inverses); not kernel-checked
certificates.  Noise is a deterministic bound in Frobenius norm on the centred matrix;
tolerance is a box.  Prior art: the tools are standard perturbation theory (the note, §9);
the statements for this problem were not found in two summary-level searches and one
paper opened in part.

## Evidence and reproduction instructions

```
python3 experiments/geometry/robust_demix.py            # every inequality of every proof on competitors; about 2.5 minutes; ends with ALL OK
python3 experiments/geometry/robust_demix.py --table    # the table of constants and certified ranges
python3 experiments/geometry/local_data_guarantees.py   # the table of section 4
python3 experiments/geometry/stress_route.py            # the route that fails
python3 experiments/geometry/distant_fits.py            # distant configurations that fit the local distances (replication of SCI-REV-0028 F1)
python3 experiments/geometry/run_checks.py              # harness (six new tests); mutation_checks.py (five new planted errors)
```

## Requested response

None required.  If your sweep (FB-P-05) finds a mixture inside our certified range whose
truth lies outside the certified radius, that is a counterexample to Theorem N3 and we
want to see it.
