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
    r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([^\s:({\[]+)")
ns_re = re.compile(r"^namespace\s+(\S+)")
sec_re = re.compile(r"^section(?:\s+(\S+))?")
end_re = re.compile(r"^end(?:\s+(\S+))?")
ROOT_NS = "MetricChain."

# `full` holds fully qualified names (namespaces tracked, the root namespace stripped);
# `last` holds last components, for unqualified citations.
full, last = set(), set()
for f in (root / "proofs").rglob("*.lean"):
    stack = []          # entries: ("ns", name) or ("sec", name-or-None)
    for line in f.read_text().splitlines():
        m = ns_re.match(line)
        if m:
            stack.append(("ns", m.group(1)))
            continue
        m = sec_re.match(line)
        if m:
            stack.append(("sec", m.group(1)))
            continue
        m = end_re.match(line)
        if m and stack:
            stack.pop()
            continue
        m = decl_re.match(line)
        if m:
            name = m.group(1)
            qual = ".".join([n for kind, n in stack if kind == "ns"] + [name])
            if qual.startswith(ROOT_NS):
                qual = qual[len(ROOT_NS):]
            full.add(qual)
            last.add(name.split(".")[-1])
declared = full | last

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
            full.add(f"{current}.{fm.group(1)}")

IGNORE = {
    "lower_bound", "native_decide", "metricchain-cert", "audit_all", "falsify_conjectures",
    "separation_benchmarks", "lake_env", "check_doc_refs", "L1_pruning_certificates",
    "L2_relaxations_partition", "L3_realizability_geometry", "prior_art", "e_lo", "e_hi",
    "vol_lo", "vol_hi", "t_hol", "c_min", "c_k", "c_i", "x_i", "I_red", "E_min", "E_lo", "E_hi",
    "residual_oracle", "eps_prune", "eps_leaf", "D_site", "I_a", "I_q", "L_q", "q_j", "d_c",
    "u_i", "p_ij", "m_ij", "h_i", "J_ij", "lo_ij", "hi_ij", "W_ij", "w_i", "ρ_max",
    "D_i", "A_i", "P_ij", "Pat_ij", "base_i", "m_k", "U_ij", "x_p", "x_q", "lo_p", "hi_q", "hi_p", "lo_a", "value_a",
    "mutation_tests", "reference_checker", "audit_selftest",
    # mathematical notation of the certification-geometry sections (theory report §§10-12)
    "D_A", "N_cov", "N_frac", "N_point", "N_value", "N_config", "N_Z", "T_P", "T_Q", "W_d", "c_T", "c_ij",
    "n_B", "n_P", "L_A", "U_A", "g_star", "L_μ", "R_β", "S_C", "L4_certified_optimisation_and_recovery",
    "L5_polytropes_interval_uncertainty", "L6_transport_entropy_and_information_limits", "R1_referee_report",
    "e_ν", "p_E", "δ_ν", "p_gap", "p_slack", "D_Q", "R2_referee_report",
    "ε_n", "a_n", "s_min", "T_Q", "T_P", "N_Z", "R_β", "c_y", "r_y", "λ_β", "Λ_β", "N_frac", "U_y", "q_a",
    "D_j", "F_j", "W_ji", "W_ij", "g_j", "λ_j", "P_j", "w_j", "R_j", "gap_j", "x_i", "A_j",
    # names of JSON conformance vectors (experiments/certs/*.json)
    "residual_inconsistent_reject", "residual_lower_only", "residual_negative_c_reject",
    "partition_negative_reject", "residual_interval", "residual_interval_inconsistent_reject",
    "residual_bad_anchor_reject", "partition_bad_domain_reject", "triangle_residual",
    "triangle_min", "triangle_min_reject", "biased_dee", "triangle_partition_exact",
    "triangle_partition_coarse", "residual_unknown_field_reject", "min_noncanonical_rational_reject",
    # a field of an earlier schema draft and a deliberately bogus example name, quoted in DEAD_ENDS
    "anchor_semantics", "Anything.existing_name",
    # qualified names that are not declarations of this development
    "Classical.choice", "Quot.sound", "Lean.ofReduceBool", "Real.exp", "Finset.sup", "Rat.add",
    # Greek-letter mathematical notation
    "Δ_θ", "Δ_res", "ε_k", "ρ_l", "ρ_k", "ψ_i", "δ_i", "δ_k", "Λ_i", "γ_k", "λ_k",
}
tok_re = re.compile(r"`([A-Za-zΑ-Ωα-ω][A-Za-zΑ-Ωα-ω0-9_.'₀-₉]*)`")
qualified_re = re.compile(r"^[A-Z][A-Za-z0-9]*\.[A-Za-zΑ-Ωα-ω_][A-Za-zΑ-Ωα-ω0-9_.']*$")
camel_re = re.compile(r"^[a-z]+[A-Z][A-Za-z0-9]*$")       # lowerCamelCase: `verifyITop`, `boxFinset`


def is_declared(tok):
    if "." in tok:
        # a qualified citation must match a fully qualified declaration (or a suffix of one at a
        # component boundary); matching only the last component is not enough
        return tok in full or any(d.endswith("." + tok) for d in full)
    return tok in last or tok in full


missing = {}
for doc in sorted((root / "docs").glob("*.md")) + [root / "README.md"]:
    for tok in tok_re.findall(doc.read_text()):
        looks_like_decl = "_" in tok or qualified_re.match(tok) or camel_re.match(tok)
        if not looks_like_decl or tok in IGNORE or tok.endswith((".lean", ".py", ".sh", ".md", ".txt", ".json")):
            continue
        if not is_declared(tok):
            missing.setdefault(doc.name, set()).add(tok)
if missing:
    for doc, toks in missing.items():
        print(f"{doc}: cited but not declared in proofs/: {sorted(toks)}")
    sys.exit(1)
print(f"doc references OK ({len(full)} declarations indexed)")
