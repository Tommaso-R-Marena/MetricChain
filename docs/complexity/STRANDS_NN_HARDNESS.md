# Hardness of multi-stranded folding in the nearest-neighbour model

Working paper of the complexity division.  Status of every statement is given by its label; the
register is `THEOREMS.md`.  First version 2026-11-26; **revised 2026-11-26 after the internal adversarial
review `COMPLEXITY-REV-0001` and the science division's independent review `SCI-REV-0019`** (what changed:
§9).  The two reviews did not know of each other and agree on the main points.

**Question addressed** (`OPEN_PROBLEMS.md` A1; Ducloz–Shalaby–Woods, DNA 31, "Future work" 1; cited as
[DSW]): "Is MFE NP-hard for […] NN O(n)-strands unpseudoknotted? If so, can the reduction map be
leveraged to show hardness results for PF and #SSEL in the NN model?"  The known hardness results for
unboundedly many strands (Condon–Hajiaghayi–Thachuk 2021, cited as [CHT]; [DSW] 2025) are for base-pair
models, in which the energy is minus the number of base pairs (in [CHT] plus an association term per strand
joined, with several complexes allowed).

## 0. Summary, attribution, status

**Answer.**  Yes, in the formal nearest-neighbour model of the papers that ask the question — a loop
containing a nick is an exterior loop, and exterior loops have energy zero — for every loop-energy
function in which the `GG/CC` stack is favourable and a bulge or interior loop is never as favourable as
the stacks it displaces (hypothesis (H2′) below; it holds in particular if bulges and interior loops are
not favourable at all).  The reduction is from bin packing with exact fill (3-PARTITION / 4-PARTITION).
The instances have one long strand and many homopolymer strands; all structures are connected,
unpseudoknotted and without rotational symmetry, so the association and symmetry terms of the model
play no role.

1. **Theorem 1, Corollary 2** [P]: strong NP-hardness of the decision version of MFE.
2. **Theorems 1c, 1d** [P]: the same instances work if a nicked "flush" stack between two helices that are
   adjacent on the template is rewarded with an energy `x` (coaxial stacking), provided
   `|x| < |σ| + min(|σ|, γ)`, where `σ` is the stack energy and `γ` the least bulge/interior-loop penalty
   (with `x = σ` and free bulges the reduction fails); and if unpaired bases next to a helix end in an
   exterior loop are rewarded (dangles), provided the rewards of a `G` and a `C` together are smaller than
   `|σ|` (the science division's statement).  **Theorem 1e** [P]: both together, with `σ ≤ x ≤ 0`.
3. **Theorem 3, Corollary 4** [P]: the number of minimum-energy structures is the number of tilings;
   `#SSEL` is #P-hard; the partition function is #P-hard when the magnification (or the temperature, for a
   temperature-independent energy function) is part of the input, by a one-call reduction.
4. **Corollary 5** [P, under ETH]: no `2^{o(c)}·poly(N)` algorithm in the number `c` of strands; the chain
   of reductions is written out with linear size in Appendix A.

What is **not** shown: #P-hardness of the partition function at a fixed temperature for a fixed model
(problem A3′); anything about dangle rules other than the abstract one of Theorems 1d and 1e, or about any
published parameter table as implemented (§8).

**Whose gadget this is.**  The template `G^B A G^B A … A G^B` with runs `C^{a_i}` is the gadget of Lyngsø's
reduction from BIN PACKING to pseudoknotted single-strand folding in the base-pair-stacking model (ICALP
2004; we know it through [DSW] Theorem 32 / Appendix B.3, which "proceed[s] exactly as Lyngsø" with the
strand `C^{w(a_1)} A C^{w(a_2)} A ⋯ A C^{w(a_k)} AAA G^B A G^B ⋯ A G^B`; Lyngsø's paper itself was not read by
us).  What we add is the observation that if the `C`-runs are *separate strands* the pseudoknots are not
needed, the argument goes through for every nearest-neighbour energy function satisfying (H0)–(H2′), and
the connectivity, association and symmetry terms of the multi-strand model are harmless.  The closest
multi-strand precedent we know is Boehmer–Berkemer–Will–Ponty (WABI 2024, Theorem 19): NP-completeness of
multi-strand MFE for unary triplet-repeat strands `(CAG)^{s_i}`, by a reduction from a strongly NP-hard
number problem, in an energy model with a reward per base pair, a multiloop penalty and a strand
association term, with several complexes; it does not concern stacking or loop energies.  The mathematics
here is elementary.  The result is, as far as our searches and those of the referee go
(`PRIOR_ART.md` §A), **apparently unpublished**; a failure to find it is not proof of novelty, and one
relevant source (a 2026 PhD thesis cited as "to appear" in Shalaby–Woods 2026) could not be inspected.

---

## 1. The model

**Strands and structures.**  A *strand* is a non-empty word over `{A,C,G,T}`, written 5′→3′.  A
*system* is a finite sequence `(s_1,…,s_c)` of strands; the *bases* are the pairs `(t,i)`, `1 ≤ t ≤ c`,
`1 ≤ i ≤ |s_t|`, and `N = Σ|s_t|`.  Two bases are *complementary* if their letters are `{A,T}` or
`{C,G}` (Watson–Crick pairs; the instances below contain only the letters `A`, `C`, `G`, and all that is
used of the pairing rule is that among these the only complementary pair is `{C,G}` — allowing `G·T` wobble
pairs changes nothing).  A *secondary structure* is a set `S` of unordered pairs of
complementary bases in which every base occurs at most once.  Two bases `(t,i)`, `(t,i+1)` are joined by
a *covalent bond*.  `S` is *connected* if the graph on the bases with the covalent bonds and the pairs of
`S` as edges is connected (one complex containing all strands).

**Polymer graph.**  For a cyclic ordering `π` of `{1,…,c}` place the bases on a circle, strand after
strand in the order `π`, each strand 5′→3′.  Two cyclically consecutive bases are joined by a *link*:
a covalent bond, or a *nick* if they belong to different strands (or are the last and the first base
of the same strand when `c = 1`).  There are exactly `c` nicks.  `S` is *unpseudoknotted* if for some
`π` the chords representing its pairs are pairwise non-crossing.  For a connected unpseudoknotted `S`
this `π` is unique (Dirks et al. 2007, Theorem 2.1 — cited, [K]; re-checked on every instance by our
enumerations and by the referee's).

**Loops.**  Fix `π` with `S` non-crossing.  The chords cut the disc into `|S| + 1` *faces*.  The
boundary of a face consists of chords and links.  A face is

* an *exterior loop* if its boundary contains exactly one nick;
* if its boundary contains no nick and `k` chords: a *hairpin* (`k = 1`); for `k = 2` a *stack* (no
  unpaired base on the boundary), a *bulge* (unpaired bases on one side only) or an *interior loop*;
  a *multiloop* (`k ≥ 3`).

**Fact 1** (Dirks et al. 2007, [K]; checked against a union–find computation on every structure of the
36 instances of `test_generalised_hypotheses.py`, and by the referee on 563.6 million pair sets).  `S` is
connected iff no face has two or more nicks; then exactly `c` faces are exterior loops.

**Energy.**  A *loop-energy function* `g` assigns a real number to every loop (it may depend on the
type of the loop, the letters on its boundary and the lengths of its unpaired segments).  For a
connected unpseudoknotted `S`,

```
ΔG_g(S) = Σ_{faces f of S} g(f) + (c − 1)·ΔG_assoc + k_B T · ln R(S),
```

where `R(S) ≥ 1` is the number of rotations of the polymer graph that map every strand to a strand
with the same sequence and `S` to itself (Shalaby–Woods 2026, Def. 11).  The *MFE* of a system is the
minimum of `ΔG_g` over connected unpseudoknotted structures; `#SSEL(k)` is the number of them with
`ΔG_g = k`, where structures that differ by a permutation of strands with equal sequences are identified
(the "physical ensemble"); the *partition function* is `Σ_S e^{−ΔG_g(S)/k_B T}` over the same set.  This is
Definition 11 of [DSW] and Definition 7 of Shalaby–Woods.  That a loop with a nick is an exterior loop of
energy zero is part of that model: "Exterior loops do not contribute to the free energy because by
definition [8], ∆G_exterior = 0" ([DSW], full version arXiv:2506.19756, Appendix A.2, read by us;
the two referees confirmed the same convention in Dirks et al. 2007, Appendix B note 3, in Shalaby–Woods
2026, footnote 19, and in the pseudocode of Shalaby–Woods ICALP 2025; the *implementation* described by
Dirks et al. adds dangle energies, which their exposition omits).

**Hypotheses on `g`.**

* **(H0)** `g(f) = 0` for every exterior loop.  (A constant `e_0` instead of `0` only shifts all energies
  by `c·e_0`, every connected structure having exactly `c` exterior loops.)
* **(H1)** There is `σ < 0` such that `g(f) = σ` for every stack whose two pairs are `G–C` pairs with
  the two `G` on one strand and the two `C` on another (the stack `5′-GG-3′ / 3′-CC-5′`).
* **(H2′)** There is `δ > 0` such that every bulge or interior loop `f` closed by two `G–C` pairs with
  the `G`'s on one strand and the `C`'s on another satisfies `g(f) ≥ (u_C(f) + 1)·σ + δ`, where `u_C(f)`
  is the number of unpaired bases on the `C`-side of `f`.

The simpler hypothesis **(H2)**, `g(f) ≥ 0` for every bulge and interior loop, implies (H2′) with
`δ = |σ|`; so does `g(f) ≥ σ + δ`.  No hypothesis on hairpins, multiloops, other stacks, `ΔG_assoc` or
the temperature (hairpins and multiloops do not occur in the instances, see (a′) below).  The stack-only
model (`g = −1` on stacks, `0` elsewhere) satisfies (H0)–(H2); so does every `j`-fold magnification of a
model that satisfies (H0)–(H2′).

*On published parameter tables.*  The first version of this note said that (H0)–(H2) is "the sign pattern
of every physical parameter set".  That is false (REV-0001, finding 1): with the single-nucleotide bulge
rule of the Turner-2004 parameters a bulged `C` between `G–C` pairs has negative energy, so (H2) fails;
(H2′) is the hypothesis the proof actually needs.  According to the referee's computation — which we have
not repeated — (H2′) holds, with a margin of at least 2.9 kcal/mol, for all 210 loop types that can occur
in the instances, in each of the five parameter files distributed with ViennaRNA (Turner 2004 and 1999,
Andronescu 2007, DNA Mathews 2004 and 1999).  (H0) is a property of the formal model, not of software
that adds dangling-end or coaxial-stacking terms to exterior loops; see Theorem 1c and §8.

---

## 2. The reduction

**EXACT BIN PACKING.**  Input: positive integers `a_1,…,a_n`, `m`, `B` in unary with `Σ a_i = m·B`.
Question: is there a map `β : {1,…,n} → {1,…,m}` with `Σ_{β(i)=t} a_i = B` for every `t`?  It contains
3-PARTITION (`n = 3m`, `B/4 < a_i < B/2`) and 4-PARTITION (`n = 4m`, `B/5 < a_i < B/3`), which are
NP-complete in the strong sense (Garey–Johnson 1979, Theorem 4.4 and Theorem 4.3 respectively — numbers
from memory; [K]; a proof for 4-PARTITION with explicit sizes is in Appendix A).

**The system `I(a, m, B)`.**

```
template   τ   =  G^B A G^B A … A G^B          (m blocks G^B separated by single A's;  mB + m − 1 bases)
items      κ_i =  C^{a_i}   for i = 1,…,n
```

`c = n + 1` strands, `N = 2mB + m − 1` bases, constructed in time polynomial in the unary input.
Put `M = Σ_i (a_i − 1) = mB − n` (the number of covalent bonds of the items).  A connected unpseudoknotted
structure of `I` is a *tiling structure* if every item is paired, base by base and antiparallel, with a
run of consecutive `G`'s inside one block, and these runs partition the `G`'s of the template.

**Theorem 1 [P].**  Let `g` satisfy (H0), (H1), (H2′), let `a_i ≥ 1`, `I = I(a,m,B)`,
`E* = σ·M + n·ΔG_assoc` and `ε = min(δ, |σ|)`.  Then for every connected unpseudoknotted structure `S` of
`I`:  `ΔG_g(S) = E*` if `S` is a tiling structure, and `ΔG_g(S) ≥ E* + ε` otherwise.  Consequently

1. if the bin-packing instance has a solution, then `MFE(I) = E*`;
2. otherwise `MFE(I) ≥ E* + ε`.

*Proof.*  Let `S` be a connected unpseudoknotted structure of `I` and `π` its ordering.

(a) *Pairs.*  `A` has no complementary letter in the system, the template contains no `C` and the
items contain no `G`.  So every pair of `S` joins a `G` of the template and a `C` of an item.

(a′) *Faces.*  Cut the circle at the nick before the 5′ end of the template: the positions are those of
the template, `1,…,mB+m−1`, followed by those of the items.  Every chord joins a template position `t` to
an item position `c`; as chords do not cross, they can be numbered `(t_1,c_1),…,(t_K,c_K)` with
`t_1 < ⋯ < t_K` and `c_1 > ⋯ > c_K` (they are nested).  The faces are therefore `F_0` (outside the first
chord), `F_k` (between the chords `k` and `k+1`, `1 ≤ k < K`) and `F_K` (inside the last chord): every face
has at most two chords on its boundary — there are no multiloops — and the two faces with one chord, `F_0`
and `F_K`, contain the two nicks at the ends of the template — there are no hairpins.  The boundary of
`F_k`, `1 ≤ k < K`, consists of the two chords, a *template side* (the links from `t_k` to `t_{k+1}`) and an
*item side* (the links from `c_{k+1}` to `c_k`, covalent bonds of items and nicks between items).

(b) *Symmetry.*  The template is the only strand with its sequence, so every rotation counted by
`R(S)` fixes it and is the identity: `R(S) = 1`.  Hence `ΔG_g(S) = Σ_f g(f) + n·ΔG_assoc`.

(c) *Accounting by item bonds.*  For a face `f` let `ι(f)` be the number of covalent bonds of items on its
boundary.  A link lies on the boundary of exactly one face, so `Σ_f ι(f) = M` and

```
Σ_f g(f) − σ·M  =  Σ_f ( g(f) − σ·ι(f) ).                                    (1)
```

The faces of the connected structure `S` are of three kinds (Fact 1 and (a′)).
*Stacks*: the item side is a single bond `(κ_i, j)–(κ_i, j+1)`, the template side a bond between two
adjacent paired template bases, both `G`; this is the stack of (H1), `ι = 1`, and the term in (1) is `0`.
*Exterior loops*: `g = 0` by (H0), the term is `|σ|·ι(f) ≥ 0`.
*Bulges and interior loops*: no nick, so the item side lies in one item and consists of `u_C(f) + 1` bonds;
`ι(f) = u_C(f) + 1 ≥ 1` and the term is `≥ δ` by (H2′).
Hence `Σ_f g(f) ≥ σM`, and `Σ_f g(f) ≥ σM + min(δ, |σ|)` unless `S` has no bulge or interior loop and no
exterior loop containing an item bond, that is, unless **every bond of every item lies on a stack**.

(d) *If every item bond lies on a stack, `S` is a tiling structure.*  Fix an item `κ_i` with `a_i ≥ 2`;
for each `j < a_i` the bases `(κ_i,j)`, `(κ_i,j+1)` are paired with two *adjacent* template bases.  The
partners `p_1,…,p_{a_i}` of the bases of `κ_i` are thus distinct template positions with
`|p_{j+1} − p_j| = 1`; a sequence of integers with unit steps that never repeats a value is monotone, so
they form a run of `a_i` consecutive positions, all `G`; a run of consecutive `G`'s contains no `A`, so it
lies in one block.  (The chords are nested, (a′), so the run is traversed 3′→5′: the pairing is
antiparallel.)  An item with `a_i = 1` is paired because `S` is connected, and its partner is a run of
length one.  All `Σ a_i = mB` item bases are paired with distinct template `G`'s, of which there are
`mB`: the runs partition the `G`'s, and each block, being a union of runs, is exactly filled.  So `S` is a
tiling structure, and `β(i) =` "block of the run of `κ_i`" solves the bin-packing instance.

(e) *A tiling structure has energy `E*`, and a solution gives one.*  Let `β` be a solution; order the
items of each block arbitrarily and let `S*` pair them accordingly, antiparallel.  In the circular order
"template, then the items in the reverse order of their runs along the template" the chords are nested,
so `S*` is unpseudoknotted.  Its faces are: `a_i − 1` stacks for every item; one face between two
consecutive items of the same block (two chords, one template bond, one nick); one face between the
last item of a block and the first of the next (two chords, the unpaired `A` with its two bonds, one
nick); `F_K`, whose boundary contains the nick between the template and the first item; and `F_0`, whose
boundary contains the nick between the last item and the 5′ end of the template.  That is `M` stacks and
`n + 1 = c` faces with exactly one nick each, so `S*` is connected (Fact 1) and, by (H0), (H1),
`ΔG_g(S*) = σM + nΔG_assoc`.  Every tiling structure arises in this way.

By (c) and (d) a structure that is not a tiling structure has energy `≥ E* + ε`; by (e) tiling structures
have energy `E*` and exist iff the instance has a solution.  ∎

**Corollary 2 [P]** (NP-hardness; answers the multi-strand half of A1).  For every loop-energy
function `g` satisfying (H0), (H1), (H2′) and every value of `ΔG_assoc` and `T`, the problem "given a
system and a number `k`, is `MFE ≤ k`?" for connected unpseudoknotted structures in the nearest-neighbour
model with rotational symmetry is NP-hard in the strong sense, already for systems consisting of one
strand over `{G,A}` and homopolymer strands `C^a`, `a ≥ 2`.

*Proof.*  Theorem 1, from 3-PARTITION (all `a_i ≥ 2` after multiplying all numbers by 2), with any
threshold `k` in `[E*, E* + ε)`; a rational `k` in this interval is computable in polynomial time from
rational approximations of the constants `σ`, `δ`, `ΔG_assoc` of the fixed model.  ∎

*Membership in NP.*  If `g` is polynomial-time computable with rational values, the problem without the
symmetry term (or restricted to systems all of whose structures have `R = 1`, such as the instances
above) is in NP: guess `π` and `S`; non-crossing, the face decomposition and the energy are computable in
polynomial time.  With the term `k_B T ln R(S)`, `R ≥ 2`, the comparison `ΔG ≤ k` involves the logarithm of
an integer; we make no membership claim for that case (the first version did, without argument:
REV-0001, finding 5).

**Remarks.**
1. The energy model may be *fixed*: the hardness is not an artefact of making `g` part of the input.
2. The same proof gives NP-hardness of maximising the number of stacks over unpseudoknotted structures of
   many strands when disconnected structures are allowed, for items with `a_i ≥ 2`, **if a stack is
   defined as a nick-free face** with two pairs and no unpaired base: steps (a), (c), (d), (e) use
   connectedness only for items of length one.  Under the literal reading of [DSW] Definition 9 applied to
   a concatenation of strands — `BPS(S) = |{(i,j) ∈ S : (i+1,j−1) ∈ S}|`, which also counts a "stack"
   across a nick — the instances are trivial (this is the case `x = σ`, `γ = 0` of Theorem 1c).
3. *Why the base-pair result does not already answer the question* (SCI-REV-0019, F11).  On the connected
   ensemble the base-pair model is itself a loop model: a connected unpseudoknotted `S` has `|S| + 1` faces,
   `c` of them exterior, so `−|S| = Σ_f g(f) − (c − 1)` with `g = −1` on every non-exterior loop.  It satisfies
   (H0), (H1) and violates (H2′) — a bulge is as favourable as a stack — and for it the instances `I(a,m,B)`
   are trivial (all `mB` pairs can always be formed), which is why the reduction of [CHT] is elaborate.
   Conversely [CHT] already gives hardness for that one loop function (their yes-instances have a
   single-complex optimum, according to the science referee's reading of their paper; we have not checked
   this).  What is shown here is hardness when loops with unpaired bases are less favourable than the stacks
   they replace, for every fixed such function.
4. The number of strands of the instances is `c = n + 1`, with `N = 2mB + m − 1`; for 3-PARTITION
   `c = Θ(N/B)`, which is unbounded and polynomial in `N`, but `o(N)`.  The instances use one long strand
   and, in general, `n + 1` different strand species.
5. *Several complexes* (SCI-REV-0019, F9 and statement (P4); proof re-derived by us).  Theorem 1 is about
   the one complex containing all strands, as in [DSW] and Shalaby–Woods.  If strands may be left out — a
   structure being a set `J` of items in one complex with the template, the other items free, with energy
   `Σ_f g(f) + |J|·ΔG_assoc` — the equivalence can fail (`a = (2,2,2)`, `m = 2`, `B = 3`, `ΔG_assoc ≥ |σ|`:
   binding two items is at least as good as any structure with three).  It holds for instances with
   `|σ|(a_i − 1) > ΔG_assoc` for every `i`: with `J` bound, the accounting of step (c) gives
   `Σ_f g(f) ≥ σ·Σ_{i∈J}(a_i − 1)`, so the energy is at least
   `E* + Σ_{i∉J}(|σ|(a_i − 1) − ΔG_assoc) > E*` unless `J` is everything, and then Theorem 1 applies.
   Multiplying all `a_i` and `B` by a constant preserves solvability, so the problem is strongly NP-hard in
   this formulation as well, for every fixed `ΔG_assoc`.

---

## 3. Coaxial stacking of flush helices

In a tiling structure two items that are neighbours in a block form two helices that are adjacent on the
template, separated by a nick.  Models with *coaxial stacking* reward this.  Call a face **flush** if its
boundary consists of two chords, one template bond, and one nick between two items, with no unpaired
base.  Replace (H0) and (H2′) by

* **(C0)** `g(f) = x` for every flush face, with a constant `x ≤ 0`, and `g(f) = 0` for every other
  exterior loop;
* **(C2)** `g(f) ≥ γ` for every bulge and interior loop of the kind in (H2′), with a constant `γ ≥ 0`.

**Theorem 1c [P].**  Let `g` satisfy (C0), (H1), (C2) with `|x| < |σ| + min(|σ|, γ)`, and let `B ≥ 2` if
`|x| ≥ |σ|`.  Put `E*_x = σM + x(n − m) + nΔG_assoc` and

```
ε_x = |σ| − |x|                          if |x| < |σ|,
ε_x = min(|σ|, γ) − (|x| − |σ|)          if |x| ≥ |σ|.
```

Then every connected unpseudoknotted structure `S` of `I(a,m,B)` has `ΔG_g(S) = E*_x` if it is a tiling
structure and `ΔG_g(S) ≥ E*_x + ε_x` otherwise.  So `MFE = E*_x` iff the bin-packing instance has a
solution, and Corollary 2 holds for these models as well.

*Proof.*  Steps (a), (a′), (b), (d) of the proof of Theorem 1 do not involve the energies.  A tiling
structure has `M` stacks, `n − m` flush faces (between neighbours in a block) and `m + 1` other exterior
loops (step (e)), hence energy `E*_x`.  Let `S` be connected and write `E = Σ_f g(f)`, `E_0 = σM + x(n−m)`.
For a face `f` let `ι(f)` be as before and `τ(f)` the number of template bonds between two `G`'s on its
boundary; `Σ_f ι(f) = M` and `Σ_f τ(f) = m(B−1) = M + n − m`.  A stack has `(ι,τ) = (1,1)`, a flush face
`(0,1)`.

*Case `|x| < |σ|`.*  Since `σM + x(n−m) = Σ_f [σ ι(f) + x(τ(f) − ι(f))]`,

```
E − E_0 = Σ_f [ g(f) + (|σ| − |x|)·ι(f) + |x|·τ(f) ].
```

The term of a stack and of a flush face is `0`; that of another exterior loop is
`(|σ|−|x|)ι + |x|τ ≥ 0`; that of a bulge or interior loop is `≥ γ + (|σ| − |x|) ≥ |σ| − |x|` because
`ι ≥ 1`.  If `S` is not a tiling structure, some item bond is not on a stack (step (d)); it lies on a
bulge or interior loop, or on an exterior loop with `ι ≥ 1`, which is not flush; either way
`E − E_0 ≥ |σ| − |x|`.

*Case `|x| ≥ |σ|`, `d = |x| − |σ| < min(|σ|, γ)`, `B ≥ 2`.*  Let `st`, `fl` be the numbers of stacks and of
flush faces, `L` the number of template `GG` bonds that lie on neither (*loose* bonds), `z` the number of
nicks between two items that lie on faces that are not flush, and `P` the total energy of the bulges and
interior loops.  Every stack and every flush face contains exactly one template `GG` bond, and every flush
face exactly one of the `n − 1` nicks between items, so `st + fl + L = M + n − m` and `fl = n − 1 − z`;
therefore `st = M − (m−1) − L + z` and

```
E − E_0 = σ·st + x·fl + P − σM − x(n−m) = |σ|·L + P − d·(m − 1 − z).                      (2)
```

*The separators.*  Each of the `m − 1` separators `A` is unpaired and lies, with its two bonds, on one
face.  Let `𝔉` be the set of faces containing a separator and `k_f ≥ 1` the number of separators on
`f ∈ 𝔉`.  The template side of a face is a set of consecutive template positions, all unpaired except its
ends ((a′)).  So a face `F_k ∈ 𝔉` with `0 < k < K` contains the `k_f − 1` blocks between its separators,
entirely unpaired, hence at least `(k_f − 1)(B − 1) ≥ k_f − 1` loose bonds; and if `F_0` or `F_K` belongs
to `𝔉`, it contains the `k_f` blocks between its end of the template and its separator farthest from that
end, hence at least `k_f` loose bonds.  (Bonds on a face of `𝔉` are loose: such a face has an unpaired base.)  A face
`F_k ∈ 𝔉`, `0 < k < K`, either has no nick — then it is a bulge or interior loop; let `r` be the number of
these — or has exactly one nick, which is a nick between two items on a face that is not flush.
Different faces contain different bonds and different nicks.  Summing over `𝔉`:

```
m − 1 = Σ_{f ∈ 𝔉} k_f  ≤  L + r + z.
```

*Conclusion.*  The `r` loops cost at least `γ` each; let `P'' ≥ 0` be the energy of the other bulges and
interior loops.  If `m − 1 − z ≤ 0`, (2) gives `E − E_0 ≥ |σ|L + P`; otherwise
`d(m − 1 − z) ≤ d(L + r)`.  In both cases

```
E − E_0  ≥  (|σ| − d)·L + (γ − d)·r + P''  ≥  0 ,
```

and `E − E_0 ≥ min(|σ|, γ) − d` as soon as `L ≥ 1` or `S` has a bulge or interior loop (each costs
`≥ γ ≥ γ − d`).  Finally, if `L = 0` and `S` has no bulge or interior loop, then `S` is a tiling structure:
every template `GG` bond lies on a stack or a flush face, so both its ends are paired, and as `B ≥ 2` every
`G` of the template is paired; then all `mB` item bases are paired; the face between the chords of two
consecutive bases of an item has that item bond as its item side, hence no nick, hence is a stack; so
every item bond lies on a stack and (d) applies.  ∎

*Sharpness (not needed for the hardness statements).*  For `x = σ`, `γ = 0` every arrangement of the items
along the template, straddling the separators or not, has energy `E*_x`, and the reduction fails.  In our
exhaustive tests the conclusion fails on small instances at `(x,γ) = (σ, 0)`, at `|x| = |σ| + γ < 2|σ|` and
at `|x| = 2|σ| < |σ| + γ` (`test_generalised_hypotheses.py`, control models), and the referee found the
condition `|x| < |σ| + min(|σ|,γ)` to be exact on a grid of values (REV-0001, finding 2, where the
statement of Theorem 1c was proposed with a proof sketch; the proof above is ours).  When the energy of a
flush stack equals that of the corresponding stack, `x = σ`, as in the usual nearest-neighbour rules for
coaxial stacking, Theorem 1c applies as soon as every bulge and interior loop of the instances costs a
positive amount: `γ > 0`.

**Dangles.**  Replace (H0) by

* **(D0)** the energy of an exterior loop `f` is `Σ_u d(u)` over the unpaired bases `u` of `f` that are
  covalent neighbours of a paired base of `f` (one term per base), with `−D_G ≤ d(u) ≤ 0` for a template
  `G`, `−D_C ≤ d(u) ≤ 0` for an item `C`, and `e_A ≤ d(u) ≤ 0` for an `A`, where `e_A` is the value taken by
  an `A` both of whose neighbours are paired.

**Theorem 1d [P; the statement and its proof are statement (P3) of the science division's review
SCI-REV-0019, re-derived and tested by us].**  Let `g` satisfy (D0), (H1), (H2) and `|σ| > D_G + D_C`.  Then
every connected unpseudoknotted structure of `I(a,m,B)` has energy `σM + (m−1)e_A + nΔG_assoc` if it is a
tiling structure, and at least `|σ| − D_G − D_C` more otherwise.

*Proof.*  Let `j = M − st(S)` be the number of item bonds that are not on a stack, and `u` the number of
unpaired item bases; it equals the number of unpaired template `G`'s.  An item with `r` unpaired bases has a
paired base (connectedness), so at least `r` of its bonds have an unpaired end — a maximal run of `ℓ`
unpaired bases touches `ℓ − 1` bonds inside it and at least one at its border — and none of these bonds
lies on a stack.  Hence `j ≥ u`.  Bulges and interior loops cost `≥ 0`, each unpaired `G` and `C`
contributes at least `−D_G`, `−D_C`, and the `A`'s together at least `(m−1)e_A`; so
`Σ_f g(f) ≥ σ(M − j) − u(D_G + D_C) + (m−1)e_A ≥ σM + (m−1)e_A + j(|σ| − D_G − D_C)`.  A tiling structure has
`j = 0`, no unpaired `G` or `C`, and each separator between two paired `G`'s: equality.  A structure that
is not a tiling has `j ≥ 1` (step (d)).  ∎

**Coaxial stacking and dangles together.**

**Theorem 1e [P; written 2026-11-26 after both reviews, unreviewed].**  Let flush faces have energy `x` with
`σ ≤ x ≤ 0`, let every other exterior loop have the dangle energy of (D0), let bulges and interior loops cost
at least `γ ≥ 0` (C2), and assume (H1), `B ≥ 2`,

```
D_C + max( D_G , |x|/B )  <  |σ|        and        |σ| − |x| + γ + |e_A|  >  0 .
```

Then every connected unpseudoknotted structure of `I(a,m,B)` has energy
`E** = σM + x(n−m) + (m−1)e_A + nΔG_assoc` if it is a tiling structure, and at least
`min( |σ| − D_C − max(D_G, |x|/B) ,  |σ| − |x| + γ + |e_A| )` more otherwise.

In particular this covers a flush stack as strong as a stack (`x = σ`) together with dangles, as soon as the
bulge over a separator costs something or a dangling separator is favourable.  For a fixed model with
`D_G + D_C < |σ|` the first condition holds for all instances with `B > |x|/(|σ| − D_C)`, and multiplying
all sizes of a bin-packing instance by a constant preserves solvability; so Corollary 2 extends to every such
model.

*Proof.*  Let `u` be the number of unpaired item bases (equal to the number of unpaired template `G`'s),
`j = M − st` the number of item bonds not on a stack, `fl` the number of flush faces and `L` the number of
template `GG` bonds on neither a stack nor a flush face.  As in the proof of Theorem 1c,
`st + fl + L = M + n − m`, so `fl = n − m + j − L`, and with `P` the energy of the bulges and interior loops
and `Dng` the total dangle energy,

```
E − E** = (|σ| − |x|)·j + |x|·L + P + Dng − (m−1)e_A .
```

`j ≥ u` (proof of Theorem 1d).  `L ≥ u − β`, where `β` is the number of blocks all of whose `G`'s are
unpaired: a maximal run of `ℓ` unpaired `G`'s in a block touches `ℓ − 1` bonds inside it and, unless it is the
whole block, at least one bond to a paired `G`; all these bonds are loose and different runs touch different
bonds.  `β ≤ u/B`.  The `G`'s of an entirely unpaired block have no paired neighbour and get no dangle term,
so `Dng ≥ −D_G(u − Bβ) − D_C u + e_A·a`, with `a ≤ m − 1` the number of separators that get a dangle term.
Hence

```
E − E**  ≥  u(|σ| − D_G − D_C) + β(B·D_G − |x|) + P + |e_A|(m − 1 − a)
         ≥  u·( |σ| − D_C − max(D_G, |x|/B) )  +  P  +  |e_A|·(m − 1 − a)
```

(if `B·D_G < |x|` use `β ≤ u/B`).  If `u ≥ 1` this is at least `|σ| − D_C − max(D_G, |x|/B)`.  If `u = 0`, every base is paired; then every template
`GG` bond lies between two chords whose item ends are consecutive positions, so it is on a stack or a flush
face and `L = 0`; an item bond is on a stack or on a bulge whose template side is one separator (a
*straddle*); with `r` straddles, `j = r`, the `r` straddled separators get no dangle term and the others get
`e_A`, and `E − E** = (|σ| − |x|)r + P + |e_A| r ≥ r(|σ| − |x| + γ + |e_A|)`.  A structure with `u = 0` and
`r = 0` has every item bond on a stack and is a tiling structure (step (d)); a tiling structure has
`u = j = L = 0`, `a = m − 1`, `P = 0`.  ∎

The dependence on `B` is real: with `x = σ`, `D_G = 0` and `D_C = ⅔|σ|` or `⅚|σ|` the conclusion fails on
instances with `B = 2` (an entirely unpaired block costs `|σ|B − |x|` and its `B` dangling item bases gain
`B·D_C`), and it fails at `D_G + D_C = |σ|` for every `B` (controls in `test_generalised_hypotheses.py`).  A
first version of this theorem had the stronger hypothesis `D_G + D_C < |σ| − |x|/B` and the guess that the
term `|x|/B` was an artefact; the guess was wrong.  What remains uncovered: dangle rules
in which an unpaired base between two helices is counted for both, terminal mismatches, and coaxial stacking
across an intervening unpaired base.

---

## 4. Counting: #SSEL and the partition function

Let `L(a,m,B)` be the number of partitions of the index set `{1,…,n}` into `m` classes each of total
size `B` (for 4-PARTITION instances this is the function shown #P-complete in [DSW], Lemma 31; [K]).
For a size `s` let `μ_s = #{i : a_i = s}`.

**Theorem 3 [P].**  Let `g` satisfy the hypotheses of Theorem 1 or of Theorem 1c, `a_i ≥ 1`,
`I = I(a,m,B)`, and let `E*` denote `E*` resp. `E*_x`.

1. With all strands regarded as distinguishable, the number of connected unpseudoknotted structures
   of `I` with energy `E*` is `Til(a,m,B)`, the number of ways to arrange the labelled items into `m`
   ordered rows (row `t` = block `t` of the template), each row an ordered sequence of items of total
   length `B`:  `Til = Σ_β Π_t |β^{-1}(t)|!` over the solutions `β` of the bin-packing instance.  For
   3-PARTITION instances `Til = L·m!·6^m`, for 4-PARTITION instances `Til = L·m!·24^m`.
2. In the physical ensemble, `#SSEL(E*) = Til(a,m,B) / Π_s μ_s!`.

*Proof.*  By Theorem 1 (1c) the structures of energy `E*` are the tiling structures, and a tiling
structure is determined by, and determines, the sequence of items along each block: 1.  The group
`Π_s Sym(μ_s)` of permutations of equal items acts on the tiling structures, and freely: a permutation
that maps a tiling structure to itself maps every item to an item paired with the same run of the
template, i.e. to itself.  So every orbit has `Π_s μ_s!` elements, and the orbits are the structures of
the physical ensemble: 2.  For 3- and 4-PARTITION instances every class of a valid partition has
exactly 3, resp. 4, elements; the `m` classes can be assigned to the blocks in `m!` ways and each
ordered in `3!`, resp. `4!`, ways.  ∎

**Corollary 4 [P]** (#P-hardness; answers the second sentence of A1 for the multi-strand case).
Let `g` satisfy the hypotheses of Theorem 1 or 1c.
(i) `#SSEL` in the nearest-neighbour model with energy function `g` is #P-hard.
(ii) The function "(system, `j`) ↦ partition function of the `j`-fold magnified model `j·g`" is #P-hard,
already for magnifications `j` bounded by a polynomial in `N`, under a reduction that makes **one** oracle
call (the oracle being exact, as in [DSW] Theorem 22).  Equivalently, for a temperature-independent `g`,
the partition function with the temperature as part of the input is #P-hard.

*Proof.*  (i) Given a 4-PARTITION instance, `L = #SSEL(E*)·Π_s μ_s! / (m!·24^m)` (if the level `E*`, a
real number, cannot be given to the oracle exactly, the number of structures of energy below any
threshold in `(E*, E* + ε)` serves equally).  The instances of
4-PARTITION produced by the proof of [DSW] Lemma 31 are those of Garey and Johnson's reduction, whose
sizes are bounded by a polynomial in the size of the 3DM instance (Appendix A, Lemma A2), so the strands
can be written out in unary in polynomial time.
(ii) Let `Z_j = Σ_S e^{−j·Σ_f g(f)/k_BT}` be the partition function of `j·g` over the physical ensemble of
`I`, without the common factor `e^{−nΔG_assoc/k_BT}` (all structures of `I` have `R = 1`).  Put
`β = j/k_BT`, let `N* = #SSEL(E*)` and let `U = n!·3^N` (the number of cyclic orderings times a bound on
the number of non-crossing sets of chords on `N` points; an upper bound for the number of structures).
By Theorem 1 (1c), `e^{β E_0}·Z_j = N* + ρ` with `0 ≤ ρ ≤ U·e^{−βε}`, where `E_0 = E* − nΔG_assoc` and `ε`
is the gap of the theorem.  For `j ≥ k_BT·ln(2U)/ε = O(N log N)` we get `ρ < 1/2` and
`N* = ⌊e^{βE_0} Z_j⌋`.  ∎

(The first version obtained (ii) only for the stack-only model, by polynomial interpolation over `M + 1`
temperatures; the one-call argument was pointed out by the referee, REV-0001 finding 6.)

*Membership.*  If `g` is polynomial-time computable with rational values, `#SSEL` restricted to systems
whose structures have `R = 1` is in #P provided structures of the physical ensemble are counted through
canonical representatives; for the polymer graph a canonical representative under permutations of equal
strands is the lexicographically least among the `c` rotations of its encoding, computable in polynomial
time.  We do not need this and do not claim #P-completeness beyond it.

What is **not** shown: #P-hardness of the partition function at a *fixed* temperature for a *fixed* `g`
(problem A3′).  In (ii) the magnification grows with the instance.

---

## 5. A lower bound in the number of strands under ETH

**Corollary 5 [P; conditional on the Exponential Time Hypothesis].**  Let `g` satisfy the hypotheses of
Theorem 1 or 1c.  Unless ETH fails, no algorithm decides `MFE ≤ k` in time `2^{o(c)}·poly(N)`, `c` the
number of strands.

*Proof.*  [K] (Impagliazzo–Paturi–Zane 2001, sparsification lemma; cited from memory, not re-read): under
ETH, 3-SAT on formulas with `m` clauses cannot be decided in time `2^{o(m)}`.  Lemma A1 maps such a formula
to a 3DM instance with at most `21m` triples; Lemma A2 maps a 3DM instance with triple set `T` to an exact
bin-packing instance with `4|T|` items and sizes polynomial in the instance; Theorem 1 maps that to a
system with `c = 4|T| + 1 ≤ 84m + 1` strands and `N = poly(m)` bases.  An algorithm running in time
`2^{o(c)}·poly(N)` would decide 3-SAT in time `2^{o(m)}`.  ∎

With `STRANDS_ALGORITHM.md` (`O(N⁴·3^c)` arithmetic operations for the partition function): the
single-exponential dependence on the number of strands is optimal up to the constant in the exponent,
under ETH and in the unit-cost model of that algorithm — provided the decision version of MFE is obtained
from the partition function as in Shalaby–Woods 2026, §7, a step we have not re-derived.

(In the first version step one was a citation of a `2^{Ω(q)}` bound for 3DM that the cited source states
without the linear bound on the number of triples it needs — REV-0001, finding 4.  Appendix A removes the
dependence on that source.)

Further remarks.
* For a bounded number of strand *species* the partition function over all orderings is computable in
  polynomial time (`STRANDS_ALGORITHM.md`, Theorem 1; [P], unreviewed).  The corresponding statement for
  the MFE — the same recursion over `(min,+)`, or [SW26, §7] applied to the partition function — is not
  written out by us; for a base-pair model it is Theorem 16 of Boehmer et al. (WABI 2024).  The hardness
  above therefore needs unboundedly many species; whether MFE is W[1]-hard in the number of species is
  open (`OPEN_PROBLEMS.md` C2).
* The single-strand pseudoknotted half of A1 is not addressed: the nearest-neighbour model of the
  cited papers has no energy rule for pseudoknots.

---

## 6. Verification

* **[X], ours.**  `experiments/complexity/strands/test_partition_reduction.py`,
  `test_partition_reduction_big.py` (log `big_run.log`): all connected unpseudoknotted structures over all
  circular orderings of 18 instances with `2 ≤ m ≤ 3`, `3 ≤ B ≤ 5` (up to 1 887 888 structures per
  instance), stack-only model and a model with random non-negative bulge/interior energies: the minimum
  is `σM` exactly when a packing exists and `≥ σ(M−1)` otherwise; the number of minimum-energy labelled
  structures equals the number of labelled tilings computed by brute force; every labelled connected
  structure occurs under exactly one circular ordering.
* **[X], ours, added in the revision.**  `test_generalised_hypotheses.py` (logs `generalised_run.log`,
  `generalised_run_big.log`): 36 instances with `1 ≤ m ≤ 3`, `1 ≤ B ≤ 5`, including `m = 1`, `B ≤ 2` and
  items longer than a block (up to 762 294 structures); 28 models satisfying the hypotheses of Theorem 1
  with (H2′) (bulge and interior loops as favourable as `σ·ι + δ`), of Theorem 1c (both cases), of
  Theorem 1d or of Theorem 1e (for the latter, on the instances whose `B` satisfies its hypothesis), and nine
  control models violating them.  For every model satisfying the hypotheses: tiling structures have
  energy exactly `E*` (resp. `E*_x`), their number is `Til`, every other structure is at least `ε`
  (resp. `ε_x`) above; for the controls the statement fails on some instance.  The same runs check Fact 1
  against union–find on every structure (`check=True`), that every structure has trivial stabiliser under
  permutations of equal strands, and that the number of orbits of minimum-energy structures is
  `Til/Π_s μ_s!`.
* **[X], ours.**  `test_eth_chain.py`: Lemmas A1 and A2 against exhaustive search on 1500 random formulas
  and 444 random 3DM instances.
* **[X], the referee's, independent code** (`experiments/complexity/reviews/rev1_strands/`, REV-0001):
  brute force over 134 instances (413.5 million connected labelled structures, 14 models satisfying
  (H0)–(H2)) and a second exact method (a transfer-matrix dynamic programme) on a further 867 instances
  including 3-PARTITION- and 4-PARTITION-shaped ones: no failure of Theorem 1 or Theorem 3.
* **[X], the science division's referee, a third independent enumerator** (their branch,
  `experiments/science/ws_R20/`, SCI-REV-0019): 74 instances, 12.6 million connected structures over all
  strand orders, five loop-energy functions inside (H0)–(H2) and seven for the generalisations: no
  violation; the controls fail; their numbers equal ours on the thirteen shared instances.
* Memory: `test_partition_reduction_big.py` kept every structure in a set and needed more than 2 GB for
  its largest case (found by the science referee); it now keeps 64-bit hashes.
* **[V]** `experiments/complexity/lean/StackPacking.lean` (register CX-V1): the counting core of step (d) —
  if all item bases are paired injectively with template `G`'s, consecutive bases with adjacent positions,
  then the items pack into the blocks.  The model of structures and loops around it is not formalised.
* Reviews: `COMPLEXITY-REV-0001` (internal, adversarial; verdict "correct with gaps", no critical finding;
  all findings and what was done about them are listed at the end of that file) and `SCI-REV-0019` (the
  science division's, independent of ours; "Theorems 1 and 3 are proved as stated", 0 critical, 2 major,
  10 minor findings; our answer is `COMPLEXITY-RES-0004`).  Reviews by AI sessions are not academic peer
  review.

## 7. What the result is and is not worth

It answers the question in the model in which the question was asked, for a fixed energy function, with the
association and symmetry terms present.  It is an elementary observation: Lyngsø's bin-packing gadget with
the `C`-blocks cut into strands; only the `GG/CC` stack parameter and a lower bound on bulge and interior
loop energies matter.  It needs one long template and unboundedly many strand species.  It is a worst-case
statement about synthetic instances and says nothing about typical instances.

## 8. Limitations (read before citing)

1. (H0) is an assumption about the model.  Energy functions that give exterior loops context-dependent
   energies are covered only in the cases of Theorem 1c (flush coaxial stacks), Theorem 1d (one dangle
   term per unpaired base next to a helix end, total strength below `|σ|`) and Theorem 1e (both, with the
   flush stack no stronger than a stack).  Whether
   a published table with dangles and coaxial stacking, as implemented, satisfies the hypotheses of either
   has been checked by nobody.  Our referee's numerical experiments with simplified re-implementations of
   such conventions (five published parameter tables valid on 112 small instances) are evidence about
   small instances, not proofs, and we have not repeated them.
2. (H2′) excludes energy functions in which a bulge or interior loop is at least as favourable as the
   stacks it displaces; the control models show that the reduction then fails.
3. Corollary 4(ii) lets the magnification grow with the instance; Corollary 5 is conditional on ETH and
   uses the sparsification lemma as a cited fact.
4. The proofs are paper proofs by this division.  "Reviewed" in `THEOREMS.md` means the internal
   adversarial review named there, which is not academic peer review.  Theorem 1c (our proof), the
   one-call form of Corollary 4(ii), Appendix A, our write-up of Theorem 1d and of Remark 5, and Theorem 1e
   were written **after** the reviews and have not been reviewed in this form (a further internal review of
   everything except Theorem 1e was commissioned at 19:05 UTC).

## 9. Changes after the review COMPLEXITY-REV-0001

| finding | change |
|---|---|
| 1 (major): "(H0)–(H2) is the sign pattern of every physical parameter set" is false | sentence removed; hypothesis weakened to (H2′), proof rewritten as an accounting over item bonds; gap `ε = min(δ,|σ|)` |
| 2 (major): the remark that coaxial stacking as strong as stacking breaks the reduction is false in general | remark replaced by Theorem 1c with a full proof; failure only stated for `x = σ`, `γ = 0` |
| 3 (major): attribution | §0 "Whose gadget this is"; Boehmer et al. Theorem 19 discussed; novelty worded as "apparently unpublished" |
| 4 (major for Cor. 5): the cited 3DM bound is not established at the source in the form used | Appendix A: explicit linear-size chain 3-SAT → 3DM → exact bin packing, with proofs and tests |
| 5: NP membership unargued | membership claimed only without the symmetry term; threshold `k` discussed |
| 6: #P membership; polynomially bounded sizes; Vandermonde unnecessary; summary too broad | membership remark; sizes via Lemma A2; one-call reduction for every `g`; summary corrected |
| 7: multiloop hypothesis vacuous | step (a′): chords are nested, no hairpins or multiloops; hypothesis removed |
| 8: cite the source of `ΔG_exterior = 0` | quoted from [DSW] full version, Appendix A.2 |
| 9: verification claims not backed by the scripts | §6 rewritten with the correct numbers; `check=True`, symmetry and physical counts now run; Lean status corrected |
| 10: unit steps cannot reverse | sentence added in (d) |
| 11: which reading of the BPS definition | Remark 2 |
| 12: "expected to be polynomial for boundedly many species" unsupported | replaced by a reference to `STRANDS_ALGORITHM.md` and an explicit statement of what is not written out |

**SCI-REV-0019** (the science division's independent review; its findings F1–F6 and F10 coincide with
findings 3, 1, 2, 6, 5, 6 and 9 above).  What it added:

| finding | change |
|---|---|
| F7: exactly what (H0) is used for; sources | constant `e_0` remark under (H0); sources with their places in §1 |
| F8: the pairing rule the theorem needs | §1: only "`{C,G}` is the one complementary pair among `A`, `C`, `G`" is used |
| F9, (P4): several complexes | Remark 5, with the condition `|σ|(a_i − 1) > ΔG_assoc` and the counterexample |
| F10: memory of the larger test | the test keeps hashes; §6 |
| F11: why the base-pair result does not answer the question | Remark 3 |
| F12: small slips | the two Garey–Johnson theorem numbers; the energy of [CHT]; the place of the quotation on exterior loops; times in message headers (corrected in COMPLEXITY-MSG-0003) |
| (P3): a sufficient condition for dangles | Theorem 1d |
| their remark on Corollary 5 (the closing sentence on optimality) | qualified in §5 |

---

## Appendix A.  A linear-size chain from 3-SAT to exact bin packing

Both reductions are textbook reductions of Garey and Johnson (1979, Theorems 3.2 and 4.3), which we did
not have at hand; the constructions below are written out and proved here, the first with the garbage
collection made local so that its size is linear.

**Lemma A1 [P; X].**  From a CNF formula `φ` with `m` clauses of at most three literals each one can
compute in polynomial time a 3DM instance `(W, X, Y, T)` with `|W| = |X| = |Y| ≤ 6m` and `|T| ≤ 21m` that
has a perfect matching iff `φ` is satisfiable.

*Construction.*  A *slot* is an occurrence of a literal in a clause; let `ℓ_C ≤ 3` be the number of slots
of the clause `C` and `L = Σ_C ℓ_C ≤ 3m`.  Number the slots of each variable `v` cyclically, `(v,1),…,(v,d_v)`.
Elements: for every slot `s` two *tips* `p_s, n_s ∈ W` and two internal elements `a_s ∈ X`, `b_s ∈ Y`; for
every clause `C` two elements `c¹_C ∈ X`, `c²_C ∈ Y` and `ℓ_C − 1` *garbage pairs* `g¹_{C,r} ∈ X`,
`g²_{C,r} ∈ Y`.  So `|W| = 2L` and `|X| = |Y| = L + m + (L − m) = 2L`.  Triples:

* for every variable `v` and `j = 1,…,d_v` the *true* triple `(n_{v,j}, a_{v,j}, b_{v,j})` and the *false*
  triple `(p_{v,j}, a_{v,j+1}, b_{v,j})` (second index mod `d_v`);
* for every clause `C` and every slot `s` of `C` the triple `(t_s, c¹_C, c²_C)`, where `t_s = p_s` if the
  occurrence is positive and `t_s = n_s` if it is negated;
* for every clause `C`, every `r` and every tip `t` of a slot of `C` the triple `(t, g¹_{C,r}, g²_{C,r})`.

`|T| = 2L + L + Σ_C 2ℓ_C(ℓ_C − 1) ≤ 9m + 12m`.

*Proof.*  Let `M'` be a perfect matching.  The elements `a_{v,j}`, `b_{v,j}` occur only in the true and
false triples of `v`.  If `M'` contains the true triple of `(v,j)`, then `a_{v,j+1}` cannot be covered by
the false triple of `(v,j)`, which contains `b_{v,j}`, so `M'` contains the true triple of `(v,j+1)`; if it
contains the false triple of `(v,j)`, then `b_{v,j+1}` cannot be covered by its true triple, which contains
`a_{v,j+1}`, so `M'` contains the false triple of `(v,j+1)`.  Hence `M'` contains all true triples of `v`
(put `v` = true; exactly the tips `p_{v,j}` are left uncovered by them) or all false triples (put `v` =
false; the tips `n_{v,j}` are left).  The element `c¹_C` is covered by a triple `(t_s, c¹_C, c²_C)`, whose
tip is not covered by a variable triple: if the occurrence is positive, `t_s = p_s` is left, so `v` is
true; if it is negated, `t_s = n_s` is left, so `v` is false.  Every clause has a true literal.
Conversely, from a satisfying assignment take the true triples of the true variables and the false
triples of the false ones; for every slot exactly one tip is left, and it is `t_s` iff the occurrence is
true.  For every clause choose a true slot and take its triple `(t_s, c¹_C, c²_C)`; the left tips of its
other `ℓ_C − 1` slots are matched with its `ℓ_C − 1` garbage pairs.  Every element is covered exactly
once.  ∎

**Lemma A2 [K (Garey–Johnson, Theorem 4.3), with a proof; X].**  From a 3DM instance with
`W = {w_1,…,w_q}`, `X = {x_1,…,x_q}`, `Y = {y_1,…,y_q}` and triple set `T`, every element lying in at least
one triple, one can compute in polynomial time an instance of EXACT BIN PACKING (in fact of 4-PARTITION)
with `4|T|` items, `|T|` bins and `B = 40r⁴ + 15`, `r = 32q`, that has a solution iff the 3DM instance has
a perfect matching.

*Construction.*  Let `N(z)` be the number of triples containing `z`.  Items: for every element `z` the
copies `z[1],…,z[N(z)]` (`z[1]` *actual*, the others *dummy*), and one item `u_t` per triple.  Sizes:

```
w_i[1] : 10r⁴ + i·r  + 1        w_i[l], l ≥ 2 : 11r⁴ + i·r  + 1
x_j[1] : 10r⁴ + j·r² + 2        x_j[l], l ≥ 2 : 11r⁴ + j·r² + 2
y_k[1] : 10r⁴ + k·r³ + 4        y_k[l], l ≥ 2 :  8r⁴ + k·r³ + 4
u_t, t = (w_i, x_j, y_k) : 10r⁴ − k·r³ − j·r² − i·r + 8.
```

The sizes sum to `|T|·B`, and each lies strictly between `B/5` and `B/3`.

*Proof.*  Each bin of an exact packing contains exactly four items.  Their sizes are congruent to `1`,
`2`, `4` or `8` modulo `r` according to the type (`w`, `x`, `y`, `u`), and four such residues add up to
`15` modulo `r ≥ 32` only if they are `1, 2, 4, 8`: one item of each type.  For `u_t` with
`t = (w_i,x_j,y_k)` and copies of `w_{i'}`, `x_{j'}`, `y_{k'}` the total is
`(10 + α)r⁴ + (k'−k)r³ + (j'−j)r² + (i'−i)r + 15` with `α` the sum of the leading coefficients of the three
copies; it equals `B` iff `i' = i`, `j' = j`, `k' = k` (reduce modulo `r²`, `r³`, `r⁴` in turn, using
`|i'−i|, |j'−j|, |k'−k| < r`) and `α = 30`, i.e. the copies are all actual (`10+10+10`) or all dummy
(`11+11+8`); the mixed sums are `28, 29, 31, 32`.  So every bin is `u_t` with copies of the three elements
of `t`, all actual or all dummy.  The triples whose bin is actual form a perfect matching, because every
element has exactly one actual copy.  Conversely, for a perfect matching `M'` give `u_t`, `t ∈ M'`, the
three actual copies, and distribute the `N(z) − 1` dummy copies of each `z` among the `N(z) − 1` triples
of `T ∖ M'` that contain it.  ∎

Both lemmas are tested against exhaustive search by `experiments/complexity/strands/test_eth_chain.py`.  The
arithmetic of Lemma A2 — the four-element property, its converse, and the bounds `B/5 < size < B/3` — is
machine-checked: `experiments/complexity/lean/FourPartition.lean` (`four_sum`, `sum_good`, `size_bounds`;
register CX-V4).
