# Hardness of multi-stranded folding in the nearest-neighbour model

Working paper of the complexity division.  Status of every statement is given by its label; the
register is `THEOREMS.md`.  First version 2026-11-26.

**Question addressed** (`OPEN_PROBLEMS.md` A1; Ducloz–Shalaby–Woods, DNA 31, "Future work" 1):
"Is MFE NP-hard for […] NN O(n)-strands unpseudoknotted? If so, can the reduction map be leveraged to
show hardness results for PF and #SSEL in the NN model?"  The known hardness results for unboundedly
many strands (Condon–Hajiaghayi–Thachuk 2021; Ducloz–Shalaby–Woods 2025) are for the base-pair-matching
model, in which the energy is minus the number of base pairs and disconnected structures are allowed.

**Answer in one paragraph.**  Yes, for every nearest-neighbour loop-energy function in which exterior
loops cost nothing, the `GG/CC` stack is favourable and bulges, interior loops and multiloops are not
favourable — the sign pattern of every physical parameter set, and the model of the cited papers
when its exterior loops have `ΔG = 0`.  The reduction is from bin packing with exact fill
(3-PARTITION / 4-PARTITION) and is short; what makes it work in the nearest-neighbour model and not in
the base-pair-matching model is that a stack needs two *covalently adjacent* bases on each side, so a
short strand that is split over two binding sites loses a stack.  The instances have one long strand
and many homopolymer strands; all structures are connected, unpseudoknotted and without rotational
symmetry, so the association and symmetry terms of the model play no role.  Counting structures at
the minimum is #P-hard by the same reduction, and so is the partition function when the temperature
(or the magnification) is part of the input.

The mathematics is elementary.  Its novelty, if any, is that the question was posed as open in 2025
and that we found no proof in print (`PRIOR_ART.md` §A; the searches are listed there).  It is **not**
a statement about any fixed published parameter table with dangles or coaxial stacking (§6).

---

## 1. The model

**Strands and structures.**  A *strand* is a non-empty word over `{A,C,G,T}`, written 5′→3′.  A
*system* is a finite sequence `(s_1,…,s_c)` of strands; the *bases* are the pairs `(t,i)`, `1 ≤ t ≤ c`,
`1 ≤ i ≤ |s_t|`, and `N = Σ|s_t|`.  Two bases are *complementary* if their letters are `{A,T}` or
`{C,G}`.  A *secondary structure* is a set `S` of unordered pairs of complementary bases in which
every base occurs at most once.  Two bases `(t,i)`, `(t,i+1)` are joined by a *covalent bond*.  `S` is
*connected* if the graph on the bases with the covalent bonds and the pairs of `S` as edges is connected.

**Polymer graph.**  For a cyclic ordering `π` of `{1,…,c}` place the bases on a circle, strand after
strand in the order `π`, each strand 5′→3′.  Two cyclically consecutive bases are joined by a *link*:
a covalent bond, or a *nick* if they belong to different strands (or are the last and the first base
of the same strand when `c = 1`).  There are exactly `c` nicks.  `S` is *unpseudoknotted* if for some
`π` the chords representing its pairs are pairwise non-crossing.  For a connected unpseudoknotted `S`
this `π` is unique (Dirks et al. 2007, Theorem 2.1 — cited, [K]; our enumeration re-checks it on every
instance it runs, `experiments/complexity/strands/test_partition_reduction.py`).

**Loops.**  Fix `π` with `S` non-crossing.  The chords cut the disc into `|S| + 1` *faces*.  The
boundary of a face consists of chords and links.  A face is

* an *exterior loop* if its boundary contains exactly one nick;
* if its boundary contains no nick and `k` chords: a *hairpin* (`k = 1`); for `k = 2` a *stack* (no
  unpaired base on the boundary), a *bulge* (unpaired bases on one side only) or an *interior loop*;
  a *multiloop* (`k ≥ 3`).

**Fact 1** (Dirks et al. 2007; [K], and re-checked exhaustively by the enumerator's `check=True`
mode against a union–find computation).  `S` is connected iff no face has two or more nicks; then
exactly `c` faces are exterior loops.

**Energy.**  A *loop-energy function* `g` assigns a real number to every loop (it may depend on the
type of the loop, the letters on its boundary and the lengths of its unpaired segments).  For a
connected unpseudoknotted `S`,

```
ΔG_g(S) = Σ_{faces f of S} g(f) + (c − 1)·ΔG_assoc + k_B T · ln R(S),
```

where `R(S) ≥ 1` is the number of rotations of the polymer graph that map every strand to a strand
with the same sequence and `S` to itself (the maximum degree of rotational symmetry; Shalaby–Woods
2026, Def. 11).  The *MFE* of a system is the minimum of `ΔG_g` over connected unpseudoknotted
structures; `#SSEL(k)` is the number of them with `ΔG_g = k`, where structures that differ by a
permutation of strands with equal sequences are identified (the "physical ensemble"); the *partition
function* is `Σ_S e^{−ΔG_g(S)/k_B T}` over the same set.  This is Definition 11 of Ducloz–Shalaby–Woods
and Definition 7 of Shalaby–Woods; in the latter the exterior loop has `ΔG = 0` (their §6: "∆G = 0 for
the energy contribution of an exterior loop").

**Hypotheses on `g`.**

* **(H0)** `g(f) = 0` for every exterior loop.
* **(H1)** There is `σ < 0` such that `g(f) = σ` for every stack whose two pairs are `G–C` pairs with
  the two `G` on one strand and the two `C` on another (the stack `5′-GG-3′ / 3′-CC-5′`).
* **(H2)** `g(f) ≥ 0` for every bulge, interior loop and multiloop.

No hypothesis on hairpins, on other stacks, on `ΔG_assoc` or on the temperature.  The stack-only
model (`g = −1` on stacks, `0` elsewhere; the multi-strand version of the BPS model with stacks defined
as loops) satisfies them; so does every `j`-fold magnification of a model that satisfies them.

---

## 2. The reduction

**EXACT BIN PACKING.**  Input: positive integers `a_1,…,a_n`, `m`, `B` in unary with `Σ a_i = m·B`.
Question: is there a map `β : {1,…,n} → {1,…,m}` with `Σ_{β(i)=t} a_i = B` for every `t`?  It contains
3-PARTITION (`n = 3m`, `B/4 < a_i < B/2`) and 4-PARTITION (`n = 4m`, `B/5 < a_i < B/3`), which are
NP-complete in the strong sense (Garey–Johnson 1979, Theorems 4.3, 4.4; [K]).

**The system `I(a, m, B)`.**

```
template   τ   =  G^B A G^B A … A G^B          (m blocks G^B separated by single A's;  mB + m − 1 bases)
items      κ_i =  C^{a_i}   for i = 1,…,n
```

`c = n + 1` strands, `N = 2mB + m − 1` bases, constructed in time polynomial in the unary input.
Put `M = Σ_i (a_i − 1) = mB − n`.

**Theorem 1 [P].**  Let `g` satisfy (H0)–(H2) and let `a_i ≥ 1`.  For `I = I(a,m,B)`:

1. if the bin-packing instance has a solution, then `MFE(I) = σ·M + n·ΔG_assoc`;
2. otherwise `MFE(I) ≥ σ·(M − 1) + n·ΔG_assoc`.

Moreover a connected unpseudoknotted structure of `I` has energy `σ·M + n·ΔG_assoc` if and only if it
is a *tiling structure*: every item is paired, base by base and antiparallel, with a run of
consecutive `G`'s inside one block, and these runs partition the `G`'s of the template.

*Proof.*  Let `S` be a connected unpseudoknotted structure of `I` and `π` its ordering.

(a) *Pairs.*  `A` has no complementary letter in the system, the template contains no `C` and the
items contain no `G`.  So every pair of `S` joins a `G` of the template and a `C` of an item; no
strand pairs with itself, hence there is no hairpin.

(b) *Symmetry.*  The template is the only strand with its sequence, so every rotation counted by
`R(S)` fixes it and is the identity: `R(S) = 1`.  Hence `ΔG_g(S) = Σ_f g(f) + n·ΔG_assoc`.

(c) *Counting stacks.*  Let `st(S)` be the number of stack faces.  The boundary of a stack consists
of two chords and two links, both covalent bonds.  Going round the boundary, a link joins two bases
of one strand and a chord joins the template with an item (by (a)); so one of the two links is a bond
between two adjacent template bases, both paired and therefore both `G`, and the other is a bond
`(κ_i, j)–(κ_i, j+1)` of an item.  Every stack is therefore of the kind in (H1) and contributes `σ`.
A link lies on the boundary of exactly one face.  Hence `st(S)` is at most the number of item bonds,
`st(S) ≤ M`, and by (H0), (H2)

```
Σ_f g(f)  ≥  σ·st(S)  ≥  σ·M .                                              (1)
```

(d) *Equality.*  Suppose `st(S) = M`.  Then every bond of every item lies on a stack.  Fix an item
`κ_i` with `a_i ≥ 2`; for each `j < a_i` the bases `(κ_i,j)`, `(κ_i,j+1)` are paired with two
*adjacent* template bases.  The partners `p_1,…,p_{a_i}` of the bases of `κ_i` are thus distinct
template positions with `|p_{j+1} − p_j| = 1`, so they form a run of `a_i` consecutive positions, all
`G`; a run of consecutive `G`'s contains no `A`, so it lies in one block.  (The two chords of a stack
are nested, so the run is traversed 3′→5′: the pairing is antiparallel.)  An item with `a_i = 1` is
paired because `S` is connected, and its partner is a run of length one.  All `Σ a_i = mB` item bases
are paired with distinct template `G`'s, of which there are `mB`: the runs partition the `G`'s, and
each block, being a union of runs, is exactly filled.  So `S` is a tiling structure and
`β(i) =` "block of the run of `κ_i`" solves the bin-packing instance.  This proves 2: without a
solution `st(S) ≤ M − 1` for every `S`, and (1) with `σ < 0` gives the bound.  It also proves the
"only if" of the last statement, because energy `σM + nΔG_assoc` forces equality in (1).

(e) *The tiling structure of a solution.*  Let `β` be a solution; order the items of each block
arbitrarily and let `S*` pair them accordingly, antiparallel.  In the circular order "template, then
the items in the reverse order of their runs along the template" the chords are nested or disjoint,
so `S*` is unpseudoknotted.  Its faces are: `a_i − 1` stacks for every item; one face between two
consecutive items of the same block (two chords, one template bond, one nick); one face between the
last item of a block and the first of the next (two chords, the unpaired `A` with its two bonds, one
nick); the face inside the innermost chord at the 3′ end of the template, whose boundary contains the
nick between the template and the first item; and the outer face, whose boundary contains the nick
between the last item and the 5′ end of the template.  That is `M` stacks and `n + 1 = c` faces with
exactly one nick each, so `S*` is connected (Fact 1) and, by (H0), (H1),
`ΔG_g(S*) = σM + nΔG_assoc`.  With (1) this proves 1 and the "if" of the last statement.  ∎

**Corollary 2 [P]** (NP-hardness; answers the multi-strand half of A1).  For every loop-energy
function `g` satisfying (H0)–(H2) and every value of `ΔG_assoc` and `T`, the problem "given a system and
a number `k`, is `MFE ≤ k`?" for connected unpseudoknotted structures in the nearest-neighbour model
with rotational symmetry is NP-hard in the strong sense, already for systems consisting of one strand
over `{G,A}` and homopolymer strands `C^a`, `a ≥ 2`.  If `g` is polynomial-time computable with
rational values, the problem is in NP, hence NP-complete.

*Proof.*  Theorem 1 with `k = σM + nΔG_assoc`, from 3-PARTITION (all `a_i ≥ 2` after multiplying all
numbers by 2).  Membership in NP: guess `π` and `S`; non-crossing, the face decomposition, `R(S)` and
the energy are computable in polynomial time.  ∎

**Remarks.**
1. The energy model may be *fixed*: the hardness is not an artefact of making `g` part of the input.
2. The same proof gives NP-hardness of maximising the number of stacks over unpseudoknotted
   structures of many strands when disconnected structures are allowed (the multi-strand BPS model
   with stacks defined as nick-free loops), for items with `a_i ≥ 2`: steps (a), (c), (d), (e) do not
   use connectedness except for items of length one.
3. If a "stack" across a nick were also rewarded (coaxial stacking with the same energy as a stack),
   the reduction would fail: every arrangement of the items along the template would be optimal.  The
   theorem is about the model in which a face with a nick is an exterior loop.
4. In the base-pair-matching model the instances `I(a,m,B)` are trivial (all `mB` pairs can always be
   formed); this is why the reduction of Condon–Hajiaghayi–Thachuk had to be elaborate, and why it
   does not answer the question for stacking energies.

---

## 3. Counting: #SSEL and the partition function

Let `L(a,m,B)` be the number of partitions of the index set `{1,…,n}` into `m` classes each of total
size `B` (for 4-PARTITION instances this is the function shown #P-complete in Ducloz–Shalaby–Woods,
Lemma 31; [K]).  For a size `s` let `μ_s = #{i : a_i = s}`.

**Theorem 3 [P].**  Let `g` satisfy (H0)–(H2), `a_i ≥ 1`, `I = I(a,m,B)` and `E* = σM + nΔG_assoc`.

1. With all strands regarded as distinguishable, the number of connected unpseudoknotted structures
   of `I` with energy `E*` is `Til(a,m,B)`, the number of ways to arrange the labelled items into `m`
   ordered rows (row `t` = block `t` of the template), each row an ordered sequence of items of total
   length `B`:  `Til = Σ_β Π_t |β^{-1}(t)|!` over the solutions `β` of the bin-packing instance.  For
   3-PARTITION instances `Til = L·m!·6^m`, for 4-PARTITION instances `Til = L·m!·24^m`.
2. In the physical ensemble, `#SSEL(E*) = Til(a,m,B) / Π_s μ_s!`.

*Proof.*  By Theorem 1 the structures of energy `E*` are the tiling structures, and a tiling structure
is determined by, and determines, the sequence of items along each block: 1.  The group
`Π_s Sym(μ_s)` of permutations of equal items acts on the tiling structures, and freely: a permutation
that maps a tiling structure to itself maps every item to an item paired with the same run of the
template, i.e. to itself.  So every orbit has `Π_s μ_s!` elements, and the orbits are the structures of
the physical ensemble: 2.  For 3- and 4-PARTITION instances every class of a valid partition has
exactly 3, resp. 4, elements; the `m` classes can be assigned to the blocks in `m!` ways and each
ordered in `3!`, resp. `4!`, ways.  ∎

**Corollary 4 [P]** (#P-hardness; answers the second sentence of A1 for the multi-strand case).
For `g` satisfying (H0)–(H2): (i) `#SSEL` in the nearest-neighbour model is #P-hard, and #P-complete if
`g` is polynomial-time computable with rational values; (ii) for the stack-only model, the partition
function with the temperature as part of the input (equivalently, with the magnification as part of the
input) is #P-hard.

*Proof.*  (i) Given a 4-PARTITION instance, `L = #SSEL(E*)·Π_s μ_s! / (m!·24^m)`.  (ii) In the
stack-only model with `ΔG_assoc = 0` every structure of `I` has energy `−st(S) ∈ {0,…,−M}` and `R = 1`,
so `Z(T) = Σ_{k=0}^{M} N_k x^k` with `x = e^{1/k_BT}` and `N_k = #SSEL(−k)`; the values of `Z` at `M + 1`
temperatures determine all `N_k` by a Vandermonde system (this is Theorem 22 of Ducloz–Shalaby–Woods,
whose hypotheses — polynomially many candidate energy levels, a temperature-independent model — hold
here), and `N_M = #SSEL(E*)`.  ∎

What is **not** shown: #P-hardness of the partition function at a *fixed* temperature (problem A3′).

---

## 4. Verification

* [X] `experiments/complexity/strands/test_partition_reduction.py`, `test_partition_reduction_big.py`
  enumerate **all** connected unpseudoknotted structures (over all circular orderings) of `I(a,m,B)` for
  the instances listed there (`m ≤ 3`, `B ≤ 5`, up to 513 120 structures per instance), with the
  stack-only model and with a model whose bulge/interior/multiloop energies are random non-negative
  integers.  In every case: the minimum equals `σM` exactly when a perfect packing exists and is
  `≥ σ(M−1)` otherwise; the number of minimum-energy labelled structures equals the number of labelled
  tilings computed by an independent brute force; every labelled connected structure occurs under
  exactly one circular ordering.  The log is `experiments/complexity/strands/big_run.log`.
* Independent adversarial review: see `THEOREMS.md` (COMPLEXITY-REV-0001 when available).
* Lean: not formalised yet.

## 5. Consequences and what remains

* With `OPEN_PROBLEMS.md` A6 (algorithms whose exponential part depends only on the number of strands):
  the instances have `c = n + 1` strands, so an algorithm with running time `2^{o(c)}·poly(N)` for MFE in
  any model satisfying (H0)–(H2) would solve 4-PARTITION with polynomially bounded numbers in time
  `2^{o(n)}·poly`.  Whether that contradicts the Exponential Time Hypothesis depends on a linear-size
  chain of reductions to 4-PARTITION, which we have **not** verified ([C] for now).
* The instances use `n + 1` different strand *species* in general.  For a bounded number of species the
  problem is expected to be polynomial (A6/C2); the template is essential.
* The single-strand pseudoknotted half of A1 is not addressed: the nearest-neighbour model of the
  cited papers has no energy rule for pseudoknots.

## 6. Limitations (read before citing)

1. (H0) is an assumption about the model: parameter sets with dangling-end or coaxial-stacking terms
   give exterior loops non-zero, context-dependent energies, and Theorem 1 does not cover them.  With
   coaxial stacking as strong as stacking the reduction fails (Remark 3).  We make no claim about any
   specific published parameter table.
2. (H2) excludes hypothetical parameter sets with favourable bulges, interior loops or multiloops.
3. The result is a worst-case statement about synthetic instances with one long strand and unboundedly
   many species; it says nothing about typical instances.
4. The proofs are paper proofs by this division; "reviewed" in `THEOREMS.md` means an internal
   adversarial review, which is not academic peer review.
