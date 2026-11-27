#!/usr/bin/env python3
"""Protocol FB-P-10: scores of PUBLIC CASP17 models against a reference already in the PDB,
computed with this division's own scoring code, to be frozen BEFORE the official numbers
exist and compared with them afterwards.

The object under test is our scoring code.  No MetricChain method is involved, the models are
the participants' own public predictions, and nothing here is an official CASP result.

usage: score_models.py MODELS_DIR REFERENCE.cif TARGET_ID TARGET_SEQUENCE OUT.csv [--chains A B] [--jobs N]

Definitions used (and where they may differ from the official evaluation):
  * correspondence: model residue numbers are positions in the CASP target sequence; reference
    residues are mapped to them by locating the target sequence inside the deposited entity
    sequence (an exact offset; mismatches are reported, not hidden);
  * reference atoms: first alternate location only; hydrogens ignored;
  * GDT_TS / GDT_HA / TM-score: CA atoms, over the reference residues that are observed
    (a model residue that is missing counts as not superposable);  heuristic superposition
    search (values are lower bounds on the true maxima);
  * lDDT: 15 A inclusion radius, thresholds 0.5/1/2/4 A, pairs within one residue excluded,
    NO stereochemistry penalty and NO relabelling of chemically equivalent atoms (the reference
    implementation does both), atoms missing from the model count as failed;
  * the official evaluation may use other residue ranges ("evaluation units") than the whole
    observed chain: that is the first thing to check when the numbers are compared.
"""
from __future__ import annotations

import argparse
import csv
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from metricchain_fb import scores  # noqa: E402

THREE_TO_ONE = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
                "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
                "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V", "MSE": "M"}


def read_model(path: Path):
    """Minimal fixed-column reader of the ATOM records of a CASP TS file: {(resnum, atom): xyz}, {resnum: resname}."""
    atoms, names = {}, {}
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if not line.startswith("ATOM"):
                continue
            try:
                atom = line[12:16].strip()
                resname = line[17:20].strip()
                resnum = int(line[22:26])
                xyz = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            except ValueError:
                continue
            element = line[76:78].strip() if len(line) >= 78 else ""
            if element == "H" or (not element and atom.startswith("H")):
                continue
            key = (resnum, atom)
            if key not in atoms:
                atoms[key] = xyz
                names.setdefault(resnum, resname)
    return atoms, names


def read_reference(cif_path: str, chain_name: str, target_sequence: str):
    import gemmi
    st = gemmi.read_structure(cif_path)
    st.setup_entities()
    chain = st[0][chain_name]
    polymer = chain.get_polymer()
    entity = st.get_entity_of(polymer)
    full = gemmi.one_letter_code(entity.full_sequence)
    # offset: target position i (1-based) <-> label_seq i + offset; chosen to maximise identities
    best = None
    for offset in range(-len(target_sequence), len(full)):
        same = sum(1 for i, c in enumerate(target_sequence, start=1)
                   if 1 <= i + offset <= len(full) and full[i + offset - 1] == c)
        if best is None or same > best[0]:
            best = (same, offset)
    identities, offset = best
    mismatches = [(i, target_sequence[i - 1], full[i + offset - 1]) for i in range(1, len(target_sequence) + 1)
                  if 1 <= i + offset <= len(full) and full[i + offset - 1] != target_sequence[i - 1]]
    atoms, resnames = {}, {}
    for res in polymer:
        i = res.label_seq - offset
        if not 1 <= i <= len(target_sequence):
            continue
        resnames[i] = res.name
        for atom in res:
            if atom.element.name == "H" or atom.altloc not in ("\0", "A"):
                continue
            atoms.setdefault((i, atom.name), (atom.pos.x, atom.pos.y, atom.pos.z))
    info = {"offset": offset, "identities": identities, "mismatches": mismatches,
            "observed_residues": len(resnames), "first": min(resnames), "last": max(resnames),
            "resolution": st.resolution}
    return atoms, resnames, info


_REF = {}


def score_one(args):
    path, chains = args
    model_atoms, model_names = read_model(Path(path))
    row = {"model": Path(path).name, "model_residues": len(model_names)}
    for chain in chains:
        ref_atoms, ref_names = _REF[chain]
        ca = sorted(i for (i, a) in ref_atoms if a == "CA")
        ref_ca = np.array([ref_atoms[(i, "CA")] for i in ca])
        present = np.array([(i, "CA") in model_atoms for i in ca])
        row[f"ca_ref_{chain}"] = len(ca)
        row[f"ca_common_{chain}"] = int(present.sum())
        if present.sum() < 3:
            continue
        # absent model residues are placed far away so that they can never be superposed or pass a distance test
        mod_ca = np.array([model_atoms.get((i, "CA"), (9e5 + 50.0 * k, 9e5, 9e5)) for k, i in enumerate(ca)])
        row[f"gdt_ts_{chain}"] = round(scores.gdt_ts(mod_ca, ref_ca), 3)
        row[f"gdt_ha_{chain}"] = round(scores.gdt_ha(mod_ca, ref_ca), 3)
        row[f"tm_{chain}"] = round(scores.tm_score(mod_ca, ref_ca), 4)
        row[f"lddt_ca_{chain}"] = round(scores.lddt(mod_ca, ref_ca, residue_index=np.array(ca)), 4)
        if chain == chains[0]:
            keys = sorted(ref_atoms)
            ref_all = np.array([ref_atoms[k] for k in keys])
            mod_all = np.array([model_atoms.get(k, (9e5 + 50.0 * n, 9e5, 9e5)) for n, k in enumerate(keys)])
            row[f"lddt_heavy_{chain}"] = round(scores.lddt(mod_all, ref_all, residue_index=np.array([k[0] for k in keys])), 4)
            row[f"heavy_atoms_ref_{chain}"] = len(keys)
            row[f"heavy_atoms_common_{chain}"] = sum(1 for k in keys if k in model_atoms)
            mism = sum(1 for i, name in ref_names.items() if i in model_names and model_names[i] != name)
            row["residue_name_mismatches"] = mism
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("models_dir")
    ap.add_argument("reference")
    ap.add_argument("target")
    ap.add_argument("sequence")
    ap.add_argument("out_csv")
    ap.add_argument("--chains", nargs="+", default=["A"])
    ap.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    for chain in args.chains:
        atoms, names, info = read_reference(args.reference, chain, args.sequence)
        _REF[chain] = (atoms, names)
        print(f"{args.target} reference chain {chain}: {info}", flush=True)
    paths = sorted(str(p) for p in Path(args.models_dir).rglob(f"{args.target}TS*") if p.is_file())
    print(f"{len(paths)} model files", flush=True)
    with Pool(args.jobs) as pool:
        rows = pool.map(score_one, [(p, args.chains) for p in paths], chunksize=4)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k != "model", k))
    with open(args.out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
