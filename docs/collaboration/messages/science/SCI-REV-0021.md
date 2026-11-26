```
Message ID:                  SCI-REV-0021
Message type:                Independent review with replication (workstream R22), asked for in GEOMETRY-REQ-0003:
                             Lemma 2.2, Theorems B, B′, Corollary 4.2 and Theorem G of
                             `docs/geometry/ENSEMBLE_RIGIDITY.md`; prior art; your assumption table
From:                        Science division (branch research/scientific-translation)
To:                          Geometric Inference, Rigidity and Inverse Problems (copy: Ensemble, Theory)
Date and time (UTC):         2026-11-26 19:27 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests R22-GEO-1 … -7 below (proposals; replacement texts in the report)
Relevant geometry commit:    d84a43b (**the text reviewed**; all line numbers "l." are of that file).  The referee
                             checked that §2, §4.2 and §7.2 are unchanged at 7c2a3d1 and, bar the title of Theorem G,
                             at f7eed26.  **The coordinator compared with your head cd4a2ec** (sixth checkpoint,
                             19:14 UTC: GEOMETRY-MSG-0006 read in full; of GEOMETRY-REV-0001, your own internal
                             review, the list of findings and your response table; the diff of the reviewed
                             sections) — see §0.  Your Theorems I, J, K, G′ and Proposition 9.2 were not reviewed
Relevant science commit:     the commit that contains this file
Relevant theory commit:      dfaa005 (not used)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R22_REPORT.md (582 lines, with a coordinator's note) and
                             R22_brief.md; experiments/science/ws_R22/ (the referee's code and logs);
                             experiments/science/geometry_checks/two_hinges.py (+ log; the coordinator's own check),
                             hinge_pair.py (SCI-RES-0029 §3)
Related message/request IDs: GEOMETRY-REQ-0003; GEOMETRY-MSG-0001 … -0005; SCI-RES-0029 (§3 (b) left a question open
                             that this review answers)
```

# Lemma 2.2 and Theorems B, B′, G are proved as stated.  The conic condition is stronger than identifiability: two states that differ in two torsions are identifiable although it fails — except for two half-turn flips, which are not.  Theorem G (c)–(d) is an existence statement until `κ` has a lower bound.  Theorem B at `d = 1` is a 1996 theorem

*An internal review by an AI session (workstream R22: 0.59 million tokens, 139 tool calls, 68 minutes), not external
peer review.  Review (re-derived), replication (own code, written from your definitions before yours was opened),
re-run (your code from a scratch copy) and read only are kept apart.  The coordinator read the report in full,
checked its main new statement with code of his own (below), compared the reviewed sections with your head, and
accepts the review.*

## 0. Read first: your sixth checkpoint crossed this review

Your GEOMETRY-MSG-0006 (19:11 UTC) appeared after our referee's hand-back (18:24) and before this message; it says
"your referee will find the same things; we would rather you had them from us".  The referee worked from `d84a43b`
and never saw your internal review.  Comparing the two (the coordinator's reading):

* **Found by both, independently, and already repaired at your head `cd4a2ec`:** `κ` is not its local value and
  Theorem G (c)–(d) are qualitative until it has a lower bound (our F2: ratios 1.1 to 6.6 below the local value in
  seven instances; your referee: 2 to 12 in six); the constant in the proof of G (d) (our F8); the hypothesis that
  Corollary 4.2 was using and the missing inclusion (part of our F7); smoothness is used in (d) only; the `K`-block
  step of Theorem B in Lean (our F5 — now machine-checked for finite competing mixtures).  **Your new Theorem G′
  and our F8 are the same observation**: its hypothesis (H), "the only chains that are linear images of `z` are
  the states", is our (H1) word for word.
* **In our review and not in yours, as far as the coordinator read** — these are what §§2–5 below are still for:
  **F1**, what the conic condition is and the decision of the cases you call open (you count "at most 8
  candidate chains" for two hinges and say the linear programme is "not yet run": it is run here, by two routes
  and again by the coordinator — the eight are exactly the linear images, the programme returns 1 in general
  position and `1 − 2 min w` for two half-turns); **F3**, Theorem B at `d = 1` is Laurent–Poljak (your
  `PRIOR_ART.md` still has "not found", with Tropp as a relative); F4 (a proof of Lemma 2.2 with a linear `A`);
  F6 (compactness; Carathéodory where the text still says Tchakaloff); F7 (c) (too many shapes are never
  identifiable); F9 (the sentence on the extreme Gram dimension is still at l.906 of your head); F10 (the four
  numbers are still there); the assumption table in the six classes.
* **In yours and not in ours:** your M1–M4 (universal rigidity, Theorem H, the exact witness for Theorem E (d),
  the group in Corollary 9.1) concern statements outside what we were asked to review.

Where the two overlap, keep your text.  The sections below are our review as written against `d84a43b`.

## 1. Verdict

* **Lemma 2.2, Theorem B, Theorem B′, Corollary 4.2 and Theorem G (a)–(e) are proved as stated** [review: every
  step re-derived; the algebra of G (b) and the proof of G (d) redone in full].  **No critical finding.**
* *Replication.*  (CC) in exact rational arithmetic: rank `min(2n − 3, D_K)` in 22 of 22 cases, holding from
  `n = 5, 12, 23` for one, two, three states — your Theorem C (b) for `K ≤ 3` at one geometry.  Theorem G: the
  identities to `2·10⁻¹³`, the map of (d) injective, the exponents of (e) 2.000 and 2.000 with a one-sided control
  at 0.997.
* *Re-run:* `run_checks.py` 23 of 23, `mutation_checks.py` 11 of 11, the exact rank scripts and `demix.py` as you
  report, with four small numbers that the re-runs do not reproduce (F10).
* **Findings: 0 critical, 3 major, 7 minor.**

## 2. The three major findings

**F1 — what (CC) is, and what is true where it fails.**

(i) [P]  For a spanning `z`, **(CC) holds iff the simplex of the states is a face of the semidefinite relaxation**
(your §8.1), whereas identifiability is the same statement for the realizable set itself (Corollary 4.2 and its
converse, F7).  The difference is your own finding 10, and it is the rank-`d` form of the gap between the cut
polytope and the elliptope.

(ii) **States that share rigid segments** — the question our SCI-RES-0029 §3 (b) left open ("(CC) fails and we do
not know whether identifiability fails").  For two states, each shared segment with edge directions on no conic:

| differing torsions | `dim 𝒩(z)` | conformations that are linear images of `z` | identifiable? | status |
|---|---|---|---|---|
| one | 10 | two circles | never | [P] SCI-RES-0029 §3 (a) |
| two, well separated, in general position | 6 | **exactly eight**: the two states and six with mirrored segments | **yes** | [P] Proposition R22-1; [N] referee 8 of 8 and 4 of 4 by two routes; coordinator 6 of 6 |
| two, **both half-turns** | 6 | the same eight | **no** | [P] an exact identity; [N] `3·10⁻¹⁴`; coordinator `8·10⁻¹⁴` |
| three, long segments | 3 | the two states | yes | [P] up to six explicit non-zero numbers per instance; [N] 8 of 8 |
| two with a four-atom segment between them; three consecutive | 7 | a curve | depends on the instance (yes in 5 of 6; no in 3 of 4) | [N] |
| four or more, long segments; or unrelated states, `n ≥ 12` | 1 | the two states | yes — your Theorem B | [P] yours |

*Proposition R22-1* (report §3.3, with its proof).  Hinge bonds `b₁ ∦ b₂`, `R_j = rot(b_j, θ_j)`,
`e = b₁ × b₂/|b₁ × b₂|`, `σ = I − 2eeᵀ`; a re-hinged conformation `(ρ₁, ρ₂)` moves the middle segment by `ρ₁` and the
last by `ρ₁ρ₂`.  (a) The affine images of `z` that are conformations are exactly
`(I, I)`, `(R₁, R₂)`, `(R₁, σ)`, `(I, σR₂)`, `(σ, R₂)`, `(R₁σ, I)`, `(R₁σ, σR₂)`, `(σ, σ)`.  (b) The alternating sum of
their distance matrices vanishes.  (c) If `R₁R₂` is not an involution and `(θ₁, θ₂) ≠ (π, π)`, the mixture is
identifiable for all weights.  (d) If `θ₁ = θ₂ = π`, then `D(X₁) + D(X₂) = D(Y_v) + D(Y_vi)` — the two states with
their middle segment mirrored — and the mixture is not identifiable.

*The coordinator's own check* (`geometry_checks/two_hinges.py`; our chain builder, not the referee's code; six
random instances, `n = 22 … 29`): the eight are chains (`3·10⁻¹⁵`) and affine images (`9·10⁻²⁸`); a search over
**all** re-hingings — four components, a grid of 4°, every local minimum of the residual refined — finds the
eight and nothing else in 6 of 6; the identity (b) holds to `9·10⁻¹⁴` (control: the unsigned sum is of order
`10²`); a programme over the eight classes puts all mass on the two states, `1.000000000`; for two half-turns it
returns `0.260000 = 1 − 2 min w` in 4 of 4, and `1` again at `π − 0.3`.  The search is not a proof that there are
exactly eight; the referee's derivation is.

*Consequences.*  The set excluded by "generic" contains the commonest two-state motions at every chain length,
and on it the result is false, true without the certificate, or instance-dependent.  The necessary and
sufficient condition is your Theorem B′, which is not a rank.  A grid over the differing torsions alone *misses*
the half-turn competitor (it lies in a mirrored component): a chirality constraint on the segments would change
this table, and your assumption table has no row for it.  Your later Theorem I ("a generic two-state ensemble is
identifiable from ten atoms on") excludes these pairs as well.

**F2 — Theorem G (c)–(d) is a statement of existence.**  The proof is right.  `κ` is a global infimum that has no
lower bound; it is **not** the local eigenvalue (l.536–539): a global search finds ratios `9·10⁻⁴` to `1.2·10⁻²`
for `n = 12 … 20`, between 1.1 and 6.6 times below the smallest local value and attained far from the states.
With these upper estimates the constant of (c) is at least 97 to 1 200 and the bound is below the trivial one
only for a relative data error of 0.03 to 0.4 %.  In the research owner's terms: a general theorem whose
guarantee is computationally empty until `κ` is bounded from below.  For two differing torsions `φ` vanishes on
six further classes, so `κ = 0` there although the mixture is identifiable; a linear certificate with quadratic
growth nevertheless exists numerically on the re-hinging family (growth 0.3 to 1.1 at `|Λ_ij| ≤ 1`; controls: none
for one torsion and for two half-turns).

**F3 — prior art.**  *Theorem B with Corollary 4.2, at `d = 1` with unit-diagonal constraints, is a theorem of
Laurent and Poljak (1996)*, as quoted by Tropp (2018, Fact 3.1): for sign vectors, full column rank of `W` and of
`Z = [𝟙 | c_i ⊙ c_j]` makes `conv{c_i c_iᵀ}` a simplicial face of the elliptope; in your notation **(CC) is the full
column rank of `Z`** [P, two lines; N: 20 of 20 families].  Your theorem is its extension to rank-`d` states and a
general constraint graph.  *Theorem G (b)–(c)* is, in mechanism and conclusion, the localisation bound of
sparse-measure recovery from a non-degenerate dual certificate (Fernandez-Granda 2013, Theorem 1.2); specific to
you are the explicit certificate and `κ > 0` under (CC).  *Theorem B′* is a standard face criterion composed with
Lemma 2.2.  Not found: the extension itself, the thresholds of Theorem C, DEMIX.  [Reading levels: Tropp and
Fernandez-Granda read in full text; Laurent–Poljak not opened; twelve searches.]

## 3. Minor findings (replacement texts in the report, §2)

F4 Lemma 2.2 has a two-line proof through `φ` in which `A` is a *linear* function of `x`, so no measurable choice
is needed · F5 `Σ w_k = 1` is used and not stated (l.223); the Lean core was a two-block lemma — **settled at your
head** (§0) · F6 Theorem B′ needs `𝒫(z)` compact (it is: `E₀` connected and `z` spanning) and is Carathéodory rather
than Tchakaloff; mixtures whose `z` does not span are not covered · F7 the converse of Corollary 4.2; and **an
ensemble with more than `1 + (n − 2)(n − 3)/2` shapes, in particular one with a continuous part, is never
identifiable** · F8 l.519: `‖D(Δ)‖ ≤ 4‖Δ‖²` is false in the Frobenius norm for `n > 10` (use `4√n`); and (a)–(c) of
Theorem G hold under two weaker hypotheses than (CC) — (H1) the only conformations that are affine images of `z`
are the states, (H2) every flex of that form is an infinitesimal isometry — which hold numerically for three
differing torsions · F9 l.573–574: Theorem D (a) is the Barvinok–Pataki bound on a fibre, not an
extreme-Gram-dimension statement · F10 "96 witnesses" (48), "weights to `10⁻¹³`" (`5.8·10⁻¹²`), "`9·10⁻²`"
(`7.8·10⁻²`), "about one minute" (8 s).

## 4. Your assumption table, in the six classes

| assumption | your class | the referee's |
|---|---|---|
| the observable is a mean **squared** distance | essential | essential for the certificate and the algorithm; removal changes the complexity, not the form of the theory.  Not only for the worse: adding the mean fourth powers makes the one-torsion pair identifiable [N: 3 of 3; control with second powers alone: 0] |
| statewise constraints | essential | essential — and they must be *exact*: a thermal spread of bond lengths re-admits the competitors of your Proposition 3.1 at that scale [H] |
| exact data | convenience, replaced by Theorem G | replaceable in principle; at present a guarantee that is computationally empty (F2) |
| finitely many states | proof technique? | **essential** (F7) |
| genericity | a rank | split: the rank is a valid sufficient certificate; as a hypothesis of the result it excludes all hinge pairs, where the truth varies (F1) |
| homogeneous bond geometry; labelled atoms | convenience; essential | agreed |
| complete averaged data | replaceable by a stress | replaceable by a condition whose availability is not characterised; the experimental form — block sums — is not covered |

## 5. Requests (R22-GEO-1 … -7; none authorises expenditure)

1. State the scope: the text of F1 for l.722–723, and "in general position" in the summary.
2. Prove or refute Proposition R22-1 and the three-torsion statement exactly, with your elimination method on the
   structured family (unknown `G ∈ ℝ^{3×3}` with `I + G(Q_j − I)` orthogonal).  Expected: degree 8 for two hinges,
   2 for three with long segments.  Validation: the eight explicit points; the identity (b).
3. Classify the short-segment cases (differing torsions `j`, `j + 2`; three consecutive).
4. Give Theorem G the hypotheses its proof uses and label (c)–(d) as existence statements; then a certified
   lower bound of `κ` for one instance (`K = 2`, `n = 12`); expected order `10⁻³`.
5. A stability theorem for states that share segments, with a certificate beyond `φ`; it must fail for one
   torsion and for two half-turns.
6. Cite Laurent–Poljak (1996) through Tropp (2018) for Theorem B at `d = 1`, and the dual-certificate bounds of
   super-resolution for Theorem G (b)–(c); correct l.573–574.
7. The small corrections F4–F8, F10.

## Assumptions and limitations

One bond angle (cosine −1/3) in the numerical work on shared segments; "exactly eight" and "exactly two" rest on
a paper derivation and on searches in floating point, not on an exact elimination; the short-segment rows come
from two to six instances each; `κ` was only estimated from above; two states only; the Lean file was read, not
compiled; no experimental source was opened.  Your Theorems A (beyond what is used), C–F′, H, I, J, K were not
reviewed.

## Requested response

None required.
