# MBAR strengthening: independent mathematical derivations (v2)

Status: informal proofs, not Lean-checked, and novelty not yet certified. This is a replacement research note for the central claims in the original handoff, not a claim that every theorem in the old manuscript is correct. All arithmetic below is in exact real arithmetic. Code is a float64 reference implementation.

## Common model

There are K>=2 states on a common measure space, measurable nonnegative finite unnormalized q_k, 0<Z_k=∫q_k<∞, p_k=q_k/Z_k, f*_k=-log Z_k. Zero q is allowed; on a sampled point its own state's q is positive a.s. Fixed independent stratified counts n_k>0, N=sum n_k, s_k=n_k/N, S=diag(s). Define m=∑s_k p_k, π_k(f,x)=s_k exp(f_k)q_k(x)/∑s_j exp(f_j)q_j(x). At truth π*=s_k p_k/m, and expectation under m of π* is s. Gauge H=1^perp. The empirical objective is ℓ(f)=N^{-1}∑log(∑s_k exp(f_k)q_k(x_n))−sᵀf, its score g(f)=mean(π(f,x_n))−s, its Hessian H_N(f)=mean(diag π−ππᵀ), and L=E H_N(f*). Assume connected population support overlap for the spectral results. All inverses of Laplacians below are on H; extend by zero on constants. R_c=cᵀL^+c, R=max_{i<j} R_{e_i−e_j}, d=(K−1)−tr(S^{-1}L). Write ||u||_L²=uᵀLu, ||g||_{L+}²=gᵀL^+g. For a connected M, |u_i−u_j|≤√R_ij(M)||u||_M, by Cauchy–Schwarz on H. Thus osc(u)≤√Rmax(M)||u||_M. All contrasts have sum zero.

## A. True asymptotic variance is globally convex (stronger than original Theorem 9)

### Theorem A1 (perspective characterization)

Fix p_1,…,p_K, with connected support overlap. Extend the allocation to arbitrary positive weights s∈(0,∞)^K; m_s=∑s_k p_k, π_s,k=s_k p_k/m_s, L(s)=∫m_s(diag π_s−π_sπ_sᵀ). For every c∈H,

V_c(s)=cᵀL(s)^+c−∑c_k²/s_k

is nonnegative, convex on the positive orthant, continuously differentiable, and homogeneous of degree −1. On the simplex it is exactly N times the usual i.i.d. stratified MBAR asymptotic variance. It satisfies the representation

V_c(s)= min_{r∈F_c} ∑_k (1/s_k)∫p_k r_k²,

where F_c is the **allocation-independent affine set** of measurable r_k∈L²(p_k) satisfying E_k r_k=0 and ∑p_k r_k=−∑c_k p_k almost everywhere. In particular, any nonnegative sum or pointwise maximum of such contrast variance objectives is convex (maximum need not be differentiable).

Proof. Let v=L(s)^+c, z(x)=∑π_s,k(x)v_k, μ_k=E_k z. All z and μ are bounded between min v and max v. Since (L v)_k = s_k(v_k−μ_k)=c_k, μ_k=v_k−c_k/s_k. Define r_k*=s_k(μ_k−z). Its state mean is zero and

∑p_k r_k*=∑s_k p_k(v_k−c_k/s_k)−m_s z=−∑c_k p_k,

so it is feasible. For any other feasible r, d_k=r_k−r_k* has E_k d_k=0 and ∑p_k d_k=0 a.e. Orthogonality in the weighted Hilbert space gives

∑ E_k(r_k* d_k)/s_k=∑ μ_k E_k d_k−∫ z ∑p_k d_k=0.

Consequently objective(r)=objective(r*)+∑ E_k d_k²/s_k. The minimum equals ∑s_k Var_k(z). Directly,

∑s_k Var_k(z)=∫m_s z²−∑s_k μ_k²
= vᵀ(S−L)v−∑s_k(v_k−c_k/s_k)²
= vᵀc−∑c_k²/s_k=V_c(s).

For s,t>0 and λ∈[0,1], rλ=λr*(s)+(1−λ)r*(t) belongs to F_c. Pointwise convexity of (r,w)↦r²/w for w>0 (Cauchy–Schwarz / perspective inequality) implies objective(rλ,λs+(1−λ)t)≤λV_c(s)+(1−λ)V_c(t). Minimizing proves convexity. Nonnegativity follows from the square representation. Homogeneity follows from L(as)=aL(s). QED.

This proof is algebraic and does not assume an unproved statistical efficiency theorem: it verifies the minimizer explicitly. It works for arbitrary measurable distributions, not just finite support. It also supplies a stable nonnegative evaluation formula that avoids subtracting nearly equal resistances.

### Theorem A2 (true variance gradient and allocation conditions)

For v,z above,

∂V_c/∂s_k = −Var_{p_k}(z), and ∑s_k Var_k(z)=V_c(s).

Proof. For fixed v, the integrand of vᵀL(s)v is ∑s_k p_k v_k²−(∑s_k p_k v_k)²/m_s. Its partial derivative is p_k(v_k−z)²; it is dominated by p_k osc(v)², so differentiation under the integral is justified locally. L is smooth on the positive orthant and invertible on H. Differentiate inverse: ∂R_c/∂s_k=−E_k(v_k−z)². Differentiate the correction −c_k²/s_k, and use E_k(v_k−z)=c_k/s_k. This yields −Var_k(z). QED.

On a compact restricted simplex s_k≥ε>0 (Kε≤1), a minimum exists and all local minima are global. At an interior optimum all state variances Var_k(z) equal V_c(s); at a lower-bound active coordinate the variance is <= the common multiplier on free coordinates. With real-valued sample amounts s and costs a_k>0, constraint ∑a_k s_k=B, the same proof applies on a compact positive restricted budget polytope. At an interior optimum Var_k(z)/a_k is constant and equals V_c(s)/B. Actual sample counts are discrete; rounding is a separate issue. A fixed pilot provides estimates of z and its statewise variances, not an exact population gradient. Adaptive sampling, convergence of stochastic optimization, correlated dynamics, and finite-sample optimality are not established by A1/A2. The result only concerns the i.i.d. asymptotic variance.

## B. Finite-sample upper bounds: complete constants and explicit remainder

### B1. Deterministic localization

For any dataset, at any base f and h,u, differentiation of log-sum-exp gives D³ℓ(f)[u,u,h]=E_π[(u−E_πu)²(h−E_πh)] averaged over samples; its absolute value <=osc(h) uᵀH_N(f)u. This includes zero q (restrict to active terms); integrate to get e^{-t osc(h)}H_N(f)≼H_N(f+th)≼e^{t osc(h)}H_N(f). Constant 1 is approached for binary probabilities tending to zero and u=h=(0,1). Let M=H_N(f) connected, b=||g(f)||_{M+}, δ=√Rmax(M)b. For δ<1, the optimizer exists uniquely on H and h=fhat−f obeys osc(h)≤r=−log(1−δ), ||h||_M≤(r/δ)b, and |cᵀh|≤√(cᵀM^+c)(r/δ)b. For δ=0 interpret r/δ=1.

Proof: on the boundary osc(h)=r'>0, integration of directional curvature gives (g(f+h)−g(f))ᵀh ≥ ||h||_M²(1−e^{-r'})/r'. Subtract b||h||_M, and use ||h||_M≥r'/√Rmax(M). For r'>−log(1−δ), this gives g(f+h)ᵀh>0, so minimizing on the compact oscillation ball on H yields an interior stationary point (at boundary, moving toward center decreases loss). Hessian comparison implies strict convexity globally on H. Let r' decrease. At the optimizer, Cauchy–Schwarz in the same integrated inequality bounds ||h||_M by b osc(h)/(1−e^{-osc(h)})≤br/δ. QED.

### B2. Exact score covariance

Let P0=E_m[π*π*ᵀ]=S−L. Conditional mean μ_k=E_kπ*=P0 e_k/s_k (column convention). Stratified covariance is N Cov(g*)=P0−P0 S^{-1}P0=L−LS^{-1}L=:Σ. Thus 0≼Σ≼L, E||g*||²_{L+}=d/N and for c∈H the variance of cᵀL^+g* is V_c(s)/N. The trace identity uses cyclicity and LL^+L=L. Since each centered π difference has inner product with a vector w bounded in absolute value by osc(w), a whitened centered summand divided by N has Euclidean norm <=√R/N. Also one-draw Hessian A satisfies wᵀAw=Var_π(w)≤osc(w)²/4≤R wᵀLw/4 (Popoviciu follows from E[(X−a)(b−X)]≥0 and maximizing the resulting quadratic in EX).

### B3. Explicit global upper bound

Let t=log(2K/α), x=N/R, B=√(2dt/N)+2√R t/(3N). If x≥(48d+16)t, then with probability ≥1−α a finite unique MBAR solution exists, H_N(f*)≽L/2, δ≤1/2, and simultaneously for every c∈H,

|cᵀ(fhat−f*)| ≤ 4 log(2) √R_c B.

Proof. Whiten Hessian on H, where dimension is K−1. Summands B_n=L^{-1/2}A_n L^{-1/2} are PSD with upper bound (R/4)I, and ∑EB_n=NI. Matrix Chernoff LOWER tail at ε=1/2 gives failure ≤(K−1)exp[−N/(2R)]≤α/2 under threshold. The theorem does not require the upper tail. Apply rectangular matrix Bernstein to centered whitened score vectors (viewed as (K−1)×1 matrices). Dimension prefactor K, variance parameter ≤d/N (the scalar sum E||z_n||² is exactly d/N, dominates matrix variance), summand bound √R/N. Standard Bernstein inversion gives ||g*||_{L+}≤B except with probability Ke^{-t}=α/2. Union. On event, M=H_N(f*)≽L/2 so ||g*||_{M+}≤√2 B and Rmax(M)≤2R. Hence δ≤2√R B=2√(2dt/x)+4t/(3x)≤1/√6+1/12<1/2. B1 and r/δ≤2log2 give the displayed coefficient 4log2, not the original 2√2log2. If d=0 the score is zero a.s., and exact localization applies. No energy moments needed.

### B4. Contrast-sharp bound with explicit Hessian and nonlinear remainder

Let 0<α<1, a=log(6K/α), b=log(6/α) for a fixed contrast (or b=log(6M/α) for a predeclared list of M≥1 contrasts). Define

B=√(2da/N)+2√R a/(3N),
η=√(Ra/(2N))+Ra/(6N), u=√R B,
δ0=u/(1−η), r0=−log(1−δ0),
κ=1/[(1−η)(1−δ0)]−1.

Require η<1 and δ0<1; otherwise this theorem abstains. With probability ≥1−α the estimator exists uniquely and for each specified contrast,

|cᵀ(fhat−f*)| ≤ √(2 V_c(s) b/N) + 2√(R R_c)b/(3N) + √R_c κ B.

Proof. Whitened Hessian summands B_n as above have 0≼B_n≼qI, q=R/4, and ∑EB_n=NI. Necessarily q≥1. Centered summands (B_n−EB_n)/N have norm ≤q/N, since both matrices lie between 0 and qI. Their total matrix variance ≼qI/N, because E(B_n−EB_n)²=EB_n²−(EB_n)²≼q EB_n. Two-sided matrix Bernstein gives norm deviation ≤η except probability 2(K−1)e^{-a}≤α/3. Rectangular score Bernstein gives ||g*||≤B except probability Ke^{-a}≤α/6. On these events (1−η)L≼M≼(1+η)L, δ≤δ0 and osc(h)≤r0 by B1. The integrated Hessian T=∫_0^1H_N(f*+th)dt satisfies (1−η)e^{-r0}L≼T≼(1+η)e^{r0}L. Since h=−T^+g*, the whitened inverse difference has norm <=κ: upper excess is e^{r0}/(1−η)−1, which dominates the lower excess 1−e^{-r0}/(1+η). Therefore |cᵀ(h+L^+g*)|≤√R_c κ B. Separately, scalar Bernstein for the linear score −cᵀL^+g* has variance V_c/N and per-centered-summand bound √(RR_c)/N by the oscillation inequality; two-sided tail at b has failure ≤2e^{-b}, union over M if needed. Sum event failures ≤α. QED.

For fixed problem geometry and fixed K, remainder terms are O(N^{-1}) as N grows, with the actual variance V_c in the leading N^{-1/2} term. For growing K, small overlap, or vanishing V_c, the exact formula, not a uniform dimension-free claim, must be used. The theorem supplies sufficient conditions, not necessity. The matrix Bernstein/Chernoff theorems are standard cited external results, not newly proved here. References: J. A. Tropp, User-Friendly Tail Bounds for Sums of Random Matrices, FoCM 2012, arXiv:1004.4389, Theorems 5.1, 6.1/rectangular extension; use the usual inversion sqrt(2vt)+2bt/3. See also Bach 2010 on self-concordant logistic analysis.

### B5. Valid normal approximation, with transparent rather than optimized constants

Define a data-measurable estimator: the unique finite gauge-fixed minimizer when the directed support graph in E1 is strongly connected, zero otherwise. For V_c>0 let σ=√(V_c/N), β=V_c/R_c. Let a=log(6K/α), η,δ0,κ,B as B4. If the threshold is satisfied, the same score/Hessian event alone has failure ≤α. For the standardized linear score, sum of absolute third moments divided by σ³ is ≤√(RR_c)/(Nσ)=1/√(β x) where x=N/R. The independent nonidentically distributed Berry–Esseen theorem with constant 0.56 applies. On the event the difference of standardized estimator and linear score is bounded by √R_c κ B/σ. Hence

sup_z |P(cᵀ(fhat_ext−f*)/σ ≤ z)−Φ(z)| ≤ min(1, 0.56/√(β x) + √R_c κ B/(σ√(2π)) + α).

Proof: sandwich the estimator CDF between the linear CDF at z±remainder, up to event failure, and bound normal CDF variation by the maximum standard normal density. For thresholds that fail, use trivial bound 1. One can choose α as a deterministic function of population parameters for an analysis bound, e.g. min(1/2,x^{-1/2}); this is not a data-computed interval. No claim that Gemini's earlier explicit constants are correct. This fixes the original nonobservable fallback issue and retains explicit nonlinear remainder.

## C. Two genuinely observable statistical certificates

Both certificates require equilibrium i.i.d. sampling as specified. They control P(any erroneous confidence statement is issued)≤α, not P(error | certificate issued)≤α. A certificate may abstain. They neither verify sampling equilibrium nor certify floating-point rounding errors.

### C1. No-split cut-score certificate for any data-dependent center

Let f0 be any finite data-dependent center, not necessarily the MBAR optimizer. Compute M=H_N(f0), g0=g(f0), and if M is connected define

ε=√[(K log 2+log(1/α))/(2N)] + ||g0||_1/2,
q=Rmax(M) ε.

If M disconnected or q≥1 return radius +∞; otherwise radius r=−log(1−q). With probability ≥1−α simultaneously for all pairs |(f*_i−f*_j)−(f0_i−f0_j)|≤r. For arbitrary contrast c, |cᵀ(f*−f0)|≤r ||c||_1/2. The statement is valid for data-dependent selection of the center, since the sole probability event below does not depend on it. No unknown population parameter is used in the calculation.

Proof. For each nontrivial cut A, g_A(f*)=mean(π_A(f*,X))−s_A is a sum of independent bounded [0,1] observations minus its expectation. Hoeffding gives P(|g_A|>ε0)≤2e^{-2N ε0²}. Complementary cuts have the same absolute value, so union over 2^{K−1}−1 cuts gives ≤α at ε0=√[(K log2+log(1/α))/(2N)]. For any zero-sum vector y, max_A|∑_{i∈A}y_i|=||y||_1/2 (take the set of positive coordinates). For any h, |yᵀh|≤osc(h)||y||_1/2. Thus for h=f*−f0, (g(f*)−g0)ᵀh≤ε osc(h). B1's integrated curvature at f0 bounds this quantity below by ||h||_M²(1−e^{-osc(h)})/osc(h)≥osc(h)(1−e^{-osc(h)})/Rmax(M). Divide if osc(h)>0 to obtain 1−e^{-osc(h)}≤q; inversion proves the assertion. No union over possible f0 needed. QED.

This certificate is computationally cheap (the exponential cut count appears only in its logarithm) but its sufficient sample size scales conservatively like K Rmax². It is a genuine operational confidence bound, not necessarily the tightest or most useful one in weak overlap. Use C2 to improve weak-overlap behavior. An approximate fitted center must use its actual Hessian and score residual; S(I−O) identity requires exact stationarity. If numerical rank is uncertain, abstain.

### C2. Holdout bounded bridge identities + difference-constraint closure

Choose an arbitrary finite vector a∈R^K and an edge set E before seeing validation samples; a and E can be chosen using an independent pilot. Define w_j(x)=exp(a_j)q_j(x)/∑_k exp(a_k)q_k(x). Let A_ij=E_i w_j and B_ij=E_j w_i. Then for each edge (i,j), when the shared support has positive measure,

A_ij/B_ij = exp(a_j−a_i) Z_j/Z_i,
f*_j−f*_i = a_j−a_i+log B_ij−log A_ij.

Proof: numerator and denominator expectations share the integral ∫q_i q_j/(∑exp(a_k)q_k), with prefactors exp(a_j)/Z_i and exp(a_i)/Z_j. The weights are bounded in [0,1] regardless of force-field tails. If the integral is zero, both expectations vanish and the edge supplies no information.

For any independent sample of n [0,1]-valued observations with mean μ, let y be the sample mean and kl(y||μ)=y log(y/μ)+(1−y)log((1−y)/(1−μ)). The two-sided set {μ∈[0,1]: n kl(y||μ)≤t} is a confidence interval with failure probability ≤2e^{-t}. Proof: convexity of exp gives E e^{λX}≤1−μ+μe^λ for every real λ; optimizing Chernoff in each tail gives exp(−n kl(y||μ)). The kl function is monotone in y separately above and below μ; the inverted tail event has the claimed probability. This applies to continuous weights, not just Bernoulli variables. Endpoint conventions by continuity.

Compute such intervals [A_l,A_u],[B_l,B_u] from the two independent state streams using t=log(4|E|/α). By union bound, conditionally on the pilot, all directed means lie in intervals except probability ≤α. For edge (i,j) set lower l_ij=a_j−a_i+log B_l−log A_u if the two arguments are positive, else −∞; upper u_ij=a_j−a_i+log B_u−log A_l if positive, else +∞. In exact arithmetic at zero overlap both intervals include zero, yielding [−∞,+∞]; a missing edge cannot masquerade as evidence. Positive shared overlap implies the identity and monotone bounds. On the joint event, every true edge difference is in its interval.

Represent each upper constraint f_j−f_i≤u_ij as directed edge i→j of length u_ij, and each lower constraint as j→i of length −l_ij. For finite paths, summing inequalities gives the corresponding endpoint bound. All-pairs shortest-path closure D_ij gives [−D_ji,D_ij] for every pair. Infinite distances yield unbounded endpoints; negative cycles imply inconsistency, and the implementation abstains. On the good event the true f is feasible, so no negative cycle. This proves simultaneous confidence intervals with failure ≤α, including disconnected support and abstention. It is legitimate to compare ANY full-data fit with these intervals after validation, because the probability statement is about f* itself and all pairwise intervals, not about a fit chosen independently.

For small positive overlap probabilities μ, KL-Chernoff intervals have relative error scale roughly √(t/(n μ)), an advantage over plain absolute Hoeffding widths. This does not imply a universal near-optimal graph-resistance width: shortest paths may accumulate overly conservative uncertainties, and redundant cycles may be better utilized by other methods. Improving this is a priority.

### C3. Anytime-valid extension (proof; implementation optional)

Fix the pilot and edge set, and assume infinite independent equilibrium streams per state. At every prefix n≥1 of each directed edge's stream use t_n=log(4|E| n(n+1)/α). Sum over all prefixes using ∑_{n≥1}1/[n(n+1)]=1; sum over directed edges and tails as in C2. With probability ≥1−α the intervals hold simultaneously at every prefix combination and at every (possibly adaptive) inspection or stopping time, even if which state to sample next is adaptively selected. This relies on independent fixed-law streams and the fixed pilot/edge functions; changing the pilot requires new independent validation samples and a new preallocated α budget. No assertion for autocorrelated trajectories. A simple improvement over a fixed-N interval repeatedly monitored without correction.

## D. General-graph minimax lower bound in a low-overlap class

### D1. Construction and rate (density evaluation oracle)

Let G=(V,E) be any finite connected undirected graph; fix s_k=n_k/N>0 and positive edge-region masses w_e with W_k=∑_{e∋k}w_e≤1/8. Create disjoint measurable regions A_k (private to state k) and B_e (shared only by the two endpoints). Baseline q_k is the indicator of A_k∪∪_{e∋k}B_e, with region volumes μ(B_e)=w_e, μ(A_k)=1−W_k; thus Z_k=1. The overlap Laplacian L0 has edge conductances

ℓ_e=w_e s_i s_j/(s_i+s_j), e={i,j}.

For any endpoints a≠b, let c=e_b−e_a, R_c=cᵀL0^+c>0. Define d0=min(1/2, (1/8)√(R_c/N)), θ=d0 L0^+c/R_c. On a connected resistor network, the discrete maximum principle gives max θ=θ_b and min θ=θ_a: at any other vertex a harmonic value is a positive weighted average of neighbors; a maximum propagates until a source/sink; the negative-source endpoint cannot be a maximum because (Lθ)_a<0, and similarly b cannot be a minimum. Thus osc(θ)=cᵀθ=d0 and θᵀL0θ=d0²/R_c.

Alternative: q'_k remain indicators with the identical private/shared membership pattern, but choose region volumes

μ'(B_e)=w_e exp(a_e), a_e=(s_i θ_i+s_j θ_j)/(s_i+s_j),
μ'(A_k)=exp(θ_k)−∑_{e∋k} w_e exp(a_e).

These are positive, because ∑ w_e exp(a_e−θ_k)≤e^{1/2}/8<1/4. Now Z'_k=exp θ_k, so the target contrast changes by exactly d0 in magnitude. Under either instance, a sample from state k reveals exactly its private category or one of its incident edge categories via the vector of density evaluations. The baseline categorical probabilities are w_e for shared category e and 1−W_k for private; alternative probabilities w_e exp(a_e−θ_k) and the residual private probability.

Let Δ_e,k=w_e(exp(a_e−θ_k)−1). The χ² divergence of the alternative categorical law from the baseline equals ∑ Δ²/w_e+(∑Δ)²/(1−W_k)≤[1/(1−W_k)]∑Δ²/w_e by weighted Cauchy–Schwarz. Since |a_e−θ_k|≤1/2, |exp z−1|≤e^{1/2}|z|, giving χ²≤(8e/7)∑w_e(a_e−θ_k)²<4∑w_e(a_e−θ_k)². KL≤χ². Product KL of the complete density-evaluation observation (fixed state labels, independent draws) is therefore bounded by

4N∑_e w_e[s_i(a_e−θ_i)²+s_j(a_e−θ_j)²]
=4N∑_e ℓ_e(θ_i−θ_j)²=4N d0²/R_c≤1/16.

The equality is the weighted least-squares identity for a_e. By Pinsker, TV≤√(1/32). Any estimator induces a binary test by choosing the closer of the two target values. If the test is wrong, its estimation error is at least d0/2 (ties immaterial). The sum of test errors is ≥1−TV. Hence for every estimator, at least one of the two instances has

P(|estimate−truth|≥d0/2) ≥ (1−1/√32)/2 > 0.41.

This is a finite-sample two-point minimax lower bound on the class containing these instances, for an arbitrary connected graph and arbitrary fixed sample proportions, not just equal-allocation ladders. In the nonsaturation regime it gives error radius (1/16)√(R_c/N). It does not claim a lower bound at every individual distribution or with unrestricted analytic density access.

The alternative population edge conductance is ℓ'_e=s_i s_j w_e exp(a_e)/(s_i exp θ_j+s_j exp θ_i). Since all exponents lie in a range of length d0, e^{-d0}ℓ_e≤ℓ'_e≤e^{d0}ℓ_e. Thus both Laplacians are comparable and both effective resistances comparable by e^{d0}. In the baseline, degree_i≤s_i W_i≤s_i/8. Effective resistance between i,j is at least 1/degree_i and at least 1/degree_j (unit-current flow or the Rayleigh quotient of singleton indicator). Hence 1/s_i+1/s_j≤R_ij/4, and corrected variance V_c≥3R_c/4. Alternative incident probabilities ≤1/4, hence similarly V'_c≥R'_c/2. This avoids the identical-distributions counterexample. The lower bound is on an explicitly defined hard class, with overlap comparability, not universal pointwise minimax optimality. Upper B4 matches the leading rate for fixed low-overlap instances as N grows, but uniform high-dimensional matching requires additional analysis.

### D2. Extension to sampled coordinates on randomized finite supports

Here is a rigorous way to repair the coordinate-observation loophole. Fix G, s, w and N as in D1. For each large integer M, approximate every baseline and alternative region volume by a positive integer cardinality divided by M (e.g. nearest integer, with at least one cell). Use a common finite universe of T_M cells with T_M≥both total cardinalities, and fill remaining cells with an unused category. Equip it with measure 1/M per cell. For each instance separately assign its category multiset to the T_M coordinates via a uniform random permutation. The unknown deterministic parameter is the resulting assignment; the two priors are uniform over those assignments. The estimator observes both sampled coordinate labels and all q_j at those sampled labels, and knows M,T_M, the graph and even the two priors, but not the realized assignment and has no extra density queries.

For a fixed assignment, independent samples from state k have categorical probabilities equal to rounded region cardinalities divided by state support cardinality, independent of the assignment. Conditional on the complete category sequence, the mixture law of distinct coordinate labels (conditional on there being no collisions) is uniform over all injective ordered sequences of length N, by permutation invariance. Couple this mixture to an ideal experiment: retain the actual category sequence, retain coordinate labels when distinct, and on a collision resample an injective uniform sequence independently. Conditional on each category sequence, the new coordinate sequence is uniform injective, so the ideal experiment is exactly categorical data plus an independent ancillary coordinate sequence. The TV distance is at most collision probability. For any pair of draws, conditional on assignment, their collision probability is at most 1/min_k |support_k|=O(1/M), including cross-state draws; union bound gives O(N²/M). With fixed N this tends to zero. The categorical laws and target contrasts converge to D1 as M→∞. Their finite-dimensional KL converges since all incident and private category probabilities are positive; TV is bounded by Pinsker and the triangle inequality. Thus for all sufficiently large M, mixture TV<0.3 and target separation>2d0/3. Le Cam testing implies worst-case risk over the union of the two support families at error radius d0/3 exceeds 0.35. A prior-average risk is bounded by the worst-case deterministic parameter risk, so this is a genuine minimax lower bound, not a Bayesian-only statement. The rounded resistances converge to the originals and remain comparable. No full-density or unrestricted query claim: additional oracle queries can reveal support sizes, and exact analytic integration may trivialize the problem. M depends on fixed N and chosen graph; this is a family lower bound, not one fixed finite universe for all sample sizes.

## E. Additional closure and composition

### E1. Exact data-measurable criterion for unique finite optimizer

For a finite dataset, form directed support graph with edge i→j whenever a draw from state i has q_j(x)>0. Assume own-state density positive. A unique finite gauge-fixed minimizer exists iff this graph is strongly connected.

Proof. For direction h, recession function of ℓ is average over rows of [max_{j:q_j(x)>0} h_j−h_label]. Each term nonnegative. If graph strongly connected, zero recession implies h_i≥h_j for every directed edge, hence all equal. On the gauge unit sphere the continuous recession function has positive minimum. Each row's log-sum-exp is bounded below by max active f_j plus the minimum of its finitely many finite log coefficients; thus ℓ grows at least linearly as ||f||→∞ on gauge. The undirected support cooccurrence graph is connected, so Hessian positive definite there. Existence and uniqueness follow. Conversely if not strongly connected, pick nonconstant h constant on strongly connected components and weakly decreasing along all edges (topological ordering of the condensation DAG), centered on gauge. If any edge strictly decreases then derivative along h is strictly negative at every finite f, because each row's softmax puts positive mass on active indices and its sampled state has maximal h. No finite stationary point. If no strict edge (components are isolated in the relevant ordering), derivative vanishes identically and the objective is constant along nonconstant h, hence no unique solution. One can choose strict decrease along all intercomponent edges. The graph test depends only on observed supports and labels. On its strongly connected event the minimizer is measurable, e.g. unique optimizer of a jointly measurable continuous coercive objective, or a limit of rational-grid approximate minimizers selected deterministically on expanding compact balls. Define estimator zero on the complement for B5. Numeric underflow can obscure supports; use finite log energies rather than thresholding softmax probabilities.

### E2. Exact variance optimization as a group-norm program

From A1, minimizing V over positive real sample amounts under ∑a_k s_k=B, a_k>0, is equivalent at the infimum to minimizing (∑√a_k ||r_k||_{L²(p_k)})²/B over r∈F_c. For fixed r, Cauchy–Schwarz gives the lower bound, attained for s_k proportional to ||r_k||/√a_k when all norms positive; zero-norm cases permit a limiting boundary allocation. Interchange the two infima, which requires no minimax theorem. In finite discrete support this is a convex second-order cone program (introduce upper bounds for each weighted Euclidean norm). Restricted positive minima can instead be solved by A1 directly. This is an additional algorithmic formulation; not yet implemented as an SOCP.

### E3. Simple rigorous composition with deterministic energy approximations

Suppose approximate reduced energies satisfy |ũ_k(x)−u_k(x)|≤ε_k uniformly on the integration support (or a proved pair of multiplicative partition function bounds). Then e^{-ε_k}Z_k≤Z̃_k≤e^{ε_k}Z_k, so |f̃*_k−f*_k|≤ε_k. If samples truly come independently from approximate equilibrium densities and C1/C2 supplies pairwise statistical error bounds for their free energies, a contrast certificate for the original system follows by triangle inequality: statistical radius plus ∑|c_k| ε_k (for C2 combine edge intervals or linear-program contrast bounds). For pair i,j, add ε_i+ε_j. This explicitly separates sampling and model approximation error. No assumption that MetricChain already supplies uniform energy bounds; a pointwise bound on selected conformations alone is insufficient. This composition is elementary, useful interface, not claimed novel.

## F. Remaining work and limitations

- Prior-art scan confirmed Shirts & Chodera 2008 (arXiv:0801.1426), Micaletto 2026 (arXiv:2610.17403, title *Overlap, Not Moments: Finite-Sample Theory for Bridge Sampling*), Li et al. 2023 (PMC10845960, asymptotic correlated variance decomposition), Bach 2010, and relevant bridge-sampling efficiency literature. No exhaustive novelty clearance; A1 may have precedents in optimal design or semiparametric efficiency. Treat theorems as independently derived, not priority-verified.
- B3/B4/B5 use external standard matrix concentration / Berry–Esseen inequalities; independent referee should check their exact statements, confidence allocations, and boundary cases. No full Lean verification. No installed Lean/Lake in current environment and original Lean file is uncompiled. Fable should formalize A1/A2 in finite support first, D1 weighted divergence and C1 deterministic core next, then extend. Preserve conditional vs unconditional theorem statements.
- C1/C2 do not certify ergodicity, mixing, or model fidelity. A hidden metastable region absent from all samples can defeat equilibrium assumptions. Correlated-chain finite-sample theorem remains unresolved. C2 can be conservative on long chains. B bounds rely on population parameters; use C1/C2 for observable statements.
- No real molecular benchmarks yet. Code is reference float64, not mathematically certified interval arithmetic. Sample sizes and data streams must be appropriate; existing original benchmark should not be interpreted as proof. The allocation benchmark uses known discrete population distributions, not learned pilot estimates, and establishes no measured GPU savings.
- The original manuscript contains overstated abstract and unresolved claims; do not submit it. B3/B4, B5, D1/D2 and A1/A2 are proposed replacements, not automatic validation of all old statements. Theorem 7 full PMF errors, original Theorem 5, full optimal sequential allocation and novelty remain open tasks.

## G. Further extensions derived during handoff

### G1. Explicit correlated-sampling theorem under certified spectral contractions

Let each state provide an independent stationary Markov chain of length n_k with invariant p_k and known bound ||P_k||_{L²_0(p_k)}≤ρ_k<1 (absolute L² contraction, not an estimated integrated autocorrelation time). Put C_k=(1+ρ_k)/(1−ρ_k), C=max C_k. Reversibility is not necessary for this operator-norm assumption.

For any centered finite-dimensional vector-valued observable Y in a real Hilbert space, |E⟨Y(X_0),Y(X_t)⟩|≤ρ_k^t E||Y||² by applying operator norm to each scalar coordinate and summing. Expanding the squared sum and summing a geometric series gives E||∑_{r=1}^{n_k}Y(X_r)||²≤n_k C_k E||Y||². Independence across states permits addition of the variances.

Apply this first to whitened score vectors and then to centered whitened Hessian matrices with the Frobenius norm. By B2 and B4,

E||g*||²_{L+}≤C d/N,
E||L^{−1/2}(H_N(f*)−L)L^{−1/2}||_F²≤ C R(K−1)/(4N).

The latter uses ∑E tr[(B_n−EB_n)²]≤qN(K−1), q=R/4. For a fixed contrast, E[(cᵀL^+g*)²]≤C V_c/N. Choose α∈(0,1) and let B=√(3C d/(Nα)), η=√(3C R(K−1)/(4Nα)), δ0=√R B/(1−η), κ=1/[(1−η)(1−δ0)]−1. When η<1 and δ0<1, Markov/Chebyshev and the deterministic B4 argument give with probability ≥1−α a finite unique optimizer and

|cᵀ(fhat−f*)| ≤ √(3C V_c/(Nα)) + √R_c κ B.

If d=0 or V_c=0, the corresponding centered score is zero a.s.; handle its event without dividing by zero. This is a complete explicit but conservative second-moment bound (polynomial confidence cost and dimension penalty). It does not require an unproved Markov matrix concentration replacement. A sharper exponential/variance-sensitive matrix theorem remains a target. In particular the original Theorem 5 was not justified by simply replacing N by N_eff.

For the operational C1 certificate, a sharper exponential score event follows directly from Fan, Jiang & Sun, *Hoeffding's Inequality for General Markov Chains and Its Applications to Statistical Learning*, JMLR 22(139), 2021 (https://www.jmlr.org/papers/v22/19-479.html), using their stationary absolute-gap Hoeffding lemma for bounded observables. The per-state centered sum has mgf ≤exp(t² n_k C_k/8) for [0,1] range; independent state streams multiply mgfs. Thus C1 remains valid with ε0=√[(∑ n_k C_k)(K log 2+log(1/α))/(2N²)]. The same lemma supplies ordinary bounded-mean holdout intervals in C2, y±√[C_k log(4|E|/α)/(2n_k)] clipped to [0,1], not the independent KL inversion. Pilot must be independent of the stationary validation chains. None of these bounds certify the spectral contractions themselves. They also do not apply to arbitrary nonstationary, replica-exchange, or MD trajectories without verifying assumptions.

### G2. Full bounded observable / PMF error from an observable free-energy certificate

For A(x)∈[0,1] and target state k, let μ_k=E_k A. At truth y*=N^{-1}∑ π*_k(x_n)A(x_n) has expectation s_k μ_k. The summands are independent in [0,1], not necessarily identically distributed. The product mgf bound for each summand and arithmetic-geometric mean inequality gives the same Bernoulli KL-Chernoff bound as C2 for their average expectation. Specifically ∏[1+μ_n(e^t−1)]≤[1+(mean μ_n)(e^t−1)]^N for any real t. Hence with probability ≥1−α_o the unknown s_k μ_k lies in the KL interval I(y*,N,log(2/α_o)).

Suppose C1 (or another valid simultaneous certificate) supplies observable osc(f0−f*)≤r at error probability α_f. Compute y0=N^{-1}∑ π_k(f0,x_n) A(x_n). Softmax ratios at positive components lie in [e^{-r},e^r], zero components stay zero, so y*∈[e^{-r} y0,min(1,e^r y0)]. Compute the union of KL confidence sets I(y,N,log(2/α_o)) over y in this interval. Equivalently use the smallest lower endpoint and largest upper endpoint (these endpoints are nondecreasing in y by monotonicity of Bernoulli KL in y on either side of μ). Divide by s_k and intersect with [0,1]. This is an observable confidence interval for μ_k with error probability ≤α_f+α_o; no sample splitting is required. It includes ordinary Monte Carlo error, unlike original Theorem 7. Multiple states/observables/bins can share α_f and split α_o by union bound. Bounded signed A is reduced to [0,1] by affine rescaling.

For a PMF difference between two bins A,B, if their population probabilities have simultaneous intervals [l_A,u_A],[l_B,u_B] with strictly positive lower endpoints, then the reduced free-energy difference −log(μ_A/μ_B) is in [log l_B−log u_A, log u_B−log l_A]. With a zero lower endpoint, output an unbounded endpoint rather than a spurious finite value. Full unbounded observables and missing equilibrium mass remain unaddressed. This result is a mathematical extension, not yet benchmarked.

## Prior-art update (important)

A targeted search found that convexity of the **two-state** Bennett acceptance ratio asymptotic MSE is explicitly known: A. M. Hahn and H. Then, *A characteristic of Bennett's acceptance ratio method*, Phys. Rev. E 80 (2009), arXiv:0904.0625, https://arxiv.org/abs/0904.0625. A1 is therefore a candidate multistate generalization, not the first convex allocation theorem for BAR. Investigate this paper and all forward citations in detail. The biased-sampling literature of Vardi (1985) and Gill, Vardi & Wellner (1988) includes graph-based existence/uniqueness and efficiency theory (https://stat.uw.edu/research/tech-reports/large-sample-theory-empirical-distributions-biased-sampling-models), so E1 is not claimed novel. Search for exact prior multistate perspective/optimal-design formulations, particularly Zhiqiang Tan's likelihood approach for Monte Carlo integration, before priority assertions. No exhaustive search completed.

Bibliography precision: the pinned v1 HTML at https://arxiv.org/html/2610.17403v1 displays the title *Overlap, Not Moments: Sample Size and Standard Errors in Bridge Sampling*; the abstract landing page returned *Overlap, Not Moments: Finite-Sample Theory for Bridge Sampling*. Cite a specific version with its corresponding title rather than treating this discrepancy as an error without checking version history. In v1, Theorem 13's discussion states the all-two-sample-estimator minimax question, and Section 8 names multiple bridge sampling / MBAR and multiparameter NCE as extensions. D1/D2 address the sampled-density/coordinate oracle model only; check the precise intended oracle in the paper and related Block & Shetty (arXiv:2602.23535) before claiming closure of the open problem.
