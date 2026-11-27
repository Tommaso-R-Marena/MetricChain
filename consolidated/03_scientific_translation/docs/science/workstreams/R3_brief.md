# Workstream R3 — adversarial referee for the science division's own note `INFERENCE_LIMITS.md`

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R3/`; your report: `docs/science/workstreams/R3_REPORT.md`.

## The object under review

`docs/science/INFERENCE_LIMITS.md` (version 2), written by this division's coordinator in a
few hours and read by nobody else.  Scripts: `experiments/science/pi_inference/`,
`experiments/science/pi_chain/` (see `experiments/science/README.md`).  It claims, on the
theory division's cube class and on the programme's lattice chain:

* Lemma 1, Theorem 2 ("invisible order": ensembles with exactly uniform `k`-body marginals
  and entropy within `⌈k/2⌉ ln(2n)` of the class minimum), Theorem 3 (basin-population bound
  for `k`-wise uniform measures), Theorem 4 (a `k`-body marginal oracle divides the
  all-algorithms lower bound at the zero residual by at most `|C|`), Theorem 5 and
  Proposition 5b (a mean-energy oracle: easy at the zero residual, worst-case exponent
  unchanged because of "hidden twins"), Proposition 6 and Theorem 7 (exactness and stability
  of maximum-entropy refinement, `TV ≤ β·osc(r)/4`), §7 (ratio of macrostates: a three-point
  example), §8 (identified sets: three certificate formats), Theorem 8 (falsification:
  certified lower bounds on model error), Proposition 9 (caloric curve), §11 (numbers on the
  diamond-lattice chain, including the claim that the theory division's limit shape of
  theory report §11.22 is the asymptotic model-free identified set), §12.

The coordinator already caught one overstatement of his own (the first draft said that no
exponent of the theory division is changed by `k`-body data; only `θ_hint` is proved).  Assume
there are more.

## What a review here means

1. **Every proof, line by line**, attempted independently before reading the given proof.
   Particular suspicion is warranted for: the BCH/puncturing bound `|C| ≤ (2n)^{⌈k/2⌉}`
   (Lemma 1's corollary; small `n`, `k` close to `n`, the case `k` odd); Theorem 2(e)
   (continuity/intermediate values; is `ν_{C,b′}` really in the class of constant `b` for
   `b′ ≤ b`?); Theorem 3 (positivity of `F_t` on `[0, r]`, the asymptotic claim, the "attainment"
   paragraph: is `ν(B(a, ρn)) ≥ (1−o(1))/|C|` right, and for which `ρ`?); Theorem 4 (does the
   argument need the algorithm to be correct only on the class? is "the oracle's answers at
   `g ≡ 0`" well defined for randomised adaptive algorithms? is the claim about `θ_hint` being
   "the worst-case exponent of adaptive algorithms" a correct reading of the theory report's
   Theorems 11.25, 11.54, 11.58, including the accuracy regimes?); Theorem 5 (McDiarmid
   constant; one-sidedness; what "certify" means when the lower end is probabilistic and the
   upper end assumes an exact oracle); Proposition 5b (the mechanism; the status label; the
   `o(1)`; whether an *exact* equality of mean energies is needed and whether the adversary
   may tune `s` per centre); Theorem 7 (existence and form of the I-projection; the use of
   Pinsker; is (v) right?); §8 third format (sign conventions of the flow inequality — re-derive
   from Farkas); Theorem 8(c); §11.3 (does Hausdorff convergence of sets give convergence of
   chords of the hulls at interior points? is the identification with a "mean-parameter set"
   correct?).
2. **Independent numerics** with your own code: Theorem 2 and 3 on a code not used by the
   author (e.g. the extended Golay code or a BCH dual with `k ≥ 4`, by sampling or exact
   methods where `n` is too large to enumerate); Theorem 7 on adversarially chosen instances
   (try to beat `βω/4`); the falsification thresholds of §9 and at least one identified
   interval of §11 with an independent LP formulation.
3. **Overstatement hunt**: every sentence in bold, the summary table of §0, the "Reading"
   paragraphs, and the corresponding sentences in
   `docs/collaboration/messages/science/SCI-MSG-0001.md` and
   `docs/collaboration/SCIENCE_TO_ALL.md`.  Flag each sentence that says more than is proved,
   and each physical reading that outruns its assumptions (the cube with zero known part is
   not a molecule; a "`k`-body ensemble-averaged observable" is an idealisation of real
   measurements; exact data do not exist).
4. **Triviality and originality check**, honestly: which statements are textbook facts in
   different words (orthogonal arrays; Rao bound; Gibbs–Bogoliubov; I-projection;
   LP duality), which are short but apparently not written down, and whether the note's
   framing claims more novelty than it disclaims.  Workstream M does the deep literature
   search; you judge the mathematics.
5. **What is missing** for the note to be worth sending to the theory division as a serious
   proposal: the single most valuable theorem that is within reach and would turn the note
   from observations into a result.

## Deliverable

`R3_REPORT.md` in the review format: for each numbered statement, verdict (proved / proved
with gaps / not proved / false / weaker than advertised) with reasons; critical / major /
minor findings, numbered, each with location, what is wrong, why it matters and a suggested
correction; reproduction status; originality assessment; recommended corrections to the
note and to the two collaboration files, as exact replacement text where possible.
