"""Exact vertex enumeration of the Lipschitz polytope of a weighted cube and the block bounds of the Markov
recursion that are computed from it (request R10-E1 of the science division; theory workstream Y, Proposition F).

Modules
-------
``polytope``   the polytope, exact vertex tests, the edges at a vertex, four independent exact enumerators
               (breadth-first search over the graph of the polytope, plain and by orbits; a depth-first search
               over tight spanning structures; brute force over bases with exact rank tests; the Parma
               Polyhedra Library when it is installed), symmetry and canonical members of orbits.
``chambers``   the symbolic form ``phi = A + r B`` of a vertex, its interval of validity in the slope ratio
               ``r``, the chamber of a vertex set, the walk over all chambers.
``ckernel``    ctypes front end of ``wcube_kernel.c`` (the same breadth-first search over orbits, and
               floating-point scans of all vertices).
``exponents``  the fixed point ``u*``, the block law, Gibbs laws, capacity and Renyi site functions with
               duality brackets, the certified supremum over ``t``, interval-arithmetic certificates, and the
               closed forms of the uniform cube.

Everything is written from the mathematical definitions (stated, with the proofs of the facts the enumeration
rests on, in the module docstrings; drivers and results: ``experiments/eng/weighted_cube/``); no code of the
other divisions is used.
"""
