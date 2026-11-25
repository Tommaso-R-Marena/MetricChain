"""compact dump of selected instances (for writing the report)"""
import json, os, sys
import numpy as np
sel = [("S",6,"E","0.70"),("S",6,"P2","0.70"),("S",6,"H","0.70"),("S",6,"H","0.60"),("V",12,"E","0.70"),("V",12,"P2","0.70"),
       ("L",16,"H","0.60"),("L",16,"E","0.60"),("L",16,"P2","0.60"),("F",10,"H","0.60"),("F",8,"E","0.60"),("F",7,"P2","0.60"),
       ("K",4,"H","0.70"),("K",4,"H","0.60"),("K",3,"E","0.70"),("K",4,"E","0.70"),("K",4,"P2","0.70"),("K",3,"P2","0.60"),
       ("LKSE",5,"H","0.60"),("LKSE",6,"H","0.60"),("LKSE",5,"E","0.60"),("LKSE",6,"E","0.60"),("LKSE",5,"P2","0.60"),("LKSE",6,"P2","0.60")]
names = sys.argv[1:] or ["GB"]
for res, n, bb, tau in sel:
    tag = f"fb_{res}{'c' if res == 'LKSE' else ''}{n}_{bb}_R3_t0.60"
    p = f"out/an_{tag}_tau{tau}.json"
    if not os.path.exists(p):
        print(f"{res}{n}/{bb}/{tau}: MISSING"); continue
    r = json.load(open(p))
    if r.get("empty"):
        print(f"{res}{n}/{bb}/{tau}: EMPTY"); continue
    for nm in names:
        g = r.get(f"Xp|{nm}"); i = r.get(f"iface|{nm}")
        if not g: continue
        line = f"{res}{n}/{bb}/{tau} [{nm}] X'={r['size_pruned']} Xtau={r['clashfree']}: c_i max {max(g['c']):.2f} min {min(g['c']):.2f} rms {np.mean(g['rms']):.2f} (sup/rms {max(g['c'])/max(np.mean(g['rms']),1e-9):.1f})"
        if "C" in g:
            line += f"; c_ij {np.max(g['C']):.2f}; halfrow {max(g['half_rowsum']):.2f}; Dob {max(g['dobrushin']):.2f}"
        if g.get("c3max") is not None:
            line += f"; c3 {g['c3max']:.4f} sum {g['c3sum']:.3f}"
        ft = g.get("fit")
        if ft:
            line += f"; fit1 {ft['ls1_rms']:.3f}/{ft['ls1_max']:.2f}; fit2 {ft.get('ls2_rms', float('nan')):.4f}/{ft.get('ls2_max', float('nan')):.4f}/{ft.get('sup2', float('nan')):.4f}; std {ft['std']:.2f}"
        if i:
            s = i["star_argmin_E"]; b = i.get("ball2", {})
            line += (f" || sharp {i['sharp_argmin_E']}/{n} lam* {i['lambda_star']:.4f} eps1 {i['eps_one_eval']:.2f} lncosh {i['lncosh']:.1f} Jensen {i['jensen']:.2f} | star N={s['nstar']} eps* {s['eps_star']:.2f} br {s['bracket']:.3f} rem {s['rem_max']:.2f}<=bound {s['bound_max']:.2f} minexc {min(s['min_excitation']):.2f} rowsum_ok {s['rowsum_plain_ok']}"
                     f" | ball N={b.get('nball')} eps {b.get('eps', float('nan')):.4f} br {b.get('bracket', float('nan')):.4f} rem {b.get('rem_max', float('nan')):.4f}<= {b.get('bound_max', float('nan')):.4f} | same_min {i['same_min']} regret {i['regret']:.2f}")
        t = r.get(f"Xtau|{nm}")
        if t:
            line += f" || Xtau: c_i {max(t['c']):.2f} c_ij {np.max(t['C']):.2f} c3 {t.get('c3max', float('nan')):.3f} fit2 {t.get('fit', {}).get('ls2_rms', float('nan')):.4f}/{t.get('fit', {}).get('ls2_max', float('nan')):.4f}"
        print(line)
