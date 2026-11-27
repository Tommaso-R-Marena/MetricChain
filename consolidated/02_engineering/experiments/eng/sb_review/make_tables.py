"""Tables of ENG-RES-0018 (the first independent review of ``src/metricchain_sb`` at the structural-biology division's
commit 720e0ec), generated from ``results/mincert_part_*.json`` so that no number of the message is typed by hand.

    python experiments/eng/sb_review/make_tables.py                 # print every block
    python experiments/eng/sb_review/make_tables.py --write FILE    # fill the <!-- TABLE:name --> blocks of FILE
    python experiments/eng/sb_review/make_tables.py --verify FILE
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"


def part(p: str):
    f = RES / f"mincert_part_{p}.json"
    return json.loads(f.read_text())["result"] if f.exists() else None


def build() -> dict[str, str]:
    blocks: dict[str, str] = {}
    a = part("a")
    if a:
        blocks["sb_a"] = (
            f"{a['cases']:,} claims on random certificate trees (models of 1 to 5 sites with 1 to 4 states; root boxes that are sometimes proper sub-boxes; trees with valid "
            f"and invalid eliminations, missing and surplus children, arbitrary messages; {a['structure_valid']:,} trees structurally valid).  For every structurally valid tree "
            f"the claim was set to what the tree proves, and to 1 and 3 units below and 1 and 2 units above it.  Their checker accepted {a['sb_accept']:,} claims and rejected "
            f"{a['sb_reject']:,}.  **Disagreements with our independent checker: {a['disagree_ours']}.  Disagreements with the theory division's reference checker after their own "
            f"conversion: {a['disagree_reference']} of {a['reference_checked']:,}.  Acceptances of a claim above the true minimum of the box (enumeration): {a['unsound_sb']}.  "
            f"Trees that prove more than the true minimum: {a['unsound_format']}.**  At the exact value proved, accepted in {a['exact_at_bound']:,} of {a['structure_valid']:,}; "
            f"conversions that raised: {a['conversion_malformed']}.")
    b = part("b")
    if b:
        lines = ["| trap | claim / true minimum of the box | their checker | reference checker (after their conversion) | ours | as it should be |", "|---|---|---|---|---|---|"]
        for r in b:
            ref = r.get("reference")
            ref = "—" if ref is None else ("accepts" if ref is True else "rejects" if ref is False else "conversion refuses it")
            mine = r.get("ours")
            mine = "—" if mine is None else ("accepts" if mine else "rejects")
            cl = f"{r['claim']} / {r['true_minimum']}" if "claim" in r else "—"
            lines.append(f"| {r['name']} | {cl} | {'accepts' if r['accepted'] else 'rejects'} | {ref} | {mine} | {'yes' if r['as_expected'] and not r['unsound'] else '**NO**'} |")
        blocks["sb_b"] = "\n".join(lines)
        blocks["sb_b_summary"] = f"{len(b)} traps; {sum(1 for r in b if r['as_expected'] and not r['unsound'])} behave as they should; unsound acceptances: {sum(1 for r in b if r['unsound'])}."
    c = part("c")
    if c:
        lines = ["| case | outcome |", "|---|---|"]
        for r in c:
            if "degree" in r:
                lines.append(f"| a hub of degree {r['degree']} whose site term is a sum of {r['hub_site_sum_bits']} bits; the tree proves {r['ours_proves']} = the true minimum | "
                             f"claim {r['ours_proves']}: {'accepted' if r['claim_proves_plus_0']['accepted'] else 'rejected (' + r['claim_proves_plus_0']['reason'] + ')'}; "
                             f"claim {r['ours_proves'] + 1}: {'accepted' if r['claim_proves_plus_1']['accepted'] else 'rejected'} |")
            elif "claim_bits" in r:
                lines.append(f"| a true claim of {r['claim_bits']} bits (4097 sites with one state of energy `2⁵⁰ − 1`) | {'accepted' if r['accepted'] else 'rejected: ' + r['reason']} |")
            elif "entry_bits" in r:
                lines.append(f"| a table entry of {r['entry_bits']} bits after scaling ({'`2^' + str(r['entry_bits'] - 1) + '`' if r['entry_is_power'] else '`2^' + str(r['entry_bits']) + ' − 1`'} × `2^{r['message_bits']}`) | "
                             f"{'accepted' if r['accepted'] else 'rejected: ' + r['reason']} |")
            else:
                lines.append(f"| an all-zero model with `message_bits = {r['message_bits']}` | {'accepted' if r['accepted'] else r['reason']} ({r['seconds']} s) |")
        blocks["sb_c"] = "\n".join(lines)
    d = part("d")
    if d:
        lines = ["| document | their `loads` | their verdict, and the claim it reports | what happened silently | our strict loader |", "|---|---|---|---|---|"]
        for r in d:
            loaded = r["their_loader"] == "loaded"
            verdict = "—" if not loaded else (f"**accepted**, bound {r['checked_claim']}" if r["their_verdict"] else f"rejected (claim checked: {r['checked_lower_bound']}; unary tables checked: `{r['checked_model_unary']}`)")
            ours_ = r["ours"].split(":")[0] if r["ours"].startswith("malformed: not JSON") else r["ours"]
            lines.append(f"| {r['name']} | {r['their_loader']} | {verdict} | {r.get('silent') or '—'} | {ours_} |")
        blocks["sb_d"] = "\n".join(lines)
        alt = [r for r in d if r["name"] != "the unchanged document"]
        blocks["sb_d_summary"] = (f"{len(alt)} altered documents: their loader loads {sum(1 for r in alt if r['their_loader'] == 'loaded')} of them and their checker then accepts "
                                  f"{sum(1 for r in alt if r.get('their_verdict'))}; our strict loader refuses {sum(1 for r in alt if r['ours'].startswith('malformed'))} as malformed and "
                                  f"rejects the other {sum(1 for r in alt if r['ours'] == 'rejected')}.")
    f = part("f")
    if f and "error" not in f:
        lines = ["| chain: sites × states | eliminations (= nesting depth − 1) | checked in memory | `dumps` | `to_metricchain_cert1` |", "|---|---|---|---|---|"]
        for r in f["produced"]:
            lines.append(f"| {r['sites']} × {r['states']} | {r['prune']} | {'accepted' if r['accepted_in_memory'] else 'rejected'} | {r['dumps']} | {r['to_metricchain_cert1']} |")
        blocks["sb_f"] = "\n".join(lines)
        blocks["sb_f_loads"] = ("`loads` on a document with a chain of nested eliminations (interpreter recursion limit " + str(f["recursion_limit"]) + "): "
                                + "; ".join(f"depth {r['depth']}: {'loaded and accepted' if r['loads'] == 'ok' and r.get('accepted') else r['loads']}" for r in f["loaded"]) + ".")
    e = part("e")
    if e:
        R = e["random"]
        blocks["sb_e_random"] = (
            f"{R['instances']:,} random instances (1 to 8 sites, 1 to 4 states, densities 0 to 1, amplitudes 1 to 1000, `scale_bits` 0, 3, 8, `message_bits` 0, 4, 12) against "
            f"enumeration: certificate rejected by their checker {R['rejected']}; optimum or witness wrong {R['wrong_optimum']}; certified gap not zero {R['gap_nonzero']}; "
            f"producer raised {sum(R['raised'].values())}; rejected by our checker {R['ours_disagrees']}; rejected by the reference checker after conversion {R['reference_disagrees']}.  "
            f"With a tolerance `eps > 0`: {e['tolerance']['instances']} instances, {e['tolerance']['bad']} outside `lower bound ≤ minimum ≤ witness`, gap `≤ eps`.  "
            f"Degenerate instances ({', '.join(x['name'] for x in e['degenerate'])}): {sum(1 for x in e['degenerate'] if x['correct'])} of {len(e['degenerate'])} exact.")
        lines = ["| sites × states (random tree) | exact (against dynamic programming) | producer, seconds | branch-and-bound nodes | eliminations in the certificate | certificate, bytes | their checker, seconds | ours (pure Python integers), seconds |",
                 "|---|---|---|---|---|---|---|---|"]
        for x in e["trees"]:
            lines.append(f"| {x['sites']} × {x['states']} | {'yes' if x.get('correct') else x.get('abstained') or x.get('raised') or 'no'} | {x.get('seconds', '—')} | {x.get('nodes', '—')} | "
                         f"{(x.get('stats') or {}).get('prune', '—')} | {x.get('bytes', '—'):,} | {x.get('check_seconds', '—')} | {x.get('ours_check_seconds', '—')} |")
        blocks["sb_e_trees"] = "\n".join(lines)
        g = defaultdict(list)
        for x in e["dense"]:
            g[(x["sites"], x["states"])].append(x)
        lines = ["| sites × states (all pairs, entries in ±100) | instances | exact (against enumeration) | abstained | producer, seconds: median / largest | nodes: median / largest | largest certificate, bytes |",
                 "|---|---|---|---|---|---|---|"]
        for (n, k), xs in sorted(g.items(), key=lambda kv: kv[0][1] ** kv[0][0]):
            ok = [x for x in xs if x.get("correct")]
            lines.append(f"| {n} × {k} (`{k ** n:,}` configurations) | {len(xs)} | {len(ok)} | {sum(1 for x in xs if 'abstained' in x)} | "
                         f"{st.median([x['seconds'] for x in ok]):.1f} / {max(x['seconds'] for x in ok):.1f} | {st.median([x['nodes'] for x in ok]):.0f} / {max(x['nodes'] for x in ok)} | "
                         f"{max(x['bytes'] for x in ok):,} |")
        blocks["sb_e_dense"] = "\n".join(lines)
        lines = ["| largest table entry, bits | `message_bits` | instances | exact and accepted by their own checker | otherwise |", "|---|---|---|---|---|"]
        for x in e["magnitude"]:
            tot = x["exact_and_accepted"] + x["not_accepted_or_not_exact"] + x["raised"]
            lines.append(f"| {x['entry_bits']} | {x['message_bits']} | {tot} | {x['exact_and_accepted']} | {json.dumps(x['notes']) if x['notes'] else '—'} |")
        blocks["sb_e_magnitude"] = "\n".join(lines)
        blocks["sb_e_abstention"] = "; ".join(f"`{x['kw']}` → {x['outcome']}" for x in e["abstention"]) + "."
    return blocks


HEAD = RES / "head_0544ff4"


def build_head() -> dict[str, str]:
    """Blocks of ENG-RES-0019: the same tests, and the checks of the stored files, at the division's commit 0544ff4."""
    blocks: dict[str, str] = {}

    def hp(name):
        f = HEAD / name
        return json.loads(f.read_text()) if f.exists() else None

    a = hp("mincert_part_a.json")
    if a:
        a = a["result"]
        blocks["sbh_a"] = (f"{a['cases']:,} claims on random certificate trees at `0544ff4`: accepted {a['sb_accept']:,}, rejected {a['sb_reject']:,}; disagreements with our "
                           f"checker {a['disagree_ours']}; with the reference checker after conversion {a['disagree_reference']} of {a['reference_checked']:,}; acceptances above "
                           f"the true minimum {a['unsound_sb']}.")
    b, c = hp("mincert_part_b.json"), hp("mincert_part_c.json")
    if b:
        b = b["result"]
        blocks["sbh_b"] = f"{len(b)} traps at `0544ff4`: {sum(1 for r in b if r['as_expected'] and not r['unsound'])} behave as they should; unsound acceptances {sum(1 for r in b if r['unsound'])}."
    d = hp("mincert_part_d.json")
    if d:
        d = [r for r in d["result"] if r["name"] != "the unchanged document"]
        still = [r for r in d if r["their_loader"] == "loaded"]
        blocks["sbh_d"] = (f"Of the {len(d)} altered documents of ENG-RES-0018 §2 (F2), the loader of `0544ff4` refuses {sum(1 for r in d if r['their_loader'].startswith('raises MalformedCertificate'))} "
                           f"with `MalformedCertificate` and raises another exception for {sum(1 for r in d if r['their_loader'].startswith('raises') and 'MalformedCertificate' not in r['their_loader'])}; "
                           f"still loaded: {len(still)}" + (" (" + "; ".join(r["name"] for r in still) + ")" if still else "") + ".")
    e = hp("mincert_part_e.json")
    if e:
        e = e["result"]
        R = e["random"]
        blocks["sbh_e"] = (f"The producer at `0544ff4`, the short version of the tests of ENG-RES-0018 §1 E: {R['instances']} random instances against enumeration — wrong optimum "
                           f"{R['wrong_optimum']}, rejected {R['rejected']}, raised {sum(R['raised'].values())}; with a tolerance {e['tolerance']['instances']} instances, "
                           f"{e['tolerance']['bad']} bad; degenerate instances {sum(1 for x in e['degenerate'] if x['correct'])} of {len(e['degenerate'])} exact; trees "
                           f"{sum(1 for x in e['trees'] if x.get('correct'))} of {len(e['trees'])} exact against dynamic programming; dense instances "
                           f"{sum(1 for x in e['dense'] if x.get('correct'))} of {len(e['dense'])} exact against enumeration.")
    dp = hp("depth.json")
    if dp:
        lines = ["| chain: sites × states | eliminations | `dumps` | `loads`, then checked | `to_metricchain_cert1` | file, bytes |", "|---|---|---|---|---|---|"]
        for r in dp["rows"]:
            lines.append(f"| {r['sites']} × {r['states']} | {r['prune']:,} | {r['dumps']} | {r.get('loads', '—')} | {r['to_metricchain_cert1']} | {r.get('bytes', 0):,} |")
        blocks["sbh_depth"] = "\n".join(lines)
    f = RES / "dev_certificates_0544ff4.json"
    if f.exists():
        rows = json.loads(f.read_text())
        order = ["1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"]
        rows.sort(key=lambda r: order.index(r["pdb_id"]) if r["pdb_id"] in order else 99)
        lines = ["| structure | sites / states / pair tables | checksum of the tables = the file's = your row's | our checker | the tree proves (kcal/mol) | = your certified minimum | witness energy − bound | nodes: leaves / branches / eliminations (yours) | our check, s (yours) | toulbar2 through our own call: optimum equal; s |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            unit = 2 ** r["unit_bits"]
            st, ts = r["stats"], r.get("their_stats", {})
            lines.append(f"| {r['pdb_id']} | {r['sites']} / {r['states_total']} / {r['pairs']} | {'yes' if r['checksum_matches_certificate'] and r.get('their_model_sha256_matches') else '**NO**'} | "
                         f"{'accepted, full box' if r['accepted'] and r['full_box'] else r['reason']} | {r['proves'] / unit:.6f} | {'yes' if r['proves'] == r['claimed_lower_bound'] else '**NO**'} | "
                         f"{r.get('gap')} | {st['leaf']} / {st['branch']} / {st['prune']} ({ts.get('leaf')} / {ts.get('branch')} / {ts.get('prune')}) | {r['seconds']} ({r.get('their_check_seconds')}) | "
                         f"{'yes' if r.get('toulbar2_equals_certified') else '**NO**'}; {r.get('our_toulbar2_seconds')} |")
        blocks["sbh_files"] = "\n".join(lines)
        blocks["sbh_files_summary"] = (f"{len(rows)} stored certificate files: {sum(1 for r in rows if r['accepted'] and r['full_box'])} accepted on the full box by our checker; "
                                       f"{sum(1 for r in rows if r['proves'] == r['claimed_lower_bound'] and r.get('gap') == 0)} with the tree proving exactly the claimed bound and a witness "
                                       f"of that energy; {sum(1 for r in rows if r.get('toulbar2_equals_certified'))} with the same optimum from toulbar2 called by us; "
                                       f"{sum(1 for r in rows if r.get('their_cert_sha256_matches'))} files with the checksum your rows record.")
    pr = RES / "probe_head_0544ff4.json"
    if pr.exists():
        pv = json.loads(pr.read_text())
        k8 = pv["k8"]
        blocks["sbh_k8"] = (f"`full_box` on {len(k8)} hand-made boxes (the full box in order and permuted; boxes missing one state of either site, the minimiser's state, all but one "
                            f"configuration): {sum(1 for r in k8 if r['as_expected'])} of {len(k8)} as they should be.")
        lines = ["| structure | seed | low-energy configurations: number; largest `|ΔE_table − ΔE_OpenMM|`, kcal/mol; closest contact `r/σ` | random configurations: number; largest relative difference; largest `|ΔE|`, kcal/mol; closest contact | spread of the bonded terms, kcal/mol |",
                 "|---|---|---|---|---|"]
        for r in pv["k5"]:
            lo, ra = r["low_energy"], r["random"]
            lines.append(f"| {r['pdb_id']} | {r['seed']} | {lo['n']}; `{lo['max_abs_diff']:.1e}`; {lo['min_contact_ratio']:.2f} | {ra['n']}; `{ra['max_rel_diff']:.1e}`; `{ra['max_abs_energy']:.1e}`; "
                         f"{ra['min_contact_ratio']:.3f} | `{r['bonded_constant_max_spread']:.1e}` |")
        blocks["sbh_k5"] = "\n".join(lines)
    ks = RES / "kernel_small.json"
    if ks.exists():
        rows = json.loads(ks.read_text())
        chains = sorted((r for r in rows if r["name"].startswith("chain") and "ms_verify" in r["lean"]), key=lambda r: r["prune"])
        lines = ["| instance (chain of sites with 4 states) | eliminations in the chain | `verify`, ms | `verifyM`, ms | both accept the claimed bound | both digests equal the Python side's |",
                 "|---|---|---|---|---|---|"]
        for r in chains:
            L = r["lean"]
            lines.append(f"| {r['sites']} sites | {r['prune']} | {L['ms_verify']:,} | {L['ms_verifyM']} | {'yes' if L['verify_claimed_bound'] and L['verifyM_claimed_bound'] else '**NO**'} | "
                         f"{'yes' if r['digest_h_matches'] and r['digest_J_matches'] else '**NO**'} |")
        dense = [r for r in rows if r["name"].startswith("dense")]
        ratio = [chains[i + 1]["lean"]["ms_verify"] / chains[i]["lean"]["ms_verify"] for i in range(len(chains) - 1)]
        blocks["sbh_kernel_plain"] = "\n".join(lines) + (
            f"\n\nEach row has three eliminations more than the one above; the time of `verify` grows by factors of " + ", ".join(f"{x:.1f}" for x in ratio) +
            f" (doubling per elimination would be 8).  On {len(dense)} branching instances from your producer ({min(r['leaf'] for r in dense)}–{max(r['leaf'] for r in dense)} leaves, "
            f"chains of at most {max(r['prune'] for r in dense)} eliminations in total) both functions were executed as well: "
            f"{sum(1 for r in dense if r['lean'].get('verify_claimed_bound') and r['lean']['verifyM_claimed_bound'])} of {len(dense)} accepted by both; in all "
            f"{len(rows)} small cases `verifyM` refuses the claimed bound plus one unit in {sum(1 for r in rows if r['lean']['verifyM_bound_plus_one_unit'] is False)} "
            f"and the kernel's own energy of the witness equals the bound in {sum(1 for r in rows if r['witness_energy_equals_bound'])}.")
    kf = RES / "kernel_0544ff4.json"
    if kf.exists():
        rows = json.loads(kf.read_text())
        order = ["1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"]
        real = sorted((r for r in rows if r["corrupt"] is None), key=lambda r: order.index(r["name"]) if r["name"] in order else 99)
        lines = ["| structure | sites / `k` | leaves / branches / eliminations | `verifyM` (= `verify`) on the claimed bound | on the bound plus one unit | witness in the box; its energy by the kernel's `energy` = the bound | digests of the instance as the kernel reads it = the Python side's (unary; pair) | `verifyM`, s |",
                 "|---|---|---|---|---|---|---|---|"]
        for r in real:
            L = r["lean"]
            if "error" in L:
                lines.append(f"| {r['name']} | {r['sites']} / {r['states_max']} | {r['leaf']} / {r['branch']} / {r['prune']} | **not run: {L['error']}** | | | | |")
                continue
            dj = "not computed" if r["digest_J_matches"] is None else ("yes" if r["digest_J_matches"] else "**NO**")
            lines.append(f"| {r['name']} | {r['sites']} / {r['states_max']} | {r['leaf']} / {r['branch']} / {r['prune']} | {'**accepted**' if L['verifyM_claimed_bound'] else '**REFUSED**'} | "
                         f"{'refused' if L['verifyM_bound_plus_one_unit'] is False else '**ACCEPTED**'} | {'yes' if L['witness_in_box'] else '**NO**'}; "
                         f"{'yes' if r['witness_energy_equals_bound'] and r['witness_energy_matches'] else '**NO**'} | {'yes' if r['digest_h_matches'] else '**NO**'}; {dj} | {L['ms_verifyM'] / 1000:.1f} |")
        blocks["sbh_kernel"] = "\n".join(lines)
        ctrl = [r for r in rows if r["corrupt"] is not None]
        if ctrl:
            names = {"bound": "the claim raised by one unit of `2⁻¹²` of a table unit", "witness-entry": "one table entry used by the witness lowered by one unit (the witness then lies below the claim)",
                     "prune-order": "the eliminations of the chain in reverse order"}
            blocks["sbh_kernel_controls"] = ("Negative controls on " + ctrl[0]["name"].split(".")[0] + " (the translator alters its output; the kernel must refuse): " +
                                             "; ".join(f"{names.get(r['corrupt'], r['corrupt'])} — {'refused' if r['lean'].get('verifyM_claimed_bound') is False else '**ACCEPTED**'}" for r in ctrl) + ".")
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", type=Path)
    ap.add_argument("--verify", type=Path)
    args = ap.parse_args()
    blocks = build()
    blocks.update(build_head())
    target = args.write or args.verify
    if target is None:
        for k, v in blocks.items():
            print(f"### {k}\n{v}\n")
        return 0
    text = target.read_text()
    new = text
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- TABLE:{re.escape(name)} -->\n)(?:.*?\n)?(<!-- /TABLE:{re.escape(name)} -->)", re.S)
        new = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), new)
    if args.verify:
        print("tables in", target.name, "match the artifacts" if new == text else "DIFFER from the artifacts")
        return 0 if new == text else 1
    target.write_text(new)
    print("updated", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
