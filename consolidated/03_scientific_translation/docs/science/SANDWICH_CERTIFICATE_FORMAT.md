# The sandwich certificate, Stage 1 — format `metricchain-sandwich/1`

*Science division, branch `research/scientific-translation`.  Written 27 November 2026 for the engineering
division's two-stage proposal (ENG-MSG-0007 §3 (d), accepted in SCI-RES-0042).  Files, producer, reference
checker, controls and test vectors: `experiments/science/sandwich_cert/`.  Sent as SCI-MSG-0036.*

**What this note is.**  A specification from which a second checker can be written without reading our code:
what a certificate file contains, what it asserts, what a checker must verify and in which arithmetic, and
what is *not* verified at this stage.  **What it is not.**  It is not a proof that the two-sided bounds of
our workstreams P3 and P6 are correct.  Stage 1 checks the part of the argument that is finite arithmetic on
published numbers; the part that needs the force field (the sums of step A, the evaluated values, the
bracketing of the evaluated part) enters as **data taken as given** and is Stage 2.  A file accepted by a
Stage 1 checker therefore yields a **conditional** statement, and every sentence that quotes one must carry
the condition.

Reading level of everything below: **[P]** proved here (the lemma of §5, by a counting argument written
out); **[T]** tested (the checker, by the controls of §8); nothing here is machine-checked.

---

## 1. The statement

Sites `0, …, n−1`; site `i` has states `0, …, k_i−1`; a state of the system is `x = (x_0, …, x_{n−1})`.  An
**anchor** state `x⁰` is fixed; `S(x) = {i : x_i ≠ x⁰_i}` is the set of changed sites.  A site with `k_i = 1`
is *inactive* (it is never changed).  The energy is `E = f + g` (kcal/mol), `f` a sum of a constant,
one-site and two-site terms, `g` an arbitrary function of the state.  `I_M g` is the anchored expansion of
`g` truncated at order `M`:

    I_M g(x) = Σ_{U ⊆ S(x), |U| ≤ M} d_U(x_U),      d_U(x_U) = Σ_{V ⊆ U} (−1)^{|U|−|V|} g(x_V ; x⁰ elsewhere).

A **band model** of width `w` is a function `t(x) = const + Σ_i one_i(x_i) + Σ_{i<j≤i+w} pair_{ij}(x_i, x_j)`.
The certificate has order `m ≥ 2` (so `M = m − 1`) and contains four band models with integer tables in a
stated unit `2^u` kcal/mol (`u ≤ 0`): `A_lower`, `A_upper`, `m_lower`, `m_upper`.

**Statement certified by an accepted file, under the data assumptions (G1)–(G3) of §2:**

    m_lower(x) ≤ E(x) ≤ m_upper(x)  at every state x,     and hence
    claim.lnZ_lower ≤ ln Z(m_upper) ≤ ln Z(E) ≤ ln Z(m_lower) ≤ claim.lnZ_upper,

where `Z(t) = Σ_x exp(−β · 2^u · t(x))` for an integer-valued model `t` and `Z(E) = Σ_x exp(−β E(x))`, with
`β` the rational number in the file (per kcal/mol).

## 2. The data taken as given

`g̃` denotes the **evaluated** values of `g` — one double-precision number for every state that differs
from the anchor at no more than `M` sites — and `I_M g̃` the expansion above formed from those numbers **in
exact arithmetic**.

* **(G1)** `2^u·A_lower(x) ≤ f(x) + I_M g̃(x) ≤ 2^u·A_upper(x)` at every state `x`.
* **(G2)** There are constants `c_T ≥ 0`, one for every set `T` of `m` sites, with
  `|g(x) − I_M g(x)| ≤ Σ_{T ⊆ S(x)} c_T` at every state, such that the sums
  `Γ^{(−A)} := Σ_{T ∩ A = ∅} c_T` lie in the intervals published in the file for `A = ∅`, for every
  one-site `A = {i}`, and for every **in-band** pair `A = {i, j}`, `0 < j − i ≤ w`.
* **(G3)** `|g̃(y) − g(y)| ≤ ε_g` at every evaluated state `y`, with `ε_g` the rational number in the file.

*What our pipeline claims about them* (workstreams P3 and P6; details in §9): (G2) is P3's Proposition 1
with Theorem 3 (term-by-term bounds `ĉ_T` on the mixed differences of the GBn2 polarisation energy, anchored
mode) and Proposition 4 (their sum over all `m`-subsets in closed form, extended in P6 to the subsets that
avoid one site or a pair of sites); (G1) is the
construction of P3's Theorem 5 (pairs beyond the band and terms of order 3 to `M` replaced by minorants and
majorants on at most two in-band sites); (G3) is an allowance, `ε_g = 10⁻⁷` kcal/mol, against a measured
error of `1.8·10⁻¹²`.  All three are **[P] with stated floating-point allowances, tested by enumeration
wherever the state space could be enumerated, not machine-checked** — which is exactly why they are Stage 2.

## 3. The file

One JSON object (RFC 8259), UTF-8.  **Every number in the file is an integer literal**; a checker must
reject a file that contains a number with a fraction or an exponent, a duplicate key in any object, a key
not listed here, or a missing key (`annotations` alone is optional).  Integers are unbounded (the entries of
our files need up to 46 bits and a sign; a checker must not read them as doubles).

| key | content |
|---|---|
| `format` | the string `metricchain-sandwich/1` |
| `unit_log2` | integer `u`, `−200 ≤ u ≤ 0`; all table entries, penalties and step-A ends are integers in units of `2^u` kcal/mol |
| `beta` | `{"num": p, "den": q}`, positive integers; `β = p/q` per kcal/mol |
| `eps_g` | `{"num": p, "den": q}`, positive integers; `ε_g = p/q` kcal/mol |
| `instance` | `{"n", "k", "anchor", "order_m", "band_w"}`: `n ≥ 1`; `k` a list of `n` integers `≥ 1`; `anchor` a list of `n` integers with `0 ≤ anchor[i] < k[i]`; `order_m = m ≥ 2`; `band_w = w` with `1 ≤ w ≤ max(1, n−1)` |
| `stepA` | `{"Gamma": [lo, up], "Gamma_minus_i": [[lo, up], …  n entries], "Gamma_minus_ij": {"i,j": [lo, up], …}}`; integers `0 ≤ lo ≤ up`; the keys of `Gamma_minus_ij` are **exactly** the in-band pairs, written `"i,j"` with `i < j` in decimal without spaces |
| `penalty` | `{"c": c, "a": [a_0, …, a_{n−1}], "b": {"i,j": b_ij, …}}`; integers `≥ 0`; keys of `b` exactly the in-band pairs |
| `A_lower`, `A_upper`, `m_lower`, `m_upper` | each `{"const": integer, "one": [[k_0 integers], …, [k_{n−1} integers]], "pair": {"i,j": [[…]], …}}`; `pair["i,j"]` has `k_i` rows of `k_j` integers, entry `[x][y]` belonging to `x_i = x`, `x_j = y`; keys exactly the in-band pairs (a pair without interaction carries a table of zeros) |
| `claim` | `{"lnZ_lower": {"num", "den"}, "lnZ_upper": {"num", "den"}}`; integers, `den > 0` |
| `annotations` | optional object, free content; **not read by any checker**, and nothing in it is certified |

The **in-band pairs** are all `(i, j)` with `0 ≤ i < j ≤ n−1` and `j − i ≤ w`.

## 4. The checks

A checker performs the five groups below.  The **verdict** (accepted / rejected) is normative: two checkers
must agree on it for every file.  The label of the first failing check is informative; the reference checker
tests in the order W, A0 (intervals), B3, B1, B2, D, A0 (tables), E, and the test vectors of §8 name the label
it reports.

Notation.  `[Γ̲, Γ̄]`, `[Γ̲_i, Γ̄_i]`, `[Γ̲_ij, Γ̄_ij]` are the published intervals of `Γ`, `Γ^{(−i)}`,
`Γ^{(−i,−j)}`.  From them, in exact integer arithmetic,

    S̄_i  = Γ̄ − Γ̲_i,                         S̲_i  = max(0, Γ̲ − Γ̄_i),
    Ḡ_ij = Γ̄ − Γ̲_i − Γ̲_j + Γ̄_ij,            G̲_ij = max(0, Γ̲ − Γ̄_i − Γ̄_j + Γ̲_ij)        (in-band pairs),

which enclose `S_i := Σ_{T ∋ i} c_T = Γ − Γ^{(−i)}` and `G_ij := Σ_{T ∋ i,j} c_T = Γ − Γ^{(−i)} − Γ^{(−j)} + Γ^{(−i,−j)}`
(inclusion–exclusion).  `P` is the set of active sites, `n_a = |P|`, `C = C(m, 2) = m(m−1)/2`,
`ε = ε_g / 2^u` (a rational number of units), and

    ψ₁ = 2ε,          ψ₂ = ε · Σ_{s=2}^{M} C(n_a − 2, s − 2) · 2^s / C(s, 2)        (ψ₂ = 0 if M < 2 or n_a < 2).

**W — well-formedness.**  §3, literally.

**A0 — the data do not contradict themselves** (exact integers).  These are properties of *every* family of
non-negative constants indexed by the `m`-sets, so a file that fails cannot have true data:

1. `Γ̲_i ≤ Γ̄` for every site; `Γ̲_ij ≤ Γ̄_i` and `Γ̲_ij ≤ Γ̄_j`, and `Ḡ_ij ≥ 0`, for every in-band pair;
2. `m·Γ̲ ≤ Σ_i S̄_i` and `Σ_i S̲_i ≤ m·Γ̄`  (every `T` is counted `m` times in `Σ_i S_i`);
3. for every site `i`: `(m−1)·S̄_i ≥ Σ_{j: 0<|i−j|≤w} G̲_ij`; and, if every other site is within the band of
   `i`, also `(m−1)·S̲_i ≤ Σ_{j≠i} Ḡ_ij`  (every `T ∋ i` is counted `m−1` times in `Σ_{j≠i} G_ij`);
4. `A_lower(x) ≤ A_upper(x)` at every state: the minimum over all states of the band model
   `A_upper − A_lower` (entrywise difference of the tables), computed exactly by the min-plus recursion along
   the band, is `≥ 0`.

**B — the covering inequalities** (exact rational arithmetic):

* **B3**  `c ≥ ε`.
* **B1**  for every in-band pair of two active sites:  `C · (b_ij − ψ₂) ≥ Ḡ_ij`.
* **B2**  for every active site `i`, with `n_out(i)` the number of active sites `j` with `|i − j| > w`:

      2C · (a_i − ψ₁ − (n_out(i)/2)·ψ₂)  ≥  max(0, (m−1)·S̄_i − Σ_{j: 0<|i−j|≤w} G̲_ij).

  (The sum on the right runs over all sites within the band of `i`, active or not.)

**D — the tables** (exact integers).  With `pen` applied only where a site is changed:

    m_lower.const = A_lower.const − c,                                   m_upper.const = A_upper.const + c,
    m_lower.one[i][x] = A_lower.one[i][x] − a_i·[x ≠ x⁰_i],              m_upper.one[i][x] = A_upper.one[i][x] + a_i·[x ≠ x⁰_i],
    m_lower.pair[i,j][x][y] = A_lower.pair[i,j][x][y] − b_ij·[x ≠ x⁰_i]·[y ≠ x⁰_j],     (and `+` for m_upper),

for every site, every in-band pair and every entry.

**E — the partition functions** (rigorous enclosures).  The checker computes enclosures `[L₊, U₊] ∋ ln Z(m_upper)`
and `[L₋, U₋] ∋ ln Z(m_lower)` by any method whose every operation is enclosed (the reference checker: transfer
matrix along the band in interval arithmetic with outward rounding, 30 significant digits, `β` and `2^u`
entered as exact rationals, table entries as exact integers) and accepts iff, **in exact comparison of
rationals**,

    claim.lnZ_lower ≤ claim.lnZ_upper,      claim.lnZ_lower ≤ L₊,      U₋ ≤ claim.lnZ_upper.

The claim is two one-sided statements, not an enclosure of each `ln Z`: a file whose claimed bracket is wider
than necessary is valid.

## 5. Why B implies `m_lower ≤ E ≤ m_upper`  [P]

Write `pen(x) = c + Σ_{i ∈ S(x)} a_i + Σ_{in-band {i,j} ⊆ S(x)} b_ij` (all in units).  By (D),
`m_lower = A_lower − pen` and `m_upper = A_upper + pen` as functions.  By (G2) and (G3), at every state,

    |E − (f + I_M g̃)|  ≤  |g − I_M g| + |I_M g − I_M g̃|
                        ≤  Σ_{T ⊆ S} c_T  +  ε_g · (1 + Σ_{U ⊆ S, 1 ≤ |U| ≤ M} 2^{|U|})   =:  R(S),      S = S(x),

because `d_∅ = g(x⁰)` is one evaluated value and `d_U`, `|U| ≥ 1`, is an alternating sum of `2^{|U|}` evaluated
values, and only the `U ⊆ S(x)` occur.  With (G1) it therefore suffices that `2^u · pen ≥ R(S)` for every set
`S` of active sites.

**Lemma (covering by pair shares, banded form).**  Let `c_T ≥ 0`.  If, in units,

    c ≥ ε,      b_ij ≥ ψ₂ + G_ij / C  (in-band pairs of active sites),      a_i ≥ ψ₁ + ½ Σ_{j ∈ P, |i−j| > w} (ψ₂ + G_ij / C)  (active sites),

then `pen ≥ R(S)/2^u` for every `S ⊆ P`.

*Proof.*  Every `U ⊆ S` with `|U| = s ≥ 2` contains `C(s, 2)` pairs, all inside `S`; give each the share
`2^s ε / C(s, 2)`.  A pair `{i, j} ⊆ S` receives shares from the `U ⊆ S` that contain it, of which there are at
most `C(n_a − 2, s − 2)` of size `s`; so `Σ_{U ⊆ S, 2 ≤ |U| ≤ M} 2^{|U|} ε ≤ Σ_{pairs ⊆ S} ψ₂`.  In the same way
every `T ⊆ S` contains `C` pairs, all inside `S`, and `Σ_{T ⊆ S} c_T = Σ_{pairs {i,j} ⊆ S} (1/C) Σ_{T ⊆ S, T ∋ i,j} c_T
≤ Σ_{pairs ⊆ S} G_ij / C`, the constants being non-negative.  Hence

    R(S)/2^u ≤ ε + Σ_{i ∈ S} ψ₁ + Σ_{pairs {i,j} ⊆ S} q_ij,       q_ij := ψ₂ + G_ij / C ≥ 0.

The in-band pairs inside `S` are covered by the `b_ij`.  An out-of-band pair inside `S` is split in halves
between its two sites, both of which are in `S`: `Σ_{out-of-band pairs ⊆ S} q_ij = ½ Σ_{i ∈ S} Σ_{j ∈ S, |i−j| > w} q_ij
≤ ½ Σ_{i ∈ S} Σ_{j ∈ P, |i−j| > w} q_ij`, which the `a_i` cover.  ∎

*From the lemma to B1–B3.*  B1 is the second condition with `G_ij` replaced by its upper end `Ḡ_ij`.  For B2
the out-of-band pair sums are not in the file; they are bounded through the identity
`Σ_{j ≠ i} G_ij = (m − 1) S_i` (every `T ∋ i` contains `m − 1` further sites):

    Σ_{j ∈ P, |i−j| > w} G_ij  ≤  Σ_{j: |i−j| > w} G_ij  =  (m−1) S_i − Σ_{j: 0<|i−j|≤w} G_ij  ≤  (m−1) S̄_i − Σ_{j: 0<|i−j|≤w} G̲_ij,

and the left side is non-negative, whence the `max(0, ·)`.

*How sharp.*  The inequalities are sufficient, not necessary.  They are necessary in one case — order `m = 2`
with every pair in the band, where `pen ≡ R` when the penalties are minimal — and the controls use that case
(§8).  In general the pair-share step gives away the difference between `C(n_a − 2, s − 2)` and the number of
supersets inside `S`, and between `G_ij` and its part inside `S`.

## 6. Units and rounding

The certificate is a statement about **integers**.  Our producer (`export_cert.py`) obtains them from the
double-precision numbers of the pipeline as follows; a different producer may do otherwise, the checker does
not care.

* **Unit** `2⁻⁴⁰` kcal/mol (`≈ 9.1·10⁻¹³`), as in the certificates of our workstream P7.  **Inverse
  temperature**: the double nearest to `1/(0.0019872041·300)` per kcal/mol, written as the exact rational
  `7554331614906417 / 4503599627370496`.  `ε_g = 1/10⁷`.
* **Tables of `A_lower` / `A_upper`**: every double is converted exactly to a rational and rounded **down / up**
  to the unit.  If the double tables satisfy (G1), so do the integer ones.
* **Step-A intervals**: for a sum `v` (a double; our code treats it as an upper bound — it has been multiplied
  by `1 + 10⁻⁹`), `up = ⌈v⌉` and `lo = ⌊v·(1 − 3·10⁻⁹)⌋` in units.  That the real sum lies in `[lo, up]` is the
  assumption **(R)**: P3's statement that such a sum of non-negative doubles (about `10⁴` operations, no
  cancellation) is within `10⁻⁹` relative of the real one.  It is not proved; check A0 is the test of it that
  Stage 1 can make (the published intervals must be compatible with the counting identities), and the doubles
  themselves satisfy the two identities to `2·10⁻¹⁶ … 2.4·10⁻¹⁵` kcal/mol, five to six orders inside the
  interval slack of `2.5·10⁻¹⁰ … 1.3·10⁻⁹` kcal/mol (`export_*.log`).
* **Penalties**: the **smallest integers that satisfy B1–B3** for the published intervals.  They are not our
  code's floating-point penalties (which add an absolute allowance `5·10⁻⁹ Γ` to every pair sum and multiply
  by `1 + 10⁻⁹`); the two differ by at most `8.0·10⁻¹⁰` kcal/mol (site) and `3.8·10⁻¹⁰` (pair) on the two
  instances.
* **`m_lower`, `m_upper`**: exact, by (D).
* **Claim**: a double-precision transfer matrix of the integer tables, each end widened by `5·10⁻⁹` and rounded
  outwards to nine decimals.  The checker's enclosures (width `< 10⁻²⁷`) show that the double-precision values
  were right to better than `10⁻¹²`, so the claim leaves a margin of `5·10⁻⁹ … 6·10⁻⁹` nats at each end.

**Effect of the rounding** on the two files, measured: the integer models' `ln Z` differ from those of the
floating-point models by less than `1.0·10⁻¹⁰` (Val₆) and `1.0·10⁻⁹` (Val₂₀) nats, in the widening direction
at both ends; with the widening of the claim, each published end lies `5.7·10⁻⁹ … 6.1·10⁻⁹` nats outside the
floating-point value.  A priori: a state uses `1 + n + p` entries of a table (`p` in-band pairs), each moved
by less than one unit, so an `A`-model moves by less than `(1 + n + p)·2⁻⁴⁰` kcal/mol at any state
(`2.0·10⁻¹¹` for Val₆, `1.3·10⁻¹⁰` for Val₂₀) and `ln Z` by less than `β` times that plus `β` times the change
of the penalty at any state.

## 7. The two files

`experiments/science/sandwich_cert/certs/` — the energy is the one of our workstreams P–P9: capped peptides
built from the force field's own geometry, vacuum terms of ff14SB as `f` (in the form of its one- and
two-residue tables), the GBn2 polarisation energy (no surface-area term) as `g`, side-chain rotamers as
states (three per valine; clash threshold 0.70), 300 K.

| file | instance | `n`, states | order, band | certified, **if (G1)–(G3) hold** | width (nats) | checker time |
|---|---|---|---|---|---|---|
| `sandwich_V6_E_m4_w5.json` (11 kB) | Ace-(Val)₆-NMe, strand backbone | 6, `3⁶ = 729` | 4, 5 (all pairs) | `198.067925225 ≤ ln Z(E) ≤ 198.068095790` | `1.7·10⁻⁴` | < 0.1 s |
| `sandwich_V20_P2_m5_w8.json` (80 kB) | Ace-(Val)₂₀-NMe, polyproline II | 20, `3²⁰ ≈ 3.5·10⁹` | 5, 8 | `518.255189142 ≤ ln Z(E) ≤ 518.271429999` | `1.6·10⁻²` | 9.5 s |

SHA-256: `4f32e54756c2b0f448fababd31483a4d7c2bbf8c0b124a19f103b62ca387bc41` (Val₆),
`ce9ed3951e4564f059fc7fbca48016d20a1a4695d1651eb4381c8100fd28e7cb` (Val₂₀).  The producer is deterministic:
repeated exports of each instance were byte-identical.

**Against the validation values** of SCI-MSG-0025 §8 (floating-point pipeline: Val₆ `198.067925`, `198.068096`;
Val₂₀ `[518.255189, 518.271430]`): reproduced to the ninth decimal up to the widening above.  **Planted truth
(Val₆ only):** by enumeration of the 729 states with the pipeline's own evaluator, `m_lower ≤ E ≤ m_upper` at
every state (smallest margin `1.0·10⁻⁷` kcal/mol, the constant, at the anchor) and the exact
`ln Z(E) = 198.068008142` lies inside the bracket.  For Val₂₀ no such check exists — the bracket is the only
value of that `ln Z` anyone has.

Step-A sizes, for orientation: `Γ = 0.432` kcal/mol (Val₆, order 4), `Γ = 0.082` kcal/mol (Val₂₀, order 5);
largest pair number `0.060` / `0.0018` kcal/mol; largest site number `2·10⁻⁷` / `2.6·10⁻⁴` kcal/mol.

## 8. Reference checker, controls, test vectors  [T]

* `check_cert.py` — the reference checker.  Python standard library plus `mpmath` (1.3.0) for interval
  arithmetic; it imports nothing from the producer.  **A Python reference: tested, not verified.**  Trusted
  base: the Python interpreter and its integers and rationals, the JSON parser, `mpmath.iv` (outward-rounded
  `exp`, `log`, `+`, `×`).  `python3 -B check_cert.py FILE …` prints `ACCEPTED` with the conditional statement
  or `REJECTED` with the first failing check; exit status 0 iff all files are accepted.
* `controls.py` — 85 controls, all behaving as expected (`controls.log`):
  * *planted truth for the recursion*: on 60 random band models the exact minimum equals enumeration and the
    enclosure of `ln Z` contains the 50-digit sum by enumeration;
  * *planted truth for the lemma*: 200 random instances with **known** constants `c_T` (orders 2–5, 2–9 sites,
    random bands, inactive sites, `ε` from 0 to 5 units): the smallest penalties allowed by B1–B3 cover the
    true right side `R(S)` at every one of 10 419 patterns of changed sites, with smallest margin exactly 0 (the
    inequalities are attained); for order 2 with a full band, lowering any one number by one unit (378 cases)
    breaks a pattern, and the checker rejects every one of them;
  * *mutations of the two published files* (77, besides the two unchanged files): each of the 71 faults is
    rejected with the expected label —
    a penalty one unit too small (B1, B2, B3, with and without rebuilt tables), `ε_g` or the unit changed,
    step-A ends moved, the order changed (A0: the data of one order contradict the identities of another),
    `A_lower` and `A_upper` exchanged, a table entry off by one unit (D), malformed files (float literal,
    duplicate key, truncation, wrong key sets), the claim moved **one step of `10⁻¹²` past the checker's own
    enclosure** (E) — and six mutated files that are still valid certificates are **accepted** (a penalty
    raised, the claim moved to just inside the enclosure, annotations removed): a checker that rejected those
    would test equality with our producer, not validity.
* `vectors/` — the 43 mutated Val₆ files with `EXPECTED.tsv` (file, verdict, label of the reference checker,
  description), so that a second checker can be tested without running ours.

One control deserves a sentence because it shows what Stage 1 can and cannot see.  For Val₆ every pair is in
the band and the two `A`-models coincide at the anchor state; after outward rounding their difference there is
exactly 22 units (one per table entry used).  A producer that rounded the wrong way would give −22 and is
rejected by A0.4 (vector 43).  For Val₂₀ the `A`-models differ by at least `1.7·10⁷` units everywhere and the
same mistake would pass: **(G1) is not checked at Stage 1, and A0.4 is only a necessary condition.**

## 9. What Stage 2 has to establish

In the order in which we would attempt them; each replaces one data assumption by a check.

1. **Step C, exactly — (G1).**  From the evaluated values `g̃` on the ball (integers in the unit after an
   exact conversion of the doubles) and the tables of `f`, recompute `A_lower` and `A_upper` by the published
   construction in exact arithmetic and compare.  The construction is finite and elementary (alternating sums,
   row and column extrema); the ball has 233 states for Val₆ and 87 441 for Val₂₀.  This needs the ball values
   as a second data file and makes (G1) a theorem about them.  Open point: `f` is *defined* by its tables in
   our pipeline; that those tables equal the vacuum energy of the force field evaluated directly is a tested
   statement (to rounding), not a certified one.
2. **The evaluation tolerance — (G3).**  A bound on the difference between the double-precision evaluation of
   the GBn2 energy and its real value at each ball state.  Our allowance is `10⁻⁷` kcal/mol against a measured
   `1.8·10⁻¹²`; a proof needs the evaluator's operation count and the accuracy of the library functions it
   calls, or an evaluator in interval arithmetic (with which `ε_g` could be dropped to the enclosure width).
3. **Step A — (G2).**  A specification of P3's Theorem 3 and Proposition 4 from which the sums
   `Γ^{(−A)}` can be recomputed with directed rounding: the parameter files (`amber14/protein.ff14SB.xml`,
   `implicit/gbn2.xml`, as shipped with OpenMM 8.6.1), the geometry, the interval enclosures of the derivative
   suprema, the generating-function sum.  This is the large item; the mathematics is in
   `docs/science/workstreams/P3_REPORT.md` §§2.1–2.6, the specification separate from our code does not exist
   yet.  It also replaces assumption (R) of §6.
4. **Not needed for the bracket but worth having:** the pair sums `Γ^{(−i,−j)}` for out-of-band pairs.  The
   double-counting bound of B2 costs nothing here (it is an identity up to the interval slack), so we do not
   publish them.

## 10. Differences from what SCI-RES-0042 announced

1. The floating-point allowances are **not listed** in the file.  They are the closed formulas `ψ₁`, `ψ₂` of
   §4 in `ε_g`, `m` and the number of active sites, and the checker recomputes them; the file carries `ε_g`.
2. The claim is two one-sided rationals (`lnZ_lower ≤ ln Z(m_upper)`, `ln Z(m_lower) ≤ lnZ_upper`), not an
   enclosure of each partition function.
3. Added: the consistency checks A0, which were not in the steps B, D, E of SCI-MSG-0025 §8.
4. The penalties are the smallest integers allowed by the inequalities, not the rounded floating-point
   penalties of our code.

## 11. Limits, and what was not done

* Everything certified is conditional on (G1)–(G3); nothing in Stage 1 touches the force field.
* The two files are for one residue type, one force field, one solvent model and idealised backbones.  The
  physical meaning of the certified numbers is discussed, with its limits (rigid rotamers: nats per torsion),
  in `INFERENCE_LIMITS_ADDENDA.md` A17 (25)–(26); this note says nothing about it.
* The reference checker is Python and slow by design (9.5 s for `3⁸` tails × 20 sites); its cost grows as
  `n · Π` of the states of `w + 1` consecutive sites.
* **Prior art.**  Checkable certificates for optimisation and counting are an established practice (proof
  logging for combinatorial solvers; interval-arithmetic enclosures); for the neighbouring side-chain
  *optimisation* certificates we recorded what we found in `PRIOR_ART_MATRIX.md`, addendum F.  Whether a
  checkable certificate format for **two-sided bounds on a partition function with a many-body term** exists
  in print was **not searched** for this note, and no novelty is claimed for the format.
* Predictions written before the runs, with outcomes: `experiments/science/sandwich_cert/PREDICTIONS.md`.
