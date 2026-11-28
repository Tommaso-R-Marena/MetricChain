# Public data used as development evidence: umbrella sampling of a valine side-chain torsion

Copied unchanged from the PyMBAR repository, <https://github.com/choderalab/pymbar>, commit
`ed40ec3bbef03bb08938ad1a74d459b0d1ab81f7`, directory `examples/umbrella-sampling-fes/data/`
(MIT licence, `LICENSE.pymbar`): `centers.dat` (26 umbrella centres in degrees and spring constants in
kJ/mol/rad²) and `prod{0..25}_dihed.xvg` (501 snapshots of the χ torsion per umbrella, 0.2 ps apart).
The energy files of the example are not needed (all umbrellas at 300 K) and were not copied.

Source of the simulations: D. L. Mobley, A. P. Graves, J. D. Chodera, A. C. McReynolds, B. K. Shoichet,
K. A. Dill, "Predicting absolute ligand binding free energies to a simple model site",
J. Mol. Biol. 371 (2007) 1118-1134 (valine 111 of T4 lysozyme L99A with benzene bound).

This is an existing public dataset with no ground truth: everything computed from it by this division is
development evidence (docs/mbar/VALIDATION.md, section 6), not a held-out evaluation.
