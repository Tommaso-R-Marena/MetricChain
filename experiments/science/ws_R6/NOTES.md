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

### Step 3 (read the proof of Thm 11.52, lines 3654-3724, and compared with my Step-2 accounting)
Term by term: their M-dagger = 2K/pi* (mine), their "every M <= 8Je^2 M-dagger" = my Mbar = 16e^2KJ/pi* (identical);
their count 2M_j^neg p(s_j e^-x) <= 16KJe^2 e^x = mine; with V3: 32KJe^2 e^x + 4K (mine: 32e^2KJe^x, the +4K covers M=K);
rounding x_{l-1} into b+N costs a factor e (same as mine); their cost sum_j sum_l min(8Je^2 M-dagger, 32KJe^3 e^{x_{l-1}}+4K)(l+1)C_l
is an over-count of mine (they charge (l+1)C_l per point and sum over levels; I charge each rung once per point).  AGREE.
Small things found while comparing (all minor, to be listed in the report):
 m-a: the case s_j e^{-x} < s_0 (no level below) is not treated in the count of 11.52 (it is in K_REPORT Step 7); trivial fix.
 m-b: the abort test "if the number of queries exceeds the bound" must be made before an inner call (R8 m1 says so for 11.56;
      the text of 11.52 was not changed).
 m-c: failure budget only "for n >= n_0(eta_0)" -> the assembly "first d tuples whose accuracy is at most x" must also require
      d >= n_0(tuple), or the tuple's procedure is not a bracket procedure with failure probability delta' at small d.
 m-d: accuracy bound gn + ln(4eJ+3) needs b <= G, true only for n >= beta/((1-phi)(g-beta)).
 m-e: l = 0 term / reference query missing in the displayed cost sum (x_{-1} undefined).

### Step 4 (derived the 2L+ analysis from the statement of Thm 11.56 before reading K_REPORT 2.4; then read K_REPORT 1-4)
Derived on my own from the four changes: width (2p_u)^n + e^b(e^lam(1+eta)/(1-eta) + eta' + theta); closing radius conditions
[N] Gamma~ <= theta(1-eta)nu0 and [P] min(Gamma~/c_eta, Gamma'') <= theta; Mbar = 2(1+eta)e^lam nu0 K/((1-eta)pi-dagger);
count M_j^neg p(s_j e^-x) <= c_eta^-1 e^lam nu e^x.  All four agree with K_REPORT Steps 4-7.
Read K_REPORT lines 1-650 (sections 0-5 start).  Checked line by line: good event and K (V2,V3 Chernoff constants OK;
number of events (J+1)(m_max+1)(L+2) OK; no circularity J->nu0->r-dagger->pi-dagger->m_max->K->nu,Mbar->delta');
Steps 1-9; Lemma K.4 (a)-(d); Prop K0; Cor K1.b; Prop E (a),(b); Thm K2 (accuracy arithmetic 5.25 c0 <= x/2 - eps OK); Thm K3 iteration.
No error found so far.  D45 read (five accountings: single threshold; v1; v2; v4; CLOSE).  H_REPORT read (2.6 = original 2L, 2.8 = the wrong ones).
NEXT: implement from the spec (K_REPORT 2.2 + theory report 3616-3652) BEFORE reading any implementation; then R7/R8, Lean, ENG-RES-0008.

### Step 5 (coordinator note received mid-work; new theory checkpoint 40c5bd7)
The coordinator informed me that the theory division published checkpoint 40c5bd7 while I work at 5ed4072.  Read (read-only):
`git diff 5ed4072 origin/claude/determined-ride-og1u7j -- docs/workstreams/K_REPORT.md` (errata e1-e4 added) and the two new
remarks after Thm 11.56 in the 40c5bd7 theory report (extracted to scratchpad, lines 4117-4160 of that version).
 (1) New remark "sample-size cap": in every run every sample is K or has fewer than 2 max{e^lam M-dagger, M-ddagger} points,
     M-ddagger = K/((1-eta) pi-ddagger), pi-ddagger = 2^-n_o |B(n_o, r-dagger - Delta)|, Delta = ceil(lam/u)
     (M-ddagger := K 2^n_o/(1-eta) if r-dagger < Delta).  [P], unrefereed.
     MY RE-DERIVATION (done on paper now): correct for r-dagger >= Delta.  Steps checked: level 0 is populated at M=K in every run
     (rung-0 bracket has L > s_0 e^-b because psi(a,0) <= psi_0 + u n_o: no inner call involved) ; case "after negligible": OK;
     case "after populated": p_low > c_eta pi-dagger, Harper radius >= kappa(r-dagger+1), E_{r-1} <= e^-u E_r (term by term, OK),
     tail <= s_{j-1} e^{lam - u Delta} 2^-n_o E_{r-dagger}; [P] at r-dagger gives tail <= theta e^b ell in both sub-cases
     (also for r-dagger = 0 with the convention Gamma~(0) = e^u - 1).  OK.
     EDGE (to test numerically): if r-dagger < Delta and M = M-ddagger = K 2^n_o/(1-eta) exactly lies in the doubling sequence
     (eta = 1/2), then q = 2^-n_o, 2^n_o q = 1 is NOT < 1, the tail is s_j 2^-n_o (e^u - 1) and closure is not forced; the sample
     may then be doubled to exactly 2 M-ddagger: "fewer than" could fail by equality in the corner 1 <= r-dagger < Delta (needs lam > u).
     Also re-derived the 2L version: an unpopulated pass with M >= max{M-dagger, M_j^neg/(4Je)} closes; hence M < 2e M-dagger.  OK.
 (2) New remark "radial landscapes are almost the whole class for the outer loop" (Harper: tail functions of all u-Lipschitz outer
     landscapes = those of landscapes whose level sets are initial segments of the simplicial order).  Consequence for my harness:
     with a simulated inner oracle only the LAW of W(a) matters; I represent an outer landscape by classes (value, probability).
 (3) Flat-instance cost numbers are best-case numbers (K_REPORT erratum e1).
All findings in my report will be tagged with the commit they refer to (5ed4072 unless stated; the cap remark is 40c5bd7).
