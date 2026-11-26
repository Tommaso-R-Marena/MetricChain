# The magnified partition function of interacting strands without enumerating strand orderings

Working paper of the complexity division, first version 2026-11-26.  Register: `THEOREMS.md` CX-T10–CX-T12.
Problem: `OPEN_PROBLEMS.md` A6 — Shalaby and Woods, arXiv:2611.27945v2 (cited [SW26]), "Future work" 3
and 4:

> "3. Checking all cyclic permutations of c strands yields the (c − 1)! factor in the multi-stranded
> running times in Table 1. Boehmer, Berkemer, Will, and Ponty [3] reduce that to 3^c, but for the simple
> BPM model. Can we make such improvements in the nearest neighbour model?
> 4. Can we increase the number of strands c beyond O(1) and still have a polynomial time partition
> function or MFE algorithm? […]"

## 0. Result and what is new in it

**Theorem 1** [P; validated [X] on 280 systems].  For a multiset of strands with `k` species of lengths
`ℓ_1,…,ℓ_k` and multiplicities `n_1,…,n_k` (`c = Σ n_i` strands, `L_0 = Σ ℓ_i`), the `α`-magnified partition
function of the multi-stranded nearest-neighbour model — connected unpseudoknotted structures over **all**
circular orderings, indistinguishable strands, rotational-symmetry term included — is computed with

```
O( L_0^4 · Σ_{d | gcd(n_1,…,n_k)}  Π_i C(n_i/d + 2, 2) )      arithmetic operations
```

(for loop-energy functions with general interior loops and affine multiloops; unit-cost arithmetic as in
[SW26]).  This is `O(N^4 · 3^c)` when all strands are distinct, against `O(N^3 (c−1)!)` in [SW26], and it is
**polynomial in `c` for every fixed number of species** (`O(N^4 c^{2k})`).  By the decoding of [SW26, §7]
([K], not re-derived here) the same bounds hold for the minimum free energy and for the density of
states, since those are obtained from one value `Q_α` with `α = Θ(N)`.

What is and is not ours.  The idea of indexing dynamic-programming states by the *set* of strands
between two positions is Boehmer–Berkemer–Will–Ponty's (WABI 2024, Thm 14: `O(3^m n³)` for MFE in a
base-pair model without the symmetry term; their Remark 15 sketches a partition-function variant with
one partition function per symmetry value; their Thm 16 uses counts of equal strands for triplet
repeats).  The decomposition of the symmetric structures into "slices" with an inclusion–exclusion over
symmetry degrees, for a *fixed* ordering, is [SW26]'s.  Ours: (i) the closed formula (1) over all
orderings at once; (ii) the bijection of §3 that lets the symmetric structures be summed over all
orderings by a sub-multiset dynamic programme without overcounting; (iii) the resulting bound in the
number of species, in the full model, with a validated implementation.  We found no statement of this
in print; [SW26] poses it as an open question three days before this was written.

Together with `STRANDS_NN_HARDNESS.md` (NP-hardness for unboundedly many species): **in the
nearest-neighbour model the number of strands is not the parameter that makes multi-strand folding hard;
the number of species is.**  Bounded species: polynomial.  Unbounded species: NP-hard, even with one
long strand and homopolymers.

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
symmetry.  The magnified partition function is

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

For a chord of the boundary of `F` call *nest* the arc of the circle that it cuts off on the side away
from `F`, with everything inside.  The nests are disjoint, every nick lies in exactly one of them, and
`r` permutes them.  A period contains `k` nests, separated by the unpaired, nick-free stretches of `F`.

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

Consequently

```
F_d = Σ over tuples of   (|A| + 1) · W(F)^α · QB^{(dα)}(nest) · B^{dα} · TOP^{(dα)}(top segment) ,                  (2)
```

with the tables of §4 evaluated at magnification `dα`.

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

**Operation count.**  For a multiset `M'`, the split tables have `O(L_0² · #{A ≤ M'})` entries; an entry
costs `O(L_0 ℓ_max)` for the terms inside `s` and `t` plus `O(L_0 ℓ_max · #{A' ≤ A})` for the terms that
split `A`; summing, `O(L_0^4 · #{(A',A) : A' ≤ A ≤ M'})`, and `#{A' ≤ A ≤ M'} = Π_i C(n'_i + 2, 2)`.

## 5. Validation

`test_multiset_dp.py`, `test_multiset_dp_random.py`: for 20 hand-chosen and 260 random systems (up to 6
strands, up to 16 bases, 1–3 species, two different rational weight models), `Q_α` for `α = 0,1,2,3` from
the dynamic programme equals, as exact rational numbers, the sum over the physical ensemble obtained by
enumerating all labelled structures over all orderings and forming orbits under permutations of equal
strands (`ref_enum.py`).  119 of the random systems have rotationally symmetric structures; among the
hand-chosen ones symmetry orders 2, 3, 4, 5, 6 occur.  Timing of the unoptimised Python:
`(GGC)×6 + (GCC)×6` (12 strands) in 0.5 s.

This validates formula (1), the bijection (2) and the recursions together; it is not a proof.  The
proofs above are paper proofs, unreviewed.

## 6. Remarks, limits, open ends

1. *From `3^c` to `2^c`.*  The sums over `A_L + A_R` are subset convolutions; in the ring of reals they
   can be done in `O(2^c c²)` instead of `3^c` (fast subset convolution), giving `O*(2^c)` for distinct
   strands.  Not implemented; stated as a remark, not a theorem.
2. *Lower bound.*  By `STRANDS_NN_HARDNESS.md` the problem is NP-hard for unboundedly many species.  A
   bound `2^{o(c)}` under ETH holds conditionally on two cited facts (CX-T14).  Whether the problem is fixed-parameter
   tractable in the number of species `k` (our bound is `c^{O(k)}`) is open (`OPEN_PROBLEMS.md` C2).
3. *MFE and density of states.*  We rely on [SW26, §7] for the decoding of `Q_α`; we have read the
   statements (their Theorems 2, 3 and Lemma 39), not checked the proofs, and the decoding needs
   `α = Θ(N)` and therefore arithmetic on numbers with `Θ(N²)` bits, which the unit-cost model hides.
4. *Model.*  Dangles, coaxial stacking and other context-dependent exterior-loop terms are not covered.
5. The interior-loop term is `O(N^4)` as in the classical algorithms; the usual restrictions bring it to
   `O(N^3)`.
