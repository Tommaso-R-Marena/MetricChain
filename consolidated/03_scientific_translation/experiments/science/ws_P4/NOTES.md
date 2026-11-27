# P4 notes (running)

Started 2026-11-26. Read COMMON.md, P4_brief.md. Directory created.

## Step 0 (01:55-02:10 UTC) reading and identification of "the 13"
- Read: theory export at 24a3c27: THEORY_REPORT §11.7 (Thm 11.16-11.18a, Prop 11.18b, 11.18c), THY-RES-0009,
  ThirdOrderModel.lean, ShareCertificates.lean; P2_REPORT (all), ws_P2/anlib.py, an_main.py, make_tables.py.
- `p4_00_find13.py` (reads P2's out/an_*.json): g_GB: 184 analyses with an "iface|GB" entry (P2's report says 181;
  see report for the difference), star exact 110, plain row-sum 97, exact & row-sum fails = 13:
  F2/P2(.70) F3/P2(.70) F4/E(.60) F4/H(.60) F4/P2(.70) F5/E(.60) F5/H(.60) F6/E(.60) F7/E(.60)
  L14/H(.60) L16/H(.60) L5/H(.60) LKSE2/H(.60).   log: logs/p4_00_find13.log
- P2's row-sum flag = `rowsum_plain_ok` = (min excitation of E at argmin E) >= 0.5*sum_j c_ij(g) per site, on X'.
  P2's exact flag = `certifies_exactly` = x0 (= argmin E over X') minimises L = f + g_star - sum c_ij.

## Step 1 (02:10-) item 1
- `p4lib.py`: my own constants (c2_matrix, c3_dict: range trick), tables at x0, star/I2, exact-rational
  Edmonds-Karp share flow + verify_shares / verify_overdense / brute force densest_excess, state-dependent
  share LP (my refinement) + exact verification after repair.  P2 code used only for loading and X'.
- `p4_01_shares.py`: test on Phe (--only fb_F) OK: c_ij identical to P2's stored matrix (0.0 difference),
  flags agree; of the 9 Phe instances among the 13 the flow certifies 8 (F4/H fails: over-dense {0,1},
  excess 0.0357; state-dependent shares certify it).
- full run started in background -> logs/p4_01_shares.log, out/p4_01_shares.json

## Step 1 result (02:03 UTC) -- item 1 DONE
- `python3 -B p4_01_shares.py` (56 s, log logs/p4_01_shares.log reached "DONE"; out/p4_01_shares.json): 184 instance
  files, 908 (instance, residual) analyses.  My c_ij == P2's stored matrix (max diff 0.0); my exact/row-sum flags ==
  P2's flags (0 disagreements).
- HEADLINE: of the 13 (g_GB), share certificate 11.18b(d) certifies **11**; fails for F4/H(.60) (over-dense {0,1},
  excess 0.0357) and LKSE2/H(.60) ({0,1}, 0.0338).  Row-sum for the deficits holds in 2 (L14/H, L16/H).
  State-dependent shares (my LP refinement, verified exactly after repair) certify all 13.
- g_GB over all 184: criterion 110, plain row-sum(c) 97, row-sum(w) 91, shares(w) 106; 4 exact-without-shares:
  F4/H, LKSE2/H, S2/E(.60), S2/E(.70).  shares & not exact: 0 everywhere (soundness).
- other residuals (criterion / shares): coul+GB 145/119, ff03 156/120, ff15ipq 155/126, ff99SB 180/125 (c_ij = 0 there!
  the certificate fails in 55 of 180 although L = E: the deficits are the known part's own negative pair terms).
- the 184 vs P2's "181": three Ser5 analyses at tau = 0.80 are in P2's out/ and not in its count; all three non-exact.
- plain row-sum (c) holds while criterion fails: ff03 6 analyses, ff15ipq 1 (so the plain condition is not sufficient
  for a pairwise known part on real instances; g_GB: none).
- tables: `python3 -B p4_01b_tables.py > logs/p4_01b_tables.log`.

## Step 2 (02:05-02:12) -- item 2 DONE (numbers), tables in logs/p4_02b_tables.log
- `python3 -B p4_02_third.py` (55 s; logs/p4_02_third.log reached DONE; out/p4_02_third.json): 136 instances of g_GB with
  >= 3 multi-state sites (n up to 16), own c_T == P2's stored (0.0 diff, 115 instances with stored triples).
- soundness m <= E: min over 1023 (instance, model) pairs of min_x(E - m) = -1.1e-13.  order site <= pair <= env3: 136/136.
- reference minimises: env3 133, pair 132, site 113 (pair yes / site no: 19; env3 yes / pair no: 1 = LKSE6/P2(.60),
  recovered by LP over pair shares).  LP over all coverings (CV-A) never beats LP over pair shares on the margin.
- ln Z(m) - ln Z(E): median env3 2.6e-4, pair 2.9e-3, site 2.0e-2; site/pair median 6.8 (1.0-137); pair/env3 median 7.8.
- largest gap: identical for the three forms in 129/136 (attained where every site is changed: the penalties coincide there).
- share certificates 11.18b(c)/(d) on the third-order models: pair form minimises in 132, shares exist in 110
  (Ser 18/27, Lys 6/9, LKSE 1/11); state-dependent shares 132/132.
- Lean: copies of ThirdOrderModel.lean and ShareCertificates.lean (lean/; the second with its import changed to
  HigherOrderEnvelope because ThirdOrderModel is not in our tree; `#print axioms` appended) compile with
  `lake env lean` from /home/user/MetricChain: exit 0, axioms propext/Classical.choice/Quot.sound (logs/p4_lean_copies.log).
- `python3 -B p4_03_review.py` (3 s; logs/p4_03_review.log DONE): blocks A-F pass; counterexample to "11.18b(b) holds
  verbatim on a reset-closed non-product domain" (3x3 minus pair (1,1)); D \ D' unconstrained (LP unbounded 41/41).

## TODO next: p4_04 (P2's X' vs D'(x0) vs X_tau), report, item 4 (P3 sandwich), harness re-run XI.16-18 (their code).

## Step 3 (02:13-02:45) -- review, domains, item 4, report
- `p4_03_review.py` extended (blocks A-G; all pass, 4 s): added (i) the example "best pair shares 1/6 < envelope 0.5",
  (ii) 3-binary-site example for mechanism (2), (iii) block G: state-dependent shares <=> local-polytope LP tight at x0
  (300/300), (iv) LP over the class on D \ D' unbounded (41/41) with the constants of g itself (the first version used
  c = 1, which made the LP infeasible -- fixed).
- `p4_04_domains.py` (20 s): 40 g_GB analyses with non-product X_tau.  X' = D'(x0) in 6, smaller in 34; x0 = argmin over X'
  is NOT the minimiser over X_tau in 14 (Phe4..8/E(.60): 1.92, 10.45, 11.90, 13.20, 13.25 kcal/mol lower outside X';
  checked directly from P2's arrays for F5, F6, F7: minimiser = state 3 at every site, s2min 0.928).  Star on D'(x*): 13/40.
  Second-order remainder bound on D' (masked constants): no violation at any state of 80 domains.
- `p4_07_dprime3.py` (39 s): third order on D'(x*), 34 analyses: bound and m <= E hold everywhere; pair model certifies
  30/34 (fails: K3/H, K4/E, K4/H, K4/P2 at .60 -- K4/E(.60) is certified on X' but not on D'(x*): c_T max 1.05 -> 3.78).
- `logs/p4_05_harness_rerun.log`: their harness XI.16-18 in full mode reproduces the numbers printed in 11.18b, 11.18c.
- `p4_06_p3pair.py` + `run_p4_06.sh` (item 4): P3's certified chat_T (re-run of P3's GFBound, cache redirected to
  ws_P4/cache_p3 so that nothing is written in ws_P3), pair form / banded pair form (w = 2) against P3's site form on
  P2's grids: V6/E m=3 cost number 16.4 -> 0.064; m=4 0.0081 -> 0.000087 (P3's own 0.008 reproduced); useless in all
  forms where Gamma_m is large (S6/H, K4/H, L8/H, V8/P2 at m = 3).
- `p4_02_third.py` re-run once more after adding "where is the largest gap attained" (all stored numbers identical, 0.0).
- Report written: docs/science/workstreams/P4_REPORT.md (sections 0-6).  Every number in it was copied from the logs
  in logs/ (all end with DONE / exit 0).

## Not done / ideas
- joint LP (pair shares of triples + state-dependent shares) -- would give an enumeration-free certificate search.
- share certificates on non-product domains (only bounds/criteria there).
- literature check of the citations in 11.18b(b) and of the LP-duality attribution of P4.1.
- item 4: ceiling side, m = 5, P3's band reductions, P3's own anchor.

## Step 4 (02:33-02:36) -- joint LP
- `p4_08_joint.py` (48 s, logs/p4_08_joint.log DONE): one LP over pair shares of the triples and state-dependent
  shares together (inputs: ball data + c_T only).  Exactly verified certificate in 133/136 = exactly the instances in
  which the three-body envelope certifies; equal thirds + state-dependent shares: 132 (gain: LKSE6/P2(.60), slack 0.0102).
  Largest LP 2161 variables x 4996 rows.  Report sections 2.2(e), 3.9, 6(3) updated.
