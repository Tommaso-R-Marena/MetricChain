# Referee report on workstream C ("other representations: reduced costs / A*, weak KAM / tropical, optimal transport / tight spans")

Reviewed: `<session scratch>/ws/C/REPORT.md`
(identical, up to the directory line, to `docs/workstreams/C_REPORT.md`), the scratch Lean file
`NormalForm.lean`, the outputs `out_*.txt` and the downloaded papers in `refs_*/`.
My code: `<session scratch>/referee_C/code/`, outputs in its
subdirectory `out/` (own implementation; none of the author's scripts was run or imported).  Nothing inside the
repository was modified; no `lake build`.

---

## 0. Summary

**No headline theorem is false.**  Theorem C1 (normal form), Theorem C4 (centre-form bound) and
Theorem C3 (Dechter–Pearl transfer) are correct *as stated in the body of the report*; Proposition C5
is reproduced digit for digit.  What needs correction is the *scope* of three of them, which the
verdict paragraph (§1 of the report) states more strongly than the theorems do:

1. **C1 — verified completely.**  Every part re-derived by hand; (i)–(iii) tested exhaustively in
   exact integer arithmetic on 5100 instances (`|X| ≤ 7`, symmetric / asymmetric / signed envelopes,
   `f` not `d`-Lipschitz in 4196 of them), all 216 300 nonempty evaluated sets, 102 000 random
   admissible `g'`: zero failures.  The mathematics is elementary (Johnson reweighting plus the
   adjointness `min(f⊗d + g) = min(f + d⊗g)`, `d⊗g = g`); the *packaging* — value certificates of
   `(d,f,g)` are, set by set and width by width, the point certificates of `(σ,0,E^d)` — is, as far
   as I can tell, new for this problem and worth adopting.
2. **C4 — correct, but its hypothesis is much stronger than it looks.**  Proof checked line by line;
   0 violations in 48 777 runs with *all* tie-breakings and *all* starting points explored
   exhaustively (2400 instances, 1995 with `κ = 1`, 1188 asymmetric).  But `ρ_σ < ∞` **forces
   `f = f^d` (every point is a contact point) and, for symmetric `d`, `Lip(f) ≤ λ < 1`** whenever
   `d(x,y)+d(y,x) > 0` for `x ≠ y`; the clause "started at a contact point (`|C|+1` otherwise)" is
   then vacuous, and the theorem is void as soon as one state is dominated in the known part (one
   sharp site of a product, any dead-end-elimination pair).  "Incomparable with Theorem 11.11" is
   right in general, but for `f ≡ 0`, symmetric `d` and `κ ≥ 1/3` **C4 implies Theorem 11.11 and
   removes its `+1`** (every 11.11 cover is a C4 cover; proof in §2, 0 exceptions in 2000 tests).
   The remark "no violation at `2θ`" is false under adversarial tie-breaking: explicit violations
   at `2θ` and at `1.2θ` (none found at `1.1θ`), so `θ = 1/(2ρ+3)` is tight within 20 % at `ρ = 1`.
3. **C5 — numbers reproduced exactly, but the family-B blow-up depends on the starting point.**
   `K = 4,5,6,6,7,8` (A) and `8,15,28,54,106,211` (B), independent of tie-breaking; extended to
   `η = 1/1280` (A: 11; B: 1674 ≈ 1.308/η); the hole between `x*` and `c` is not essential (same
   `K` on a full grid).  **However the report's own `BF*` (σ-centre start, Theorem C3) solves
   family B in 2 evaluations for every `η`** — the σ-centre *is* the hub `c`.  A one-point
   modification `B'` repairs this (σ-centre `= x*`, `K = 9,16,29,55,107,212`, `N_point = 3`).
   Family A is robust (σ-centre `= x*`).
4. **C3 — correct for `BF*` only.**  Definitions match Dechter–Pearl §4.2 verbatim (I read the
   text, in my own download of the paper); the proof is theirs (Theorem 10) transposed and is
   complete; 5489 constructions against eight kinds of competitors (including instance-tailored
   ones that evaluate a minimum certificate) all succeed.  The verdict's "best-first search is type-3 optimal" is too strong:
   the best-first search of Theorems 11.11/C4/C5 (start at `argmin f`, point stopping rule) *can*
   be strictly dominated (two-point example in §2).  Type 3 is "not strictly dominated on the
   whole class by a sequential correct algorithm" — no bound on the number of evaluations.
5. **Prior art.**  I read Hetland (arXiv:2008.09607v1) in full.  The report's own description is
   accurate; the paraphrase now in `prior_art/L7` ("all of it in that case") is too strong for
   Theorem 11.5 — see §4 for the exact split.
6. **C6–C8.**  Correct, routine; one false "iff" in C6(ii); "exact reason" in the summary of C8 is
   not proved (only sufficiency).  C7 confirmed by brute force (Ising ring: threshold `2h` for all
   `n ≤ 12` and all `J` tested).

---

## 1. Verdict per statement

| statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|
| C1(a) gauge: `d^φ` envelope, `Lip(d^φ) = φ+Lip(d)`, slack and McShane envelopes gauge-invariant | yes | re-derived; Lean (`reduce_isEnvelope`, `admissible_reduce_iff`, `slack_reduce`); numerics (random gauge, point/value/config widths, all `A`) | trivial | known (Johnson reweighting; "cohomologous costs"); the slack = reduced cost remark was already in `prior_art/L4` item 14 and in the brief | fine |
| C1(b) signed normal form `(σ_f,0,E)` for point, value, configuration certificates | yes | re-derived; exhaustive numerics | trivial | new packaging | exact for *all* notions |
| C1(c)(i) `min(f+g') = min(f^d+g')` on the class | yes | re-derived (it is `⟨f⊗d,g⟩ = ⟨f,d⊗g⟩`, `d⊗g = g`); Lean `regularised_ge` (one direction, the other is `f^d ≤ f`); 102 000 random `g'` incl. signed envelopes | elementary | known in substance (min-plus adjointness; implicit in Theorem 2.3) | holds for envelopes with negative entries |
| C1(c)(ii) `w_val^{(d,f,g)}(A) = w_pt^{(σ,0,E^d)}(A) = w_val^{(σ,0,E^d)}(A)` for every `A` | yes | re-derived; exhaustive, exact (216 300 sets) | elementary | **apparently new for certification** | not in Lean |
| C1(c)(iii) three covering relations; `gap^d` slack-Lipschitz; `E^d ∈ Lip(σ)` | yes | re-derived; exhaustive for `ε ∈ {0,1,2,4}`; Lean `client_eq_centre`, `gap_slack_lipschitz` | elementary | new formulation (centre form) | (2)⇔(3) holds pair by pair; (1)⇔(2) only for the set (pairs differ in 315 192 cases); first equivalence not in Lean |
| C1(d) symmetric `d` + known part ⇔ gradient quasi-metric | yes | re-derived; 400 instances | elementary | known mathematics (Kolmogorov criterion) applied | "≡" is for value certificates, covers, best-first; not for finite temperature (the report says so) |
| C1(e) `ι` = max cycle mean; inclusion in a symmetric class enlarged by `ι` | yes | re-derived; LP vs brute-force cycle enumeration (400), inclusion (8000) | routine | [K] + routine | a relaxation only (upper bounds transfer, lower bounds do not) |
| "What this buys" 1–6 | yes | re-derived (exchange via `σ(x,a)=0`; product formula; D30; contact points) ; remark 6 on 500 instances | routine | — | "one-liners" is generous for the exchange lemma (needs the domination argument) |
| C2 (A* with landmarks = certification instance) | yes | re-derived; own A* on 600 random digraphs, two tie-breakings: must-expand set = uncovered set, no node with `f^d+L_A > C*` expanded | routine | [K+R] as claimed | `L_A` is only one of the two ALT bounds |
| C3(i) forced points | yes | repository theorems; `BF*` contained all forced points in 1800 instances | routine | known | |
| C3(ii) `BF*` type-3 optimal | **yes for `BF*`** (σ-centre start, normal form, value stopping rule, sequential algorithms, full admissible class) | proof re-derived line by line; D–P §4.2–4.3 read; 5489 constructions, 0 failures | low–moderate | a transfer; I know no earlier statement for certified Lipschitz optimisation (search budget ran out, see §4) | **summary overstates** (MAJOR 3) |
| C3(iii) no type-2 optimal algorithm in general; `BF*` not type-2 | yes | triangle and 3-point example recomputed by hand and by code | trivial | routine | proper sub-certificate in 9–11 % of my random instances (report: 15 %; distribution-dependent) |
| C4 centre-form bound | **yes** | proof re-derived; Lean `not_cocovered_centre` type-checked and compared with the prose; 48 777 exhaustive-tie runs + 300 larger asymmetric line instances + 120 line instances | low–moderate | new as stated; for `f ≡ 0`, symmetric `d` it is the folklore packing argument (Bouttier et al., Bachoc et al.; zooming-dimension arguments) | hypothesis forces `f = f^d` (MAJOR 2); constants (MINOR 1) |
| "C4 and 11.11 incomparable" | yes in general | hypotheses compared; table reproduced (C4 smaller in 90/90 instances with `λ=0` or `κ=λ=0.5`, 11.11 smaller in 30/30 with `κ=0`, `λ>0`) | — | — | for `f ≡ 0`, `κ ≥ 1/3`: C4 ⟹ 11.11 without `+1` |
| C5 line families | **yes as stated** (start at `argmin f = x*`) | recomputed exactly (integers), 4 tie rules + random; extended to `η = 1/1280`; hole filled | constructive | new negative examples | start-dependent for family B (MAJOR 1); asymptotics numerical |
| best-first on `{0,1}ⁿ`; exponent bracket | yes (spot check) | `N_cov = 6,13,23` (MILP), `K = 12, 19, 37–52, 66–78, 141–147, 253–260` for `n = 4..14`; bracket `[0.1882,0.3553]`, `[0.3509,0.4756]`, `[0.0798,0.2704]`; shrunk-cover exponents `0.535`, `0.477` | routine | routine | `n ≥ 16` not recomputed |
| rule CC (exploratory) | qualitatively | light replication | — | exploratory | ratios softer than quoted and start-dependent (MINOR 7) |
| C6 calibration order, uniqueness sets | yes, except one "iff" | re-derived; 400 instances, 8948 subsets | routine | known in substance | MINOR 2 |
| C7 chain threshold = min cycle ratio; Ising `c* = 2h` | yes | brute force: Ising rings `n = 2..12`, six `(J,h)`; 300 random chains, 1800 `(chain,n)` pairs, 5400 certificate checks | routine | routine | the Ising value is the all-minus configuration, immediate |
| C8 (i)–(iii) | yes (sufficiency) | re-derived; 4514 checks | routine | (i) known, rest routine | "exact reason" not proved (MINOR 4) |
| §2.5 identities (Kantorovich, Gromov, Funk, Yoneda, soft gap `= E^{d,β} − F`, `Λ` Lipschitz, topical bracket, `F(0,g) = −ln(1−κ)`) | yes (those tested) | re-derived; 300 instances | routine | identities | tight-span paragraph not checked |
| prior art: Hetland; AESA; ALT; Mustăţa | accurate with qualifications | Hetland full text; others see §4 | — | — | MINOR 5, 6 |
| `NormalForm.lean` | compiles | `lake env lean`, 7 s, no errors, no warnings; `#print axioms`: `propext, Classical.choice, Quot.sound` only; no `sorry` | — | — | algebraic core only (MINOR 8) |

My own scratch file `<session scratch>/referee_C/lean/RefereeC.lean`
(two lemmas used in MAJOR 2; `lake env lean`, 20 s, no errors or warnings, standard axioms) is not part of
the work under review.

---

## 2. Errors and gaps

### CRITICAL
None.

### MAJOR

**MAJOR 1 — Proposition C5 / verdict §1: the linear blow-up of family B disappears for the report's
own `BF*`.**
*Location:* §2.3 Proposition C5 and the sentence of §1 "on the line with a known part best-first
search uses … `≈ 1.3/η` (extremal residual) evaluations against a certificate of two".
*Finding.*  In family B the one-point widths are `w₁(c) = G`, `w₁(x*) = 1.48 G`, so the σ-centre is
the hub `c`.  Best-first search started there evaluates `c`, then `x*`, and stops: **`K = 2` for
every `η`** (computed for `η = 0.2 … 0.00625`; by hand: after `c` the lower bound is
`G − σ(c,·)`, which is `0` at `x*` and `≥ 0.02 G` elsewhere; after `x*` the lower bound is `≥ 0 = UB`).  So the algorithm that Theorem C3 calls
`BF*` is optimal on family B, and the family is a counterexample only for the start at `argmin f`.
(Family A is robust: its σ-centre is `x*`, `K = 4,5,6,6,7,8` from the centre as well; from the hub
`c` both families need 2.)
*Fix (verified).*  Family `B'` = family B plus one point `y₀ = x* − 2G` with `f(y₀) = f(x*) + 1.4 G`,
`g(y₀) = g(x*) + 2G` (`f` 1-Lipschitz, `g` admissible).  Then the σ-centre is `x*`, best-first from
the σ-centre makes `K = 9, 16, 29, 55, 107, 212` evaluations for `η = 0.2, …, 0.00625`, and
`{x*, c, y₀}` is a point certificate with `N_point = 3` exactly (`x*` is the only `ε`-minimiser,
`y₀` is forced, `{x*,y₀}` is not a certificate).  From the hub, `K = 3`.  The statement should name
the starting rule, or use `B'`.  Also: the growth laws `log₂(1/η)+O(1)` and `≈1.3/η` are
*computed* (I extended them to `η = 1/1280`: A: 9, 10, 11; B: 420, 838, 1674), not proved; and
Hansen–Jaumard–Lu is a theorem on an interval while the families are finite sets with a hole — I
checked that filling the hole with grid points and the steepest admissible known part leaves `K`
and the certificate `{x*,c}` unchanged, so this is not an artefact.

**MAJOR 2 — Theorem C4: the hypothesis `ρ_σ < ∞` forces `f = f^d`.**
*Location:* §2.3, statement of C4 ("started at a contact point … (`|C|+1` for an arbitrary first
point)"), and §1 ("a second bound … that needs no `κ < 1`").
*Finding.*  If `w` is not a contact point, `f^d(w) = f(x) + d(x,w)` for a contact point `x ≠ w`,
hence `σ(x,w) = 0`; quasi-symmetry gives `σ(w,x) = 0`, so `d(x,w) + d(w,x) = σ(x,w)+σ(w,x) = 0`.
Therefore, for every envelope with `d(x,y)+d(y,x) > 0` (`x ≠ y`), **finite `ρ_σ` implies that every
point is a contact point** (machine-checked: `contact_of_quasiSymm` in my scratch file
`…/referee_C/lean/RefereeC.lean`), i.e. `f(y) − f(x) ≤ d(x,y)` for all pairs, and for symmetric `d` that
`f` is `λ`-Lipschitz with `λ = (ρ−1)/(ρ+1) < 1`.  Consequences: (i) the contact-start clause and the
`+1` clause are vacuous except for zero-distance duplicates (I built such instances: 2757 non-contact
starts, `K = |C|+1` reached in 76); (ii) the theorem says nothing when one state is strictly
dominated in the known part — e.g. a product landscape with a single sharp site, where `ρ_σ = ∞`;
(iii) "needs no `κ < 1`" is true, but the price is "needs `Lip(f) < 1` and no dominated state".
*Corrected statement.*  "Let `f = f^d` and let `σ = d^f` be `ρ`-quasi-symmetric.  Then for every
admissible `g` and every `ε ≥ 0`, every best-first run (any start, any tie-breaking) has at most
`|C|` evaluations for every `C` with `∀y ∃c∈C: σ(c,y) ≤ (gap(c)+ε)/(2ρ+3)`."  (With the *value*
stopping rule the same bound holds from any start even when non-contact duplicates exist: 0
exceptions in 48 777 runs, and the proof of (a) goes through with `UB = min_A E^d`.)
*Addendum on "incomparable".*  For `f ≡ 0`, symmetric `d`, `g` `κ`-Lipschitz: a pair of the 11.11
relation satisfies `(1−κ)d(c,y) ≤ s(c,y) ≤ (1−κ)(gap(y)+ε/6)/(4(1+κ))`, so
`d(c,y) ≤ (gap(y)+ε/6)/(4+4κ)`; and `gap(c) ≥ gap(y) − κ d(c,y)` shows that
`d(c,y) ≤ (gap(y)+ε)/(5+κ)` implies the C4 relation.  Since `4+4κ ≥ 5+κ` iff `κ ≥ 1/3`, **every
11.11 cover is a C4 cover for `κ ≥ 1/3`** (machine-checked: `cover1111_imp_coverC4` in
`RefereeC.lean`; 0 exceptions in 2000 random metric spaces and on 75 line instances, where it also
held at `κ = 0.2`).  So without a known part C4 is the stronger theorem
(and has no `+1`); the two are incomparable only because of the known part (`λ → 1`) or small `κ`.

**MAJOR 3 — verdict §1: "best-first search is type-3 optimal".**
*Location:* §1; Theorem C3 itself is stated correctly.
*Finding.*  What is proved is type-3 optimality of `BF*`: normal form, **σ-centre start**, **value
stopping rule**, deterministic history-dependent tie-breaking, against *sequential* correct
algorithms, relative to the *whole* admissible class (the instance `g' = L_A` used in the proof is
extremal, so nothing is claimed for a class with `κ < 1`).  The best-first search of Theorems
11.11 / C4 / C5 is a different algorithm and is **not** type-3 optimal in general.
*Counterexample.*  `X = {x₀,x₁}`, `f ≡ 0`, `d(x₀,x₁) = 2`, `d(x₁,x₀) = 1`, `ε = 1.5`.  One-point value
widths are `w₁(x₀) = 2`, `w₁(x₁) = 1` for every `g`.  Best-first search started at `x₀` (an `argmin f`)
evaluates `{x₀,x₁}` on every instance; "evaluate `x₁`" is correct and evaluates `{x₁}` on every
instance: strict domination.  (Likewise, from a non-contact first point the point stopping rule is
strictly dominated by the value stopping rule: `X = {x₀,x₁}`, `d ≡ 1`, `f = (0,20)`, `g = (0,1/2)`,
`ε = 2`, start `x₁` — the value rule stops after one evaluation, the point rule needs two, and the
value-rule set is always contained in the point-rule set.)  The summary should say "`BF*`", and "in general no
algorithm is type-2 optimal" (it drops "in general").
*What type 3 means here.*  Only: no sequential correct algorithm evaluates a subset of `BF*`'s
points on every instance and a proper subset on one.  It does not bound `K` against `N_cov`
(hub family: `N+1` vs 2; `B'`: `≈1.3/η` vs 3), it is not unique to best-first search, and an
algorithm can be type-3 optimal and exponentially worse than another on most instances.  The
author says this (Reading (4)); the verdict paragraph should too.  Note also that C3 concerns
decision-tree algorithms; the repository's abstract `QueryAlgorithm` class is strictly larger
(`Referee3.pathoAlg_not_a_tree`) and the step "B makes the same first query outside `A` on `g'`"
uses the tree structure.

### MINOR

1. **C4, constants** (§2.3, "no violation of C4 at `2θ` in 2500 random instances").  With all
   tie-breakings and starts explored: 686 violations at `2θ` in 48 777 runs, and violations at
   `1.2θ` (3 in 15 000), none at `1.05θ`, `1.1θ`.  Explicit instances (`f ≡ 0`, symmetric integer
   metrics, `ρ = 1`, `θ = 1/5`), re-verified by an independent enumeration of all best-first runs:
   * 5 points, `d` = rows `(0,8,4,12,8),(8,0,4,8,4),(4,4,0,12,8),(12,8,12,0,4),(8,4,8,4,0)`,
     `g = (4,4,0,12,8)`, `ε = 3`: run `1,3,0,2` (4 evaluations); minimal cover at `2θ` has 3 points.
   * 7 points, `d` = rows `(0,4,8,4,4,2,6),(4,0,6,2,4,4,6),(8,6,0,8,6,6,4),(4,2,8,0,4,2,4),(4,4,6,4,0,2,4),(2,4,6,2,2,0,4),(6,6,4,4,4,4,0)`,
     `g = (1,−1,−3,1,1,3,1)`, `ε = 3`: run `6,0,4,3,2` (5 evaluations); minimal cover at `1.2θ` has 4.
   So the best constant at `ρ = 1` lies in `[1/5, 6/25)`: "not tight" should read "tight within 20 %".
2. **C6(ii)**: "It is all of `X` iff no envelope inequality is tight" is false.  `X = {a,y}`, `d = 1`,
   `g = (1,0)`: `s(a,y) = 0`, yet `Min ∪ Max = X` and neither singleton determines `g`.  Correct:
   `Min ∪ Max = X` iff the calibration order has no chain of three distinct points; "no tight
   inequality" is sufficient only (false as "iff" in 183 of 400 random instances).  Uniqueness of the
   minimal uniqueness set also needs `⪯` to be a partial order (stated, but not repeated in (ii)).
3. **C5**: growth laws are numerical; state the start (see MAJOR 1).
4. **C8 / §1**: "tropical linearity … is the *exact* reason why single dips are extremal" — only
   sufficiency is proved; the converse is the author's own open item 4, and the link to D34 is an
   interpretation, not a proof.
5. **Hetland (§1, §4)**: "proves, for metric nearest-neighbour search" — the theorems are for *range*
   queries; `k`NN is covered only when the result is unique and upper-bound eliminations are ignored
   (his footnote 5), and the adversary part is an informal argument.  The function class is not
   `Lip(d)` but distance functions to a query (`Lip` + Katětov `g(x)+g(y) ≥ d(x,y)`); the two
   coincide on instances with `g ≥ diam/2` (which includes the gadget).  See §4.
6. **AESA (§2.2 table, "literal")**: Vidal's AESA selects by the *sum* `D₁`; the max rule is the
   `D_∞` ordering of Figueroa et al. and the rule of LAESA (`G[p] := max(G[p], |D[p,s] − d(x,s)|)`,
   select `argmin G`), and the bound is two-sided.  "Literal up to the Katětov term" is accurate.
   Similarly `L_A` is one of the two ALT bounds (distances *from* landmarks).
7. **Rule CC (§1, §2.3)**: "55–72 %" rests on 12 and 6 instances; my replication (30 and 8 instances,
   `{0,1}⁸`, `{0,1}¹⁰`) gives 0.60 / 0.71 / 0.82 and 0.74 / 0.82 / 0.89 for `κ = 0 / 0.5 / 1`.
   "Finds the hubs of C5" holds for the start at `x*` used in that test (CC: 2 and 3 — reproduced);
   from the σ-centre CC needs 22, 47, 50 evaluations on family B where best-first needs 2.
8. **Lean**: `NormalForm.lean` proves ten algebraic lemmas.  Not formalised: the width identities
   C1(c), the first covering equivalence, (d), (e), the separation properties (a), (b) of a
   best-first run and the counting step of C4, and all of C3, C5–C8.  The tag "[V core]" is honest;
   note that (a), (b) *are* the repository's `bestFirst_sep_a`, `bestFirst_sep_b` rewritten through
   `client_eq_centre`, so a full machine check of C4 is a short exercise.  Hypotheses of
   `not_cocovered_centre` match the prose (`σ(y_j,c) ≤ ρσ(c,y_j)`, `ε < σ(y_j,y_k)`,
   `gap(y_j) ≤ σ(y_j,y_k)`, `θ(2ρ+3) ≤ 1`); it asks `0 ≤ ρ` only.
9. **"Free" regularisation**: `f → f^d` and the σ-centre are free in evaluations of `g`, not in
   computation (`f^d(y) = min_x[f(x)+d(x,y)]` is a white-box minimisation for each `y`; explicit for
   additive `f` and weighted Hamming `d`).  Worth one sentence if §11 is rewritten in normal form.
10. **C1, "what this buys" 1**: the exchange lemma in normal form is not one line; it is the
    domination argument "`σ(x,a) = 0` ⟹ `E^d(x) ≤ E^d(a)` and `σ(x,·) ≤ σ(a,·)`" (correct, three
    lines).

**Statements of the summary (§1) that are stronger than what is proved:** "best-first search is
type-3 optimal" (MAJOR 3); "no algorithm is type-2 optimal" (in general only); "needs no `κ < 1`"
without "needs `f = f^d`, `Lip(f) < 1`" (MAJOR 2); "`≈1.3/η` … against a certificate of two"
without the starting rule (MAJOR 1); "exact reason" (MINOR 4); "Hetland proves, for metric
nearest-neighbour search" (MINOR 5); "finds these hubs and needs 55–72 %" (MINOR 7).

---

## 3. Independent numerical checks (own code, directory `…/referee_C/code/`)

| script | what | size | result |
|---|---|---|---|
| `c1_normal_form.py` | C1(a)–(c), exact integers, all nonempty `A`, `ε ∈ {0,1,2,4}`; envelopes symmetric / asymmetric / signed (1700 each); random integer `f` | 5100 instances `|X| ≤ 7`; 216 300 sets; 102 000 `g'` | 0 failures in: `min(f+g') = min(f^d+g')`; three widths equal; signed normal form and random gauge (point, value, configuration); three covering relations; value certificate ⇔ centre form with the incumbent; `gap^d` slack-Lipschitz; `N_value = N_point(σ,0,E^d)`; `N_cov ≤ N_value = N_point ≤ N_cov+1`.  Raw gap not slack-Lipschitz in exactly the 4196 instances with `f ≠ f^d` |
| `c1_de.py` | C1(d),(e) | 400 + 400 instances, 8000 inclusions | all hold (LP value = max cycle mean by enumeration) |
| `c4_bestfirst.py` | C4; memoised DFS over **all** tie-breakings, all starts; exact minimal covers; duplicates for non-contact starts | 2400 instances (`|X| ≤ 12`), 48 777 runs | 0 violations; equality 4496 times; non-contact start: `|C|+1` reached 76 times; value rule: 0 violations from any start; violations at `2θ`: 686, at `3θ`: 3796 |
| `c4_tight.py`, `c4_examples.py` | enlarged radii | 15 000 runs; 2 explicit instances | violations from `1.2θ` on; none at `1.05θ`, `1.1θ` |
| `c4_line_asym.py` | C4, asymmetric line quasi-metric, extremal `g`, `λ ∈ {0,0.3,0.6}` | 300 instances of 40 points | 0 violations (mean `K` 5.0, mean cover 16.4) |
| `c4_compare.py` | C4 vs 11.11; C5(2) | 120 line instances of 60 points; 2000 metric spaces | table reproduced (e.g. `κ=0.5,λ=0`: 32.2 vs 42.5; `κ=0,λ=0.9`: 38.0 vs 27.0); 11.11-pair ⟹ C4-pair for `f ≡ 0`: 0 exceptions; family A shrunk client covers 6, 6, 8, 9; family B centre covers 35, 68, 134, 266 — as reported |
| `c5_line.py`, `c_misc.py` | C5 families, exact integers; ties low/high/left/right/random; hole filled | `|X|` up to 13 382 | `K` = 4,5,6,6,7,8 / 8,15,28,54,106,211; `{x*,c}` certificate, no singleton; `η = 1/320, 1/640, 1/1280`: A 9,10,11; B 420, 838, 1674 |
| `c5_centre_start.py`, `c5_allstarts.py` | start dependence; variant `B'` | all starts | family B from σ-centre: `K = 2`; `B'`: 9,16,29,55,107,212 with `N_point = 3`; from the hub: 2 (A, B), 3 (`B'`) |
| `c5_control.py` | line, `f ≡ 0` vs 1-Lipschitz known part, all ties and starts, exact `N_point` | 2 × ≈3000 instances, `|X| ≤ 11` | `f ≡ 0`: `K ≤ 2.5 N_point`; known part: `K/N_point` up to 9 |
| `c3_dp.py` | C3: own `BF*`; competitors: fixed priority (3), worst-first, upper-first, mid-first, other start, reversed ties, random linear score, instance-tailored (minimum certificates in several orders) | 1800 instances (mean `K` = 4.0), 25 534 (instance, competitor) pairs | construction of the proof succeeds in all 5489 cases where the competitor skips a `BF*` point (2454 times case `j ≥ 2`); competitor's set a proper subset of `BF*`'s in 1065 cases; `BF*` minimum in 88–91 %; 1000 further instances with two earlier, easier generators: 5259 more constructions, all successful (not reproducible from the final script) |
| `c7_chain.py` | C7 | Ising `n = 2..12`, 6 `(J,h)`; 300 chains, `n ≤ 7` | `c*(n) = 2h` always; `c*(n) ≥ c*` in 1800/1800, equality whenever `n` is a multiple of the optimal cycle length (1507/1507); 5400 certificate checks agree |
| `c68_spot.py` | C3 examples, C6, C8, §2.5 identities | 400 / 4514 / 300 checks | all hold; C6 "iff" fails in 183/400 |
| `c2_astar.py` | C2; remark 6 | 600 digraphs; 500 instances | hold |
| `c_product.py`, `c_exponents.py` | product table, exponents | `n ≤ 14` | consistent with the report |
| `c_cc.py`, `c_cc2.py` | rule CC | 114 product instances; C5 families | see MINOR 7 |

A bug of my own (a transposed index in the check of `Λ(y) − Λ(y') ≤ β s(y',y)`) produced a
spurious failure and was fixed; the identity holds.

---

## 4. Literature

**Hetland, "Optimal metric search is equivalent to the minimum dominating set problem",
arXiv:2008.09607v1 — read in full (14 pages; my own download, same file as the author's).**
Setting: a metric space `(X,δ)` with all inter-object distances known, a query `q`; the unknowns are
`g = δ(q,·)`, constrained to extend the metric (`|g(x)−g(y)| ≤ δ(x,y) ≤ g(x)+g(y)`); cost = number of
evaluations of `g`.  For `f ≡ 0` and symmetric `d`:

| repository | in Hetland | not in Hetland |
|---|---|---|
| Theorem 11.4 / first half of 11.5 (certificates = coverings; evaluations do not combine) | **yes, for range queries**: eq. (1) and Lemma 1 (pivoting bounds, each attained by a (pseudo)metric), "no interactions between eliminations", Proposition 1 (least number of distance computations = domination number of the directed elimination graph) | accuracy `ε`; slack quasi-metric; the class `Lip(d)` (his class has the extra Katětov eliminations) |
| Theorem 11.5 proper (point / value / configuration certificates, exchange lemmas, `N_cov ≤ N_value = N_point ≤ N_cov+1`, `N_point = max(1,N_config)`) | **only fragments**: Corollary 2 (`u(x) ≤ ℓ(y)` is necessary — the configuration-certificate criterion), Lemma 2 (`k`NN optimum ≤ range optimum at the `k`NN radius), Fig. 1–2, footnote 5 ("optimal kNN with upper bounds does not map as cleanly to dominating sets") | the exchange lemma, the `+1`, the equality of the three numbers |
| Theorem 11.10 (hardness) | **yes, the same gadget**: Theorem 1 — `X = V ∪ {q}`, distance 1 on edges, 2 otherwise, `δ(q,·) ≡ 2`, radius `r < 1`; objective preserved; no approximation within `(1−ε) ln n`; 1-NN version with an extra object at distance `r < 1` (the repository's `o`).  The repository's `(f = 1` on `V`, `f(o) = 0`, `g ≡ 0)` is the same instance after moving `f` into `g` | the machine-checked "iff" |
| Theorem 11.23(a) (instance-wise deterministic optimum = smallest certificate) | **yes, informally**: Corollaries 1–2 (adversary: no method beats pivoting) and §§1, 3 ("attainable … with lucky guesses"; "you would need to determine `G`") | formal model, `ε`, value certificates |
| hub phenomenon | remark in §5 ("a pivot that is far away might eliminate an entire nearby cluster"); greedy by elimination power with an oracle | a lower bound for all algorithms (hub family), randomised bounds |
| — | — | known part, asymmetry, exponents / rate–distortion, LP and exponential-weights bounds, best-first guarantees, all of the thermal theory |

So the report's sentence in its §4 is accurate (it lists "the `+1` analysis" as *not* there); the
paraphrase in `docs/prior_art/L7` ("all of it in that case") should be weakened for Theorem 11.5.
At the time the report was written the repository did not cite Hetland; `L7` at HEAD now does.

**Dechter–Pearl (1985)** — §§4.1–4.3 and the discussion of Fig. 9 read (text layer of the PDF from
the first author's page; I downloaded it independently: same SHA-256 as the author's copy, same
extracted text).  Dominance, the four types, Theorem 8 (Fig. 5), Fig. 6a/6b,
Theorems 9–10, Corollaries 3–4 and the table entry "admissible / `A_ad`: A** is 3-optimal, no
2-optimal exists" are as the report says.  Type 3 is literally "no tie-breaking rule is strictly
dominated".  One difference: D–P note that their proof of Theorem 10 does not use admissibility of
`B`; the report's proof does use correctness of `B` (to make `B` leave `A`), correctly.

**AESA.**  Vidal (1986) was *not* read by me (the PDF I fetched under that title is
Micó–Oncina–Vidal's LAESA paper; I read its algorithm: `G[p] := max(G[p], |D[p,s] − d(x,s)|)`,
eliminate if `G[p] ≥ d*`, select `argmin G`).  Figueroa et al. (2009) §3.1 (author's copy, the
relevant lines): AESA selects by `D₁` (sum) and eliminates by `D_∞` (max); "at least two basic ways
to induce an order: `D_∞` and `D₁`".  The identification "best-first = AESA-type search with the
`D_∞` ordering" is right up to the two-sided bound.

**Goldberg–Harrelson (2005)** — author's text extraction, §2 and the landmark section: reduced
cost `ℓ_π(v,w) = ℓ(v,w) − π(v) + π(w)`, feasibility, Lemma 2.1, A* = Dijkstra on reduced costs,
landmark bounds by the triangle inequality.  Identification literal for one of the two bounds.

**Mustăţa (2009)** — automatic summary of the page hosting the paper (not the paper itself):
sequential method on a quasi-metric space, next point = maximiser of the maximal semi-Lipschitz
extension, monotone bracket `M̄_n ≤ M_f ≤ M_n`, convergence; no count of evaluations, no stopping
rule.  The report's description is accurate; the computable bracket is there.

**Novelty searches.**  One extended web search for a known additive part absorbed into an
asymmetric (quasi-metric) Lipschitz condition in certified Lipschitz optimisation: no hit (results
were the standard Piyavskii–Shubert / LIPO literature).  Abstracts of Bachoc–Cesari–Gerchinovitz
(arXiv:2102.01977) and Bouttier et al. (arXiv:2002.02390) fetched: `ℝ^d`, `f ≡ 0`, packing numbers
and an integral; nothing on a known part or asymmetry.  **The session's web-search budget was then
exhausted** (my fourth query was refused), so I could not search for a Dechter–Pearl-type statement
in Lipschitz optimisation, nor re-verify Hansen–Jaumard–Lu's `4n_B+1`, Eckerle/Chen et al., Bauer et
al.; those rest on the report and on my memory.  From memory (not re-verified): gap-proportional
packing in a general metric space is the mechanism of the zooming dimension (Kleinberg–Slivkins–
Upfal), which should be cited next to Bouttier/Bachoc for the `f ≡ 0` case of C4.

**Novelty, honestly.**  C1: ingredients standard; the statement for certification (value
certificates = point certificates of the regularised instance; centre form; known part = gradient
asymmetry) apparently new; depth low, expository value high.  C4: new as stated; a routine
adaptation of a known packing argument; real content = `κ`-free bound for `f ≡ 0` that supersedes
11.11 for `κ ≥ 1/3`.  C5: new examples.  C3: a correct transfer of a weak notion.  C2, C6–C8,
§2.5: known or routine, as tagged.  The most valuable item for the repository is the prior art.

---

## 5. Not checked

* The best-first table on `{0,1}ⁿ` for `n ≥ 16`, the greedy covers, the layer lower bounds, and the
  values for `ρ = 1/4, 3/4`.
* The exploratory tables for rule CC beyond the light replication (hub family, line, grid, random
  metric spaces, alternation).
* Statistics quoted from `t1`–`t13` that depend on the author's instance distribution (66 % forced,
  15 % proper sub-certificates, 897 of 1200, 251 equalities).
* C6(iv) (shortest cycle through the data node in `D_A`), the Kantorovich LP identity (derived by
  hand only), the tight-span paragraph and its citations (Develin–Sturmfels, Hirai–Koichi,
  Willerton), the weak-KAM vocabulary (Zavidovique, Garibaldi–Thieullen, Akian–Gaubert–Walsh).
* Vidal (1986), Hansen–Jaumard–Lu (1991), the bidirectional-search papers, Bauer et al., Mérő,
  Felner et al.: not read.
* C7 for chains with more than 3 states or `n > 7` (Ising up to `n = 12`); open chains.
* Whether a family exists that defeats *every* instance-independent starting rule on the line
  (`B'` defeats the σ-centre rule; from the hub all three families are easy).
* Lean: I type-checked the author's file and printed its axioms; I formalised only the two
  counter-statements of MAJOR 2 (`RefereeC.lean`), nothing else.
