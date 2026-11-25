# R4 notes — review SCI-REV-0003 of theory report §11.24 (rounds of adaptivity)

Referee: workstream R4 (independent).  Started 2026-11-25.
Rule: updated after every step.  Own code first, authors' code only afterwards.

## Step 0 — set-up
* Read COMMON.md and R4_brief.md.  Created `experiments/science/ws_R4/`.
* Repository head: 49110f8 (science branch), theory content at 5ed4072.
* §11.24 is at line 5568 of docs/THEORY_REPORT.md (to 5791).

## Reading order (planned)
1. §11.24 (the object).  2. §11.16, §11.18, §11.19 as needed.  3. U_REPORT.md.
4. TwoRounds.lean.  5. DEAD_ENDS D45, D50.  6. R7, R8 referee reports.
7. Authors' code LAST (experiments/workstreams/U, experiments/coordinator_checks/rounds_U).

## Step 1 — reading (no authors' code opened)
Read: THEORY_REPORT §11.24 (lines 5568-5791), §11.16 (3015-3203), Thm 11.25 (2283-2370),
§11.18 (3528-3904), §11.19 (3905-4196), U_REPORT.md (whole), TwoRounds.lean (whole, 308 lines).

Conventions fixed (important, the sign is easy to get wrong):
* L_u(Q_n) = u-Lipschitz psi wrt Hamming distance; w = e^{-psi}; A = 2^{-n} sum_x w(x);
  correct = |output - ln A| <= eps/2 with prob >= 1-delta for EVERY member.
* p_u = 1/(1+e^u); Lambda_1 = ln(2/(1+e^{-u})); f(rho)=KL(rho||1/2); k(rho)=KL(rho||p_u)=f+u rho-Lambda_1;
  a = f(p_u); h = f(Lambda_1/u); theta_na(e) = min{f(rho): k(rho)<=e}; theta_hint(e)=f((Lambda_1+e)/u).
* D(theta) = u f^{-1}(theta) - Lambda_1; x_na(theta) = D(theta)+theta = k(f^{-1}(theta)).
* block-radial: psi_s(x) = F(d(x^1,s^1), d(x^2,s^2)); A(F) = sum_d P_1(d_1)P_2(d_2) e^{-F(d)}.

First-pass re-derivation (by hand, before any code):
* Lemma 11.85, r=2: virtual-run argument re-derived; correct.  Observation: "batch sizes at most
  M_t" must hold for the VIRTUAL run (first batch answered by G_1(d_1)); in the application G_1 = g_1
  and x -> g_1(d(x^1,s^1)) IS a member of L_u, so the bound needed is on class members only, and the
  expected-size version E|B_1| p_1 + E|B_2 on g_1-instance| p_2 >= 1-2 delta follows directly (no Markov).
* Thm 11.86 mass of type (p_u,p_u) under F_D: second alternative -> phi_2 k(y^1); first -> Xi.  Re-derived.
* theta_2^* > h: E_theta(c) = c + u(phi_1 z + phi_2 rho^s) - Lambda_1 >= c + D(theta) (Jensen), D(h)=0; OK.
* Lean: TwoRound = (first : Finset X, second : (X->R)->Finset X, output) with congruence axioms;
  card_distinguished_le / two_round_bound say what the prose says for r=2 (abstract S_1,S_2,W_1,W_2,v);
  hM2 is required for ALL f (stronger than needed); randomness = finite Omega with weights.
  two_round_witness shows hypotheses are jointly satisfiable.  To do: compile + #print axioms.

Open questions for myself (to test numerically BEFORE believing):
 Q-a  exact finite-n twins: Lipschitz, coincidence, gap, p_1, p_2 (own code).
 Q-b  theta_2^*(u)/a, T^(2)(0)/a, h/a (own code).
 Q-c  is "tau^(2)" well defined (total cost vs batch, expected vs worst)?
 Q-d  Claim A/B of Thm 11.84 vs Algorithm 2L+ as written in K_REPORT §2.2.
 Q-e  README headline: which regime exactly.

## Step 2 — own exponent code (exponents.py; written before reading any authors' code)
First version (scalar brentq inside Python loops) too slow on the shared machine (load avg 16); killed
after 10 min, rewritten vectorised (same formulas).  Output: out_exponents_u1.txt  (7.5 min wall, 2 min CPU).
MY VALUES at u = 1:
  a = 0.11094407, h = 0.02913914, h/a = 0.26265
  theta_2^* = 0.03987221, theta_2^*/a = 0.35939, theta_2^*/h = 1.36834, best phi_1 = 0.6406
  T^(2)(0)/a = 0.62432 (2-d grid directly from the statement AND the balance formula a(a+xi)/(2a+xi-theta_na(xi)));
     optimal phi = 0.5555, xi = 0.04488
  small-slope limit: theta_2^*/a = 0.346035, theta_2^*/h = 1.38414, phi_1 = 0.654; T^(2)(0)/a = 0.618034 = (sqrt5-1)/2,
     at sqrt(xi/a) = 0.61803
  Xi(h, phi_1) > 0 at phi_1 = 0.1,0.3,0.5,0.64 (u=1: +0.0020,+0.0064,+0.0113,+0.0152); small slope +0.0171,+0.0540,+0.0958,+0.1318
  theta -> Xi(theta, phi_1) is decreasing on (0, phi_2 a) on a 60-point grid (justifies bisection).
=> agree with the report's 0.359 / 1.37 / 0.64 / 0.624 / 0.346 / 1.38 / 0.65 / 0.618 to all printed digits.
Other slopes (0.5, 2, 3) to be run in the background later.

## Step 3 — exact finite-n twins (twins_exact.py; own implementation from the statement of Thm 11.86)
Outputs: out_twins_u1_small.txt, out_twins_u1_large.txt, out_twins_u2.txt.
For each (n, split n1/n in {0.45,...,0.65}): bisection for the largest budget T with gap > 1; ALL structural
checks pass on every pair (u-Lipschitz in each argument: FD, FS, Fcap; FD=FS=g1 on W1; FD=FS on V2; W1 subset V2;
A(F_S) <= (n1+1)(n2+1) and every type mass <= 1; p1 <= (n1+1)(n2+1)e^-T; p2 <= (n2+1)e^-T; twins differ only
outside V2).
  u=1:  n=400  E=0.03005 (n1=180)   all-algorithms 0.03477   | report: 0.0301 / 0.0348
        n=800  E=0.03411 (n1=360)   all 0.03234              | report: 0.0341 / 0.0323
        n=1600 E=0.03543 (n1=800)   all 0.03092              | report: 0.0354 / 0.0309
        n=3200 E=0.03684 (n1=1760)  all 0.03011              | report: 0.0368 / 0.0301
  u=2:  n=200  E=0.11294 (n1=90)    all 0.11164              | report: 0.1129 / 0.1116
        n=400  E=0.11520 (n1=180)   all 0.10441              | report: 0.1152 / 0.1044
        n=1600 E=0.12117 (n1=880)   all 0.09934              | report: 0.1212 / 0.0993
=> the coordinator's table in section 11.24 REPRODUCED to all printed digits with independent code.
Observation: at n=400,u=1 the two-round bound (0.0301) is BELOW the bound for all algorithms (0.0348): the
twins say nothing there; crossover between n=400 and 800 (as the report says).
Observation (headline): the comparison at n=3200 is between two LOWER bounds.  No adaptive algorithm is known to
cost less than e^{0.037 n} at n=3200 (section 11.19: two levels cost 0.55a=0.061n at n=4000 at the flat instance,
three levels 0.46a=0.051n).  So the finite-n sentence is not a separation at n=3200; the separation is asymptotic.

## Step 4 — Theorem 11.84 against Algorithm 2L+ as written (K_REPORT §2.2, read in full §§1-3.4)
Paper check, line by line:
* Claim A (on G'): call (i,l) at level j, pass M >= i  =>  M <= max{K, 2 nu s_j/(l_j e^b)} (K1(iv), l_j = value at
  entry of level j, which is what step (e) uses); need l_j >= lambda_j: populated i': q <= pbar/c_eta, l >= s e^-b pbar;
  negligible i': s q <= e^b l/((1-eta)nu_0) <= e^b l; q_i' >= p(s_i') (Step 2); (V3') gives p(s_i') >= N_L/((1+eta)M').  OK.
* Claim B: stored lower ends >= s_0; member i>K with witness j has L_i > s_j e^{-x_{l-1}} PROVIDED the stored
  bracket of rung l-1 has ratio <= e^{x_{l-1}}; counted in N_L(i',M*); M* > K (the parenthesis "< K/2" in U_REPORT
  is garbled; correct reason: i > K and i <= 2 nu s_j/(lambda_j e^b) force 2 nu s_j/(lambda_j e^b) > K);
  M* <= 4 nu s_j/(lambda_j e^b); count <= 4(1+eta)c_eta^-1 e^lambda nu e^{x_{l-1}}.  OK.
  !! "in every run" (theory report (ii)) needs the stop rule "a stored bracket of rung l-1 wider than e^{x_{l-1}}
  => stop BEFORE stage l"; U_REPORT puts this rule under *Output*, the theory report omits it.  Minor (an explicit
  abort "if |C_l| > N_l" repairs it).
* Rounds: base bracket (Prop. K0) has M fixed in advance from (d,x,delta') => one batch.  Stage 1 = reference
  point + trivial brackets + I_1 on all M_max fibres: no evaluation depends on another of the same stage.  OK.
* Two rounds: L=2, x_1 = xi n_i (one-round bracket, cost e^{n_i theta_na(xi)}), x_2 = b = x/2 (one-round bracket of
  bounded accuracy, e^{n_i a + O(sqrt n_i)}), M_max = e^{phi a n + O(sqrt n)}, |C_2| <= min(M_max, poly e^{xi n_i})
  => exponent max{phi a + (1-phi) theta_na(xi), min(phi a,(1-phi)xi) + (1-phi) a}.  OK.
* Looseness: "Theorems 11.54 and 11.58 hold ... independently of n" — the o(n) in those theorems needs the number of
  levels -> infinity; what holds with n-independent rounds is: for every eta there is r(eta) with tau^(r) <= h+3 eta.

## Step 5 — small cubes and an end-to-end test of Lemma 11.85 (small_cube.py -> out_small_cube.txt, 15 s)
Part A (7 configurations, n = 12..16, u in {0.5,1,2,3}): psi_D, psi_S as functions on all 2^n points with a random
centre: largest edge difference EXACTLY u; ln A by enumeration = type sum to 10 digits; equal on V2; = g1 on W1;
fraction of points outside W1 / V2 = p1 / p2 (h1,h2 of the Lean lemma hold with equality by translation
invariance x -> x xor s).  One configuration (8,6,T=4.5) is degenerate (W2 = everything, twins identical).
Part B: posterior-greedy two-round distinguisher (a REAL two-round algorithm; batch 2 chosen greedily on the
posterior after batch 1), exact count over ALL centres: 144 tests, 0 violations of (#distinguished)/2^n <= M1 p1 + M2 p2;
largest fraction/bound = 0.777 (the bound is nearly attained by a real algorithm at these sizes);
two rounds beat one blind batch of the same total size (e.g. 0.361 vs 0.219 at (6,6), 4+4 points).

## Step 6 — Lean (lean/AxiomCheck.lean -> lean/out_AxiomCheck.txt; source file elaborated from scratch)
* `lake env lean proofs/Frontiers/TwoRounds.lean`: exit 0, no output (no error, no warning, no sorry). sha256 0113907b...
* axioms of output_eq_of_virtual, card_distinguished_le, prob_output_ne_ge, two_round_bound, two_round_witness:
  [propext, Classical.choice, Quot.sound] only.
* Statement read: X arbitrary type, S1,S2 finite, deterministic TwoRound = (first, second, output + 2 congruences);
  randomness = finite Omega with weights P >= 0 summing to 1; hM1: forall omega; hM2: forall omega AND forall f : X -> R
  (all functions, not only class members); conclusion 1 - 2 delta <= M1 p1 + M2 p2.

## Step 7 — asymptotic formula vs exact twins (asymptotic_check.py -> out_asymptotic_u1_phi06.txt, 32 s)
u=1, phi1=0.6, n=800/3200/6400: exact gap/n vs gamma = min(Xi, phi2 k(y1)):
  theta=0.75h: gamma .00440 | .00585 .00451 .00443      theta=h: .00179 | .00208 .00162 .00166
  theta=1.15h: .00085 | .00111 .00060 .00066            theta=1.25h: .00044 | .00067 .00023 .00023
  theta=1.33h: 0 (Xi<0) | .00048 .00010 .00007          theta=1.40h: 0 | .00034 .00004 .00000
Heaviest type of F_D at (0.269,0.269) = (p_u,p_u) in every case with a positive predicted gap.  Consistent with
"ln A(F_D) - ln A(F_S) >= n gamma - O(log n)" (ln(6400)/6400 = 0.0014).  lnA_S/n -> 0 (0.0008 at n=6400).

## Step 8 — AFTER my own code: read the coordinator's scripts (experiments/coordinator_checks/rounds_U) and
skimmed the workstream's (experiments/workstreams/U/code).
* u_check2.py is an independent implementation of the same statement; its table (n1, T/n, gap, E) coincides with
  mine in every printed digit (e.g. n=3200: n1=1760, T/n=0.03928, E=0.03684).  Its k* is my k*+1 (open-ball
  convention: uses |B(n,k-1)|); same bound.
* workstream's lb2_exact.py uses a different W2 ("balance": smallest central interval with p2 <= p1; W1 not inside V2,
  bound (1-2 delta)/(p1+2p2)) -> its E differs in the 3rd digit (0.0339/0.0360/0.0366), as the report says.
* u_check1/3: T2(0)/a = 0.6243 at u=1 (mine 0.62432); T3(0) <= 0.5406a via ladders (1,1,1), (2,1), (1,2).
  Theorem 11.84: "no script" (paper check only) by the coordinator; simulation only by the workstream.

## Step 9 — own Lean strengthening (lean/TwoRoundsExpected.lean -> out_TwoRoundsExpected.txt; exit 0;
axioms propext, Classical.choice, Quot.sound only)
* card_distinguished_le_sum: #distinguished <= |B1| p1 N + (sum_{s1} |B2(v s1)|) p2 |S2|.
* two_round_expected_bound: 1 - 2 delta <= E|B1| p1 + E_{omega,s1}|B2(v s1)| p2  (NO bound on batch sizes assumed).
* two_round_expected_cost:  1 - 2 delta <= p * E_{omega,s1}[ |B1| + |B2(v s1)| ]  if p1,p2 <= p.
* two_round_bound_of_class: worst-case form with hM2 only for f in the class G (needs v s1 in G).
Meaning for Thm 11.86: v s1 = g1(d(x^1,s1)) is in L_u, so every (eps/2,delta)-correct two-round algorithm makes at
least (1-2 delta) e^{n theta}/(n+1)^2 evaluations IN EXPECTATION AT THE FLAT-HISTOGRAM INSTANCE of the first block
(averaged over its centre) — the exact analogue of Thm 11.25(a) "at the zero function".  Closes the workstream's
"extension to expected batch sizes: only the Markov remark".
