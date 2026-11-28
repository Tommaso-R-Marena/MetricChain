# HIE-REQ-0001, Q1 and Q2: independent replication (engineering)

*Saved by the coordinator of the Computational Research Division from the text returned by the independent
verifier (a subagent): the harness does not let a subagent write a report file.  The text below is the
verifier's, unchanged except for this note.  What the coordinator checked is stated in
`docs/collaboration/responses/engineering/ENG-RES-0020.md`.*

Files in this directory: `PREDICTIONS.md`, the scripts `q1_lemma_b.py`, `q1_crosscheck.py`,
`q1_negctl_large.py`, `q1_hidden_witness.py`, `q2_r3.py`, `make_q1_table.py`, and the raw outputs in `out/`.
The full 220-row per-case table of Q1 is `out/q1_table.md`.

*Written 2026-11-28 by one AI session working as an independent verifier.  Requesting branch at `0ec16b8`.
Q3 was not done, by the coordinator's decision.  Predictions were written at 02:51 UTC, before any run; the
runs took place 02:52–03:07 UTC.*

## 1. Summary and verdicts

I wrote my own code from HIERARCHY_REPORT §1, §3 and §4.  I did not import or run any of their scripts.  I
read their Q1 script only after my numbers existed, to explain a difference.

**Q1 (Lemma B): passes the lemma criterion.**

- **Coverage:** 220 cases — their 124 (parameters read from their stored output) and 96 of my own
  (Θ ∈ {1.0, 1.1, 1.3}·nh, n ≤ 400).  In each I computed the exact pointwise-largest −F.
- **Result:** no case exceeds m(u + 5 ln(n+1)).  The largest value is **+4.969 nats**, against allowances
  of about 90–120, under both readings described below.

Two qualifications:

- **Their script tests a different hypothesis from their report.**  The report's §3 definition of "sees
  only S" allows parities.  Their script imposes plain independence, which is a stronger hypothesis.  Under
  plain independence I reproduce their 124 stored numbers to within 5e-4 (their print rounding).  Under the
  report's definition my values are higher by up to 0.164 nats.
- **Their sharp side claim fails in general.**  The claim is "≤ 0.01 nats (report: +0.002) over types with
  t_T > Θ when Θ ≥ 1.1nh".  It fails:
  - in 2 of their own cases under the parity definition (+0.0188);
  - in 4 of my cases under both readings, up to **+0.617** (u = 1, blocks (30, 30, 50, 70), roles QQTT).
    This was re-checked by an independent feasibility test, and by Dijkstra and LP on smaller analogues.
  - This does not contradict Lemma B, whose allowance is about 100 nats.

Every case lies outside the lemma's own hypothesis Θ ≥ nh + 2mL, and 24 cases have n_j < N_u.  So the test
asks more than the lemma claims.

**Negative controls work only at larger n.**

- At n ≤ 400, dropping hypotheses gives up to +97.7, which is still below the allowance.  At these sizes
  only the sharp expectations, not the allowance, separate valid from invalid profiles.
- At n = 820–1000:
  - dropping (H1) gives +191.8 against an allowance of 112.7;
  - dropping both gives up to +243 against 115.6;
  - with all hypotheses kept, the same cases stay at ≤ +5.08.

**Q2 (Algorithm R3): (a), (b) and (c) pass, and the mutation is caught.**

- **Runs:** 32 instances (n = 12–16, two or three blocks, four profile families), giving 100
  (instance, M) tests and 39 056 runs.
  - M ∈ {10², 10³, 10⁴} on all 32 instances; M = 10⁵ on 4.
  - Repetitions: R = 1000 at M = 100, R = 200 at M = 1000, R = 20 at M = 10⁴, R = 4 at M = 10⁵.
- **(a):** 14 933 849 candidate computations; 0 were neither the centre nor its antipode.
- **(c):** 31 788 runs revealed all blocks; 0 of them gave Â ≠ A beyond a relative 1e-12.
- **(b):** 100/100 tests within 3 standard errors.
  - Caveat: in 81 of those tests every run revealed everything, so only 19 tests are statistically
    informative (max |z| = 1.87).
  - A stronger exact check covers all 39 056 runs: E[Â | rounds 1–2], computed over all 2ⁿ points, equals
    A(ψ) to within 1.4e-14 relative.
- **Mutation (uniform shell weights):**
  - |z| > 3 in 99/100 tests.  The one miss is a test where almost nothing was revealed, so the weights are
    an empty product and the mutation does nothing.
  - The exact conditional mean is biased in 32 934/32 934 runs with a non-empty revealed set S₂.

## 2. Definitions used, and ambiguities

**Definitions** (all section numbers refer to HIERARCHY_REPORT.md at `0ec16b8`):

- **From §1:**
  - f(ρ) = KL(ρ‖½), Λ₁ = ln(2/(1+e^{−u})), κ = Λ₁/u, h = f(κ).
  - Types: 𝒟 = Π{0..n_j}; neighbouring types differ by 1 in one coordinate.
  - t_j = ln P_j(⌊n_j/2⌋) − ln P_j(d), with P_j = Bin(n_j, ½), computed from exact integer log C(n_j, d).
  - V_S(Θ) = {t_{S^c} ≤ Θ}.
  - N_u = ⌈5/(1−2κ)⌉ (from F4); L = ln(n+1).
- **From §3:** "F sees only S on V" means F(d) = F(d′) whenever d_S = d′_S and d_j ≡ d′_j (mod 2) for
  j ∉ S.  (H1) is "sees only P" on V_∅; (H2) is "sees only P ∪ Q" on V_P.
- **From the request:** the quantity V = max_y [ν(y) − n_P h + min{t_T(y), Θ − (n − n_P)h}].
- **From §4:** Algorithm R3 as written.

**Ambiguities, and what I did:**

1. **Parities.**  The request and their script say "independent of the coordinates".  The report §3
   includes parities and says they "cannot be dispensed with".  My primary reading is the report's (with
   parities).  I also ran the reading without parities (`--no-parity`).
2. **ν₀.**  The request's number omits ν₀.  For the extremal G, G ≥ 0 and G(d*) = 0, so ν₀ = 0; I verified
   this in all cases.
3. **Hypotheses of the lemma vs the test grid.**
   - §3 assumes Θ ≥ nh + 2mL and n_j ≥ N_u.  HIE-MSG-0001 states the lemma under θ ≥ h only.
   - All 220 cases violate Θ ≥ nh + 2mL (2mL ≈ 35 nats at n = 360).
   - 24 cases have n_j < N_u (for example n_j = 18 or 36 at u = 0.5, where N_u = 41).
   - I ran them anyway, as the request asks.
4. **Θ values.**  Their 4-block cases use θ/h ∈ {1.0, 1.2}, not the request's {1.0, 1.1, 1.3}.  I ran their
   parameter list as stored, plus my own grid with {1.0, 1.1, 1.3}.
5. **The sharp threshold.**  The request says 0.01 and the report says 0.002.  For hidden types the bracket
   equals ν(y) + Θ − nh.  I report that bracket against 0.01.
6. **Readings in R3.**
   - An empty revealed set gives one shell (the empty product), so the next round is plain uniform
     sampling.
   - "Fix a candidate" means the first revealing point.  Check (a) is still applied to every revealing
     point.
   - Round 3 has no neighbours.
   - "Exactly two values" was checked on up to 50 revealing rows per batch, with 0 exceptions.

## 3. Q1 details

**Method.**

- The constraints are closed under pointwise maximum.  So the largest G = −F is the shortest-path function
  G(y) = min over s ∈ V_∅ of t(s) + dist(s, y), where dist uses edges of length u between neighbouring types
  and length 0 inside each class.
- I compute it as a fixed point: an exact L1 distance transform (forward and backward passes along each
  axis), then class minima, repeated.  It converged in 3 sweeps in every case.
- I then verified the result: every step ≤ u, every class constant, and ν ≤ 0 on V_∅.  This held in all
  cases.

**Cross-checks** (`out/q1_crosscheck.txt`).  These share no class code with the main solver.

- *Dijkstra*, on 6 cases with 15 625 to 116 025 types: max |difference| = **0**.
- *HiGHS LP*, on 6 tiny cases with 990 to 6 237 variables.  Equalities were enumerated pairwise from the
  definition.
  - Maximising Σ G: difference **0**.
  - Maximising single G(y), 4 points per case: difference **0**.
  - V recomputed from the LP solution agrees, for example +4.111 at (8, 10, 12) QQT, u = 4, θ = 1.1h.
- *A 7th LP*, at (6, 6, 10, 14) with 8 085 variables, agrees as well.

**Results.**

| | parities (report) | no parities |
|---|---|---|
| cases | 220 | 220 |
| V > allowance | **0** | **0** |
| largest V | **+4.9688** (u = 4, (120,120,120), QQT, Θ = nh) | +4.9523 (theirs: +4.952) |
| V > 5 | 0 | 0 |
| max hidden bracket, Θ ≥ 1.1nh | **+0.617** (mine); +0.0188 (theirs) | +0.617 (mine); +0.0023 (theirs) |
| hidden cases > 0.01 | 6 (2 of theirs) | 4 (0 of theirs) |
| max \|mine − their viol\| | 0.164 (mine ≥ theirs in every case) | **0.0005** |

Hidden-type cases above 0.01 under the parity reading:

- (120, 120, 120) QQT and QTT, u = 0.5, θ = 1.1h: +0.0188.  These are their own cases.
- (30, 30, 50, 70) QQTT:
  - u = 0.5: +0.348 at θ = 1.1h and +0.096 at θ = 1.3h;
  - u = 1, θ = 1.1h: **+0.617**;
  - u = 4, θ = 1.1h: +0.198.

**Re-check of the hidden excesses** (`out/q1_hidden_witness.txt`).

- The witness G is feasible under constraints rebuilt independently (dict classes spread 0, max step
  exactly u, ν ≤ 0 on V_∅).  Any feasible G is a valid profile, so the excess is real.
- Smaller analogues reproduce it, with min-plus and Dijkstra agreeing (and the LP too in the last QQTT
  case):
  - (12, 12, 20, 28), u = 1: +0.408
  - (15, 15, 25, 35), u = 1: +0.618
  - (10, 10, 16, 24), u = 2: +2.345
  - (8, 8, 12, 16), u = 4: +4.382
  - (6, 6, 10, 14), u = 4: +1.333 (min-plus, Dijkstra and LP agree)
  - (20, 20, 30) QQT, u = 0.5: +0.433
- All are far below the allowance.  They refute only the "no logarithmic loss" remark, not the lemma.

**Negative controls.**  Values are V; allowances are given in the first column.  The (36,162,162) and
(50,50,50,50) rows give the hidden bracket instead.

| case | full | no H2 | no H1 | no H1, H2 |
|---|---|---|---|---|
| (120,120,120) PQT, u = 4, 1.1 (allowance 100.3) | −28.7 | +16.5 | −10.0 | +84.2 |
| (120,120,120) QQT, u = 4, 1.1 | +0.017 | +0.017 | +46.2 | +84.2 |
| (20,20,360) QQT, u = 4, 1.0 (allowance 101.9) | +2.28 | +2.28 | +11.0 | +97.7 |
| (36,162,162) PQT, u = 1, 1.1, hidden bracket | −2.78 | +0.12 | +1.63 | +10.9 |
| (50,50,50,50) PQTT, u = 2, 1.1, hidden bracket | −9.68 | +2.98 | −5.09 | +21.0 |
| (400,400,20) QQT, u = 4, 1.0 (allowance 112.7) | +2.52 | +2.52 | **+191.8** | **+198.4** |
| (400,400,20) QQT, u = 4, 1.1 | +0.095 | +0.095 | **+175.5** | **+182.3** |
| (20,400,400) PQT, u = 4, 1.1 | −4.78 | −4.78 | +53.8 | **+189.8** |
| (20,20,960) QQT, u = 4, 1.0 (allowance 115.6) | +5.08 | +5.08 | +10.0 | **+243.1** |
| (20,20,960) PQT, u = 4, 1.3 | −4.78 | −4.78 | −4.78 | **+222.2** |

Bold values exceed the allowance.  Dropping (H2) alone never exceeded the allowance in my cases (V at most
+16.5, hidden bracket at most +3.0).  So a pass at n ≤ 400 shows the lemma is not false at these sizes.  It
is weak evidence about how tight its constants are.

## 4. Q2 details

**Instances** (`q2_r3.py`, seed 20261128, `out/q2_r3.txt`):

- **Block configurations and slopes:** (8,8) at u = 1 and 2; (7,7) at u = 2; (6,6) at u = 1; (6,5,5) at
  u = 1 and 4; (5,5,5) at u = 2; (6,6,4) at u = 0.5.
- **Profile families, each crossed with every configuration:**
  - *hidden:* one dip at a corner of the type grid, depth 0.6u–1.9u;
  - *capped:* the minimum of 0 and 1–3 cones;
  - *cones:* a minimum of cones, no cap;
  - *parity:* half a capped dip plus (u/2)·(d_j mod 2) in one block, a component that no point can reveal.
- F was checked admissible, and A was checked against Σ_d P(d)e^{−F(d)}.

**Outcomes:**

- **(a)** 0 bad candidates out of 14 933 849.
- **(c)** 0 failures out of 31 788 fully revealed runs.
- **(b)** 100/100 tests within 3 standard errors.
  - Only 19 tests have non-zero sampling variance; the other 81 tests revealed all blocks in every run
    (where the SE is below 1e-12·A I set z = 0).
  - The exact conditional mean is unbiased in all runs, to within 1.4e-14.
- **Mutation:** caught in 99/100 tests.  The miss is instance 7 (hidden, (6,5,5), u = 4, M = 100), where the
  mean size of S₂ was 0.08 (almost nothing revealed).  Biased in 32 934/32 934 conditional checks.

## 5. Problems found in their work

1. **Their Q1 script omits the parity allowance that report §3 says is required.**  It therefore checks a
   stronger hypothesis.  Under the report's own definition the values are higher by up to 0.164 nats.
2. **The §3 claim "≤ ν₀ − n(θ − h) + 0.002 at θ ≥ 1.1h" holds only for their case list without parities**
   (+0.0023 there).  It fails in their own cases with parities (+0.0188) and on other block splits under
   either reading (+0.617).
3. **All their test cases violate the lemma's hypothesis Θ ≥ nh + 2mL, and some violate n_j ≥ N_u.**  The
   report does not say so.  HIE-MSG-0001 states the lemma under "θ ≥ h", which is a different hypothesis.
4. **Their extremal function is built by a fixed sequence of passes, not iterated to a fixed point.**  In
   their own reading it still equals the exact maximum, to print rounding, in all 124 cases.
5. **Minor:** the report lists θ/h ∈ {1, 1.1, 1.2, 1.3}, but the 3-block cases use {1, 1.1, 1.3} and the
   4-block cases {1, 1.2}.
6. **R3's description was sufficient** to implement literally, and I found no error in it.  I did not read
   their Q2 scripts.

## 6. Not done, commands and run times

**Not done:**

- Q3.
- Q2 was not run above n = 16, did not check the evaluation count against 3(n+1)^{m+1}M, and ran M = 10⁵ on
  only 4 instances × 4 runs.
- No line-by-line check of the proofs.
- No Q1 case meets Θ ≥ nh + 2mL.  At these n that would need Θ of roughly 2–4·nh.

**Commands**, run from `experiments/eng/phase2_hie_req/` with the project's virtual environment active.
`<hie>` stands for a read-only worktree of the requesting branch at `0ec16b8`.

```
python3 q1_lemma_b.py --their-output <hie>/experiments/phase2_hierarchy/out/h1_relaxation_lemma_check.txt --extra --out out/q1_main.txt                          # 3 min 13 s
python3 q1_lemma_b.py --their-output <hie>/experiments/phase2_hierarchy/out/h1_relaxation_lemma_check.txt --extra --no-parity --out out/q1_main_noparity.txt   # 1 min 52 s
python3 q1_crosscheck.py          # 58 s
python3 q1_negctl_large.py        # 25 s
python3 q1_hidden_witness.py      # 34 s
python3 q2_r3.py                  # 6 min 04 s
python3 make_q1_table.py          # writes the appendix table, out/q1_table.md
```

**Resources:** at most 2 processes at a time, memory well under 2 GB, largest grid 6.8e6 types.
