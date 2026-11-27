# fragility_real.py -- the reduction under published nearest-neighbour parameter values
# (ViennaRNA parameter files: Turner 2004, Turner 1999, Andronescu 2007, DNA Mathews 2004/1999),
# with exterior loops (i) free [the model of the theorem], (ii) with dangles in two conventions,
# (iii) with flush coaxial stacking as strong as the corresponding stack.
# Same criterion as fragility.py: threshold E_til (energy of any tiling structure);
# the reduction is valid for a model iff every NO instance has MFE > E_til.
import os, sys
from lib import *
from params import *
import test_main
from fragility import e_tiling

PDIR = os.path.join(os.path.dirname(HERE), "review1_params")
SETS = ["rna_turner2004", "rna_turner1999", "rna_andronescu2007", "dna_mathews2004", "dna_mathews1999"]


def build_models(name):
    P = Params(os.path.join(PDIR, name + ".par"))
    sigma = P.stack(2, 1)
    nf = lambda f: nickfree_energy(P, f)
    nf_nndb = lambda f: nickfree_energy(P, f) + states_bulge_correction(f)
    ms = [
        Model(name + " | exterior 0 (theorem's model)", sigma, nf, None),
        Model(name + " | dangles 'all' (d2 style)", sigma, nf, lambda f: ext_d2(P, f)),
        Model(name + " | dangles 'some'", sigma, nf, lambda f: ext_some(P, f)),
        Model(name + " | coax(flush)=stack, no dangles", sigma, nf, lambda f: sigma if f.flush else 0),
        Model(name + " | coax(flush)=stack + dangles 'some'", sigma, nf, lambda f: sigma if f.flush else ext_some(P, f)),
    ]
    if name == "rna_turner2004":
        ms += [
            Model(name + " + NNDB 1-nt bulge rule | exterior 0", sigma, nf_nndb, None),
            Model(name + " + NNDB 1-nt bulge rule | dangles 'all'", sigma, nf_nndb, lambda f: ext_d2(P, f)),
            Model(name + " + NNDB 1-nt bulge rule | coax + dangles 'some'", sigma, nf_nndb, lambda f: sigma if f.flush else ext_some(P, f)),
        ]
    return P, ms


if __name__ == "__main__":
    insts = [i for i in dict.fromkeys(test_main.INSTANCES) if i[1] * i[2] <= 10 and i[3] != "L"]
    data = []
    for a, m, B, mode in insts:
        res = run_enum(system(a, m, B), prune=(mode in "PL"), orbit=(mu_fact(a) <= 24 and m * B <= 10))
        faces = {i: Face(s) for i, s in res["desc"].items()}
        data.append((a, m, B, packable(a, m, B), res, faces))
    ny = sum(d[3] for d in data)
    print("instances: %d (YES %d, NO %d); energies in 0.01 kcal/mol" % (len(data), ny, len(data) - ny))
    allfaces = {}
    for d in data:
        for f in d[5].values():
            allfaces[f.s] = f
    for name in SETS:
        P, models = build_models(name)
        # hypotheses check on every nick-free loop that occurs in the instances
        sigma = P.stack(2, 1)
        nfl = [(nickfree_energy(P, f), f) for f in allfaces.values() if f.kind in ("bulge", "interior")]
        neg = [(e, f.s) for e, f in nfl if e < 0]
        worst = min(nfl, key=lambda t: t[0])
        # generalised hypothesis: g(f) > sigma * iota(f)
        viol_gen = [(e, f.s) for e, f in nfl if not (e > sigma * f.iota)]
        mingap = min(e - sigma * f.iota for e, f in nfl)
        print("\n=== %s: GG/CC stack = %d; %d distinct bulge/interior loops occur; min energy %d (%s); negative: %d; "
              "generalised hypothesis g > sigma*iota violated by %d loops (min of g - sigma*iota = %d)" % (
                  name, sigma, len(nfl), worst[0], worst[1].s, len(neg), len(viol_gen), mingap))
        if name == "rna_turner2004":
            nfl2 = [(nickfree_energy(P, f) + states_bulge_correction(f), f) for f in allfaces.values() if f.kind in ("bulge", "interior")]
            neg2 = sorted((e, f.s) for e, f in nfl2 if e < 0)
            print("    with the NNDB single-nucleotide bulge rule (special C bulge, -RT ln states): negative loops: %s" % neg2[:6])
        for mod in models:
            no_ok = no_bad = yes_ok = yes_bad = til_ok = til_bad = 0
            ex = None
            mingap = None
            for a, m, B, pk, res, faces in data:
                n = len(a)
                M = m * B - n
                et = e_tiling(mod, n, m, M)
                h = evaluate(res, mod, faces)
                mfe = min(h)
                if pk:
                    for e, (l_, p_, t_) in h.items():
                        assert (t_ == 0) or (e == et), (mod.name, a, m, B, e, et)
                    if mfe == et:
                        yes_ok += 1
                    else:
                        yes_bad += 1
                        ex = ex or ("YES %s m=%d B=%d: MFE %d < E_til %d" % (a, m, B, mfe, et))
                    if mfe == et and h[mfe][0] == h[mfe][2]:
                        til_ok += 1
                    else:
                        til_bad += 1
                else:
                    if mfe > et:
                        no_ok += 1
                        mingap = (mfe - et) if mingap is None else min(mingap, mfe - et)
                    else:
                        no_bad += 1
                        ex = ex or ("NO %s m=%d B=%d: MFE %d <= E_til %d" % (a, m, B, mfe, et))
            print("  %-62s NO: MFE>E_til %2d ok/%2d bad (min gap %s) | YES: MFE==E_til %2d/%2d | minima==tilings %2d/%2d  %s" % (
                mod.name.split("|", 1)[1].strip() if "NNDB" not in mod.name else mod.name.split("+", 1)[1].strip(),
                no_ok, no_bad, mingap, yes_ok, yes_bad, til_ok, til_bad, ex or ""))
