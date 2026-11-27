# Which sites must be observed?  Ensembles from averaged squared distances among a labelled subset

**Geometric Inference division — fourth note** (twelfth checkpoint).  Labels as in
`ENSEMBLE_RIGIDITY.md`: [P] proof on paper, [P-exact] proof whose finite part is an exact
computation, [N] numerical, [C] conjecture, [K] known.  **Unreviewed.**  Written in answer to
the research owner's supplementary directive (does a structural conclusion remain
identifiable under incomplete observations; where it does not, a precise obstruction).

## 0. Summary

The main results of `ENSEMBLE_RIGIDITY.md` assume that every point of the chain is observed.
Here only a subset `S` of the points is, through all ensemble-averaged squared distances
among `S`.  One number decides what can be said: **`c(S)`, the number of labelled pairs at
chain separation 1 or 2** — the pairs whose distance is the same in every conformation.

1. **Nothing changes in the theorems** (Theorem P1): the identifiability theorem, the linear
   and the quartic certificate and the demixing algorithms apply verbatim to the labelled
   sites with the constraints that survive among them.  What is determined is the ensemble
   of configurations *of the labelled sites*.
2. **The linear certificate needs `c(S) ≥ (9K² + K + 2)/2`** constrained labelled pairs — 20,
   43, 75 for two, three, four states — and for patterns in general position that is
   enough: proved for labelled bonds that are not adjacent, and for any pattern that
   contains a long enough run of consecutive points; exact for 100 random patterns; a
   conjecture in general (Theorem P2).  Twelve consecutive labelled points, seven labelled
   triples, twenty labelled bonds or twenty-one labels at every second point all do for two
   states — and **one such "anchor" determines every other labelled site**, however
   isolated, in every state.
3. **The quartic certificate needs 17** for two states [P-exact on the patterns tried], and
   scattered patterns reach this number without the structural point that contiguous chains
   have.
4. **Sparse labels determine nothing** (Proposition P3).  If no two labelled sites are at
   chain separation 1 or 2, the ensembles with the same data form a family of dimension at
   least `9K(K − 1)/2` — explicit second solutions are computed — and even one conformation
   shares its data with two-state ensembles.  More generally, below `c(S) = 9K/2` an
   ensemble is not even locally identifiable.

All of this is for the idealised observable of the main report (exact averaged *squared*
distances), abstract chains with exact common bond lengths and bond angles, generic states.
It says nothing about a measurement.

## 1. Setting

A chain of `n` points with unit bonds and a fixed bond angle; `𝒞` its conformation space;
`E₀` the pairs at chain separation 1 and 2, whose distances `1` and `c₁₃` are the same in every
conformation.  `S ⊂ {1, …, n}` is the set of **labelled sites**, `m = |S|`.  For an ensemble `μ`
on `𝒞` the data are `M_S(μ) = (⟨|x_i − x_j|²⟩)_{i,j ∈ S}`.  Put

    E₀(S) = { {i, j} ⊂ S : |i − j| ∈ {1, 2} },      c(S) = |E₀(S)|,      D_K = 3K(3K + 1)/2,      N_K = D_K − K + 1 = (9K² + K + 2)/2 .

A run of `r` consecutive labelled points contributes `2r − 3` pairs to `c(S)`; a labelled
bond 1; two labelled points with one unlabelled point between them 1; labelled points at
separation 3 or more nothing.  `μ_S` is the ensemble of labelled-site configurations
`X_S`, `X ∼ μ`; `z_S` its stacked configuration (`m` points in `ℝ^{3K}` for a `K`-mixture).  `μ` is
*identifiable from `S`* if every ensemble `ν` on `𝒞` with `M_S(ν) = M_S(μ)` has `ν_S = μ_S` up to
congruence of the states.  The unlabelled points are never determined and are not asked
for.

## 2. The theorems transfer

**Theorem P1 [P].**  Theorems A, B, B′ and Propositions 6.1 and 6.2 of
`ENSEMBLE_RIGIDITY.md` hold with the points replaced by `S` and `E₀` by `E₀(S)`.  In particular:
if the only quadrics on `ℝ^{3K}` that vanish on the stacked `E₀(S)`-edge vectors of `z_S` are the
`K − 1` trivial ones (condition CC`_S`), then `μ` is identifiable from `S` among all ensembles,
and DEMIX applied to `(M_S, E₀(S))` returns the labelled-site states and the weights; and the
quartic certificate `h_4 = K` (or `K + dim L` with a structural point) for the space `L` built
from `E₀(S)` has the same consequences.

*Proof.*  Those statements are proved for an arbitrary set of points with an arbitrary set
of statewise-constrained pairs, and use the chain only through `E₀`.  If `ν` is an ensemble on
`𝒞`, then `ν_S` is an ensemble of configurations of `S` satisfying the constraints `E₀(S)`, with
complete averaged data `M_S`.  ∎

**Corollary P1.1 (an anchor carries every other label) [P; P-exact with Theorem C].**  If `S`
contains a subset `S′` for which CC`_{S′}` holds and whose stack spans `ℝ^{3K}` — for instance
`⌈(9K² + K + 8)/4⌉` consecutive points of a generic chain — then CC`_S` holds: the configuration
of **all** labelled sites, including isolated ones, is determined in every state.  (A
quadric vanishing on the edge vectors of `S` vanishes on those of `S′`.)

## 3. How many constrained pairs

**Theorem P2.**
(a) [P] CC`_S` requires `c(S) ≥ N_K`.
(b) [P] *Labelled bonds.*  Let `S` consist of `r` labelled bonds `{s_j, s_j + 1}` with
`s_{j+1} ≥ s_j + 4` (so that `E₀(S)` is exactly these bonds).  For generic chains CC`_S` holds iff
`r ≥ N_K`, for every `K`; below that the conic system has nullity `D_K − r`.
(c) [P-exact, `K ≤ 20`] If `S` contains `⌈(9K² + K + 8)/4⌉` consecutive points, CC`_S` holds for
generic chains (Corollary P1.1 with Theorem C (b)).
(d) [P-exact, pattern by pattern] For 50 random label patterns and 50 random sets of
constrained pairs (`K = 1, 2, 3`; two bond angles; `experiments/geometry/exact_label_patterns.py`)
the generic rank of the conic system is `min(c, N_K)`.
(e) [P-exact] *The rule fails for one state.*  For `K = 1` and two labelled triples
(`c = 6 = N_1`) the rank is 5: the constrained edge directions lie on a pair of planes, a
conic at infinity.  With one more labelled bond the rank is 6.
(f) **Conjecture P [C].**  For `K ≥ 2` and every label pattern the generic rank of the conic
system is `min(c(S), N_K)`: CC`_S` holds for generic chains iff `c(S) ≥ N_K`.

*Proof.*  (a) The system has `c(S)` equations in `D_K` unknowns and a `(K − 1)`-dimensional
space of trivial solutions.  (b) Let `u_s^{(k)}` be the direction of bond `s` in state `k`.  For a
generic chain the directions `(u_{s_1}, …, u_{s_r})` of the labelled bonds form a generic point
of `(S²)^r`: the direction of bond `s + 3` in the frame of bonds `s`, `s + 1` depends on the two
torsions about bonds `s + 1` and `s + 2` through a map onto an open subset of the sphere, so
the derivative of torsions `↦ (u_{s_1}, …, u_{s_r})` is block triangular with surjective
diagonal blocks.  The states are independent, so the stacked edge vectors are those of a
generic freely jointed chain with `r` bonds, and Theorem C (a) — whose proof uses nothing
else — gives the rank `min(r, N_K)`.  (d), (e) At a witness with rational torsion parameters
the rank modulo a prime equals `min(c, N_K)`, which is an upper bound for every chain; so
the generic rank is that number.  For (e): each labelled triple spans a plane, a conic at
infinity that is the union of two planes contains both, so the six functionals are
dependent for every chain; the rank 5 is computed.  ∎

Why the exception in (e) does not recur for `K ≥ 2` at the linear threshold: a reducible
quadric `abᵀ + baᵀ` vanishes on all constrained edge vectors only if two hyperplanes of `ℝ^{3K}`
cover them, and two hyperplanes cover at most `2(6K − 3) = 12K − 6` constrained pairs, which
is less than `N_K` from `K = 2` on.  Below the linear threshold such patterns exist, and they
are exactly the ones with a structural point (§4).

Checked in floating point as well (`label_patterns.py`): on fourteen patterns — an anchor
with sparse labels, scattered triples, scattered bonds, every second point, mixed runs, for
two and three states — the certificate holds and DEMIX recovers the labelled-site states
(RMSD `10⁻⁷`) exactly when `c(S) ≥ N_K`, and the nullity is `max(K − 1, D_K − c(S))` throughout.

## 4. Between the thresholds: the quartic certificate on patterns

With `m_L = dim L = D_K + 1 − c(S)` below the linear threshold, Proposition 6.2 needs
`C(m_L + 3, 4) − K ≤ δ₄(3K)`: for two states `c(S) ≥ 17`.

**Proposition P4 [P-exact; `exact_label_patterns.py`, rational witnesses].**  Two states:

| pattern | `c(S)` | `dim L` | `h_4` | verdict |
|---|---|---|---|---|
| five labelled triples and two labelled bonds | 17 | 5 | 2 | certified |
| runs of 5, 5 and 3 consecutive points | 17 | 5 | 2 | certified |
| every second point, 18 labels | 17 | 5 | 2 | certified |
| six labelled triples | 18 | 4 | 2 | certified |
| two runs of 6 | 18 | 4 | 6 `= K + dim L` | certified modulo one structural point |
| runs of 5 and 6 and a labelled bond | 17 | 5 | 7 `= K + dim L` | certified modulo one structural point |
| ten consecutive points (Theorem I′) | 17 | 5 | 7 `= K + dim L` | certified modulo one structural point |
| five labelled triples and one labelled bond | 16 | 6 | 21 | not certified (the count fails) |

So for these patterns two states are identifiable among all ensembles from 17 constrained
labelled pairs.  A structural point (a matrix `abᵀ + baᵀ` in `L` with `c = 0`) exists exactly
when the labelled bond vectors can be divided between two hyperplanes — two runs of 6; a
run of 10 — and then the defect is exactly `dim L`, as Proposition 6.2 (h) requires;
scattered patterns have none.  Nothing was computed for three states.

## 5. Obstructions

**Regularity (R).**  At each state of `μ` the map `X ↦ X_S` from `𝒞` to the configurations of `S`
that satisfy `E₀(S)` is a submersion.  [N: the rank of torsions `↦` labelled shape is `3m − 6`
for labels every third, fourth and sixth point, and `3m − 6 − c(S)` for every second point —
`label_patterns.py`.  For labels every third point the image is a small neighbourhood:
realisability is lost at displacements of a few hundredths of a bond.]

**Proposition P3 [P, given (R)].**  Let `μ` be a `K`-mixture whose labelled stack spans.
(a) The `K`-state ensembles `ν` with `M_S(ν) = M_S(μ)` form, near `μ_S` and modulo congruence of
states, an analytic set of dimension at least `(K − 1)(9K/2 − c(S))`.  Hence for
`c(S) < 9K/2` the ensemble is **not locally identifiable**, even among `K`-state ensembles.
(b) *Sparse labels.*  If no two labelled sites are at chain separation 1 or 2, that family
has dimension at least `9K(K − 1)/2`; and a single conformation (`K = 1`) has the same labelled data as
two-state ensembles of nearby conformations.
(c) For one state, identifiability from `S` among all ensembles holds iff the constrained
labelled edge directions lie on no conic at infinity (Theorem A); in particular not for
`c(S) ≤ 5`, and not for two labelled triples.

*Proof.*  (a) For `Q ∈ O(3K)` let `y^{(k)}(Q)` be the `k`-th block of `z_SQ` divided by `√w_k`.  The
mixture of the `y^{(k)}(Q)` with the weights `w` has stacked configuration `z_SQ`, hence the data
of `μ`.  Its states satisfy `E₀(S)` iff `|(eQ)_k|² = w_kℓ_e²` for every constrained edge vector `e`
and every block `k`; the sum over `k` of these equations is an identity, so they are at most
`(K − 1)c(S)` equations on `O(3K)`, whose zero set through the identity has dimension at
least `3K(3K − 1)/2 − (K − 1)c(S)`.  Block rotations give congruent states and account for
`3K` dimensions.  By (R) the states `y^{(k)}(Q)`, `Q` near the identity, are labelled-site
configurations of chains.  Two such mixtures with the same weights agree up to congruence
of states only if the `Q`'s differ by a block rotation (the stack spans).  (b) `c(S) = 0`; for
one state take `A_± = I + t_±S` with any symmetric `S ≠ 0` and `w t_+ + (1 − w) t_- = 0`: the states
`X_S A_±^{1/2}` have the averaged data of `X_S`.  (c) Theorem A for the labelled constraint
graph.  ∎

*The count is exact where computed* [N]: the local dimension of the family is `max(0, 9 − c(S))`
for two states (patterns with `c = 0, 6, 8, 9, 12`; contiguous chains with 6 and 7 points)
and `max(0, 27 − 2c(S))` for three (`c = 12, …, 15`).

*Explicit second solutions* [N; `label_patterns.py`, harness test
`sparse_labels_second_solution`; benchmark instance C6].  Two states, 41 points, labels at
every fourth: after a rotation of the labelled stack the two blocks are the labelled sites
of two other chains (fitted to `10⁻¹⁴`), at RMSD `0.18` from the true ones, with the same
averaged squared distances to `10⁻¹⁴`.  With labels at every sixth point the second ensemble
can be taken at RMSD `0.57`.

## 6. The picture for two and three states

`c = c(S)`, patterns in general position:

| `c(S)` | two states | three states | status |
|---|---|---|---|
| `< 9K/2` | `c ≤ 8` | `c ≤ 13` | **not even locally identifiable** [P given (R)] |
| from `9K/2` | from 9: locally identifiable in the cases computed; **not** globally at 11 and 13 (contiguous chains of 7 and 8 points) | from 14 | [N] |
| information threshold `9K − 2` (dimension count) | 16; contiguous chains reach 15 (identifiable, numerically) and 17 | 25 | [C] |
| quartic certificate | from 17 | not computed for patterns; contiguous chains from 29 (16 points) | [P-exact] |
| linear certificate `N_K` | from 20 | from 43 | [P] in the cases of Theorem P2; [C] in general |

For a contiguous chain `c = 2n − 3`, and the thresholds of the main report are these numbers.

## 7. Remarks

1. *The unit is the constrained labelled pair, not the labelled site.*  Twenty labelled
   bonds (40 sites) and twelve consecutive sites carry the same certificate for two states.
   Labels at separation 3 or more from every other label add nothing to any certificate —
   and are nevertheless located in every state once an anchor has demixed the stack.
2. *What is not determined.*  The unlabelled points; and, with sparse labels, anything
   about how the labelled sites are arranged *within* a conformation: the family of
   Proposition P3 (b) contains ensembles whose individual states are far from the true
   ones.
3. *Means against distributions.*  The obstruction is specific to averages.  Whether the
   *distributions* of the same distances identify the ensemble is a question of the Ensemble
   division's theory (laws of edge lengths), not treated here.
4. *Other constraint types.*  Any statewise equality — not only chain separations 1 and 2 —
   enters `c(S)` in the same way; a rigid body with `p` labelled sites contributes
   `p(p − 1)/2` constrained pairs spanning `p − 1` dimensions (up to 3).  Not worked out.

## 8. Prior art

Two web searches at the level of summaries, one paper opened.
* The mechanism of the obstruction is the rotation indeterminacy of second-moment data
  (factor analysis; in structural biology Kam's autocorrelation — both [K], from memory and
  search summaries), restricted to configurations that chains can realise.  No novelty is
  claimed for it; Proposition 3.1 of the main report is the unconstrained case.
* J. M. Hays, E. Boland, P. M. Kasson, "Inference of joint conformational distributions from
  separately-acquired experimental measurements", arXiv 2010.15612 [read through an
  automated fetch, without its supplement]: data are *distributions* of single distances
  measured in separate experiments; "separately measured label sets do not provide
  information on the joint distribution"; a simulation-based estimator; no identifiability
  theorem, no count of label pairs, no second moments.
* A statement of the form "the number of statewise-constrained labelled pairs decides",
  with the thresholds `9K/2`, `N_K`: **not found** — on a thin basis.  The positive part is
  Theorem B for a constraint graph (for one-dimensional states: Laurent–Poljak 1996).

## 9. Limitations and open ends

* The observable is the idealised one of the main report; exact data; exact common local
  geometry; generic states; nothing about noise.
* Conjecture P is proved for labelled bonds and for patterns with an anchor, exact on 100
  random patterns and subsets with at most three states, and open in general.
* (R) is numerical.  For labels at every third point the realisable neighbourhood is small,
  so Proposition P3 gives a family of nearby ensembles only.
* The middle rows of §6 are numerical or conjectural; the quartic certificate on patterns
  was computed for two states only.
* Patterns mixed with states that share rigid parts (`HINGE_ENSEMBLES.md`) are not treated.
