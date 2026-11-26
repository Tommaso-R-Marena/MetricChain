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

## Statements established by exact computation only

| id | statement | label | program |
|---|---|---|---|
| CX-X1 | The NANUQ metric of a network depends only on the circular split system `Split(T(N))`; for arbitrary circular split systems on 6 points it can fail to be Kalmanson (33 systems; 3 of them unions of binary-tree split systems) | [X] | `experiments/complexity/nanuq/exhaust_all_systems.py`, `exhaust_tree_generated.py` |
| CX-X2 | For every outer-labeled planar galled bloblet with `k` hybrids and `n` leaves, `(k,n)` ∈ {1,2}×{4..7}, {3}×{4..8}, {4}×{4..8}, {5}×{5,6,7}, {6}×{6,7}: the NANUQ metric is circular decomposable with support exactly the displayed splits | [X] | `experiments/complexity/nanuq/test_bloblets.py` (generator `networks.py`) |

## Conjectures

| id | statement | evidence |
|---|---|---|
| CX-C1 | Under ETH there is no `2^{o(c)}·poly(N)` algorithm for MFE in the models of CX-T2 (`c` = number of strands) | follows from CX-T1 **if** 4-PARTITION with polynomially bounded numbers has no `2^{o(n)}` algorithm under ETH; that chain is not verified |
