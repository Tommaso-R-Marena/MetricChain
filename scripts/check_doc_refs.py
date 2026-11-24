#!/usr/bin/env python3
"""Check that every Lean declaration name cited in docs/*.md exists in proofs/.

A backticked token is treated as a declaration reference if it looks like a Lean identifier with
an underscore (e.g. `robust_minimizer_iff`, `PairModel.goldstein_isLeast`).  Tokens listed in
IGNORE are prose/math notation.  Exit code 1 if a cited name is missing.
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
decl_re = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([^\s:({\[]+)", re.M)
declared = set()
for f in (root / "proofs").rglob("*.lean"):
    for m in decl_re.finditer(f.read_text()):
        name = m.group(1)
        declared.add(name)
        declared.add(name.split(".")[-1])

IGNORE = {
    "lower_bound", "native_decide", "metricchain-cert", "audit_all", "falsify_conjectures",
    "separation_benchmarks", "lake_env", "check_doc_refs", "L1_pruning_certificates",
    "L2_relaxations_partition", "L3_realizability_geometry", "prior_art", "e_lo", "e_hi",
    "vol_lo", "vol_hi", "t_hol", "c_min", "c_k", "c_i", "x_i", "I_red", "E_min", "E_lo", "E_hi",
    "residual_oracle", "eps_prune", "eps_leaf", "D_site", "I_a", "I_q", "L_q", "q_j", "d_c",
    "u_i", "p_ij", "m_ij", "h_i", "J_ij", "lo_ij", "hi_ij", "W_ij", "w_i", "ρ_max",
    "D_i", "A_i", "P_ij", "Pat_ij", "base_i", "m_k", "U_ij", "anchor_semantics",
    # names of JSON conformance vectors (experiments/certs/*.json)
    "residual_inconsistent_reject", "residual_lower_semantics", "residual_negative_c_reject",
    "partition_negative_reject",
}
tok_re = re.compile(r"`([A-Za-z][A-Za-z0-9_.'₀-₉]*)`")
missing = {}
for doc in sorted((root / "docs").glob("*.md")):
    for tok in tok_re.findall(doc.read_text()):
        if "_" not in tok or tok in IGNORE or tok.endswith((".lean", ".py", ".sh", ".md", ".txt", ".json")):
            continue
        last = tok.split(".")[-1]
        if tok not in declared and last not in declared:
            missing.setdefault(doc.name, set()).add(tok)
if missing:
    for doc, toks in missing.items():
        print(f"{doc}: cited but not declared in proofs/: {sorted(toks)}")
    sys.exit(1)
print(f"doc references OK ({len(declared)} declarations indexed)")
