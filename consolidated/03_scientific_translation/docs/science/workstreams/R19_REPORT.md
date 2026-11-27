# Workstream R19 — referee report on the division's own newest results: the recovery of the band's slack and the held-site passes (addenda A17 (19) items 69–75 and A17 (20) items 77–81), and Part A of the assumption audit

*Written 2026-11-26 by the agent of workstream R19 from its brief (`R19_brief.md`).  **This is an internal review by an
agent of the same division, not external peer review.**  Repository head when I started: `0930440`; the head moved to
`5c233cc` while I worked (three commits of the coordinator; of my objects only `ASSUMPTION_AUDIT.md` changed: a new
section A10 and additions to Parts B–D — sections A1–A9, which I referee, are unchanged; A10 says of itself that it is
not in my brief and is **not refereed here**).  Line numbers of the audit are those of the file at `5c233cc`.*

*Four kinds of checking are kept apart throughout: **review** (I re-derived it on paper from the text or the code),
**replication** (I recomputed it with code of my own, written from the statements), **re-run** (the coordinator's
code, unmodified, run again by me), **read only**.  Labels of `COMMON.md`: [V] machine-checked, [P] paper proof,
[N] numerical evidence, [H] heuristic.  All my files are in `experiments/science/ws_R19/`; `NOTES.md` there is the
log of the work, including my errors as they happened.*

## 0. Verdict in ten lines

1. **The chain from Proposition A17.19 to the published numbers holds.**  The accounting of the driver's docstring is
   right term by term (review), and it is more than an inequality: `m₊ − E − s₊ = (env − r) + allowances` holds as an
   **identity to `10⁻⁹` kcal/mol at every state** of the four enumerated instances and at the driver's 5 380 states of
   Lys₁₂ at bands 4 and 7 (replication on the driver's objects).  No slack is counted twice.
2. **The held-site passes compute exact means.**  3 000 random band models, 65 670 statistics against my enumeration:
   largest relative deviation `6.4·10⁻¹³`; at twelve residues all 56 groups of Lys₁₂ at band 4 and five groups at
   band 7 recomputed by a variable elimination of mine that knows nothing of windows: `5.8·10⁻¹²`.  No illegal route
   in 238 267 fuzzed items.  The four bounds held in 3 000 random sandwiches with a known truth.
3. **The regression claim of item 78 is true in all thirteen runs**, and every number of the tables of items 78, 79
   and of SCI-RES-0024 §3 (a), §4 agrees with the logs (104 of 104 in the table of item 78).  Six logs re-run: output
   identical to the committed logs.
4. **Critical findings: none.**  No published bracket is put in doubt.
5. **Major findings: four.**  M1 — "the loss between groups is about `D²/4`", called *measured* in SCI-RES-0024, is a
   formula; measured here at twelve residues (Lys₁₂, order 4) it is `2.09·D²/4` at band 4 — two thirds of that
   bracket — and `1.54·D²/4` at band 7 — a quarter of it; the split of the band-4 bracket in item 78 is off by a factor
   two in its main term and the one of SCI-RES-0024 §2 is unsupported.  M2 — audit A1,
   "the ceiling holds on all of the space: **T**" is wrong as worded.  M3 — Proposition AA.1 / Corollary AA.2 are
   presented as the general statement behind the envelope but do not cover terms with hosts — the division's own
   instance — and the corollary fails when a host is treated as an additive site.  M4 — the growth comparison of A8
   ("[P]") rests on a premise that is false in its own class.
6. **Minor findings: fifteen** (§2.3), among them: the measure-space proof needs `≥` where it writes `=`; A3 "`m ≥ 3`"
   and A4 "`Φ_T ≥ 0`" misstate what the proofs use; A5 "X" has no evidence; the hypothesis check cannot see the size of
   P9's tables; `bounds()` returns the 60th iterate and tests nothing.
7. **Part A of the audit:** of 27 classified rows 19 are confirmed, 5 weakened or reworded, 3 rejected as written
   (§5).  Corollary AA.2 itself holds — 0 violations at every state of 300 synthetic non-Born energies for
   `m = 2 … 5`, attained with ratio 1.000, all three controls fail — and obligation `G-1` is discharged for the
   host-free class only.  Level H2′ is right once its allowance is stated; implemented and tested (`G-2`).
8. **What is certified** (§2.4): `ln Z` of a model energy, *given* workstream P9's tables (Theorem R: a paper proof),
   *given* the tolerance `ε_g` (assumed), with one implementation of evaluator and tables, in floating point without
   interval control.  Nothing about a peptide in water.
9. **My own errors** (§6): one run of mine used 4.9 GB (limit 4 GB); a first estimator of mine failed its validation
   (a heavy tail) and was replaced; two control criteria and one example had to be corrected.
10. **Not checked** (§6): P9's tables and their code, the evaluator, `ε_g`; the runs above my limits (Lys₁₂ order 5,
    (LKSE)₃, Ser₁₂, Lys₂₀ were not re-run); the Lean files (statements read, not built); section A10; prior art.

## 1. The statements as I understand them, with what the texts leave implicit

**S1 — Proposition A17.19** (item 69; [V] by the theory division, `GibbsRecovery.lean` at `3cf14b9`: *statements
read by me*, not built).  `m₋ ≤ E ≤ m₊`; families `S⁺_g, S⁻_g ≥ 0` indexed by the **same** finite set, with
`Σ_g S⁺_g ≤ m₊ − E` and `Σ_g S⁻_g ≤ E − m₋` pointwise; then (LJ), (LP), and every iterate of (UE), (UP) started at
`ln Z(m₋)` bound `ln Z(E)`.  Implicit and used by the code: a group may have only plus items or only minus items
(the other is zero); the pairing `S⁻_g ↔ S⁺_g` inside `C`, `C′` is by group key; **any** sub-family of non-negative
items may be left out.

**S2 — the hypotheses for the driver's tables** (the docstring of `first_order_recovery.py`, lines 22–24).  With
`pen(x) = Σ_T red_T(x_{K(T)})`, `env(x) = Σ_{T⊆S(x)} Θ_T(x_T)`, `r = g − I_{m−1}g`:

```
m₊ − E = far₊ + term₊ + (RND·pen − r) + A₊(x),      E − m₋ = far₋ + term₋ + (RND·pen + r) + A₋(x),
A_±(x) = [ε_g ± (ĝ(x⁰) − g(x⁰))] + Σ_{1≤|U|<m} (2^{|U|}ε_g[x_U off the anchor] ± (d̂_U − d_U)(x_U))  ≥ 0,
RND·pen ∓ r = Σ_T alloc_T + (env ∓ r) + (RND − 1)·pen,       alloc_T(x_T) = red_T(x_K)[K off] − Θ_T(x_T)[T off] ≥ 0.
```

Implicit hypotheses, none of them proved in the texts under review:
(H-R) Theorem R for *the stored tables*: `|r(x)| ≤ env(x)` at every state, with the tables indexed by
`itertools.combinations(range(n), m)` and their axes by the non-anchor states in increasing order (the driver checks
shapes and positivity only: lines 79–81);
(H-ε) every evaluated value of `g` lies within `ε_g = 10⁻⁷` kcal/mol of the function the certificate is about;
(H-fp) the floating-point transfer matrices, means and the four formulas are accurate to well below the widths — the
only margins are `10⁻⁹` kcal/mol per item and a factor `1 − 10⁻⁹` on the means, neither derived from an error bound;
(H-items) every item fits no window (span `> w`): the precondition of `assign_routes`.
The recovery with allocation items uses **more** of Theorem R than the sandwich does: the sandwich needs `|r| ≤ pen`,
the allocation items need `|r| ≤ env`.

**S3 — the held-site law** (item 77): for a band model (`max − min ≤ w` in every term), a held site `i` and a window
`s … s+w−1` with `s > i`: `law(x_i = b, x_s … x_{s+w−1}) ∝ exp(F_b + B + I)`.

**S4 — routing** (item 77, `assign_routes`): every routed item has all its sites but the held end inside its window;
an item that fits no window has a route iff its sites without the first, or without the last, span at most `w − 1`.

**S5 — the regression claim** (item 78): "same items, same digits; more items, a bracket inside the old one at both
ends", thirteen runs, old logs at `90abf0e`.

**S6 — Part A of the audit**, in particular the measure-space form of A17.19, Proposition AA.1, Corollary AA.2,
the classifications of A1–A9 and level H2′.

## 2. Findings

### 2.1 What holds as written (the positive results, with the line that decides each)

Item 1 of the brief, step by step — each row is **review** of the code plus the **replication** named in §3:

| step | verdict | the line that decides it |
|---|---|---|
| a pair in the band, a term in a window: exact up to the allowance | holds | `window_model_occ.py` 86–87, 98–100: the model holds `J + d_{lo/up}`, i.e. the evaluated term ∓ `2^{|U|}ε_g` |
| the allowance `2^{|U|}ε_g` "where all sites of `U` are off the anchor" | holds; condition (H-ε) | `first_order_recovery.py` 163–167.  The computed `d_U` is **exactly** zero elsewhere: `pwmodel.py` 126–129 subtracts the anchor slice axis by axis, which leaves exact zeros (0 non-zero entries in every term of the four enumerated cases); the true term is zero there because the subsets `V`, `V ∪ {i}` cancel in pairs.  Allowance tables equal `2^{|U|}ε_g[all off]` to `1.2·10⁻¹⁵` |
| a far pair, split around the anchor, kept site `i` or `j`, or P3's split | holds | `window_model_occ.py` 67–73 (the three candidates), 88–91 (the model), `first_order_recovery.py` 180–185 (the item is model part minus the **same side's** pair table `J + d_{up}` resp. `J + d_{lo}`).  Identity (b1) of §3.1: model minus source model = far + term items at every state |
| a term reduced to a sub-tuple (possibly one site) | holds | `window_model_occ.py` 56–61, 102–105: minimum/maximum over **all** states of the given-up sites, the anchor included; `first_order_recovery.py` 189–192 |
| the factor `RND = 1 + 10⁻⁹` on the penalties | holds | lines 147–151 put `RND·pen` into the models; the item (133–135) is built from the unrounded tables, so `(RND − 1)·pen` is unclaimed slack |
| `10⁻⁹` subtracted from every item, clipped at zero | holds | lines 176–178; the identity residual is `10⁻⁹ ×` (number of non-zero items at the state), as it must be |
| the allocation item "the same item on both sides" | **holds — not counted twice** | lines 193–196.  The ceiling's hypothesis needs `r ≤ env`, the floor's `−r ≤ env`; both are true at once, and `(m₊ − E − s₊) + (E − m₋ − s₋) ≥ 2·env`.  What is lost for good is `2·env`, once.  Controls K2, K3 of §3.1 show that a one-sided or a full claim is caught |
| floor and ceiling items from each side's own choices | holds | line 168–169 builds the floor from `d_lo` and the ceiling from `d_up` in two calls; lines 180, 189 pair each side's items with its own choices (the comment "common to floor and ceiling" in `window_model_occ.py` 52 is true per call only — finding m15) |
| items without a route are left out | holds | any sub-family of non-negative items is valid; `hyp()` (232–239) tests **all** items |

Item 2 of the brief:

| statement | verdict | basis |
|---|---|---|
| every term of a band model is in exactly one of `F_b`, `B`, `I` | holds | review: a term with first site `≤ s − 1` ends at `≤ s − 1 + w` and is attached to a site eliminated forwards (`held_site_laws.py` 106, 110–114); one with last site `≥ s + w` starts at `≥ s` and is attached, on the mirrored chain, to a site eliminated backwards (86–90); the rest is `inside_terms` (39–52).  Replication §3.2 including a term through the held site, a window right after the held site (2 724 cases), the last window (2 760), unequal alphabets, one-state sites, multi-site terms |
| `assign_routes` | holds under (H-items); otherwise it stops by assertion | lines 62–74 and the assertion at 157.  Fuzz: 0 illegal routes, 0 wrong route/no-route decisions, 0 key collisions, order-independent.  An item that fits a window and lies entirely in the last (first) `w` sites would get a window containing its held site (review); the assertion at line 157 stops such input — 118 of my instances with items that fit a window ended there — never a silent number |
| two different routes inside one group | cannot happen | a group **is** a route key `(direction, held site, window start)`; the driver's enumeration check (line 247) and its bounds use the same keys |
| plus and minus items, and the three classes, are routed in separate greedy sweeps | holds; costs tightness only | `held_site_laws.py` 144: the "same" window may start at different sites for plus and minus items or for different classes; they then fall into different groups, which is valid |
| `bounds()` against item 69 | the four formulas are those of the proposition; see finding m11 | `slack_recovery.py` 194–203 |

Item 3: the regression claim holds in all thirteen runs; all tables agree with the logs (§4).

### 2.2 Major findings

**M1 [major] — "The loss between groups is about `D²/4`" is a rule of thumb that the texts call a measurement;
where I measured it at twelve residues it is 2.1 and 1.5 times that, and the split of the band-4 bracket in item 78
is off by a factor two in its main term.**
*Where:* addenda item 73 (l. 3335–3336: "costs about `D/2` times the amount recovered above: `1.3·10⁻⁵` for Lys₁₂"),
item 78 (l. 3510–3513: "the rest of the `6.4·10⁻⁴` is the loss between groups (`D²/4 = 2·10⁻⁴` for `D = 0.029`) and
the envelope"), item 81 (iii); SCI-RES-0024 §2 (l. 42–45: "consistent with what we measure: the loss between groups
is about `D²/4` …: `1.3·10⁻⁵` of the `2.2·10⁻⁵` nats left for Lys₁₂ at order 5, `8·10⁻⁵` of the `4·10⁻⁴` left for
Lys₂₀.  So pair terms could remove up to about half of what is left in the first case and a fifth in the second;
the rest is the envelope") and its last section (l. 120: "the size of the loss between groups is measured"); audit
A6 (l. 141) and row H4.
*What the logs contain:* the numbers `1.3·10⁻⁵` and `8·10⁻⁵` are `D²/4` evaluated (`0.007138²/4 = 1.27·10⁻⁵`,
`0.01814²/4 = 8.2·10⁻⁵`); no log beyond five residues contains a measurement of the loss.
*What a measurement gives* (loss := corrected width − width with the **same** routed items put back exactly):

| instance | `D` | corrected width | same items put back exactly | **loss** | loss / (`D²/4`) | loss / corrected | source |
|---|---|---|---|---|---|---|---|
| Lys₅, 4, band 2 | 0.04765 | 0.002885 | 0.001614 | 0.001271 | **2.24** | 0.44 | the coordinator's log (enumeration) |
| Lys₅, 4, band 3 | 0.01891 | `6.437·10⁻⁵` | `4.996·10⁻⁵` | `1.44·10⁻⁵` | **0.16** | 0.22 | the same |
| Lys₅, 5, band 3 | 0.01870 | `7.104·10⁻⁶` | `1.573·10⁻⁶` | `5.5·10⁻⁶` | **0.06** | 0.78 | the same |
| LKSE:5, 4, band 2 | 0.2054 | 0.001558 | `8.185·10⁻⁴` | `7.4·10⁻⁴` | **0.07** | 0.47 | the same |
| **Lys₁₂, 4, band 4** | 0.02877 | `6.449·10⁻⁴` | `2.135·10⁻⁴ ± 6·10⁻⁷` | **`4.314·10⁻⁴ ± 6·10⁻⁷`** | **2.085 ± 0.003** | **0.67** | R19, §3.4 [N: exact first order, sampled second order, 10⁶ samples] |
| **Lys₁₂, 4, band 7** | 0.007329 | `8.161·10⁻⁵` | `6.099·10⁻⁵ ± 1.9·10⁻⁷` | **`2.061·10⁻⁵ ± 1.9·10⁻⁷`** | **1.535 ± 0.014** | **0.25** | R19, §3.4 [N; 4·10⁵ samples] |
| 810 random sandwiches with `D < 0.3` | | | | | quartiles 0.002, 0.25, 0.57; **largest 13.3** | | R19, §3.2 (enumeration) |

*Consequences.*  (i) At band 4 the bracket of `6.449·10⁻⁴` is `4.31·10⁻⁴` of loss between groups plus `2.13·10⁻⁴`
that an exact treatment of the routed items would leave — items without a route, the envelope and the allowances
*together*.  Item 78's sentence gives `2 × 1.1·10⁻⁴` to the subsets without a route, `2·10⁻⁴` (`D²/4`) to the loss
and, by difference, `2.2·10⁻⁴` to the envelope; the measured split is `4.3·10⁻⁴` for the loss and `2.1·10⁻⁴` for
everything else.  (ii) At band 7, where 415 of 465 items are routed, the exact treatment leaves `6.10·10⁻⁵` — three
quarters of that bracket — of which the subsets without a route are `5·10⁻⁶` to first order and the evaluation
allowance `2·10⁻⁶` (§3.4): the envelope is about `5.4·10⁻⁵` at order 4, and the loss between groups is one quarter
of the bracket.  (To first order the same `5.6·10⁻⁵` of envelope and allowance sits inside the `2.13·10⁻⁴` of band 4
[H], which leaves about `1.6·10⁻⁴` there for the items without a route; the log's first-order estimate, from 960
Gibbs states, is `2.2·10⁻⁴`.)  (iii) "Pair terms could remove up to about half of
what is left [Lys₁₂ at order 5] and a fifth [Lys₂₀]; the rest is the envelope" (SCI-RES-0024 §2) is not supported.
For order 5 the logs themselves leave no room for an envelope: it is `10⁻⁹` there (item 73), the items without a
route carry `6.5·10⁻⁷`, the evaluation allowance about `2·10⁻⁶` to first order — so roughly `1.9·10⁻⁵` of the
`2.18·10⁻⁵`, about `1.5·D²/4` as measured at order 4, would be loss between groups [H: my inference from first-order
numbers of the log, not a measurement].  For Lys₂₀ nothing is measured.  (iv) `D²/4` is neither a bound nor a
typical value: slacks of different groups that occur at the same states (two groups with the same held site are the
obvious case) lose their cross terms entirely, and a rare, large, shared slack gives 13 times `D²/4` at `D = 0.054`.
*This changes no bracket.*  It changes what the division tells the theory division is left to gain, and where.
*Replacement texts.*  Item 78: "At band 4 the loss between groups, measured with the routed items put back exactly
(workstream R19), is `4.31·10⁻⁴ ± 6·10⁻⁷` — twice `D²/4`, two thirds of the bracket; the subsets without a route
(`1.1·10⁻⁴` per side by the first-order number of the Gibbs sample), the envelope and the allowances are the other
`2.13·10⁻⁴` together."  SCI-RES-0024 §2 and l. 120: "the loss between groups is of order `D²`; `D²/4` is a rule of
thumb for many weakly dependent groups, not a bound: measured, it is 0.06 to 2.2 times `D²/4` on the four enumerated
instances and 2.1 and 1.5 times at Lys₁₂, order 4, bands 4 and 7 (67 and 25 per cent of those brackets); it has not
been measured for Lys₁₂ at order 5 or for Lys₂₀."  Audit l. 141 and H4: "a loss of order `D²` (measured between 0.06
and 2.2 times `D²/4`; no bound of that form holds: up to 13 times on random sandwiches)."

**M2 [major] — audit A1, third row: "the ceiling holds on all of the space: T" is wrong as worded.**
*Where:* `ASSUMPTION_AUDIT.md` l. 49.  *Why:* the evidence next to it ("a ceiling may be `+∞` outside any region")
shows that the ceiling need not be **finite** everywhere; a ceiling that is `+∞` outside a region still *holds* on
all of the space.  The pointwise inequality `E ≤ m₊` wherever `m₊` is finite cannot be dropped, and dropping it is
exactly the mistake the row invites: a band model that is a valid majorant near one mode only, summed over all states
by the transfer matrix.  *Run* (`r19_audit_tests.py` S7, the audit's own ten-state example): ceiling `= E` on the first
mode, `+∞` elsewhere: lower end `0.4519 ≤ ln Z = 0.8825`; a **finite** model that is a ceiling on the first mode only
(`−1` elsewhere): "lower end" `2.7188 > 0.8825` — false; control, a finite ceiling valid everywhere: `0.4548`.
*Replacement:* "| the ceiling is finite on all of the space | **T** | `E ≤ m₊` is needed only where `m₊ < ∞`:
`ln Z(E) ≥ ln ∫_{m₊<∞} e^{−βm₊}dν` [P, one line; X] |" and a new row "| `E ≤ m₊` wherever `m₊` is finite | **F** | a
finite model that is a ceiling on one mode only gives a 'lower end' of 2.72 against `ln Z = 0.88` [X, R19].  A
restricted ceiling is computable only if the region is tractable for the model class: a sub-product of the alphabets
is, a Hamming ball is not band-limited |".

**M3 [major] — A3′, Proposition AA.1 and Corollary AA.2 are presented as "the general statement" of what the proof
uses of `g`; they cover terms without hosts only, the division's own instance is outside them, and the corollary is
false when a host is treated as one more additive site.**
*Where:* l. 79–86 (the class is described **with** hosts — "quantities fixed by the states of a bounded number of
host sites" — and the next sentence drops them: "So the envelope exists, with the same proof, for every energy whose
many-body part is a sum of terms `φ(u(x))`, `u(x) = c + Σ_i a_i(x_i)`"); l. 88–101 (the proposition and the corollary,
stated without hosts); the examples of l. 84–86 ("implicit-solvent terms through effective radii; embedding
functions of a local density") are additive only for a fixed host state.  The owner's directive, as relayed in
SCI-MSG-0029 §1 (l. 88; I read that line only): "Avoid presenting results for restricted models as universal
conclusions."
*Run* (`r19_audit_tests.py` S8): `τ(x) = φ(c(x_h) + Σ_{i≠h} a_i^{x_h}(x_i))`, one host `h`, 200 random instances,
every state.  The bound written from P9's Lemma T′ in this class — `M^{c⁰}_m Π_{i∈T} δ^{c⁰}_i` for `h ∉ T`,
`Σ_{c∈{c⁰, x_h}} M^c_{m−1} Π_{i∈T∖h} δ^c_i` for `h ∈ T` — has **0 violations** in 26 855, 26 855 and 24 635 states
(`m = 2, 3, 4`) and is attained (ratio 1.000).  Corollary AA.2 *as stated*, with the host as an additive site of
increment `|c(x_h) − c(x⁰_h)|`: **1 253, 2 630, 2 068 violations**.  Control of the correct bound, one host
assignment forgotten: 1 485, 2 651, 2 345 violations.
*Replacement:* state the proposition with hosts and call AA.1 its case without:
"**Proposition AA.1′.**  Let `τ(x) = φ_c(κ(c) + Σ_{i∉H} a^c_i(x_i))` with `c = x_H`, `|H| = h < m`, each `φ_c ∈ C^{m}` on
an open convex set containing the values of its argument, and take an order of the sites with `H` last.  For
`T ⊆ S(x)`, `|T| = m`: `|Δ_T τ(z^{T,x}; x_T)| ≤ Σ_{c ∈ 𝒞_x(T)} M^c_{m−|H∩T|} Π_{i∈T∖H} δ^c_i(x_i)`, where `𝒞_x(T)` has
`c_l = x⁰_l` for `l ∈ H∖T` and `c_l ∈ {x⁰_l, x_l}` for `l ∈ H∩T`, `δ^c_i(y) = ‖a^c_i(y) − a^c_i(x⁰_i)‖` and `M^c_j` is the
supremum over the hull, for host state `c`, of the operator norm of `D^jφ_c` induced by `‖·‖`.  The table of `T` is a
sum of at most `2^h` products over the non-host sites of `T` — rank one only for `h = 0`.  [P: P9's Lemma T′ and
Theorem R step (b), which need `m > h`; N: R19 for `h = 1`.]"

**M4 [major] — the growth comparison of A8, labelled [P], rests on a premise that is false in the class it speaks of.**
*Where:* l. 170: "the penalty of `s` displaced sites grows like `s^m` and the cost at most linearly: **such a floor
delocalises on a long enough chain at any fixed order** [P, a growth comparison …]"; repeated to the theory division
in SCI-RES-0024 §3 (b).  *Why false:* the floor is `f + I_{m−1}g − pen`, and `I_{m−1}g` is a sum of `Σ_{j<m} C(s, j)`
evaluated terms; on an exchangeable instance it is Newton's forward polynomial of degree `m − 1` in `s`.  *Run* (S6):
`|I_{m−1}g(s) − g(0)|` grows like `s^{1.00}`, `s^{2.02}`, `s^{2.85}` for `g = sin(2u)` and `s^{1.00}`, `s^{2.03}`, `s^{3.06}`
for `g = e^{−u}` at `m = 2, 3, 4`; a pairwise known part grows like `s²`.  *What survives:* for `m ≥ 3`, `s^m` beats
`s^{max(2, m−1)}`: in the toy the floor's gap `ln Z(m₋) − ln Z(E)` passes one nat at `n = 4 … 7` whatever the pair cost
(S6b), and the floor's mean number of displaced sites exceeds the true one by `n/4` from `n = 4 … 13` (S6).  *What
does not:* "at any fixed order" — at `m = 2` with a pair repulsion `c₂ = 2 > M₂δ² = 1` the gap grows to only 1.07
nats at `n = 200` (one nat at `n = 181`); with `c₂ = 0.5` it passes one nat at `n = 6` and reaches `10⁴` nats.
*Replacement:* "For an envelope `M_m·e_m(δ)` with `M_m` and a positive fraction of the `δ_i` bounded below, the penalty
of `s` displaced sites grows like `s^m`; everything else in the floor grows at most like `s^{max(2, m−1)}` when the
tables are bounded (the pair part like `s²`, the evaluated terms of order `j < m` like `C(s, j)`).  So for `m ≥ 3`
such a floor leaves the anchor on a long enough chain [H, a growth comparison; N: an exchangeable instance, R19];
at `m = 2` it depends on the pair part.  No rate function: `G-4`."

### 2.3 Minor findings

**m1 — the measure-space proof (l. 144–154) is complete except for two signs and one reason.**  With `m₊ = +∞` on a
set of positive measure where `E` is finite — the case A1 advertises — `Z(E)/Z(m₊) = ⟨e^{β(m₊−E)}⟩` is false; it is
`≥` (the mean sees only `{m₊ < ∞}`); likewise `Z(m₋)/Z(E) ≥ ⟨e^{β(E−m₋)}⟩_E` when `E = +∞` where `m₋` is finite.  Both
inequalities point the right way and the result stands.  The last sentence gives the wrong reason: the iterates
are upper bounds by induction (if `u_t ≥ ln Z(E)` the inequality just proved gives `u_{t+1} ≥ ln Z(E)`); monotonicity
of the right-hand sides is what makes the sequence decrease.  The rest I checked and found complete: `e^{βs₊}` is
integrable under the ceiling because its mean is at most `Z(E)/Z(m₊) < ∞`, hence `⟨s₊⟩ < ∞` and Jensen applies;
countable sums by monotone convergence and finite partial products; `C`, `C′ < ∞` follow from the hypotheses;
`Z(E) = ∞` is excluded by `Z(m₋) < ∞`; points with `m₊ = ∞` carry no ceiling weight and drop out because `X ≥ 0`;
σ-finiteness is not used.  *Replacement:* "`Z(E)/Z(m₊) ≥ ⟨e^{β(m₊−E)}⟩`, with equality iff `m₊ < ∞` almost everywhere
on `{E < ∞}`" (twice), and "If `u_t ≥ ln Z(E)` then `u_{t+1} ≥ ln Z(E)` by the last display; the right-hand sides are
non-decreasing in `u`, so the iterates decrease."

**m2 — A3, "`m ≥ 3`: T / Q … used once … the general condition is the one of A2 (hosts per term at most `m`)"
(l. 76).**  The proof of the envelope uses it twice: step (b) of Theorem R (a host outside `T` at the anchor needs
`h ≤ m`) and the hypothesis `B = T∖𝓗(τ) ≠ ∅` of Lemma T′ (needs `h ≤ m − 1`).  At `h = m` the subset `T = 𝓗(τ)` has no
bound of the class A3′: two hosts, `m = 2`, all additive increments zero — remainder 0.80 at order 2, `6·10⁻¹⁷` at
order 3 (S7).  *Replacement:* "`m ≥ 3` | **Q** | `m > h` (hosts per term) for an envelope built from derivative bounds
(Lemma T′ needs a non-host site in every `T`); `h ≤ m` suffices for the identity and for abstract constants [V,
theirs: `anchored_remainder_bound_hosts`; header read by R19], but at `h = m` the table of `T = 𝓗(τ)` is the hosts'
mixed difference times `sup|φ|` and does not vanish with the displacement [X, R19]".

**m3 — A4, "non-negative bounds `Φ_T`: E" (l. 115).**  The machine-checked statement the row cites says "nothing is
assumed about the signs of `Φ` and `γ`" (`resolved_allocation`, docstring and hypotheses read by me at `3cf14b9`):
what is needed is `c_{T,U} ≥ 0` (its hypothesis `hc0`), and that one is **F** without: two binary sites, `Φ_T = −1`,
`c = max Φ = −1`: the allocation inequality reads `0 ≤ −1` (S9).  *Replacement:* "| tables `c_{T,U} ≥ 0` | **F**
without | [X, R19]; [V, theirs] | `Φ_T ≥ 0` | **T** — sufficient for `c ≥ 0`, not needed [V, theirs] |".

**m4 — A5, "finite alphabets: X / [?]" (l. 127), and `G-8`.**  Class X needs "the two complexities, with the source
of each"; the row gives neither.  By the audit's rule (1) it is **[?]**.  `G-8` (l. 290) counts three "[K, from
memory]" entries; the text has two topics (hardness of general partition functions; treewidth) — the third,
"information-based complexity of smooth classes", occurs nowhere.

**m5 — A6, "every group slack is non-negative: F for (LP), (UE), (UP)" (l. 138)** has a run counterexample for (LP)
only, against the audit's rule (2).  Supplied (S7): (UP), the same two groups as minus-slacks: limit `0.4055 < ln Z =
0.6931`; (UE), a negative minus-group paired with a positive plus-group: first iterate `−0.804 < 0.693`; a negative
plus-group: `−0.421 < 0.693`; the three controls hold.  One precision: signed minus-groups alone do not break (UE)
when every `S⁺_g` is zero (the formula is then linear in `S⁻`); the failure needs the pairing.  **Confirmed.**

**m6 — A7, second row (l. 161)** is out of date: "being removed … regression runs in progress … not yet in the
addenda and its code not yet in the tree".  It is item 77, `held_site_laws.py` is in the tree since `0930440`.

**m7 — item 78, l. 3478–3480:** "They do in every row that uses only the old routes — far pairs; far pairs and terms;
all three stages where no item goes through an inner window".  The far-pairs-and-terms row is unchanged in six of the
thirteen runs only; in seven (Lys₅ and LKSE:5 at band 2, Lys₁₂ order 5, Lys₁₂ order 4 at bands 5 and 4, (LKSE)₃
order 5, Ser₁₂) term items are newly routed and that row moves.  The claim "same items, same digits" is unaffected.
*Replacement:* "They do in every row whose routed items are the same: the far-pair row in all thirteen runs, the
far-pairs-and-terms row in the six runs in which no term goes through an inner window, all three stages in three."

**m8 — "The published brackets stand" (SCI-RES-0024 l. 99–100); "confirmed as brackets — the new ones lie inside
them" (item 81 (ii)).**  Nesting follows from the monotonicity of the four bounds in the items whenever both
computations are right, and would hold just as well if both were wrong in the same way (same models, same tables,
same `bounds()`): it is evidence of **consistency** of two versions of one code, not of validity.  The evidence of
validity is elsewhere: the hypotheses at every state and the exact `ln Z` on four enumerated instances, the sampled
intervals, and now §3.  *Replacement:* "the published brackets are implied by the new ones, which lie inside them;
that either is a bracket rests on items 71, 73 and on the referee's replication, not on the nesting."  (A consistency
check with more content, from the logs: all six deterministic brackets of the same `ln Z` of Lys₁₂ — order 3,
order 4 at bands 4, 5, 6, 7, order 5, from three balls and six pairs of models — and the sampled interval of part
(18) have the common part `[517.1285396, 517.128559]`.)

**m9 — what the checks of items 71, 73, 78 can see.**  (a) The hypothesis check sees a doubling of **every single
item** on the enumerated instances (25/25, 11/11, 15/15, 25/25) and of all far and term items and 458 of 462 /
277 of 285 allocation items at the 5 380 states of Lys₁₂ (bands 4, 7): the accounting is tested item by item.
(b) It sees **nothing** when every `Θ_T` inside the allocation items is halved or divided by ten (0 violations in all
six cases): the envelope is at least 10.75 times the remainder at every state tested, so the check certifies the
bookkeeping of the reductions, not the size of P9's tables.  (The audit's new A10 notes the same of a control of its
own.)  (c) "The means against exact samples within 1.6 standard errors" has no power: with 400 000 samples of my own
15 of 280 group statistics of Lys₁₂ at band 4 are more than three standard errors off, the worst 12.8, while my
exact replication agrees with the driver to `6·10⁻¹²` — the summands are dominated by rare states, the sample means
are biased low and their standard errors too small.  The coordinator says "the test of the means is item 71, not
this"; at twelve residues there was then no test of the means at all.  There is one now (§3.3).
*Replacement for "Checks in every row" of item 78:* add "the hypothesis check tests the accounting of the
reductions item by item; it cannot see an error of P9's tables smaller than a factor ten; the sampled comparison of
the means is a sanity check only".

**m10 — coverage of the enumerated tests.**  Routed allocation items occur in one of the four enumerated cases (Lys₅,
order 4, band 3: two items); the route through a window inside the chain is exercised by four **term** items; no
allocation item through an inner window is enumerated, while these are the bulk of the new routes (Lys₂₀: 2 029 of
3 823 routed items go through inner windows).  Closed by §3.3 (Lys₁₂ at band 4: 161 routed allocation items, 251
items through inner windows, 56 groups, all recomputed).

**m11 — `slack_recovery.bounds` (l. 194–203) and its use (driver l. 227).**  (a) Item 69 and the docstring state the
limits `u*`, `v*`; the code returns the 60th iterate.  Valid — every iterate is a bound — but not the limit for a
wide sandwich: (UP) is short by `2.3·10⁻³` at `D = 2.36` and by 3.2 nats at `D = 7.3` (irrelevant at `D ≤ 0.2`, where
60 steps reach machine precision).  (b) Nothing tests lower ≤ upper: inconsistent statistics give `UE = −∞` and an
empty bracket that only `--enum` would notice.  (c) A mean that overflows gives `LP = +∞`, which `max(LJ, LP)`
selects; a `nan` is survived only by the order of the arguments of `max` and `min`.  *Replacement:* iterate to a
tolerance; `assert np.isfinite(...)` and `lo_ <= up_`; cap every item table at a few hundred `kT` (a smaller
non-negative table is always valid).

**m12 — level H2′ (hierarchy)** — right in substance, incomplete as stated; see §5.3 for the statement with its
allowance.  The number of bins is not a free parameter (`B ≈ R/h + n`), and the allowance accumulates over the sites
and is attained.

**m13 — A3′ (b), "the mean of such an envelope under any band model is exactly computable".**  True; I implemented it
(a transfer matrix with polynomial entries: 923 means against enumeration, `7·10⁻¹⁵`).  What it yields is a
first-order number or a Jensen lower end; a floor needs `Z(m − env)`, which no band model holds.  Without an
allocation to tables the envelope `M_m·e_m(δ)` is not a certificate — the audit should say so where it says
"exactly computable".

**m14 — AA.1, the norm (l. 93, 100).**  "The norm of `D^mφ`" must be the operator norm induced by the norm used for
the increments.  With Euclidean increments and the `ℓ¹` operator norm: `φ = (u₁ + u₂)²/2`, two sites with increments
`(1, 1)`: remainder 4, "bound" 2 (S2).  Also: for infinite `X_i` ("any sets") `M_m` may be `+∞`.

**m15 — a comment.**  `window_model_occ.py` l. 52, "the choices, once, common to floor and ceiling": the driver calls
the builder twice, so the two sides choose separately.  Harmless.

### 2.4 Item 5 — what the certified numbers do and do not show

A reader of SCI-MSG-0028 and SCI-RES-0024 sees "Lys₁₂ certified within `8·10⁻⁵` nats", "Lys₂₀ within `4·10⁻⁴`".
**What is certified** is an interval for `ln Z` of one *model* energy — the ff14SB vacuum energy plus the GBn2
solvent term of Ace-Lysₙ-NMe on a fixed helical backbone with a finite rotamer library (`9.5·10¹⁰` and `5.5·10¹⁷`
states), at one temperature — **given** (i) that workstream P9's stage-2 tables satisfy Theorem R at every state: a
paper proof by one workstream, re-derived by the coordinator, machine-checked only in its abstract skeleton, tested
at every state on five residues and entry by entry at 5 000–20 000 states with exactly `m` side chains off, where
the tables exceed the remainder by a factor of at least 8.9 (4.6 for serine) — so a table too small by less than that
would pass every test; (ii) that every evaluated value of `g` is within `ε_g = 10⁻⁷` kcal/mol of the function —
assumed, with an a-priori estimate that is not a proof for the summation order used; (iii) one implementation of the
evaluator, of the tables and of the transfer matrices, of which this review replicated the held-site statistics and
the accounting and re-ran six logs, and nobody has re-implemented the tables; (iv) double-precision arithmetic with
margins of `10⁻⁹` and no interval control.  **What a reader may not conclude:** that the free energy of a peptide in
water is known to `10⁻⁴` nats (`10⁻⁴` nats is `6·10⁻⁵` kcal/mol; the error of an implicit-solvent model against
explicit water is commonly put at the order of a kcal/mol [from memory — unverified], and backbone, rotamer library
and force field are modelling choices); that the bracket is a machine-checked certificate (the proposition and the
allocation are; the hypotheses for these tables, the transfer matrices and the arithmetic are not); that the width
measures what the evaluations know (a quarter to two thirds of it is the loss between groups where I measured it,
and the envelope behind the rest is at least ten times the remainder at every state I tested); that the method
reaches such widths in general (these are side-chain ensembles on a fixed helix that are mostly frozen at the
anchor — 1.2 of 12 lysine side chains off on average; (LKSE)₃ at order 3 is not certified at all); or, for Lys₂₀,
that the number has been compared with anything (no sampled interval, 38 % of its items without a route, a run above
the limits of this review).

## 3. My own tests, with their controls

All scripts and logs are in `experiments/science/ws_R19/`; every log cited reached its last line; the last line of
each prints the peak memory.

### 3.1 The accounting as an identity (item 1) — `r19_item1_identity.py`, `r19_item1_sampled.py`

*Method.*  The committed driver is run unmodified in-process (a **re-run**); a profile hook copies the local objects
of its `main()` (models, items, routes, tables, choices).  With **my** code: my own evaluation of the two models from
their tables; my own interpolant from the enumerated values of `g`; `env(x)` and `pen(x)` from P9's raw tables and the
kept sub-tuples; `A(x) = ε_g(1 + Σ_{j<m} C(t, j)2^j)`, `t` sites off.  Tested: `R₊ := m₊ − E − s₊ = A + (RND − 1)pen + env − r`
and the same below with `+r`, up to the `10⁻⁹` by which the driver lowers each item.  A slack counted twice anywhere
makes the residual negative by that slack, whatever the margin.

| instance | states | residual `R − P` (allowed) | (b1) model − source model = far + term items | (b2) `pen − env` = alloc items | (b3) smallest `env/|r|` |
|---|---|---|---|---|---|
| Lys₅, 4, band 2 | all 115 248 | `[−2.2·10⁻¹³, 1.5·10⁻⁸]` (`[0, 15·10⁻⁹]`); 0 states outside | 0 outside | 0 outside | 10.75 |
| Lys₅, 4, band 3 | all 115 248 | `[−4.7·10⁻¹³, 7·10⁻⁹]` (`[0, 7·10⁻⁹]`); 0 | 0 | 0 | 10.75 |
| Lys₅, 5, band 3 | all 115 248 | `[−4.7·10⁻¹³, 8·10⁻⁹]` (`[0, 8·10⁻⁹]`); 0 | 0 | 0 | 12.49 |
| LKSE:5, 4, band 2 | all 14 508 | `[−1.1·10⁻¹³, 1.5·10⁻⁸]` (`[0, 15·10⁻⁹]`); 0 | 0 | 0 | 17.03 |
| Lys₁₂, 4, band 4 | the driver's 5 380 | `R − P − 10⁻⁹·`(non-zero items) in `[−3.2·10⁻¹², 1.0·10⁻⁹]` | — | — | 13.28 (2 331 states outside the ball) |
| Lys₁₂, 4, band 7 | the driver's 5 380 | `[−3.5·10⁻¹², 1.7·10⁻⁹]` | — | — | 13.28 |

(The positive ends at twelve residues are one or two items whose raw value lies in `(0, 10⁻⁹]` and is clipped.)

*Controls* — "hyp" is the driver's own test (violations at ceiling, floor), "id" my identity:

| control | Lys₅ 4/2 | Lys₅ 4/3 | Lys₅ 5/3 | LKSE:5 4/2 | Lys₁₂ band 4 | Lys₁₂ band 7 |
|---|---|---|---|---|---|---|
| no change (must be 0) | 0, 0 | 0, 0 | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| **K1** each single item doubled: items seen by hyp | 25 of 25 | 11 of 11 | 15 of 15 | 25 of 25 | far 56/56, term 336/336, alloc 458/462 | 20/20, 160/160, 277/285 |
| **K2** allocation slack of the floor moved to the ceiling (`s₊ + s₋` unchanged) | 86 594, 0 | 44 361, 0 | 22 906, 0 | 8 804, 0 | 2 552, 0 | 1 931, 0 |
| **K3** the whole penalty claimed on both sides (the envelope counted as recoverable) | 40 889, 21 383 | 40 892, 21 386 | 815, 1 910 | 5 500, 3 186 | 387, 343 | 387, 343 |
| **K4** `Θ` halved inside the alloc items: hyp / id | **0, 0** / 105 612 each | **0, 0** / 105 612 | **0, 0** / 66 905 | **0, 0** / 9 336 | **0, 0** | **0, 0** |
| **K4b** `Θ` divided by ten: hyp | **0, 0** | **0, 0** | **0, 0** | **0, 0** | **0, 0** | **0, 0** |
| **K5** one class doubled alone (far; term; alloc): hyp | all fail | all fail | all fail | all fail | all fail | all fail |

K1–K3 are the controls "the coordinator did not run that would catch a slack counted twice": every single item is
tight at some state, a one-sided double count of the allocation slack is caught at thousands to tens of thousands of
states, and so is a claim of the envelope itself.  K4 marks the limit of the driver's check (finding m9).

### 3.2 The held-site passes against brute force (item 2) — `r19_heldsite_fuzz.py`, log `r19_heldsite_fuzz_v3.log`

Imports: workstream P3's `pwmodel`, the coordinator's `window_model` (the model class), `slack_recovery`,
`held_site_laws`.  Mine: instances, enumeration, model evaluation, grouping by route, statistics, legality test.

* **Part A**, 3 000 random instances (4–9 sites, 1–4 states per site and different per site, band 1–4; 3 382 797
  states enumerated; 7 702 multi-site terms; 3 191 one-state sites); 30 880 items, 14 172 routed (7 587 forward,
  6 585 on the mirrored chain, **3 570 through a window inside the chain**), 16 708 without a route.  Illegal routes
  0; wrong route/no-route decisions 0.  **65 670 statistics (`a, e, b, c, cp`, three cumulative stages) against
  enumeration: largest relative deviation `6.35·10⁻¹³`**; masses to `2.8·10⁻¹⁴`; the older module
  `slack_recovery.group_stats` on 4 507 groups: `6.35·10⁻¹³`.  The four bounds of `bounds()` and mine against the
  exact `ln Z` of a truth built to satisfy the hypotheses: 0 violations in 3 000; every iterate of (UE), (UP) an
  upper bound; both iterations monotone.
  *Controls that must fail:* one item left out of the enumeration of its group: detected in 5 074 of 5 074; the law
  without the backward message differs in 740 groups — the transfer-matrix numbers agree with the right law and not
  with the wrong one in 740 of 740; every item doubled: the "bracket" excludes the truth in 937 of 3 000.
* **Part B**, windows chosen by me (every legal start): 4 190 groups, 2 724 with the window right after the held
  site, 2 760 with the last window: `1.6·10⁻¹⁴`.
* **Part C**, `assign_routes` alone on chains of up to 40 sites, band up to 8: 238 267 items, 90 850 routed, 0
  illegal, 0 incomplete, 0 key collisions, 0 changes under permutation of the list.
* **Part D**, `bounds()` at the edges: finding m11.

### 3.3 The group statistics at twelve residues, exactly, without windows — `r19_groups_exact.py`

The law of `S_g` needs only the joint marginal of the sites that the items of the group touch.  My code sums out all
other sites of the ceiling model by plain variable elimination on its tables (stored by `r19_dump_case.py` from a
re-run of the driver) — no window, no held-site pass, no code of the division.

| case | groups recomputed | statistics | largest relative deviation from the driver | masses | `ln Z(m₊)`, `ln Z(m₋)`: mine − driver | control (one item left out) |
|---|---|---|---|---|---|---|
| Lys₅, 4, band 2 | 6 of 6 | 30 | `9.6·10⁻¹³` | `8.9·10⁻¹⁴` | 0, 0 | 6 of 6 detected |
| **Lys₁₂, 4, band 4** | **56 of 56** (161 routed allocation items; 251 items through inner windows) | 280 | **`5.8·10⁻¹²`** | `7.8·10⁻¹³` | `+4.5·10⁻¹³` each | 56 of 56 |
| **Lys₁₂, 4, band 7** | 5 of 20: `fwd0@3`, `rev11@2`, `rev11@4` (inner windows), `fwd3@5`, `rev8@5` | 25 | **`2.8·10⁻¹³`** | `1.2·10⁻¹²` | `0`, `−4.5·10⁻¹³` | 5 of 5 |

For band 4 the four bounds recomputed from my `ln Z` and my statistics give `[517.128329993, 517.128974847]`, the
driver's to `1.5·10⁻¹¹`.  **The published Lys₁₂ bracket at band 4 is reproduced by an independent computation of
everything between the tables (of the two models and of the items, with the driver's grouping) and the number**; at
band 7 the two `ln Z` and five groups are.

### 3.4 The loss between groups, measured — `r19_loss_between_groups.py` (finding M1)

`ln Z(m₊ − s₊)` and `ln Z(m₋ + s₋)` (`s_±`: the routed items) from `10⁶` (band 7: `4·10⁵`) exact samples of the
**floor**, with bounded integrands and the first order removed exactly: `⟨m₊ − m₋⟩` under the floor by workstream
P3's transfer matrix for moments (checked by my enumeration: `0.08987236088` both), `⟨s_±⟩` under the floor by
held-site passes on the stored routes (the module validated in §3.3).  *Validation* against the driver's enumeration: Lys₅ band
3: width `5.0025·10⁻⁵ ± 5.5·10⁻⁷` against `4.996·10⁻⁵`; Lys₅ band 2: `0.001639 ± 1.3·10⁻⁵` against `0.001614`
(1.9 standard errors; heavy tails at band 2).  Results: the table of M1 — Lys₁₂, order 4, band 4:
`[517.128439887 ± 1.5·10⁻⁶, 517.128653342 ± 1.2·10⁻⁶]`; band 7: `[517.128513845 ± 3.1·10⁻⁷, 517.128574839 ± 2.4·10⁻⁷]`
(the two ends are computed from the same samples; the error of the width is that of the per-sample difference).
The first-order cost of the evaluation allowance attached term by term, `2β⟨A⟩`, is `2.1`–`2.2·10⁻⁶` nats at order 4
and `2.2`–`2.3·10⁻⁶` at order 5 for Lys₁₂ (`r19_allowance_first_order.py`, `10⁶` samples of floor and ceiling).
(A first version sampled `⟨e^{βs₊}⟩` under the ceiling and failed this validation by 22 standard errors — my error, §6.)

### 3.5 Part A of the audit — `r19_audit_tests.py` (no code of the division), log `r19_audit_tests_v3.log`

| test | sizes | result | controls |
|---|---|---|---|
| **S1** Corollary AA.2, `g = Σ_p φ_p(c_p + Σ_i a_{p,i}(x_i))`, families `e^{λu}`, `sin(ωu + θ)`, `(c + u)^{−s}`, `u^q`, 1–5 terms, random anchor, every state | 300 instances, 227 561 states for each of `m = 2, 3, 4` (225, 221 729 for `m = 5`) | **0 violations**, for the sum, term by term, for the cruder `(Σδ)^m/m!`, and at the states with exactly `m` sites off.  Attained (bound/remainder 1.000); median over instances of the smallest ratio 1.8–2.2, of the median ratio 9–14 | `M_m` halved: 8 540, 12 447, 13 966, 15 082 violations; `M_m` → supremum of the derivative of order `m − 1`: 7 647, 11 711, 12 301, 11 597; `M_m` → `|φ^{(m)}|` at the anchor's value: 24 501, 30 280, 34 217, 24 928.  On an instance built to be tight (`e^{2u}`, small increments: ratio 1.29–1.51) the halved bound fails at **every** state with a non-zero bound (716, 656, 496) |
| **S2** two statistics, `φ = ψ₁(u₁)ψ₂(u₂)` | 200 instances per `m` | 0 violations with (`ℓ¹` increments, `ℓ¹` operator norm) and with (Euclidean, `2^{m/2}·ℓ¹` norm) | inconsistent pair: 1, 0, 11 violations at random; deterministic: remainder 4 against 2 |
| **S3** the remainder identity with its contexts, random functions, random orders; AA.1 for every term with a non-anchor context | 12 instances, 1 418 states, 1 796 terms | identity to `10⁻¹⁵`; 0 violations; largest ratio 0.806 | — |
| **S4** `⟨e_j(δ)⟩` under a band model by a polynomial transfer matrix (`G-1`, second half) | 200 models, 923 means | `7·10⁻¹⁵` from enumeration | the product-measure formula differs (1.676 against 1.571) |
| **S5** level H2′ | 120 instances × 4 grids | the exact `ln Z` inside in 480 of 480; width/(`β·Lip·n·h`): median 0.71, largest 0.93 | allowance of one cell: truth outside in 2–9 of 120 at random, and for `n = 2, 4, 8` on an instance built for it, where the accumulated allowance is attained |
| **S6, S6b** A8 | exchangeable instance, `n ≤ 400` | finding M4 | — |
| **S7, S9** classifications | — | findings M2, m2, m3, m5 | each with its control |
| **S8** the class with a host | 200 instances | finding M3 | two |

## 4. Re-runs, and the check of the tables

*Re-runs of the coordinator's driver* (unmodified; output compared with the committed log after removing timings and
memory): `K5 4 2 --enum`, `K5 4 3 --enum`, `K5 5 3 --enum`, `LKSE:5 4 2 --enum`, `K12 4 4`, `K12 4 7` — **all six
identical**, including the brackets `[517.1283300, 517.1289748]` and `[517.1285108, 517.1285924]`.  Not re-run: Lys₁₂
at order 3 and at bands 5, 6; Lys₁₂ at order 5 and (LKSE)₃ at order 5 (3.9 and 4.3 GB by their logs, at or above my
4 GB limit); (LKSE)₃ order 4; Ser₁₂; Lys₂₀ (5.5 GB, 23 minutes).  A snapshot of every cache directory and of the
committed logs before and after my runs (`snap_*.txt`) shows no change made by me; files that changed in the same
period (`floor_transition_*.log` and others) were written by other processes of the division.

*The regression claim* (`r19_item3_logs.py`, **read only**; old logs by `git show 90abf0e:`).  In all thirteen runs:
sandwich, items, ball, allowance bracket identical; the hypothesis check and its two controls identical to the last
digit; every stage row whose routed items (by class) are unchanged is identical in all printed digits; every other
row lies inside the old bracket at both ends (Lys₁₂ order 5: the upper end equal to seven decimals).  Three runs are
identical throughout (Lys₅ at band 3, twice; Lys₁₂ at order 3).  The item tables themselves are not in the logs, so
"same items" is read from the numbers of routed items per class.

*Tables.*  Item 78: 104 of 104 numbers agree with the logs; "within 1.6 standard errors": largest 1.6; "343 to
2 733": yes; "8 and 6 per cent": 7.8 and 6.2; "`1.1·10⁻⁴`": 0.000105952.  Item 79: every number that the log
contains agrees (45.23; 385 566; `0.0181381`; `[800.5150660, 800.5154710]`; `7.586·10⁻⁴`, `6.98·10⁻⁴`, `4.051·10⁻⁴`;
6 175 = 156 + 1 664 + 4 355; 3 823; 2 029; 2 352; 2 240; `1.15·10⁻⁵`; 156 groups; 8 029, 3 501; 10.859, 239.7, 5 556;
1 390 s, 5 469 MB); the sentence on the heterogeneity of the tables ("`2·10⁻⁶` to 0.8 `kT`, median `4·10⁻⁴`") has no
counterpart in the log and was not checked.  SCI-RES-0024 §3 (a): the eight `ln Z` agree digit for digit, as do
0.0097 and 0.0117; §4: `8.297·10⁻⁵ → 8.161·10⁻⁵`, `1.433·10⁻⁴ → 1.407·10⁻⁴`, `6.875·10⁻⁴ → 6.449·10⁻⁴`; §2: 20 and
156 groups — and the two numbers of finding M1.

*Is "the published brackets stand" justified?*  As a statement that nothing contradicts them and that the new
brackets imply them: yes.  As evidence that they are brackets: no — finding m8.

## 5. Part A of the audit

### 5.1 The two propositions

* **Measure-space form of A17.19** (A6): complete after the repair of finding m1 [P; review].
* **Proposition AA.1**: the proof is correct [P; review; N: S3, 1 796 terms with non-anchor contexts].  The points of
  evaluation `u(z) + Σ t_i d_i`, `t ∈ [0, 1]^m`, are convex combinations of the `2^m` values `u(z ∪ y_V)`, so they lie
  in the hull; the context `z^{T,x}` enters only through `u(z)`, which is a value of `u`.  Conditions to add: the
  operator norm induced by the norm of the increments (m14); `M_m < ∞` (automatic for finite `X`); no hosts (M3).
* **Corollary AA.2**: holds [P; N: S1, 0 violations at every state, attained, three controls fail].  `G-1` is
  discharged for the host-free class; with hosts the statement to test is AA.1′ of finding M3, which also held.
  "The resolved table of a subset has rank one" **does** claim that the *bound of one host-free term* is a product
  over the sites of `T`; it **does not** claim that the true mixed difference is, nor that P9's table `Θ²_T` (a sum
  over terms, blocks, host assignments and partitions) is, nor that a sum of `P` terms is — that has rank up to `P`.

### 5.2 The classifications

"Confirmed" means the evidence next to the row suffices for its class, or I supplied what was missing.

| row | class in the audit | verdict | remark |
|---|---|---|---|
| A1 the space is finite | T | **confirmed** | one line; with `m₊ = +∞` allowed |
| A1 the floor holds on all of the space | F | **confirmed** | run, with control |
| A1 the ceiling holds on all of the space | T | **rejected as worded** | M2: finiteness is T, validity where finite is F |
| A1 `Z(m_±)` computable | X | confirmed | refers to A5 |
| A2 product structure | E | confirmed | — |
| A2 finite alphabets | T [V, not read] | **confirmed**, reading level raised | header of `TermOrders.lean` at `3cf14b9` read by me: arbitrary types with decidable equality |
| A2 one anchor | C | confirmed | — |
| A2 one order for all terms | T up to `h ≤ m`, F beyond | **confirmed** | their example re-run (S9): pair mixed differences 0, remainder 1 |
| A3 some bound on the mixed differences | F without | **confirmed** | numbers of `aa01_essential.log` agree with the text |
| A3 `g` is GBn2 | C, structural condition | **weakened** | M3: the structural condition proved here excludes hosts |
| A3 `m ≥ 3` | T / Q | **weakened** | m2: used twice; the envelope needs `m > h` |
| A4 chain, band, geometry | not used | confirmed | [V, theirs; docstring read] |
| A4 non-negative `Φ_T` | E | **rejected** | m3: `c_{T,U} ≥ 0` is what is needed (F without); `Φ` may be signed |
| A5 chain with a band | C; X [K, from memory] | confirmed as tagged | the tag is honest; sources still owed (`G-8`) |
| A5 the band is wide enough | Q | confirmed | `6.449·10⁻⁴` against `7.329·10⁻³` in the logs |
| A5 finite alphabets | X / [?] | **weakened to [?]** | m4 |
| A6 the space is finite | T | **confirmed** | after m1 |
| A6 group slacks non-negative | F for (LP), (UE), (UP); T for (LJ) | **confirmed** | m5: the missing runs supplied |
| A6 laws known exactly | Q | confirmed | all four bounds are monotone in the statistics |
| A6 which items form a group | C; Q | confirmed | — |
| A6 no joint law: "a loss of about `D²/4`" | — | **rejected** | M1 |
| A6 the ceiling is a band model | C | confirmed | — |
| A7 one window | C | confirmed | replicated (§3.2, §3.3) |
| A7 chain at most `2w` | C, "being removed" | **weakened** (out of date) | m6 |
| A8 "concentrated near one reference" | Q | confirmed | numbers agree with the logs |
| A8 "the floor stays at the anchor" | Q; [P] growth comparison | **weakened** | M4: [H], true for `m ≥ 3`, false premise |
| A9 `ε_g` | E, unproved | confirmed | stated honestly |

(A8 "the band holds what matters" and A9 "the instance" refer to other rows and are not counted.)  19 confirmed, 5
weakened or reworded, 3 rejected as written.

### 5.3 The hierarchy

H0–H2 are standard and correctly costed.  **H2′**, with its allowance: *let `E = m + φ(u)`, `m` a band model,
`u = c + Σ_i a_i(x_i) ∈ ℝ`, `|φ(v) − φ(v′)| ≤ Lip·|v − v′|` on the range.  Round every increment to a grid,
`ã_i(b) = h·round(a_i(b)/h)`, and put `ρ = Σ_i max_b |a_i(b) − ã_i(b)| ≤ nh/2`.  A transfer matrix whose state is (window,
grid value of the partial sum) gives the exact law of `ũ = c + Σ ã_i` under `m` at cost `O(n k^{w+1} B)`,
`B = (range of ũ)/h + 1 ≤ R/h + n + 1`.  Then `ln Z(m + φ(ũ) + Lip·ρ) ≤ ln Z(E) ≤ ln Z(m + φ(ũ) − Lip·ρ)`, of width
exactly `2β·Lip·ρ ≤ β·Lip·n·h`; with the extreme values of `φ` on `[ũ − ρ, ũ + ρ]` in place of `φ(ũ) ∓ Lip·ρ` the
bracket is narrower and needs no Lipschitz constant.*  For a width `ε`: `B ≈ β·Lip·n·R/ε`, cost
`O(n k^{w+1}(β·Lip·n·R/ε)^r)` for `r` statistics — polynomial in `n` and `1/ε` at fixed `r`.  The audit's "width
`≲ β·Lip(φ)·n·`(cell size)" is right; what it leaves out is that `B` grows with `n` at fixed `h` and that the
allowance is the **accumulated** rounding, which is attained (S5: with the allowance of one cell the truth is outside
for `n = 2, 4, 8`).  [P, elementary; N: S5, 480 of 480, `r = 1` only; `r ≥ 2` not tested.]
*Against H3 on one instance* (nine sites, three states, `g = sin(1.5u + 0.4)`, 6.1 of 9 sites off the anchor on
average): the bracket of the H3 envelope itself, by enumeration, is 7.6, 11.8, 7.2, 1.24, 0.21 nats at orders 2–6
(balls of 19 to 6 883 evaluations); H2′ gives 0.74, 0.23, 0.046 nats with 65, 257, 1 025 grid values and no ball.
H3 "width `≈ 2β⟨envelope⟩`" and H4 "`D²/4` between groups": see M1.  H5, H6: read only.

### 5.4 Restricted results presented as general; general statements that are computationally empty

Restricted as general: M3 (AA.1 without hosts), M4 ("at any fixed order"), M1 (a rule of thumb as a law).  Valid but
computationally empty without saying so: m13 (the exactly computable mean of the envelope is not a floor).  The
measure-space forms of A1 and A6 are valid and empty beyond tractable models; A6 says so ("exact means need a model
whose conditional marginals are computable") and A5 flags the continuous case as [?] — adequate.

## 6. What I did not check; my own errors; files

**Not checked.**  Workstream P9's stage-2 tables, their code and the proof of Theorem R (not my object; I tested its
consequence `|r| ≤ env` at every state of two five-residue peptides and at 2 331 states of Lys₁₂).  The evaluator,
the ball values, `ε_g`.  The runs I did not re-run (§4) — in particular nothing of Lys₂₀, of Ser₁₂ and of (LKSE)₃
beyond their logs.  The Lean files (statements and docstrings read at `3cf14b9`, nothing built).  The nested-sampler
intervals quoted for comparison.  The prior-art sentences of item 69 (no network).  Items 72 and 74 beyond their
numbers in the logs of `90abf0e`.  Section A10 of the audit, Parts B–D except H2′ and the rows named.  *Reading
levels:* the addenda items 58–81, the audit at `0930440`, SCI-RES-0024, the five code files, `pwmodel.py`,
`window_model.py`, `GibbsRecovery.lean` (statements) — in full; `P9_REPORT.md` — §1 in full, the rest not;
`ResolvedPenalties.lean`, `TermOrders.lean` — docstrings and the statement of `resolved_allocation`;
SCI-MSG-0028, SCI-MSG-0029, `OWNER_DIRECTIVES.md` — only the lines found by a search for the sentences quoted.  Floating-point
error bounds: none exist; my replications agree with the driver to `10⁻¹¹`, which is evidence, not a bound.  H2′ for
more than one statistic.  The loss between groups for Lys₁₂ at order 5 and for Lys₂₀.

**My own errors.**  (1) `r19_groups_exact.py` on Lys₁₂ band 4, first run: **4 915 MB peak, 823 s** — above the 4 GB
limit of the brief; my elimination order built arrays over nine sites for groups whose held site is on the right.
Noticed at the end of the run; the numbers are right; a corrected order does the same in 2 s and 79 MB
(`…_v2.log`, the one to cite).  The same run exceeded the ten-minute limit of the shell call and went on in the
background.  (2) The first version of the loss estimator sampled `⟨e^{βs₊}⟩` under the ceiling and was off by 22 of
its own standard errors on Lys₅ at band 2 (a heavy tail); caught by the validation I had planned, replaced by an
estimator with bounded integrands; its logs are in `not_cited/`.  (3) In the fuzz test the control "one item left
out" had an absolute threshold and "missed" 1 of 975 and then 12 of 5 074 groups; the criterion was wrong, not the
code under test; `…_v3.log` is the one to cite.  (4) In the audit tests I iterated (UE) on an input that violates
its hypotheses and the iteration overflowed (the stopped log is in `not_cited/`); and my first deterministic example
for the inconsistent pair of norms (`φ = u₁u₂`) did not fail — it is attained — and was replaced.  (5) My time
estimates were poor ("seconds per group" for (1)).  (6) I first read the per-group `z`-scores of a sampling test as
a possible sign of a bias in the exact means; they are an artefact of rare events, and the question was settled by
the exact replication.  (7) **While the band-7 measurement of §3.4 was still running I typed provisional figures
for it into this report** (a ratio of 4.1, "two thirds"); the measurement gave 1.54 and one quarter.  From the band-4
number alone I had also concluded that the envelope's share there was below `10⁻⁵`; the band-7 measurement shows
it is about `5·10⁻⁵` at order 4.  Both were corrected before the hand-back; `NOTES.md` has the times.  No number in
this report is now without a log of mine or of the coordinator's behind it, except where it is marked [H] or
[from memory].

**Follow-ups I would ask for (not findings).**  (a) The loss between groups for Lys₁₂ at order 5 and for Lys₂₀ with
`r19_loss_between_groups.py` (it needs the memory of those runs, above my limit).  (b) Proposition AA.1′ of finding
M3 as a machine-checked statement, next to the theory division's `resolved_remainder_bound`.  (c) The two requests
that are already open and on which every number rests: an independent implementation of the stage-2 tables (P9-E2)
and a proof or a measurement protocol for `ε_g` (A19-E2).  (d) In the driver: an identity check of the kind of §3.1
at the sampled states (it costs nothing beyond the energies already evaluated and sees what the inequality cannot),
and the guards of finding m11.

**Files** (all in `experiments/science/ws_R19/`): `NOTES.md`; scripts `r19_item1_identity.py`,
`r19_item1_sampled.py`, `r19_heldsite_fuzz.py`, `r19_item3_logs.py`, `r19_dump_case.py`, `r19_groups_exact.py`,
`r19_loss_between_groups.py`, `r19_allowance_first_order.py`, `r19_audit_tests.py`, `snap_caches.sh`; cited logs
`r19_item1_identity_{K5_m4_w2,K5_m4_w3,K5_m5_w3,LKSEc5_m4_w2}.log`, `r19_item1_sampled_K12_m4_{w4,w7}.log`,
`r19_heldsite_fuzz_v3.log`, `r19_item3_logs.log`, `r19_groups_exact_{K5_m4_w2_enum,K12_m4_w4_v2,K12_m4_w7}.log`,
`r19_loss_between_groups_{K5_m4_w2_enum,K5_m4_w3_enum,K12_m4_w4,K12_m4_w7}_v3.log`,
`r19_allowance_first_order_K12_m4_w4.log`, `r19_audit_tests_v3.log`,
`r19_dump_case_*.log`; superseded complete logs kept beside them (`r19_heldsite_fuzz.log`, `…_v2.log`,
`r19_audit_tests.log`, `…_v2.log`, `r19_groups_exact_K12_m4_w4.log` — the run above the memory limit);
`r19_groups_exact_K5_m4_w2_enum_restrict.log` (the state-by-state branch on the small case); `*.err` (standard
error of each run; the three of the fuzz test hold the overflow warnings of `slack_recovery.py` provoked on purpose
in Part D); `*.time` (start and end of the long runs).
`not_cited/`: `r19_audit_tests_try1.log` (stopped by an OverflowError of mine); `r19_heldsite_fuzz_debug1.log` (a
40-instance debugging run); `r19_loss_between_groups_K5_m4_w2_enum_v1.log` (the first estimator, which failed its
validation); `r19_loss_between_groups_{K5_m4_w2_enum_v2,K5_m4_w3_enum,K12_m4_w4}.log` (complete runs of the second
estimator with an error bar that ignored the correlation of the two ends; same central values as the `_v3` logs).
`old_logs_90abf0e/` (the thirteen old logs, by `git show`); `case_*.pkl` (the tables of four cases written by
`r19_dump_case.py`, 55 MB in all, for re-use); `snap_*.txt` (snapshots of the cache directories and committed logs).

## Coordinator's note (2026-11-26, after the hand-back; the report above is the referee's, unchanged)

*What I did with this report.*  Read in full.  **Checked:** (1) finding M1 — the referee's measurement for Lys₁₂ at
order 4, band 4 repeated with another sampling seed (a copy of `r19_loss_between_groups.py` with the seed changed,
`10⁶` samples, 33 s): loss `4.312·10⁻⁴ ± 5.6·10⁻⁷`, ratio to `D²/4` 2.084 ± 0.003 (the referee: `4.314·10⁻⁴`, 2.085);
the four enumerated rows of its table against my own committed logs (`first_order_recovery_*_enum.log`, the line
"with the routed items put back exactly"): they agree — the numbers that contradict "about `D²/4`" were in my logs
when I wrote it; (2) `r19_audit_tests.py` re-run (`python3 -I -B`, 8 s): output identical to `r19_audit_tests_v3.log`
apart from timings; (3) the quoted lines of my texts (addenda, SCI-MSG-0028, SCI-RES-0024, the audit) located and
compared with the findings.  **Not checked by me:** the fuzz of the held-site passes, the identity runs and the
exact group statistics were not re-run (their logs read); the referee's code was not reviewed line by line.

*Verdict.*  I accept every finding, major and minor.  There is nothing in the report I would dispute; one
reference is corrected in what I publish: the sentence of SCI-MSG-0028 on the loss between groups is in its §6 (b),
and the delocalisation sentence of SCI-RES-0024 is in its §3 (l. 83).

*What was done.*  Linked correction: SCI-MSG-0030.  `ASSUMPTION_AUDIT.md`: every change marked "[R19 …]" and listed in
its §6; Proposition AA.1′ added in the referee's formulation.  Addendum A17: marks at items 73, 78, 81 and a new
part (21), items 82–83.  `OPEN_PROBLEMS.md` D10, D15 and the status table: the same correction.  **Not done, on
purpose:** finding m11 (the 60th iterate; no test of finiteness or order in `slack_recovery.bounds`) and m15 (a
comment) are recorded in item 83 (e) and not changed in the code, because the fourteen committed logs must be those
of the committed code; they go in with the next re-run.  The referee's follow-ups (a)–(d) of its §6 are open:
the loss for Lys₁₂ at order 5 and Lys₂₀; AA.1′ machine-checked; requests P9-E2 and A19-E2; an identity check in the
driver.

*Not in the repository:* `case_*.pkl` (55 MB, written by `r19_dump_case.py`; regenerable), `old_logs_90abf0e/`
(copies of our own logs at that commit: `git show 90abf0e:<path>`), `not_cited/` and the `.err`, `.time` and
`snap_*` side files of the referee's directory.
