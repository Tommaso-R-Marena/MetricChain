# Theorem register (complexity division)

Labels as in `README.md`.  "Review" names the COMPLEXITY-REV file of the independent adversarial review
(internal; not academic peer review).  A statement without a review entry is **unreviewed**.

| id | statement (short) | label | where | verification | review | prior art checked |
|---|---|---|---|---|---|---|
| CX-T1 | For every NN loop-energy function with exterior loops `0`, the `GG/CC` stack `< 0` and bulge/interior/multi loops `≥ 0`: the MFE of the system `I(a,m,B)` (one template `G^B(AG^B)^{m−1}`, items `C^{a_i}`) equals `σM + nΔG_assoc` iff the exact bin-packing instance is solvable, and is `≥ σ(M−1) + nΔG_assoc` otherwise; minimum-energy structures are exactly the tiling structures | [P] | `STRANDS_NN_HARDNESS.md` Thm 1 | [X] exhaustive enumeration, `experiments/complexity/strands/test_partition_reduction*.py` (`m ≤ 3`, `B ≤ 5`) | unreviewed (review commissioned) | `PRIOR_ART.md` §A searches 1–4: no proof of NN-model hardness for many strands found |
| CX-T2 | Hence dMFE in the multi-stranded unpseudoknotted NN model (connected structures, association and symmetry terms included) is strongly NP-hard for every such fixed energy function, even for one strand over `{G,A}` plus homopolymer strands | [P] | ibid. Cor. 2 | as CX-T1 | unreviewed | as CX-T1 |
| CX-T3 | Number of minimum-energy structures of `I(a,m,B)`: `Til(a,m,B)` (labelled), `Til/Π μ_s!` (physical ensemble) | [P] | ibid. Thm 3 | [X] labelled count checked in the same enumeration | unreviewed | — |
| CX-T4 | `#SSEL` is #P-hard in the same models; the partition function of the stack-only model with the temperature as input is #P-hard | [P] | ibid. Cor. 4 | — | unreviewed | uses Ducloz–Shalaby–Woods Lemma 31 and Thm 22 [K] |

## Statements established by exact computation only

| id | statement | label | program |
|---|---|---|---|
| CX-X1 | The NANUQ metric of a network depends only on the circular split system `Split(T(N))`; for arbitrary circular split systems on 6 points it can fail to be Kalmanson (33 systems; 3 of them unions of binary-tree split systems) | [X] | `experiments/complexity/nanuq/exhaust_all_systems.py`, `exhaust_tree_generated.py` |
| CX-X2 | For every outer-labeled planar galled bloblet with `k` hybrids and `n` leaves, `(k,n)` ∈ {1,2}×{4..7}, {3}×{4..8}, {4}×{4..8}, {5}×{5,6,7}, {6}×{6,7}: the NANUQ metric is circular decomposable with support exactly the displayed splits | [X] | `experiments/complexity/nanuq/test_bloblets.py` (generator `networks.py`) |

## Conjectures

| id | statement | evidence |
|---|---|---|
| CX-C1 | Under ETH there is no `2^{o(c)}·poly(N)` algorithm for MFE in the models of CX-T2 (`c` = number of strands) | follows from CX-T1 **if** 4-PARTITION with polynomially bounded numbers has no `2^{o(n)}` algorithm under ETH; that chain is not verified |
