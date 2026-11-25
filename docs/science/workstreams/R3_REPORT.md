# Workstream R3 — adversarial referee report on `docs/science/INFERENCE_LIMITS.md` (version 2)

*Referee: workstream R3 of the science division.  Object: the coordinator's note (version 2,
checkpoint 2), its scripts in `experiments/science/pi_inference/` and `pi_chain/`, and the two
collaboration files that summarise it (`SCI-MSG-0001.md` §4, `SCIENCE_TO_ALL.md` digest item 2).
All of my code and outputs: `experiments/science/ws_R3/` (`NOTES.md` is the running log).
Nothing outside that directory and this file was written.*

Labels as in `COMMON.md`: **[V]** machine-checked · **[P]** paper proof (here: *mine* unless said
otherwise — written in one session, **not read by anyone else**) · **[K]** known, with reading
level · **[N]** numerical only · **[C]** conjecture · **[H]** heuristic.  "Reviewed" = I re-derived
the statement independently; "replicated" = I re-computed it with my own code.  My own code was
written before I opened the author's scripts (one exception, stated in §5: the definitions of the
"compact decile" and of the "full histogram").

---

## 1. Verdicts in one paragraph

**No numbered statement of the note is false, and I could not break any proof.**  Lemma 1, the
BCH bound `|C| ≤ (2n)^{⌈k/2⌉}` (all `n ≤ 31`, all `k ≤ n`, exact), Theorems 2, 3, 4, 5, 7, 8,
Propositions 6 and 9 and the three certificate formats of §8 are **proved** as stated; every
number I tried to reproduce (Theorem 2 on two new codes, Theorem 3 with an exact linear programme,
Proposition 5b, all of §9, §11.1, §11.2 and two rows of §11.4) **reproduces**.  The defects are of
three other kinds.  (i) **Sentences that say more than the theorems**: the summary table of §0 and
four "Reading"/bold sentences overstate quantifiers, scope or physics (Major findings M1–M7; two of
them are false sentences, not just loose ones); the same overstatements were exported to
`SCI-MSG-0001` and `SCIENCE_TO_ALL`.  (ii) **One headline rests on a numerical root**
(Proposition 5b) and one natural completion is left as a conjecture (`θ_na` with the marginal
oracle): both can be proved in a page each, and I give the proofs (§4, R5 and R6) — with them
the note's central observation becomes a theorem about *the class*, not about one instance.
(iii) **Several statements are weaker than what the same three lines prove**: Theorem 7 holds with
`tanh(βω/4)` in place of `βω/4` and is then sharp at every `βω` (R1); the entropy price
`⌈k/2⌉ ln(2n)` of Theorem 2 is `⌊k/2⌋ ln n + O_k(1)` and that is *sharp* within mixtures of
polarised basins (R2, R3); Theorem 3 is one dual point of an elementary linear programme whose
exact value I computed — the bound is asymptotically exact among all measures, poor near `n/2`.
**Originality, honestly:** Lemma 1, Theorem 2(a,b), Theorem 3, Theorem 5, Propositions 6 and 9 and
§8 are textbook facts in other words (orthogonal arrays / gauge invariance; noisy codewords;
Rao's bound and the moment method under `k`-wise independence; Gibbs–Bogoliubov; I-projection;
thermodynamic integration; LP duality and Donsker–Varadhan).  Short and, as far as I can judge
without workstream M, not written down in this form: Theorem 4 (symmetrised alternatives against a
marginal oracle), Proposition 5b (hidden twins), Theorem 7 (the cancellation of the feature
part), the reading of the limit shape as an identified set.  **The single theorem I would prove
next** is the *oracle-invariance theorem* of §9: on the cube class neither exponent of the theory
division (`θ_na`, `θ_hint`) is changed by a free exact oracle for all `k`-body marginals,
`k = o(n/ln n)`, and at bounded accuracy the adaptive exponent is unchanged even when the exact
mean residual energy is given as well.

### Verdict table

| statement | verdict | reviewed | replicated | remarks |
|---|---|---|---|---|
| Lemma 1 | **proved** | yes | yes (Fourier, all subsets, 3 codes) | textbook |
| "Codes": `|C| ≤ (2n)^{⌈k/2⌉}` | **proved**; weaker than available for odd `k` | yes | yes, exact dual distances, `n ≤ 31`, all `k` | R3: `2(2n)^{⌊k/2⌋}` |
| Theorem 2 (a)–(e) | **proved**; (e) can be vacuous; price not optimal | yes | yes: `[15,8,4]` (`k=4`), Golay (`k=7`), `[31,10,12]` (`k=4`, see §5) | M1, R2, R4 |
| Theorem 3 | **proved**; the "Reading" after it contains a false sentence | yes | yes + exact LP optimum | M2, m1, m2 |
| Theorem 4 | **proved** | yes | ingredients, exact, 3 codes | m3; R5 completes it |
| Theorem 5 + Corollary | **proved** (inequalities [K]) | yes | yes | m4 |
| Proposition 5b | **proved with a gap** in the note (root is [N]); **proved** with §4 R6; scope narrower than the summary says | yes | yes (numbers reproduced) | M3 |
| Proposition 6 | **proved** [K] | yes | — | m9, m13 |
| Theorem 7 (i)–(v) | **proved**; **weaker than advertised as "sharp"** — sharp form in R1 | yes | yes + adversarial | m5 |
| §7 example | correct, but it is the one case with a closed form | yes | by hand | m8 |
| §8 three formats | **proved** (signs of the flow inequality re-derived from Farkas: correct) | yes | third format used in §9/§11.4 replication | — |
| Theorem 8 (a)–(c) | **proved** | yes | yes (all of the §9 table) | M7, m10 |
| Proposition 9 | **proved** [K]; physical reading overstated | yes | — | M5 |
| §11.1, §11.2, §11.4 numbers | **reproduced** | — | 27 + 22 + 16 numbers | m12 |
| §11.3 | **proved for bridges at interior points**; the bold sentence is **weaker than advertised** | yes | — | M4 |

---

## 2. Statement-by-statement review

Notation: `σ = σ(b) = 1/(1+e^{−b})`, `τ = tanh(b/2) = 2σ − 1`, `κ = 1/cosh(b/2) = 2√(σ(1−σ))`,
`t = ⌊k/2⌋`, `h` the binary entropy in nats, `B(n,r)` a closed Hamming ball.

### Lemma 1 and the "Codes" paragraph — proved

Re-derived before reading the proof: a `C`-invariant measure is a mixture of uniform measures on
cosets; `π_S : C → F₂^S` is onto iff no non-zero dual word is supported in `S`.  The proof in the
note is complete.  For the codes: the dual of a punctured code is the *shortened* dual, a subcode
of `C^⊥`, so the dual distance survives restriction to **any** coordinate subset (the note's
"a marginal of a marginal" says the same); `2^m ≤ 2n` for `m = ⌈log₂(n+1)⌉`; in the degenerate
case `2t+1 > 2^m − 1` the BCH code is `{0}`, `C = F₂^{n′}`, and `2^{n′} ≤ 2^{mt}` still holds; `k`
odd gives dual distance `≥ k + 2`.  **Replicated exactly** (`r3_codes.py`): for every `n ≤ 31`,
every `0 ≤ k ≤ n`, and two coordinate choices (the first `n`; a random `n`-subset), the punctured
dual-BCH code has dual distance `> k` (brute force or MacWilliams, integers) and
`|C| ≤ (2n)^{⌈k/2⌉}`; 0 failures; the bound is attained with equality when `n = 2^{m−1}`.
Two remarks: (1) the bound is a factor `≈ n` from optimal for odd `k` (finding m1, statement R3);
(2) puncturing can destroy the *minimum* distance of `C` itself — the simplex code `[15,4,8]`
restricted to 8 well-chosen coordinates contains a word of weight 1.  The note never uses
`d_min(C)`, so nothing breaks; but any sharpening that wants the basins of `ν_{C,b}` to be
distinguishable (R2, R5) must choose the coordinates, or the code, with care.

### Theorem 2 (invisible order) — proved; three caveats

(a) cone + convexity: correct.  (b) `P_a(x + a′) = P_{a+a′}(x)`: correct.  (c) mixture bound:
correct.  (d) `H(x_i | x_{<i}) ≥ H(x_i | x_{−i}) ≥ h(σ(b))`: correct, and equality forces every
conditional odds to be `e^{±b}`.  (e) `ν_{C,b′}` **is** in the class of constant `b` for `b′ ≤ b`
(the cone is monotone in `b`), `b′ ↦ S(ν_{C,b′})` is continuous, so the intermediate-value
argument is sound.

*Replication* (`r3_thm2.py`, exact): on the dual of BCH(15, `t=2`) (`[15,8,4]`, `k = 4`) and on the
extended Golay code (`[24,12,8]`, self-dual, `k = 7`) I evaluated `ν_{C,b}` on every coset by direct
summation over the code, expanded it to the whole cube (`2^{24}` points for Golay), checked it at
300 random points against direct summation (`10^{−15}`), took a full Walsh–Hadamard transform and
read off **every** Fourier coefficient: orders `1…k` are zero, order `k+1` equals `τ^{k+1}` for the
mixture (Golay, `b = 2`: `0.113`); all single-flip ratios are `≤ e^b`; entropies lie between the
two ends of (c); the path of (e) is monotone.  The same for the author's variant
`∝ e^{−b·d_H(x,C)}`.  (d) on 3 200 random members of the class and by adversarial descent
(`n = 4`): minimum of `S − n·h(σ(b))` is `−3·10^{−15}`.

*Caveat 1 (quantifier; finding M1).*  The theorem is about ensembles whose `k`-body marginals are
**uniform**.  It does not say that `k`-body data never identify the entropy: if the one-body
marginals are `P(x_i = a_i) = σ(b)`, the ensemble is `P_a` and the entropy is known exactly (the
note itself uses this fact in the "Reading" after Proposition 5b).

*Caveat 2 (when is there any hidden order?).*  The statement has content only if
`n·(ln 2 − h(σ(b))) > ln|C|`; otherwise the upper end of (c) exceeds `n ln 2` and (e) is an empty
interval.  This is not a remote corner.  Golay, `b = 1`: `S(ν) = 16.6341`, `n ln 2 = 16.6355` — the
"ordered" ensemble is uniform to `0.0014` nats, and the upper end of (c) is `22.29`.  Golay, `b = 2`:
upper end `17.09 > 16.64`.  By the same arithmetic **9 of the author's 16 numerical cases** (`b = 0.5`
and `b = 1` on all four codes; `b = 2` on `RM(1,3)`) test an inequality that is implied by
`S ≤ n ln 2`.  For `b = 2` and `k = 7` the per-site reading "`0.365` against `0.693` nats" needs
`n ≫ 4 ln(2n)/0.328`, i.e. `n` in the hundreds.

*Caveat 3 (the price is not `⌈k/2⌉ ln(2n)`).*  For odd `k` the extended BCH dual gives
`ln|C| ≤ ⌊k/2⌋ ln(2n) + ln 2` (R3), and within mixtures `Σ_a π(a) P_a` a matching lower bound
`⌊k/2⌋ ln n − ln ⌊k/2⌋! − o(1)` holds (R2).  So the honest form of the result is two-sided:
*hiding maximally polarised basins from `k`-body data costs `⌊k/2⌋ ln n + O_k(1)` nats of
entropy — no less, no more.*  Whether the lower bound holds in the whole class is open (§8).

*Minor.*  The numerical check in the note is for the variant `e^{−b·d_H(x,C)}`, for which the
upper end of (c) is not proved in the note (the mixture bound does not apply to it).  It is true;
proof in R4.

### Theorem 3 (basin bound) — proved; the reading after it is wrong in one sentence

Re-derived: `f = Σ_{|T|≤t} χ_T(a)χ_T` is the reproducing kernel of the polynomials of degree `≤ t`
at `a`; `E_μ f² = M_t` because `f²` has degree `2t ≤ k`; Markov.  The hypothesis "`F_t > 0` on
`[0,r]`" is not needed for the inequality (it holds with `min_{d≤r} F_t(d)²`, possibly `0`), only
for its usefulness; `F_t(d) = K_t^{(n−1)}(d−1)`, so positivity means "below the first root of a
Krawtchouk polynomial", i.e. `r < n/2 − O(√(tn))` (first non-positive radius at `n = 100`:
`46, 42, 39` for `t = 2, 3, 4`).  The asymptotic claim is correct (`n = 10²…10⁵`: the ratio of the
bound to `t!/(n^t(1−2ρ)^{2t})` tends to 1), but slowly near `ρ = ½`: `t = 2`, `ρ = 0.45`: `20.9` at
`n = 100`, `1.18` at `n = 1000`.

*Where the theorem sits* **[P for the reduction; N for the numbers]**.  For a fixed centre the
largest value of `μ(B(a,r))` over **all** measures with uniform `k`-body marginals is the value
of a linear programme in the distance distribution `p_d = μ(d_H(x,a) = d)`:
`max Σ_{d≤r} p_d` subject to `Σ_d p_d K_j(d) = 0` (`1 ≤ j ≤ k`), `Σ p_d = 1`, `p ≥ 0` (symmetrise `μ`
over the permutations of coordinates and the constraints become these `k` equations).  Theorem 3
is the dual-feasible point `F_t²/min F_t²`.  I solved the programme (`r3_thm3.py`):

* *attained ≤ LP ≤ bound* in every row, for `[15,8,4]` (`k=4`), Golay (`k=7`), `[31,10,12]`
  (`k=4`), `[31,15,8]` (`k=6`), `RM(1,5)` (`k=3`), radii `0…n/2`; for `[15,8,4]` and Golay the
  inequality was also checked for `Unif(C)` at **all** centres (every coset) and all radii;
* LP/bound `→ 1` as `n` grows at fixed `ρ` (`n = 400`: `0.9975`, `0.9950`, `0.9944` for `t = 1, 2, 3`
  at `ρ = 0`; `0.993`, `0.985`, `0.977` at `ρ = 0.3`): **among all measures the bound is
  asymptotically exact, constant `t!` included** — it is the Christoffel-function bound for the
  binomial weight;
* near the first root it is poor, and the plain `2t`-th moment bound is better there (Golay,
  `r = 8`: Theorem 3 gives `5.27`, the moment bound `0.727`, the exact optimum is `0.186`);
* for odd `k` the right point bound is Rao's odd-strength bound `1/(2M_t(n−1))`, not `1/M_t`
  (Golay: optimum `1/4096`, attained; Theorem 3: `1/2325`).

*The "Attainment" paragraph.*  `ν_{C,b}(B(a,ρn)) ≥ |C|^{−1}·P(Bin(n, 1−σ) ≤ ρn) = (1−o(1))/|C|` is
right for `1 − σ(b) < ρ < ½` (fixed `b`, `ρ`; `n → ∞`); without a class it holds for every `ρ ≥ 0`
with `Unif(C)`.  "Attained up to constants" is then right for **even** `k` with the note's code and
false for odd `k` with the note's code (gap `≈ n`); it becomes right for odd `k` with the
extended code (m1).  The author's check covers `t = 1` only (three codes, three centres per
measure); `t = 2, 3` are covered by mine.

*The false sentence (finding M2).*  "Populations of individual states are identified up to
polynomial factors" does not follow and is not true: the theorem bounds the population of a
basin from *above* by `≈ n^{−t}`; from below nothing better than `≈ 2^{−n}|B|` holds (the uniform
ensemble has uniform marginals).  The identified interval of a basin population spans
exponentially many orders of magnitude; only its *upper end* is known up to constants.

### Theorem 4 (marginal oracle) — proved

Re-derived independently.  Points the brief asked about:

* *Correctness is used only on the class*: the run at `g ≡ 0` is compared with the runs at
  `g_a^C`, all members of the class.  
* *"The oracle's answers at `g ≡ 0`"* are well defined for randomised adaptive algorithms: the
  answer is a deterministic function of `g` (the marginals of `μ_g`), identical for `0` and every
  `g_a^C`; for a fixed seed the two runs coincide until a query enters `U_a`.  Tolerances on the
  marginals leave exact answers admissible, so the bound survives ("only help the adversary":
  correct).
* *Zero known part is essential* (`μ_{g_a^C}` must be `C`-invariant); the note says so.
* *Reading of the theory report.*  Theorem 11.54 gives the adaptive worst-case exponent
  `θ_hint(ε₁)` at extensive accuracies `0 < ε₁ < ln cosh(u/2)`; Theorem 11.58 gives `h = θ_hint(0+)`
  at every fixed accuracy and for `ε_n = o(n)` with `ln(1/ε_n) = o(n)`.  For `ε = e^{−λn}` the adaptive
  exponent without a hint is open in the theory report.  So "θ_hint … is the worst-case exponent of
  adaptive algorithms" is a correct reading **for accuracies with `ln(1/ε) = o(n)`**, and the
  conclusion "the worst-case adaptive exponent is the same with and without the oracle" is then a
  complete statement: lower bound by Theorem 4 at `g ≡ 0`, upper bound by ignoring the oracle.  Two
  things should be said in the note: the regime, and that Theorem 11.54 is a paper proof whose own
  referee's verdict was "proved with gaps" (theory report §11.18, status paragraph).  (m3)
* *Convention.*  The note's "within `ε`" with "`> 2ε`" is the theory report's width `ε_th = 2ε`.  At
  extensive accuracy the argument of `θ_hint` is therefore `2ε/n` in the note's `ε`.  (m3)

*Replication of the ingredients* (`r3_extensions.py`, part C; exact): on simplex `[15,4,8]` (`k=2`),
`[15,8,4]` (`k=4`) and Golay (`k=7`), `u = 1.5`, `r = 2, 3, 4`: `g_a^C` is in the class (largest flip
ratio `= e^u`), all Fourier coefficients of `μ_{g_a^C}` of order `1…k` vanish and those of order
`k+1` do not, `|U_a| ≤ |C|·V(n,r)`, `ln Z(g_a^C) ≥ ln Z(g_a)`.

*What is missing* is the non-adaptive exponent (the note's remark (i), a conjecture there).  It
is a theorem: R5.  A small strengthening for free: with Gilbert–Varshamov codes Theorem 4 holds
for `k = κn` with `|C| ≤ 4e^{n·h(κ)}`, so the exponential cost at the zero residual survives
marginals of *extensive* order as long as `h(κ) < θ_hint` (and the method cannot go beyond
`h(κ/2) ≥ θ_hint`, by Rao's bound).

### Theorem 5 and its Corollary — proved

Both Jensen steps, the identity `width = KL(μ₀‖μ_g) + KL(μ_g‖μ₀)` and the McDiarmid constant
(`Σ_i c_i²/N` for the mean of `N` samples; one-sided) are correct; `N = n b² ln(1/δ)/(2ε²)` follows.
Replicated on 450 random class members (`n = 10`): no violation, `|width − J| < 4·10^{−14}`, empirical
failure rate of the sampled lower end `10^{−4}` at `δ = 0.1` (`r3_thm5.py`).

*What "certify" means* (m4).  The bracket is a `(1−δ)`-confidence statement that is valid at
**every** `g`; its width is instance dependent.  To compare with the theory division's lower
bound — which is about algorithms that are correct on the whole class — the algorithm must be
completed: *compute the bracket; if its width is at most `ε`, return the midpoint; otherwise fall
back on any class-correct procedure.*  This is `(ε/2, δ)`-correct on the class and costs exactly
`N` at `g ≡ 0` (all samples are `0`, `U = 0`, the width is `ε` deterministically).  With that
sentence the Corollary is a correct comparison.  Two further remarks: at an extensive accuracy
`N < 1`, i.e. **one** evaluation suffices (`n = 1000`, `b = 1`, `ε = 0.05n`: `N = 0.46`); and the
positive result is robust to a tolerance `τ_U` on the datum (the bracket widens by `βτ_U`), whereas
the *negative* result of Proposition 5b needs an exactly matched twin only because the oracle is
assumed exact.

### Proposition 5b (hidden twins) — mechanism correct; root [N] in the note; proved in §4 (R6); scope overstated in §0

* The construction is legitimate: `g′ = min(g₀, twin)` is in the class; the adversary **may** tune
  `s` per centre (the alternatives are just a family of class members, each with the same oracle
  answer as `g₀`); exact equality of the mean energies **is** needed for an exact oracle.
* *Replication* (`r3_prop5b.py`; own exact sums over the joint law of the two distances, in the
  log domain, with the cancellation-free identity of R6).  With the integer radius
  `r₁ = round(ρ₁n)` that the author's script uses: `n = 1000`, `ρ₁ = ρ₀ + 0.01`: `s* = −0.00490`,
  `ln Z′ − ln Z₀ = 0.6907`, for hidden centres at `0.3n`, `0.45n`, `0.5n` alike; `n = 5000`,
  `ρ₁ = ρ₀ + 0.002`: `s* = −0.0393`, `0.6737`; equal mean energies to `10^{−16}` relative.  These are
  the note's numbers.  (With the real radius `r₁ = ρ₁n` that the text of the note writes:
  `−0.00549` and `−0.0256`.)  `s ↦ U′(s) − U₀` is monotone on an 81-point grid: the root is unique.
* *Small inaccuracies.*  "Cost exponent `0.0281`" is the asymptotic `ln 2 − h(ρ₁)`; the finite-`n`
  value `ln 2 − n^{−1} ln V(n, r₁+1)` is `0.0289`.  "When the visible basin does not dominate
  (`ln B₀ ≲ 2`) there is no root" is not the right criterion: at `ρ₁ = ρ₀ + 0.01` there is no root
  for `n ≤ 300` (`ln B₀ = 3.0`) and one from `n = 400` (`ln B₀ = 4.0`); the root exists roughly when
  `B₀ ≳ |U₀|/c`, i.e. `ln B₀ ≳ ln n`.  "Exact arithmetic" in the status label is floating-point
  log-sum-exp, not rational arithmetic.
* *Scope* (finding M3).  The twin changes `ln Z` by `≈ ln 2`, so the lower bound holds for
  accuracies `ε < ½ ln 2` (note's convention) only.  The proposition says "at bounded accuracy";
  the summary table of §0 says "the worst-case exponent is unchanged" without qualification.  At
  extensive accuracy twins of equal depth give `ln 2 − h(ρ₀) − ε₁`, strictly below `θ_hint(ε₁)`, and
  whether the datum lowers the exponent there is open (the note lists it as open in the text).
* *The root can be proved*, for every `u > 0`, with explicit sufficient conditions: R6.  For
  `u > u₀ = 2.4375` (where `ρ₀ < ¼`) the twins can be taken disjoint and the proof is five lines.

### Proposition 6 — proved [K]

Correct, including the caveat on the constant function.  "Determined" is information-theoretic
(solving the maximum-entropy problem costs partition functions), and the count of data is the
same as the count of evaluations it replaces (`K` expectations for rank-many evaluations — the
theory report's statement is Theorem 11.47(c), not a "Proposition").  On the scattering paragraph
see m9.

### Theorem 7 — proved; not sharp; sharp form in R1

Existence and form of the I-projection: the linear family contains `μ`, which has full support,
so the I-projection of `μ₀` has the exponential form (Csiszár 1975 **[K: from memory]**; on a
finite space it is elementary convex duality).  (i) correct; the use of Pinsker is correct;
(ii)–(iv) follow; (v) is the Pythagorean identity and is correct.  Replicated on 4 000 random
instances (`|X| < 40`, `≤ 6` features): identity (i) and (v) to `3·10^{−9}`, largest
`TV/(βω/4) = 0.99994`.

"Sharp to first order" is all that can be said for `βω/4`: the bound exceeds 1 for `βω ≥ 4`.
Replacing Pinsker by the sharp inequality between the symmetrised divergence and the total
variation gives `TV ≤ tanh(βω/4)`, with equality at **every** `βω` (R1); an adversarial search over
`(μ₀, Φ, r)` with up to 5 points and 2 features reaches `tanh(βω/4)` to six digits and never
exceeds it (`βω = 0.5, 2, 4, 8`: `0.124353`, `0.462117`, `0.761594`, `0.964028`).

### §7 — correct, but the example is the easy case

The three-point example is right.  It has `B = {y}`, and for a single state `y` the robust
maximum of `Z_g(A)/Z_g(y)` **does** have a closed form of the kind of Theorem 11.12:
`g = −d(y,·)` is admissible and minimises every `g(x) − g(y)` simultaneously, so the maximum is
`Σ_{x∈A} e^{−β(f(x) − f(y) − d(y,x))}`.  The example therefore shows that the extremal residual is not
constant on `A` (nobody should expect it to be) and does not show where the difficulty is, which
is `|A|, |B| ≥ 2`.  (m8)

### §8 — proved (soundness), signs correct

Model-free format: one line, correct; equality is LP duality.  Divergence ball: Donsker–Varadhan,
correct.  Envelope class: I re-derived the certificate from Farkas' lemma for the homogeneous
system in `w = e^{−βg} ≥ 0`: constraints `w(y) − κ(x,y)w(x) ≤ 0` with multipliers `F(x,y) ≥ 0`, data
constraints with `λ^± ≥ 0`; the coefficient of `w(z)` in `Σ F(x,y)(w(y) − κ(x,y)w(x))` is
`Σ_x F(x,z) − Σ_y κ(z,y)F(z,y)`.  **The inequality in the note has the right orientation and the
right sign of `Λ`.**  The format is also complete (LP duality for the Charnes–Cooper form), which
the note does not claim.

### §9, Theorem 8 — proved; numbers reproduced

(a) definition.  (b) Donsker–Varadhan and `−λ·m ≥ −h_D(λ)`: correct.  (c) is §8 with `ψ ≡ 1`,
`t = 0`: correct; `b_min(D) > b` (strict) holds because the infimum is attained on a finite space.
The whole table is reproduced (§5): all 12 thresholds within `10^{−3}`, with two formulations.
Three remarks.  (1) **Only (b) has a certificate the kernels can check** (two partition-function
bounds, for pairwise `f`, `Φ`); the certificate of (c) is one inequality per configuration and a
flow on pairs of configurations, for which the note itself lists the structured families as
open.  The summary table says "kernel-checkable" for both.  (M7)  (2) `b_min` depends on what an
elementary move is: with the two gauche states labelled by absolute bond index instead of by
the sign of the dihedral (my first, wrong, labelling) the profile column comes out
`0.215/0.425/0.835` instead of `0.220/0.438/0.866`.  The note should say "per torsion-angle state
`(t, g⁺, g⁻)`".  (m10)  (3) "The certified bound tracks the typical strength" rests on two sizes
and one family of truths **[N]**.

### §10, Proposition 9 — proved [K]; the bold sentence is physics that outruns the mathematics

Monotonicity, the two Riemann sums and the width are correct.  The reading is not (finding M5):
the proposition integrates from `β₀ = 0`, where `Z = |X|`; no experiment reaches infinite
temperature on a fixed configuration space, and absolute entropies are measured the other way —
from `T → 0` with the third law.  A calorimeter measures the energy of all degrees of freedom
(kinetic, vibrational, solvent), not `E_μ(f+g)` on the model's `X`.  And Theorem 11.35 of the
theory report, quoted for "populations, contact probabilities, subsystem entropies", is a
statement about one observable, the mean magnetisation on the cube (m11).

### §11 — numbers reproduced; §11.3 overstated in bold

§11.1: all 27 entries reproduced.  §11.2: all 22 interval ends reproduced from the engineering
tables with a different (dual) linear programme.  §11.4: the gauche-fraction and `R²` rows
reproduced.  Class tables: my enumerator agrees with the engineering tables for `n = 1…9`.

§11.3 **[P, reviewed]**.  The convex hull is 1-Lipschitz for the Hausdorff distance, so the hulls
of `𝒟_N^{br}` converge to `K^{br}`; for convex bodies Hausdorff convergence gives uniform convergence
of the lower and upper boundary functions on compact subsets of the **interior** of the
projection (epi-convergence of convex functions), hence convergence of the chords there.  So the
statement is right **for bridges, at interior points of `𝒦`, provided `𝒦` has interior points in
`ℝ³`** (the theory report proves a triangle of inner points and one further point; it calls `𝒦` a
"body" and bounds its volume from below only conditionally — the note should cite what it
uses).  The identification with a mean-parameter set (marginal polytope of the exponential
family generated by `(h, g)`, normalised) and of the support function with a ground-state energy
density is correct.  What is not right is the bold sentence (M4): the numbers of §11.2 are for
**all walks**, the limit theorem is for **bridges**, and equality of the two limits is Conjecture
11.75.  What *is* unconditional is one inclusion, and it is the one the note needs: bridges are
walks, so the identified interval for walks contains that for bridges, and its lower limit
contains the chord `[γ(p), γ⁺(p)]` of `K^{br}`.

---
## 3. Findings

**Critical: none.**  No numbered statement is false; no proof has a hole that I could not close.

### Major

**M1 — §0 table, row 1; title of §2; `SCI-MSG-0001` "Why it matters".**  *What is wrong:* "I2(`Φ_k`)
certifies nothing about the entropy beyond the a-priori range of the class" and "Entropy is not
identified by local ensemble data in a first-order class" are universal statements; Theorem 2 is
existential (it concerns the single data vector "all `k`-body marginals uniform") and is
asymptotic (empty unless `n(ln 2 − h(σ(b))) > ln|C|`; see Caveat 2 above: 9 of the 16 numerical
cases are in the empty regime).  For other data the entropy can be identified exactly (one-body
marginals `σ(b)`).  *Why it matters:* the table is what the other divisions will quote.
*Correction:* §7, N1.

**M2 — "Reading" after Theorem 3; `SCI-MSG-0001` §4, "Two complements".**  *What is wrong:*
"Populations of individual states are identified up to polynomial factors" is false; only the
*upper end* of the identified interval of a basin population is `≈ n^{−⌊k/2⌋}` up to constants; the
lower end is exponentially small.  *Why it matters:* it reverses the message — the data do not
identify populations at all, they exclude dominance.  *Correction:* §7, N3 and S2.

**M3 — §0 table, row "I1 + I3"; Proposition 5b.**  *What is wrong:* (a) the table says "the
worst-case exponent is unchanged"; what is shown is a lower bound `ln 2 − h(ρ₀)` at **bounded**
accuracy `ε < ½ ln 2`; at extensive accuracy the question is open (and equal-depth twins fall
short of `θ_hint(ε₁)`).  (b) the bound rests on a root that is only numerical.  (c) the criterion
"`ln B₀ ≲ 2`" for the absence of a root is wrong (it is `B₀ ≲ |U₀|/c`), and the status label says
"exact arithmetic" for floating-point sums.  *Why it matters:* a bold headline with an [N] step.
*Correction:* the root is a theorem (R6) — replace the status by [P] after checking R6, and
restrict the table entry to bounded accuracy (§7, N2, N5).

**M4 — §11.3, bold sentence and header "[P, given theory report Theorem 11.69]".**  *What is
wrong:* "The limit shape of §11.22 is the asymptotic model-free identified set" is proved for the
ensemble of **bridges**, at **interior** profile densities; for the chains of §11.1–11.2 (all
walks) it is Conjecture 11.75; the caveat comes two sentences after the bold claim and not at
all in the header.  *Why it matters:* the 27-bead numbers are compared with an object that is
theirs only conjecturally.  *Correction:* state the unconditional inclusion (§7, N7).

**M5 — §10, bold sentence.**  *What is wrong:* "the total `ln Z` is the one quantity of the
programme that experiment delivers without any model" is not supported by Proposition 9: the
proposition needs the caloric curve from `β = 0` on the model's own configuration space; "this is
how absolute entropies are measured" is not so (third law, from `T → 0`); a calorimetric energy
is not `E_μ(f+g)`.  *Why it matters:* it is a physical claim, in bold, with a [K] label.
*Correction:* relabel [H] and reword (§7, N6).

**M6 — `SCI-MSG-0001` §4 heading and "Why it matters"; `SCIENCE_TO_ALL` digest 2(b), 2(c).**
*What is wrong:* "local ensemble-averaged data are worth at most a polynomial factor in a
first-order class" and "In a first-order class, neither energy evaluations … nor any bounded
order of local ensemble-averaged data … certify a free energy or an entropy at sub-exponential
cost" are stated for first-order classes in general; the theorem is for the **cube with zero
known part**, the factor is polynomial **at the zero residual** (in the worst case over instances
only "the same exponent" is known — the theory division's upper bound has an unquantified
`e^{o(n)}`), and on other instances the oracle is worth an exponential factor to a non-adaptive
algorithm (cones: the one-body marginals reveal the centre, and then one evaluation suffices).
"Local experimental data" identifies `k`-site marginals of an abstract cube with measurements;
for a chain, pair distances are not `k`-local in the torsions (the note's own §12).  2(c) omits
the hypothesis "when the marginals are uniform".  *Correction:* §7, S1–S4.

**M7 — §0 table, row "I2(Φ) + model + envelope class".**  *What is wrong:* "kernel-checkable"
applies to the lower bound on `KL(truth‖model)` (Theorem 8(b)) only; the lower bound on the
envelope constant (Theorem 8(c)) has a certificate with one inequality per configuration and no
structured family of flows is known (§8, "Open").  *Correction:* §7, N4.

**M8 — §4, "Not proved here (i)"; `SCI-MSG-0001` §7 invitation (a).**  *What is missing:* the
non-adaptive exponent with the marginal oracle is left as a conjecture and sent to the theory
division as a question.  It follows in a few lines from the note's own symmetrisation and the
theory division's machine-checked Theorem 11.45(a) (R5).  *Why it matters:* without it the note
shows that one lower bound survives; with it, that the theory division's whole exponent diagram
for the cube is invariant under the oracle.

### Minor

**m1 — odd `k`.**  The code bound can be `2(2n)^{⌊k/2⌋}` (R3); with the note's code "attained up to
constants" (§0 table, Theorem 3) is false for odd `k`; the point bound for odd `k` is Rao's
`1/(2M_t(n−1))`.

**m2 — Theorem 3.**  Say that the hypothesis `F_t > 0` restricts `r` to `r < n/2 − O(√(tn))`, that
the exact optimum is a `(k+1)`-constraint linear programme, that the bound is asymptotically
exact among all measures and is beaten by the plain moment bound near `n/2`.  The author's check
covers `t = 1` and three centres per measure ("all centres tried" reads as "all centres").

**m3 — Theorem 4.**  State the accuracy convention (`ε_th = 2ε`), the regime in which
Theorems 11.54/11.58 apply (`ln(1/ε) = o(n)`), and the status of Theorem 11.54.

**m4 — Theorem 5, Corollary.**  State the class-correct algorithm (bracket, then fallback) and
that the confidence statement assumes an exact `U`; add the tolerance remark.

**m5 — Theorem 7.**  Replace `βω/4` by `tanh(βω/4)` and "(βω)²/4" by `βω·tanh(βω/4)`; replace
"Sharp to first order" by the extremal example of R1.

**m6 — numerical check of Theorem 2.**  It checks the variant `e^{−b·d_H(x,C)}`, for which (c) is
not proved in the note (R4 proves it), and it is vacuous in 9 of 16 cases.

**m7 — Proposition 5b,** see M3(c).

**m8 — §7.**  Say that for a single state `B = {y}` the closed form exists (`g = −d(y,·)`), and
that the open case is `|A|, |B| ≥ 2`.

**m9 — §6, scattering.**  A *small-angle* experiment gives the form-factor-weighted *total*
pair-distance distribution at a resolution `≈ π/q_max`; the contact shells of the profile class
(squared distances 3, 8, 11) are wide-angle information, and partial distributions per pair of
types need contrast variation.  "Complete scattering measurement" should be labelled [H], and
"Henderson's theorem" is an analogy (it is a statement about homogeneous fluids).

**m10 — §9.**  Define the elementary move (torsion-angle state); label the "typical strength"
sentence [N, two sizes].

**m11 — §10.**  Theorem 11.35 concerns the mean magnetisation only.

**m12 — §11.2.**  "Still widening": the increments of the width per two beads are
`0.155, 0.121, 0.059, 0.053, 0.029, 0.024, 0.027, 0.014, 0.023, 0.010` — widening, and
decelerating; say so.

**m13 — Proposition 6.**  "Zero queries" is a statement about information, not about computation.

---

## 4. Statements of the referee, with proofs

All **[P]** here are mine, written during the review and checked numerically as stated; none
has been read by a second person.

### R1.  Sharp form of Theorem 7

**Lemma.**  For probability measures `P, Q` on a finite set with `V = TV(P,Q) < 1`:
`KL(P‖Q) + KL(Q‖P) ≥ 2V·ln((1+V)/(1−V))`.

*Proof.*  `J(P,Q) = Σ (p−q) ln(p/q)` is an `f`-divergence (`f(t) = (t−1) ln t`), so it does not
increase under the map to the two-cell partition `{p > q}, {p ≤ q}`.  With `a = P(p > q)`,
`b = Q(p > q) = a − V` the two-cell value is `V·(logit a − logit(a − V))`, minimal at `a = (1+V)/2`,
where it equals `2V ln((1+V)/(1−V))`.  ∎  (Checked on `2·10⁵` random pairs: least ratio `1.000000`.)

**Theorem R1 [P].**  In the setting of Theorem 7,

    TV(μ,ν) ≤ tanh(βω/4),   KL(μ‖ν) + KL(ν‖μ) ≤ βω·tanh(βω/4),   |E_μψ − E_νψ| ≤ osc(ψ)·tanh(βω/4),

and all three are attained for every value of `βω`: two points, no feature, `r = (0, ω)`,
`μ₀ = (1, e^{βω/2})/(1 + e^{βω/2})`.

*Proof.*  By (i) of the note, `J = β(E_ν r − E_μ r) ≤ βω·V`.  With the lemma,
`ln((1+V)/(1−V)) ≤ βω/2`.  In the example `μ = (1, e^{−βω/2})/(1+e^{−βω/2})`, `ν = μ₀`,
`V = (e^{βω/2} − 1)/(e^{βω/2} + 1)`.  ∎
(Checked: `TV = tanh(βω/4)` to 10 digits at `βω = 0.1, 1, 4, 10`; never exceeded on 4 000 random
instances — largest ratio `0.99999` — nor by adversarial ascent.)  The bound is never vacuous, and
it shows where the extremal case is: no feature at all, and the model putting weight
`1/(1+e^{βω/2})` on the favoured set.

### R2.  Theorem 2 is sharp within mixtures of polarised basins

**Theorem R2 [P].**  Let `π` be any probability measure on `{0,1}ⁿ`, `Z ∼ π`, `X = Z ⊕ N` with `N`
i.i.d. Bernoulli(`1−σ(b)`), so that `X ∼ ν_π = Σ_a π(a) P_a` (for `π = Unif(C)` this is `ν_{C,b}`).
(a) `ν_π` has uniform `k`-body marginals iff `π` has (`E_{ν_π}χ_T = τ^{|T|} E_π χ_T`).
(b) `S(ν_π) = n·h(σ(b)) + I(Z;X)`, and `I(Z;X) ≥ −ln E κ^{d_H(Z,Z′)}`, `Z, Z′` i.i.d. `∼ π`,
`κ = 1/cosh(b/2)`.
(c) If `π` has uniform `k`-body marginals, then for every `r` with `F_t > 0` on `[0,r]`

    E κ^{d_H(Z,Z′)}  ≤  M_t / min_{d≤r} F_t(d)²  +  κ^{r+1},

so `S(ν_π) ≥ n·h(σ(b)) + t ln n − ln t! − o(1)` as `n → ∞` (`b`, `k` fixed, `t = ⌊k/2⌋`).
Consequently, with R3,

    min { S(ν_π) − n·h(σ(b)) : π with uniform k-body marginals }  =  ⌊k/2⌋ ln n + O_k(1).

*Proof.*  (b): for any conditional law `q(a|x)`, `I(Z;X) ≥ E ln(q(Z|X)/π(Z))` (the defect is a
relative entropy).  Take `q(a|x) ∝ π(a)√(P_a(x))`:
`I ≥ E_{a∼π} E_{x∼P_a}[−ln Σ_{a′} π(a′)√(P_{a′}(x)/P_a(x))] ≥ −E_a ln Σ_{a′} π(a′) Σ_x √(P_a P_{a′})`
(Jensen), and the Bhattacharyya coefficient of `P_a, P_{a′}` is `κ^{d_H(a,a′)}`; Jensen once more in
`a`.  (c): `κ^d ≤ 1[d ≤ r] + κ^{r+1}`, and Theorem 3 applied to `π` bounds `π(B(a,r))` for every
centre.  Take `r = ⌈(t+1) ln n / ln(1/κ)⌉`.  ∎
The inequality in (b) is the pairwise-distance bound for mixture entropies of Kolchinsky–Tracey
(2017) **[K: abstract]**; the proof above is self-contained.
*Checked* (`r3_extensions.py`, parts B, B′, B″): `Δ := S − n·h ≥ −ln E κ^{d} ≥` the bound of (c) on
three codes × three `b` and on four 4-wise uniform mixing laws that are not uniform on a code
(`n = 15`); e.g. Golay, `b = 4`: `8.3158 ≥ 8.2987 ≥ 4.93`; the bound of (c) against `t ln n − ln t!`
against the note's `t ln 2n`: `22.33 / 22.33 / 24.41` at `n = 10⁵`, `t = 2`, `b = 2`.
*Not proved:* the same lower bound for members of the class that are not mixtures of products
(e.g. `e^{−b·d_H(x,C)}`, which is not one already for `n = 2`); see §8.

### R3.  The code bound for odd `k`

**Proposition R3 [P; K for the BCH bound].**  For all `n` and `k` there is a linear code of length
`n`, dual distance `> k` and `|C| ≤ 2·(2n)^{⌊k/2⌋}`.
*Proof.*  Even `k`: the note's code.  Odd `k = 2t+1`: the extended BCH code of length `2^m`
(`m = ⌈log₂ n⌉`, designed distance `2t+1`, overall parity bit) has minimum distance `≥ 2t+2`; its
dual has at most `2·2^{mt} < 2(2n)^t` words; restrict to `n` coordinates.  ∎  (Dual distances
computed exactly for `m = 3…6`, `t = 1, 2, 3`: `4, 6 or 8, 8`.)  By Rao's bound no code can do better
than `M_{⌊k/2⌋} ≈ n^{⌊k/2⌋}/⌊k/2⌋!`.

### R4.  The variant of the numerical check satisfies (c)

**Proposition R4 [P].**  `μ ∝ e^{−b·d_H(x,C)}` has `S(μ) ≤ n·h(σ(b)) + ln|C|`.
*Proof.*  Write `λ_a(x) = 1/m(x)` if `a` is one of the `m(x)` codewords nearest to `x`, and `0`
otherwise; `μ` is the uniform mixture over `a ∈ C` of `Q_a ∝ P_a·λ_a`, so `S(μ) ≤ ln|C| + S(Q_0)`.
`λ_0` is non-increasing in the coordinatewise order (removing ones from `x` keeps `0` nearest and
can only break ties), `d_H(x,0)` is increasing, `P_0` is a product measure; by Harris' inequality
`E_{Q_0} d_H ≤ E_{P_0} d_H`, and `E_{Q_0}[−ln λ_0] + ln E_{P_0}λ_0 ≤ 0` by Jensen for `λ ln λ`.  Hence
`S(Q_0) = E_{Q_0}[−ln P_0] − E_{Q_0} ln λ_0 + ln E_{P_0}λ_0 ≤ n·h(σ(b))`.  ∎

### R5.  The non-adaptive exponent is unchanged by the marginal oracle

Conventions of the theory report (§11.16): `X = {0,1}ⁿ`, `f ≡ 0`, `u = βc`; an algorithm is
`(ε/2, δ)`-correct if its output is within `ε/2` of `ln Z` with probability `≥ 1 − δ` on every member
of the class; `D_R` is the drop of `ln Z` when the cone `c·d_H(·,a)` is flattened at radius `R`.
Call an algorithm with the marginal oracle *non-adaptive* if its set of evaluation points is a
function of the oracle's answer and of its internal randomness (not of the evaluations).

**Theorem R5 [P, given theory report Theorem 11.45(a) [V] and Theorem 11.44 [P]].**  Let `C` be a
linear code of length `n` with dual distance `> k` and
`γ := ½(|C| − 1)·cosh(u/2)^{−d_min(C)} < 1`.  For `a ∈ F₂ⁿ` and `R ≥ 1` put
`cone_a^C = c·d_H(·, a + C)`, `flat_a^C = max(cone_a^C, cR)`.
(1) Both are `C`-invariant members of the class, so all their `k`-body marginals are uniform;
they differ exactly on `U_a = {d_H(·, a+C) < R}`, and `|U_a| ≤ |C|·|B(n, R−1)|`.
(2) `ln Z(cone_a^C) − ln Z(flat_a^C) ≥ D_R + ln(1 − γ)`.
(3) Hence every non-adaptive `(ε/2, δ)`-correct algorithm with a free exact oracle for all `k`-body
marginals makes at least `(1 − 2δ)·2ⁿ/(|C|·|B(n, R−1)|)` evaluations in expectation on every
instance with uniform `k`-body marginals (in particular at `g ≡ 0`), whenever
`D_R + ln(1−γ) > ε`.
(4) For `k ln n = o(n)` there are such codes with `|C| ≤ 4n^{k+2}` and `d_min ≥ n/4` for all large
`n`.  Therefore the non-adaptive exponent with the oracle is `θ_na(ε₁)` at extensive accuracies
`0 < ε₁ < ln cosh(u/2)` and `a = KL(p_u‖½)` at accuracies with `ln(1/ε) = o(n)` — the values without
the oracle.

*Proof.*  (1) A distance to a set is 1-Lipschitz; a maximum of a member and a constant is a
member; Lemma 1.  (2) `Z(flat^C) = Σ_x max_{a′} e^{−u·max(d(x,a′),R)} ≤ |C|·Z(flat)`, and, since a
maximum is at least the sum minus the pairwise minima,
`Z(cone^C) ≥ |C|·Z(cone) − Σ_{a′<a″} Σ_x e^{−u(d(x,a′)+d(x,a″))/2}`; for two centres at distance `D`
the inner sum is `(1+e^{−u})^{n−D}(2e^{−u/2})^D = Z(cone)·cosh(u/2)^{−D}`.  (3) On the sub-class of
members with uniform `k`-body marginals the oracle's answer is constant, so the algorithm,
restricted to that sub-class, is a non-adaptive algorithm in the sense of the theory report, and
correct on it; Theorem 11.45(a) ("any class, any functional") with the pairs
`(cone_a^C, flat_a^C)`, `a ∈ F₂ⁿ`, unit weights: a point lies in `|U_0|` of the sets `U_a`.
(4) A uniformly random `K × n` generator matrix with `K = ⌈k log₂ n⌉ + 2⌈log₂ n⌉`: a fixed
non-zero vector is a dual word with probability `2^{−K}`, a fixed non-zero message gives a
uniformly random word; union bounds over `≤ (n+1)^k` light vectors and `2^K` messages.  The upper
bounds: plain Monte Carlo ignores the oracle (Theorem 11.44).  ∎
*Checked* (`r3_extensions.py`, part A; exact, on the cosets of five codes — simplex `[15,4,8]`,
`RM(1,4)`, `[15,8,4]`, Golay, `[31,10,12]` — `u = 0.5, 1, 2`, all `R` up to the covering radius `+1`):
`drop_C ≥ D_R` in every case (e.g. Golay, `u = 2`, `R = 3`: `0.853 ≥ 0.522`; `[31,10,12]`, `u = 1`,
`R = 6`: `0.416 ≥ 0.096`), and `|U_a| = |C|·|B(R−1)|` while the balls are disjoint.

### R6.  Proposition 5b is a theorem, and it survives the marginal oracle

Units `β = 1`, `c = u`.  Let `r₁ < n/2` be an integer, `g₀ = −u(r₁ − d_H(x,a₀))₊`,
`W = Σ_{d<r₁} C(n,d) e^{u(r₁−d)}`, `Z₀ = Σ e^{−g₀}`, `U₀ = E_{μ_{g₀}} g₀`.  For a centre `a′` and
`s ∈ [−1,1]` let `T_s = −u(r₁ + s − d_H(x,a′))₊`, `g′_s = min(g₀, T_s)`, `Z′_s, U′_s` its partition
function and mean energy, `ω_s = Σ_{x : g₀(x)<0, T_s(x)<0} e^{−T_s(x)}` (the weight of the twin inside
the visible basin).

**Lemma R6.1 (excess identity) [P].**  With
`E_s = Σ_x (e^{−T_s} − e^{−g₀})₊` and `D_s = Σ_{T_s<g₀} (T_s e^{−T_s} − g₀ e^{−g₀})`:
`Z′_s = Z₀ + E_s` and `U′_s − U₀ = (E_s/(Z₀+E_s))·(D_s/E_s − U₀)`.  *The twin leaves the mean
energy unchanged iff the mean energy of its excess mass equals `U₀`.*

**Lemma R6.2 (signs at the ends) [P].**  If
(i) `W ≥ 8 r₁ e^u·2ⁿ` (the visible basin dominates) and
(ii) `ω_{+1} ≤ e^{−u} W/(2(r₁+1))` (the twin hardly overlaps it),
then `U′_{+1} < U₀ < U′_{−1}`; hence there is `s* ∈ (−1,1)` with `U′_{s*} = U₀` **exactly**, and
`ln Z′_{s*} − ln Z₀ ≥ ln(1 + e^{−u}(1 − 1/r₁))`; `g′_{s*} = g₀` outside `B(a′, r₁)`.

*Proof.*  Let `A′ = −Σ g₀e^{−g₀} > 0`, `V = |B(n,r₁−1)|`; then `Z₀ = 2ⁿ + W − V`, `U₀ = −A′/Z₀`,
`uW ≤ A′ ≤ u r₁ W`.  If `g₀` were `0` the sums would be `E^f_{+1} = e^u W⁺ − |B(n,r₁)|`,
`D^f_{+1} = −e^u(A′ + uW⁺)` with `W⁺ = W + C(n,r₁)`, and `E^f_{−1} = e^{−u}W − V`,
`D^f_{−1} = −e^{−u}(A′ − uW)`.  On the overlap each true summand lies between `0` and the free one,
so `E^f − ω ≤ E ≤ E^f` and `D^f ≤ D ≤ D^f + u(r₁+1)ω`.  At `s = +1`:
`D + (A′/Z₀)E ≤ −e^u A′(1 − W⁺/Z₀) − u e^u W⁺ + u(r₁+1)ω < 0` because `W⁺ ≤ Z₀` and by (ii).
At `s = −1`: `D + (A′/Z₀)E ≥ u[e^{−u}W − r₁(e^{−u}2ⁿ + V + ω)] > 0` by (i), (ii) and `V ≤ 2ⁿ`.
`s ↦ U′_s` is continuous; `E_s` is non-decreasing in `s`, so
`E_{s*}/Z₀ ≥ (e^{−u}W − V − ω_{−1})/(2ⁿ + W) ≥ e^{−u}(1 − 1/r₁)`.  ∎

**Lemma R6.3 (overlap) [P; Hoeffding's inequality for sampling without replacement, K].**  If
`|d_H(a₀,a′) − n/2| ≤ Δ`, then `ω_s/Σ_{T_s<0} e^{−T_s} ≤ exp(−(n/2 − r₁ − 2Δ)²/(2r₁))` for every `s`.
(For `x` uniform on a sphere of radius `j ≤ r₁` about `a′`, `d_H(x,a₀) = D + j − 2i` with `i`
hypergeometric of mean `jD/n`.)

**Theorem R6 [P].**  Let `u > 0`, `ρ₀ = ln(2/(1+e^{−u}))/u < ρ₁ < ½`, `r₁ = ⌈ρ₁n⌉`, `0 < δ < ½`, and
let an algorithm evaluate `g` adaptively, be given `U = E_{μ_g} g` exactly, and return `ln Z_g`
within `ε < ½ ln(1 + e^{−u})` with probability `≥ 1 − δ` for every `g` of the class.  Then for all
large `n`, at `g₀`,

    E[#evaluations]  ≥  (1 − 2δ)(1 − 2/n²)·2ⁿ / |B(n, r₁)|,

so the worst-case exponent with the thermodynamic oracle is at least `ln 2 − h(ρ₀)`, and by
theory report Theorem 11.58 it equals it at every fixed accuracy below `ln(1+e^{−u})` (width).
*Proof.*  (i) holds for large `n`: `W/2ⁿ ≥ e^{n·u(ρ₁−ρ₀) − O(ln n)}` (take the term `d ≈ n/(1+e^u)`).
A uniformly random `a′` has `|d_H(a₀,a′) − n/2| ≤ √(n ln n)` with probability `≥ 1 − 2/n²`, and then
(ii) holds by R6.3.  For such `a′` the member `g′_{s*(a′)}` has the same oracle answer as `g₀`, a
value of `ln Z` more than `2ε` away, and differs from `g₀` inside `B(a′, r₁)` only; the
indistinguishability argument of Theorem 4.  ∎

**Corollary R6′ (all three oracles) [P].**  Replace `a₀`, `a′` by the cosets `a₀ + C`, `a′ + C` of a
linear code with dual distance `> k` and `|C| = e^{o(n)}`: `g₀^C = −u(r₁ − d_H(x, a₀+C))₊`, twin
`−u(r₁ + s − d_H(x, a′+C))₊`.  The algebra of R6.2 is unchanged (with `W`, `V`, `A′` the sums of the
symmetrised basin, whatever its self-overlaps), the overlap is at most `|C|²` times that of a
pair, and both `g₀^C` and the twin instance are `C`-invariant.  Hence **an algorithm that is given
the evaluations, all `k`-body marginals exactly and the mean residual energy exactly still needs
`(1−2δ)(1−o(1))·2ⁿ/(|C|·|B(n,r₁)|)` evaluations at `g₀^C`: the exponent `h = ln 2 − h(ρ₀)` at bounded
accuracy is unchanged by both oracles together.**  (The note conjectures twins "around `a₀`" for a
given visible state; for a worst-case statement the visible state may be chosen symmetric.)

*Checked.*  R6.1 is the formula my replication of Proposition 5b uses.  R6.2:
`U′_{±1} − U₀ = −0.731, +0.269` at `u = 1` (i.e. `−uσ`, `+u(1−σ)`), same pattern at `u = 0.5, 2`,
`n = 2000, 4000`, distances `0.45n, 0.5n, 0.55n` (`r3_prop5b_overlap.py`); disjoint twins at
`u = 2.6, 3, 4` (`r3_prop5b.py`, part 3).  R6.3: observed overlaps are far below the Hoeffding
bound (`ln` of the ratio `−54.6` against `−25.0` at `u = 1`, `n = 2000`, `D = n/2`).  R6′: on the
cosets of the Golay code (`n = 24`, `k = 7`), `u = 5`, `r₁ = 3`, twin around a deep hole:
`s* = −0.005574`, `U′ = U₀` to machine precision, `ln Z′ − ln Z₀ = 0.678`, every marginal of order
`≤ 7` uniform for both instances.

*Remark (tolerance).*  If the datum has any tolerance `τ_U ≥ |U′_0 − U₀|` — and `|U′_0 − U₀|` is
exponentially small — the twin with `s = 0` already does, and no root is needed.  The exact root
is the price of the exact oracle, not of the phenomenon.

---
## 5. Numerics: what was computed, sizes, results, how to re-run

Everything is in `experiments/science/ws_R3/`; Python 3.13, NumPy ≥ 2 (`np.bitwise_count`),
SciPy/HiGHS.  Run from that directory.  Outputs of my runs are the `*.out` files next to the
scripts.  All computations are exact enumerations or exact sums in floating point unless marked
"sampling" (none is) — "exact" below never means rational arithmetic, except where "integers" is
said.

| script (command) | what | size | result | time |
|---|---|---|---|---|
| `r3_codes.py` | own GF(2) algebra, BCH codes from `GF(2^m)`, duals, punctured codes, exact dual distances (brute force / MacWilliams, integers) | all `n ≤ 31`, `k ≤ n`, 2 coordinate sets | bound `|C| ≤ (2n)^{⌈k/2⌉}` and dual distance `> k`: **0 failures**; extended-BCH duals `m = 3…6`, `t = 1, 2, 3`: sizes `≤ 2(2^m)^t`, dual distance `2t+2` or more; puncturing example with `d_min = 1` | 5 s |
| `r3_thm2.py` | Theorem 2 on `[15,8,4]` (`k=4`) and Golay `[24,12,8]` (`k=7`): `ν_{C,b}` and the variant; all Fourier coefficients (full WHT), all flip ratios, entropies, path (e); (d) on random members | `2^{15}`, `2^{24}` states; 3 200 members `n ≤ 10` | all of (a)–(e) confirmed; first visible order is exactly `k+1` | 4 min |
| `r3_thm2.py big` | the same on `[31,10,12]` (`k = 4`) through the coset table (no full cube: uniformity follows from the exact dual distance 5 and `E_νχ_T = τ^{|T|}[T ∈ C^⊥]`) | `2^{21}` cosets × `2^{10}` words | `b = 1, 2, 4`: `S = 21.4201, 18.0444, 9.7244` inside `[18.05, 24.98]`, `[11.33, 18.26]`, `[2.79, 9.72]`; hidden order `n ln 2 − S = 0.07, 3.44, 11.76` nats | +1 min |
| `r3_thm3.py` | Theorem 3: identities (integers); **exact LP optimum** vs bound vs attained on 5 codes; all centres on 2 codes; asymptotics `n ≤ 10⁵`; LP/bound for `n ≤ 400`; moment bound | LPs with `n+1` variables | see §2 | 6 s |
| `r3_extensions.py` (`big` adds `[31,10,12]`) | Theorem 4's ingredients on 3 codes (C); R5 on 4 (+1) codes (A); R2 on 3 (+1) codes and 4 non-code laws, asymptotics (B, B′, B″) | up to `2^{24}` states, `2^{21}` cosets | all inequalities hold | 1.5 min (+2 min) |
| `r3_thm5.py` | Theorem 5 bracket, identity, sampled lower end | 450 members, `9·10⁴` sample sets | 0 violations; failure rate `10^{−4}` at `δ = 0.1` | 10 s |
| `r3_prop5b.py` | Proposition 5b: the note's cases; root structure in `n`; disjoint twins (`u = 2.6, 3, 4`); joint oracle on Golay | `n ≤ 5000` (`6.25·10⁶` terms) | note's `s*` and `ln Z′ − ln Z₀` reproduced with integer `r₁`; root from `n = 400`; R6 checks | 1 min |
| `r3_prop5b_overlap.py` | R6.2, R6.3 with overlapping supports | `n = 2000, 4000`; `u = 0.5, 1, 2` | signs at `s = ±1`, Hoeffding bound | 45 s |
| `r3_thm7.py` (`adv` for the ascent), `r3_thm7_kl.py` (guarded ascent) | Theorem 7 and R1: lemma on `2·10⁵` pairs; 4 000 random instances; extremal family; adversarial ascent (Nelder–Mead restarts) on `TV`, `J` and the two one-sided divergences | `|X| < 40`; ascent `|X| ≤ 5`, `≤ 2` features, `βω ∈ {0.5, 2, 4, 8}` | largest `TV/tanh(βω/4)` over random instances `0.99999`; extremal family exact; ascent reaches `tanh(βω/4)` and `βω·tanh(βω/4)` to six digits and never more; the one-sided divergences never exceed their no-feature suprema (`0.4745` at `βω = 2`, `4.9229` at `βω = 8`) **[N]** | 1 min; ascent 8 min per `βω` |
| `r3_chain.py tables 9` | own enumerator of the diamond-lattice chain vs the engineering tables | `n = 1…9` torsions (17 107 conformations) | class tables identical (classes, counts, `gmin`, `#gmin`, `gmax`) | 10 s |
| `r3_chain.py sec112` | §11.2 from the engineering tables, **dual** LP (4 multipliers) | `N = 7…27` beads, up to 4 532 classes | all 22 ends agree with the note to `≤ 10^{−3}` | 3 s |
| `r3_chain.py sec111` | §11.1, dual LP on the un-aggregated conformations | 13 beads, 49 833 conformations, up to 57 features | all 27 entries agree to two decimals | 2 min |
| `r3_chain.py sec9` | §9 thresholds `b_min`: bisection on LP feasibility, single-flip formulation on all `3ⁿ` patterns; at 8 beads also all ordered pairs of conformations | 8, 9 beads | all 12 values within `10^{−3}` of the note; both formulations give `0.438` | 3 min |
| `r3_chain.py sec114` | §11.4, own Charnes–Cooper LP | 9 beads | gauche-fraction and `R²` rows: 16 interval ends agree to the digits printed | 15 s |

**Reproduction status of the note's numerical claims.**

| claim in the note | status |
|---|---|
| §2 check ("all sixteen cases") | not re-run on the same four codes; the same statement confirmed on three *other* codes, for `ν_{C,b}` itself and for the variant |
| §3 check ("attained/bound up to 0.995", simplex `[15,4]`) | not re-run; consistent with the LP (`|C| = M_1 = 16` is tight); my largest ratio at all centres: `0.61` (`[15,8,4]`), `0.57` (Golay) |
| Proposition 5b numbers | **reproduced** (with `r₁ = round(ρ₁n)`); the criterion "`ln B₀ ≲ 2`" **not confirmed** |
| Theorem 7: "3 906 random instances, largest ratios 0.99989" | compatible: my 4 000 instances give `0.99994` |
| §9 table | **reproduced** (12/12) |
| §11.1 table | **reproduced** (27/27) |
| §11.2 table | **reproduced** (22/22); the "athermal value 0.64–0.65" confirmed at 9 beads (`0.652`) only |
| §11.4 table | gauche fraction and `R²` **reproduced** (16/16); compact-decile row not re-run |
| replication of engineering tables `n = 1…10` | confirmed for `n = 1…9` (and the count `49 833` at `n = 10`) |

A lesson worth recording: my first chain run labelled the two gauche states by absolute bond
index rather than by the sign of the dihedral; the class tables are unaffected, but the
single-flip graph is a different graph and `b_min` changed in the second digit.  The agreement
reported above is with torsion-angle states.

---

## 6. Originality and triviality

### Statement by statement

| statement | assessment |
|---|---|
| Lemma 1 | **Textbook.**  A linear code is an orthogonal array of strength `d^⊥ − 1` (Bose–Bush; Delsarte) **[K: from memory]**.  In physics language it is the gauge-invariance argument: a measure invariant under a group of local transformations gives zero expectation to every observable that is not invariant (Wegner's Ising gauge models, "phase transitions without local order parameters", J. Math. Phys. 12 (1971) 2259 **[K: search snippet]**).  "Order invisible to all local observables" is, in that literature, the definition of a gauge/topological phase; the note should say so. |
| "Codes" | **Textbook** (dual BCH codes as small `k`-wise independent sample spaces: Alon–Babai–Itai 1986 **[K: from memory]**). |
| Theorem 2 (a), (b) | **Textbook object in new clothes**: `ν_{C,b}` is the law of a noisy codeword (`X = Z ⊕ N`); its `k`-wise uniformity is the Fourier one-liner `E χ_T = τ^{|T|}[T ∈ C^⊥]`, the basis of statistical-query lower bounds for parities with noise **[K: from memory]**.  (c) is the mixture bound, (d) a two-line chain-rule argument.  What is specific to the note is the *question* (does a bounded-difference class help?) and the answer "no"; that is an observation, correctly disclaimed as assembled from textbook parts. |
| Theorem 3 | **Textbook method, slightly better constant.**  `r = 0`: Rao's bound.  `r > 0`: the moment method for sums of `k`-wise independent signs (Schmidt–Siegel–Srinivasan, SIAM J. Discrete Math. 1995; Bellare–Rompel) **[K: search snippet]** with the reproducing kernel in place of the `2t`-th power — constant `t!` instead of `(2t−1)!!`; equivalently one dual point of a Delsarte-type linear programme.  The reading (basin populations; "maximum occurrence") is the note's own. |
| Theorem 4 | **Short; apparently not written down** for this query model.  The technique — hide the alternative from low-order statistics by symmetrising it over a code — is the standard device of statistical-query lower bounds. |
| Theorem 5 | **Textbook** (Gibbs–Bogoliubov in both directions; the width as a sum of relative entropies is the dissipation identity of free-energy perturbation) **[K: from memory]**.  The Corollary is a correct and, I think, useful observation. |
| Proposition 5b | **Short; I do not know it elsewhere.**  The cleanest new idea of the note. |
| Proposition 6 | **Textbook.** |
| Theorem 7 | **Short; textbook ingredients; I have not seen the statement.**  The one non-obvious line is that matching the moments cancels the feature part of `ln(dμ/dν)` in the *symmetrised* divergence.  Without features it is the classical bound for a density-ratio class (`TV ≤ tanh(L/4)` for a log-density of oscillation `L`, as in the differential-privacy literature **[K: from memory]**), which is also the sharp form with features (R1). |
| §8 | **Textbook** (generalised moment problem; Donsker–Varadhan; LP duality).  The third format is the LP dual of a linear-fractional programme over a polyhedral cone — routine; "flow with gains" is a good name for it. |
| Theorem 8 | (a) definition, (b) maximum-entropy duality, (c) Farkas.  `ρ_min` is the relative entropy of the maximum-entropy reweighted ensemble, a standard diagnostic of force-field error in ensemble refinement **[K: from memory; workstream M to confirm]**; what the note adds is that a *dual* point gives a bound that does not depend on sampling.  `b_min` (a "Lipschitz divergence") I have not seen. |
| Proposition 9 | **Textbook** (thermodynamic integration). |
| §11.3 | An **observation** that is immediate from the definitions once stated — and a good one: the theory division's limit shape is a marginal polytope in the limit. |

### Does the framing claim more than it disclaims?

The header disclaimer ("no statement here is claimed to be new") is honest and should stay.  The
collaboration files are less careful: "a first result of our own", "we can prove a
dimension-free stability bound", "the experimental twin of D28".  The mathematics supports
"an observation with a three-line proof, assembled from textbook parts" for Theorems 2, 3, 5, 7
and "a short new argument" for Theorem 4 and Proposition 5b.  It becomes a *result* with §9.

### Search log (rule 5)

I judged the mathematics; the deep search is workstream M's.  Three web searches, snippets and
abstracts only, no full text read:
1. *"Schmidt Siegel Srinivasan Chernoff-Hoeffding bounds for applications with limited
   independence"* → SIAM J. Discrete Math. 1995 (SODA 1993); moment-based tail bounds under
   `k`-wise independence; described by later papers as stronger than Bellare–Rompel **[search
   snippet]**.  I did not verify their constants; the comparison "`t!` against `(2t−1)!!`" in this
   report is against the plain `2t`-th moment bound, which I computed myself.
2. *"Wegner 1971 Duality in generalized Ising models and phase transitions without local order
   parameters"* → J. Math. Phys. 12, 2259–2272 **[search snippet of the abstract]**.
3. *"Kolchinsky Tracey Estimating mixture entropy with pairwise distances"* → Entropy 19 (2017)
   361, arXiv:1706.02419: Chernoff-`α` divergences give a lower bound on mixture entropy
   **[abstract]**.  The inequality of R2(b) is proved independently above.
Everything else marked **[K: from memory]** was not looked up and must not be cited from this
report without verification: Bose–Bush / Delsarte (orthogonal arrays from codes), Rao 1947,
Alon–Babai–Itai 1986, Kearns 1998 (statistical queries), Hoeffding 1963 (sampling without
replacement), Harris 1960, Csiszár 1975, the Carlitz–Uchiyama bound, Gilbert–Varshamov, the
`tanh` bound for density-ratio classes, the sharp Jeffreys–total-variation inequality (proved
above in two lines, so nothing depends on a citation).

---
## 7. Recommended corrections, as replacement text

### 7.1 In `docs/science/INFERENCE_LIMITS.md`

**N1 — §0 table, first row.**  Replace the first two cells by

> | I2(`Φ_k`), **when the data are the uniform marginals** | **nothing about the entropy** beyond the a-priori range of the class, up to `⌊k/2⌋ ln(2n) + ln 2`: some class members with exactly these data have entropy within that distance of the class minimum (Theorem 2).  A statement about one data vector and about large `n` (it has content when `n(ln 2 − h(σ(b)))` exceeds `ln|C|`); other data can identify the entropy exactly. |

and retitle §2 "Uniform local data do not identify the entropy in a first-order class".  After
Theorem 2 add: *"(e) is an empty statement unless `n(ln 2 − h(σ(b))) > ln|C|`; of the sixteen
numerical cases below, nine are in that regime."*

**N2 — §0 table, row "I1 + I3".**  Replace the second cell by

> **at bounded accuracy (`ε < ½ ln 2`) the worst-case exponent is unchanged**: a visible basin can have a hidden twin with exactly the same mean energy (Proposition 5b).  At extensive accuracy: open.

**N3 — "Reading" after Theorem 3.**  Replace "Populations of individual states are identified
up to polynomial factors; the number of populated states — the entropy — is not identified at
all." by

> The population of every single basin is bounded **above** by `≈ n^{−⌊k/2⌋}`, and up to a constant this is the largest value compatible with the data; it is not bounded below (the uniform ensemble has the same data).  So the data exclude dominance of one basin; they identify neither the populations nor the number of populated basins — the entropy.

**N4 — §0 table, row "I2(Φ) + model + envelope class".**  Replace "kernel-checkable (Theorem 8)"
by

> the bound on `KL(truth‖model)` with a certificate the kernels can check (two partition-function bounds, for pairwise `f` and `Φ`); the bound on the envelope constant with a flow certificate for which no structured family is known yet (Theorem 8, §8)

**N5 — Proposition 5b.**  (a) Status: "[mechanism P; root N]" until R6 of this report has been
checked by a second reader, then "[P]"; delete "exact arithmetic" (write "exact sums in floating
point").  (b) Replace "`r₁ = ρ₁n`" by "`r₁ = round(ρ₁n)`" (that is what produced the numbers).
(c) Replace the last sentence of the numerical paragraph by

> There is a root as soon as the visible basin dominates by a factor of order `n` (`W ≥ 8r₁e^u·2ⁿ` suffices, R3 report R6.2); at `u = 1`, `ρ₁ = ρ₀ + 0.01` this is `n ≥ 400` (`ln B₀ ≥ 4`), and there is none for `n ≤ 300`.

(d) "cost exponent `0.0281`" → "asymptotic exponent `ln 2 − h(ρ₁) = 0.0282` (`0.0289` at `n = 5000`
with the polynomial prefactor)".  (e) State the accuracy: "for `ε < ½(ln Z_{g′} − ln Z_{g₀}) ≈ ½ ln 2`".

**N6 — §10, the paragraph after Proposition 9.**  Replace by

> This is thermodynamic integration.  It is recorded here because of what it says about targets **[H]**: within the model's own configuration space the total `ln Z` is determined by a caloric curve without any evaluation of `g` — provided the curve is known down to `β = 0`, which no experiment provides (calorimetry reaches absolute entropies from the other end, `T → 0`, and it measures the energy of all degrees of freedom, not `E_μ(f+g)`).  The quantities for which a certificate would be scientifically new — the population of a structural state, a contact probability, the entropy of a subsystem — are ratios of restricted partition functions and conditional averages, for which the exact robust theory is missing (§7); for one Boltzmann average, the mean magnetisation on the cube, the theory division's Theorem 11.35 shows the uncertifiable fraction to be larger than for `ln Z`.

**N7 — §11.3.**  Header: "[P, given theory report Theorem 11.69; for bridges]".  Replace the bold
sentence by

> **For bridges, the limit shape of §11.22 is the asymptotic model-free identified set at interior profile densities.  For all walks — the ensembles of §§11.1–11.2 — the asymptotic identified interval contains the chord `[γ(p), γ⁺(p)]` of `K^{br}` (bridges are walks), with equality under Conjecture 11.75.**  Its lower boundary is the theory division's least-gauche function, its upper boundary has not been computed.

and add "(this uses that `𝒦` has interior points in `ℝ³`: cite the statement of the theory report
that gives four affinely independent points of `K^{br}`, or ask for it)".

**N8 — Theorem 7.**  Replace (ii)–(iv) by

>     (ii)  TV(μ, ν) ≤ tanh(βω/4);
>     (iii) KL(μ‖ν) + KL(ν‖μ) ≤ βω·tanh(βω/4);
>     (iv)  |E_μ ψ − E_ν ψ| ≤ osc(ψ)·tanh(βω/4) for every bounded ψ;

in the proof replace "Pinsker's inequality gives `KL(μ‖ν) + KL(ν‖μ) ≥ 4·TV²`; so `4TV² ≤ βω·TV`" by
"`KL(μ‖ν) + KL(ν‖μ) ≥ 2·TV·ln((1+TV)/(1−TV))` (reduce to the two-cell partition `{μ > ν}`, `{μ ≤ ν}`
and minimise); so `ln((1+TV)/(1−TV)) ≤ βω/2`", and replace "Sharp to first order: …" by

> Sharp for every `βω`: two points, no feature, `r = (0, ω)`, `μ₀ = (1, e^{βω/2})/(1+e^{βω/2})` give `TV = tanh(βω/4)` and equality in (iii).

In (v) keep `KL(μ‖ν) ≤ βω·tanh(βω/4)`.

**N9 — §4, "Not proved here (i)".**  Replace by the statement of Theorem R5 (after a second
reading), and change the bold sentence after Theorem 4 to

> **for accuracies with `ln(1/ε) = o(n)` below the threshold, both exponents of the theory division's diagram for the cube — the non-adaptive `θ_na` (Theorems 11.44–11.45) and the adaptive `θ_hint` (Theorems 11.54 and 11.58, paper proofs) — are the same with and without free access to all `k`-body ensemble data, `k = o(n/ln n)`.**

and add after the proof of Theorem 4: "(Convention: `ε` here is half the width `ε` of the theory
report.)"

**N10 — "Codes" paragraph.**  Add: "For odd `k` the extended BCH code gives `|C| ≤ 2(2n)^{⌊k/2⌋}`;
by Rao's bound no code has fewer than `Σ_{j≤⌊k/2⌋} C(n,j)` words.  Restricting to `n` coordinates
preserves the dual distance, not the minimum distance of `C`."  In the "Attainment" paragraph
replace "So for even `k`" by "So, with the extended code for odd `k`, for every `k`" and
`n^{−k/2}` by `n^{−⌊k/2⌋}`.

**N11 — Theorem 5, Corollary.**  Add: "(The algorithm: compute the bracket; return its midpoint
if its width is at most `ε`; otherwise fall back on any class-correct procedure.  It is correct
on the whole class and costs `N` at `g ≡ 0`.  A tolerance `τ_U` on the datum widens the bracket by
`βτ_U`.)"

**N12 — §7.**  Add: "(For a single state `B = {y}` the maximum has the closed form
`Σ_{x∈A} e^{−β(f(x)−f(y)−d(y,x))}`, attained by `g = −d(y,·)`; the open case is `|A|, |B| ≥ 2`.)"

**N13 — §9.**  In the caption of the table add "single-torsion moves between the three
torsion-angle states `(t, g⁺, g⁻)`"; label the last sentence "[N: two sizes, one family of
truths]".

### 7.2 For the collaboration files

`SCIENCE_TO_ALL.md` states that corrections are new linked messages, never silent rewrites.  I
therefore recommend a short **correction message** (e.g. `SCI-MSG-0002`, "Corrections to
SCI-MSG-0001 §4 after internal review R3") with the following content, and an edit of the
digest entry that points to it.

**S1 — `SCI-MSG-0001` §4, heading.**  Corrected heading:

> A first result: on the cube class with zero known part, exact `k`-site marginals divide the lower bound at the zero residual by at most a polynomial factor and leave the adaptive exponent unchanged

**S2 — `SCI-MSG-0001` §4, "Two complements".**  "populations of single states are identified up
to polynomial factors, their number — the entropy — not at all" is withdrawn; correct statement:

> the population of every single basin is bounded above polynomially (`≈ n^{−⌊k/2⌋}`, attained up to a constant) and is not bounded below; the entropy is not identified.

**S3 — `SCI-MSG-0001` §4, "Why it matters", first two sentences.**  Corrected:

> It is the analogue of D28 for one idealised kind of experimental information.  On the cube class with zero known part, exact marginals of any bounded order do not lower the exponent of the cost of certifying a free energy (worst case over the class; the hard instance is the zero residual), and when they are uniform they do not identify the entropy: an ensemble can look fully disordered to every `k`-site marginal and be as ordered as the class permits, up to `⌊k/2⌋ ln n + O(1)` nats.  Nothing is proved for a known part without a large translation symmetry (a field, a chain), and on a chain pair distances are not `k`-local in the torsions.

Also: Theorem B is non-empty only for `n(ln 2 − h(σ(b))) > ln|C|`; the stability bound should read
`TV ≤ tanh(βω/4)` and `KL(μ‖ν) + KL(ν‖μ) ≤ βω·tanh(βω/4)` (sharp); the sentence "Whether the
worst-case exponent with such an oracle stays positive … is open" is superseded (it stays at
`h` at bounded accuracy: Proposition 5b of version 2 and R6 of the R3 report); invitation (a) of
§7 is answered (Theorem R5 of the R3 report), subject to a second reading.

**S4 — `SCIENCE_TO_ALL.md`, digest item 2.**  Replace (b)–(d) and the last sentence by

> (b) an oracle for all `k`-site marginals divides the lower bound for all algorithms at the zero residual by at most `2(2n)^{⌊k/2⌋}`, so **the worst-case exponent of adaptive algorithms, `θ_hint`, is unchanged by exact marginals of bounded order** (cube, zero known part; the cube's idealisation of local data); the same holds for the non-adaptive exponent `θ_na` (R3 report, R5; second reading pending); (c) uniform marginals bound the population of every single basin from above, polynomially (`≈ n^{−⌊k/2⌋}`), and not from below; (d) one *thermodynamic* datum, the mean residual energy in the true ensemble, closes the free-energy bracket at the zero residual with `O(nβ²c²/ε²)` evaluations — the hardest instance for evaluations alone becomes easy — but at bounded accuracy it leaves the worst-case exponent unchanged (a visible basin can have a hidden twin of the same mean energy).  The positive counterpart is classical: in a class that is linear in the measured observables the data determine the ensemble, and maximum-entropy refinement is stable, `TV ≤ tanh(β·osc(r)/4)` for a remainder `r` outside the span, sharp.

---

## 8. What I did not settle

1. **The lower bound of R2 in the whole class.**  Is `S(μ) ≥ n·h(σ(b)) + ⌊k/2⌋ ln n − C(b,k)` for
   every member of the class with uniform `k`-body marginals?  Members of the class are not
   mixtures of products in general.  What I know: every member is the output law of a binary
   symmetric channel *with feedback* (`x_i = z_i ⊕ n_i`, `z_i` a function of `x_{<i}` and private
   randomness), and `S − n·h(σ)` is the directed information from `z` to `x`; for laws that satisfy
   only the *sequential* bound in one order the price is smaller (noisy linear recurrences cost
   `(1 − h(σ)/ln 2)·t ln n`), so a proof must use the bound on all full conditionals.  **[C]**
2. **The thermodynamic oracle at extensive accuracy.**  Equal-depth twins give
   `ln 2 − h(ρ₀) − ε₁ < θ_hint(ε₁)`; wider, flatter twins of the same mean energy come close to
   `θ_hint(ε₁)` to first order in `ε₁` (back-of-envelope, not in this report's proofs).  Open.
3. **Known parts that are not `C`-invariant** (a field, a chain).  Not touched.
4. **§11.3**: whether `𝒦` has interior points is taken from the theory report's wording; the
   existence of the limit of the athermal profile density is not known to me; the chord at the
   athermal point is the note's [C].
5. **The theory report's theorems** 11.25, 11.44, 11.45, 11.54, 11.58, 11.69 were used as stated;
   I read the statements and status paragraphs, not the proofs.
6. **R5, R6, R6′** are mine and unrefereed.  R6′ is written as a corollary with its overlap count
   in one sentence; it needs the same care as R6.
7. **Prior art**: three spot checks; see §6.
8. **Not re-run**: the author's own scripts (I compared numbers, not executions); the
   compact-decile row of §11.4; §11.1 at sizes other than 13 beads ("grow or level off").
9. **The exact optimum of Theorem 3 within the class** (finite `b`): I computed it over all
   measures only.
10. The adversarial ascent for Theorem 7 was limited to `|X| ≤ 5`, two features and
    `βω ≤ 8` (`r3_thm7_adv.out`, `r3_thm7_kl.out`).  In the unguarded run two searches on
    `KL(μ‖ν)` returned `inf`: an underflow of `ν` in floating point, not a counterexample
    (`KL(μ‖ν) ≤ J ≤ βω·tanh(βω/4)` is proved); the guarded script rejects such instances.  A side
    observation **[N]**: with features the one-sided divergences never exceeded their no-feature
    suprema, which suggests a sharp form of (v) that I did not try to prove.

---

## 9. What is missing: the theorem within reach

The note shows that *one lower bound, at one instance,* survives a marginal oracle, that a
thermodynamic datum kills that instance, and — numerically — that another instance takes its
place.  The result that these observations are pieces of is:

> **Theorem (oracle invariance of the complexity diagram of the cube class).**  Cube class, zero
> known part, `u = βc > 0`; algorithms that return `ln Z` within `ε/2` with probability `1 − δ` on
> the whole class.  Give every algorithm, free and exact, all marginals of `μ_g` on at most `k`
> sites, `k ln n = o(n)`.
> (a) *Adaptive.*  The worst-case number of evaluations is `exp(n·θ_hint(ε₁) + o(n))` at extensive
> accuracies `0 < ε₁ < ln cosh(u/2)` and `exp(n·h + o(n))` when `ln(1/ε) = o(n)`, `ε = o(n)`.
> (b) *Non-adaptive* (evaluation points chosen from the marginals and private randomness).  It is
> `exp(n·θ_na(ε₁) + o(n))`, respectively `exp(n·a + o(n))`.
> (c) *With the mean residual energy `E_{μ_g} g` given exactly as well*, the adaptive exponent at
> every fixed accuracy `ε < ln(1 + e^{−u})` is still `h`; and at the zero residual the cost is
> `O(n u²/ε²)`.
> In words: the theory division's exponents are those of the *class*, not of the *oracle* — local
> ensemble data of bounded order change neither, and calorimetry changes the hardest instance,
> not the exponent.

Status of the parts: (a) lower bound = Theorem 4 of the note (reviewed here: proved); upper
bound = theory report Theorems 11.54, 11.58.  (b) = R5 (lower bound; mine, [P], checked on four
codes) + Theorem 11.44.  (c) = R6, R6′ (mine, [P], checked numerically) + Theorem 11.58 + the
Corollary of Theorem 5.  What has to be done to make it a result: a second reading of R5 and R6;
the overlap count of R6′ written out; a machine check of the three finite inequalities (R5(2),
R6.1, R6.2), which are of the kind the theory division's Lean development already contains;
and the prior-art check of workstream M for Theorem 4's symmetrisation in the statistical-query
literature.  It is within reach because every new ingredient is a finite inequality with an
elementary proof, and every hard ingredient is already in the theory report.

The runner-up, harder and of more physical interest, is item 1 of §8: *the entropy that can be
hidden from `k`-body data in a first-order class is the class maximum minus exactly
`⌊k/2⌋ ln n + O(1)`* — proved here for mixtures of polarised basins (R2), open in the class.

### The three most promising next steps

1. Write, referee and (for the finite inequalities) machine-check the oracle-invariance theorem;
   then replace Theorem 4, its remark (i) and Proposition 5b by it.
2. Decide item 1 of §8 (prove the lower bound in the class, or find a member that undercuts
   mixtures); start with exact vertex enumeration for `n ≤ 5` and the feedback representation.
3. The thermodynamic oracle beyond bounded accuracy and beyond the zero residual: the
   instance-wise complexity with the datum (what replaces the soft gap when the bracket of
   Theorem 5 is available?), and the extensive-accuracy exponent.

### Requests

**To the theory division.**
* T1.  Please check (and, if you agree, formalise) three finite statements: (i) R5(2): for a
  linear code `C` with `γ = ½(|C|−1)cosh(u/2)^{−d_min} < 1`,
  `ln Z(c·d_H(·,a+C)) − ln Z(max(c·d_H(·,a+C), cR)) ≥ D_R + ln(1−γ)`; (ii) the excess identity
  R6.1; (iii) the sign lemma R6.2 with its two hypotheses.  And confirm that
  `nonadaptive_expected_queries_ge` is stated for an arbitrary class of residuals, so that it
  applies to the sub-class of `C`-invariant members.
* T2.  Does the report contain four affinely independent points of `K^{br}` (so that `𝒦` has
  interior points in `ℝ³` unconditionally)?  If not, which explicit bridges would give them
  through the one-sided rate `168/(N+3)`?
* T3.  With the oracle `U = E_{μ_g} g` added to the query model, what is the adaptive exponent at
  extensive accuracy `ε₁n`?  Lower bound known to us: `ln 2 − h(ρ₀) − ε₁` (equal twins); upper
  bound: `θ_hint(ε₁)`.

**To the engineering division.**
* E1.  *Class tables for bridges.*  Motivation: §11.3 compares numbers for walks with a limit
  proved for bridges.  Formulation: the tables `dia_Sc12_n*.txt` with the enumeration restricted
  to bridges (first bead strictly lowest, last bead highest in the coordinate `y`).  Inputs:
  none new.  Outputs: same columns (`h₃ h₈ h₁₁ | count | gmin | count_gmin | gmax`), `n ≤ 24`.
  Validation: for `n ≤ 9` against an independent enumerator (ours: `r3_chain.py` can be
  restricted in ten lines); every bridge class is a walk class with `gmin_walk ≤ gmin_bridge`.
  Stopping: `n = 24` or one core-hour per size.  Resource estimate: below the cost of the walk
  tables (bridges are a subset).  Use: chords of walks and of bridges at the athermal profile,
  size by size — a direct test of how much Conjecture 11.75 matters for identified sets.
* E2.  *Joint counts.*  The present tables give `gmin`, `gmax` per profile class; with the full
  histogram of the gauche number per class (one extra line per class) the exact athermal mean
  gauche fraction, and identified sets for truths that depend on the gauche number (the "stiff"
  truth of §11.1), become available up to 27 beads.  Validation: row sums equal the present
  `count`; minima and maxima equal `gmin`, `gmax`.
