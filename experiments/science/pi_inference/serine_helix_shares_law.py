#!/usr/bin/env python3
"""Addendum A17 (15), item 34: the law  width(k-share form) ~ 2 p^k Gamma_m  -- coordinator's check.

Reads serine_helix_shares.json (exact enumeration; evaluated terms exact) and compares the bracket width of the site
(k = 1), pair (k = 2), triple (k = 3) forms and of the envelope (k = m) with  2 p^k Gamma_m,  where p is the mean
fraction of side chains off the anchor under the true ensemble and Gamma_m (in k_B T) the sum of the certified
constants of order m.

Why this should hold: the k-share penalty at a state x is  sum_T chat_T C(|T n S(x)|, k) / C(m, k)  (k = m: the
envelope).  If the sites were off the anchor independently with probability p, |T n S| would be Binomial(m, p), whose
k-th factorial moment gives  E C(|T n S|, k) = C(m, k) p^k,  so the mean penalty would be  p^k Gamma_m  EXACTLY; and
for a narrow sandwich  ln Z(m_-) - ln Z(m_+) ~ 2 E[penalty].  Nothing here is a theorem about the real ensemble (sites
are neither independent nor exchangeable, and wide brackets are not first order); the table says how well it holds.
Run:  python3 -B serine_helix_shares_law.py > serine_helix_shares_law.log
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "serine_helix_shares.json")))
print("# instance m | p = off-anchor fraction | Gamma_m (kT) | width / (2 p^k Gamma_m) for site (k=1), pair (k=2), triple (k=3), envelope (k=m) "
      "| the same for the first-order quantity  2 p^k Gamma_m  itself (nats)")
worst = 0.0; worst_narrow = 0.0
for r in rows:
    n = int(r["seq"][1:]); m = r["m"]; p = r["n_off"] / n; G = r["Gamma_kT"]
    e = r["exact_terms"]; rat = []; pred = []
    for name, k in (("site", 1), ("pair", 2), ("triple", 3), ("envelope", m)):
        pr = 2 * p ** k * G; pred.append(pr); rat.append(e[name] / pr)
    dev = max(abs(v - 1) for v in rat); worst = max(worst, dev)
    if e["site"] < 0.5: worst_narrow = max(worst_narrow, dev)
    print(f"{r['seq']}/{r['bb']} m={m} | {p:.3f} | {G:9.4g} | " + ", ".join(f"{v:.3f}" for v in rat) + " | " + ", ".join(f"{v:.4g}" for v in pred))
print(f"largest deviation of a ratio from 1: {worst:.3f} (all {len(rows)} rows, {4 * len(rows)} brackets); "
      f"among the rows whose site bracket is below 0.5 nats: {worst_narrow:.3f}")
print("ALL DONE")
