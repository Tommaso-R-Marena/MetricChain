# The magnified partition function of interacting strands without enumerating strand orderings

Working paper of the complexity division, first version 2026-11-26; **revised 2026-11-26 after the internal
adversarial review `COMPLEXITY-REV-0003`** (what changed: §7; internal AI review, not peer review).
Register: `THEOREMS.md` CX-T10–CX-T12, CX-T30.
Problem: `OPEN_PROBLEMS.md` A6 — Shalaby and Woods, arXiv:2611.27945v2 (cited [SW26]), "Future work" 3
and 4:

> "3. Checking all cyclic permutations of c strands yields the (c − 1)! factor in the multi-stranded
> running times in Table 1. Boehmer, Berkemer, Will, and Ponty [3] reduce that to 3^c, but for the simple
> BPM model. Can we make such improvements in the nearest neighbour model?
> 4. Can we increase the number of strands c beyond O(1) and still have a polynomial time partition
> function or MFE algorithm? […]"

## 0. Result and what is new in it

**Theorem 1** [P; validated [X]: 280 systems by us, about 740 by the referee].  For a multiset of strands with
`k` species of lengths `ℓ_1,…,ℓ_k` and multiplicities `n_1,…,n_k` (`c = Σ n_i` strands, `L_0 = Σ ℓ_i`), the
`α`-magnified partition function of the multi-stranded nearest-neighbour model — connected unpseudoknotted
structures over **all** circular orderings, indistinguishable strands, rotational-symmetry term included —
is computed with

```
O( L_0^4 · Σ_{d | gcd(n_1,…,n_k)}  Π_i C(n_i/d + 2, 2) )      arithmetic operations
```

(for loop-energy functions with general interior loops and affine multiloops; unit-cost arithmetic as in
[SW26]).  This is `O(N^4 · 3^c)` when all strands are distinct, against `O(N^3 (c−1)!)` in [SW26], and it is
**polynomial in `c` for every fixed number of species** (`O(N^4 c^{2k})`).  For loop energies that are integer
multiples of a unit, the **minimum free energy and the number of structures at every energy level,
separately for every degree of symmetry**, are obtained within the same operation count from one
evaluation (Proposition 5); the numbers involved have `O(cN²)` bits.

**What is and is not ours** (rewritten after the review; the first version of this paragraph was wrong —
REV-0003, finding 1).

* *In print for the base-pair model.*  Boehmer, Berkemer, Will and Ponty, journal version (Algorithms Mol.
  Biol. 21:4, first published December 2025; this is the version [SW26] cite as [3]), section "Translation
  to partition function": partition functions `Z_r` of the `r`-symmetric structures "without iterating over
  all circular permutations"; a bijection (their Lemma 12) between `r`-symmetric structures and structures
  with one *marked base pair* on the strand set in which every sequence occurs `r` times less often, the
  energy multiplied by `r`; a recursion over symmetry degrees (Lemma 14); **Theorem 4: "The partition
  function Z over m strands can be computed in time O(3^m · n^3 · m^2)"**; Remark 3: the correction
  `kT log r` of Dirks et al. can be added; Remark 4: the technique carries over to their count-indexed
  algorithm for triplet repeats (Theorem 5, polynomial for a bounded number of different strands), and the
  problem is NP-complete for unboundedly many (Theorem 6).  We had read only the conference version (WABI
  2024: Theorem 14 for the minimum free energy, Remark 15 with a sketch, Theorem 16), and wrote that the
  closed treatment over all orderings was "not found in print".  It was in print, for the base-pair model.
  Our marked nick inside a designated nest (§3) and their marked base pair encode the same quotient
  construction.
* *In print for a fixed ordering in the nearest-neighbour model.*  The central loop of a symmetric
  structure (our Lemma 3) is Lemma 18 of Shalaby and Woods (ICALP 2025, arXiv:2407.09676); nests are
  [SW26] Definition 25 and Remark 26; the nest that crosses the border of a period, with its two cases, is
  [SW26] Lemma 31, Eqs. (39)–(40) and Algorithm 6.
* *What this note adds*, as far as the referee and we could find: the same programme **in the
  nearest-neighbour model over all orderings** — the central face charged as a multiloop
  `m_a^α (m_b^k m_c^u)^{dα}` or, for `d = 2` and one nest per period, as a two-pair loop; top levels without
  nicks; exterior loops summed over sub-multisets — for **arbitrary magnification `α`** with the closed
  formula (1); the operation count in terms of the multiplicities of the species; the decoding of minimum
  free energy and level counts per symmetry class with its bit cost; and a tested implementation.  [SW26]
  (version 2, 23 November 2026) lists exactly this as open ("Future work" 3, quoted above).  A failure to
  find it elsewhere is not evidence of novelty.

Together with `STRANDS_NN_HARDNESS.md` (NP-hardness for unboundedly many species): **in the
nearest-neighbour model the number of strands is not the parameter that makes multi-strand folding hard;
the number of species is.**  Bounded species: polynomial.  Unbounded species: NP-hard, even with one
long strand and homopolymers.  For the base-pair model of Boehmer et al. this dichotomy is their
Theorems 5 and 6.

## 1. Model

As in `STRANDS_NN_HARDNESS.md` §1, with loop weights `W(f) = e^{−g(f)/k_BT}` of the usual
dynamic-programming form:

* hairpin with `u` unpaired bases: `hp(u)` (it may also depend on the closing letters);
* a nick-free loop with two pairs and unpaired sides `l_1, l_2` (stack, bulge, interior): `il(l_1,l_2)`
  (it may depend on the letters; it must be a function of the loop, i.e. invariant under exchanging the
  roles of the two pairs);
* multiloop with `b` pairs and `u` unpaired bases: `m_a · m_b^b · m_c^u`;
* exterior loop: `1`.

For a structure `S`, `w(S) = Π_f W(f)`.  The physical ensemble `Ω̄` consists of the connected
unpseudoknotted structures with strands of equal sequence identified; `R(S)` is the degree of rotational
symmetry.  (Notation: in [SW26] the physical ensemble is `Ω` and `Ω̄` is the algorithmic one — the reverse
of ours.  The quantity below is their Definition 17; at `α = 1` it is Eqs. (2.2)–(2.3) of Dirks et al.; the
referee checked both identifications.)  The magnified partition function is

```
Q_α = e^{−α(c−1)ΔG_assoc/k_BT} · Σ_{S ∈ Ω̄} w(S)^α · R(S)^{−α} .
```

## 2. From orbits to fixed points

Let `𝒲` be the set of pairs `(Y,S)`: `Y = (Y_1,…,Y_c)` a sequence of species with `n_i` occurrences of
species `i`, read as a circular arrangement of strands with a marked first slot, and `S` a connected
non-crossing structure on the polymer graph of that arrangement.  The cyclic group `C_c = ⟨ρ⟩` acts by
shifting the slots.

**Lemma 2 [P].**  The physical structures are the orbits of `C_c` on `𝒲`, and `R(S)` is the order of the
stabiliser.  Hence, with `F_d = Σ_{(Y,S) : ρ^{c/d}(Y,S) = (Y,S)} w(S)^α`,

```
Σ_{S ∈ Ω̄} w(S)^α R(S)^{−α}  =  (1/c) Σ_{(Y,S) ∈ 𝒲} R^{1−α} w^α  =  (1/c) Σ_{d | gcd(n_i)} J_{1−α}(d) · F_d ,          (1)
```

where `J_k(d) = Σ_{e | d} μ(d/e) e^k` is Jordan's totient with exponent `k` (any real `k`).

*Proof.*  A connected unpseudoknotted structure of labelled strands has a unique circular ordering in
which it is non-crossing (Dirks et al. 2007, Thm 2.1, [K]).  Forgetting the labels and marking a first
strand maps it to `𝒲`; the `c` choices of the first strand give one `C_c`-orbit, and two labelled structures
have the same orbit iff they differ by a permutation of equal strands.  A rotation `ρ^j` fixes `(Y,S)` iff
it maps every strand to a strand of the same species and `S` to itself, which is the definition of a
rotational symmetry ([SW26] Def. 11).  The orbit of `(Y,S)` has `c/R` elements, which gives the first
equality.  The stabiliser is the subgroup of order `R`, so `ρ^{c/d}` fixes `(Y,S)` iff `d | R`; with
`Σ_{d | R} J_k(d) = R^k` (Möbius inversion) the second equality follows.  If `ρ^{c/d}` fixes `Y` then
`Y = y^d`, so `d | n_i` for all `i`.  ∎

At `α = 0` this is Burnside's lemma (`J_1 = φ`); at `α = 1` only `d = 1` survives (`J_0(d) = [d = 1]`) and
(1) is the division by the symmetry number of Dirks et al.; for general `α` it replaces the recursion
over symmetry degrees of [SW26, Lemma 19] by one line.

`F_1 = Σ_Y Z̃(Y)` is the sum over all sequences `Y` of the symmetry-naive partition function of the
circular arrangement `Y`.

## 3. The structures fixed by a rotation

Let `d ≥ 2`, `d | n_i`, `r = ρ^{c/d}`, `(Y,S)` fixed by `r`; so `Y = y^d` with `y` a sequence of `c/d` strands (a
*period*, `L` bases).

**Lemma 3 (central loop) [P].**  Exactly one face `F` of the polymer graph is mapped to itself by `r`.  Its
boundary contains no nick and `kd` chords, `k ≥ 1`.

*Proof.*  The faces and chords form a tree (faces as vertices, chords as edges).  `r` is an automorphism
of finite order of this tree, so it fixes a vertex or exchanges the two ends of an edge.  A chord mapped
to itself has its two ends exchanged by `r` (a non-trivial rotation fixes no base), so it joins a base to
its own image, which has the same letter: impossible.  So a face is fixed, and only one (two fixed faces
would fix the chords on the path between them).  `r` acts freely on the nicks and on the chords of the
boundary of `F`.  If a nick lay on it there would be at least `d ≥ 2`, and the structure would be
disconnected.  If no chord lay on it, `S` would be empty, and `c ≥ 2`.  ∎

Lemma 3 is known [K]: it is Lemma 18 of Shalaby–Woods (ICALP 2025), including the case `d = 2` in which the
central loop is a stack or an interior loop, and is quoted as Remark 29 in [SW26] (we checked both texts
after the review — finding 3).  Only the proof by the automorphism of the tree of faces is ours.

For a chord of the boundary of `F` call *nest* the arc of the circle that it cuts off on the side away
from `F`, with everything inside.  The nests are disjoint, every nick lies in exactly one of them, and
`r` permutes them.  A period contains `k` nests, separated by the unpaired, nick-free stretches of `F`.
("Nest" and "every nick lies in a nest" are Definition 25 and Remark 26 of [SW26]; the nest crossing the
border of a period, with the cases "one nest per slice" and "several", is their Lemma 31 for a fixed
ordering.  What Proposition 4 adds is the marked nick — the factor `|A| + 1` — which makes the sum over
all orderings exact, and the tables over multisets.)

**Proposition 4 (bijection) [P].**  For `d ≥ 2`, the pairs `(y, S)` — `y` a sequence of the period's strands,
`S` a `d`-fold symmetric connected non-crossing structure on `y^d` — are in bijection with the tuples
consisting of

* a *designated nest*: a pair `((s,i),(t,j))` of bases, where `(s,i)` is base `i` of a strand of species `s`
  and `(t,j)` base `j` of a strand of species `t`, with all strands of a multiset `A` between them in some
  order, and a structure inside it;
* one of the `|A| + 1` nicks inside the designated nest (the *marked nick*);
* a *top segment*: the rest of the period, from `(t,j+1)` to `(s,i−1)`, with a multiset `A_3` of strands in
  between in some order, carrying a structure whose top level is nick-free;

such that either (I) `s`, `t` are different strands of the period and `{s} + {t} + A + A_3` is the period, or
(II) `(s,i)` and `(t,j)` are bases of the same strand of the period in two consecutive periods, `j < i`,
`{s} + A` is the period and the top segment is `s[j+1..i−1]`.  The weight of `S` is

```
w(S)^α = W(F)^α · ( w(nest) · w(top) )^{dα} ,
```

where `F` is a multiloop with `kd` pairs and `d·u` unpaired bases (`u` = unpaired bases of the top segment at
top level), except when `d = 2` and `k = 1`, where `F` is a two-pair loop with sides `u, u`.

*Proof.*  Given `(y,S)`, the nick before the first strand of `y` lies in exactly one nest of the period;
this is the designated nest and that nick the marked nick.  Reading the period from the end of the
designated nest gives the top segment; its top level consists of the other `k − 1` nests of the period and
the unpaired bases of `F`, and contains no nick (Lemma 3).  If the two ends of the designated nest lie in
different strands of the period we are in case (I); otherwise the nest starts in a strand and ends in the
next copy of the same strand, case (II).  Conversely a tuple determines the circular arrangement of the
period (designated nest, then top segment), the structure on one period, hence on `y^d` by rotation, and
the marked nick determines where `y` starts; the designated nest of the result is the given one.  Every
loop other than `F` occurs `d` times.  ∎

Consequently `F_d` is the sum of the following terms, with the tables of §4 at magnification `γ = dα`
(this replaces the display (2) of the first version, which counted the factors `m_b`, `m_c` of the central
face twice when read literally — REV-0003, finding 4; the formulas below are the implemented ones):

```
case (I),  top segment (t,j+1; A_3; s,i−1), necessarily with a further nest:
      (|A| + 1) · QB^γ(s,i; A; t,j) · m_a^α · m_b^γ · QM^γ(t,j+1; A_3; s,i−1)
case (II), top segment s[j+1..i−1] with u = i−1−j bases, A = period − s:
   further nests in the top segment:   (|A| + 1) · QB^γ(s,i; A; s,j) · m_a^α · m_b^γ · QM^γ(s[j+1..i−1])
   no further nest, d ≥ 3:             (|A| + 1) · QB^γ(s,i; A; s,j) · m_a^α · m_b^γ · m_c^{γu}
   no further nest, d = 2:             (|A| + 1) · QB^γ(s,i; A; s,j) · il(u,u)^α                          (2)
```

`QB^γ` contains the loop closed by the nest's own pair on the side away from `F`; the central face is charged
once, with exponent `α`, as `m_a^α` times the `kd` branch factors `m_b^γ` (one written, `k − 1` inside `QM^γ`) and
the unpaired factors, or as the two-pair loop `il(u,u)^α`.

## 4. Tables indexed by sub-multisets

A *stretch* is either `s[i..j]` inside one strand, or `(s,i;A;t,j)`: the bases `s[i..ℓ_s]`, then all strands
of the multiset `A` **in every possible order** (summed), then `t[1..j]`.  At magnification `γ` (all loop
weights raised to `γ`) define for a stretch:

* `Q`: sum over structures on the stretch whose top level contains no nick (so the empty structure only
  inside one strand) and in which every loop has at most one nick; weight = product over the enclosed
  loops;
* `QB`: the same with the two end bases paired, including the loop closed by that pair;
* `QM`: as `Q` with at least one top-level pair and multiloop weights `m_b^γ` per top-level pair, `m_c^γ` per
  top-level unpaired base.

Recursions (the single-strand ones are McCaskill's; the others extend those of Dirks et al. by a sum
over the species of the strand in which a pair starts and over the sub-multisets on its two sides):

* `Q(s,i;A;t,j)`: by the rightmost top-level pair `(d,e)`; `e` lies in `t` (the unpaired tail must be
  nick-free) and `d` lies in `t` (`d ≥ 2`), in `s`, or in a strand `u ∈ A` at an index `d ≥ 2`, splitting
  `A − u = A_L + A_R`:
  `Σ_e [ Σ_{d∈t} Q(s,i;A;t,d−1)·QB(t[d..e]) + Σ_{d∈s} Q(s[i..d−1])·QB(s,d;A;t,e)
        + Σ_{u, A_L+A_R=A−u, d} Q(s,i;A_L;u,d−1)·QB(u,d;A_R;t,e) ]`.
* `QB(s,i;A;t,j)`: two-pair loops with inner pair `(d ∈ s, e ∈ t)`; multiloops (the inside has nick-free top
  level and at least two branches); and exterior loops — exactly one nick on the loop: either the nick
  after `s` (then `Q(s[i+1..ℓ_s])` times the sum over the first strand `u'` of the rest of
  `Q(u',1;A−u';t,j−1)`), or the nick after a strand `u ∈ A` (then `i < ℓ_s` and
  `Q(s,i+1;A_1;u,ℓ_u)` times the same kind of term for `A_2`, `A − u = A_1 + A_2`).
* `QM`: as `Q`, with the multiloop weights.

Then `F_1 = Σ_{s,t} Q(s,1; M−s−t; t,ℓ_t)` (`M` the full multiset; for `c = 1` the single-strand `Q`), and
`F_d` is (2) with `M/d`.  Exact formulas: `experiments/complexity/strands/multiset_dp.py`.

**Conventions and the tables not listed above** (added after the review, finding 4).
(a) *Multiloop interior* `QM2(s,i;A;t,j)`: the stretch strictly inside the pair `((s,i),(t,j))`, top level
without nick and with at least two branches; it is `0` if `i = ℓ_s` or `j = 1` (a nick would lie on the
loop); its recursion is that of `QM` with the term "no branch to the left" removed.  The multiloop term of
`QB` is `m_a^γ m_b^γ · QM2`.
(b) *Stretches that start at a strand boundary* (after the nick of an exterior loop): the strands of a
multiset `A'` in every order followed by `t[1..j']`, top level without nick; it is the single-strand `Q` if
`A'` is empty (equal to `1` for `j' = 0`), it is `0` if `A'` is non-empty and `j' = 0` (a second nick would lie on
the loop), and otherwise it is `Σ_{u ∈ A'} Q(u,1; A'−u; t,j')`.
(c) In the exterior-loop term of `QB` with the nick after a strand `u ∈ A`, the stretch from `(s,i+1)` to the
end of `u` must cover the nick after `s`; this requires `i < ℓ_s`.
(d) In `Q` and `QM` on a split stretch, the left end `d` of the rightmost top-level pair satisfies `d ≥ 2` when
it lies in `t` or in a strand of `A`: with `d = 1` the nick before that strand would lie on the top level.

**Why every pair (ordering, structure) is counted exactly once.**  A table entry for a stretch with a
multiset `A` is, by definition, a sum over the `|A|!/Π_u A_u!` orders `σ` of the strands of `A` and over the
structures on the resulting sequence.  For a fixed order the recursions are the classical ones (McCaskill
inside a strand; Dirks et al. across nicks): a structure with nick-free top level has a unique rightmost
top-level pair `(d,e)`; the loop closed by a pair is of exactly one of the kinds hairpin, two-pair loop,
multiloop, exterior loop; and in a connected structure an exterior loop contains exactly one nick, whose
position is determined.  The strand containing `d` (resp. the strand before the nick) is a strand `u` of
`A` at a definite place of the order, and `σ` is then the concatenation of an order `σ_L` of the strands to
its left, `u`, and an order `σ_R` of the strands to its right.  The map `σ ↦ (u, A_L, A_R, σ_L, σ_R)` is a
bijection between the orders of `A` and the tuples with `A_L + A_R = A − u`; summing the classical recursion
over `σ` and grouping by `(u, A_L, A_R)` gives the recursions above, with the two sub-sums being table
entries.  Two different species sequences in `A` give different `σ`; equal strands are not distinguished,
so each *sequence of species* is counted once, which is what `𝒲` requires.

**Operation count.**  For a multiset `M'`, the split tables have `O(L_0² · #{A ≤ M'})` entries; an entry
costs `O(L_0 ℓ_max)` for the terms inside `s` and `t` plus `O(L_0 ℓ_max · #{A' ≤ A})` for the terms that
split `A`; summing, `O(L_0^4 · #{(A',A) : A' ≤ A ≤ M'})`, and `#{A' ≤ A ≤ M'} = Π_i C(n'_i + 2, 2)`.

## 4a. Minimum free energy and level counts

The first version claimed these "by the decoding of [SW26, §7]".  That citation does not apply
(REV-0003, finding 2): [SW26] decode one ordering at a time (their Algorithm 4 loops over the orderings;
Lemma 39 and Theorem 41 are for a fixed ordering), the multiset algorithm never computes a single
ordering, and the free energy contains `k_BT ln R`, so levels of different symmetry classes are not
separated by the energy unit and cannot be read off the single number `Q_α`.  The conclusion is
nevertheless true; the argument below is the referee's, checked and implemented by us.

**Proposition 5 [P; X].**  Suppose every loop energy is an integer multiple of `ε`, of absolute value at most
`Gε`.  Let `g = gcd(n_1,…,n_k)`, `K = ⌈N log_2 24⌉ + 1`, and evaluate the sums `F_d`, `d | g`, with the loop
weights `2^{−K·g(f)/ε}` (magnification `α = K ε^{-1} k_BT ln 2 = Θ(N)`, with the constant `ln 24`).  Then for
every `R | g`

```
T_R  :=  Σ_{d : R | d | g}  μ(d/R) · F_d   =   Σ_m  N_R(m) · 2^{−Km} ,
```

where `N_R(m)` is the number of pairs `(Y,S) ∈ 𝒲` with symmetry exactly `R` and loop energy `mε`; `0 ≤ N_R(m) <
2^K`, so the `N_R(m)` are the digits of `T_R` in base `2^K`; the number of **physical** structures with
symmetry `R` and loop energy `mε` is `N_R(m)·R/c`; and

```
MFE  =  min { mε + k_BT ln R  :  R | g,  N_R(m) > 0 }  +  (c − 1) ΔG_assoc .
```

All numbers have `O(cGN²)` bits; the number of arithmetic operations is that of Theorem 1.

*Proof.*  `F_d` is the sum of `w(S)` over the pairs whose symmetry is a multiple of `d` (Lemma 2), so the
first equality is Möbius inversion on the divisors of `g`.  The number of pairs `(Y,S)` is at most
`8^N · 3^N = 24^N < 2^K` (a letter string with nick positions, times the non-crossing matchings on `N`
points), which bounds every `N_R(m)`.  A physical structure with symmetry `R` is an orbit of `c/R` pairs
(Lemma 2).  Its free energy is `mε + (c−1)ΔG_assoc + k_BT ln R`.  The exponents `m` lie in `[−GN, GN]` and the
tables for `F_d` use the weights to the power `d ≤ c`.  ∎

So `α = Θ(N)` is `α = (N log_2 24 + O(1)) · ε^{-1} k_BT ln 2`; the unit-cost count hides a factor
`Õ(cGN²)` in bit operations.  A symmetry-naive `(min,+)` version of the recursion does **not** give the
minimum free energy: it returns `min_d (m_d + k_BT ln d)`, with `m_d` the least energy among structures whose
symmetry is a *multiple* of `d`, which lies below the true value whenever the loop-energy minimiser is
symmetric (this is the difficulty that Shalaby and Woods handle by backtracking in their ICALP paper).

`level_counts.py` implements Proposition 5 with exact integers and compares the table `(R, m) ↦` number of
physical structures with exhaustive enumeration on 17 systems (symmetry degrees 2, 3, 4, 5, 6): all
agree; in 11 of them the symmetry-naive value is below the true minimum.

## 5. Validation

`test_multiset_dp.py`, `test_multiset_dp_random.py`: for 20 hand-chosen and 260 random systems (up to 6
strands, up to 16 bases, 1–3 species, two different rational weight models), `Q_α` for `α = 0,1,2,3` from
the dynamic programme equals, as exact rational numbers, the sum over the physical ensemble obtained by
enumerating all labelled structures over all orderings and forming orbits under permutations of equal
strands (`ref_enum.py`).  119 of the random systems have rotationally symmetric structures; among the
hand-chosen ones symmetry orders 2, 3, 4, 5, 6 occur.  Timing of the unoptimised Python:
`(GGC)×6 + (GCC)×6` (12 strands) in 0.5 s.

This validates formula (1), the bijection (2) and the recursions together; it is not a proof.

**Scope of our tests, and the referee's** (REV-0003, finding 5).  Our 280 systems have `N ≤ 16`, at most six
strands, gcd of the multiplicities at most 3 for several species, and weights that depend on loop sizes
only; `multiset_dp.py` does not implement letter-dependent weights, which Theorem 1 allows.  The referee
closed this gap with programs written from the definitions (`experiments/complexity/reviews/
rev3_strands_algorithm/`): an own enumerator and a C++ version of it; our dynamic programme against them
on about 740 system runs (2–10 identical copies; 2–4 species with gcd 2, 3, 4, 5, 6; palindromes;
hairpin-forming and length-one strands; `α ∈ {−2,…,5, 40}`, and non-integer `α` to `8·10⁻¹⁵`), about 17 800
comparisons of `Q_α`, `F_1` and every `F_d`, no mismatch; and an own implementation of the algorithm with
letter-dependent hairpin and two-pair weights, including the central two-pair loop, against brute force
(about 5 600 comparisons, no mismatch).  After the review: `test_multiset_dp_edges.py` (species must be
pairwise different — the first version silently returned a wrong value for duplicated species; a minimum
hairpin size as a pairing constraint, tested for `α = 0, 1, 2, −1`; weight `0` is refused at magnification
`≤ 0`, where it was counted as `1`), and `level_counts.py` (Proposition 5).

The proofs are paper proofs with one internal review.

## 6. Remarks, limits, open ends

1. *From `3^c` to `2^c`.*  The sums over `A_L + A_R` are subset convolutions; in the ring of reals they
   can be done in `O(2^c c²)` instead of `3^c` (fast subset convolution), giving `O*(2^c)` for distinct
   strands.  Not implemented; stated as a remark, not a theorem.
2. *Lower bound.*  By `STRANDS_NN_HARDNESS.md` the problem is NP-hard for unboundedly many species.  A
   bound `2^{o(c)}` under ETH holds (CX-T14; since Appendix A of the hardness note the only cited ingredient is
   the sparsification lemma).  Whether the problem is fixed-parameter
   tractable in the number of species `k` (our bound is `c^{O(k)}`) is open (`OPEN_PROBLEMS.md` C2).
3. *MFE and density of states.*  See §4a (Proposition 5): per symmetry class, from the `F_d` at one
   magnification, with numbers of `O(cGN²)` bits.  The coefficients `J_{1−α}(d)` of formula (1) are negative
   for `α > 1`, so `Q_α` itself is an alternating sum of large terms; Proposition 5 uses the `F_d` directly and
   exact arithmetic, not floating point.
4. *Model.*  Dangles, coaxial stacking and other context-dependent exterior-loop terms are not covered.
5. *Where `L_0^4` comes from.*  Not from the interior loops alone, as the first version said (REV-0003,
   finding 6): the tables `Q`, `QM` are decomposed by the rightmost top-level pair with both ends free, which
   costs `Θ(ℓ_t L_0)` per entry whatever the loop model (on one poly-A strand of length 16 / 32 / 64 the
   single-strand table alone makes 3 060 / 46 376 / 720 720 pair tests, about `ℓ⁴/24` — the referee's
   count).  Last-base recursions (`Q(…;t,j) = Q(…;t,j−1) + Σ_d …`) together with the usual treatment of
   interior loops would give `L_0^3`; not implemented.  The stated bound holds: in the referee's 33
   instrumented runs (up to 64 copies of one strand, 16 + 16 copies of two, eight distinct strands) the
   number of pair tests and multiset splits stayed below `0.58` times the bound.

## 7. Changes after the review COMPLEXITY-REV-0003

| finding | change |
|---|---|
| 1 (major): the novelty paragraph was wrong as worded — the journal version of Boehmer et al. has an exact partition function over all orderings with rotational symmetries for the base-pair model | §0 "What is and is not ours" rewritten after reading that section of the journal version (their Lemmas 8–14, Theorem 4, Remarks 3–4, Theorems 5–6); registers CX-T10–T12, `PRIOR_ART.md` A-III, `OPEN_PROBLEMS.md` A6 |
| 2 (major): the clause on minimum free energy and level counts was not proved; the cited decoding is per ordering | §4a, Proposition 5 (the referee's argument: Möbius inversion per symmetry class, digits in base `2^K`), with the bit cost; implemented and tested (`level_counts.py`); the `(min,+)` alternative withdrawn here and in the hardness note |
| 3: Lemma 3 and the nests are Shalaby–Woods' | attributions at Lemma 3 and before Proposition 4, both texts checked |
| 4: formula (2) misprinted; recursions incomplete and unproved | formula (2) replaced by the implemented cases; conventions and the missing table in §4; the uniqueness argument |
| 5: validation narrower than the statement; implementation edges | scope paragraph in §5; `multiset_dp.py` refuses duplicated species and weight 0 at magnification ≤ 0, and has a minimum hairpin size as a pairing constraint; `test_multiset_dp_edges.py` |
| 6: Remark 5 on the source of `L_0^4` was wrong | Remark 5 rewritten; `ASSUMPTION_AUDIT.md` §2 |
| 7: notation `Ω̄`; a stale remark; the constant in `α = Θ(N)` | §1; Remark 2; Proposition 5 |
