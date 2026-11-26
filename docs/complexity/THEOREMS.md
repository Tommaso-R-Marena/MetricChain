# Theorem register (complexity division)

Labels as in `README.md`.  "Review" names the COMPLEXITY-REV file of the independent adversarial review
(internal; not academic peer review).  A statement without a review entry is **unreviewed**.

| id | statement (short) | label | where | verification | review | prior art checked |
|---|---|---|---|---|---|---|
| CX-T1 | For every NN loop-energy function with exterior loops `0`, the `GG/CC` stack `< 0` and bulge/interior/multi loops `≥ 0`: the MFE of the system `I(a,m,B)` (one template `G^B(AG^B)^{m−1}`, items `C^{a_i}`) equals `σM + nΔG_assoc` iff the exact bin-packing instance is solvable, and is `≥ σ(M−1) + nΔG_assoc` otherwise; minimum-energy structures are exactly the tiling structures | [P] | `STRANDS_NN_HARDNESS.md` Thm 1 | [X] exhaustive enumeration, `experiments/complexity/strands/test_partition_reduction*.py` (`m ≤ 3`, `B ≤ 5`) | unreviewed (review commissioned) | `PRIOR_ART.md` §A searches 1–4: no proof of NN-model hardness for many strands found |
| CX-T2 | Hence dMFE in the multi-stranded unpseudoknotted NN model (connected structures, association and symmetry terms included) is strongly NP-hard for every such fixed energy function, even for one strand over `{G,A}` plus homopolymer strands | [P] | ibid. Cor. 2 | as CX-T1 | unreviewed | as CX-T1 |
| CX-T3 | Number of minimum-energy structures of `I(a,m,B)`: `Til(a,m,B)` (labelled), `Til/Π μ_s!` (physical ensemble) | [P] | ibid. Thm 3 | [X] labelled count checked in the same enumeration | unreviewed | — |
| CX-T4 | `#SSEL` is #P-hard in the same models; the partition function of the stack-only model with the temperature as input is #P-hard | [P] | ibid. Cor. 4 | — | unreviewed | uses Ducloz–Shalaby–Woods Lemma 31 and Thm 22 [K] |

| CX-T5 | **Local criterion.** The split weights of the NANUQ metric of a tree-generated circular split system are sums of terms on ≤ 6 leaves (`α/2 = Φ4 + ΣΦ5 + ΣΦ6`); the 5-point terms are always non-negative; if the 6-point terms are non-negative and vanish for undisplayed splits, the metric is circular decomposable with support exactly the system | [P] + [X] (16 five-point systems) | `NANUQ_LOCAL_CRITERION.md` Prop. 2, Lemma 4, Thm 4 | `check_decomposition.py`, `five_point_facts.py` | unreviewed | network-free formulation not found in print; the third-party claim B-II mentions a "six-label reduction" (proof not seen) |
| CX-T6 | **All galled outer-labeled planar networks.** For every binary semi-directed outer-labeled planar galled network (any level, any number of blobs) the NANUQ metric is circular decomposable with support `Split(T(N))` — contains conjectures B1 and B2 of Holtgrefe et al. | [P] + [X] (102 systems of class 𝒜 on 6 leaves, 108 in the substitution closure) | ibid. Lemmas A, B, 7, 8, Thms 6′, 7 | `verify_class.py`, `characterize6.py`; direct tests `test_bloblets.py` (levels 1–6), `test_multiblob.py` (≤ 7 leaves) | unreviewed | **claimed earlier (2026-09-29) by an unreviewed third-party repository, `PRIOR_ART.md` B-II; derived here independently without access to that proof** |
| CX-T7 | **Galled cannot be dropped.** An explicit outer-labeled planar, level-2, non-galled bloblet `N*` on 7 leaves whose NANUQ metric is Kalmanson for none of the 360 circular orders (weight `−1` on a displayed split for the planar order); a family with weights → `−∞` | [X] | ibid. §6, Thm 9 | `counterexample7.py`, `verify_nongalled.py`, `verify_nongalled2.py` (independent code path `netcalc.py`) | unreviewed | `PRIOR_ART.md` §B search 2: no non-galled example found |
| CX-T8 | **Sharpness.** Of the 150 tree-generated systems on 6 points, 141 are globally good, 127 satisfy the local criterion, 108 come from galled planar networks; each of the 23 excluded systems fails itself or after replacing leaves by small clades; the class defined by the criterion is the largest class closed under restriction and cherry substitution on which the statement holds | [X] + [P] | ibid. §7, Thm 10 | `characterize6.py` | unreviewed | — |
| CX-T9 | **Union property.** In class 𝒜 (planar trees with twin leaves): two displayed splits cutting `{z,w}` off from `a_1a_2a_3` and from `a_2a_3a_4` imply one cutting it off from all four; equivalently `Φ6 ≥ 0`, with a proof that needs no computer | [P] | ibid. Lemma 5, Prop. 6 | consistent with `characterize6.py` | unreviewed | — |

| CX-T10 | **Orbit formula.** `Σ_{physical S} w(S)^α R(S)^{−α} = (1/c) Σ_{d | gcd(n_i)} J_{1−α}(d) F_d`, `F_d` = magnified sum over rooted circular arrangements with a structure fixed by the rotation of order `d`, `J` = Jordan totient with exponent `1−α` | [P] | `STRANDS_ALGORITHM.md` Lemma 2 | [X] `test_multiset_dp*.py` (through CX-T12) | unreviewed | the per-ordering inclusion–exclusion is [SW26] Lemma 19; closed form over all orderings not found in print |
| CX-T11 | **Fixed structures.** A structure fixed by a rotation of order `d ≥ 2` has a unique fixed face, without nick, with `kd` pairs; bijection (designated nest, marked nick, top segment) | [P] | ibid. Lemma 3, Prop. 4 | as CX-T10 | unreviewed | "central loop"/slices in [SW26] for a fixed ordering |
| CX-T12 | **Algorithm.** Magnified partition function of the multi-strand NN model over all orderings, with symmetry, in `O(L_0^4 Σ_{d} Π_i C(n_i/d+2,2))` arithmetic operations: `O(N^4 3^c)` for distinct strands, polynomial for a bounded number of species; MFE and #SSEL within the same bounds via [SW26, §7] [K] | [P] | ibid. Thm 1 | [X] exact agreement with exhaustive enumeration on 280 systems | unreviewed | answers "Future work" 3 of [SW26] (posed 23 Nov 2026) and part of 4; subset DP for a base-pair model without symmetry is Boehmer et al. (WABI 2024) |

## Machine-checked (Lean 4.31.0 + Mathlib v4.31.0; files under `experiments/complexity/lean/`, see its README)

| id | declaration | statement | covers |
|---|---|---|---|
| CX-V1 | `Complexity.StackPacking.packing_of_all_stacked`, `Complexity.StackPacking.exact_packing_of_all_stacked` | **[V]** If every base of every item is paired with a `G` of the template `G^B(AG^B)^{m−1}`, injectively, and consecutive bases of an item with adjacent positions, the items can be assigned to the `m` blocks with total length `≤ B` per block; `= B` if the lengths sum to `mB` | the counting step (d) of CX-T1 — **not** the model of structures and loops around it |
| CX-V2 | `Complexity.JordanOrbit.weighted_fixed_point_formula` (with `sum_jordan`, `fix_iff_dvd_stab`, `stab_eq`) | **[V]** For a permutation `ρ` of a finite set with `ρ^c = 1`, `g : X → ℚ`, `k ∈ ℤ`: `Σ_x R(x)^k g(x) = Σ_{d∣c} J_k(d) Σ_{x : ρ^{c/d}x=x} g(x)` | the second equality of formula (1) in CX-T10 — **not** the identification of physical structures with orbits |

## Statements established by exact computation only

| id | statement | label | program |
|---|---|---|---|
| CX-X1 | The NANUQ metric of a network depends only on the circular split system `Split(T(N))`; for arbitrary circular split systems on 6 points it can fail to be Kalmanson (33 systems; 3 of them unions of binary-tree split systems) | [X] | `experiments/complexity/nanuq/exhaust_all_systems.py`, `exhaust_tree_generated.py` |
| CX-X2 | For every outer-labeled planar galled bloblet with `k` hybrids and `n` leaves, `(k,n)` ∈ {1,2}×{4..7}, {3}×{4..8}, {4}×{4..8}, {5}×{5,6,7}, {6}×{6,7}: the NANUQ metric is circular decomposable with support exactly the displayed splits | [X] | `experiments/complexity/nanuq/test_bloblets.py` (generator `networks.py`) |

## Conjectures

| id | statement | evidence |
|---|---|---|
| CX-C1 | Under ETH there is no `2^{o(c)}·poly(N)` algorithm for MFE in the models of CX-T2 (`c` = number of strands) | follows from CX-T1 **if** 4-PARTITION with polynomially bounded numbers has no `2^{o(n)}` algorithm under ETH; that chain is not verified |
