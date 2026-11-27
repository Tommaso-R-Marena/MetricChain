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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", type=Path)
    ap.add_argument("--verify", type=Path)
    args = ap.parse_args()
    blocks = build()
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
