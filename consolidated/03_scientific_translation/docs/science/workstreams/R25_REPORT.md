# Workstream R25 — second look at two places of the Complexity division's hardness note: Theorem 1c in the regime `|x| ≥ |σ|`, and Lemma A1

*An internal review by an AI session, briefed to attack; **not external peer review**.  Work done 21:02–22:35 UTC on
2026-11-26 (times read from the clock; running log in `experiments/science/ws_R25/NOTES.md`).  Object: the read-only
copy of `STRANDS_NN_HARDNESS.md` at the Complexity division's commit `89114ea` (720 lines, sha256 `3df75bc9…e115fc7`);
read in full: l.1–446 and l.647–721; skimmed l.447–646 only to see how the two places are used.  I had not seen the
note before.  Reviewed: **only** the proof of Theorem 1c for `|x| ≥ |σ|` (l.286–303, 317–366) and Lemma A1
(l.647–684), with the steps of Theorem 1 they use.  Four kinds of checking are kept apart: **review** (re-derived on
paper), **replication** (my own code, written from the statements), **re-run** (their code — none: it was not
available to me), **read only**.  Labels: [P] paper proof, [N] numerical evidence, [K] in print with the reading
level, [V] machine-checked (none here).*

## 0. Verdict in eight lines

1. **Theorem 1c, regime `|x| ≥ |σ|`: proved as stated.**  Every line of l.317–356 was re-derived; I found no gap.
   `B ≥ 2` is used three times, the hypothesis `|x| < |σ| + min(|σ|,γ)` once, each with the right sign and count.
2. **Replication:** no non-tiling structure below `E*_x + ε_x` among 321 675 760 413 connected structures of the
   1 385 instances of the 27 families `(m,B)` with `B ≥ 2`, `mB ≤ 15`, at 1 060 parameter points — 2 841 068 of them
   enumerated one by one from the definitions, the rest counted by a transfer matrix validated against that
   enumeration; a direct face-by-face energy test (8 models × 2 loop tables) on 957 901 structures agrees.
3. **`B ≥ 2` is necessary:** `a = (2), m = 2, B = 1` (template `GAG`, item `CC`, no packing) has four one-pair
   structures of energy `E*_x − (|x| − |σ|)`: equal to `E*_x` at `x = σ`, below it beyond.
4. **The bound on `|x|` is exact at `B = 2` and only there.**  For every `B ≥ 1` the conclusion holds on
   `|x| < min(B|σ|, |σ| + γ)` with gap `min(|σ|, |σ|+γ−|x|, B|σ|−|x|)`, and for `m ≥ 2` neither can be improved
   ([P] in §2.2; [N] on all 39 families enumerated); so Corollary 2 for coaxial models needs only `|x| < |σ| + γ`.
   Smallest failure beyond the stated range: `a = (4), m = B = 2`.
5. **Lemma A1: proved with one degenerate gap, closed here** — the statement admits empty clauses, for which the
   construction gives `|X| ≠ |W|`; for clauses of one to three literals both directions and both counts are right.
6. **Replication:** 182 033 formulas (all on 3 variables with ≤ 3 clauses, all on 4 variables with ≤ 2, random up to 7
   variables and 42 clauses): satisfiable ⇔ perfect matching, 0 disagreements either way, and the *number* of
   matchings equals `Σ_α Π_C t_C(α)(ℓ_C−1)!`; every control (one triple removed, …) produces disagreements.
7. Findings: critical **0**, major **0**, minor **7** (§2).  The strongest is positive (line 4), not an error.
8. Not checked: the rest of the note; their scripts and logs (unavailable); anything machine-checked; `mB ≥ 16`.
   Errors of mine on the way are in §4.2; one of them is a breach of the memory limit of the brief.

## 1. The two statements as I understand them, with the hypotheses the text leaves implicit

### 1.1 Theorem 1c, regime `|x| ≥ |σ|`

*Setting.*  Positive integers `a_1,…,a_n`, `m`, `B` with `Σ a_i = mB`; the system `I(a,m,B)` consists of the template
`G^B (A G^B)^{m−1}` and the items `C^{a_i}`; `M = mB − n`.  A structure is a set of `G–C` pairs, each base at most
once, connected and non-crossing for some circular order of the strands; its energy is the sum of `g` over the
faces plus `nΔG_assoc`.  A face is *flush* if its boundary is two chords, one template bond and one nick between
two items, with no unpaired base.  The loop-energy function satisfies (H1) every stack costs `σ < 0`; (C0) every
flush face costs `x ≤ 0` and every other exterior loop costs `0`; (C2) every bulge and interior loop costs at
least `γ ≥ 0`.

*Claim.*  If `B ≥ 2` and `|σ| ≤ |x| < |σ| + min(|σ|, γ)`, then a tiling structure has energy
`E*_x = σM + x(n−m) + nΔG_assoc` and every other connected unpseudoknotted structure at least
`E*_x + ε_x`, `ε_x = min(|σ|,γ) − (|x| − |σ|) > 0`.

*Hypotheses the text leaves implicit* (none of them is wrong; all are used):

| | implicit hypothesis | where it is used |
|---|---|---|
| i1 | `a_i ≥ 1` and `Σ a_i = mB` (the definition of the instance; Theorem 1c does not restate them).  `n < m` and items longer than a block are allowed; then no tiling exists and `E*_x` is not attained | l.354 "then all `mB` item bases are paired" |
| i2 | among `A, C, G` only `{C,G}` pairs, so every chord joins the template to an item and chords are nested; no hairpin, no multiloop (steps (a), (a′)) | the list of face types; `F_0`, `F_K` |
| i3 | Fact 1 (connected ⇒ at most one nick per face) [K in the note; **read only** by me, replicated on small instances] | l.321 `fl = n−1−z`; l.335–336 "no nick … or exactly one nick" |
| i4 | **which faces can be flush**: only inner faces, between two *different item strands*, on a template bond *inside a block*, with both item ends paired.  Never at a separator (the `A` is unpaired: the exterior loop helix–`A`–helix costs exactly 0), never at a template end (`F_0`, `F_K` have one chord), never with a dangling item base | (C0); l.320–321 |
| i5 | every other exterior loop costs exactly 0: no dangles, no mismatch-mediated coaxial stacking across the separator | eq. (2) has no exterior term |
| i6 | `x` and `σ` are constants, the same for every flush face and every stack; `γ` bounds *every* bulge and interior loop, in particular the one-base `A` bulge over a separator, which is the loop that decides the `γ`-branch | l.343, 348 |
| i7 | in this regime `γ > 0` is forced (`|x| ≥ |σ|` and `|x| < |σ| + min(|σ|,γ)`); at `γ = 0` the regime is empty | — |

### 1.2 Lemma A1

*Claim.*  From a CNF formula with clauses `C_1,…,C_m`, each a list of `ℓ_C ≤ 3` literal occurrences (*slots*),
`L = Σ ℓ_C`, the construction of l.657–667 gives disjoint sets `W, X, Y` with `|W| = |X| = |Y| = 2L ≤ 6m` and a set
`T ⊆ W × X × Y` with `|T| = 3L + Σ_C 2ℓ_C(ℓ_C−1) ≤ 21m`, and `T` contains a perfect matching (a subfamily covering
every element exactly once) iff the formula is satisfiable.

*Implicit.*  (j1) **every clause has at least one literal** — see finding G1; (j2) a slot is an *occurrence*: a
literal repeated in a clause, or `v` and `¬v` in one clause, give separate slots with their own tips (the proof
never needs the literals of a clause to be distinct); (j3) variables that do not occur have no gadget; (j4) "second
index mod `d_v`" means `d_v + 1 ↦ 1`, and `d_v = 1` is allowed (the true and the false triple then share `a` and
`b`); (j5) the triples are pairwise distinct, and every element lies in a triple — which Lemma A2 requires of its
input (true when j1 holds).

## 2. Findings

Severity: 0 critical, 0 major, 7 minor.  F = Theorem 1c, G = Lemma A1.

### 2.1 Theorem 1c, line by line (review)

| lines | step | verdict |
|---|---|---|
| 298–303 | tiling: `M` stacks, `n−m` flush faces, `m+1` other exterior loops; `Σι = M`, `Στ = m(B−1) = M+n−m` | correct (replicated: the signature of every tiling is `(st, fl) = (M, n−m)`, no bulge, 0 violations of 15 766) |
| 317–322 | `st + fl + L = M + n − m`; `fl = n − 1 − z` | correct.  Uses: each template `GG` bond on exactly one face; the `n−1` inter-item nicks lie on inner faces, one per face (i3) |
| 324–326 | eq. (2): `E − E_0 = |σ|L + P − d(m−1−z)` | correct; it is `(x−σ)(m−1−z) − σL + P` with `x − σ = −d`.  Pure algebra: valid for either sign of `d` |
| 328–334 | a face with `k_f` separators holds `k_f − 1` (inner) or `k_f` (`F_0`, `F_K`) wholly unpaired blocks, hence that many loose bonds | correct; **first and second use of `B ≥ 2`** (`(B−1) ≥ 1`).  More is true: `(k_f−1)(B−1)` resp. `k_f(B−1)` loose bonds — see F1 |
| 335–341 | inner face with a separator: bulge/interior (`r`) or a non-flush inter-item nick (`z`); `m − 1 ≤ L + r + z` | correct; different faces carry different bonds and nicks.  Replicated on every structure: 0 violations for `B ≥ 2`; with any one of the three terms dropped the inequality fails (controls, §3) |
| 343–351 | `E − E_0 ≥ (|σ|−d)L + (γ−d)r + P''`, and `≥ min(|σ|,γ) − d` if `L ≥ 1` or a bulge/interior loop exists | correct; **the only use of `|x| < |σ| + min(|σ|,γ)`**, as `d < |σ|` and `d < γ`; `d ≥ 0` is used in both branches of l.344–345 |
| 352–356 | `L = 0` and no bulge/interior ⇒ tiling | correct; **third use of `B ≥ 2`** (every `G` is an end of a `GG` bond); then i1, then step (d) |

So the count over separators is right as it stands.

### 2.2 The findings on Theorem 1c

**F1 (minor; l.331–334 and l.358–363) — the hypothesis is exact for `B = 2` only; the proof gives more.**
The sentence "the referee found the condition `|x| < |σ| + min(|σ|,γ)` to be exact on a grid of values" is true of
instance sets that contain `B = 2`.  For `B ≥ 3` the conclusion of the theorem holds on the larger range
`|x| < min(B|σ|, |σ| + γ)`: l.332 discards the factor `B − 1`.  Replicated: in the ten families with `B ≥ 3`, `m ≥ 2`
the conclusion holds at **every** grid point outside the stated hypothesis with `|x| < min(B|σ|, |σ|+γ)` (74 to 204
points per family, `run27` C6b); the first failure for `B = 3` is at `|x| = 3|σ|` (`a = (6), m = 2`).
*Consequence worth having:* for a fixed model, hardness (Corollary 2) needs only `|x| < |σ| + γ` — take instances
with `B > |x|/|σ|`, which multiplying all sizes by a constant achieves, as the note itself does after Theorem 1e.

*Replacement text* (statement; [P], proof below; [N] on 39 families):

> **Theorem 1c′.**  Let `g` satisfy (C0), (H1), (C2) and `|x| < min(B·|σ|, |σ| + γ)`.  Put
> `E*_x = σM + x(n − m) + nΔG_assoc` and `ε_x = min(|σ|, |σ| + γ − |x|, B·|σ| − |x|)`.  Then every connected
> unpseudoknotted structure of `I(a,m,B)` has energy `E*_x` if it is a tiling structure and at least `E*_x + ε_x`
> otherwise.  (For `B = 1` the hypothesis reads `|x| < |σ|`; for `B = 2` it is `|x| < |σ| + min(|σ|,γ)`; for `B ≥ 3`
> it is weaker.)  For every `m ≥ 2` neither the hypothesis nor `ε_x` can be improved: in the instance
> `a = (2B, B, …, B)` (`m − 1` items; no packing) the structure in which the long item covers blocks 1 and 2 with the
> separator bulged has energy `E*_x + |σ| + g_A − |x|`, `g_A ≥ γ` being the energy of the one-base `A` bulge, and the
> structure in which the long item is paired with block 2 only, block 1 being unpaired, has energy
> `E*_x + B|σ| − |x|`; and in `a = (B, …, B)`, `B ≥ 2`, the tiling with the pair at the 5′ end of the template removed
> has energy `E*_x + |σ|`.
> Consequently Corollary 2 holds for every model with `|x| < |σ| + γ` (use instances with `B > |x|/|σ|`).

*Proof* (changes to the present proof only).  Eq. (2) holds for every `x ≤ 0`.
(a) `B ≥ 2`, `d = |x| − |σ| ≥ 0`.  In "The separators" keep the blocks: let `h` be the number of wholly unpaired
blocks found there (`k_f − 1` for an inner face of `𝔉`, `k_f` for `F_0`, `F_K`).  They carry `h(B−1)` loose bonds, so
`L ≥ h(B−1)`, and `m − 1 = Σ k_f = h + #{inner faces of 𝔉} ≤ h + r + z`.  With `d ≥ 0`, (2) gives
`E − E_0 ≥ |σ|L + P − d(h + r) ≥ |σ|(L − h(B−1)) + h((B−1)|σ| − d) + r(γ − d) + P''`, four non-negative terms.
A structure that is not a tiling has a bulge or interior loop — then `r ≥ 1` or `P'' ≥ γ`, so `E − E_0 ≥ γ − d` — or
`L ≥ 1` (present last paragraph) — then `E − E_0 ≥ (B−1)|σ| − d` if `h ≥ 1` and `≥ |σ|` if `h = 0`.
(b) `B ≥ 2`, `|x| ≤ |σ|`.  In the identity of case 1 a bulge or interior loop contributes `≥ γ + |σ| − |x|`.  If there
is none and the structure is not a tiling, some item bond is not on a stack (step (d)) and some template `GG` bond is
loose (present last paragraph); both lie on exterior loops that are not flush, whose terms add up to at least
`(|σ| − |x|)·1 + |x|·1 = |σ|`.
(c) `B = 1`: case 1 as it stands; `ε_x = |σ| − |x|`.
(d) For `a = (2B, B, …, B)`: `n − m = −1`, `M = m(B−1) + 1`, `E_0 = σM − x`; the first structure has `m(B−1)` stacks
and one bulge, the second `(m−1)(B−1)` stacks and nothing else (the unpaired half of the long item and block 1 lie on
`F_0`).  For `a = (B, …, B)`: `M − 1` stacks, no flush face.  (All three signatures occur in the enumerations, e.g.
for `a = (6,3)`, `m = B = 3` and `a = (3,3,3)`.)  ∎

**F2 (minor; l.289–292) — the stated gap jumps at `|x| = |σ|`.**  `ε_x → 0` as `|x| ↑ |σ|`, but `ε_x = min(|σ|,γ)` at
`|x| = |σ|`.  Both lines are valid lower bounds; the first is not sharp for `B ≥ 2`, `γ > 0` (true gap
`min(|σ|, |σ| + γ − |x|)`, [P] (b) above, [N] C7).  It matters only where the gap is used as a number: the threshold
interval of Corollary 2 and the magnification in Corollary 4(ii).
*Replacement:* the single formula of Theorem 1c′, or after l.292: "(for `B ≥ 2` and `|x| < |σ|` the gap is in fact
`min(|σ|, |σ| + γ − |x|)`)".

**F3 (minor; l.286 and l.358) — say that `B ≥ 2` cannot be dropped, with the example.**  The text gives no reason
for the hypothesis.  It is necessary: see verdict line 3.  At `B = 1` the conclusion fails on **every** instance with
an item of length ≥ 2: there are no `GG` bonds, hence no stack and no flush face; a structure with one pair per item
has energy `nΔG_assoc`, and `E*_x − nΔG_assoc = (m − n)(|x| − |σ|) ≥ 0` with `m − n = M ≥ 1` ([P]; [N] `run27` C3:
failure at all 1 010 grid points of the regime for each `m = 2,…,12`).  These instances are all no-instances, so
nothing is lost for hardness.
*Replacement* (add to the sharpness paragraph): "`B ≥ 2` cannot be dropped: for `a = (2)`, `m = 2`, `B = 1` (template
`GAG`, item `CC`; no packing) the four structures with one pair have energy `nΔG_assoc = E*_x − (|x| − |σ|)`."

**F4 (minor; l.358–359) — wording.**  "For `x = σ`, `γ = 0` every arrangement … has energy `E*_x`" needs the bulge
over a separator to cost *exactly* 0; `γ = 0` is only a lower bound.  *Replacement:* "For `x = σ` and a one-base
bulge of energy 0 every arrangement …".

**F5 (minor, editorial; l.343).**  `P''` is introduced with no `P'` anywhere; and l.286 does not restate
`a_i ≥ 1`, `Σ a_i = mB`, which l.354 uses.  *Replacement:* "`P_r ≥ 0`" (or any unprimed name); "Let `a_i ≥ 1`,
`Σ a_i = mB`, and let `g` satisfy …".

What I tried in order to break the statement, without success: `n < m`; items longer than a block, up to the
single item of length `mB`; `m = 1`; `K = 1` (one chord); structures with every `G` paired but straddling; flush
faces next to dangling bases; the boundary `|x| = |σ|` with `γ` down to `10⁻⁶`; `|x|` within `10⁻⁶` of
`|σ| + min(|σ|,γ)`; `σ ≠ −1`; loop energies above `γ` depending on both loop sizes.

### 2.3 Lemma A1, step by step (review)

| lines | step | verdict |
|---|---|---|
| 657–661 | elements; `|W| = 2L`, `|X| = |Y| = L + m + (L−m) = 2L` | correct **iff every `ℓ_C ≥ 1`** (G1) |
| 663–669 | triples; `|T| = 2L + L + Σ 2ℓ_C(ℓ_C−1) ≤ 21m` | correct; per clause 3, 10, 21 triples for `ℓ_C = 1, 2, 3`; no two triples coincide |
| 671–676 | `b_{v,j}` lies only in the true and false triple of `(v,j)`, `a_{v,j}` only in the true triple of `(v,j)` and the false triple of `(v,j−1)`; propagation round the cycle | correct, also for `d_v = 1` |
| 677–679 | `c¹_C` is covered by a clause triple whose tip no variable triple covers ⇒ that literal is true | correct; the garbage triples play no role in this direction |
| 680–684 | after the variable triples every slot has exactly one free tip; one goes to the clause triple of a true slot, the other `ℓ_C − 1` to the `ℓ_C − 1` garbage pairs of the clause | correct; every element exactly once (replicated on 809 792 satisfying assignments) |

*What makes it linear.*  Tips exist per **occurrence**, so after the truth setting a clause owns exactly `ℓ_C` free
tips and its garbage can be collected by `ℓ_C − 1` pairs joined only to its own `2ℓ_C` tips.  In the textbook
gadget every variable has `2m` tips, one pair per clause whether or not it occurs there ([K], full text of §2.1.11
of a secondary source that follows Garey–Johnson "changed slightly": Pfaue, arXiv:2411.05796v1), so garbage must
be collected globally; from my memory, unverified, by `m(n−1)` pairs each joined to all `2mn` tips, i.e. `Θ(m²n²)`
triples; the search tool's summary of a source I did not open gives the same `Θ(m²n²)` [search snippet], and the
abstract of Kushagra, arXiv:2003.00336, as paraphrased by the fetch tool, speaks of a power-4 blow-up [abstract].
So the coordinator's "quadratic" is right relative to the size `mn`.  Garey–Johnson's book itself was not read by
me.

### 2.4 The findings on Lemma A1

**G1 (minor; l.653 with l.660–661) — empty clauses.**  "`m` clauses of at most three literals each" admits
`ℓ_C = 0`.  Then "`ℓ_C − 1` garbage pairs" is `−1`; read as none, the construction gives `|X| = |Y| = |W| +` (number of
empty clauses), and `c¹_C`, `c²_C` lie in no triple, which also breaks the hypothesis of Lemma A2 ("every element
lying in at least one triple").  Replicated: `[(x∨y), ()]` gives `|W| = 4`, `|X| = |Y| = 5` (`run30`).  The answer
"no perfect matching" is still right; the *statement* `|W| = |X| = |Y|` is not.  Irrelevant for Corollary 5.
*Replacement:* "with `m` clauses of one to three literals each (a formula with an empty clause is unsatisfiable;
map it to the instance of `(x) ∧ (¬x)`, which has six triples and no perfect matching)".

**G2 (minor; l.649–651) — a precedent to cite.**  A linear-size reduction from 3-SAT to 3DM is in print
(Kushagra 2020, arXiv:2003.00336: a linear-time reduction, with the ETH bound `2^{o(m)}`; [abstract, through the
fetch tool's summary]; I did not compare the construction with Lemma A1).  The note claims no novelty for A1, so
this is a citation, not a correction.
*Replacement* (add to the first paragraph of Appendix A): "A linear-size reduction of this kind was published by
Kushagra (arXiv:2003.00336); we have not compared the constructions."

Answers to the brief's question (iii), for statement / proof / their test:

| case | statement | proof | their test (`test_eth_chain.py`) | my replication |
|---|---|---|---|---|
| variable occurring once (`d_v = 1`) | covered | covered (the propagation is vacuous) | **not visible to me** (read only: "1500 random formulas", l.565) | 50 440 + 11 152 + 44 093 + 1 090 formulas |
| variable only positive / only negative | covered | covered | not visible | 55 467 / 55 467 (3 variables, exhaustive) |
| clauses with one or two literals | covered | covered | not visible | 20 180 / 58 660 (3 variables, exhaustive) |
| repeated literal in a clause; `v` and `¬v` in a clause | covered if "literal" means occurrence (j2) | covered | not visible | 89 096 / 58 660 (3 variables, exhaustive) |
| empty clause | admitted by the wording, **not** covered (G1) | not covered | not visible | one example |

## 3. My tests, with their controls (replication)

All code is mine, written from §1–§3 and Appendix A of the note; nothing of theirs was run.  Machine rules kept
except once (§4.2): `OMP_NUM_THREADS=1`, at most two processes, every script caps its own address space at 2 GB,
no run above ten minutes, `python3 -B`, peak memory in the last line.  Every log named below starts with a clock
line and **reached its last line**.  Runs 21–36 are the cited ones; runs 01–13 are an earlier pass with the same
numbers (kept, not overwritten; every signature file of the second pass is byte-identical to the first).

### 3.1 Item 1 — the enumerators (`nn_model.py`) and their validation

* **L0**: every partial `G–C` matching × every labelled circular order, pairwise chord-crossing test, union–find.
* **LA**: for one circular order, backtracking over all pairwise non-crossing pair sets with a generic crossing
  predicate; faces as orbits of the successor map on links; loop types from the definitions of §1; flush from §3;
  tiling **by the definition** of §2.
* **LB**: transfer matrix over nested chords, counting structures by signature `(st, fl, nb, L, z, r)`.

| check | size | violations | control (must fail) | control result |
|---|---|---|---|---|
| LA = L0, order by order (`run21`) | 29 labelled instances, 126 621 pair sets, 16 654 connected and unpseudoknotted | 0 | enumerator that never pairs the last base | differs on 29 of 29 |
| uniqueness of the order of a connected structure (`run21`) | 84 924 connected pair sets | 0 | the same without connectivity (`run29`) | 4 520 of 27 538 pair sets admit ≥ 2 orders |
| Fact 1 (`run22`, `run23`) | 19 603 658 non-crossing pair sets | 0 | "three or more nicks" (`run29`, `mB ≤ 7`) | 296 372 violations among 567 498 pair sets |
| no hairpin, no multiloop, `c` exterior loops, `|S|+1` faces, stacks are `GG/CC` (`run22`, `run23`) | 3 192 458 structures | 0 (an exception would have stopped the run) | none of its own (assertions) | — |
| tiling ⇔ every item bond on a stack (`run22`, `run23`) | 3 192 458 | 0 | "tiling ⇔ every base paired"; "tiling ⇔ no bulge/interior" (`run29`, `mB ≤ 7`) | 164; 46 243 violations among 126 571 structures |
| LB = LA, composition by composition (`run22`, `run23`) | 1 093 compositions (all with `mB ≤ 8`, and `(3,3)`) | 0 | DP whose flush test ignores the template side | differs on 1 065 of 1 093 |

*Agreement with the only output of their enumerators that I can see* (`run36`).  §6 of the note quotes two
per-instance counts of connected structures, without naming the instances: "up to 1 887 888" and "up to 762 294".
With all strands labelled my enumeration gives exactly 1 887 888 for `a = (2,2,3,3), m = 2, B = 5` and exactly
762 294 for `a = (2,4,4), m = 2, B = 5`.  This is agreement of two seven-digit numbers, not a comparison instance by
instance.

### 3.2 Item 1 — the proof's intermediate claims, on every structure

Families: every `(m,B)` with `mB ≤ 12`, and `(2,7), (7,2), (3,5), (5,3)`; in each, **every** composition of `mB`
(every multiset `a` in every circular order): 39 families, 1 656 instances, 67 141 ordered instances,
322 270 116 708 connected structures with equal items not distinguished (59 513 958 395 467 with all strands
labelled).  LA up to `mB ≤ 8` and `(3,3)`; LB beyond (`run24`–`run26`).

| claim (line of the note) | structures | violations | control | control result |
|---|---|---|---|---|
| `st + fl + L = m(B−1)` (l.321) | all | 0 | the same with a mis-defined flush face (template side ignored; `run35`, `mB ≤ 7`) | fails for 53 026 of 126 571 structures |
| `fl = n − 1 − z` (l.321) | all | 0 | the same (`run35`) | fails for 53 026 of 126 571 |
| `m − 1 ≤ L + r + z` for `B ≥ 2` (l.340) | 321 675 760 413 | 0 | the same without `r`; without `L`; without `z` | 302 271 336; 18 133 641 957; 1 379 325 464 violations |
| the same inequality for `B = 1` (excluded) | 594 356 295 | 594 352 200 | — | (this *is* a control: the inequality needs `B ≥ 2`) |
| tiling ⇒ `(st, fl, nb, L, z, r) = (M, n−m, 0, 0, m−1, 0)` (l.299) | 15 766 tilings | 0 | none of its own | — |
| `B ≥ 2`: tiling ⇔ `L = 0` and no bulge/interior (l.352) | 321 675 760 413 | 0 | "tiling ⇔ no bulge/interior" (`run29`) | 46 243 |

### 3.3 Item 1 — the theorem (`run27`, `t1c_analysis.py`; `σ = −1`, `X = |x|`)

In the extremal model (every bulge and interior loop exactly `γ`; any other admissible `g` only raises the energy of
structures that have such loops, and tilings have none) `E − E_0 = (M − st) − X(fl − (n−m)) + γ·nb`, so each family
is decided by the finitely many triples `(M − st, fl − (n−m), nb)` of its non-tiling structures, exactly, for all
`(X, γ)` at once.

| check | parameters | result | control | control result |
|---|---|---|---|---|
| C1 tilings at `E_0` | parameter-free | 0 violations of 15 766 | none of its own | — |
| **C2 Theorem 1c as stated**, `B ≥ 2` | 1 050 grid points `X, γ ∈ (1/20)ℤ` (also `γ = 5, 50`) and 10 boundary points (`X = 1 + min(1,γ) − 10⁻⁶`; `X = 1` with `γ = 10⁻⁶ … 50`) | **0 violations**; least value of gap `− ε_x` is 0, so `ε_x` is attained | C2c: gap claimed `1/20` larger | fails at 9 293 (family, point) pairs |
| C3 the same at `B = 1` | the 1 010 grid points of the regime | — | (is a control) | fails at 1 010 of 1 010 for each `m = 2,…,12` |
| C4 outside the hypothesis at `B = 2` | 435 grid points (`X, γ ∈ ¼ℤ ∩ [0,6]`) with `X ≥ 1 + min(1,γ)` | — | (is a control) | a non-tiling structure at or below `E_0` at 435 of 435, for each `m = 2,…,7` |
| C5 the note's three control models | `(σ,0)`; `|x| = |σ|+γ < 2|σ|`; `|x| = 2|σ| < |σ|+γ` | replicated: 1 079, 1 079, 280 of 1 385 instances violate | (are controls) | — |
| C6 exact range `X < min(B, 1+γ)` | exact vertex test on the triples, all 39 families | 0 violations; triples `(1,1,1)` and `(B,1,0)` present for every `m ≥ 2` | none of its own (C4 and those two triples show that any larger range fails) | — |
| C7 gap `min(1, 1+γ−X, B−X)` | `X, γ ∈ ¼ℤ ∩ [0,6]` | never undercut; attained at every grid point for every family with `m ≥ 2` | none of its own (attainment shows a larger gap fails) | — |

`t1c_direct.py` (`run28`), independent of that algebra: energies summed face by face in exact rationals over the
837 ordered instances with `mB ≤ 8`, eight models in the regime (`x = σ` with `γ = ½, 3, 10⁻³`; `|x| = 5/4, γ = ½`;
`|x| = 1.49, γ = ½`; `|x| = 7/4, γ = 2`; `|x| = 1.99, γ = 5`; `σ = −3, x = −4, γ = 2`) × two loop tables (extremal; a
seeded random table `γ + {0, ¼, …, 2}` by loop shape): **0 violations** on 957 901 structures with `B ≥ 2`, gap
attained in all eight extremal cases.  Controls: at `B = 1` the gap claim fails for 68 199 to 351 135 of 351 390
structures in every case; outside the hypothesis (extremal table) 220, 220, 1 730, 1 730 non-tiling structures lie at
or below `E_0`.

*Smallest counterexamples beyond the stated range* (C8/C9; each can be checked by hand):

| where | instance | structure | `E − E_0` |
|---|---|---|---|
| `B = 1` | `a = (2), m = 2` (`GAG` + `CC`; 5 bases, 2 strands; no packing) | one pair, e.g. `G3–C1` | `|σ| − |x|` |
| `B = 2`, `γ`-branch | `a = (4), m = 2` (`GGAGG` + `CCCC`; 9 bases, 2 strands; no packing) | all four pairs, `A` bulged | `|σ| + g_A − |x|` |
| | `a = (1,1,2), m = 2, B = 2` (a yes-instance), order `1,2,1` | `G1–C`, `G2–C₂C₁–G4` over the `A`, `G5–C` | `|σ| + g_A − |x|` |
| `B = 2`, `σ`-branch | `a = (4), m = 2` | `G4–C2, G5–C1` only (block 1 unpaired) | `2|σ| − |x|` |
| | `a = (2,2), m = 2, B = 2` (a yes-instance) | `G4`, `G5` paired with one base of each item | `2|σ| − |x|` |
| `B = 3` | none at `|x| = 2|σ|`; first at `|x| = 3|σ|`: `a = (6), m = 2` | last block only | `3|σ| − |x|` |

### 3.4 Item 2 — Lemma A1 (`a1_3dm.py`)

Construction coded from l.657–667; perfect matchings counted exactly by an exact-cover search memoised on the
covered set (validated against naive enumeration of all `q`-subsets of `T` on 112 small instances, 0
disagreements; a naive count that ignores the `W` coordinate differs on 14); satisfiability by brute force.
Checks: **S** sizes, distinct triples, `T ⊆ W×X×Y`, every element in a triple; **E** satisfiable ⇔ matching; **N**
number of matchings `= Σ_α Π_C t_C(α)(ℓ_C−1)!` (`t_C` = number of true slots); **F** the matching built by the recipe
of the proof is perfect, for every satisfying assignment; **B** every matching found (≤ 50 per formula) decodes to a
consistent satisfying assignment.

| family (log) | formulas (unsat.) | largest `q`, `|T|` | S | E: sat-no-match / unsat-match | N | F | B |
|---|---|---|---|---|---|---|---|
| all formulas, 3 variables, ≤ 3 clauses (`run31`) | 102 339 (2 862) | 18, 63 | 0 | 0 / 0 | 0 | 0 of 344 430 | 0 of 3 731 374 |
| all formulas, 4 variables, ≤ 2 clauses (`run32`) | 13 694 (36) | 12, 42 | 0 | 0 / 0 | 0 | 0 of 77 896 | 0 of 468 304 |
| 60 000 random, 4 variables, 3 clauses, seed 20261126 (`run33`) | 60 000 (653) | 18, 63 | 0 | 0 / 0 | 0 | 0 of 367 971 | 0 of 2 605 230 |
| 3 000 random, 2–7 variables, ≤ 21 clauses of 1–3 literals (`run34`) | 3 000 (639) | 114, 379 | 0 | 0 / 0 | 0 | 0 of 13 321 | 0 of 92 193 |
| 3 000 random 3-CNF, 3–7 variables, `3n…6n` clauses (`run34`) | 3 000 (713) | 252, 882 | 0 | 0 / 0 | 0 | 0 of 6 174 | 0 of 114 350 |
| 15 special formulas (`run30`) | 15 (4) | 48, 168 | 0 | 0 / 0 | 0 | — | — |

A clause is a non-empty multiset of at most three literals, so unit clauses, repeated literals and `v ∨ ¬v` are
all in the exhaustive families (counts in §2.4).

Controls — the brief asks that one triple removed from a gadget produce a disagreement.  Number of formulas on
which "satisfiable" and "has a perfect matching" then disagree:

| mutation of the instance | 3 var., ≤ 3 cl. | 4 var., ≤ 2 cl. | 4 var. sample | random (`run34`) | direction |
|---|---|---|---|---|---|
| first true triple removed | 22 172 | 1 512 | 7 313 | 542 | satisfiable, no matching |
| first false triple removed | 22 172 | 1 512 | 7 448 | 554 | satisfiable, no matching |
| first clause triple removed | 21 093 | 1 348 | 3 596 | 417 | satisfiable, no matching |
| first garbage triple with a `p` tip removed | 926 | 24 | 226 | 39 | satisfiable, no matching |
| first garbage triple with an `n` tip removed | 2 226 | 48 | 264 | 46 | satisfiable, no matching |
| a clause triple with the opposite tip added | 2 477 | 36 | 480 | 123 | unsatisfiable, matching |
| variable gadget unlinked (`a_{v,j}` for `a_{v,j+1}`) | 2 862 (all unsat.) | 36 | 653 | not run (§4.2) | unsatisfiable, matching |
| counting identity without `(ℓ_C−1)!` | 95 814 | 12 640 | 58 263 | 2 187; 2 287 | count differs |

The smallest disagreements are the expected ones: `(x)` for the true and the clause triple, `(¬x)` for the false
triple, `(x) ∧ (¬x ∨ y)` and `(¬x) ∧ (x ∨ ¬x)` for the garbage triples, `(x) ∧ (¬x)` for the last two.

## 4. What I did not check; my own errors; files

### 4.1 What I did not check

* Anything outside the two places: Theorems 1, 1d, 1e, 3, Corollaries 2, 4, 5, Lemma A2, and the case `|x| < |σ|`
  of Theorem 1c beyond re-deriving its ten lines and one by-product check (`run27` C2d: 0 violations).  Step (d) of
  Theorem 1 was re-derived and replicated (tiling ⇔ all item bonds stacked) but its Lean file was not opened.
* Their scripts and logs (not available): no **re-run** of anything; §6 of the note is **read only**.
* Fact 1 and the uniqueness of the ordering: cited [K] in the note (Dirks et al. 2007), not read by me; replicated
  on small instances only.
* No machine check.  Theorem 1c′ of §2.2 is my paper proof [P], numerically checked on 39 families [N], reviewed by
  nobody else.
* Beyond `mB = 8` (and `(3,3)`) the structures were counted by the transfer matrix, not visited one by one; its
  correctness there rests on its agreement with the generic enumerator on 1 093 smaller compositions.  Nothing with
  `mB ≥ 16`; nothing with `B ≥ 8`; 3- or 4-PARTITION-shaped instances only as far as they occur among all
  multisets with `mB ≤ 15`.
* Loop-energy functions other than the extremal one: one random table, `mB ≤ 8`; the general case by monotonicity.
* Lemma A1: nothing beyond 7 variables / 42 clauses; exhaustive only up to 3 variables × 3 clauses and 4 × 2.
  Garey–Johnson's book was not read; its theorem numbers (3.2, 4.3) stay unverified.
* Whether any published coaxial-stacking rule satisfies (C0): out of scope, not looked at.

### 4.2 My own errors

1. **A false observation, caught by the enumeration.**  My first notes said "`B ≥ 2` is redundant: for `B = 1`,
   `Σ a_i = m` forces all `a_i = 1`".  False — I confused `n ≤ m` with `n = m`.  The first enumeration showed 8 922
   non-tiling structures at `B = 1`; the hypothesis is necessary (verdict line 3).  Corrected in the notes before
   any report text was written.
2. **A breach of the memory limit.**  A trial of the random mode of `a1_3dm.py` grew to about 12 GB resident and was
   killed by the memory-cgroup OOM killer (`dmesg`: `anon-rss:12050272kB`).  Cause: the control "variable gadget
   unlinked" makes every slot an independent choice, and my memoised counter then has `2^L` states.  The kill was
   confined to my own cgroup; another division's job on the machine kept running.  Nothing is cited from that
   trial.  Since then every script caps its address space at 2 GB and the counter stops at 2·10⁶ states; that
   control runs only on the small families.  Because the scripts changed, all cited runs were repeated with the
   frozen scripts (same numbers, byte-identical outputs).
3. A second trial of the same mode hit its 300 s limit: my explicit enumeration of matchings backtracked
   exponentially on formulas with few models.  Fixed by pruning with the counter; no cited run affected.
4. Three control totals in the first draft of this report were added by hand and were wrong in the fourth to
   seventh digit; every sum in the report is now computed from the logs by a script (values in `NOTES.md`).
   Likewise a time written from a guess ("20 minutes") instead of the clock in one line of the notes; corrected.
5. Shell slips without effect on results: `tail -2 a b` at the end of a background command made the tool report
   "exit code 1" for two runs that had completed; one foreground `sleep 100`.
6. `run27` peaked at 1 449 MB — inside the limit, but only because the limit is 2 GB; the signature files could have
   been read as a stream.
7. One write outside the two permitted places: the text extracted with `pdftotext` from a downloaded PDF (the
   secondary source of §2.3) went to a temporary file in the session scratchpad; I removed it by name afterwards.
   (The fetch tool itself keeps the PDF in its own tool-results directory.)  Nothing existing was modified.

### 4.3 Files (all in `experiments/science/ws_R25/`)

* `NOTES.md` — the running log, with every step, both passes, the errors and the network use.
* Code (sha256 in `NOTES.md`): `nn_model.py` (model, enumerators L0/LA/LB), `t1c_levelA.py`, `t1c_dp.py`,
  `t1c_analysis.py`, `t1c_direct.py`, `t1c_controls_extra.py`, `t1c_controls_ident.py`, `t1c_labelled_counts.py`,
  `a1_3dm.py`.
* Cited logs: `run21_part1.log`, `run22_levelA_q8.log`, `run23_levelA_3x3.log`, `run24_dp_q9to12.log`,
  `run25_dp_2x7_7x2_3x5.log`, `run26_dp_5x3.log`, `run27_analysis.log`, `run28_direct_q8.log`,
  `run29_controls_extra.log`, `run35_controls_ident.log`, `run36_labelled_counts.log`, `run30_a1_special.log`,
  `run31_a1_exh_nv3_m3.log`,
  `run32_a1_exh_nv4_m2.log`, `run33_a1_sample_nv4_m3.log`, `run34_a1_random.log`.
* Data: `sig_levelA_q8_v2.json`, `sig_levelA_3x3_v2.json`, `sig_dp_q9to12_v2.json`, `sig_dp_q14_15a_v2.json`,
  `sig_dp_5x3_v2.json` (about 120 MB in all; regenerated by runs 22–26 in about 20 minutes).
* First pass, kept and not cited: `run01`–`run06`, `run10`–`run13` logs, `sig_levelA_q8.json`, `sig_levelA_3x3.json`.
  Scratch, not cited: `logs_tmp_*.txt`, `tmp_trial_*.json`.  Three first-pass data files, byte-identical duplicates
  of second-pass ones, were deleted by name (recorded in `NOTES.md`).
* To re-run, from that directory with `OMP_NUM_THREADS=1`: `python3 -B t1c_levelA.py part1`;
  `python3 -B t1c_levelA.py part2 8 OUT.json`; `python3 -B t1c_levelA.py part2f "3,3" OUT.json`;
  `python3 -B t1c_dp.py "2,7;7,2;3,5" OUT.json`; `python3 -B t1c_analysis.py sig_*_v2.json`;
  `python3 -B t1c_direct.py 8`; `python3 -B t1c_controls_extra.py 7`; `python3 -B t1c_controls_ident.py 7`;
  `python3 -B a1_3dm.py special`; `python3 -B a1_3dm.py exh 3 3`; `python3 -B a1_3dm.py exh 4 2`;
  `python3 -B a1_3dm.py exh 4 3 60000 20261126`; `python3 -B a1_3dm.py rand 20261126 3000`.

*Network:* two generic searches and five addresses, for the textbook statement only; listed with reading levels in
`NOTES.md` and in the hand-back.  Nothing of this project was put into a query.  **Tool actions declined: none**
(one address answered HTTP 403 and was not read; I did not look for another route to it).

*Not mine:* an untracked `NOTES.md` at the root of the repository (written 22:31 UTC; its content is about another
workstream's scripts) — seen in a read-only `git status`, not touched.

---

## Coordinator's note (appended 22:51 UTC, 26 Nov 2026)

*What the coordinator did with this report before publishing it as SCI-REV-0024.*

1. **Read in full** (the 411 lines above).
2. **Checked by hand** the smallest instances on which everything turns: `a = (2), m = 2, B = 1` (template `GAG`,
   item `CC`: four one-pair structures of energy `nΔG_assoc = E*_x − (|x| − |σ|)` — the theorem's conclusion fails
   for `|x| ≥ |σ|`, so `B ≥ 2` is needed); `a = (4), m = B = 2` (`GGAGG` + `CCCC`: all four pairs with the `A` bulged
   has `E − E*_x = |σ| + g_A − |x|`; block 2 alone has `2|σ| − |x|`); `a = (6), m = 2, B = 3` (last block alone:
   `3|σ| − |x|`).  With them the range of F1, `|x| < min(B|σ|, |σ| + γ)`, is what it must be.  I followed the algebra
   of the strengthened inequality of F1 (from the note's eq. (2) and `m − 1 ≤ h + r + z`:
   `E − E_0 ≥ |σ|(L − h(B−1)) + h((B−1)|σ| − d) + r(γ − d) + P″`) and found it right; I did not re-derive the case
   analysis (a)–(d) line by line.
3. **Re-ran two of its scripts** (`a1_3dm.py special`; `t1c_levelA.py part1`): outputs identical to its logs
   `run30` and `run21` apart from the clock, time and memory lines.  The large runs were not repeated.
4. **The one citation it proposes** (G2) checked at the level of the public arXiv record, by me: S. Kushagra,
   "Three-dimensional matching is NP-Hard", arXiv:2003.00336 (29 February 2020); its abstract: "The standard proof
   of NP-Hardness of 3DM provides a power-4 reduction of 3SAT to 3DM. In this note, we provide a linear-time
   reduction. Under the exponential time hypothesis, this reduction improves the runtime lower bound from"
   `2^{o(m^{1/4})}` "(under the standard reduction) to" `2^{o(m)}`.  The paper itself was not opened; the
   constructions were not compared.
5. **Compared with the Complexity division's own referee** (COMPLEXITY-REV-0003, which this workstream was
   deliberately not given) and with their note as revised after it (`1ba144d`; unchanged at `75266b2`).  The two
   referees agree wherever they overlap: Theorem 1c correct; Lemma A1 correct for clauses of one to three
   literals, wrong as worded for an empty clause (their finding 8a = G1 here — already applied in their note).
   Their referee tested 63 points `(x, γ)` on 46 instances with `B ≥ 2` and found the hypothesis "exact on my grid";
   that is F1 seen from the side of `B = 2`.  **New relative to their review:** F1 (the range for `B ≥ 3`, with a
   proof and the consequence for their Corollary 2), F2 (the gap for `|x| < |σ|`), the example of F3, the two
   wordings F4, F5, the citation G2, and the counting identity for matchings.
6. **Process, for the research owner.**  No tool action was declined.  One trial of the agent grew to about 12 GB
   and was killed by the memory limit of its own cgroup — a breach of the 2 GB rule of its brief; nothing is cited
   from it and every cited run was repeated with a cap.  One temporary file went to the scratch space and was
   removed by name.  One address refused the request and was not retried.  The directory `ws_R25/` is committed
   **without** its signature files (`sig_*.json`, `tmp_trial_*.json`: 119 MB, regenerated by its runs 22–26 in
   about twenty minutes); code, logs and notes are 356 kB.  The untracked `NOTES.md` it saw at the root of the
   repository belonged to workstream R26, which moved it after a message from the coordinator.
7. The verdict is accepted.  This is an internal review by an AI agent, checked by an AI coordinator — not
   external peer review.  Theorem 1c′ of §2.2 is the agent's paper proof and has had no second reader.
