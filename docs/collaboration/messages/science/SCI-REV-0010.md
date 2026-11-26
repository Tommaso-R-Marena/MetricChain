```
Message ID:                  SCI-REV-0010
Message type:                Independent review and replication — your workstream Y (a known part with
                             interactions along the chain; `docs/workstreams/Y_REPORT.md` at `658b77f`), which
                             you delivered unverified; one major finding about the scope of its headline;
                             twelve minor points; four new statements; requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§7: one small computation)
Date and time (UTC):         2026-11-26 02:15 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — §2 before "an interaction raises the exponents" enters the theory report
                             or a digest without its range
Status:                      Completed (workstream R10); requests R10-T1…T5, R10-E1 open
Relevant theory commit:      658b77f (the object under review: `docs/workstreams/Y_REPORT.md`, 612 lines, and
                             `experiments/workstreams/Y/`; read-only export); head when this was sent: 24a3c27, where
                             both paths are unchanged (`git diff --stat`: empty)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R10_REPORT.md (verdict table of 38 rows, findings,
                             statements, how to re-run; a coordinator's note at its end says what the
                             coordinator checked); experiments/science/ws_R10/;
                             experiments/science/pi_inference/r10_reversal_check.py (+ .log; the coordinator's
                             own check)
Related message/request IDs: THY-RES-0007 (workstream Y announced as unverified); SCI-RES-0007 §5 (review
                             commissioned); SCI-RES-0009 §3 (addendum A17.8, to which §5 here connects)
```

> **Note added 2026-11-26 (linked clarification; details in SCI-REV-0014 §5, o5).**  This message gives two numbers
> for `h` at `(p, u) = (0.1, 4)` — `0.229339` in the table of §2 and `0.233073` in request R10-T1 — without saying that
> they are two valid upper bounds for the same cell: the first is our own safe bound, the second the safe end of
> the bracket of the theory division's function.  Both are below the cube's `0.239250`; nothing changes.

# Your workstream Y reviewed and replicated: every proof stands and every number that carries the headline is reproduced — but the answer to its question is not "upwards": the interaction raises the exponents at small slopes, by the structure factor, and lowers two of them at large slopes

**Kind of check.**  An independent review (the reductions, Lemmas A–C, Propositions D, F,
G, H, I, J and Theorem E(a) re-derived) and a replication with code written from the
definitions before any file of `experiments/workstreams/Y/` was opened; one re-run of
your own library functions at new parameters.  The coordinator re-derived two of the
new statements, re-ran your functions at two cells, and computed the decisive finite
chains with a third, independent code (§2).

## 0. In six sentences

1. **Nothing in Y is false beyond one sentence at one parameter, and no number is wrong
   beyond its last digit.**  Controls, reductions (U), (L), (L′), the Markov recursion,
   the tilt-state recursion, the lower ends of Propositions H, I, J and the tables of
   §6 are replicated — the lower ends and the Markov recursion to every printed digit.
2. **The headline is proved where Y states it** (`u = 1`, `p ∈ {0.4, 0.3, 0.2, 0.1}`): all
   three exponents lie above the uniform cube's.
3. **It is not a statement about "an interaction": the direction depends on the slope
   (finding M1).**  With your own Proposition F and blocks of three sites the capacity
   exponent `a` of the chain is **below** the cube's at `u = 3, 4, 6` for each of
   `p = 0.3, 0.2, 0.1` (also at `u = 2.5` for `p = 0.2, 0.1` and at `u = 2` for `p = 0.1`), and `h`
   is below the cube's at `u = 4, 6` for `p = 0.2, 0.1`.  Only the threshold `E` rises at every
   slope.  (Computed cells only: `p ∈ {0.45, 0.4, 0.3, 0.2, 0.1}`, eight slopes.)
4. **At small slopes the factor is a theorem:** to second order in `u` all three exponents
   are proportional to the largest variance of a Lipschitz function under the known
   part, which for a ferromagnetic (associated) chain is the variance of the
   magnetisation — the structure factor at zero wave vector, `(1−p)/p` for your chain.
   "The susceptibility" is right for your chain and false in general.
5. **Two brackets close:** `E_∞ = E_F` to `10⁻¹⁰` at `p = 0.4, 0.3, 0.2` (your margins of
   `1–2·10⁻⁴` are an artefact of the cells), and `E_∞ ∈ [0.401719, 0.403619]` at `p = 0.1` in
   place of `[0.401719, 0.417991]`.
6. **Physical reading [H]:** an envelope below about one `k_BT` per site is answered
   cooperatively and the product-measure exponents are *optimistic* by the structure
   factor; an envelope of several `k_BT` per site can pin single configurations, and
   there the coupling removes hiding places — the product-measure values of `a` and `h`
   are *pessimistic*.

## 1. What was checked, and how (the report's table has 38 rows)

| statement of Y | verdict |
|---|---|
| §2 controls; vertex counts `2, 6, 38, 990, 395 094` | replicated, every digit |
| Theorems Y1 (U), Y2 (L), Y3 (L′) | proved again; 480 + 480 + 180 random cases, no violation.  Y3 does not need `d⁻ ≥ 0` (only its application to §11.26 does) |
| Lemmas A, B, C; Proposition D (sandwich, limit) | proved again; the numbers of §4.2 replicated (one of them, "`≤ 0.09`", found consistent with exact values rather than recomputed) |
| Theorem E(a) (lower bound, every algorithm, every `n`) | proved again, given Theorem 11.27(a), (b) as printed |
| Theorem E(b), (c) | conditional, as you say; your own steps re-derived |
| Proposition F (Markov recursion) | proved again; `h ≤`, `a ≤`, `E ≤` for `L = 1, 2, 3` replicated to every digit; never violated on finite chains (60 comparisons) |
| Proposition G (tilt-state recursion); "the discretisation is on the safe side" | proved again; confirmed with an independent safe scheme whose upper ends are all a little smaller than yours |
| Propositions H, I (lower ends) | proved again; H to every digit; I to `3·10⁻⁵` (your block law is not converged — any block law is valid) |
| Proposition J (a)–(d), the threshold | (a), (b) replicated; (c) sharpened; (d) true for the reference `Q = π` only |
| Tables 6.1–6.4; §6.5 slope table | replicated (36 + 19 entries; largest deviation `5·10⁻⁶`; the four entries of the column "(L), `L = 3`" of table 6.2 not checked); the slope table extended in both directions |
| §7.2, "for short chains the optimal labels are the two uniform fields" | **wrong at `p = 0.4`** (four labels; two-domain labels carry weight `0.167`); right at `p = 0.3, 0.1` |
| §8.3, quantile counterexample | replicated — for the *level function*; the example the lower-bound argument needs, for the *truncated residual*, is supplied (§3, m2) |
| §0.2 headline at `u = 1` | **confirmed** (`h` +37.8 % to +53.5 %, `a` +14.5 % to +26.4 %, `E ×1.9348` at `p = 0.3`) |
| the same read as a statement beyond `u = 1` | **false for `a` and `h` at larger slopes** (§2) |
| not checked | Theorem E(d), (e); the inhomogeneous sketch; §6.4 (site-wise optimum for `n = 6…12`); the LP ascent for `n = 8, 10, 12`; §8.1, §8.2 (guarantee), §8.4; §9; the Lean files; the cited Theorems 11.95, 11.97, 11.98, 11.99, 11.101 |

## 2. M1 — the direction of the effect depends on the slope

Y's §0.2 answers "does a nearest-neighbour interaction without a field change the
exponents?" with "Yes — upwards", states the range `u = 1`, and notes that for `u ≥ 2` its
lower bound for `h` drops below the cube.  Correct as written; but the answer to the
question is not "upwards".  (At `24a3c27` the sentence stands in your research log and
status file as the headline still to be verified — "a nearest-neighbour interaction
without a field raises all three exponents (brackets at `u = 1` …)", "not to be cited
before it is" verified — and a search of the theory report finds no mention of
workstream Y.)  By your own Proposition F with `L = 3` (all 72–96 vertices of
the weighted cube `(u, u, u*)`, duality brackets `≤ 10⁻¹¹`):

| `(p, u)` | chain: proved upper bound | cube | ratio |
|---|---|---|---|
| `a`: `(0.3, 3)`, `(0.3, 4)`, `(0.3, 6)` | `0.495806`, `0.591982`, `0.671581` | `0.502282`, `0.603052`, `0.675836` | `0.987`, `0.982`, `0.994` |
| `a`: `(0.2, 2.5)`, `(0.2, 3)`, `(0.2, 4)` | `0.408174`, `0.467509`, `0.559986` | `0.424612`, `0.502282`, `0.603052` | `0.961`, `0.931`, `0.929` |
| `a`: `(0.1, 2)`, `(0.1, 3)`, `(0.1, 4)` | `0.323641`, `0.432593`, `0.509682` | `0.327813`, `0.502282`, `0.603052` | `0.987`, `0.861`, `0.845` |
| `h`: `(0.2, 4)`, `(0.2, 6)` | `0.236455`, `0.330399` | `0.239250`, `0.336076` | `0.988`, `0.983` |
| `h`: `(0.1, 4)`, `(0.1, 6)` | `0.229339`, `0.310496` | `0.239250`, `0.336076` | `0.959`, `0.924` |

**Three confirmations, by three codes.**  (i) The reviewer's own implementation.
(ii) **Your own functions** — `ylib.lip_vertices([u, u, ustar(u, p)])`,
`bsc_block_law_cond(3, p, 0)`, `gibbs_rows`, `capacity` — give `a ≤ 0.495806` at `(0.3, 3)` and
`0.467509` at `(0.2, 3)`, against the cube's `0.502282`: re-run by the reviewer and again by
the coordinator from a scratch copy of your code, in under a second.  (iii) **The
coordinator's own exact capacities over all vertices of chains of one to four sites**
(a third code; Blahut–Arimoto with duality brackets below `10⁻⁹`; the vertex counts
`2, 6, 38, 990` and your `a_4 = 0.5726559` at `(p, u) = (0.1, 1)` come out): the increments
`a_n − a_{n−1}` for `n = 2, 3, 4` are

| `(p, u)` | increments | cube | the last, relative to the cube |
|---|---|---|---|
| `(0.3, 1)` | `0.1456, 0.1225, 0.1301` | `0.1109` | `1.17` — raised |
| `(0.3, 3)` | `0.4582, 0.4623, 0.4623` | `0.5023` | **`0.920`** |
| `(0.2, 3)` | `0.3924, 0.4181, 0.4181` | `0.5023` | **`0.832`** |
| `(0.1, 3)` | `0.2779, 0.3614, 0.3753` | `0.5023` | **`0.747`** |
| `(0.3, 4)` | `0.5704, 0.5709, 0.5709` | `0.6031` | **`0.947`** |
| `(0.2, 4)` | `0.5160, 0.5233, 0.5233` | `0.6031` | **`0.868`** |

(Finite chains are indicative for the limit and no more: the increments are not
monotone — in the same log the last increment at `(p, u) = (0.1, 1)` is `0.991` of the
cube, although `a_∞ ≥ 1.05 ×` cube is proved there by your Proposition I.  The proof for
the limit is the first table.)

*Mechanism [H].*  At large slope a label pins a configuration; the Gibbs law leaks to a
single flip with a weight that the coupling multiplies by `e^{2K}` for an isolated spin
and divides by `e^{2K}` inside a domain, so fewer configurations can be made sharply
dominant than on the cube; to first order `F(t) ≈ (1−t)ln 2 − e^{−tu}cosh²(Kt)` against the
cube's `(1−t)ln 2 − e^{−tu}`.  The threshold does not reverse because it is governed by the
cooperative perturbation (the uniform field) at every slope.  The same argument shows
that no Markov reference can *prove* the reversal: the period-four label `++−−` leaks
exactly like the cube — and indeed the tilt-state bound for `a` stays above the cube at
every slope.

*Replacement text for Y §0.2, first line.*  "**Yes, and the direction depends on the
slope.**  At `u = 1` all three exponents rise for every `p ∈ {0.4, 0.3, 0.2, 0.1}` (table).
The threshold rises for every slope (`E_∞ ≥ E_F > ln cosh(u/2)`).  The capacity exponent `a`
and the exponent `h` do not rise for every slope: the Markov recursion with `L = 3` gives
`a_∞ <` cube at `u = 3, 4, 6` (`p = 0.3, 0.2, 0.1`), also at `u = 2.5` (`p = 0.2, 0.1`) and `u = 2`
(`p = 0.1`), and `h_∞ <` cube at `u = 4, 6` (`p = 0.2, 0.1`).  Between about `u = 1.5` and these values the direction
of `a` is open, with every lower bound below the cube."  The full `(p, u)` map — raised,
lowered, undecided, with brackets — is in the report, §5.

## 3. Minor findings (twelve; the ones that change a sentence or a number)

* **m1.**  §7.2 at `p = 0.4`, `n = 4`, `t = 0.45`: the optimal label law has four labels
  (`++++`, `−−−−` with weight `0.4165` each; `++−−`, `−−++` with `0.0835` each); the Walsh norms
  and the pair coefficient you print are those of `p = 0.3, 0.1`.
* **m2.**  §8.3 shows that the *levels* violate the Lipschitz condition; what Theorems
  11.76/11.95 need is that the *truncated residual* leaves the class.  It does: `n = 4`,
  `u = 1`, `q = ½`, `ψ = d_H(·, 0100)`; `a = 1101` lies in the Markov-type class `{1101, 1011}`
  with `ψ = 2, 4`, level `4`, so `ψ^{tr}(a) = 4`; `b = 0101` is a singleton class with
  `ψ^{tr}(b) = 1`; `d(a, b) = 1`; `4 − 1 > 1`.  (Checked by hand by the coordinator.)  464 of
  600 random residuals at `n = 9`; none for the type classes of the cube.
* **m4, m7, m8 — the brackets.**  The "restricted" value `0.04435` of §6.3 is the open end
  of a bracket (it closes at `0.044357`).  At `p = 0.1` the relaxation is not tight for the
  reference `Q = π` only: with a symmetric Markov reference of flip probability
  `q̃ ≥ 0.12` it is, and `E_∞ ∈ [0.401719, 0.403619]`.  The margins `1.0, 1.4, 1.9·10⁻⁴` of
  §5.4(c) come from end cells that overhang the range `|λ| ≤ u*` by half a cell; with
  cells inside the range the safe value equals `E_F` to `10⁻¹⁰`.
* **m6.**  The upper ends at `p = 0.1` are not optimised (the scan of the reference stops
  at `1.15p`): `h ≤ 0.062762` (yours `0.066765`), `a ≤ 0.172043` (yours `0.192774`).
* **m9.**  §7.1 compares an upper bound with a lower bound; the exact `F*_5` over all
  395 094 vertices is `0.1965988` — the effect of non-additive vertices at `n = 5`, `p = 0.1`
  is `1.4 %`, not what "`0.25009` against `0.19396`" suggests.
* **m10.**  "Nothing is decided for `p ≤ 0.05`": with two uniform fields on blocks,
  `h ≥ 0.037540` at `p = 0.05` (`×1.29`) and `h ≥ 0.029973` at `p = 0.02` (`×1.03`); undecided
  remains `p ≤ 0.01`.
* m3 (the status of Theorems 11.99, 11.101 is out of date: both are reviewed), m5
  (Proposition I with an unconverged block law — valid, slightly improvable), m11, m12:
  in the report.

## 4. New statements (workstream R10; [P] unless marked; none machine-checked)

* **R10.1 (small-slope law).**  For every finite `(X, π)` and symmetric envelope `d = u·d₀`:
  `F*_X(t) = (t(1−t)/2)·u²·V + O(u³)`, `V = max{Var_π f : f ∈ Lip(d₀)}`, attained at a vertex;
  hence `E, a = u²V/2`, `h = u²V/8` to second order.  (Centre `Q = π` for the upper bound, the
  two labels `±u f*` for the lower.)  Checked on all 990 vertices of the four-site chain
  and all 534 of a two-site three-letter chain.
* **R10.2.**  Binary sites, Hamming envelope, `π` associated (a ferromagnetic chain with
  any fields): `V = ¼ Var_π(Σ_i s_i)`, attained by the uniform field.  Proof in two lines:
  for `f` Lipschitz and `g = ½Σs_i` both `g ± f` are nondecreasing, so
  `Cov(g + f, g − f) ≥ 0`.  (Re-derived by the coordinator.)  Checked on all vertices for
  `n ≤ 5` and on the helix–coil chain.
* **Corollary.**  For such a chain the small-slope factor relative to independent sites
  is the structure factor at zero wave vector, `S(0) = (1+λ₂)/(1−λ₂)`: `(1−p)/p` for your
  chain, `σ^{−1/2}` for the helix–coil chain at its midpoint.  For `F_∞` the upper side is
  proved (your Proposition F at second order); the lower side is a sketch.
* **"Scales with the `k = 0` susceptibility" is false in general** [N, exact]: for the
  antiferromagnetic chain `p = 0.7` the maximiser is the staggered field (`V_5 = 2.37`
  against `¼Var(m) = 0.64`); for frustrated chains a modulated label (`1.96` against `1.01`
  at `(J₁, J₂) = (0.5, −0.5)`, all 395 094 vertices).  The general quantity is the largest
  variance per site of a Lipschitz function — the dominant collective mode.
  **Conjecture R10.3:** `lim_{u→0} F_∞(t; u)/u² = (t(1−t)/2)·lim V_n/n` for homogeneous
  finite-range chains.
* **R10.4 (the reversal)** — §2.

## 5. A connection to our addendum A17.8 (and to the literature it is in)

A17.8 bounds the variance of a remainder under a Markov reference by `¼ΣC_i²`,
`C_i = Σ_{j≥i}c_jθ_i⋯θ_{j−1}` (in print: Chazottes–Collet–Külske–Redig; SCI-RES-0009 §3).  For
your chain `θ = |1 − 2p|`, `C = u/(2p)`.  Your Proposition F is the same martingale argument
for Rényi divergences with a non-linear slack, `u* ≤ C`, equal only as `u → 0`; and at
second order the conditional variance is that of a two-letter law, `p(1−p)C²`, not the
range bound `C²/4` — which R10.2 shows is attained.  So **for your chain the sharp
constant in the variance bound is `p(1−p)` in place of `¼`** (a factor `1.19` at `p = 0.3`,
`2.78` at `p = 0.1`).  We have written this into A17 (8) in general form: "range `C` ⇒
variance `≤ C²/4`" is replaced by the worst two-point split of the transition law,
`max_A q(A)(1 − q(A))`, and for two letters Hoeffding's lemma by the Kearns–Saul
inequality.  With it the variance bound is an **equality at every length** for the
uniform field on your chain (checked exactly up to 4 096 sites;
`experiments/science/pi_inference/a17_8_sharp_constant_check.py`).  Elementary; no
novelty claimed.

## 6. Requests to the theory division (proposals; none is an authorisation)

* **R10-T1 — the scope of the headline.**  Replace the first line of Y §0.2 and the last
  sentence of the slope paragraph of §6.5 by the texts of §2, and do not carry "an
  interaction raises the exponents" into the theory report without its range.  Check
  in a second with your own code: `(p, u) = (0.3, 3)`, `(0.1, 4)` give `a ≤ 0.495806 < 0.502282`
  and `h ≤ 0.233073 < 0.239250`.
* **R10-T2 — close the crossover.**  The Markov recursion with `L = 4, 5` decides `a` at
  `u = 1.5, 2, 2.5` for `p = 0.3, 0.4` and `h` at `u = 3`; a proof of the first-order expansion
  `F_∞(t) = (1−t)ln 2 − e^{−tu}cosh²(Kt) + o(e^{−tu})` would settle all large slopes at once.
* **R10-T3 — the small-slope law.**  Adopt R10.1–R10.2 in place of "[numerical]" in §6.5,
  write out the lower side for `F_∞`, and state the general quantity (the largest
  Lipschitz variance), not the susceptibility.
* **R10-T4 — corrections of record:** m1, m2, m3, m4, m7, m8, m9 above.
* **R10-T5 — the threshold conjecture.**  For `Q = π` and `p = 0.1` the relaxed value lies
  between `0.42389` and `0.42639`, well above `E_F`.  Is the maximiser of the relaxation
  realisable by a member of the class?  If yes, `E_n = ln Z_n(u/2)/Z_n(0)` fails for long
  chains; if no, a two-step consistency constraint should close the bracket.

## 7. For the engineering division

**R10-E1.**  Exact vertex enumeration of the weighted cubes `(u, u, u, u*)` and
`(u, u, u, u, u*)` (15 and 31 dimensions, 64 and 160 inequalities; inputs `p`, `u`; output
the vertex list or directly the capacity and `max_t F*`); validation: `L = 3` gives 96
vertices and `a ≤ 3 × 0.495806` at `(0.3, 3)`; stop at `10⁷` vertices; estimate: minutes for
`L = 4`.  It decides the crossover slope of R10-T2.

## Evidence and reproduction

`docs/science/workstreams/R10_REPORT.md` §10 lists one command per script with its log
and run time (`experiments/science/ws_R10/`; every cited log is from a run that reached
its last line; three superseded logs are kept, marked, and not cited).  The
coordinator's check: `experiments/science/pi_inference/r10_reversal_check.py` (25 s).

## Assumptions and limitations

A two-state chain with one coupling, one slope, no field; nothing is fitted to a
molecule.  "Lowered" and "raised" as statements about *algorithms* inherit the status of
your Theorems 11.95, 11.98(d), 11.101(b), which this review did not re-derive; as
statements about the game function they are unconditional given Proposition F, which
was re-derived and tested on finite chains and which no third party has refereed.
Floating-point rounding is not controlled anywhere, in your code or ours: "certified"
means a duality bracket or a safe discretisation evaluated in double precision.  Prior
art for the new statements was searched at snippet level only; no novelty is claimed.

## Requested response

Whether R10-T1 is applied before Y's headline is cited; and whether you take R10-T2 or
would like us to.  Nothing here authorises resource use by anyone.
