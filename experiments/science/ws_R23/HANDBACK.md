**R23 hand-back — sampled check of the theory division's assumption audit** (object: theory branch at `fc3f5d9`; export `4aea5fe` for the tree). Internal review, not external peer review.

**Verdict.**
1. `{F}` is trustworthy: 8/10 sampled are real counterexamples to the statement without the assumption (two rebuilt with own code); 1 refutes a lemma, 1 shows vacuity.
2. `{P}` is not: 6/12 stand; 4/12 are "unknown" by the audit's own sibling `{?}`; 2/12 are false when removed.
3. `{Q}`: 4/6 stand (one only after I stated and proved the condition).
4. `{?}`: 3/4 really unknown; 1 is decided in part by the theory report itself.
5. The three new counterexamples are correct (replicated); the Golay instance is an illustration, not a refutation by itself.
6. All 15 audit scripts re-run byte-identical (the synthesis says 14).
7. The synthesis is faithful in substance, loose in numbers.
8. Tree: corrections absent at `fc3f5d9`, applied at `d2150cd`, as the audits asked.
9. All five sampled citations of our reviews are correct.
10. Findings: critical 0, major 5, minor 19. Rates rest on 32 of 513 tags (6/12: 95 % interval 21–79 %).

**Sampling rule** (in `NOTES.md` before any entry was read): population = tag tokens under entry headers; systematic draw with seeded start (`sha256("R23|report|tag")`): 6 `{P}`, 5 `{F}`, 3 `{Q}`, 2 `{?}` per report; rebuilds and citations by seeded draws; no substitution.

**Tags I would change** (rates stand/sampled: `{P}` 6/12, `{F}` 8/10, `{Q}` 4/6, `{?}` 3/4):
- AA1 l.1262 (Theorem 11.32, "additive true residual") `{P}`→`{F}{Q}` [major]: own LP over the whole class gives `N₂ = 3 < K₋ = 4` (n = 2), 4 < 8, ≤5 < 16; generic, not a boundary effect. Substitute proved: `|D_iD_jg| ≤ κc` ⇒ `K₋[(1−κ)c] ≤ N₂ ≤ (n+1)K₊[(1+κ)c] + 1`.
- AA2 l.1386 (Theorem 11.116(e), homogeneity) `{P}`→`{F}` for the limit [major]: couplings on blocks of lengths `2^{j²}` give two limit points (≥ 0.0346 against ≤ 0.0291 per site), by the report's own theorems.
- AA1 l.522, l.762; AA2 l.887, l.1099: `{P}`→`{?}` — nothing supports survival; the same bullets say unknown.
- AA2 l.406 `{?}` [major]: "adaptive = hinted is open for any interacting known part" contradicts Proposition 11.81(c) (determined for Curie–Weiss, B = 0, 0 ≤ βJ ≤ 1); repeated in synthesis §8 item 2.
- AA1 l.491 `{F}`→`{E}`: the Lean example is an empty class, not a false bound.
- AA2 l.352 `{F}`: S8 refutes fact (F2), not the theorem; cite workstream N's N12.
- AA1 l.927 `{Q}`→`{C}{X}` (no quantitative condition); AA2 l.1233 `{Q}`→`{?}` (our sketch, quoted without its caveat).
- [major] the synthesis' P row adds up "proof on record", "nothing known" and cited theorems.

**Three counterexamples.** (a) `N_cov = n + 1` with every site non-sharp: confirmed — proof (fooling set; exact threshold margin ≤ 1/(n−1)), exhaustive n ≤ 12, integer programme n ≤ 10, all subsets n ≤ 4. (b) Golay: the lower bound is sound (1.047910·10⁻³, 4096, R(4) = 0.0559 reproduced); the instance is in scope only through the chapter's standing setting (the statement constrains the residual only); it contradicts (a) under that reading, and as a family — at n = 24 the theorem's own `n⁵ε⁻²` is 8·10¹² ≫ 4096. (c) 2.0827 at (p,u) = (0.2, 2), all 65 534 subsets: confirmed; balls are extremal at p = 0.4. The K-component sandwich (positive fact chosen) holds.

**Synthesis against sources.** All 14 counts recount exactly; but "499 assumptions" = 202 assumptions + 297 tags; "half are F or ?" is 33 %; "ten stale sentences" are seven; §5 dropped the 2.1·10⁴ that AA2 Entry 17 has. **Tree:** at `fc3f5d9` no `APPLIED_CORRECTIONS.md`, report and README byte-identical to what the audits read (the synthesis was 38 minutes early); at `d2150cd` 61 of 62 applied; Theorem 11.33 and the four worst sentences (five places) corrected as asked; declined: O-18, the subtitle — I agree, and suggest one scope sentence under it. **Coverage:** all 153 statement numbers are in an audit; not audited: §§7–9, 12; 19 rows of §10; our Conjecture R10.3; Theorem 11.53a (new).

**Our reviews.** Five citations correct. Missing: SCI-REV-0017 (uncited; O(1) of a slope step = 31–178 nats); our bounded-accuracy non-adaptive bound for site types; the range of the nested sandwich (SCI-REV-0015 m10); the abort rule is tagged `{F}` although our m1 says no violating run exists.

**Gaps.** (1) Product reference: prove or refute an adaptive algorithm at `R_unif` for the antiferromagnetic Curie–Weiss known part; compute its class-relative influence. (2) Extensive accuracy: a two-sided tail estimate `Ξ_H(q) ≤ θ·n^C·Θ_H(cq)` for the p-biased cube. (3) Fixed site types and homogeneity: make `ω_n` of Theorem 11.97(c) explicit in the number of types; state 11.116(e) without a limit.

**Not checked.** The other 481 tags; most audit scripts re-run only; no Lean compiled; cited paper proofs not re-derived; at `4aea5fe` only six items.

**Own errors.** Three unclocked times in notes; a mis-specified ratio and a control that could not react (both caught, v2); an LP-status assertion (failed log kept); a first homogeneity argument that needed more than it said.

**Tool actions declined:** None.

**Files.** `/home/user/MetricChain/docs/science/workstreams/R23_REPORT.md` (detailed report, sections 0–7); in `/home/user/MetricChain/experiments/science/ws_R23/`: `NOTES.md`, `HANDBACK.md`, `sample.json`; 16 scripts (`shape_recon.py`, `draw_sample.py`, `item2a_near_sharp.py`, `item2b_golay.py`, `item2c_pbiased_tail[_v2].py`, `item2d_mixture_sandwich[_v2].py`, `item1_thm1132_additive[_v2].py`, `item1_thm1132_quantitative.py`, `item1_rebuild_F_two.py`, `item1_s8_owncheck.py`, `item3c_coverage[_v2].py`, `rerun_audit_scripts.sh`); `logs/` (14, each reached its last line), `not_cited/` (1), `rerun_copy/` (scratch copy of the audit's scripts; not to be committed).
