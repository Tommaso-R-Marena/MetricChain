# Workstream G — what the certification theory predicts for articulated chains: envelopes from geometry

Directory: `<session scratch>/ws/G/`
(all scripts `e*.py`, outputs `out_*.txt`, scratch Lean files `lean/*.lean`; nothing in the repository was
modified).  Scope: idealised model chains with made-up parameters only (fixed bond length and angle,
rotameric torsions, synthetic energies); no sequences, no targets, no experimental data.

Status tags: **[P]** proved here (paper proof), **[L]** machine-checked in a scratch Lean file of this
directory against the repository's definitions, **[N]** numerical (own Python code), **[H]** heuristic.
"Theory report" = `docs/THEORY_REPORT.md`; its theorem numbers are used as given.

Contents: 1 verdicts · 2 statements and proofs (2.0 setting … 2.12 table of regimes) · 3 numerics ·
4 prior art and search log · 5 not settled · 6 next steps · 7 file list.

---

## 1. Verdicts in one paragraph

(i) The verified torsion→RMSD route (theory report §4.4, blueprint §7) gives bounded-difference
constants that obey a **lever-arm law** `c_i = Θ(Λ b m_i^{3/2})`, `m_i = min(i, n+1−i)`, with explicit
constants (closed form for the extended chain, a certified uniform bound that is asymptotically
attained, exact Kabsch values up to a factor 4.4 below the verified bound); in RMSD units
`c_i ≈ 0.82 L b m_i^{3/2}/√N`, from `∝ L/√N` at the ends to `≈ 0.29 L b N` at the centre.
(ii) With such constants §11 predicts that certification **is exhaustive enumeration to leading order**:
`ln N_cov ≥ n ln k − C (n e/c_0)^{2/5}` for every algorithm, also randomised, also for `ln Z` at any
extensive accuracy and any fixed temperature (Theorem G3); only `O(N^{1/3})` end sites are sharp at fixed `L`,
none for large `N` when `L` is extensive — and for an extensive local residual `L` *is* of order `N`
(Theorem G2: `L = O(ℓN)` always, and `L ≥ 0.387 n e_g/b` already for the gauche count on the diamond
chain).  So a first-order RMSD-Lipschitz envelope in weighted-Hamming form is hopeless for long chains.
(iii) **No invariant metric repairs this inside the weighted-Hamming format** when the residual
contains contacts between atoms far apart along the chain: any envelope, in any metric, for which a
contact count is admissible has `c_i ≥ u_0 ⌊(m_i−1)/2⌋` (zipper bound, Theorem G4); second-order
(mixed-difference) envelopes in torsion coordinates are dense and growing, because one contact is an
interaction of order ≈ 0.6 × loop length in torsion space (G6).  Chain-length-independent constants
exist exactly for *sequence-local* residuals and local-frame metrics with a sequence window (G5).
(iv) What helps is to **leave the product format**.  Using the RMSD envelope itself, not its
Hamming relaxation, the certificate is *stretched-exponential*:
`0.05 √(L b N/e) ≤ ln N_cov ≤ 4.91 √((L b N/e) ln(e(k−1)n)) + ln(81(n+1))` (Theorem G8) against
`n ln k − o(n)` for the relaxation; at finite temperature the randomised (spot-check) cost is
`exp(O(√(β L b N)))` for every instance, by a residual-independence identity for `E_π e^Λ` and a
metric-entropy bound (Theorem G9, machine-checked).  For contact-type residuals the contact-map metric
makes sharpness a *per-contact* condition, independent of chain length (G10), and gives certificates
two to three orders of magnitude smaller than the best Hamming envelope at the sizes we could
enumerate (2 against 359–452 at `n = 7`), but it stays exponential asymptotically; treating the class
as what it is — linear in unknown pair coefficients — needs at most `rank ≤ P+1 = O(N²)` evaluations
(G11).
(v) Caveats: the tools are elementary (triangle inequalities, Chernoff counting, Kolmogorov–Tikhomirov
coarse-graining); the constants of G8 are two orders of magnitude apart; the product-domain theorems
ignore excluded volume; everything is synthetic.

---

## 2. Precise statements, with proofs or counterexamples

### 2.0 Setting and notation

* **Chain.**  Atoms `0,…,N−1` of unit mass, `N = n+3`, bond length `b`, bond angle `θ`.  Torsion
  `i ∈ {1,…,n}` is the dihedral of atoms `(i−1,i,i+1,i+2)`; changing it rotates atoms `i+2,…,N−1`
  about the bond `(i,i+1)`.  Side `A` of torsion `i` = atoms `0..i−1` (`i` atoms off the axis), side
  `B` = atoms `i+2..N−1` (`n+1−i` atoms); `m_i = min(i, n+1−i)`.  Each torsion has `k` rotameric
  states; numerics use `k = 3`, states `t, g⁺, g⁻ = 180°, ±60°` (largest change `δ = 120°`), and two
  geometries: the *generic chain* (`θ = 111°`, as in the repository's `build_chain`) and the
  *diamond-lattice chain* (`θ = arccos(−1/3)`; integer coordinates; a *contact* is a pair of
  non-bonded atoms on adjacent lattice sites; "SAW" = self-avoiding conformations, "phantom" = all
  `3ⁿ`).  `x ∈ [k]ⁿ ↦ X(x) ∈ ℝ^{N×3}`.
* **Distances.**  `D_K(X,Y) = min_{g∈SE(3)} ‖X − gY‖_F` (Kabsch, proper motions),
  `RMSD = D_K/√N`.  A residual is `Λ`-Lipschitz in the `ℓ²` superposition distance (the hypothesis of
  Corollary 4.7) iff it is `L`-Lipschitz in RMSD with **`L = Λ √N`**.  Both normalisations are used;
  which one is "intensive" matters and is discussed in 2.2.
* **Known part** (synthetic): `f(x) = Σ_i φ_i(x_i)`, `φ_i(t) = 0`, `φ_i(g^±) = e` unless stated;
  `G = Σ_i k⁻¹ Σ_s φ_i(s)` (`= 2ne/3` for `k = 3`).  `N_cov(ε)`, slack, soft gap `Λ(y)`, `R*`, etc. as
  in the theory report §11.  `λ := L b/e`.
* `h(x) = −x ln x − (1−x) ln(1−x)`.

### 2.1 Theorem G1 — the lever-arm law for the verified constants

`I_A, I_B` = moments of inertia of the two sides about the torsion axis (theory report Thm 4.6).

**(a) Extended chain [P, N].**  In the all-trans conformation the atom `p ≥ 1` positions before
atom `i` (and, symmetrically, the atom `p+1` positions after atom `i`) is at distance
`b sin θ · ⌈p/2⌉` from the axis of torsion `i`; hence

    I_A = b² sin²θ · S(i),   I_B = b² sin²θ · S(n+1−i),   S(m) = Σ_{p=1}^{m} ⌈p/2⌉² = m³/12 + O(m²).

*Proof.*  The zigzag is `X_j = (j a, (−1)^j h/2, 0)` with `a = b sin(θ/2)`, `h = b cos(θ/2)`; the bond
direction is `(a, ∓h)/b`; the distance of `X_j` from the line through `X_i, X_{i+1}` is
`|(j−i) a h ± (y_j − y_i) a|/b`, which is `|j−i| ah/b` for even `j−i` and `(|j−i| ± 1) ah/b` for odd,
and `ah/b = (b/2) sin θ`. ∎  (`t0_selftest.py`: agreement to `10⁻⁹` for `N = 8, 13, 30`.)

**(b) Regular helices [N + sketch].**  If all torsions are equal the chain is a helix with rise `h_r`
per atom, the bond makes the angle `ψ`, `cos ψ = h_r/b`, with the helix axis, and
`I(m) = ⅓ h_r² (1 − h_r²/b²) m³ (1 + O(1/m))` (an atom at axial distance `z` is at distance
`|z| sin ψ + O(radius)` from the bond line).  Checked for `φ₀ = 180°, 120°, 90°, 60°, 40°` at
`m = 400`: agreement within 1.5 % (`out_e9.txt`, part iii).  The cubic law is not special to the
extended chain; only compact conformations escape it (see (f)).

**(c) Uniform bound over the whole rotamer domain [P; attained N].**  For every conformation,

    I_A ≤ Ī(i) := Σ_{p=1}^{i} d̄(p)²,     d̄(p) = b (2⌊p/2⌋ sin(θ/2) + (p mod 2)),

and the same for `I_B` with `n+1−i`; `Ī(m) = ⅓ sin²(θ/2) b² m³ (1 + O(1/m))`.
*Proof.*  The distance to the axis is at most the distance to the axis atom `i`; atoms two bonds
apart are at the fixed distance `2b sin(θ/2)`; triangle inequality. ∎  The tables use the slightly
smaller zigzag form (`d(p) = b (p² sin²(θ/2) + cos²(θ/2))^{1/2}` for odd `p`: the planar zigzag
maximises every intra-chain distance — classical; confirmed by continuous optimisation for
`p ≤ 11`, `out_e9d.txt`).  The bound is asymptotically attained: the exhaustive maximum over all arm
conformations (`m ≤ 12`, `3^{m−1}` each) is reached by *one gauche next to the axis followed by
all-trans* (an arm almost perpendicular to the axis), with `max I/m³ = 0.256 → 0.228` (`m = 12 → 200`,
pattern search) against `sin²(θ/2)/3 = 0.2264` (`out_e1.txt`, E1b).  The extended chain itself has
`sin²θ/12 = 0.0726`: **the domain-wide constant is 1.77 times the extended-chain constant.**

**(d) Verified constants.**  By Corollary 4.7 / blueprint §7, for every `Λ`-Lipschitz invariant
residual and rotamer changes of at most `δ`,

    c_i^ver = 2 Λ sin(δ/2) √Ī(m_i)  ≤  (2/√3) sin(δ/2) sin(θ/2) · Λ b m_i^{3/2} (1 + O(1/m_i))
            = 0.824 Λ b m_i^{3/2}      (θ = 111°, δ = 120°)

is a valid weighted-Hamming envelope.  In RMSD units `c_i^ver = 0.824 L b m_i^{3/2}/√N`: between
`≈ 1.7 L b/√N` at the chain ends and `0.29 L b N` at the centre.

**(e) The smallest valid constants obey the same law [P + N].**  For the class of all `Λ`-Lipschitz
functions of `D_K` the smallest valid weighted-Hamming constants are
`c_i* = Λ max_{x,a} D_K(X(x), X(x^{i→a}))` (the function `D_K(·, X₀)` is in the class), and

    c_i* ≥ Λ ρ^sym(m_i),      ρ^sym(m) ≥ 0.186 b m^{3/2}   (θ = 111°, δ = 120°; computed for all m ≤ 240),

where `ρ^sym(m)` is the Kabsch distance of the central rotamer change of the all-trans chain with
two arms of `m` atoms.  *Proof of the first inequality:* restricting both conformations to a subset
of atoms does not increase the Kabsch cost (the optimal motion of the whole is admissible for the
part); restrict to the `m_i` atoms nearest to the axis on each side. ∎  The second is a computation:
`ρ^sym(m)/m^{3/2} = 0.217, 0.196, 0.191, 0.189, 0.1875` for `m = 10, 30, 60, 120, 240` (minimum over
all `m ≤ 240`: 0.1875), tending to the thin-rod limit `0.1863` (a straight rod against a rod bent by
`γ = 58.75°`, `cos γ = cos²α + sin²α cos δ`, `α = (π−θ)/2`; cost
`(⅔(1−cos(γ/2))² + ⅙ sin²(γ/2)) ℓ³`) (`out_e9e.txt`, `out_e9.txt` part ii).  So
`c_i* = Θ(Λ b m_i^{3/2})` and **the verified bound loses at most a factor `0.824/0.186 = 4.4`**
(1.77 from the worst conformation, ≤ 2.05 from coaxial instead of optimal superposition, the rest
from `min(I_A,I_B)` against the exact coaxial cost).  Exhaustive check (`n ≤ 8`, all `3ⁿ`
conformations, E1c): exact/verified = 0.59–0.95.

**(f) Conformation-specific values [N]** (`out_e1.txt`, E1a; RMSD caused by one rotamer change at
the central torsion, `n = 240`): extended 16.0 (verified bound at that conformation 39.9), helix
18.8 (40.6), random coil 5.8 (7.9), compact (`R_g = 5.5`) 6.1 (7.7); at the end torsion 0.10 in all
cases.  Growth exponents `d ln ρ/d ln m`: extended and helical `→ 3/2`, coil `≈ 1`, compact
`ρ ≈ min(m, √m R_g/b) b`.  These matter for envelopes that are *not* uniform (2.7c).

*Classification.*  (a)–(d) are routine consequences of Theorem 4.6; that the uniform constant is
attained by a kinked arm, and the factor 4.4, were not in the repository.

### 2.2 Theorem G2 — normalisation: for an extensive local residual `L` is of order `N`

**(a) Upper bound [P, routine].**  Let `Δ = Σ_{t=1}^{M} φ_t(X_{S_t})` be invariant, each `φ_t`
`ℓ`-Lipschitz in the Euclidean norm of the coordinates of its atom set `S_t`, each atom in at most
`q` sets.  Then `|Δ(X) − Δ(Y)| ≤ ℓ √(qM) · D_K(X,Y)`: `Λ ≤ ℓ√(qM)`, i.e. `Λ = O(ℓ√N)`, `L = O(ℓN)` for
`M = O(N)` terms.  (Cauchy–Schwarz over the terms, invariance to insert the optimal motion.)

**(b) Lower bound on the diamond-lattice chain [P + N].**  The two words of five torsions
`A = t t g⁺ t t` and `B = g⁺ t g⁻ t g⁺` have the same end frame (found by enumeration,
`out_e9c.txt`).  Hence for `n = 5r` the conformations `A^r` and `B^r` coincide on three of every five
atoms and no atom is displaced by more than `√(8/3) b`; `RMSD(A^r, B^r) ≤ √(2/5)·√(8/3) b = 1.033 b`
for every `r` (measured 0.999, 1.024, 1.031 at `n = 50, 200, 800`), while their numbers of gauche
torsions differ by `2r`.  Therefore **every RMSD-Lipschitz envelope of the residual
`e_g · #gauche` has `L ≥ 2r e_g/(1.033 b) = 0.387 n e_g/b`.**  All mixtures of the two words that
were generated are self-avoiding and lie within the same RMSD ball of radius `≈ b`, with residual
values spread over `2 r e_g`: RMSD cannot resolve an extensive amount of local structure.
Generic chain [N]: the exact `L_eff = max |Δ#g|/RMSD` is `0.78 N` for `n = 5, 6, 7`
(`out_e10.txt`); the helices `(g⁺)ⁿ` and `(g⁻ t t)^{n/3}` stay at RMSD 1.16–1.23 for `n = 48…192`
(`L_eff ≥ 0.53 N`; this pair drifts apart slowly, so it does not prove extensivity off-lattice).

**Consequences.**  (1) Three scalings of `L` are natural and are kept apart below:
*RMSD-intensive* (`L` fixed: residuals that see only global shape), *Frobenius-intensive*
(`Λ` fixed, `L = Λ√N`: the convention of Corollary 4.7 with a fixed certified constant), *extensive*
(`L = ℓN`: the generic case for a sum of `Θ(N)` local terms — the upper bound (a) is attained up to a
constant by the gauche count, (b)).  (2) For a local residual of per-torsion
amplitude `e_g` the exact constants are `c_i = e_g` (sharp iff `e_g ≤ e`), whereas the RMSD route
gives at least `L_eff ρ_i*/√N`, i.e. between `≈ 0.6 √n e_g` (end torsion) and `≈ 0.025 n² e_g`
(centre): **the detour through RMSD inflates the constants of a local residual by `√n` to `n²`.**
Small-chain illustration (`out_e10.txt`, `n = 7`, `e_g = ½`): torsion envelope 1 evaluation, verified
Hamming relaxation of the RMSD envelope 123–169.

### 2.3 Theorem G3 — the weighted-Hamming format with growing constants: sharp sites, exponents, thresholds

**Theorem G3 [P; uses Theorems 11.6(c), 11.23(b), 11.24(b) of the theory report, which are [V]].**
Let `X = [k]ⁿ`, `f` additive with `min φ_i = 0`, envelope `Σ_i c_i [x_i ≠ y_i]`, zero residual, and
suppose `c_i ≥ c_0 m_i^γ` with `γ > 0`, where at most two sites share each value of `m_i`.  Put
`C_{k,γ} = (1+γ) [2(k−1) Γ(1+1/γ)/γ]^{γ/(1+γ)}`.  Then for every `ε ≥ 0`

    ln N_cov(ε)  ≥  n ln k − C_{k,γ} ((G + ε)/c_0)^{1/(1+γ)},

every randomised `(ε/2, δ)`-correct algorithm for the minimum makes at least `(1−2δ)` times that
many evaluations in expectation, and every randomised `(ε/2, δ)`-correct algorithm for `ln Z` at
inverse temperature `β` satisfies

    ln E|Q|  ≥  ln(1−2δ) + n ln k − C_{k,γ} ((G + (n ln k + ε)/β)/c_0)^{1/(1+γ)}.

On the other hand `N_cov ≤ k^{n − n_sharp}`, `n_sharp = #{i : c_i ≤ min_{s≠t} φ_i(s)}`.

*Proof.*  Theorem 11.6(c): `N_cov ≥ e^{−tε} Σ_y e^{−t gap(y)} / max_a Σ_y e^{−t s(a,y)}` for every
`t ≥ 0`.  Numerator: `Π_i Σ_s e^{−tφ_i(s)} ≥ kⁿ e^{−tG}` (Jensen).  Denominator:
`Π_i (1 + (k−1)e^{−tc_i}) ≤ exp((k−1) Σ_i e^{−tc_i})` and
`Σ_i e^{−tc_i} ≤ 2 Σ_{m≥1} e^{−t c_0 m^γ} ≤ 2 ∫_0^∞ e^{−t c_0 u^γ} du = 2Γ(1+1/γ)(t c_0)^{−1/γ}`.
So `ln N_cov ≥ n ln k − t(G+ε) − 2(k−1)Γ(1+1/γ)(tc_0)^{−1/γ}`; the optimal `t` gives the claim
(`At + Bt^{−1/γ}` has minimum `(1+γ) A^{1/(1+γ)} (B/γ)^{γ/(1+γ)}`).  Randomised, minimum: Theorem
11.23(b) with the same weights.  `ln Z`: Theorem 11.24(b) in product form (the soft gap is additive
over sites) with site weights `v_i(b) = e^{−tΛ_i(b)/β}`: the site factor is
`ln Σ_b e^{−tΛ_i(b)/β} − ln(1 + (k−1)e^{−tc_i}) ≥ ln k − (t/β) k⁻¹Σ_b Λ_i(b) − (k−1)e^{−tc_i}`, and
`Λ_i(b) ≤ −ln π_i(b) ≤ βφ_i(b) + ln k`.  Upper bound: enumerate the non-sharp sites; a configuration
is covered by its copy with the sharp sites reset to the ground state (slack `≤` gap). ∎

*Reading.*  The deficit is sublinear for **every** growth exponent `γ > 0`: `n^{2/5}` for the
lever-arm law (`γ = 3/2`), `n^{1/2}` for the zipper law of 2.4 (`γ = 1`), `n^{2/3}` for constants
valid only on a compact box (`γ = ½`, 2.1f) — conformation- or box-specific constants do not rescue
the format.  The mechanism is the needle: a dip of depth `gap(y) + ε = O(n)` at `y` is supported on
the configurations that differ from `y` only at the `O(n^{1/(1+γ)})` torsions nearest to the two
chain ends, and it must be excluded for every `y`.  An extensive tolerance does not help,
randomisation does not help, a fixed positive temperature does not help.

**Predictions for the verified lever-arm constants** (`k = 3`, `e = b = 1`, `θ = 111°`; exact
evaluation of `LB = max_t Σ_i max_v r_i(t; v)`, `out_e2.txt`, `out_e11.txt`):

* *Sharp sites.*  Site `i` is sharp iff `m_i ≤ m* = (e√N/(0.824 L b))^{2/3}`: `≈ 2m*` sharp sites,
  a fraction `∝ N^{−2/3}`.  All sites are sharp iff `L ≤ 3.44 e/(bN)`.

  | n | all sharp iff `L ≤` | #sharp at `L = 0.1` | `L = 1` | `L = 10` | `Λ = 1` (`L = √N`) | `L = 0.1 N` |
  |---|---|---|---|---|---|---|
  | 10 | 0.336 | 10 | 4 | 0 | 0 | 2 |
  | 100 | 0.0343 | 48 | 8 | 0 | 0 | 0 |
  | 1000 | 0.00343 | 104 | 20 | 2 | 0 | 0 |

* *Zero temperature* (`ln N_cov ≥ LB`; `n ln 3 = 109.9, 1098.6`):

  | scaling | n | `c_1` | `c_mid` | LB | LB/(n ln 3) | deficit | G3 bound on deficit |
  |---|---|---|---|---|---|---|---|
  | `L = 1` | 100 | 0.17 | 29 | 65.3 | 0.594 | 44.6 | 62.0 |
  | `L = 1` | 1000 | 0.055 | 291 | 910.4 | 0.829 | 188 | 246 |
  | `L = 10` | 1000 | 0.55 | 2914 | 1024 | 0.932 | 74 | 98 |
  | `Λ = 1` | 1000 | 1.73 | 9228 | 1053 | 0.958 | 46 | 62 |
  | `L = 0.1 N` | 100 | 1.76 | 300 | 93.1 | 0.847 | 16.8 | 24.4 |
  | `L = 0.1 N` | 1000 | 5.49 | 29225 | 1070 | 0.974 | 28.3 | 38.9 |

  The deficit grows like `n^{3/5}` at fixed `L`, `n^{2/5}` at fixed `Λ`, `n^{1/5}` for extensive `L`,
  as G3 predicts (measured ratios for `n: 1000 → 2000`: 1.53, 1.34, 1.16; predicted 1.52, 1.32, 1.15).
  The implementation was cross-checked against exact fractional covers on a 729-state product.

* *Finite temperature* (`H` = Gibbs entropy; `U = ln E_π e^Λ`; `ε_crit = β Σ_i val_i`, the accuracy
  below which the randomised lower bound has a positive exponent — on the cube it is
  `Σ_i ln cosh(βc_i/2)`, the heterogeneous form of Theorem 11.25, same proof):

  | scaling | β | n | H | U | `ε_crit` | `ln E[#Q] ≥` at `ε = 0` | at `ε = 0.1n` | at `ε = n` |
  |---|---|---|---|---|---|---|---|---|
  | `L = 1` | 1 | 100 | 97.5 | 98.2 | 695 | 53.2 | 51.1 | 35.7 |
  | `L = 1` | 1 | 1000 | 975 | 1071 | 7.7·10⁴ | 859 | 850 | 791 |
  | `L = 1` | 2 | 1000 | 666 | 1078 | 1.5·10⁵ | 897 | 892 | 852 |
  | `L = 0.1 N` | 1 | 100 | 97.5 | 109.0 | 8165 | 87.9 | 87.1 | 81.2 |
  | `L = 0.1 N` | 1 | 1000 | 975 | 1098.6 | 7.8·10⁶ | 1062 | 1061 | 1051 |

  The threshold accuracy is super-extensive (`∝ β L b n²` at fixed `L`), so every extensive accuracy
  is deep inside the exponential regime; the soft gap tends to its maximum `−ln π(y)`, the spot-check
  exponent `U` to `n ln k`, and the randomised lower bound exceeds the Gibbs entropy at low
  temperature (needles hide where `π` is small).

* *Reference: what chain-length-independent constants would give* (homogeneous sites, `k = 3`):
  `R* = 0, 0.186, 0.312, 0.577, 0.772` nats per torsion for `c/e = 1, 1.5, 2, 4, 8`
  (`ln 3 = 1.099`); at `β = 1`: `R^rand(0) = 0.027, 0.060, 0.104, 0.309, 0.577`.

*Classification.*  An application of Theorems 11.6–11.8, 11.23–11.25; the closed form of the deficit
and the conclusion "sublinear deficit for every `γ > 0`" are new relative to the repository; routine.

### 2.4 Theorem G4 — the zipper bound: growth is intrinsic to torsion-Hamming envelopes of contact residuals

**Theorem G4 [P + N].**
(i) Let `d` be an envelope on a set of conformations, obtained from *any* metric and *any*
Lipschitz constant, for which `g = u_0·#C` and `−g` are admissible (`#C` = number of contacts).
Then `d(x,x') ≥ u_0 |#C(x) − #C(x')|` for all `x, x'`; in particular a weighted-Hamming envelope
needs `c_i ≥ u_0 zip_i`, `zip_i := max |#C(x) − #C(x^{i→a})|`.  If the class contains all signed
contact energies `|ε_p| ≤ u_0`, then `c_i ≥ u_0 max |C(x) △ C(x^{i→a})|`.
(ii) On the diamond-lattice chain, for self-avoiding pairs, for every `n` and every torsion `i`,

    ⌊(m_i − 1)/2⌋  ≤  zip_i  ≤  2 m_i + 1.

*Proof.*  (i) is the definition of admissibility applied to the pair.  (ii) Upper bound: a rotamer
change at `i` moves one side rigidly, so only contacts between the two sides change (distances to
the two axis atoms are preserved); each atom of the lighter side has at most 2 non-bonded lattice
neighbours (3 for a chain end).  Lower bound: the *hairpin* `t^{p₁} g⁺g⁻g⁺ t^{p₂}` (the three gauche
torsions close a six-ring; the two all-trans arms run on adjacent parallel zigzag lines and touch at
every second atom) has `⌊min(p₁,p₂)/2⌋ + 1` contacts `(a, b)` with `a + b` constant, and changing
the first torsion of the turn alone removes all of them while the chain stays self-avoiding; put the
turn at torsions `i, i+1, i+2` (or `i−2, i−1, i`).  The contact pattern is periodic along the arms
(two more trans torsions on each arm add one contact), which extends the finite verification
(`n ≤ 643` in `out_e3b.txt`; every position `i` for `n ∈ {12, 13, 30, 31, 60, 61, 200, 201}` in
`out_e9.txt`, part i) to all `n`. ∎

Exhaustive values for short chains (`out_e3a.txt`, all SAW pairs): at `n = 12`, `zip_i = 3…4`,
symmetric-difference version `4…6`, phantom chains `4…13`; a *typical* rotamer change alters only
`0.2–0.4` contacts — the growth is a worst-case phenomenon, and the weighted-Hamming format can only
store worst cases.

**Corollary [P].**  With Theorem G3 (`γ = 1`, `c_i ≥ u_0 (m_i − 2)/2`): for the phantom product
domain and *the best possible* weighted-Hamming envelope of the contact class,
`ln N_cov ≥ n ln k − 4 √((k−1)(G+ε)/u_0) (1 + o(1))`.  Numerically (`out_e11.txt`, `k = 3`):
`u_0 = e`, `n = 1000`: 8 sharp sites, `LB = 973.8` of `1098.6`.

*Answer to question 3 of the brief.*  There is **no** invariant metric in which sums of pair terms
of bounded range have Lipschitz constants and single-torsion diameters whose product stays bounded
along the chain: the product is at least `u_0 ⌊(m_i−1)/2⌋` whatever the metric.  The obstruction is
the *hinge*: a torsion is a non-local move in space, and the Hamming format charges every hinge its
worst case.

### 2.5 Theorem G5 — what does not grow: sequence-local residuals and windowed local-frame metrics

**Theorem G5 [P].**  Let `g(x) = Σ_{a<b, b−a ≤ w} φ_{ab}`, each `φ_{ab}` a function of the distance of
atoms `a, b` with oscillation at most `u`.  Then for every `n` and `i`

    c_i := max |g(x^{i→a}) − g(x)| ≤ u (w−1)(w−2)/2,
    c_ij := max |mixed second difference in torsions i, j| ≤ 2u · C(w−1−|i−j|, 2)   (= 0 for |i−j| ≥ w−2),
    ½ Σ_{j≠i} c_ij ≤ 2u · C(w−1, 3).

The same holds, with `O(w²)` and `O(w³)` constants, when `φ_{ab}` depends on the relative geometry
of the local frames at `a` and `b` (frames built from the bonded neighbours).
*Proof.*  The distance of atoms `a < b` depends on torsion `i` iff `a ≤ i−1` and `b ≥ i+2`; there are
`s − 2` such pairs of separation `s`, and `Σ_{s=3}^{w}(s−2) = (w−1)(w−2)/2`.  A pair depends on both
`i < j` iff `a ≤ i−1`, `b ≥ j+2` (`s − (j−i) − 2` pairs of separation `s`); a term that depends on one
of the two torsions only has zero mixed difference. ∎  Check (`out_e4.txt`): six-ring contacts only
(`w = 5`, one pair per separation 5): `c_i = 3`, bandwidth 2, row sums 3, for every `n = 6…10`.

**Local-frame metrics [P + N].**  Let `ξ_{ab}(X)` be the coordinates of atom `b` in the frame of
atoms `(a−1,a,a+1)`, and `D_F(X,Y) = Σ_{(a,b)∈𝓔} min(|ξ_{ab}(X) − ξ_{ab}(Y)|, d_c)` — a clamped
frame-aligned point error; an `SE(3)`-invariant, chirality-sensitive pseudo-metric.  A rotamer change
at `i` alters `ξ_{ab}` only if `a` and `b` lie on different sides of bond `i` (or `a` is the hinge
frame), so the single-torsion diameter of `D_F` is at most `d_c ·` (number of such pairs in `𝓔`):
`O(w² d_c)` for a sequence window, `≈ 2 d_c i(N−i)` for all pairs, the cross-contact count (hence
the zipper law) for a spatial cutoff.  Measured maxima (`out_e9.txt`, part vi; clamp `4b`): window
`w = 4`: 29.1 and `w = 8`: 176.9 at every interior torsion for `n = 20, 40, 80`; all pairs: 806,
3215, 12834.

*Reading.*  Constants are chain-length independent **iff the residual (or the metric) is local in
sequence**.  Then §11.4 applies with a fixed `c/e`: one evaluation if `c_i ≤ e_i`, otherwise the
rate `R*(e/c) < ln k` of the table in 2.3, uniformly in `n`, and the row-sum condition of §11.7 is
a fixed inequality.  Such a residual is a banded many-body model in torsion space — the regime the
existing kernels were built for.

### 2.6 Theorem G6 — second-order structure in torsion coordinates is the wrong structure for tertiary contacts

**Lemma (three rigid segments) [P].**  For torsions `i < j` and `g = Σ_{a<b} φ_{ab}(|X_a − X_b|)`,
the mixed second difference of `g` in `(i, j)` receives contributions only from pairs with
`a ≤ i−1` and `b ≥ j+2` (first segment against last segment).  Hence
`c_ij ≤ 2u ·` (largest number of such pairs within range in one of the four conformations), which
can be of order `min(i, n−j)`: the matrix `(c_ij)` is **dense and growing**, largest for neighbouring
central torsions.

**Numerics [N]** (`out_e4.txt`; contact count on the diamond chain).

| n | `c_i` (centre, phantom) | `½Σ_j c_ij` (centre, phantom) | SAW only | share of variance in orders ≤ 2 |
|---|---|---|---|---|
| 6 | 5 | 9.5 | 3.5 | 0.749 |
| 8 | 7 | 23 | 9 | 0.715 |
| 10 | 9 | 41.5 | 13.5 | 0.680 |

The row-sum condition of §11.7 (`½Σ_j c_ij ≤` excitation energy) fails by an amount that grows with
`n`.  The reason is the interaction order: the indicator of one contact `(a, a+s)` depends on the
`s−2` torsions of the loop and its ANOVA weight sits at orders `≈ 0.6 (s−2)`:

| loop torsions | P(contact) | variance share of orders ≤ 2 | dominant orders |
|---|---|---|---|
| 3 | 0.074 | 0.72 | 2–3 |
| 5 | 0.058 | 0.40 | 2, 4 |
| 7 | 0.038 | 0.11 | 4–6 |
| 9 | 0.031 | 0.058 | 6–7 |
| 11 | 0.025 | 0.032 | 6–8 |

A pair term in Cartesian space is a high-order term in torsion space.  Bounded mixed differences
"in the sites" are therefore not the structural assumption that fits chain geometry; additivity
lives in pair (feature) space (2.11).

### 2.7 General facts used below (any envelope, any finite space) [P, routine]

**(a) Monotonicity.**  If `d ≤ d'` are envelopes and `g` is admissible for `d`, then every
`ε`-cover for `d'` is one for `d`: `N_cov^{d} ≤ N_cov^{d'}`.  The best envelope of a class `𝒢` is
its support quasi-metric `d_𝒢(x,y) = sup_{g∈𝒢} [g(x) − g(y)]`.

**(b) Certificate size is the metric entropy of the low-energy set at its own scale.**  Zero
residual, `X_G = {gap ≤ G}`, `𝒩(S, r)` = least number of points of `X` whose `d`-balls of radius `r`
cover `S`.  Then for every `G` and every `0 = G_0 < G_1 < … < G_J` with `X_{G_J} = X`:

    𝒩(X_G, G + ε)  ≤  N_cov(ε)  ≤  1 + Σ_{j≥1} 𝒩(X_{G_j} \ X_{G_{j−1}}, G_{j−1} + ε).

(With a residual, replace `d` by the slack.)  This is the finite-scale form of the near-optimality /
zooming dimension of optimistic optimisation (§4).

**(c) State dependence.**  One evaluation at `x_0` certifies iff `d(x_0,y) ≤ f(y) − f(x_0) + ε` for
all `y` (Theorem 11.7 for general `d`): only the distances *from the minimiser* enter.  A
weighted-Hamming envelope must use the worst conformation of the domain; a metric envelope uses the
lever arms at `x_0` (2.1f: a factor 1.8–4.4 for an extended minimiser, `R_g√m` instead of `m^{3/2}`
for a compact one).

**(d) Hamming hull and capped Hamming.**  For a metric `D` on a product domain,
`D^H(x,y) = Σ_i c_i[x_i ≠ y_i]`, `c_i = max_{x,a} D(x, x^{i→a})`, is the smallest weighted-Hamming
envelope above `D`; `min(D^H, diam D)` is again an envelope, and it is still verified by the pairwise
kernel (two lower bounds, take the larger).  For the chain, `RMSD(X,Y)² ≤ R_g(X)² + R_g(Y)²`
(centre both, use `σ_1 + σ_2 − σ_3 ≥ 0`), so `diam ≤ √2 R_max ≤ 0.41 bN`, while
`Σ_i c_i ≈ 0.03–0.12 · L b N²`: the relaxation overshoots the diameter by a factor of order `N`.
With the cap, every `y` with at least `w_cap = ⌈0.41 λ N⌉` excitations is covered by the
ground state: `ln N_cov ≤ ln Σ_{w<w_cap} C(n,w)(k−1)^w ≈ n [h(0.41λ) + 0.41λ ln(k−1)]`
(`out_e11.txt`: 0.113, 0.198, 0.456, 0.959 nats per torsion for `λ = 0.05, 0.1, 0.3, 1`; no gain for
`λ ≥ 1.63`).  A one-line change in the kernel's envelope already divides the exponent by 5 at
`λ = 0.1` — and is still exponentially worse than 2.8.

### 2.8 Theorem G8 — the RMSD envelope used directly: a stretched-exponential certificate

Envelope `d(x,y) = L · RMSD(X(x), X(y))` on the product domain `[k]ⁿ` (no excluded volume), `f`
additive with `φ_i(t) = 0` and `e_min ≤ φ_i(s) ≤ e_max` for `s ≠ t`, zero residual.  The admissible
class is exactly the class of Corollary 4.7.

**Theorem G8 [P; the constant `η` is numerical].**
(a) *Upper bound.*  With `s_w = ⌊(w e_min + ε)/((1+√3) L b)⌋`,

    N_cov(ε) ≤ 1 + Σ_{w=1}^{n} min{ C(n,w)(k−1)^w ,  81^{⌈(N−1)/s_w⌉} }      (second entry only if s_w ≥ 1).

Consequently, for `e_min = e`, `ε = 0`, `λ = Lb/e ≤ N/ln(e(k−1)n)`:
`ln N_cov ≤ 4.91 √(λ N ln(e(k−1)n)) + ln(81(n+1))`.
(b) *Lower bound.*  Let `σ_0, σ_1` be two conformations of a block of `s ≥ 8` atoms, each with
exactly one `g⁺` among its `s−3` internal torsions, and `Δ_s = D_K(σ_0, σ_1)`.  For every `w` with
`ws ≤ N`,

    N_cov(ε) ≥ exp( w [ln 2 − h(ϑ)] ),    ϑ = 2N (w e_max + ε)² / (L² w Δ_s²),   provided ϑ ≤ ½,

and every randomised `(ε/2, δ)`-correct algorithm pays `(1−2δ)` times this.  With the kink at the
first internal torsion or at the centre, `Δ_s = η_s s^{3/2} b`, `η_s = 0.059…0.071` for
`8 ≤ s ≤ 20`, `→ 0.0659` (generic chain; `out_e6_b.txt`), which gives for `e_min = e_max = e`,
`ε = 0` and large blocks: `ln N_cov ≥ 0.197 √(η λ N) = 0.0506 √(λ N)` (as long as
`2/(ηN) ≤ λ ≤ 1.5 N`).
(c) Hence **`ln N_cov = Θ̃(√(L b N/e))`**, capped at `n ln k`: `√N` for RMSD-intensive `L`,
`N^{3/4}` for Frobenius-intensive `Λ`, and linear in `N` with rate between `0.0506 √(ℓb/e)` and
`min(ln k, max_μ min{h(μ) + μ ln(k−1), 24 ℓb/(eμ)})` for extensive `L = ℓN`.

*Proof of (a).*  All conformations are built from the same first three atoms.  For a block length
`s` record the positions of every `s`-th atom (and the last one) rounded to the grid `(sb)ℤ³`.  The
first sample is fixed and consecutive rounded samples differ by an integer vector of norm at most
`1 + √3`, of which there are 81; so there are at most `81^{⌈(N−1)/s⌉}` codes.  Two conformations
with the same code differ by at most `√3 sb` at the samples and by at most `(1+√3) sb` at every atom
(nearest sample within `s/2` bonds), so their RMSD — even without superposition — is at most
`(1+√3) s b`.  Conformations with exactly `w` non-trans torsions have gap `≥ w e_min`; one
representative per code, with `s = s_w`, covers them within the required slack radius; if `s_w < 1`
take all of them.  For the simplified form use `s_w ≥ w/(2(1+√3)λ)` (for `w ≥ (1+√3)λ`) and
`min(wA, B/w + c) ≤ √(AB) + c` with `A = ln(e(k−1)n)`, `B = 2(1+√3) ln 81 · λN`, `c = ln 81`. ∎
*Proof of (b).*  (1) *Block superadditivity:* for any partition of the atoms into blocks,
`D_K²(X,Y) ≥ Σ_blocks D_K²(X_B, Y_B)` (one motion for all blocks is admissible for each).  (2) The
shape of a block depends only on its internal torsions.  (3) Family: `w` blocks of `s` atoms, block
`j` in shape `σ_{z_j}`, `z ∈ {0,1}^w`, junction torsions trans; every member has exactly `w`
excitations.  If the centre `a` covers `y_z` then `D_K²(a, y_z) ≤ Θ := N(w e_max + ε)²/L²`, hence
`Σ_j cost_j(z_j) ≤ Θ` with `cost_j(0) = D_K²(a_{B_j}, σ_0)`, `cost_j(1) = D_K²(a_{B_j}, σ_1)`; by the
triangle inequality for `D_K`, `cost_j(0) + cost_j(1) ≥ Δ_s²/2`.  (4) For `α, β ≥ 0`,
`α + β ≥ 2τ`: `e^{−tα} + e^{−tβ} ≤ 1 + e^{−2tτ}` (because `(1−e^{−tα})(1−e^{−tβ}) ≥ 0`; **[L]**
`two_letter_moment`).  So one centre covers at most `min_t e^{tΘ}(1 + e^{−tΔ_s²/2})^w = e^{w h(ϑ)}`
members, and there are `2^w`.  The bound is of the weights form of Theorem 11.6(a), so Theorem
11.23(b) applies. ∎

*Remarks.*  (1) *The Hamming relaxation of the same class is exponentially worse.*  By G1(e) and G3,
every valid weighted-Hamming envelope of this class has
`ln N_cov ≥ n ln k − C_{k,3/2} ((G+ε)√N/(0.186 L b))^{2/5}`.  Explicit numbers (`out_e6_c.txt`,
`k = 3`, natural logarithms):

| λ | n | direct: lower | direct: upper | Hamming relaxation: lower | `n ln 3` |
|---|---|---|---|---|---|
| 0.1 | 10³ | 0.5 | 83.6 | 324.6 | 1098.6 |
| 0.1 | 10⁵ | 5.1 | 1002 | 96068 | 109861 |
| 1 | 10³ | 1.6 | 234.7 | 760.2 | 1098.6 |
| 1 | 10⁵ | 16.0 | 2937 | 104338 | 109861 |
| 10 | 10³ | 5.1 | 635.8 | 961.6 | 1098.6 |
| 10 | 10⁵ | 50.7 | 8458 | 107659 | 109861 |

and exactly, on small chains (`out_e5_small.txt`, `out_e5_n8.txt`; LP lower bound – greedy upper
bound of `N_cov`; `H-ver` = verified constants, `H-opt` = smallest valid constants `c_i*`, `R` = the
RMSD envelope):

| n (`3ⁿ` states) | L | H-ver | H-opt | R |
|---|---|---|---|---|
| 6 (729) | 2 | 41–57 | 21–24 | 3 |
| 6 | 4 | 153–185 | 137–161 | 16–20 |
| 7 (2187) | 2 | 75–99 | 32–48 | 4 |
| 7 | 4 | 327–419 | 198–268 | 21–24 |
| 8 (6561) | 2 | ≤ 206 | ≤ 98 | 4–6 |
| 8 | 4 | 723–961 | 452–649 | 26–31 |
| 8 | 8 | 2478–2945 | 1632–2257 | 462–530 |

At `L = 4` one more torsion multiplies the Hamming certificates by ≈ 2.2 and the direct one by
≈ 1.25.  At `L = 1` the direct envelope needs one evaluation for all `n ≤ 8` while H-opt needs
3, 5–6, 7–12, 12–19 for `n = 5, 6, 7, 8` (state dependence, 2.7c).
(2) *Mechanism.*  The critical number of kinks is `w* ≈ √(λN)`: with `w` kinks the gap radius is
`w e/L` in RMSD and the kink spacing is `N/w`; the two meet at `w*`.  Conformations with fewer kinks
must be resolved kink by kink, those with more are merged by the gap.  Layer data (`out_e6_e.txt`,
`n = 60`, two kinks, 7080 conformations): at `λ = 0.5`, 3 centres cover all 2894 that the ground
state does not; at `λ = 1`, at most 21 cover 5958.  (The RMSD between single-kink conformations is
`≈ 0.21 b` per position of kink displacement in the middle of a chain of 100 torsions.)
(3) *The constants are far apart* (0.05 against 4.9·√log).  Block superadditivity discards the
lever-arm displacement of the rest of the chain: in the family used in (b) the true squared
distances exceed the bound used in the proof by factors 2 to 2900 (`out_e6_d.txt`).  A kink-rounding
heuristic (`ln N_w ≈ w ln(Cλn/w²)`) suggests `ln N_cov ≈ c √(λN)` with `c` of order one and no
logarithm [H].
(4) *Cost of verification.*  The theorem counts residual evaluations.  A kernel that wants to
*check* such a certificate needs certified upper bounds on RMSD over boxes that saturate; the
verified chain rule is the `ℓ¹` (Hamming) bound, the cap of 2.7(d) is the first step, a multiscale
(block-wise) bound is open (§6).

*Classification.*  The statement was not found (searches in §4); the tools are the ε-entropy of
Lipschitz curves (Kolmogorov–Tikhomirov) and Chernoff counting.

### 2.9 Theorem G9 — finite temperature for arbitrary envelopes: residual-independence and metric entropy

**Lemma G9a (the spot-check constant does not depend on the residual) [L].**  For every finite `X`,
`f`, `g`, `d` and `β`, with `π` the Gibbs measure of `f + g` and `Λ` the soft gap of Theorem 11.24,

    π(y) e^{Λ(y)} = e^{−βf(y)} / Σ_a e^{−β(f(a) + d(a,y))},
    Ξ_β(f,d) := E_π[e^{Λ}] = Σ_y e^{−βf(y)} / Σ_a e^{−β(f(a)+d(a,y))} = Σ_y π_f(y) / Σ_a π_f(a) e^{−βd(a,y)}.

*Proof.*  `E(a) + s(a,y) = f(a) + d(a,y) + g(y)`: the residual at `a` cancels. ∎
(`lean/SoftGapIndep.lean`: `gibbs_mul_exp_softGap`, `sum_gibbs_exp_softGap_indep`,
`sum_dipWeight_indep`, stated with the repository's `softGap`, `slack`, `dipWeight`; random-instance
test `out_e8c.txt`, relative error `6·10⁻¹⁶`, asymmetric envelopes included.)
So the number of evaluations of the thermal spot-check of Theorem 11.26,
`⌈2 ln(1/δ) Ξ_β/(1 − e^{−ε/2})⌉`, is **the same for every instance of the class**; the half of the
sampling distribution that is proportional to `π e^Λ` is a function of `(f, d, β)` only; and as
`β → ∞`, `Ξ_β →` the (multiplicity-weighted) number of states that are optimal for some admissible
residual (the contact set of the theory report §2.3).

**Lemma G9b (metric-entropy bound) [L].**  If `X` is partitioned into cells such that `d(a,y) ≤ r`
whenever `a, y` are in the same cell, then `Ξ_β ≤ e^{βr} · #cells`.  Hence
`ln Ξ_β ≤ inf_r [βr + ln 𝒩*(X, d, r)]`, `𝒩*` the least number of sets of `d`-diameter `≤ r` covering
`X` (`≤ 𝒩(X, d, r/2)` for symmetric `d`).
*Proof.*  `Σ_a π_f(a)e^{−βd(a,y)} ≥ e^{−βr} π_f(cell(y))`, and `Σ_{y ∈ cell} π_f(y)/π_f(cell) = 1`. ∎
(`lean/SoftGapCover.lean`: `spotCheck_const_le_cover`; numerical check `out_e8b.txt`, `out_e8c.txt`.)

**Theorem G9 (chains) [P].**  For the RMSD envelope `d = L·RMSD` on the chain, *every* known part
`f` (additive or not), every `β ≥ 0` and every admissible residual,

    ln Ξ_β ≤ min_{s ≥ 1} [ (1+√3) β L b s + ln 81 · ⌈(N−1)/s⌉ ] ≤ 6.93 √(β L b N) + 2.73 β L b + 4.39,

so `ln Z` is certified to within `ε` with confidence `1−δ` by
`exp(O(√(βLbN))) · ln(1/δ)/(1 − e^{−ε/2})` evaluations (given the hint), at every accuracy.  For any
weighted-Hamming relaxation with lever-arm constants, by contrast, `ln Ξ_β → n ln k` and every
algorithm needs `k^{n−o(n)}` evaluations at every extensive accuracy (Theorem G3).
*Proof.*  The code cells of the proof of G8(a) have unsuperposed RMSD diameter `≤ (1+√3)sb`; apply
G9b and optimise `s`. ∎

Also, for every instance: `Λ(y) ≤ inf_r [2βLr − ln π(B(y,r))]` (zero residual: `βLr`), and one
evaluation at `x_0` pins `ln Z` within a window of width
`ln E_{π_f} e^{βd(x_0,Y)} − ln E_{π_f} e^{−βd(Y,x_0)} ≤ 2βL · max_y RMSD(x_0,y) ≤ 2βL (R_g(x_0)² + R_max²)^{1/2}`
(`π_f` = Gibbs measure of the known part; valid for every admissible residual).

**Exact small-chain values [N]** (`out_e8_n7.txt`, `out_e8_n8.txt`; `f = #gauche`; `U = ln Ξ_β`;
`W1` = width after one evaluation at the ground state):

| n | L | β | `n ln 3` | `U`: R | H-opt | H-ver | `W1`: R | H-opt | H-ver |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 2 | 1 | 7.69 | 1.75 | 5.41 | 5.84 | 4.10 | 12.9 | 16.8 |
| 8 | 2 | 1 | 8.79 | 1.93 | 6.40 | 6.80 | 4.67 | 16.4 | 20.4 |
| 8 | 4 | 1 | 8.79 | 3.73 | 7.97 | 8.14 | 9.73 | 34.1 | 42.4 |
| 8 | 4 | 2 | 8.79 | 5.82 | 8.54 | 8.62 | 16.2 | 62.5 | 79.0 |

From `n = 7` to `8` the spot-check exponent grows by 0.18 for the RMSD envelope and by 0.99
(`≈ ln 3`) for the Hamming relaxations.  The explicit bound of Theorem G9 is vacuous at these sizes
(it becomes non-trivial for `N ≳ 40 βLb`); with exact covering numbers Lemma G9b gives 5.8 against
the true 1.75 (`out_e8b.txt`).

*Classification.*  G9a is an identity that is not stated in the repository (the text expresses `U_β`
through `π` and `s`, i.e. as if it depended on the instance); elementary.  G9b is a standard
covering argument.  A matching randomised *lower* bound for the RMSD envelope is not proved (§5).

### 2.10 Theorem G10 — the contact-map metric: per-contact sharpness, and what it cannot do

Features `χ_p(x) ∈ {0,1}` (`p` = a pair of atoms; `χ_p = 1` iff in contact), class
`𝒢_u = {Σ_p ε_p χ_p : |ε_p| ≤ u_p}`.  Its support metric (2.7a) is the weighted symmetric
difference of contact maps, `d_C(x,y) = Σ_p u_p |χ_p(x) − χ_p(y)|`; it is invariant, and it is not
a weighted-Hamming metric in torsion coordinates.

**(a) Per-contact sharpness [L].**  Let `f = f_0 + Σ_p θ_p χ_p`.  If `u_p ≤ −θ_p` for the contacts
present in `x_0`, `u_p ≤ θ_p` for the absent ones, and `x_0` minimises `f_0`, then
`d_C(x_0,y) ≤ f(y) − f(x_0)` for all `y`: **one evaluation at `x_0` is an exact certificate, for
every chain length** (`lean/ChainLemmas.lean`: `contact_sharp`).  In general `x_0` is certified iff
it minimises the pessimistic model `f_0 + Σ_p (θ_p + σ_p u_p) χ_p` (`σ_p = +1` on the contacts of
`x_0`, `−1` off them) — a model *of the same form as* `f`, so the check is one ordinary
minimisation.

**(b) The weighted-Hamming envelope of the same class is not sharp [N].**  Gō-type synthetic
instance on self-avoiding diamond chains: `f = 0.10·#g⁺ + 0.15·#g⁻ − |C ∩ C_nat| + |C \ C_nat|`,
native = hairpin with arms of `p` torsions and `h = p/2+1` contacts; `u_C`, `u_H` = largest residual
amplitude `u_0` for which one evaluation certifies under `d_C`, respectively under the weighted
Hamming envelope with the smallest valid constants (`out_e7_c.txt`):

| p | n | h | `u_C` | `u_H ≤` (mirror turn) | `u_H ≤` (best contact-changing local move) |
|---|---|---|---|---|---|
| 4 (exhaustive, 145379 SAWs) | 11 | 3 | 0.883 | 0.0033 | — |
| 16 | 35 | 9 | 0.961 | 0.0019 | 0.193 |
| 64 | 131 | 33 | 0.989 | 0.00051 | 0.198 |
| 128 | 259 | 65 | 0.995 | 0.00026 | 0.199 |

(`u_C ≥ min(ε_0, ε_1) − 0.35 = 0.65` is proved: a conformation with the native contact map contains
the six-ring turn, hence three gauche torsions; the values for `p ≥ 16` are minima over all changes
within windows of five torsions, hence upper bounds.)  Two mechanisms: a move that changes `≈ h`
contacts by re-routing the turn flips several central torsions, each of which *alone* would change
`≈ h` contacts, so the Hamming distance is `≈ 5 h u_0` against a true change of `h` — a constant
factor 5; and the mirror-image turn `g⁻g⁺g⁻` has the *same* contact map (`d_C = 0`) and a tiny
`Δf`, but Hamming distance `3h u_0` — the threshold decays like `1/h`.  The Hamming format cannot
see that hinge motions cancel.

**(c) Without a contact-structured known part the contact metric is still exponential [P + N].**
Phantom diamond chain, `f = e·#gauche`, `u_p = u_0`, zero residual.  Take blocks of `2p+6` atoms,
each either all-trans or a hairpin `t^p g⁺g⁻g⁺ t^p` (three excitations, `h = p/2+1` contacts inside
the block; contacts inside a block depend on its internal torsions only).  For every centre the two
block costs add up to at least `h u_0`, and the counting of Theorem 11.8 (with the moment bound of
G8) gives, whenever `h u_0 > 3e`,

    ln N_cov(ε) ≥ ⌊N/(2p+6)⌋ · R*_bin(3e/(h u_0)) − t*ε,      R*_bin(ρ) = max_x [ln(1+x) − ln(1+x^{1/ρ})].

Optimising `p`: rates `≥ 0.0020, 0.0039, 0.0077, 0.0144, 0.0260` nats per torsion for
`u_0/e = 0.25, 0.5, 1, 2, 4` (`out_e7d.txt`) — positive for **every** `u_0 > 0`: with a purely
torsional known part a long chain is never sharp against contact residuals (a hairpin of
`h > 3e/u_0` contacts may be stabilised by the unknown part).  The family is self-avoiding for all
members that were enumerated (`2⁸` members at `p = 2, 4`; `2⁶` at `p = 6`).

**(d) Sizes [N]** (`out_e7_a.txt`; phantom domain, `f = #gauche`, zero residual; LP bound – greedy;
`H` = best valid weighted-Hamming envelope `c_i = u_0 z_i`; `C` = contact metric; last column = 2.11):

| n | distinct contact maps | `u_0 = e`: H | C | `u_0 = 2e`: H | C | `u_0 = 4e`: H | C | rank |
|---|---|---|---|---|---|---|---|---|
| 6 | 17 | 83–103 | 1 | 305–345 | 3 | 729 | 10 | 7 |
| 7 | 43 | 359–452 | 2 | 1654–1675 | 5 | 2187 | 14 | 10 |
| 8 | 101 | 955–1280 | 3 | 3861–4065 | 8–10 | 6561 | 25–26 | 13 |
| 9 | 276 | ≥ 661 | 3–4 | ≥ 2348 | 14–18 | ≥ 5397 | 57–58 | 17 |
| 10 | 708 | ≥ 1814 | 4–7 | ≥ 6498 | 25–31 | ≥ 15139 | 115–129 | 21 |

The contact metric gains two to three orders of magnitude at these sizes; at `u_0 = 4e` its
certificate doubles with every torsion from `n = 8` on and passes the rank at `n ≈ 8`.

*Classification.*  (a) is immediate once the metric is chosen; choosing the support metric of the
class in *feature* space, and the resulting length-independent sharpness condition, is the point.

### 2.11 Theorem G11 — the class is linear: polynomially many evaluations, always

**[P, routine; N].**  If the residual is `g_ε = Σ_p ε_p χ_p` with known features and unknown
coefficients, then the values of `g` on any set `A` whose feature vectors `(1, χ(a))` span those of
`X` determine `g` on all of `X`: `r = rank ≤ P + 1` evaluations, non-adaptively, for every functional
(minimum, `ln Z`, any `β`, any accuracy), whatever the amplitudes `u_p`.  If `g` is only
`η`-close to the class in sup norm, a barycentric spanner (coefficients `|α_j(y)| ≤ 1`) pins `g`
everywhere to within `(1 + ‖α(y)‖₁) η ≤ (1 + r) η`.
Numbers (`out_e7_b.txt`, `out_e9e.txt`, `out_e7d.txt`): contact features of the diamond chain have
full rank `P + 1 = 7, 10, 13, 17, 21, 26, 31` for `n = 6, …, 12` (`P = Σ_{odd s ≥ 5} (N − s) ≈ N²/4`),
on the phantom and on the SAW domain; a swap-algorithm spanner has `max_y ‖α(y)‖₁ = 3, 7, 7.6, 10`
for `n = 6, 8, 10, 12`.
*Contrast.*  The first-order envelope `d_C` is the tightest envelope that contains this class, and
under it the cost is exponential (G10c); the gap between a parametric class and its Lipschitz hull
is the gap between `O(N²)` and `exp(Ω(n))`.  In the language of §11.7: the "star" should be taken in
feature coordinates, where the mixed differences vanish identically, not in torsion coordinates,
where they are dense (G6).

### 2.12 Which regimes are certifiable according to the theory

`e` = excitation energy of the known torsional part, `λ = Lb/e`, `m_i = min(i, n+1−i)`.

| residual class | envelope format | constants | one evaluation iff | otherwise |
|---|---|---|---|---|
| `L`-RMSD-Lipschitz (Cor. 4.7) | weighted Hamming, verified | `0.82 L b m_i^{3/2}/√N` | `L ≤ 3.4 e/(bN)` | `n ln k − O(n^{3/5})`; same for randomised algorithms and for `ln Z` at every extensive accuracy (G3) — **not certifiable** |
| same | Hamming capped at the diameter | same | same | rate `≤ h(0.41λ) + 0.41λ ln(k−1)` per torsion (2.7d) |
| same | RMSD metric itself | — | `L·RMSD(x*,y) ≤ gap(y)` ∀y (lever arms at `x*` only) | `Θ̃(√(λN))` (G8); `ln Z`: `exp(O(√(βLbN)))` randomised (G9) — certifiable in the query count for RMSD-intensive `L`; needs a kernel that bounds RMSD over boxes |
| extensive local residual (`L` of order `N`, G2) | any RMSD form | `≥ 0.6√n … 0.025 n²` × exact | never for large `N` | `exp(Θ(n))`; rate `ln k` (Hamming) or `Θ̃(√(ℓb/e))` (direct) — **use torsion or feature envelopes instead** |
| sequence-local, window `w` | weighted Hamming, exact | `≤ u (w−1)(w−2)/2`, uniform in `n` | `c_i ≤ e_i` | rate `R*(e/c) < ln k`, uniform in `n` (G5) |
| contacts, amplitude `u_0` | best weighted Hamming | `≥ u_0 ⌊(m_i−1)/2⌋` | `u_0 ≲ 2e/n` | `n ln k − O(√(n e/u_0))` (G4) — **not certifiable** |
| same | second-order in torsions | `½Σ_j c_ij` grows with `n` | row-sum condition fails | star data useless beyond short loops (G6) |
| same | contact-map metric | per contact | contact-structured known part with `u_p ≤ abs(θ_p)` (G10a), any length; torsion-only known part: never beyond `n ≈ 12 e/u_0` | exponential with a small rate `≥ 0.19/(24e/u_0 + 6)`; 10²–10³ times smaller than Hamming at `n ≤ 10` |
| same, as a linear class | none (parametric) | — | — | `≤ P+1 = O(N²)` evaluations always (G11) |

---

## 3. Numerical studies (what, sizes, results)

All code is in this directory; `chainlib.py` (builder, Kabsch, inertias, lattice contacts, set-cover
LP/greedy/MILP) is tested by `t0_selftest.py` (bond lengths/angles/dihedrals, torsion move = axis
rotation, Kabsch against 20000 random rotations, zigzag closed form, lattice sanity).

| script → output | what | sizes | used in |
|---|---|---|---|
| `e1_constants.py` → `out_e1.txt` | lever-arm constants: min-inertia bound, coaxial cost, exact Kabsch; extended / helical / compact / coil; uniform maximum; exhaustive exact maxima | `n = 30…240`; arms `m ≤ 12` exhaustive, `m ≤ 200` patterns; all `3ⁿ`, `n ≤ 8` | G1 |
| `e2_hamming_predictions.py` → `out_e2.txt` | §11 predictions for the lever-arm Hamming envelope: sharp sites, `max_t Σ_i max_v r_i`, deficit against G3, soft gaps, `U`, `ε_crit`, randomised bound; cross-check against exact LP | `n = 10…2000`; LP on 729 states | 2.3 |
| `e3_zipper.py`, `e3b_hairpin.py` → `out_e3a.txt`, `out_e3b.txt` | zipper numbers, exhaustive; hairpin motif search and single-flip contact loss | all `3ⁿ`, `n ≤ 12` (531441); hairpins up to `n = 643` | G4 |
| `e4_secondorder.py` → `out_e4.txt` | first and mixed second differences of the contact count, SAW/phantom/local; ANOVA spectra | `n = 6…10`; loops up to 11 torsions (177147 states) | G5, G6 |
| `e5_small_cover.py` → `out_e5_small.txt`, `out_e5_n8.txt` | exact `N_cov` (LP/greedy/MILP) under H-ver, H-opt and the RMSD envelope | all pairs of `3ⁿ` conformations, `n = 5…8` (43·10⁶ Kabsch pairs) | G8 |
| `e6_stretched.py` → `out_e6_a…e.txt` | block superadditivity (3000 random trials, minimum `−4·10⁻¹⁶`); `η_s`; explicit bounds of G8 and the Hamming lower bound; packing in a block family; layer covers | formulas up to `n = 10⁶`; families of 256–1024 conformations, `N ≤ 300`; layers `w ≤ 2`, `n ≤ 100` | G8 |
| `e7_contact.py`, `e7d_blocks_spanner.py` → `out_e7_a/b/c.txt`, `out_e7d.txt` | contact class: `N_cov` under Hamming and contact metric; rank; Gō-type thresholds; hairpin-block family; spanner | `n ≤ 10` (59049 states, 708 contact maps); hairpins `n ≤ 259`; rank up to `n = 12` | G10, G11 |
| `e8_thermal_small.py`, `e8b_entropy_bound.py`, `e8c_identity.py` → `out_e8_n7/n8.txt`, `out_e8b.txt`, `out_e8c.txt` | exact soft gaps, `U`, one-evaluation width, Jensen-gap brackets; G9b with exact covers; G9a on 300 random (also asymmetric) instances | `n = 7, 8`; random spaces of 4–40 points | G9 |
| `e9_aux.py`, `e9b…e9e` → `out_e9.txt`, `out_e9b…e.txt` | zipper at every position; `ρ^sym(m) ≥ 0.186 m^{3/2}` for all `m ≤ 240`; helix law; code cells; effective Lipschitz constants; clamped frame metric; extensive-`L` pairs; equal-frame words; maximal span; ranks for odd `n` | `n ≤ 480`; words `u ≤ 8`; `n ≤ 800` | G1, G2, G4, G5, G11 |
| `e10_matching.py` → `out_e10.txt` | gauche-count residual under torsion / RMSD / verified-Hamming envelopes | `n = 5, 6, 7` | 2.2 |
| `e11_summary_numbers.py` → `out_e11.txt` | contact-Hamming lower bounds, capped Hamming, sharpness thresholds | `n ≤ 10⁴` | 2.3, 2.4, 2.7 |
| `e12_smallball.py` → `out_e12.txt` | Monte Carlo of `P(RMSD ≤ r)` between random coils | `n = 50…400`, 2.25·10⁶ pairs each | §5 (heuristic) |
| `lean/SoftGapIndep.lean`, `lean/SoftGapCover.lean`, `lean/ChainLemmas.lean` | G9a, G9b, G10a, moment bound of G8 | compiled with `lake env lean` (≈ 6 s each); axioms `propext, Classical.choice, Quot.sound` | [L] |

Negative or corrective numerical findings:

1. The bound `zip_i ≥ ⌈m_i/2⌉` that the first runs suggested is false at the middle torsion(s)
   (`n = 13`: 3 contacts, not 4); the correct statement is `⌊(m_i−1)/2⌋`.
2. The first candidate for extensivity of `L` on the generic chain (two helices with almost equal
   rise) drifts apart (RMSD 1.16 → 1.23 for `n = 48 → 192`), so it proves nothing asymptotically; the
   lattice construction of G2(b) is exact.  Pure-translation torsion words on the diamond lattice
   never differ in gauche count up to length 6; equal *frames* with different counts first appear at
   length 5.
3. For torsion-additive residuals the maximal ratio `|Δg|/D_K` is not attained by a single end flip
   but by collective changes (`out_e9.txt`, part v) — a "Frobenius-intensive" constant is not what a
   local residual has.
4. Block superadditivity is a very lossy lower bound on RMSD (`out_e6_d.txt`), which is why the
   constant of G8(b) is small; and the first choice of block shapes (kinks at ¼ and ¾) was worse
   (`η = 0.043`) than first-versus-centre (`0.066`).
5. The Brownian small-ball constant overestimates `−ln P(RMSD ≤ r)` between random coils by a
   factor 2–5 at accessible radii (`out_e12.txt`); only the scaling form `−ln P = Φ(r/⟨RMSD⟩)` is
   confirmed.
6. Among contact-changing local moves of a hairpin the Hamming threshold is a constant factor 5
   below the contact-metric threshold, not vanishing; the `1/h` decay needs a quasi-degenerate
   alternative (the mirror turn).  A first version of the Gō instance was exactly degenerate (mirror
   turn with `Δf = 0`); the chirality splitting `0.10/0.15` removes this.
7. At small sizes the explicit bounds of G8/G9 are vacuous (constants), and for a residual that
   saturates its own RMSD envelope the direct certificate is tiny (1–4 points for the gauche count
   at `n ≤ 7`), so the lower bound of G8 is specific to residuals well inside the class.

---

## 4. Prior art and search log

What is known (and how I know it):

* *Lever arms.*  That small torsion changes produce large, non-local Cartesian displacements is
  folklore in torsion-space modelling ("lever-arm effect"); the reduced-inertia bounds are those of
  the theory report §4.4 (Pitzer–Gwinn, Gō–Scheraga, Noguti–Gō etc., cited there).  The closed
  form for the zigzag and the `m^{3/2}` law are immediate.  [search summaries only]
* *RMSD and covering.*  Reva–Finkelstein–Skolnick (Folding & Design 1998) estimate how many compact
  structures are needed to come within a fixed RMSD of a given one by chance — an empirical covering
  statement, exponential in length at fixed radius [abstract via search summary; no data used here].
  ε-entropy of fragment conformations appears in a 2015 arXiv note on fragment libraries [search
  summary].  Kolmogorov–Tikhomirov (1959): the ε-entropy of Lipschitz functions on an interval is
  `≍ (length × Lipschitz constant)/ε` — the mechanism of G8(a) [secondary source via search summary].
  Berger (1970): the rate–distortion function of the Wiener process under mean-squared error is
  `R(D) = 2σ²/(π²D)` nats per unit time [formula read in a summary of Kipnis–Goldsmith–Eldar,
  arXiv:1608.04679; not used in a theorem].  Small-ball probabilities of Brownian motion in `L²`
  (`−ln P ~ 1/(8ε²)`) [from memory, not re-verified].
* *Gap-scaled covering.*  2.7(b) is the finite-scale form of the near-optimality dimension (Munos
  2011) / zooming dimension (Kleinberg–Slivkins–Upfal 2008) and of the covering picture of
  Bachoc–Cesari–Gerchinovitz (2021) already cited in the theory report [search summaries].
* *Metrics.*  lDDT (Mariani et al. 2013) is a superposition-free score built from distances within
  an inclusion radius; frame-aligned point error with a clamp (Jumper et al. 2021) restricted to a
  sequence window is the local-frame metric of 2.5; contact-map overlap and Gō-type energy functions
  are standard in polymer and lattice models [lDDT: search summary; the rest from memory and from
  the theory report].
* *Barycentric spanners*: Awerbuch–Kleinberg (2004) [search summary].
* *Lattice chains*: rotational-isomeric-state chains on the diamond lattice, the six-ring closure
  `g⁺g⁻g⁺` and adjacent re-entry folds are textbook polymer physics [from memory].

What was not found: the stretched-exponential law of G8 for certificates under an RMSD envelope and
its separation from the Hamming relaxation; the zipper bound stated as a lower bound on envelope
constants; the per-contact sharpness condition as a certification statement; the residual-independence
of `E_π e^Λ` (this is internal to the repository's framework; it is not in the theory report, the
blueprint, the research log or `SoftGapBounds.lean`).  None of these is deep; I claim them as
*apparently new consequences* with medium confidence — the searches below were short.

Search log (web search tool; I read only the result summaries it returned, never a full paper):

1. "number of chain conformations within RMSD … covering number conformational space polymer" — no
   direct treatment found.
2. "Berger 1970 Information rates of Wiener processes rate distortion function" — reference
   confirmed; formula taken from the fetched summary of ar5iv 1608.04679.
3. "near-optimality dimension zooming dimension Lipschitz optimization packing" — definitions
   (Munos 2011; Grill–Valko–Munos 2015; Bouttier et al. 2020).
4. "Sullivan Kuntz Conformation spaces of proteins RMSD dimensionality" — reference only.
5. "Reva Finkelstein Skolnick 1998 probability of a chance prediction … rmsd" — abstract-level summary.
6. "lever arm effect torsion angle space … RMSD" — qualitative statements only.
7. "Kolmogorov Tikhomirov epsilon-entropy Lipschitz functions" — secondary statement of `H_ε ~ cL/ε`.
8. "lDDT … FAPE … definition" — lDDT definition; FAPE not returned (taken from the theory report).
9. "epsilon-net covering conformational space RMSD … fragments" — fragment libraries; no scaling law
   with chain length.
10. "Awerbuch Kleinberg barycentric spanner" — definition confirmed.
11. "small ball probability Brownian motion L2 norm" — context only; constant not confirmed.

---

## 5. What I did not settle

1. **Constants and the logarithm in G8.**  Lower `0.0506 √(λN)`, upper `4.91 √(λN ln(e(k−1)n))`.
   The truth is probably `c √(λN)` with `c = O(1)`; a proof needs a lower bound on RMSD that keeps
   the lever-arm displacement (the family is separated far better than block superadditivity shows)
   and an upper bound by kink rounding with vector balancing instead of a uniform grid.
2. **Extensive `L`, exact rate.**  For `L = ℓN` the rate lies between `0.05 √(ℓb/e)` and the type
   optimisation in G8(c).  I expect a rate–distortion formula for the "kink process" under
   squared-error distortion of the *positions* (Berger's Wiener-process function is the
   coarse-grained limit: `≈ 6 C_∞ b²/(π² r²)` nats per bond at RMSD radius `r` for coil-like types)
   [H]; not derived.  The Monte Carlo check of the underlying small-ball law is only qualitative.
3. **Randomised lower bounds for metric envelopes at finite temperature.**  G9 is an upper bound.
   The typical soft gap under the RMSD envelope should scale like `(βLb)^{2/3} n^{1/3}` (tube
   entropy `∝ n b²/r²` against `βLr`) [H], which would put the randomised exponent between `n^{1/3}`
   and `n^{1/2}`; this is the two-measure isoperimetric problem of workstream A on path space with
   the RMSD metric.
4. **`ρ^sym(m) ≥ 0.186 b m^{3/2}`** is computed for all `m ≤ 240` (minimum 0.1875) and supported by
   the thin-rod limit 0.1863, not proved for all `m`.  **G2(b)** is exact on the diamond lattice
   only.  The planar-zigzag maximality used for the tables is classical but I did not prove it (the
   certified bound of G1(c) does not need it).
5. **Excluded volume.**  G3, G8 and G10(c) are stated on the product (phantom) domain.  With a
   hard-core term in `f` the landscape is not a product; the block families used in the lower bounds
   are self-avoiding in all enumerated cases, but no general statement is proved, and the
   weighted-Hamming theory on a non-product domain was not developed.
6. **Contact metric, true rate.**  Between the lower bound of G10(c) (0.008 per torsion at `u_0 = e`)
   and the growth seen at `n ≤ 10` (×1.6–2 per torsion at `u_0 = 2e…4e`) there is room; the number
   of distinct contact maps itself grows like `≈ 2.7ⁿ`, so the contact metric does not reduce the
   *asymptotic* rate by much unless the known part is contact-structured.
7. **Non-zero residuals.**  G8 and G10(c) are for the zero residual; with a residual that nearly
   saturates the envelope the slack balls are anisotropic (`out_e10.txt`).
8. **Continuous torsions** (voxelised boxes): all statements are for rotamer sets; for small changes
   `δ` the constants scale with `sin(δ/2)` and steep pair terms bring back the lever arm
   (`|∂g/∂φ_i| ≤ ℓ Σ_{cross contacts} ρ`), not analysed.

---

## 6. The three most promising next steps

1. **Give the kernel a non-product residual interface in feature space.**  Replace
   "constants `c_i` per torsion" (blueprint §7) by "amplitudes `u_p` per pair feature": the envelope
   is `Σ_p u_p|χ_p(x) − χ_p(y)|`, the pessimistic model of an anchor is again a pairwise
   (contact-additive) model, so `verifyR` generalises with the same leaf rules; G10(a) is the
   sharpness criterion, G11 the "learn-then-certify" route (evaluate a barycentric spanner, certify
   the fitted model, bound the misfit `η`), and §11.7's second-order class should be re-stated in
   feature coordinates (mixed differences of *contacts*), which is where it is sparse.  Open
   mathematics: lower bounds for the linear class with tolerance, and features that are not
   indicator functions (distance bins).
2. **A certified, saturating upper bound for RMSD over boxes.**  G8/G9 show that the whole
   exponential price of the RMSD route is the `ℓ¹` chain rule.  Needed: a machine-checkable bound of
   the form `D_K(x,y) ≤ F(set of changed torsions)` that is sub-additive across scales (a change
   inside a block of `s` atoms costs at most `O(s b √N)` plus a rigid re-placement of the rest, which
   the superposition partly absorbs), ideally the Eckart-frame `ℓ²` bound left open in §4.4.  The
   capped Hamming envelope of 2.7(d) is a zero-cost first step with a quantified gain.
3. **Sharpen G8/G9 into exact exponents.**  (i) Remove the logarithm and determine the constant of
   `√(λN)`; (ii) the rate for extensive `L` as a rate–distortion function of rotamer sequences under
   positional squared error; (iii) the randomised finite-temperature exponent for metric envelopes,
   using Lemma G9a (the sampler's hint-free half) — does a hint-free algorithm reach `Ξ_β`?  This
   connects to workstreams A (isoperimetry with two measures) and D (soft gaps): the identity
   `Ξ_β = Σ_y π_f(y)/(K_β π_f)(y)`, `K_β(a,y) = e^{−βd(a,y)}`, holds for every envelope and every
   instance and may simplify their statements too.

---

## 7. File list

* `REPORT.md` — this file.
* `chainlib.py`, `t0_selftest.py` — library and self-tests.
* `e1_constants.py` … `e12_smallball.py` — experiments (see §3); outputs `out_*.txt`.
  `cache_rmsd_n5…8.npy` — cached pairwise RMSD matrices of the generic chain (172 MB for `n = 8`).
* `lean/SoftGapIndep.lean`, `lean/SoftGapCover.lean`, `lean/ChainLemmas.lean` (outputs
  `lean/*.out`) — scratch Lean 4 files, checked with `lake env lean <file>` from the
  repository root (read-only use of the built library; no `lake build`).
