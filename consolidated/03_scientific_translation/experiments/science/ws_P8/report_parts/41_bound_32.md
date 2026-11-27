### 3.2 Is it loose for far pairs?  No — the slack is in the host step [M]

**Far pairs.**  For every atom pair and every subset `T` of every enumerated instance I computed
the exact anchored constant of the single pair term, `c_T(t_pq)` (`p8_01_measure.py`), and P3's
summand for the same pair (`p8lib.GFDecomp`: P3's `theta` / `self_sum` with the summands exposed;
its totals equal P3's to the last bit, asserted).  Pairs are classed by `Dmin`, the smallest value
of `D = r²/(4B_pB_q)` over **all** states (a pair of moving atoms that is far in the anchor state
can be close in another rotamer; my first table, by `D` at the anchor, was misleading — §7).

<!--T:T4-->

Pairs that are far in every state (`Dmin ≥ 4`) carry 0.04–4 % of P3's cross bound and 0.05–2.5 %
of the best pair-by-pair bound, on all instances of the table; with `Dmin ≥ 8` less than 0.01 %.
After the state-wise maximum of §3.3 the ratio bound/exact does not grow with the distance: on
the charged helix instances (Lys₃–Lys₅, LKSE:4–LKSE:6) it is 2.0–9.6 for `Dmin < 1`, 2.1–8.0 for
`1 ≤ Dmin < 4`, 2.1–5.6 for `Dmin ≥ 4` (growing with the order in all three classes); for pairs
of fixed atoms alone 3.0–12, 2.4–8.7, 2.9–10 — so the hull of the Born radii does not open a
gap for far pairs either.  (On the three strand instances the far class has the largest ratio,
2.8–7.9, on 0.4–3.6 % of the bound.)

<!--T:T4b-->

**Where the slack is.**  P3's Theorem 3 is a statement per host state; its *computable closed
form* (`gfbound.GFBound`, "types") replaces, for a host outside `T`, every ingredient — the
deviations `δ_i` of each free site, `sup|ℓ^{(k)}|`, `sup|∂_w^k h|` — by its maximum over all rotamers of
the host (type X), and for a host in `T` by the anchor's value plus the maximum over the non-anchor
rotamers (types A + N), *each ingredient separately*.  For a lysine side chain (6–13 non-anchor
rotamers per site in P2's domain, 15 moving atoms, the ammonium group at the end of a chain of
four rotatable bonds) the maxima are attained at different rotamers: the rotamer in which the ammonium
group is closest to site `i` is not the one in which it is closest to site `j`, nor the one in
which two head groups approach each other.  The product of the maxima is then far above the
maximum of the products:

<!--T:T3|Lys₅,LKSE:5,LKSE:6,Ser₆-->

(Rows of Lys₅, LKSE:5, LKSE:6 and Ser₆; all instances: `out/tables.md`, table T3.)

On Lys₅ at orders 3, 4, 5 P3's bound is 3.4, 4.0, 7.7 times the best pair-by-pair bound for pairs
of fixed atoms, **6.1, 23, 56** times for a fixed and a moving atom whose site is in `T`, and
**8.9, 68, 191** times for two moving atoms whose sites are both in `T`; for hosts outside `T` the
ratios reach 303 and 493 (on small totals).  By atom class (table T2 in §1) the head–head pairs
alone are 40–45 % of P3's bound for Lys₅ and exceed their own best pair-by-pair bound by factors
12, 98, 313.  P3's single-term sharpness test (its §3.2: "median factor 4.2–5.5 for atoms of two
side chains") was run on valine and serine, where a side chain has at most nine states and four
moving atoms; it could not see this.
