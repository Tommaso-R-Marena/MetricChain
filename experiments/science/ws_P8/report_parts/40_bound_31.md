
---

## 3. P3's cross bound for far pairs: what it is, where its slack really is, the sharper form with proof and validation

### 3.1 What P3's bound is, and that it does carry the factor `e^{−r²/4B_aB_b}` [K: P3's code and report, read in full; M]

**The statement relied on (P3_REPORT §2.3, Theorem 3, quoted).**  "*For every `T` with `|T| = m ≥ 3`,
every base point and every `y_T`,*
`|Δ_T g(z; y_T)| ≤ Σ_p Σ_{states of l(p) met} σ_p(T∖{l(p)}) + Σ_{p<q} Σ_{states of l(p), l(q) met} θ_pq(T∖{l(p), l(q)})`,
*where 'states met' means: the single state `z_l` if the host `l ∉ T`, and the two states `z_l, y_l`
if `l ∈ T`*", with
`σ_p(B) = (κ/2) q_p² Bd_{|B|} ∏_{i∈B} δ^p_i` and
`θ_pq(B) = κ|q_p q_q| Σ_{π∈Part(B)} H_{|π|} ∏_{β∈π} (L^p_{|β|} ∏_{i∈β} δ^p_i + L^q_{|β|} ∏_{i∈β} δ^q_i)`,
"*for two atoms in host states `(b, b′)`*, `H_k := sup{|∂_w^k h(w; r_pq)| : w ∈ [ℓ_p⁻ + ℓ_q⁻, ℓ_p⁺ + ℓ_q⁺]}`".
*Whether I checked its proof:* yes — I re-derived Lemma 2 (the integral representation of a mixed
difference of a composite and the bound of each block derivative by its vertex values), its
corollaries L1 and L2 and the host step L3, and found them correct as written; the per-term form
I use is restated as Lemma T in §3.3 with its proof.

**The kernel constant, in code and in formula.**  `ws_P3/encl.py`, `EnvelopeSup.sup_h`, lines 296–305:

```
Dlo = r * r * np.exp(-whi) / 4.0 * (1.0 - 1e-9);   Dhi = r * r * np.exp(-wlo) / 4.0 * (1.0 + 1e-9)
...  z = self.rmZ[k].query(a.ravel(), b.ravel())  ...  return 2.0 / r * z * (1.0 + 1e-12)
```

called by `ws_P3/gfbound.py`, `GFBound._supH_states`, lines 156–172, with the pair's own distance
`r` in the two host states and the hull `[wlo, whi]` of `ℓ_p + ℓ_q`.  It returns a rigorous
enclosure of

```
H_k = (2/r) · sup { |ζ_k(D)| : D ∈ [D_lo, D_hi] },     D = r² e^{−w}/4 = r²/(4 B_p B_q),     ∂_w^k h(w; r) = (2/r) ζ_k(D),
ζ_0(D) = √D (4D + e^{−D})^{−1/2},     ζ_1(D) = −½ (1 + D) e^{−D} √D (4D + e^{−D})^{−3/2}   ( ≈ −(1 + D) e^{−D}/(16 D) for large D ),
```

and every `ζ_k`, `k ≥ 1`, is a finite sum of monomials `c · D^{a+1/2} e^{−bD} (4D + e^{−D})^{−c′/2}` with `b ≥ 1`
(`ws_P3/dfun.py`, line 94: asserted for `k ≤ 5`; `encl.zeta_tail` asserts it again for the tail cell
`[80, ∞)`).  For a far pair this is `|∂_w h| ≈ B_pB_q (1 + D) e^{−D}/(2r³)`.  **So P3's bound of the mixed
differences of `1/f` does carry the factor `e^{−r²/4B_aB_b}` — as a supremum over the hull, i.e. at
the largest product of Born radii that any context allows.**  The brief's suspicion (step 3) is
not borne out.

