```
Message ID:                  GEOMETRY-REV-0001
Message type:                Internal adversarial review (referee report), preserved verbatim, followed by the division's response
From:                        a referee commissioned by the Geometric Inference, Rigidity and Inverse Problems Division: a separate session with its own code and no write access to the repository (not an independent division, not external peer review)
To:                          Geometric Inference division; copy: all divisions (Science in particular, whose review R22 covers the same text at d84a43b)
Date and time (UTC):         report handed back 2026-11-26 18:55 (time stamp of the referee's last output); this file: the commit that adds it
Priority:                    High — four statements said more than was proved
Status:                      Completed.  No stated theorem was found false.  4 major and 16 minor findings, all acted on (GEOMETRY-MSG-0006; docs/geometry/DEAD_ENDS.md DG-13 … DG-17)
Relevant source commit:      the text reviewed: docs/geometry/ENSEMBLE_RIGIDITY.md at e8e2582 (first read at d84a43b, then the diffs of 7c2a3d1, f7eed26, e8e2582); line numbers in the report refer to e8e2582
Related theorem or experiment: every statement of docs/geometry/ENSEMBLE_RIGIDITY.md up to the fifth checkpoint; the referee's scripts, logs, saved counterexample ensembles and Lean check files are preserved unmodified in experiments/geometry/review1/
Related message/request IDs: GEOMETRY-MSG-0001 … -0005; GEOMETRY-REQ-0003 (the request for an independent review, to the Science division); GEOMETRY-MSG-0006 (the linked correction)
```

# Internal adversarial review of the cycle-1 report

**How to read this file.**  Part I is the referee's report, verbatim (the referee could not
write files into the repository; the report was handed back as text, and its working
directory, which the report calls "this directory", is preserved as
`experiments/geometry/review1/` — everything except Python caches and the referee's snapshot
of our own report at `e8e2582`, which is `git show e8e2582:docs/geometry/ENSEMBLE_RIGIDITY.md`).
Part II is an addendum from the referee's hand-back message (rows of one table that were
still running when the report text was frozen).  Part III is the division's response, finding
by finding.  The brief given to the referee asked it to try to break the theorems with its
own code, to audit every proof step, and to say what it did not check.

---

## Part I — the referee's report (verbatim)

# Referee report (review 1) on `docs/geometry/ENSEMBLE_RIGIDITY.md`

Independent adversarial review.  Nothing inside the repository was modified, created or
deleted; everything of mine is in this directory
(`/tmp/claude-0/-home-user-MetricChain/97d06659-48fd-552a-a608-15beabe7c002/scratchpad/review1/`).

## 0. What was reviewed, and a warning about the moving target

The report changed **four times while it was being reviewed**.  I first read commit `d84a43b`
(first checkpoint, 729 lines), then re-read the diffs of `7c2a3d1` (Theorem I), `f7eed26`
(Theorem J, renaming to "second-moment rigidity", instance A) and `e8e2582` (fifth checkpoint,
18:14 UTC, 936 lines: `mixture_state_of_conic`, Remark 5.1, Proposition 9.2).
**All line numbers below refer to `e8e2582`**; a snapshot is
`REPORT_UNDER_REVIEW_e8e2582.md` in this directory.  After `e8e2582` the working tree changed
again (a "Theorem G′", `exists_linearMap_of_gram_eq`, `finite_mixture_identifiable` in Lean,
uncommitted when I finished): **not reviewed**, except that I read the statement of Theorem G′
(see §2, remark R1).

Two findings I had made on earlier versions were corrected by the authors before I finished and
are therefore *not* listed as open: the wrong times in §9 ("forty minutes before our first
commit", "read at 18:30 UTC" in a commit made at 17:55 UTC), and the claim that identifiability
among all ensembles "starts at `n = ⌊9K/2⌋+1`" presented as a numerical fact for `K = 2`
(their own `n = 9` data contradicted it; the current text is consistent, see m12).

Conventions of my code: own chain builder by frame propagation (`mylib.py`), bond angle 97°
unless said otherwise (never 111°, cos = −5/13 or tetrahedral in the float checks; the exact
replications use −5/13 because that is the claim to replicate, plus −3/5, −7/25, +3/5), also
unequal bond lengths and unequal bond angles.  None of the authors' code is imported.

---

## 1. Verdict per statement

"Proved" = I re-derived every step and found no gap.  "Replicated" = the computational part
was reproduced with my own code and my own witnesses.

| statement | verdict | remarks |
|---|---|---|
| Lemma 2.1 | proved; V for finite mixtures only | the `L²` sentence is not machine-checked (m9) |
| Lemma 2.2 | **proved** | measure theory is fine (A.1) |
| Proposition 3.1 | proved | (a) is weaker than the truth, (b) ignores the free weights (m6) |
| Theorem A | **proved** | needs "X spans ℝ^d", which the Summary drops (m2) |
| Corollary 4.1 | proved for the two geometries and generic ones | geometry not stated (m5) |
| Theorem B | **proved** | no hidden hypothesis (A.3); searched hard for a counterexample: none (§3b) |
| Theorem B′ | **proved** | the "Tchakaloff" step is elementary and correct (A.4) |
| Corollary 4.2 | proved **with a hypothesis that is used but not stated** | pairwise non-congruent states, `w_k > 0` (m4) |
| Theorem C(a) | **proved** | dimension count `D_K` correct; replicated numerically |
| Theorem C(b) | **proved; replicated exactly for all `K ≤ 12`** | own exact builder, cos = −5/13 and three other geometries |
| Theorem C(c), Lemma R | **proved** | both cases of the recursion checked; constructive check |
| Theorem C(d) | conjecture; I could not falsify it | 16 special bond angles, unequal bonds, `K ≤ 3` float, `K ≤ 12` exact at a new geometry |
| Theorem H(a),(b),(c) | **proved given the exact base cases** (authors' script reproduces "ALL OK"; I confirmed `K = 2, 3` at 60 digits) | the sentences drawn from it are overstated (**M2**) |
| Theorem F′ | **proved** | hypotheses dropped in the Summary; genericity of the general-position hypothesis is not proved in the report — verified exactly by me for `K ≤ 4` (m8) |
| Theorem I (new) | **proved; computation replicated independently** (Hilbert function by my own Macaulay matrices, and Singular on my own witness: degree 7 = 1+1+5) | — |
| Theorem J (new) | (a) correct *given* the Ensemble division's E5/E6, which I did not read; (b) see m14 | outside my mandate |
| Proposition 6.1 (DEMIX) | **proved**; replicated with my own implementation | can be strengthened (m10) |
| Theorem F | **proved** | no instance with incomplete data in the report; I exhibit some and show the theorem cannot beat F′ on band data (m7) |
| Theorem G (a),(b),(c) | **proved** — and without the smoothness hypothesis | `κ` is much smaller than its local values (§3d) |
| Theorem G (d) | **proved with one false intermediate inequality** (harmless) | `‖D(Δ)‖ ≤ 4‖Δ‖²` is false in Frobenius norm for `n ≥ 10` (m1); bracketed claim re-derived in full, correct |
| Theorem G (e) | proved | — |
| Theorem D (a),(b) | **proved; replicated** (constructive decomposition; exact rank-4 witnesses by a different construction) | — |
| Theorem E (a),(b),(c) | **proved** | but the Summary's version of (a) is false (**M1**) |
| Theorem E (d) | **gap, filled by me** | existence of a *generic* framework with indefinite stress rests on a non-generic floating-point instance (**M3**) |
| Corollary 9.1 | moment formula proved; **last sentence wrong/ambiguous** | handedness under `SO(3)`; order 4 under `O(3)` (**M4**) |
| Proposition 9.2 (new) | proved (paper check only) | — |
| "Second-moment rigid, not universally rigid" (instance A, [N]) | numerically replicated with my own code | not certified, as the authors say |
| Lean file | compiles (copy outside the repo), 0 warnings, standard axioms; prose matches statements, slogans do not (**M1**, m11) | — |

**No stated theorem was found to be false.**  The errors are in sentences that summarise the
theorems (Summary, remarks after theorems, §9), in one proof (E(d)) and in one constant.

---

## 2. Findings by severity

### CRITICAL (a stated theorem is false)

None.

### MAJOR (a proof has a real gap, or a statement says more than is proved)

**M1. "Universal rigidity ⇒ second-moment rigidity" is false as written.**
*Where:* Summary item 7, lines 55–63 ("A new rigidity notion **between** global and universal
rigidity … Universal rigidity ⇒ second-moment rigidity ⇒ global rigidity … for chains with at
most 6 atoms the first is an equivalence"); §9 lines 827–830 ("means ⇒ global rigidity,
⇐ universal rigidity, and neither converse holds on chains"); `THEOREM_REGISTER.md` row G1.18
("universal ⇒ ensemble ⇒ global rigidity"); the docstring heading of section 5 of the Lean file
("The hierarchy: universal ⇒ ensemble ⇒ global rigidity").
*Why:* Theorem E(a) needs the extra hypothesis `𝒩(X) = 0` and the Lean theorem
`secondMomentRigid_of_universal` needs `SecondMomentRigid E₀ Set.univ x`.  Without it the
implication fails:
* the report's own Example 3.3: a non-planar 4-atom chain with `F = {14}`; `F ∪ E₀` is the
  complete graph, so the framework is universally rigid, and the cis/trans mixture has the same
  averaged `d₁₄²`;
* machine-checked with the report's own Lean definitions (my file
  `lean_check/Check_e8e2582.lean`, theorem `referee_universal_not_secondMoment`, standard axioms):
  three points `(1, 0, i)` in `ℂ = ℝ²`, `E₀` = the path 0–1–2, `F = {(0,2)}`;
  `UniversallyRigid (F ∪ E₀) x ∧ ¬ SecondMomentRigid E₀ F x`.
"For chains with at most 6 atoms the first is an equivalence" is false for the same reason
(every 4-atom chain; every planar chain).  The notion is *not* between global and universal
rigidity: for complete `F` universal rigidity is vacuous while second-moment rigidity is the
conic condition.  Also "neither converse holds" in §9 is stated as a fact although one of the two
(second-moment rigid but not universally rigid) is [N] only.
*Correction:* "(universal rigidity of `(F ∪ E₀, X)` **and** `𝒩(X) = 0`) ⇒ `F`-second-moment
rigidity ⇒ (global rigidity **and** `𝒩(X) = 0`); for `|E₀| ≤ 9` the first is an equivalence."
Fix the register row and the Lean heading; label the second non-converse [N].

**M2. Theorem H is local, proved for `2 ≤ K ≤ 8` (resp. `1 ≤ K ≤ 8`) at two bond geometries;
three sentences claim more.**
* Summary item 9, lines 73–76, and §5.5 lines 494–500: "identifiable if the number of states is
  known" with threshold 7; "the number of states is exactly the prior that restores
  identifiability"; "identifiable when the number of states is known (`n ≥ 7`)".  Only *local
  injectivity of the two-state parametrisation* is proved (Theorem H(c); §12 itself says
  "Theorem H is local").  Whether another two-state ensemble far away has the same `M` at
  `n = 7, 8, 9` is not addressed.  My direct search found none (§3b: `n = 7, 8, 9`, two instances
  each, 800 starts each, every converged run is the true ensemble) — that is [N], not [P].
* Lines 422–424: "the minimal sequence separation … is **exactly** `K + 3`: each additional
  state costs one more unit of range, and nothing else."  False for `K = 1`: separation
  `3 = K + 2` gives a square Jacobian of full rank (it is diagonal with entries `B_i sin θ_i`;
  confirmed at 60 digits, §3e), so the step from one to two states costs *two* units; and for
  `K ≥ 9`, and for other bond geometries, sufficiency is not proved.
* Summary item 8, line 67: "separation `K + 2` never is" — needs "`K ≥ 2`" (same counterexample).
*Correction:* say "locally identifiable among `K`-state ensembles"; "minimal separation `K + 3`
for `2 ≤ K ≤ 8` (3 for `K = 1`)"; label global uniqueness within the two-state family [N].

**M3. Theorem E(d): the proof asserts the existence of a generic framework with indefinite
stress but gives only a non-generic floating-point instance.**
*Where:* lines 750–756.
*Why:* (i) The theorems of Connelly / Gortler–Healy–Thurston and Gortler–Thurston are for
*generic* configurations (coordinates algebraically independent).  A chain with unit bonds and
bond angle 111° is not generic, so neither "globally rigid" nor "not universally rigid" follows
from the citations for the instance of `hierarchy_example.py`; for that instance non-universal
rigidity is shown directly (a 4D realisation), global rigidity is not shown at all.
(ii) For the theorem one may take `X` generic and *define* `(E₀, ℓ)` by `X` — then the
citations apply — but one then needs a proof that the open set "stress space 1-dimensional,
stress matrix of rank 2, indefinite, `𝒩(X) = 0`" is non-empty.  The report has only floating
point for this.
*Filled:* `g_hierarchy.py` gives exact rational witnesses, e.g.
`X = (0,0,0),(1,0,0),(1,2,0),(3,1,2),(2,−1,3),(4,2,1)`: rigidity rank 12, stress matrix of rank
2 with `e₂(eigenvalues) = −5761/128 < 0` (indefinite), `E₀`-conic rank 6 — all in `ℚ`.  The
conditions are open, so they hold at generic configurations nearby, and E(d) follows via E(c).
For the authors' kind of instance (unit bonds; mine at 97°) I also checked global rigidity
numerically: the four measured-pair equations have exactly two zeros on the 3-torus, `X` and
its mirror image.  Among 2000 Gaussian 6-point configurations 68 % have an indefinite stress.
*Correction:* add an exact witness and the sentence "`X` generic, `(E₀, ℓ)` defined by `X`";
keep the instance as [N].

**M4. Corollary 9.1, last sentence: the moment order depends on the group and on what is
estimated; as written it is wrong in both cases.**
*Where:* lines 839–848 with Proposition 9.2 (lines 850–867).
*Why:* The second moment is invariant under an *independent reflection of each state*.  So
under (CC) it determines the law of shapes modulo reflections — which is what the first half
of the corollary says, correctly — but not the estimand of Proposition 9.2 ("`μ` up to a proper
rotation of each state").  Hence:
* data rotated by `SO(3)`: without constraints order 3 determines the handed mixture
  (Prop. 9.2); with constraints order 2 leaves `2^K` handedness assignments undetermined and
  order 3 is still needed for them.  "From `q = 3` to `q = 2`" holds only for the reflection-
  blind estimand;
* data rotated by `O(3)`: the third moment vanishes; by the report's own parenthesis the
  unconstrained order is at least 4, so "from `q = 3`" is wrong; it is "from `≥ 4` to 2".
The moment formula `E[(g x_i)(g x_j)ᵀ] = ⟨x_i, x_j⟩/3·I` is right for both groups (checked
exactly on the octahedral group and by Monte Carlo); "determines exactly `M(μ)` and nothing
else" is right given `σ`.  The caution "we did not re-derive the sample-complexity theorem" is
adequate for the theorem itself, but the theorem is asymptotic (`σ → ∞`, fixed signal) and its
`q` is defined for a *group orbit*; the estimand must be stated for the sentence to mean
anything.
*Correction:* state the two cases separately and say "up to reflection of each state" for
`SO(3)`.

### MINOR

**m1. Proof of Theorem G(d), line 656: `‖D(Δ)‖ ≤ 4‖Δ‖²` is false** in the Frobenius norm (the
norm used for `M` throughout).  One displaced atom gives `‖D(Δ)‖_F = √(2(n−1))‖Δ‖²`, which
exceeds 4 for `n ≥ 10`, i.e. in every case where (CC) holds with `K ≥ 2` (`h_misc.py`, item 4).
Correct bound: `‖D(Δ)‖_F ≤ 2n‖Δ‖²` (or 2 in the max norm).  Only the unspecified constant
`C_μ` changes.

**m2. Summary item 3, lines 34–36:** "A single conformation is the only ensemble with its `M`
**iff** its constrained edge directions lie on no conic at infinity" — false for planar
conformations: the cis 4-atom chain is identifiable (`d₁₄` is minimal) and `𝒩(X) ≠ 0`.
Theorem A has the hypothesis; the Summary needs "non-planar".

**m3. Summary item 4, line 44:** "a weaker threshold … for every `K` and **every geometry**" —
Theorem C(c) is for *homogeneous* non-degenerate geometries (one bond angle); the heterogeneous
case is `PROOF_OBLIGATIONS` O-10, "not written".  Line 314: "`m₀ = 3` for bond angles between
60° and 120°" except 90°, where `m₀ = 2`.

**m4. Corollary 4.2 (line 278)** uses "the `X_k` are pairwise non-congruent" (line 284) and
`w_k > 0`; neither is in the statement, and without them the first claim is false
(`D(X_1) = D(X_2)`).  Under (CC) both are automatic.  The inclusion `conv{D(X_k)} ⊆ Φ` is
not written (one line: a face containing a relative interior point of a simplex contains it).

**m5. Corollary 4.1 (line 226):** "a generic chain with `n ≥ 5` atoms satisfies it" — the
witness is for two bond geometries (and generic ones by analyticity); say so.  (True at every
geometry I tried, exactly at four rational ones.)

**m6. Proposition 3.1.**  (a) "no configuration of affine dimension ≥ 2" (line 169): without
statewise constraints *no* non-trivial configuration is determined (`X` has the `M` of
`½δ_{√2·X} + ½δ_{point}`).  (b) The weights of `μ_Q` are not determined by the blocks of `zQ`
when there are no constraints (`√w'_k X'_k` is what is given); the family of `K`-state
mixtures with the same `M` has dimension `d²K(K−1)/2 + (K−1)` (10, not 9, for two states in
space).

**m7. Theorem F has no instance with incomplete data in the report** (register: evidence "—").
By a semidefinite programme (`k_stress.py`) such certificates exist for `K = 2`:
`n = 14, 16`, band `3 ≤ |i−j| ≤ 7` and `≤ 8`, and 45 or 55 random pairs out of 66
(`λ_min` of the reduced stress 1.5·10⁻³ … 0.30, kernel exactly `span(𝟙, z)`).  They **cannot**
exist for a band `w ≤ dK` when every `dK+1` consecutive stacked points are affinely
independent: the first row of a banded `Ω` with `Ω[𝟙, z] = 0` is a vanishing combination of
`w+1 ≤ dK+1` independent rows, hence zero, and inductively `Ω = 0`.  So on sequence-local data
Theorem F never improves on Theorem F′; worth saying next to "Between `K+3` and `3K+1` we know
nothing" (line 442).

**m8. Theorem F′ / Summary item 8, line 68:** "among all ensembles a separation of `3K + 1`
suffices [P]" omits the hypotheses ((CC), hence at least `n ≥ n₀(K)`, and affine independence
of every `3K+1` consecutive stacked points).  That the second hypothesis is generic is nowhere
proved (one float test, `K = 2`).  I verified it exactly (mod p, rational witnesses, together
with (CC)) for `K ≤ 4` at `n₀(K)`; it fails, like (CC), when all states are helices.

**m9. Labels.**  Lemma 2.1 "[V]" covers the finite mixture only.  `fourAtom_virtual_value_witness`
is the statement "a number between `a` and `b` is a convex combination of `a` and `b`" and
`block_rigidity_nonvacuous` is `‖u‖² = 1·‖u‖² + 0·‖u'‖²`; neither instantiates the hypotheses
of a theorem of the file, so "non-vacuity" (table of §10) oversells them.  Table row G1.5/§10:
`block_rigidity` is the two-block statement (the report says so in §10; fine since
`mixture_state_of_conic` now covers `K` blocks).

**m10. DEMIX.**  (i) The certificate is sound for *every realizable* input, which the report
does not say: if `M = M(ν)` for some ensemble, `rank G = dK` and `dim 𝒩(Z) = K − 1`, then a
minimal representation of `I` on `𝒫(Z)` has `≤ K` points (affine dimension) and `≥ K` points
(rank), their ranges are then mutually orthogonal, so `ν` is a `K`-mixture satisfying (CC).
(ii) Step 1 refuses rank-deficient stacks; this excludes e.g. every mixture of ideal helices
(stack rank `2K + 1`), which is nevertheless identifiable in my computations (m13).

**m11. Process.**  Line 9 cites `GEOMETRY-REV-0001.md` as "the internal adversarial review";
the file did not exist during the review, and `THEOREM_REGISTER.md` already carries
"REV-0001" in the review column of 20 rows.  Rows should be marked reviewed only with the
verdicts of §1 (in particular G1.18 as it stands is false, M1).

**m12. Two states below the threshold (§5.5).**  Line 487: "4 to 6 further real, positive
semidefinite points" — instance- and geometry-dependent: at 97° I find 4, 8, 2, 6, 4, 10, 6, 6, 4
in nine instances (each isolated, residual 10⁻¹⁵; `f_verify_n9.py`), at 111° 4–6.  The affine
chart contains 48 complex points at `n = 9` (Singular, my witnesses).  Line 491: "`𝒫(z)` is a
surface (dimension `18 − 2n`)" — dimension 4 at `n = 7`.  Line 370: "it gives the right numbers
where we can check them" — for `K = 2` the count gives 10 while identifiability already holds at
`n = 9` in every instance computed (theirs: 6; mine: 18 by LP, 2 by direct search); the data for
`K = 1, 2, 3` fit `⌈9K/2⌉` (5, 9, 14).  Summary item 9 "three different thresholds (10, 7, 12)"
should read "(10 proved / 9 numerically, 7 locally, 12)".  Line 483: at `n = 12`, `dim L = 2`
(by (CC)), not `25 − 2n = 1`.

**m13. Limitations (§12) that are missing.**
* *Helices.*  For `K ≥ 2` states of constant torsion the stacked configuration has rank
  `2K + 1` and `dim 𝒩(z) = 7` (`K = 2`) at every length (`n = 12 … 40`): (CC), DEMIX and
  Theorem G never apply to mixtures of ideal helices.  "Planar and other symmetric
  conformations" (line 927) does not make this visible, and helices are the most common regular
  conformations.  (A single helix has `𝒩 = 0`; a helix plus a generic chain satisfies (CC); a
  two-helix mixture is still identifiable numerically — only the two states are linear images of
  the stack restricted to its span, `m_helix.py`.)
* The mechanism needs the statewise constraints to hold *exactly and identically* in all
  states; nothing is proved for bond data known to finite accuracy.
* (CC) needs `3K ≤ n − 1` and a finite mixture; an ensemble with any continuous spread is
  outside every identifiability theorem of the report (Theorem G only bounds its distance to a
  mixture that satisfies (CC)).
* `κ` in Theorem G: in all six instances I computed the infimum is attained *far* from the
  states and is 2–12 times smaller than the local value (§3d); the remark of lines 673–676
  ("its local value … is a linear-algebra quantity") should not be read as an estimate.

**m14. Theorem J(b) (line 530, outside my mandate).**  "there are chimeras" over the reals is
justified only where the image of the *real* chain variety contains the splice; for
`s ≥ 4` the image is not a product of intervals and a splice of two generic image points need
not be an image point.  The conclusion "not determined" is true for a trivial reason: one
separation does not determine even one state up to congruence (for `s = 3` the signs of the
torsions are free).

**m15. Remark 5.1 (line 381, "from memory").**  "The linearisation … has at least as many
equations as monomials exactly when `dim 𝒩(z) ≤ K − 1`": with all monomials (`t_a` and
`t_a X_ij`) there are `9K(K−1)` equations against `(D+1)(9K−8)` monomials, so at the conic
threshold `D = K − 1` there are `K` too few (18 against 20 for `K = 2`), and for `K = 2` under
(CC) only 10 of the 18 equations are independent.  The sentence "the conic threshold is where
this cheapest algebraic method starts to work" is not supported by the count.

**m16. `PRIOR_ART.md` (supporting file).**  The non-identifiability for exponent 2 is a result
of Belyaeva et al. (cited as such on p. 3 of Cifuentes et al., which I read), not a 2024 result;
"12 ambiguous pairs" should be "at least 12 loci".  The sentence of §9 (line 811) is correct.
I did not verify the other bibliographic statements beyond my own memory of the literature
(they agree with it).

**R1 (remark, uncommitted text).**  Theorem G′ (working tree after `e8e2582`): the reduction of
Theorem G to (H) `𝒫(z) = {E_k/w_k}`, (H′) `𝒩(z) ∩ T_k = 0`, (J) is correct as far as I read it:
those are exactly the three uses of (CC) in the proof, `sym(Π_kᵀB) ∈ 𝒩(z) ∩ T_k`, and (H′) is
the reducedness of `[E_k]` in Theorem I's scheme, which my replication confirms (Jacobian rank
4 at `[E_1]`, `[E_2]`).  Not audited further.

---

## 3. What I verified numerically (all with my own code)

Run everything from this directory.  Random seeds are fixed in the scripts.

### (a) Nullity formula `dim 𝒩(z) = max(K−1, dim Sym(3K) − (2n−3))`

`python3 a_nullity.py` → `a_nullity.out`.  `K = 1, 2, 3`, `n₀(K)−3 … n₀(K)+2`, three instances
each, for (i) unit bonds, 97°, (ii) unequal bonds in [0.7, 1.9], 97°, (iii) unequal bonds and
unequal bond angles in [75°, 150°]: **0 mismatches** (e.g. `K = 2`: 6, 4, 2, 1, 1, 1 at
`n = 9 … 14`; `K = 3`: 8, 6, 4, 2, 2, 2 at `n = 20 … 25`); at and above `n₀` the null space is
the trivial quadrics to 10⁻¹³.  Adversarial scan (attempt to falsify C(d)): bond angles 20, 30,
45, 60, 70.53, 72, 90, 100, 108, 109.47, 120, 135, 144, 150, 160, 170°, `K = 1, 2, 3`: nullity
`K − 1` at `n₀(K)` and the predicted value at `n₀(K) − 1` everywhere.

Exact: `python3 j_exact.py 4` (`j_exact.out`) and `python3 j_exact_big.py 12`
(`j_exact_big.out`): own exact builder (frames in ℚ), rank over `𝔽_p`, `p = 2³¹−1`:
* cos(bond angle) ∈ {−5/13, −3/5, −7/25, +3/5}, unit and unequal rational bonds, `K = 1 … 4`,
  `n ∈ {n₀−1, n₀, n₀+1}`: rank `min(D_K, 2n−3)` in all 96 cases;
* `K = 5 … 12` at `n₀(K) − 1` and `n₀(K)`: cos = −5/13 with unit bonds (the authors' claim)
  and cos = −3/5 with unequal bonds: rank `D_K` at `n₀(K)` in all 16 cases
  (`K = 12`: rank 655 at `n = 329`, 653 at `n = 328`).

### (b) Attempt to falsify Theorem B

*Direct search in torsion space* (no use of the stacking theory): `python3 b_direct.py n K' nstart seed [angle] [hetero]`;
logs `b_direct_part1_n12.out`, `b_direct_part2.out`.  True ensemble: 2 states; fit: `K'` states
(torsions and weights), Levenberg–Marquardt with analytic Jacobian from random starts; a run
"converges" if `max|ΔM| < 10⁻¹⁰`; it is "the true ensemble" if `Σ_a v_a min_k d_P(Y_a, X_k)² < 10⁻⁶`
and the aggregated weights agree to 10⁻³.

| `n` | `K'` | starts × instances | converged | not the true ensemble |
|---|---|---|---|---|
| 12 | 2 | 1200 × 3 (+800 heterogeneous) | 116, 188, 181 (+86) | **0** |
| 12 | 3 | 800 × 3 (+400 het.) | 296, 415, 497 (+265) | **0** |
| 12 | 4 | 400 × 1 | 184 | **0** |
| 13 | 2 | 800 × 2 (+500 het.) | 182, 75 (+44) | **0** |
| 13 | 3 | 500 × 2 (+300 het.) | 322, 295 (+225) | **0** |
| 14 | 2 | 800 × 2 (+500 het.) | 81, 105 (+15) | **0** |
| 14 | 3 | 500 × 2 | 248, 202 | **0** |
| 13, 14 | 3 (het.), 4 | see `b_direct_part2.out` (appended at the end of this file if finished) | | |

Largest `max Q` among converged runs: 3·10⁻⁹ (a state split by `ε ≈ 10⁻⁴`, the effect of
Theorem G(e); my first classifier, with a 10⁻⁶ tolerance on squared distances, flagged these as
"alternatives" — they are not: `b_direct_firstpass.out`).

*Power of the search where the theorem makes no claim* (same code):

| `n` | `K'` | starts | converged | genuine alternatives (all states far from the true ones) |
|---|---|---|---|---|
| 8 | 2 | 800 × 2 | 258, 387 | 0 |
| 8 | 3 | 500 × 2 | 319, 381 | **160**, 0 (e.g. weights 0.704, 0.197, 0.099; `max|ΔM| = 3·10⁻¹⁴`; states at `d_P` ≥ 0.29 from the true ones) |
| 8 | 4 | 150 × 1 | 124 | **120** |
| 7 | 2 | 800 × 2 | 502, 448 | 0 |
| 7 | 3 | 500 × 2 | 500, 500 | **500, 500** |
| 7 | 4 | 150 × 1 | 150 | **150** |
| 9 | 2 | 800 × 2 | 210, 188 | 0 |
| 9 | 3 | 500 × 1 | 381 | 0 |

*Search in `𝒫(z)` + linear programme* (Lemma 2.2 / Theorem B′; own code): `python3 b_pz.py K n nstart seed`.

| `K`, `n` | instances | points of `𝒫(z)` other than the states | alternative ensemble |
|---|---|---|---|
| 2, 12 | 3 | 0 | none |
| 2, 11 | 3 | 0 | none |
| 2, 10 | 3 | 0 | none |
| 2, 9 | 9 (+9 at 111°) | 2 … 10 (finite) | none (LP: no mass off the states) |
| 2, 8 | 3 | a surface (1783–2460 sampled) | **yes**: 9 chains, none a true state, `max|ΔM| = 3.6·10⁻¹⁵, 3.8·10⁻¹³, 4.4·10⁻¹⁵`, bond data to 2·10⁻¹⁴ |
| 2, 7 | 2 | 4-dimensional family | **yes**: 11 chains, `max|ΔM| ≤ 8·10⁻¹⁵` |
| 3, 13 | 1 | a curve | **yes**: 23 chains (one of them a true state, weight 0.14), `2·10⁻¹⁴` |
| 3, 14 | 1 | 0 | none |
| 4, 17 and 18 | 1 | many (surface resp. ≥ 649 isolated points) | none found — inconclusive (sampling) |

Logs: `b_pz_K2.out`, `b_pz_K2_n8.out`, `b_pz_K2_n7.out`, `b_pz_K3.out`, `b_pz_K4_*.out`,
`f_verify_n9.out`; the alternative ensembles are saved as `alt_K*_n*_s*.npz`.

**Result: no counterexample to Theorem B (nor to Theorem I) was found; at `n = 7, 8` (two
states) and `n = 13` (three states) explicit competing ensembles exist to machine precision.**

### (c) Theorem D

`python3 c_theoremD.py` → `c_theoremD.out`.  `n = 6`: four random chains in ℝ⁴ (unit bonds,
`u_a·u_{a+1} = cos 83°`): quadric space of dimension 1, decomposition into **2** chains in ℝ³,
`max|D(Y) − Σ w D(X)| ≤ 2·10⁻¹⁴`, bond data to 2·10⁻¹⁴; four chains in ℝ⁵: quadric space of
dimension 6, recursive decomposition into **4** chains in ℝ³ to 1.4·10⁻¹⁴.  `n = 7`: six random
chains in ℝ⁴: no quadric (smallest singular value of the 11 × 10 system 1.7·10⁻³ … 0.30); the
functional `‖Π^⊥_Y X‖²` (zero at the 4D chain) has minimum 4·10⁻⁷ … 7.5·10⁻³ > 0 over 3D chains
(300 starts each) — small when the 4D chain nearly has a quadric.
Exact (`j_exact.py`, Householder frames instead of quaternions): rank over ℚ of the quadric
system = 10 for six rational 7-atom chains in ℝ⁴ (`γ = 5/13` and `3/5`), 9 for their first six
atoms.

### (d) Theorem G: the certificate

`python3 d_certificate.py n seed nstart` → `d_certificate_*.out`.  `K = 2`, 97°.
`φ(X_k) ≈ 10⁻³⁰`; `φ = −½⟨Π^⊥, D⟩` to 2·10⁻¹⁴; invariance under isometries to 10⁻¹⁴; `φ > 0`
on 5000 random chains (min 0.93 … 1.19 at `n = 14`).  Local values = smallest eigenvalue of
`Π^⊥` on the torsional flexes modulo isometries (confirmed by finite steps to 4 digits).
Global attack: minimise `φ` (BFGS) and `φ/min_k d_P²` (Nelder–Mead + BFGS) from random starts.

| `n` | instance | local values at the two states | smallest ratio found | at `d_P` (RMSD = `d_P/√n`) | global / smallest local |
|---|---|---|---|---|---|
| 12 | 0 | 0.0772, 0.0520 | **0.0236** | 2.49 | 0.45 |
| 14 | 0 | 0.0358, 0.0278 | **0.00233** | 2.60 | 0.084 |
| 14 | 1 | 0.0465, 0.00568 | **0.00317** | 3.68 | 0.56 |
| 14 | 2 | 0.0587, 0.0389 | **0.00551** | 3.59 | 0.14 |
| 14 | 3 | 0.0169, 0.0325 | **0.00514** | 4.27 | 0.30 |
| 18 | 0 | 0.0332, 0.0426 | **0.0134** | 4.99 | 0.40 |

In every instance the minimum is a chain *far from both states* with tiny `φ` (e.g. `φ = 0.0156`
at `d_P = 2.58`, `n = 14`): a near-affine image of the stack.  The constant of G(c),
`√(n−1−3K)/(2κ)`, is therefore at least 47 … 570 in these instances, not the 16 … 230 the
local values would suggest.  Consistently, the largest `Q/‖M(ν) − M(μ)‖_F` over all end points
of the direct search at `n = 12, 13, 14` was 30.

The bracketed claim of G(d): Jacobian of (torsions, weight) ↦ `M` at (CC) points has full
column rank (19 of 19 at `n = 12`, 21 at 13, 23 at 14; smallest singular value 0.38 … 0.63),
`h_misc.py` item 7.

### (e) Theorem H (60-digit central differences, singular values in 60 digits)

`python3 e_jacobian.py` → `e_jacobian.out`.  cos = −1/3 and 97°; also unequal bonds.

| case | parameters, data | rank |
|---|---|---|
| `K=2`, complete, `n=7` | 9, 10 | 9 (full; smallest s.v. 0.11) |
| `K=2`, complete, `n=6` | 7, 6 | 6 (deficient) |
| `K=2`, band `w=5`, `n=7` (square) | 9, 9 | 9 (full; 0.088) |
| `K=2`, band `w=5`, `n=8, 10` | 11, 12; 15, 18 | 11; 15 (full) |
| `K=2`, band `w=4`, `n=7, 8, 9, 10, 12` | `2n−5`, `2n−7` | `2n−7` (deficient) |
| `K=3`, complete, `n=9` / `n=8` | 20, 21 / 17, 15 | 20 (full) / 15 (deficient) |
| `K=3`, band `w=6`, `n=11` (square) | 26, 26 | 26 (full; 0.012) |
| `K=3`, band `w=5`, `n=11` | 26, 21 | 21 (deficient) |
| **`K=1`, band `w=3 = K+2`, `n=8`** | 5, 5 | **5 (full)** — the counterexample of M2 |

### (f) Section 5.2/5.5: extra rank-3 solutions at `n = 9`, none at `n = 10`

Confirmed (table in (b)); the number at `n = 9` is 2–10, not 4–6 (m12).  Algebraic counts
(`python3 l_theoremI.py n seed 3`, Singular on my witnesses, mod `2³¹−1`): affine chart `c = 1`:
**48** complex points at `n = 9`, **2** at `n = 10` and `n = 11`.

### Further checks

* **Theorem I** (`python3 l_theoremI.py 10 0 9`, `l_theoremI.out`): my rational witness,
  `dim L = 5`; Hilbert function of the ideal of the 120 minors from my own Macaulay matrices
  mod p: `1, 5, 15, 35, 7, 7, 7, 7, 7, 7` — a finite scheme of degree **7**; Jacobian rank 4 at
  `[E_1]`, `[E_2]` (reduced), 0 at `[S]`, `S = abᵀ + baᵀ ∈ L`; Singular agrees (dim 1, mult 7)
  for two witnesses.  `n = 11`: Hilbert function `1, 3, 6, 10, 2, 2, …`, degree **2**.
* **Theorem E(d)** (`g_hierarchy.py`): see M3; chain instance at 97°: stress eigenvalues
  −1.568, 0.402; 4D realisation with the 13 lengths to 2·10⁻¹⁵; two-state ensemble with weights
  0.9446, 0.0554 reproducing `X` on `F` to 5·10⁻¹⁵, its states differing from `X` on `F` by
  0.25 and 4.28.
* **Instance A** (`n_instanceA.py`, the authors' torsions in their dihedral convention,
  re-implemented): stress eigenvalues (−1, −0.5232, +0.0705); flex Hessian negative definite
  (−1.098 … −0.0204); grid 40⁴ + 3300 local maximisations: two local maxima up to congruence,
  `X` with `H_c = 3.68885` and another with 3.64100 (margin 0.0478 with `max|c| = 1`, i.e. the
  authors' 0.015 in their normalisation); 4D framework with the 16 lengths to 10⁻¹⁵.  Agrees
  with the report; still [N].
* **Lemma R, C(a), C(c)** (`h_misc.py`): simulated reachable ranges inside the claimed `J_m`
  for nine angles on both sides of 90°; recursion equals the closed formulas for 400 angles and
  `m ≤ 39`; "`J_m = [0, π]` iff `m ≥ m₀`": 0 mismatches; `D_K` random points of `(S²)^K` give
  rank `D_K` (`K ≤ 4`), `D_K − 1` give nullity `K`; explicit chains with prescribed every
  `m₀`-th bond (bond angles 97°, 150°, 40°, 130°; `K = 1, 2`): rank `D_K` from the prescribed
  bonds alone at `n = m₀(D_K−1)+2`.
* **DEMIX** (`i_demix.py`): own implementation recovers `K = 1 … 4` at `n₀(K)` and above
  (squared distances of the states to 2·10⁻¹¹, weights to 4·10⁻¹⁴), refuses at `n = 11` and
  `n = 8` (nullity 2, 8), on helices and with a planar state (rank 5).  `s*` at 111°, 20
  instances: median 9·10⁻³ at `n = 12`, 0.10 at `n = 16` — the report's numbers are typical.
* **Theorem F** (`k_stress.py`): m7.  **Helices** (`m_helix.py`): m13.
* **Lean** (`lean_check/Check_e8e2582.lean`, a copy compiled with the repository's toolchain
  and its existing Mathlib `.olean`s, nothing written to the repository): exit 0, no warning,
  all 12 theorems depend on `propext, Classical.choice, Quot.sound` only; the printed statements
  agree with the table of §10; my counterexample of M1 compiles in the same file.
* **Authors' scripts, unmodified, run with `python3 -B` from outside the repository**
  (`authors_repro/`): `exact_conic_rank.py 12` ALL OK (49 lines), `exact_jacobian_rank.py 8`
  ALL OK, `exact_4d_extreme.py` OK, `exact_nonlinear_threshold.py 10 0 32003` degree 7,
  `run_checks.py` 31 of 31.  (Reproducibility only; none of my checks depends on them.)

---

## 4. What I did NOT check

* Theorem H base cases for `K = 4 … 8` (I did `K ≤ 3` in high precision and ran the authors'
  exact script, which reports all of them).
* Theorem C(b) at the tetrahedral angle over `ℚ(√2)` exactly (only in floating point; the
  exact replication is at cos = −5/13 and three other rational geometries).
* Theorem I over ℚ (I worked mod `2³¹−1`, which suffices at a rational witness by
  semicontinuity, and at two witnesses) and its statement for generic bond geometry.
* The Ensemble division's Theorems E1, E5–E7, E10 (not read): Theorem J(a) and the paragraph of
  §9 that relates the two reports are unverified.
* Anything committed after `e8e2582`, the cycle-2 note (Theorem K), `torsion_sharpness.py`,
  `third_moment.py` (Proposition 9.2 was checked on paper only).
* The literature statements of Remark 5.1 and of §9 beyond Cifuentes et al. (read) and my own
  memory; the sample-complexity theorem behind Corollary 9.1.
* `lake build` of the whole project and the count "5072 declarations" (I compiled only the one
  file, as a copy).
* A certified value of `κ`, a certified global maximum for instance A, completeness of the list
  of real solutions at `n = 9` (multi-start only; bounded by 48 complex ones).
* Theorem G(d),(e) numerically, beyond the injectivity of the linearisation and the
  `ε²` effect seen in the direct search.

---

## Appendix A. Proof audit, step by step

**A.1 Lemma 2.2.**  `ζ_i ∈ L²(ν; ℝ^d)` bounded (connected `E₀`): correct.  Equality of Gram
matrices by polarisation: correct.  `T` well defined and isometric on the span, which is `ℝ^m`
by affine spanning: correct.  Representatives of the finitely many classes `T e_c` give a
measurable `A`; `Tv = A(·)v` a.e., simultaneously for finitely many `i`: correct.
`∫AᵀA dν = I` (entries of `A` in `L²`): correct.  `AᵀA − I ∈ 𝒩(z)` uses `|e| = ℓ_e`, which
holds for stacked configurations by (2.1): correct.  No gap.

**A.2 Proposition 3.1, Theorem A.**  Direct computations; (iii)⇒(ii): `I ± tS ≻ 0`, images in
`𝒞`, average `D(X)`, `D(X_±) ≠ D(X)` because a quadratic form vanishing on all differences of
an affinely spanning set vanishes: correct.  (ii)⇒(i) by Lemma 2.2: correct.

**A.3 Theorem B.**  (CC) ⇒ `z` spans: `vvᵀ` has rank 1, non-zero elements of `𝒯` have rank
`≥ 2d` (two non-zero `s_k` because `w_k > 0`) — the text uses `d ≥ 2` instead, which is a
standing assumption; either way correct.  (CC) also forces pairwise non-congruent states (a
congruence makes the columns of `z` dependent), which the last sentence of the theorem needs.
`P = Σ c_k E_k`, `Σ w_k c_k = 1`, `c_k ≥ 0`, rank ⇒ exactly one `c_κ = 1/w_κ`; `A` vanishes on
the other blocks and is `w_κ^{-1/2}` × isometry on block `κ`; weights from `∫AᵀA = I` and linear
independence of the `E_k`: all correct.  Uses nothing unstated.

**A.4 Theorem B′.**  `𝒫(z)` is compact (PSD with prescribed values on a spanning set of edge
vectors).  (⇐) correct.  (⇒) the "Tchakaloff" step is: the barycentre of a probability measure
with compact support lies in the convex hull of the support (Carathéodory), applied to the
normalised restrictions to `B` and to its complement, `ρ'(B) > 0` because the centre of `B` is in
the support: correct.  `Y_j ∈ 𝒞`, `M(ν') = M(μ)`, `Y_j ≅ X_k ⇔ P_j = E_k/w_k` (affine
spanning): correct.

**A.5 Corollary 4.2.**  Correct with the hypotheses of m4.

**A.6 Theorem C.**  (a) `F_S ≡ 0` iff off-diagonal blocks vanish (flip signs of two unit
vectors) and diagonal blocks are scalar with zero sum: correct, so the function space has
dimension `D_K = (9K²+K+2)/2`; greedy choice of points and analyticity on the connected
manifold `((S²)^K)^N`: correct — the product structure is legitimate because the bonds of a
freely jointed chain are independent.  (b) rank mod p ≤ rank over the number field, analyticity
in torsions and geometry, monotonicity in `n`, counting: correct.  (c) Lemma R: the recursion
(spherical triangle inequality, continuity) is right; for `α ≤ π/2`, `J_m = [0, min(mα, π)]`
(`m ≥ 2`) by induction; for `α > π/2` the substitution `v_a = (−1)^a u_a` turns steps of angle
`α` into steps of angle `β = π − α` and gives `J_m = [0, min(mβ, π)]` (even `m`),
`[max(0, π − mβ), π]` (odd `m`): correct, and `J_m = [0, π]` iff `m ≥ max(2, ⌈π/β⌉)`.
Prescribing every `m₀`-th bond direction of each chain independently is possible (the chains
are independent, consecutive bonds are never parallel, so every such sequence is a point of
the torus); `m₀(D_K − 1) + 1` bonds: correct.

**A.7 Theorem H.**  Counts: `K(n−2) − 1 ≤ (n−2)(n−3)/2` fails for all `n ≤ 2K+2`, `K ≥ 2` (the
text checks only `n = 2K+2`); `Σ_{s=3}^{K+2}(n−s) < K(n−2) − 1` iff `(K+2)(K−1) > 0`; square at
`n = (K²+3K+4)/2`, `w = K+3`: all correct.  Extension lemma: block-triangular structure
(old data do not depend on the new torsions; the weights are old parameters): correct.
`B_{ik} ∝ w_k ×` signed volume of `(i, n−1, n, n+1)` ∝ height of atom `i` above the plane of the
last three atoms: correct.  Heights of atoms `n−2, n−3, …` depend on the new torsion, the new
and the previous one, …: triangular Jacobian with generically non-zero diagonal, so the height
vectors fill an open set of `ℝ^{w−2}` and `K ≤ w−2` of them are independent: correct.  Both
conditions are non-vanishing of analytic functions on a connected manifold, hence hold
together: correct.  (c): full column rank gives injectivity on a neighbourhood *in parameter
space*; nothing is said, and nothing can be said by this argument, about ensembles far away —
mirror images of states and permutations of states give the same shape distribution, any other
far-away coincidence is not excluded (M2).

**A.8 Theorem F′.**  Trilateration in Hilbert space (projection to `𝔸` determined by
differences of squared distances, then the distance from `𝔸` is zero): correct.

**A.9 Theorem I.**  `L = ℝI ⊕ 𝒩(z̃)`, `dim L = 25 − 2n` for `n ≤ 11`.  `S = abᵀ + baᵀ ∈ 𝒩(z̃)`:
correct (each edge vector is orthogonal to `a` or to `b`).  All minors in `𝔪²` at a point of
rank ≤ 2 (adjugate of a 4 × 4 matrix of rank ≤ 2 is zero), local length ≥ 5: correct.
Properness, semicontinuity of fibre dimension, finiteness, semicontinuity of fibre length:
correct.  Weights: `P ↦ WPW` reduces the weighted statement to the unweighted one: correct.
Longer chains: restriction to the first ten atoms: correct.

**A.10 Proposition 6.1.**  `Z = z_c Q₀`, `𝒩(Z) = Q₀ᵀ𝒯Q₀`, a generic element has distinct `s_k`
(for `K = 2` every non-zero element), eigenspaces = blocks: correct.

**A.11 Theorem F.**  Energy identity, `Ω ⪰ 0 ⇒ ΩX = 0` a.e., `X = 𝟙tᵀ + zAᵀ`,
`AᵀA ∈ 𝒫(z)`, Theorem B, weights by affine independence on `F`: correct.

**A.12 Theorem G.**  (a) correct.  (b) Compactness reduces to sequences `X_j → [X_k]`
(reflections are in `d_P`, so a sequence tending to the mirror image is covered after
reflecting; `φ` is reflection invariant).  Optimal alignment gives `X_j − X_k ⟂` infinitesimal
isometries *at `X_j`*; because `⟨ΩV, V⟩ = 0` for skew `Ω` this is the same as *at `X_k`*:
correct.  The limit `V` of unit secants satisfies the linearised constraints — true at singular
points as well.  `φ(X_j)/ρ_j² = ‖Π^⊥V_j‖²` exactly, because `Π^⊥X_k = 0`.  `V = zBᵀ + 𝟙tᵀ`,
`sym(Π_kᵀB) ∈ 𝒩(z) = 𝒯`, blocks: `B_l = 0` (`l ≠ k`), `s_l = 0`, `s_k = 0`, `B_k` skew: `V` is an
infinitesimal isometry, contradiction: correct.  **The smoothness hypothesis is not used in
(a)–(c).**  (c) correct, `‖Π^⊥‖_F = √(n−1−dK)`.  (d) Decomposition into nearest-state cells,
`Δ ⟂` isometries, `τ = P_TΔ ∈ T ⊖ Iso` (because `Iso ⊂ T`), `|Δ − τ| ≤ C|Δ|²` globally
(smoothness near, boundedness far); remainder `≤ C₂Q` (with the constant of m1 corrected).
Bracket, re-derived: if `Σ a_kD(X_k) + Σ w_kL_k(τ_k) = 0` then `ż`, with blocks
`(a_k/2√w_k)X_k + √w_kτ_k`, is an infinitesimal flex of the complete graph on the spanning
configuration `z`, so `ż = zΞ + 𝟙cᵀ`, `Ξ` skew; the flex condition of state `k` on the stacked
edges reads `e[sym(ΞE_k) − (a_k/2w_k)E_k]eᵀ = 0`; this matrix has off-diagonal blocks
`Ξ_{lk}/2` and diagonal blocks `−(a_k/2w_k)I` at `(k,k)`, 0 elsewhere; membership in `𝒯` gives
`Ξ_{lk} = 0` and `w_k·(−a_k/2w_k) = 0`: `a = 0`, `τ_k = X_kΞ_{kk} +` const, trivial.  Correct
(the weights `w_k` in front of `L_k` are absorbed in `τ̄_k`).  Transport: `W₂² ≤ 2Q +
diam²·Σ|ν_k − w_k|`: correct; all constants depend on `μ` only.  (e) correct.

**A.13 Theorem D.**  Barvinok–Pataki as used: an extreme point of
`{G ⪰ 0 : ⟨A_e, G⟩ = ℓ_e², e ∈ E₀}` (Gram matrices of order `n−1`, `m = |E₀|` equations, no
others) has rank `r` with `r(r+1)/2 ≤ m`.  `m ≤ 9 ⇒ r ≤ 3`.  `𝒮` compact (connected `E₀`) and
convex, hence the hull of its extreme points: correct.  (b) extreme ⇔ `𝒩(y) = 0` for a
spanning realisation; an extreme point of `𝒮` lying in `𝒦 ⊆ 𝒮` is extreme in `𝒦`, hence in the
compact set `D(𝒞)`, hence of rank ≤ 3: correct.  Prolongation and generic geometry: correct.

**A.14 Theorem E.**  (a), (b), (c) correct.  (d): M3.

**A.15 Corollary 9.1.**  `E_g[g B gᵀ] = (tr B/3) I` for Haar measure on `O(3)` and on `SO(3)`
(both act irreducibly): correct; noise term: correct.  Last sentence: M4.

## Appendix B. Files in this directory

`mylib.py` (chain builder etc.), `a_nullity.py`, `b_direct.py`, `b_pz.py`, `c_theoremD.py`,
`d_certificate.py`, `e_jacobian.py`, `f_verify_n9.py`, `g_hierarchy.py`, `h_misc.py`,
`i_demix.py`, `j_exact.py`, `j_exact_big.py`, `k_stress.py`, `l_theoremI.py`, `m_helix.py`,
`n_instanceA.py`, their `*.out` logs, `alt_*.npz` (explicit competing ensembles),
`lean_check/` (copies of the Lean file with `#print axioms` and the counterexample of M1),
`authors_repro/` (outputs of the authors' scripts, run unmodified), `run_b_direct*.sh`,
`REPORT_UNDER_REVIEW_e8e2582.md` (the version reviewed).

---

## Part II — addendum from the hand-back message (verbatim rows of the table of §3(b))

The hand-back message repeated the report with the last searches completed:

| n | K' | starts × instances (+ heterogeneous) | converged | not the true ensemble |
|---|---|---|---|---|
| 12 | 2 | 1200 × 3 (+800) | 116, 188, 181 (+86) | 0 |
| 12 | 3 | 800 × 3 (+400) | 296, 415, 497 (+265) | 0 |
| 12 | 4 | 400 | 184 | 0 |
| 13 | 2 | 800 × 2 (+500) | 182, 75 (+44) | 0 |
| 13 | 3 | 500 × 2 (+300) | 322, 295 (+225) | 0 |
| 13 | 4 | 120 | 48 | 0 |
| 14 | 2 | 800 × 2 (+500) | 81, 105 (+15) | 0 |
| 14 | 3 | 500 × 2 (+300) | 248, 202 (+71) | 0 |
| 14 | 4 | 120 | 53 | 0 |
| 9, 10, 11 | 2, 3, 4 | 800, 500, 150 per instance | 67 … 459 each | 0 |

and summarised: "**No stated theorem was found to be false.**  Theorem B survived a hard
attack (14 640 random starts at n = 12–14, 4 194 runs converged to max|ΔM| < 1e-10, every one
the true ensemble), while the same code finds explicit competing ensembles to 1e-14 at
n = 7, 8 (K = 2) and n = 13 (K = 3).  Every exact computation was replicated with my own code
and witnesses (Theorem C(b) for all K ≤ 12, Theorem D(b), Theorem I's degree 7).  The errors
are in sentences that summarise the theorems, in one proof (E(d)) and in one constant."  It
also recorded that the referee "could not create `REPORT.md`: the harness refuses report
files from subagents", and that "nothing inside the repository was modified, created or
deleted" by it.

---

## Part III — the division's response

Every finding was checked against the text and, where it rests on a computation, re-run or
re-derived by us before the text was changed.  We accept all twenty.

| finding | our check | what was changed |
|---|---|---|
| **M1** "universal ⇒ second-moment rigidity" false as written | the counterexamples are correct (Example 3.3 with `F = {14}`; the three points `(1, 0, i)`); the referee's Lean proof compiles in our file | Summary item 7, §9, register row G1.18, the Lean section heading and docstring now carry the conic condition `𝒩(X) = 0`; the counterexample is in the Lean file as `universal_not_secondMomentRigid` (axiom audit); bracketed notes in GEOMETRY-MSG-0002, GEOMETRY-RES-0001, GEOMETRY-REQ-0006; `DEAD_ENDS.md` DG-13 |
| **M2** Theorem H is local; three sentences claimed more | agreed; `K = 1` with separation 3 is a square full-rank Jacobian by the formula `d²_{i,i+3} = A_i − B_i cos θ_i` | Summary items 8, 9; the closing paragraph of §5.3; §5.5; §12; register row G1.20; note in GEOMETRY-MSG-0002, -0003; DG-14 |
| **M3** Theorem E(d): a generic framework asserted, a non-generic floating-point instance given | agreed; the exact witness re-verified by an independent implementation of ours (`experiments/geometry/exact_hierarchy_witness.py`: rigidity rank 12, stress matrix of rank 2 with `e₂ = −5761/128`, conic rank 6) | the proof of E(d) rewritten with the witness and the genericity sentence; harness test `hierarchy_exact_witness` with a mutation; DG-15 |
| **M4** Corollary 9.1, last sentence | agreed (the second moment is blind to a reflection of each state) | Corollary 9.1 states the two groups and the estimands separately; register row G1.22; DG-16 |
| m1 false constant in the proof of G(d) | `‖D(Δ)‖_F ≤ Σ_{ij}|Δ_i − Δ_j|² ≤ 2n‖Δ‖²` | constant corrected |
| m2 Summary item 3 lacks "X spans" | agreed | "that spans space (is not planar)" added |
| m3 "every geometry"; `m₀` at 90° | agreed; Theorem C(c) has since been replaced by a stronger statement that does not involve `m₀` | Summary says "the same bond angle at all positions"; the heterogeneous case stays open (O-10) |
| m4 Corollary 4.2: unstated hypothesis, unwritten inclusion | agreed | hypothesis stated, inclusion written |
| m5 Corollary 4.1: geometry | agreed; in fact Theorem C(c) with `K = 1` gives every bond angle | statement extended and sourced |
| m6 Proposition 3.1 (a) too weak, (b) ignores the weights | agreed (`D(X) = ½D(√2X) + ½D(point)`; dimension `d²K(K−1)/2 + K − 1`) | both corrected; Proposition 9.2's count as well |
| m7 Theorem F had no instance; cannot beat F′ on band data | the band argument re-derived (a banded stress with `Ω𝟙 = 0`, `Ωz = 0` vanishes row by row) | instances cited as the referee's [N]; the obstruction stated in §5.4 [P] |
| m8 Theorem F′: hypotheses dropped in the Summary; genericity unproved | agreed; and the genericity follows for every `K` from the proof of the new Theorem C(c)(iii) | Summary item 8; §5.4; exact check `exact_general_position.py` (`K ≤ 5`) |
| m9 labels; "non-vacuity" oversold | agreed | Lemma 2.1 label; §10 table and the Lean docstring describe the two lemmas as elementary identities; the instance that satisfies the hypotheses of a theorem is `line_mixture_example` (added independently, after `e8e2582`) |
| m10 DEMIX: the certificate is sound for every realizable input | the argument re-derived (Carathéodory in the `(K − 1)`-dimensional affine space; ranks; orthogonality of the ranges) | added to Proposition 6.1 with proof, credited |
| m11 the register cited a review that did not exist | agreed — a process error | the review column now carries the referee's verdicts; "not reviewed" where nobody but the author checked; DG-17 |
| m12 numbers and dimensions in §5.5, §5.2 | agreed | corrected (2 to 10 extra points; dimension `18 − 2n`; `dim L`; what the heuristic count predicts) |
| m13 missing limitations | agreed; the helix statement follows from the fact that the bond vectors of a helix have coordinates in the span of a constant and one harmonic | §12 rewritten (helices; exact and identical constraints; continuous spread; `κ`); the Science division's hinge pairs added |
| m14 Theorem J(b): real chimeras for `s ≥ 4` | agreed | statement and proof reworded |
| m15 Remark 5.1: the Kipnis–Shamir count | not re-derived by us; the sentence is withdrawn | Remark 5.1 |
| m16 `PRIOR_ART.md` attribution | taken from the referee's reading of the 2024 paper | corrected |
| R1 Theorem G′ | — | unchanged; marked "statement read only" in the register |

What the review did not cover, in the referee's words, is its §4; in addition everything
written after `e8e2582` — Theorem G′, the present Theorem C(c), the exact ranks for
`13 ≤ K ≤ 20`, `mixture_identifiable_stacked`, and the corrections above — has been checked by
its author only.
