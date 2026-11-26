"""Discrete rotamer model with pairwise-decomposable energy tables (STRUCTBIO molecular layer).

THE MODEL.  Every downstream claim is conditional on exactly this definition.

1. Structure.  One protein chain of a PDB entry, first model, first alternate location, waters
   and heterogens dropped, input hydrogens deleted and re-added by OpenMM 8.6
   `Modeller.addHydrogens(ForceField('amber14-all.xml'), pH=7.0)` (this also fixes histidine
   tautomers and termini: NH3+ / COO-; the new H are minimised by addHydrogens itself with heavy
   atoms immobile, from random starts seeded by `seed`).  Heavy atoms are the deposited coordinates, unchanged;
   no minimisation.  Missing residues/heavy atoms or non-standard residues -> `StructureRejected`
   (see prepare.py).  Fixed sequence: no residue is ever mutated.

2. Sites.  A residue is a flexible site iff it has >= 1 chi angle (table in chi.py) and is not
   PRO (its ring closes on the backbone N) and not a disulfide-bonded CYS (CYX).  GLY and ALA
   have no chi.  Chain-terminal residues ARE sites (their charged termini are backbone atoms,
   which never move).  The moving atoms S_i of a site are the atoms reached from CB in the bond
   graph without crossing CA, excluding CB itself (so CB's hydrogens move under chi1).  A state
   is produced from the prepared coordinates by rigid rotations about chi bonds 1, 2, ... in
   turn (Rodrigues rotation of the atoms distal to atom 3 of the chi about the atom2->atom3
   axis by target - current); bond lengths and bond angles are those of the prepared structure.

3. States.  State 0 = "native": the prepared coordinates (chi angles as measured).  States
   1.. = the Cartesian product of the idealised staggered library (rotamers.py) over the chis
   of the site, in chi order.  `max_states_per_site=m` keeps the native state plus the m-1
   library states with lowest UNCLIPPED self energy U_i (ties by library order), kept in
   library order; recorded in meta.  `include_native=False` drops the native state.

4. Energy (kcal/mol), Amber ff14SB parameters as assigned by OpenMM's ForceField:
   E(x) = E_const + sum_i U_i(x_i) + sum_{i<j} P_ij(x_i, x_j), with E_const := 0.0 (energy of
   the fixed atoms alone; not computed).  Pair energy of atoms p, q at distance r (Angstrom):
       e_pq(r) = 4 eps_pq [(sig_pq/r)^12 - (sig_pq/r)^6] + C qq_pq / (eps0 r^2)
   with C = ONE_4PI_EPS0 (as used by OpenMM's NonbondedForce, 138.935457644382 kJ mol^-1 nm
   e^-2) * 10 / 4.184 = 332.0637133... kcal mol^-1 A e^-2 (distance-dependent dielectric
   eps(r) = eps0 * r/A, eps0 = 4 by default).  For ordinary pairs qq = q_p q_q,
   sig = (sig_p + sig_q)/2, eps = sqrt(eps_p eps_q) (Lorentz-Berthelot); for pairs listed in the
   NonbondedForce exceptions (1-2, 1-3: zero; 1-4: chargeProd = q_p q_q / 1.2, eps scaled 0.5)
   the exception's (chargeProd, sigma, epsilon) are used.  No cutoff.
   U_i(a) = sum of all PeriodicTorsionForce terms (propers and impropers) with >= 1 atom in S_i
            + sum of e over pairs inside S_i(a) + sum of e over pairs S_i(a) x B,
   P_ij(a, b) = sum of e over pairs S_i(a) x S_j(b), B = all atoms in no S_i.
   It is asserted that no torsion and no exception couples moving atoms of two sites.
   Bond and angle terms are invariant under chi rotation (checked numerically in
   reference.py) and are omitted.  No solvent term: the model is "ff14SB vdW + torsions +
   distance-dependent-dielectric Coulomb, in vacuo" — a force-field model, not nature.

5. Clipping.  With e_clip set (default 1000 kcal/mol) unary/pair = min(entry, e_clip) after
   construction; the unclipped tables are kept and are the ones validated against OpenMM.
"""
from __future__ import annotations

import dataclasses
import functools
import itertools
import json
import platform
import time

import numpy as np
import openmm

from .chi import CHI_ATOMS, dihedral_deg, rotate_about_axis
from .prepare import PreparedStructure, prepare_structure
from .rotamers import library_table, library_values

FORMAT = "structbio-energy-tables/1"
KJ_PER_KCAL = 4.184
_PAIR_BLOCK = 2_000_000   # max atom-pair-state elements per vectorised block


@functools.lru_cache(maxsize=1)
def one_4pi_eps0() -> float:
    """OpenMM's Coulomb constant (kJ mol^-1 nm e^-2), read from a two-charge NonbondedForce."""
    system = openmm.System()
    force = openmm.NonbondedForce()
    for _ in range(2):
        system.addParticle(1.0)
        force.addParticle(1.0, 1.0, 0.0)
    system.addForce(force)
    ctx = openmm.Context(system, openmm.VerletIntegrator(1.0), openmm.Platform.getPlatformByName("Reference"))
    ctx.setPositions([openmm.Vec3(0, 0, 0), openmm.Vec3(1, 0, 0)])
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(openmm.unit.kilojoule_per_mole)


def coulomb_kcal() -> float:
    return one_4pi_eps0() * 10.0 / KJ_PER_KCAL


@dataclasses.dataclass
class Site:
    index: int
    residue: object                 # openmm.app.Residue
    resname: str
    moving: np.ndarray              # global atom indices of S_i (sorted)
    state_coords: np.ndarray        # (k, m, 3) Angstrom
    chis: list                      # per state: list of chi angles (degrees, measured)
    origins: list                   # per state: 'native' | 'library'

    @property
    def n_states(self) -> int:
        return len(self.origins)

    def subset(self, keep):
        self.state_coords = self.state_coords[keep]
        self.chis = [self.chis[a] for a in keep]
        self.origins = [self.origins[a] for a in keep]


@dataclasses.dataclass
class MolecularModel:
    prepared: PreparedStructure
    sites: list
    eps0: float

    @property
    def topology(self):
        return self.prepared.topology

    @property
    def positions(self) -> np.ndarray:
        return self.prepared.positions

    def positions_for(self, x) -> np.ndarray:
        """Full coordinates (Angstrom) for a configuration: a sequence of states, or {site: state}."""
        items = x.items() if isinstance(x, dict) else enumerate(x)
        pos = self.positions.copy()
        for i, a in items:
            site = self.sites[i]
            pos[site.moving] = site.state_coords[a]
        return pos


@dataclasses.dataclass
class EnergyTables:
    unary: list
    pair: dict
    unary_unclipped: list
    pair_unclipped: dict
    meta: dict
    model: MolecularModel | None = dataclasses.field(default=None, repr=False, compare=False)  # not persisted

    def table_energy(self, x, clipped: bool = True) -> float:
        unary, pair = (self.unary, self.pair) if clipped else (self.unary_unclipped, self.pair_unclipped)
        e = sum(float(u[x[i]]) for i, u in enumerate(unary))
        return e + sum(float(p[x[i], x[j]]) for (i, j), p in pair.items())


# --------------------------------------------------------------------------- geometry
def _neighbours(topology):
    nbr = [set() for _ in range(topology.getNumAtoms())]
    for a, b in topology.bonds():
        nbr[a.index].add(b.index)
        nbr[b.index].add(a.index)
    return nbr


def _distal(nbr, start, blocked):
    """Atoms reachable from `start` without passing through `blocked` (start included)."""
    seen, todo = {start}, [start]
    while todo:
        u = todo.pop()
        for v in nbr[u]:
            if v == blocked and u == start:
                continue
            if v == blocked:
                raise ValueError(f"atoms {start} and {blocked} lie on a ring: not a rotatable chi bond")
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def _disulfide(res, nbr, atoms):
    sg = next(a.index for a in res.atoms() if a.name == "SG")
    return any(atoms[v].name == "SG" and atoms[v].residue is not res for v in nbr[sg])


def _make_site(index, res, positions, nbr, include_native):
    names = {a.name: a.index for a in res.atoms()}
    quads = [tuple(names[n] for n in q) for q in CHI_ATOMS[res.name]]
    moving = sorted(_distal(nbr, names["CB"], names["CA"]) - {names["CB"]})
    local = {g: k for k, g in enumerate(moving)}
    distal = []
    for q in quads:
        d = _distal(nbr, q[2], q[1]) - {q[2]}
        if not d <= set(moving):
            raise ValueError(f"{res.name}{res.id}: chi atoms distal to {q[1]}-{q[2]} are not side-chain atoms")
        distal.append(np.array([local[g] for g in sorted(d)]))
    native = [float(dihedral_deg(*positions[list(q)])) for q in quads]
    coords, chis, origins = [], [], []
    if include_native:
        coords.append(positions[moving].copy())
        chis.append(native)
        origins.append("native")
    for target in itertools.product(*[library_values(res.name, k) for k in range(len(quads))]):
        pos = positions.copy()
        for q, d, t in zip(quads, distal, target):
            cur = dihedral_deg(*pos[list(q)])
            idx = np.asarray(moving)[d]
            pos[idx] = rotate_about_axis(pos[idx], pos[q[1]], pos[q[2]], t - cur)
        coords.append(pos[moving])
        chis.append([float(dihedral_deg(*pos[list(q)])) for q in quads])
        origins.append("library")
    return Site(index, res, res.name, np.array(moving), np.array(coords), chis, origins)


# --------------------------------------------------------------------------- energies
def _nb(r2, qq, sig, eps, c_over_eps0):
    inv = 1.0 / r2
    s6 = (sig * sig * inv) ** 3
    return 4.0 * eps * (s6 * s6 - s6) + c_over_eps0 * qq * inv


class _Params:
    """Per-atom nonbonded parameters (e, Angstrom, kcal/mol) and the exception table."""

    def __init__(self, system):
        forces = {f.__class__.__name__: f for f in system.getForces()}
        expected = {"HarmonicBondForce", "HarmonicAngleForce", "PeriodicTorsionForce", "NonbondedForce"}
        if set(forces) != expected:
            raise ValueError(f"unexpected force set {sorted(forces)} (expected {sorted(expected)})")
        nb = forces["NonbondedForce"]
        if nb.getNonbondedMethod() != openmm.NonbondedForce.NoCutoff:
            raise ValueError("NonbondedForce must use NoCutoff")
        n = system.getNumParticles()
        self.q, self.sig, self.eps = np.zeros(n), np.zeros(n), np.zeros(n)
        for p in range(n):
            q, s, e = nb.getParticleParameters(p)
            self.q[p], self.sig[p] = q.value_in_unit(openmm.unit.elementary_charge), s.value_in_unit(openmm.unit.angstrom)
            self.eps[p] = e.value_in_unit(openmm.unit.kilojoule_per_mole) / KJ_PER_KCAL
        self.exceptions = {}
        for k in range(nb.getNumExceptions()):
            p1, p2, qq, s, e = nb.getExceptionParameters(k)
            self.exceptions[(min(p1, p2), max(p1, p2))] = (
                qq.value_in_unit(openmm.unit.elementary_charge ** 2), s.value_in_unit(openmm.unit.angstrom),
                e.value_in_unit(openmm.unit.kilojoule_per_mole) / KJ_PER_KCAL)
        self.partners = [[] for _ in range(n)]
        for (p1, p2), val in self.exceptions.items():
            self.partners[p1].append((p2, val))
            self.partners[p2].append((p1, val))
        self.torsions = []
        tf = forces["PeriodicTorsionForce"]
        for k in range(tf.getNumTorsions()):
            *atoms, per, phase, kk = tf.getTorsionParameters(k)
            self.torsions.append((tuple(atoms), per, phase.value_in_unit(openmm.unit.radian),
                                  kk.value_in_unit(openmm.unit.kilojoule_per_mole) / KJ_PER_KCAL))

    def block(self, rows, cols):
        """(qq, sig, eps) matrices for atoms rows x cols, exceptions applied."""
        qq = np.outer(self.q[rows], self.q[cols])
        sig = 0.5 * (self.sig[rows][:, None] + self.sig[cols][None, :])
        eps = np.sqrt(np.outer(self.eps[rows], self.eps[cols]))
        cpos = {g: k for k, g in enumerate(cols)}
        for r, a in enumerate(rows):
            for b, val in self.partners[a]:
                if b in cpos:
                    qq[r, cpos[b]], sig[r, cpos[b]], eps[r, cpos[b]] = val
        return qq, sig, eps


def _torsion_energy(site, torsions, positions):
    local = {g: k for k, g in enumerate(site.moving)}
    k = site.n_states
    e = np.zeros(k)
    for atoms, per, phase, kk in torsions:
        p = [site.state_coords[:, local[a]] if a in local else np.broadcast_to(positions[a], (k, 3))
             for a in atoms]
        phi = np.radians(dihedral_deg(*p))
        e += kk * (1.0 + np.cos(per * phi - phase))
    return e


def _unary(site, torsions, params, positions, background, c):
    mv = site.moving
    X = site.state_coords                                         # (k, m, 3)
    qq, sig, eps = params.block(mv, background)
    r2 = np.sum((X[:, :, None, :] - positions[background][None, None]) ** 2, axis=-1)
    e = _nb(r2, qq, sig, eps, c).sum(axis=(1, 2))
    iu, iv = np.triu_indices(len(mv), 1)
    qq, sig, eps = params.block(mv, mv)
    r2 = np.sum((X[:, iu] - X[:, iv]) ** 2, axis=-1)
    e += _nb(r2, qq[iu, iv], sig[iu, iv], eps[iu, iv], c).sum(axis=1)
    return e + _torsion_energy(site, torsions, positions)


def _pair(si, sj, params, c):
    qq, sig, eps = params.block(si.moving, sj.moving)
    Xi, Xj = si.state_coords, sj.state_coords
    out = np.empty((si.n_states, sj.n_states))
    step = max(1, _PAIR_BLOCK // (sj.n_states * qq.size))
    for a0 in range(0, si.n_states, step):
        d = Xi[a0:a0 + step, None, :, None, :] - Xj[None, :, None, :, :]
        out[a0:a0 + step] = _nb(np.sum(d * d, axis=-1), qq, sig, eps, c).sum(axis=(2, 3))
    return out


# --------------------------------------------------------------------------- build
def build_model(pdb_path, chain_id=None, eps0=4.0, include_native=True, repair_with_pdbfixer=False, seed=0):
    prepared = prepare_structure(pdb_path, chain_id, repair_with_pdbfixer=repair_with_pdbfixer, seed=seed)
    nbr = _neighbours(prepared.topology)
    atoms = list(prepared.topology.atoms())
    sites, fixed = [], []
    for res in prepared.topology.residues():
        if not CHI_ATOMS[res.name]:
            reason = "no side-chain chi angle"
        elif res.name == "PRO":
            reason = "proline ring closes on backbone N"
        elif res.name == "CYS" and _disulfide(res, nbr, atoms):
            reason = "disulfide-bonded cysteine (CYX)"
        else:
            sites.append(_make_site(len(sites), res, prepared.positions, nbr, include_native))
            continue
        fixed.append({"resnum": res.id, "resname": res.name, "reason": reason})
    return MolecularModel(prepared, sites, eps0), fixed


def build_energy_tables(pdb_path: str, chain_id: str | None = None, eps0: float = 4.0,
                        e_clip: float | None = 1000.0, max_states_per_site: int | None = None,
                        include_native: bool = True, seed: int = 0,
                        repair_with_pdbfixer: bool = False) -> EnergyTables:
    t0 = time.perf_counter()
    model, fixed = build_model(pdb_path, chain_id, eps0, include_native, repair_with_pdbfixer, seed)
    t1 = time.perf_counter()
    params = _Params(model.prepared.system)
    site_of = np.full(len(model.positions), -1)
    for s in model.sites:
        site_of[s.moving] = s.index
    background = np.flatnonzero(site_of < 0)
    for (p1, p2) in params.exceptions:
        if site_of[p1] >= 0 and site_of[p2] >= 0 and site_of[p1] != site_of[p2]:
            raise ValueError(f"exception {p1}-{p2} couples moving atoms of sites {site_of[p1]} and {site_of[p2]}")
    site_torsions = [[] for _ in model.sites]
    for tor in params.torsions:
        owners = {int(site_of[a]) for a in tor[0]} - {-1}
        if len(owners) > 1:
            raise ValueError(f"torsion {tor[0]} involves moving atoms of sites {sorted(owners)}")
        if owners:
            site_torsions[owners.pop()].append(tor)
    c = coulomb_kcal() / eps0
    unary = [_unary(s, site_torsions[s.index], params, model.positions, background, c) for s in model.sites]
    if max_states_per_site is not None:
        first = 1 if include_native else 0
        for i, s in enumerate(model.sites):
            lib = first + np.argsort(unary[i][first:], kind="stable")[:max(0, max_states_per_site - first)]
            keep = list(range(first)) + sorted(int(a) for a in lib)
            s.subset(keep)
            unary[i] = unary[i][keep]
    t2 = time.perf_counter()
    pair = {(i, j): _pair(model.sites[i], model.sites[j], params, c)
            for i in range(len(model.sites)) for j in range(i + 1, len(model.sites))}
    t3 = time.perf_counter()

    n_clip_u = n_clip_p = 0
    if e_clip is None:
        unary_c, pair_c = [u.copy() for u in unary], {k: p.copy() for k, p in pair.items()}
    else:
        unary_c = [np.minimum(u, e_clip) for u in unary]
        pair_c = {k: np.minimum(p, e_clip) for k, p in pair.items()}
        n_clip_u = int(sum(np.sum(u > e_clip) for u in unary))
        n_clip_p = int(sum(np.sum(p > e_clip) for p in pair.values()))
    meta = dict(model.prepared.meta)
    meta.update({
        "format": FORMAT,
        "model": "ff14SB vdW + torsions + distance-dependent-dielectric Coulomb, in vacuo (see tables.py docstring)",
        "energy_function": {
            "units": "kcal/mol", "forcefield": "Amber ff14SB (openmm amber14-all.xml)",
            "terms": ["PeriodicTorsionForce terms with >=1 moving atom", "LJ 12-6 Lorentz-Berthelot",
                      "Coulomb with eps(r) = eps0 * r/Angstrom"],
            "eps0": eps0, "one_4pi_eps0_kJ_nm": one_4pi_eps0(), "coulomb_constant_kcal_A": coulomb_kcal(),
            "kJ_per_kcal": KJ_PER_KCAL, "cutoff": None, "solvent": None,
            "exceptions": "OpenMM NonbondedForce exceptions as assigned (1-2/1-3 zero, 1-4 scaled 1/1.2 and 0.5)",
            "omitted_constant_terms": ["HarmonicBondForce", "HarmonicAngleForce", "fixed-atom torsions",
                                       "fixed-fixed nonbonded"],
        },
        "e_const": 0.0,
        "e_const_note": "energy of the fixed atoms alone; not computed, stored as 0.0",
        "clipping": {"e_clip": e_clip, "n_clipped_entries": n_clip_u + n_clip_p,
                     "n_clipped_unary": n_clip_u, "n_clipped_pair": n_clip_p},
        "max_states_per_site": max_states_per_site, "include_native": include_native,
        "seed": seed, "seed_note": "seeds the random initial H positions of addHydrogens (prepare.py); nothing else is random",
        "terminal_residues": "included as sites when they have a chi (termini are backbone atoms)",
        "library": library_table(),
        "sites": [{
            "index": s.index, "chain": meta["source"]["chain"], "resnum": s.residue.id, "resname": s.resname,
            "variant": meta["preparation"]["histidine_protonation"].get(s.residue.id) if s.resname == "HIS" else None,
            "chi_names": [f"chi{k + 1}" for k in range(len(CHI_ATOMS[s.resname]))],
            "chi_atoms": [list(q) for q in CHI_ATOMS[s.resname]],
            "n_moving_atoms": len(s.moving), "n_torsions": len(site_torsions[s.index]),
            "n_states": s.n_states, "chi_angles": s.chis, "origin": s.origins,
        } for s in model.sites],
        "fixed_residues": fixed,
        "n_sites": len(model.sites), "n_pairs": len(pair), "n_background_atoms": int(len(background)),
        "software": {"openmm": openmm.__version__, "numpy": np.__version__, "python": platform.python_version()},
        "timings_s": {"prepare_and_states": t1 - t0, "unary": t2 - t1, "pair": t3 - t2, "total": t3 - t0},
    })
    return EnergyTables(unary_c, pair_c, unary, pair, meta, model)


# --------------------------------------------------------------------------- io
def save_energy_tables(t: EnergyTables, path_prefix: str) -> None:
    arrays = {}
    for i, (u, uu) in enumerate(zip(t.unary, t.unary_unclipped)):
        arrays[f"unary_{i}"], arrays[f"unary_unclipped_{i}"] = u, uu
    for (i, j), p in t.pair.items():
        arrays[f"pair_{i}_{j}"], arrays[f"pair_unclipped_{i}_{j}"] = p, t.pair_unclipped[(i, j)]
    np.savez_compressed(path_prefix + ".npz", **arrays)
    with open(path_prefix + ".json", "w") as fh:
        json.dump(dict(t.meta, format=FORMAT), fh, indent=1)


def load_energy_tables(path_prefix: str) -> EnergyTables:
    with open(path_prefix + ".json") as fh:
        meta = json.load(fh)
    if meta.get("format") != FORMAT:
        raise ValueError(f"{path_prefix}.json: format {meta.get('format')!r} is not {FORMAT!r}")
    n = meta["n_sites"]
    with np.load(path_prefix + ".npz") as z:
        unary = [z[f"unary_{i}"] for i in range(n)]
        unary_u = [z[f"unary_unclipped_{i}"] for i in range(n)]
        keys = [(i, j) for i in range(n) for j in range(i + 1, n)]
        pair = {k: z[f"pair_{k[0]}_{k[1]}"] for k in keys}
        pair_u = {k: z[f"pair_unclipped_{k[0]}_{k[1]}"] for k in keys}
    return EnergyTables(unary, pair, unary_u, pair_u, meta)
