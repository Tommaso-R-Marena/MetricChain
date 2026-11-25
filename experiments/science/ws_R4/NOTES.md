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
