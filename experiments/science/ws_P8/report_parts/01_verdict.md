---

## 0. Verdict in five sentences

1. **Step 3 of the brief is answered in the negative, and the slack is elsewhere.**  P3's cross
   bound does carry the factor `e^{−r²/4B_aB_b}` (`ws_P3/encl.py`, lines 296–305, called from
   `gfbound.py`, lines 156–172: `H_k = (2/r)·sup|ζ_k(D)|`, `D = r²/4B_aB_b`, every `ζ_k` with a factor
   `e^{−bD}`, `b ≥ 1`), and pairs that are far in every state carry at most 4 % of the bound; what
   loses is the closed form's merging of the maxima over the rotamers of a pair's host side
   chains, ingredient by ingredient, which costs a factor 12, 98, 313 on the ammonium–ammonium
   pairs of Lys₅ at orders 3, 4, 5.
2. **The truth for lysine is larger, but easy:** per subset it is 12–22 times serine's, carried
   to 95–101 % by atom pairs that involve an ammonium group, with one sign, so that a sign-blind
   bound must lose only a factor 3–7 there (13–37 for the patterned sequence at orders 3–5); it
   falls 55- and 83-fold per order on Lys₅ and 20-fold from order 3 to 4 at twelve residues
   (20.0 → 0.99 `k_BT`, measured), the response of a group to a far side chain decays like `r⁻⁴` to
   `r⁻⁵` for charged and neutral groups alike, the third-order sum at twelve residues is 98 %
   contact triples, and exact constants would bracket Lys₁₂ within about half a nat at order 3
   and 0.03–0.2 nats at order 4.
3. **The sharper bound:** taking the maximum over the host states of the bound itself (P3's
   Theorem 3 without the merging step — not new as a bound, P3's `termwise` has it) and expanding
   every term in its own order of the sites, so that a host outside `T` sits at its anchor
   (Theorem AH, proved in §3.3; I did not find it in P3, P5 or P6), gives constants that were
   never below an exact one in 12.9 million comparisons and 9.1 billion state-by-state checks on
   fourteen enumerated instances (smallest ratio 1.0001), nor below the exact anchored term of
   any four-subset of the twelve-residue peptides, and that are for Lys₁₂ on the helix **34.0, 2.40, 0.136 `k_BT` at
   orders 4, 5, 6 against P3's 689, 145, 23.4** (factors 20, 60, 172), for (LKSE)₃ 296, 42.8, 4.87
   against 1 874, 568, 147, with gains of 1.6–1.8 for Ser₁₂ and 1.1 for Leu₁₂.
4. **The lever is this bound plus one more order:** fed with the new constants, the existing
   pipeline brackets `ln Z` of Lys₁₂ on the helix within 2.81 nats at order 4 (96 366 evaluations;
   1.56 nats with band 7) and within **0.45 nats at order 5 with band 6 and 0.19 nats with band
   7** (1.62 million evaluations, half an hour on one core) — below one nat in every share form,
   where P3's constants stood at 7–31 nats to first order; a sharper sign-blind bound could add
   at most a factor 5–20 on Lys₅, the sandwich sampler tolerates two to three nats (inside the
   1.56 nats of order 4 it would need 10 500 points, not run), and at order 5 the bracket is
   limited by the band, not by the constants.
5. **Limits:** the patterned sequence is not rescued — (LKSE)₃ is bracketed within 4.49 nats at
   order 5 (3.47 million evaluations), its new constants are still 119 times its exact
   four-body terms, and what is left of its bound is the apolar part where the sign-blind class
   is the obstacle; nothing here is refereed or machine-checked and the pipeline runs
   were made with my own driver and have not been repeated by anyone else; and four of my
   enumeration passes broke the 3 GB memory limit (one reached 11.7 GB) before the coordinator
   noticed — cause found (a reference cycle in P5's `anch_walk`), fixed, re-run at 1.1 GB.
