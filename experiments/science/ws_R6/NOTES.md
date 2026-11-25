# R6 working notes (independent review of theory report §§11.18–11.19)

Reviewer: independent referee, workstream R6, science division.
Repository: /home/user/MetricChain at branch research/scientific-translation (theory files at 5ed4072).
Rules: write only here and in docs/science/workstreams/R6_REPORT.md; no state-changing git; no lake build.

## Log

### Step 0 (start)
- Read COMMON.md and R6_brief.md in full.
- Created this directory. Machine: 4 cores, 15 GB, Python 3.13.18.
- Plan: (1) read §11.18–11.19 for the *specification* only (algorithm + statements), not the cost proof;
  (2) write my own accounting; (3) implement myself; (4) then read their proof, H/K reports, referees,
  D45, ENG-RES-0008 and compare.

### Step 1 (reading for the specification only)
Read in THEORY_REPORT.md: lines 3015-3203 (§11.16: Lemma 11.43, Thm 11.44, 11.45, Prop 11.46), 2283-2372 (Thm 11.25),
3528-3653 (§11.18 up to and including the algorithm text of Thm 11.52; NOT the proof at 3654-3724 yet),
3725-3905 (Thm 11.53, 11.54 with proof of 11.54, remarks), 3905-4003 (§11.19 up to statement of Thm 11.56),
4024-4196 (Prop 11.57, Thm 11.58, remarks). NOT yet read: proof of 11.52 (3654-3724), proof of 11.56 (4004-4023),
K_REPORT, H_REPORT, R7, R8, D45, ENG-RES-0008, any implementation.

### Step 2 (my own accounting for Algorithm 2L, written BEFORE reading the proof at 3654-3724)
Setting: Q_n = Q_o x Q_i, m := n_o = floor(phi n), n_i = n - n_o, W(a) fibre average, p(s) = P(W > s),
levels s_j = s_0 e^j, tolerance b = x_last, G = g n, K, J as in the text.

Deterministic facts (hold in EVERY run, no probability):
 (D1) M <= max(K, 2 M_j^neg) at level j [M is doubled only when M < M_j^neg; ell is constant while a level is unpopulated].
 (D2) a level left as populated has s_{i+1} q_i <= 4 e^{b+1} ell (ell after the update); a level left as negligible has
      s_{i+1} q_i <= e^b ell / J.
 (D3) "closing radius": let r* := largest r <= m-1 with Gamma~(r') <= e^{G-b}/4 for all r' <= r*  (Gamma~(r)=E_r(m)/|B(m,r-1)|,
      Gamma~(0)=e^u-1), pi* := 2^{-m}|B(m,r*)|.  If a level is left without closure then q > pi* at that moment.
      Proof: populated: ell >= s_i e^{-b} q/4, tail = s_i 2^{-m} E_r <= s_i q Gamma~(r) (r=r(q); |B(r-1)| < 2^m q), no closure
      => Gamma~(r) > e^{G-b}/4 => r > r* => q > pi*.  negligible: q <= 2K/M <= ell e^b/(J e s_i), tail <= s_i q Gamma~(r)
      <= ell e^b Gamma~(r)/(Je), no closure => Gamma~(r) > Je e^{G-b} => r > r*.  (r = n_o case: q > 1-2^{-m} >= pi*.)
 (D4) hence after leaving level i: ell >= s_i e^{-b} pi*/4 (populated) or ell > J e pi* s_i e^{-b} (negligible, from
      M_i^neg <= M < 2K/pi*).  So at level j=i+1: M_j^neg <= 8 e^2 K J/pi*, and M <= Mbar := 16 e^2 K J / pi* at every level
      (level 0: M <= max(K, 4KJe^{1-b}) <= Mbar).
 Width: U/ell <= 1 + (J+1) 4e^{b+1} + e^G  (populated levels dominate) => accuracy G + ln(4eJ+3)-ish provided b <= G.

Good event: (V1) all inner brackets valid (incl. width); (V2) for all j and M in {K 2^t}: M p(s_j) >= 2K => at least M p(s_j)/2
 of a_1..a_M have W > s_j; (V3) for all j, M, x in b+N: #{i<=M: W(a_i) > s_j e^{-x}} <= max(2 M p(s_j e^{-x}), K/2).
 Chernoff: each (V2) event fails w.p. <= e^{-K/4}; each (V3) event w.p. <= e^{-K/12}.
 Validity lower end: high => W >= L > s_j e^{-b}; N >= K & V3(x=b) => N <= 2 M p(s_j e^{-b}) => s_j e^{-b} N/(2M) <= A (Markov).
 Validity upper end: V1 => (W > s_j => high); V2 => q >= p(s_j) at every (j,M); layer cake + tail lemma (r <= m-1).
 Count: for x in b+N, level j, M <= max(K,2M_j^neg): let i be the level with s_i <= s_j e^{-x} < s_{i+1} (i<j).
   p(s_j e^{-x}) <= p(s_i) <= q_i <= 4e^{b+1} ell_j / s_{i+1};   M <= 4KJe s_j/(ell_j e^b)
   => M p(s_j e^{-x}) <= 16 e^2 K J e^{j-i-1} <= 16 e^2 K J e^x.   (if s_j e^{-x} < s_0: M <= 4KJe e^{x-b} directly.)
   => #{i<=M: W(a_i) > s_j e^{-x}} <= 32 e^2 K J e^x.
 A point is refined to rung l at level j only if W in (s_j e^{-x_{l-1}}, s_j e^{x_{l-1}-b}] (V1).
 => calls at rung l <= min(Mbar, (J+1) 32 e^2 K J e^{x_{l-1}+1}).
 COST (my bound): 1 + Mbar + sum_{l>=1} min(Mbar, (J+1) 32 e^3 K J e^{x_{l-1}}) C_l.
 Exponents: Mbar -> phi theta_na((g-beta)/phi) (Stirling for Gamma~), count -> (1-phi) xi_{l-1}, C_l -> (1-phi) T(xi_l). OK = (11.18.2)+eta_0.
 Termination on the good event: at level J, N=0 and M_J^neg >= 2KJ e^{11} 2^{m} so M reaches K 2^{m+2}, 2^m q < 1, tail=0.
 Things to compare against their text: the constant in the count; delta' and the union bound over inner calls
 (needs #calls <= something like 2^{n+5} n^3 / L !); the abort rule (must be checked BEFORE an inner call);
 b <= G only for n >= beta/((1-phi)(g-beta)); r* = -1 when e^{G-b}/4 < e^u - 1 (bound void for small n).
