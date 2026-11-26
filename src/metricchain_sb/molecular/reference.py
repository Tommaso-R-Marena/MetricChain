"""Independent validation of the tables against a full-system OpenMM energy (§6).

The reference System re-expresses the model with OpenMM force objects, evaluated by OpenMM
(Reference platform, double precision) on full coordinates — no table code is used:
  group 0: PeriodicTorsionForce (all torsions, as assigned),
           CustomNonbondedForce  4 eps((sig/r)^12-(sig/r)^6) + C q1 q2 / (eps0*10*r^2)   (r in nm,
                                 Lorentz-Berthelot, NoCutoff, every NonbondedForce exception excluded),
           CustomBondForce       the same expression with the exception's (chargeProd, sigma, epsilon)
                                 for every exception with nonzero chargeProd or epsilon (the 1-4 pairs);
  group 1: HarmonicBondForce and HarmonicAngleForce (must be constant under chi rotation).
Differences E(x) - E(x_ref) cancel the constant terms (fixed-atom torsions and fixed-fixed pairs).
"""
from __future__ import annotations

import numpy as np
import openmm

from .tables import KJ_PER_KCAL, EnergyTables, MolecularModel, one_4pi_eps0

_LJ_DDD = "4*eps*((sig/r)^12-(sig/r)^6) + {c!r}*{qq}/({eps0!r}*10*r^2)"


def build_reference_system(model: MolecularModel) -> openmm.System:
    src = model.prepared.system
    forces = {f.__class__.__name__: f for f in src.getForces()}
    nb = forces["NonbondedForce"]
    ref = openmm.System()
    for p in range(src.getNumParticles()):
        ref.addParticle(src.getParticleMass(p))
    clone = lambda f: openmm.XmlSerializer.deserialize(openmm.XmlSerializer.serialize(f))
    for name, group in (("PeriodicTorsionForce", 0), ("HarmonicBondForce", 1), ("HarmonicAngleForce", 1)):
        f = clone(forces[name])
        f.setForceGroup(group)
        ref.addForce(f)
    c, eps0 = one_4pi_eps0(), float(model.eps0)
    pair = openmm.CustomNonbondedForce(
        _LJ_DDD.format(c=c, qq="q1*q2", eps0=eps0) + "; sig=0.5*(sig1+sig2); eps=sqrt(eps1*eps2)")
    for name in ("q", "sig", "eps"):
        pair.addPerParticleParameter(name)
    pair.setNonbondedMethod(openmm.CustomNonbondedForce.NoCutoff)
    for p in range(nb.getNumParticles()):
        q, s, e = nb.getParticleParameters(p)
        pair.addParticle([q._value, s._value, e._value])          # e, nm, kJ/mol
    one_four = openmm.CustomBondForce(_LJ_DDD.format(c=c, qq="qq", eps0=eps0))
    for name in ("qq", "sig", "eps"):
        one_four.addPerBondParameter(name)
    for k in range(nb.getNumExceptions()):
        p1, p2, qq, s, e = nb.getExceptionParameters(k)
        pair.addExclusion(p1, p2)
        if qq._value != 0.0 or e._value != 0.0:
            one_four.addBond(p1, p2, [qq._value, s._value, e._value])
    for f in (pair, one_four):
        f.setForceGroup(0)
        ref.addForce(f)
    return ref


def openmm_reference_energy(model: MolecularModel, configs, group: int = 0,
                            platform: str = "Reference") -> np.ndarray:
    """OpenMM energies (kcal/mol) of force group `group` for full configurations `configs`."""
    system = build_reference_system(model)
    ctx = openmm.Context(system, openmm.VerletIntegrator(1.0), openmm.Platform.getPlatformByName(platform))
    out = []
    for x in configs:
        ctx.setPositions(model.positions_for(x) / 10.0)     # Angstrom -> nm
        e = ctx.getState(getEnergy=True, groups={group}).getPotentialEnergy()
        out.append(e.value_in_unit(openmm.unit.kilojoule_per_mole) / KJ_PER_KCAL)
    return np.array(out)


def icm_descent(t: EnergyTables, x0, clipped: bool = False) -> list[int]:
    """Iterated conditional modes on the tables from x0 (a local minimum: no single-site move lowers E)."""
    unary, pair = (t.unary, t.pair) if clipped else (t.unary_unclipped, t.pair_unclipped)
    n, x = len(unary), list(x0)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            cond = unary[i].copy()
            for j in range(n):
                if j < i:
                    cond += pair[(j, i)][x[j], :]
                elif j > i:
                    cond += pair[(i, j)][:, x[j]]
            best = int(np.argmin(cond))
            if cond[best] < cond[x[i]] - 1e-12:
                x[i], changed = best, True
    return x


def low_energy_walk(t: EnergyTables, x0, n: int, window: float, rng) -> list[list[int]]:
    """`n` distinct configurations with unclipped E <= E(native) + window, by a seeded random walk
    from x0 that changes one random site to a random state and rejects moves leaving the window."""
    e_cap = t.table_energy([0] * len(t.unary), clipped=False) + window
    x, e, out, seen = list(x0), t.table_energy(x0, clipped=False), [], {tuple(x0)}
    for _ in range(200 * n):
        if len(out) == n:
            break
        i = int(rng.integers(len(x)))
        y = list(x)
        y[i] = int(rng.integers(len(t.unary[i])))
        ey = t.table_energy(y, clipped=False)
        if ey <= e_cap:
            x, e = y, ey
            if tuple(x) not in seen:
                seen.add(tuple(x))
                out.append(list(x))
    return out


def _min_contact_ratio(model: MolecularModel, x) -> float:
    """min r / sigma_pq over LJ-active (eps_pq > 0) non-excluded atom pairs with >= 1 moving atom."""
    from .tables import _Params
    params = _Params(model.prepared.system)
    pos = model.positions_for(x)
    moving = np.unique(np.concatenate([s.moving for s in model.sites]))
    qq, sig, eps = params.block(moving, np.arange(len(pos)))
    r = np.linalg.norm(pos[moving][:, None] - pos[None], axis=-1)
    ok = (eps > 0) & (r > 0)
    return float(np.min(r[ok] / sig[ok]))


def validate_against_openmm(t: EnergyTables, n_random: int = 20, seed: int = 0, n_clash_free: int = 20,
                            window: float = 10.0) -> dict:
    """Compare E_table(x) - E_table(ref) with E_OpenMM(x) - E_OpenMM(ref), ref = all-native (all 0)."""
    model = t.model
    ks = [len(u) for u in t.unary]
    rng = np.random.default_rng(seed)
    x_ref = [0] * len(ks)
    rand = [[int(rng.integers(k)) for k in ks] for _ in range(n_random)]
    x_min = icm_descent(t, x_ref)
    icm = [x_min] + low_energy_walk(t, x_min, n_clash_free, window, rng)
    configs = [x_ref] + rand + icm
    e_omm = openmm_reference_energy(model, configs, group=0)
    e_bonded = openmm_reference_energy(model, configs, group=1)
    e_tab = np.array([t.table_energy(x, clipped=False) for x in configs])
    d_omm, d_tab = e_omm - e_omm[0], e_tab - e_tab[0]
    diff = d_omm - d_tab
    nr = 1 + n_random

    def block(sl, xs):
        dd, ee = diff[sl], d_omm[sl]
        return {"n": len(dd), "diff": dd.tolist(), "e_openmm": ee.tolist(),
                "max_abs_diff": float(np.max(np.abs(dd))),
                "max_rel_diff": float(np.max(np.abs(dd) / np.maximum(np.abs(ee), 1e-300))),
                "max_abs_energy": float(np.max(np.abs(ee))),
                "min_contact_ratio": min(_min_contact_ratio(model, x) for x in xs)}

    return {
        "seed": seed, "reference": "all-native configuration (state 0 at every site)",
        "e_ref_openmm_group0": float(e_omm[0]), "e_ref_table": float(e_tab[0]),
        "random": block(slice(0, nr), configs[:nr]),
        "clash_free": dict(block(slice(nr, None), icm), window_kcal=window,
                           how="ICM descent on the unclipped tables from native, then distinct configurations "
                               "of a seeded single-site random walk restricted to E_table <= E_table(native) + window"),
        "bonded_constant_max_spread": float(np.max(e_bonded) - np.min(e_bonded)),
    }
