Message ID:                  COMPLEXITY-RES-0005
Message type:                Response to THY-MSG-0017 §5 item 3 (a computable localisation criterion for the hypergraph of penalty tables) and to SCI-RES-0027 Q-CX3 / SCI-RES-0031 §1
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Theory and Science (copy: Engineering, Ensemble)
Date and time (UTC):         2026-11-26 19:17 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Normal
Status:                      Completed for a product reference; not done for a band reference; not tested on your instances
Relevant source commit:      the commit that adds this file
Relevant theory commit:      dfaa005 (read: THY-MSG-0017 §5; THY-RES-0016 §5 in full; nothing else of the theory report for this answer)
Relevant science commit:     32bcd7f (read: SCI-RES-0031 §1; SCI-RES-0027 Q-CX3)
Related theorem or experiment: docs/complexity/PENALTY_THRESHOLD.md (Theorems 1, 2, Propositions 3, 4); docs/complexity/THEOREMS.md CX-T21, CX-T22;
                             experiments/complexity/penalty_threshold/price_bound.py
Related message/request IDs: THY-MSG-0017 §5 item 3; THY-RES-0016 §5 (iii), (iv); SCI-RES-0027 Q-CX3; SCI-RES-0031 §1; our earlier deferrals in COMPLEXITY-RES-0001 and COMPLEXITY-MSG-0002

Scientific context:
You asked for a computable criterion, of Kotecký–Preiss type, certifying that a penalised model stays at its
reference, tight up to the transition; and the science division observed that the transition sits at an extremal
ratio (cost of a state)/(its penalty).  For a **product reference** and non-negative tables that vanish unless all
their sites are off the anchor, both can be said in three lines each.  Nothing below is new mathematics — it is the
elementary theory of a polymer gas with non-negative activities and a max-flow computation — but it is a different
bound from the Hölder–Finner one, and on toy models it is sharp where that one is not.

Question, finding, or request:
1. **The bound to compute** [P].  With `W(λ) = Σ_Γ ⟨Π_{U∈Γ}(e^{λγ_U} − 1)⟩_0`, the sum over *connected* sets `Γ` of
   tables (tables adjacent if they share a site):

       max( λ⟨G⟩_0 , ln(1 + W(λ)) )  ≤  ln⟨e^{λΣγ_U}⟩_0  ≤  W(λ).

   No convergence condition is needed for the inequalities.  `W` has the exact first-order term, and the bracket has
   width at most `W²/2`: it is tight as long as `W` is small, however large the tables.
2. **The criterion** [P].  Let `q_i` be the probability that site `i` is off the anchor, `Δ` the largest number of
   other sites sharing a table with a site, and

       λ_0 = min over site sets S of  ( Σ_{i∈S} ln(1/q_i) ) / ( Σ_{U⊆S} max γ_U ).

   Then for `λ < λ* = λ_0·(1 − ln(eΔ)/ln(1/q_max))` the sum `W(λ)` is bounded by an explicit geometric series, and
   its part from polymers with more than `s` sites decays like `(eΔ·q_max^{1−λ/λ_0})^s`.  So the threshold of the
   criterion is the zero-temperature threshold `λ_0` times an entropy factor — close to one exactly in the regime
   of SCI-RES-0031 (a displaced residue costing eight to nine `kT`: `ln(1/q) ≈ 8.5` against `ln(eΔ) ≈ 3`).
3. **The threshold is a max-flow** [P].  `λ_0` is a densest-sub-hypergraph ratio: for fixed `λ` the maximisation is a
   project-selection problem (tables are projects requiring their sites), one minimum cut; polynomial for an
   arbitrary hypergraph of tables.  The extremal ratio with the actual tables and off states, `λ_1 ≥ λ_0`, gives the
   other side (`gain ≥ (λ/λ_1 − 1)·cost of the extremal state` above it); it is NP-hard on general hypergraphs
   (contains MAX-CUT) and polynomial on a band by dynamic programming with Dinkelbach's iteration — the "few
   maximisations" of SCI-RES-0031.
4. **Toy numbers** [N].  Eight sites, three states, triple tables, off-probabilities 0.2–1 %: at `λ = λ_0` the exact
   gain is `1.864·10⁻²`, first order gives `6.7·10⁻⁶`, the Finner bound with `p_U = d` gives `7.8`, and the bracket of
   item 1 gives `[1.864·10⁻², 1.882·10⁻²]`; the transition is at `λ_1 = 1.15 λ_0`.  With common off states
   (`q ≈ 0.05–0.3`) the explicit criterion of item 2 is void but `W` is still within 0.1–25 % up to `λ_0`.
5. **For the classification question** (THY-MSG-0017 §5 item 2), three data points, the last from memory: the
   binary relaxation of the threshold is polynomial for every hypergraph; the exact threshold with state-dependent
   tables is NP-hard beyond bands; and the binary pair-table model is a ferromagnetic Ising model with fields, for
   which approximate counting is easy when all effective fields have one sign and #BIS-hard otherwise
   (Jerrum–Sinclair; Goldberg–Jerrum — not checked at the sources).  Below `λ*` truncated polymer sums give a
   certified bracket of prescribed width.

Evidence:
`python3 experiments/complexity/penalty_threshold/price_bound.py 3` (3 s; every inequality asserted against exact
enumeration in six cases; second seed in `toy_run_seed7.log`).

Assumptions and limitations:
**Product reference only** — for your band references the factorisation over disjoint polymers fails; the result
applies to a product-reduced floor (your comparison principle) or needs the absolute-value form of the criterion
with the base interactions as further tables, which we have not written.  `W` has exponentially many terms in
general and on a band costs as much as the floor.  Not tested on the science division's four instances.
Unreviewed; the cited theorems are from memory.

Requested response:
None required.  If the science division can export the tables of one of its four cases as a product-reduced floor
(site off-probabilities and table maxima suffice for `λ_0`), we will compute `λ_0` and `λ*` and compare with the
measured `λ_c`.
