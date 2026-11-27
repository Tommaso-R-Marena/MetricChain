### 3.6 What was tried and not gained [N, exploration with sampled suprema — not rigorous, not used anywhere else]

After the state-wise maximum the largest remaining ratio bound/exact is on pairs of **fixed**
atoms (3.2–9.2, growing with the order; tables T3, T4b), where there is no host and nothing to
resolve.  Two things were tried on those pairs (`x01_ff_proto.py`; Lys₄ and LKSE:5, all pairs of
fixed atoms, suprema sampled on a 9 × 9 grid of the hull rectangle; the sampled version of P3's
own formula reproduces P3's rigorous value within 4 %):

* **Dead end: expanding in the inverse Born radii instead of their logarithms.**  I expected the
  Faà di Bruno sum over `w = ln B_p + ln B_q` to lose by a "log–exp detour" and the variables
  `b_p = 1/B_p` to avoid it.  It is the other way round: the `b`-version is 1.2–3.6 times *worse*
  than P3's (orders 3–5), because `b(I)` — a `tanh` of a cubic — is strongly non-linear while
  `ln B` is not.  P3's choice of variable is the right one.
* **A ceiling.**  The best that a chain-rule bound with one supremum per split of the free sites
  between the two atoms can do — the supremum over the hull rectangle of the exact mixed partial
  `∂_{I_p}^a ∂_{I_q}^b h` — is 1.9–2.7 times the exact constants at orders 3–4 and 3.7 at order 5, where
  P3 has 3.0–5.0 and 9.1.  A two-dimensional interval enclosure per atom pair would therefore
  gain at most a factor 1.5–2.5 on these pairs (which carry 14–33 % of the new bound), at the
  price of interval arithmetic for every pair of atom instances.  Not pursued.  Replacing the
  Bell polynomials of suprema by suprema of Bell polynomials (a table per atom class) gains
  2–13 %.
