"""
P7 item 4: further lines derived from out/p7_04_survey.json (no computation; run after p7_04_survey.py).

usage: python3 -B p7_04b_tables.py > logs/p7_04b_tables.log   (last line "DONE p7_04b_tables")
"""
import sys, os, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, "out", "p7_04_survey.json")))
assert J["complete"]
rows = J["rows"]
sh = [r for r in rows if r["status"] == "shares"]
gp = [r for r in rows if r["status"] == "gap"]
print(f"{len(rows)} models: {len(sh)} with shares, {len(gp)} with a gap, other statuses: {sorted(set(r['status'] for r in rows) - {'shares', 'gap'})}")
t = sorted((r["t"], r["family"] + str(r["nres"]) + "/" + r["bb"], r["tau"], r["model"]) for r in sh)
print(f"slack t of the share programme over the {len(sh)} certified models: smallest {t[0][0]:.3e} kcal/mol ({t[0][1]} tau {t[0][2]} {t[0][3]}), "
      f"median {t[len(t) // 2][0]:.4f}; the rounding unit of the published instance is 2^-40 = {2.0 ** -40:.2e}")
print(f"models with a gap: in {len(set((r['tag'], r['tau']) for r in gp))} of {len(set((r['tag'], r['tau']) for r in rows))} instance files; "
      f"distinct (peptide, backbone): {sorted(set(r['family'] + str(r['nres']) + '/' + r['bb'] for r in gp))}")
print(f"root certificates by shares {J['stat']['root_cert']}, by one triple {J['stat']['root_bf'] - J['stat']['root_cert']}")
print("\ngap models (x0 min. = the reference minimises the model, so the certificate certifies x0 for the class):")
print(f"{'instance':11s} {'tau':4s} {'model':18s} {'x0 min.':>7s} {'vertex den.':>11s} {'gap':>9s} {'gap/margin':>10s} | {'sites that certify':18s} {'leaves, 1 per state':>19s} {'single-state splits':>19s} {'closing triples':>15s}")
for r in gp:
    print(f"{r['family'] + str(r['nres']) + '/' + r['bb']:11s} {r['tau']:4s} {r['model']:18s} {'yes' if r['criterion'] else 'no':>7s} {r['vertex_den']:11d} {-r['relaxation']:9.5f} {-r['relaxation'] / r['margin']:10.2f} | "
          f"{str(r['working']):18s} {str(r['least_leaves_depth1']):>19s} {len(r['single_state_splits']):19d} {str(len(r['closing_triples'])) + ' of ' + str(r['ntriples']):>15s}")
print("DONE p7_04b_tables")
