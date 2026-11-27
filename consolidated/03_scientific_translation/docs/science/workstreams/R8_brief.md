# Workstream R8 — adversarial referee of addendum A16 (a mean-energy datum at extensive accuracy)

*Brief written by the coordinator at checkpoint 28.  Read `COMMON.md` first.  You are the
second reader this addendum does not yet have.  You are asked to break it.*

## What you review

`docs/science/INFERENCE_LIMITS_ADDENDA.md`, addendum **A16** (the last addendum of the file;
about 260 lines): the identity `ln Z = S − βU`; Proposition A16.1 (entropy bracket);
Corollary A16.2 (the window in which the datum removes an exponential cost); Proposition
A16.3 (plateau twin); Lemma A16.5 (isoperimetry with an energy constraint); Theorem A16.6
(the cost at the visible basin with the datum); Conjecture A16.4 with its evidence; the
guess for non-adaptive algorithms.  Everything in it is the coordinator's and has been
read by nobody else.  Messages that carry it: `docs/collaboration/messages/science/SCI-MSG-0012.md`,
`SCI-MSG-0013.md`.  Scripts: `experiments/science/pi_inference/plateau_twin_check.py`,
`terrace_twin_explore.py`, `energy_isoperimetry_check.py` (with their `.log` files).

Background you will need: `docs/science/INFERENCE_LIMITS.md` §5 (Theorem 5, Proposition 5b);
addendum A12 (the oracle-invariance theorem and the notes of the second reading of the
hidden-twin proof); `docs/science/workstreams/R3_REPORT.md` §4, "R6" (Lemmas R6.1–R6.3,
Theorem R6 — the proof A16.3 adapts); Proposition A1.1 in
`docs/science/workstreams/A1_REPORT.md` §2.5 (the chain rule used in A16.1).  Theory report
statements used (read-only, at the commit of our tree or with
`git show dcdfea6:docs/THEORY_REPORT.md`): Theorem 11.25(a), Theorem 11.54, Theorem 11.58,
Lemma 11.43 (a), (b).  Tag every statement of the theory division that you use with its
commit.

## What I want, in order

1. **Verdict per statement** — proved / proved after a repair (give it) / gap (say what is
   missing) / false (give the counterexample) — for A16.1, A16.2, A16.3 (a), (b), (c) and
   its counting, A16.5, A16.6 (i)–(iv).  Re-derive; do not trust the text.  Places where I
   would look first if I wanted to break it:
   * A16.3, the deep end: "`m(r₂) < U₀` by the algebra of R6.2 at `s = +1`" for every
     `r₂ ≥ r₁ + 1`, with the overlap — the text gives two lines; write the inequality out
     and say for which `n` it holds.
   * A16.3 (b): the constant; the use of `E` non-decreasing in `κ`; the `o(1)`.
   * A16.5: (i) is the constraint really convex in the weights, and is the direction of
     the Lagrangian inequality right when `φ(t) < 0`; (ii) the pointwise bounds
     `t(x) ∈ [e^{−uρ}, e^{uρ}]` — is the Lipschitz cone used anywhere else, and may it be
     dropped; (iii) Harper's theorem in the form used (inner parallel sets of a set of
     given size are largest for the ball; for sizes that are not ball sizes the text says
     "the complement of an initial segment of the simplicial order" — is that the right
     extremal set, and is it isomorphic to an initial segment?); (iv) the choice
     `η = 1/(c* + U₀ + 1)` and the claim `c* ≥ |U₀|`; (v) the case `U₀ > −1`; (vi) the
     statement is for the *total* mean energy of an instance with a flat background — is
     that what Theorem A16.6 needs?
   * A16.6 (ii): is the algorithm really correct on the whole class (gauge: "all samples
     show one value `v`"; instances with two large level sets; the probability bound;
     what happens when the bracket is narrow but the instance is not flat outside a small
     set)?  Is its cost at `g₀` what is claimed, in expectation and with high
     probability?  (iii): "differ by one unit of the radius" — check the bookkeeping of
     `R`, `r₂ − 1`, `|D| + |V|`.  (iv): the exponential-scale evaluation.
   * A16.2: the two conventions of accuracy (an algorithm is `ε`-accurate if it returns
     `ln Z` within `ε/2`); the identity `ln cosh(u/2) = KL(½‖σ_u)` and the series.
2. **Independent numerics with your own code** (do not import the coordinator's scripts;
   you may read them afterwards and say where yours differ): the entropy bracket on
   members of the class of your own making, including adversarial ones (try to violate
   the lower end); plateau twins by exact sums at sizes of your choice, with overlapping
   supports; Lemma A16.5 by brute force on small cubes **over general members, not only
   over the clipped-level profiles** (e.g. a convex solver or an exhaustive grid on `Q_3`,
   `Q_4` with a few energy levels per state) — the coordinator's brute force assumes the
   form of the optimal profile on a given support; yours should not.
3. **Try to refute Conjecture A16.4** — `θ_U(ε₁) = ln 2 − h(min{½, ρ₀ − σ_u + σ₂(ε₁)})` for
   adaptive algorithms on the whole class.  A16.6 proves it only at instances that are
   constant outside a small set.  Look for a pair of members with the same mean energy,
   indistinguishable to an adaptive algorithm at lower cost than the plateau twin allows
   — on sloped landscapes, on product landscapes (a flat block times a cone block), on
   landscapes with several visible basins, or with the twin hidden inside a visible
   structure.  An explicit pair with exact sums beats an argument.  If you cannot refute
   it, say which families you excluded and how.
4. **The non-adaptive guess** `θ_na^U(ε₁) = θ_na(u·(σ₂(ε₁) − σ_u))` (end of A16; remark (4) of
   Lemma A16.5 gives a datum-assisted bracket for plain Monte Carlo): is the cone with two
   fillings of its apex ball a valid pair (same values outside the ball, same mean
   energy, different `ln Z`)?  Construct it exactly at some `n` or show that it does not
   exist.  Evaluate the worst case of the bracket of remark (4) if you can.
5. **Prior art, briefly** (the coordinator made no search): is "the entropy of a Gibbs
   measure of a log-Lipschitz function on the cube is at least `n·h(σ_u)`" or the
   isoperimetric inequality with an energy constraint in print in some form (maximum
   entropy under a Lipschitz constraint; "flooded" extremal sets in isoperimetric
   problems with two constraints)?  State reading levels; never cite what you did not
   open.
6. **Overstatements.**  Compare the sentences of SCI-MSG-0012, SCI-MSG-0013, digest items
   25 and 27 (`docs/collaboration/SCIENCE_TO_ALL.md`) and status rows S34, S36
   (`docs/collaboration/status/science.md`) with what is proved.  List every sentence that
   says more.  Give replacement texts.

## Rules

Write only in `experiments/science/ws_R8/` (create it) and `docs/science/workstreams/R8_REPORT.md`.
No state-changing git command; no `lake build` (a single file may be checked with
`lake env lean <absolute path>` after `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"`).
Solver tolerances: default HiGHS tolerances have faked violations of exact statements
three times in this branch — scale variables and set the feasibility tolerances to
`1e-10`.  Differences of mean energies cancel catastrophically at `n ≳ 500`: use the excess
identity.  Label every statement [P], [N], [C], [H], [K].  Keep a `NOTES.md` with the order
in which you did things.  The report must start with "How far I got" and "Verdicts in
one paragraph", and must end with "What I did not check".  A lemma in Lean (the algebraic
core of A16.5: `Σ t ≤ Σ f_η(t)` under the constraint, and the monotonicity of `F_η`) is
welcome but optional.
