#!/usr/bin/env python3
"""Check that every Lean declaration name cited in docs/*.md and README.md exists in proofs/.

A backticked token is treated as a declaration reference if it looks like a Lean identifier with
an underscore (e.g. `robust_minimizer_iff`, `PairModel.goldstein_isLeast`) or is a qualified name
`Namespace.name` whose first component is capitalised (e.g. `RProblem.Consistent`).  Tokens listed
in IGNORE are prose/math notation.  Unqualified names without an underscore (`verify`, `tilt`)
cannot be told apart from prose and are not checked.  Exit code 1 if a cited name is missing.
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

# structure fields: `structure Name ... where` followed by indented `field : type` lines
struct_re = re.compile(r"^structure\s+([^\s:({\[]+)")
field_re = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_']*)\s*:")
for f in (root / "proofs").rglob("*.lean"):
    current = None
    for line in f.read_text().splitlines():
        m = struct_re.match(line)
        if m:
            current = m.group(1)
            continue
        if current is None:
            continue
        if line.strip() == "" or not line[0].isspace():
            current = None
            continue
        fm = field_re.match(line)
        if fm:
            declared.add(f"{current}.{fm.group(1)}")

IGNORE = {
    "lower_bound", "native_decide", "metricchain-cert", "audit_all", "falsify_conjectures",
    "separation_benchmarks", "lake_env", "check_doc_refs", "L1_pruning_certificates",
    "L2_relaxations_partition", "L3_realizability_geometry", "prior_art", "e_lo", "e_hi",
    "vol_lo", "vol_hi", "t_hol", "c_min", "c_k", "c_i", "x_i", "I_red", "E_min", "E_lo", "E_hi",
    "residual_oracle", "eps_prune", "eps_leaf", "D_site", "I_a", "I_q", "L_q", "q_j", "d_c",
    "u_i", "p_ij", "m_ij", "h_i", "J_ij", "lo_ij", "hi_ij", "W_ij", "w_i", "ρ_max",
    "D_i", "A_i", "P_ij", "Pat_ij", "base_i", "m_k", "U_ij", "x_p", "x_q", "lo_p", "hi_q", "hi_p", "lo_a", "value_a",
    "mutation_tests", "reference_checker", "audit_selftest",
    # names of JSON conformance vectors (experiments/certs/*.json)
    "residual_inconsistent_reject", "residual_lower_only", "residual_negative_c_reject",
    "partition_negative_reject", "residual_interval", "residual_interval_inconsistent_reject",
    "residual_bad_anchor_reject", "partition_bad_domain_reject", "triangle_residual",
    "triangle_min", "triangle_min_reject", "biased_dee", "triangle_partition_exact",
    "triangle_partition_coarse",
    # qualified names that are not declarations of this development
    "Classical.choice", "Quot.sound", "Lean.ofReduceBool", "Real.exp", "Finset.sup",
}
tok_re = re.compile(r"`([A-Za-z][A-Za-z0-9_.'₀-₉]*)`")
qualified_re = re.compile(r"^[A-Z][A-Za-z0-9]*\.[A-Za-z_][A-Za-z0-9_.']*$")
missing = {}
for doc in sorted((root / "docs").glob("*.md")) + [root / "README.md"]:
    for tok in tok_re.findall(doc.read_text()):
        looks_like_decl = "_" in tok or qualified_re.match(tok)
        if not looks_like_decl or tok in IGNORE or tok.endswith((".lean", ".py", ".sh", ".md", ".txt", ".json")):
            continue
        last = tok.split(".")[-1]
        if tok not in declared and last not in declared:
            missing.setdefault(doc.name, set()).add(tok)
if missing:
    for doc, toks in missing.items():
        print(f"{doc}: cited but not declared in proofs/: {sorted(toks)}")
    sys.exit(1)
print(f"doc references OK ({len(declared)} declarations indexed)")
