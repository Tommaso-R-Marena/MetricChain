---

## 2. Monopoles: what makes the truth larger, the law in the distance, and what an ideal certificate would need (step 2 of the brief)

### 2.1 Is the truth larger because of a monopole?  Yes — through the displacement of the charged group, not through its far field [M; H for the reading]

Three measurements on the enumerated instances (§1): (i) for lysine 95–101 % of the true
anchored constants are carried by class pairs that involve an ammonium group, 42–45 % by the
class of pairs of ammonium atoms alone (within one head group or between two), all
with one sign — the sum of the absolute class shares is 1.03–1.11 times the truth; (ii) a bound
that ignores signs loses only a factor 3–7; (iii) per subset the truth is 12–22 times serine's at
the same place.  This is what a monopole does: the self-energy `−κQ²/2B` of a group with net
charge has nothing to cancel against.  (Part of the factor is the length of the side chain and
not its charge [H]: at twelve residues the third-order sums of §2.3 are 0.98 (Ser₁₂), 4.3 (Leu₁₂),
18 ((LKSE)₃) and 20 (Lys₁₂) `k_BT` — leucine, a long neutral side chain with only two rotamers in
P2's domain, is four times serine; lysine another five times leucine.)

But the far field of a charged group is *not* special.  `p8_06_distance.py` evaluates, for the
twelve-residue peptides, the own solvation energy `E_A = Σ_{p≤q∈A} t_pq` of every rigid group `A`
(per residue: the fixed backbone part, the head, the aliphatic chain, or the neutral side chain)
with `A`'s own site **at the anchor**, and its exact response to changes at other sites:
`R1[A, j] = max_y |E_A(x⁰; j → y) − E_A(x⁰)|` and the three-body response
`R2[A; j, k] = max |Δ_{jk} E_A|` (only Born radii of `A` change; no energy evaluation of the whole
peptide is needed).

<!--T:T9-->

*Reading* [M].  With the group held in place, the response of an ammonium head to another site
is of the same size as that of a neutral backbone group at the same distance (Lys₁₂: medians
0.028 against 0.011 kcal/mol at 0.6–0.8 nm, 0.0040 against 0.0052 at 0.9–1.2 nm, `5·10⁻⁴` against
`1·10⁻³` at 1.4–1.8 nm), and its three-body response is *smaller* (sum over the pairs of other
sites `4.6·10⁻⁴` kcal/mol per head against 0.069 per backbone group).  What the class
decomposition of §1 measures is something else: in the subsets that carry the truth the charged
group's own site is in `T`, and the term is the *difference between two positions of the head* of
its response to the other sites — for a group with a net charge of 0.64 e at the end of a long
side chain, which in the states that carry the sum comes within 0.35–0.6 nm of another ammonium
group (§2.2).

### 2.2 The law in the distance [M, anchor context; no law derived]

* **First-order response of a rigid group to another site** (fit `ln R1 = a ln d + c` beyond
  0.8 nm, `d` the distance between the centroid of the group and the centroid of the other side
  chain in its maximising state): `a = −4.7` and `−5.1` for the charged heads (Lys₁₂, (LKSE)₃),
  `−3.7` and `−4.7` for the aliphatic chains, `−4.2, −4.9, −6.3, −4.7` for the backbone groups of the
  four peptides, `−3.4, −3.8, −4.5` for neutral side chains (rms residuals 0.5–1.4 in `ln`, a factor
  1.7–4).  **About `r⁻⁴` to `r⁻⁵` for charged and neutral groups alike — the power of the
  descreening integral, not slower.**  A charged group has no long-range many-body tail of its
  own: the pair kernel of two far atoms depends on the Born radii only through `e^{−r²/4B_aB_b}`
  (§3.1), and what is left is the descreening of each atom by the others.
* **Third-order terms in the anchor context**, `M_T = max_y |d_T(y_T)|` for all 220 triples (exact
  evaluations on the full grid of the three sites; a lower bound of `c_T^anch`): with `P` the
  smallest, over the three groups, of the product of its distances to the other two in the
  maximising states, `ln M_T = a ln P + c` gives `a = −3.0` (Lys₁₂), `−3.1` ((LKSE)₃), `−5.6` (Ser₁₂),
  `−3.9` (Leu₁₂) over all triples and `−3.8, −3.9, −6.3, −3.9` over the triples whose three groups stay
  more than 0.6 nm apart: again about `r⁻⁴` per partner, with a scatter of a factor three.
* **The sums are contact terms.**  For Lys₁₂ `Σ_T M_T = 11.9` kcal/mol (20.0 `k_BT`; Ser₁₂ 0.98,
  Leu₁₂ 4.3, (LKSE)₃ 18.3 `k_BT`), and 98 % of it comes from the 146 triples in whose maximising
  states two of the three ammonium groups are within 0.6 nm of each other.  Along the sequence it is the helix that speaks: spans
  4 and 7 (side chains on one face, `i, i+3/i+4, i+7`) carry 61 % and 30 % of the sum; spans 5, 6
  and 8–11 together 3.6 %.
* **With against without a charged side chain, at equal distance** ((LKSE)₃, the 220 triples by
  the number of Lys/Glu among the three): medians of `M_T` 0.0050, 0.0097, 0.012, 0.018 kcal/mol for
  0, 1, 2, 3 charged side chains; restricted to triples whose smallest group distance is
  0.6–1.0 nm: 0.0060, 0.0041, 0.0049, 0.016.  At comparable distance a triple with one or two
  charged side chains is not larger than one with none; with three it is about three times
  larger.  The sums differ because the charged side chains are long: 0.49, 2.4, 7.6, 0.42 kcal/mol
  for the 20, 90, 90, 20 triples.

### 2.3 The truth at twelve residues, and what an ideal certificate would need [M; the reading of first-order numbers as brackets is an estimate and labelled so]

1. **The exact anchored terms at twelve residues, orders 3 and 4** (`p8_14_exact_terms12.py`).
   The ball of radius `M` around the anchor — the same evaluations the certificate of order
   `M + 1` pays for — determines every anchored term `d_T`, `|T| ≤ M`, exactly (P3's
   `pwmodel.anchored_terms`).  `M_T = max_y |d_T(y_T)|` is what the truth contributes at `T` in
   the anchor context, a lower bound of the exact anchored constant `c_T^anch`.  On the
   enumerated charged instances the all-context constants are only a few per cent larger
   (last column: Lys₅ 4.6 % and 1.6 % at orders 3, 4; LKSE:5 14 % and 2.9 %), so there `Σ M_T` is
   the truth to that accuracy; for leucine less so — Leu₁₂, which P5 enumerated, has all-context
   sums of 3.92 and 1.07 kcal/mol at orders 3, 4 (P5's Table 1a) against 2.57 and 0.77 in the
   anchor context, a factor 1.5 and 1.4.

<!--T:T12-->

   *The truth at twelve residues falls fast for lysine* [M]: Lys₁₂ 20.0 → 0.99 `k_BT` from order
   3 to 4 (20-fold; Lys₅ by enumeration 55-fold), Ser₁₂ 0.98 → 0.067 (15-fold), (LKSE)₃
   18.3 → 2.49 (7.3-fold), Leu₁₂ 4.3 → 1.3 (3.3-fold).  At order 4 the truth of Lys₁₂ is 15 times
   serine's, *below* leucine's and 2.5 times below the patterned sequence's.  *And the necessary condition holds* [M]: every bound of this
   report must dominate `M_T` subset by subset (the anchor context is among the contexts each of
   them covers); this is the one comparison with exact quantities that is possible at twelve
   residues — 11 880 comparisons (495 four-subsets, four peptides, six variants), no violation;
   the smallest ratio of a new constant to its exact term is 15 (Lys₁₂), 24 ((LKSE)₃), 11 (Ser₁₂),
   24 (Leu₁₂).  *What is left for any sharper bound* [M]: the new constants are 34 (Lys₁₂), 119
   ((LKSE)₃), 52 (Ser₁₂), 221 (Leu₁₂) times the exact terms in sum at order 4 — P3's were 695,
   752, 82, 245.  **Lysine has gone from one of the two worst ratios to the best.**

2. **The floor of the architecture** [M, exact at every sampled state].  Any sandwich
   `[f + I_{m−1}g] ∓ pen` needs `pen(x) ≥ |R_m(x)|`, `R_m = g − I_{m−1}g`, at every state; by Lemma A17.16 its
   bracket is then at least about `2β⟨|R_m|⟩`.  `p8_08_ideal.py` computes `R_m` **exactly** at every
   state of the Gibbs sample (from the `2^s` corner energies of a state with `s` changed sites):

<!--T:T8-->

   For Lys₁₂ the floor is `5·10⁻⁵` nats at order 3 and `2·10⁻⁸` at order 4: 9.6 % of the states have
   three or more side chains off the anchor, and there the true third-order remainder averages
   `1.6·10⁻⁴` kcal/mol.  For (LKSE)₃ `6·10⁻⁴` and `2·10⁻⁶`.  Serine, with 6.3 side chains off the
   anchor, has by far the largest floor (0.017 nats at order 3); the frozen leucine helix the
   smallest (`3·10⁻⁶`).  **Measured by what the ensemble does, lysine is three hundred times
   easier than serine, not harder.**

3. **Exact terms in place of constants** [M for the numbers; an estimate of a bracket].  With
   `M_T` in place of `ĉ_T` and the share forms of §4 (table T7, rows "exact3", "exact4"; first-order
   estimate, in square brackets the exponential estimate and the largest penalty on the sample):
   Lys₁₂ at **order 3**: 3.6 (site form), 0.76 (banded pairs), 0.54 (banded triples, band 6), 0.024
   (every triple charged to itself — at order 3 the envelope), with penalties of 4–9 `k_BT` on
   the sample in the first three forms, so that the true brackets would be larger (at order 4 with the certified
   constants the pipeline's bracket is 2.5 times the first-order estimate, §4.1); at **order 4**:
   0.18, 0.043, 0.035 with penalties below 0.5 `k_BT` — reliable.  (LKSE)₃ at order 3: 8.4, 2.0, 0.57,
   0.45, and at order 4: 1.09, 0.26, 0.097 (penalties up to 1.5 `k_BT`); Ser₁₂: 1.04, 0.56, 0.30, 0.29
   at order 3 and 0.070, 0.037, 0.021 at order 4.  **So an ideal
   certificate — exact constants per subset — would bracket Lys₁₂ within about half a nat at
   order 3 only with triple shares and without margin, and within 0.03–0.2 nats at order 4
   with any share form** (balls of 3 841 and 96 366 evaluations; not counting what the band
   costs in the pipeline, 0.14–0.35 nats for Lys₁₂, §4.1).  The certified constants reach the same
   at order 5 (§4): one order is the price of the factor 34.

4. **Where the remaining gap is.**  The exact constants are suprema over all rotamers of the
   sites of `T`; the ensemble visits few of them.  Between the floor of item 2 (`5·10⁻⁵` nats at
   order 3) and what exact constants would pay (0.02–0.5) lie three to four orders of
   magnitude that no constant per subset can reach — only a penalty that depends on the
   rotamer states (request P8-E4).
