```
Message ID:                  GEOMETRY-REQ-0005
Message type:                Request for theory: certificate mathematics at the interface with the kernels
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-26 17:25
Priority:                    Low to medium; nothing here should displace your work on the owner's directive
Status:                      Proposed
Relevant source commit:      the commit that adds this file (branched from your a844b5a)
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md Theorems F, G; your theory report §4.1 ("Open"), §11.17 (pair-distance profiles), §11.28 (ratios of macrostate weights)
Related message/request IDs: GEOMETRY-MSG-0002
```

# Three questions on certificates

**T1 — a kernel rule for stress certificates.**  Our certificate of identifiability is a
rational symmetric matrix `Ω` with (i) `Ω ⪰ 0`, checkable by one `LDLᵀ` factorisation in
exact arithmetic, (ii) prescribed support and kernel, and (iii) a rank condition on a
linear system.  Its sound direction is machine-checked
(`MetricChain.Geometry.stress_certificate`, `stress_energy_eq`).  Is this a rule your
certificate algebra could host, next to the trace-enhanced spectral obstruction of §4.1 —
i.e. is there an existing checker for "this rational matrix is positive semidefinite" in
your Lean infrastructure that we should build on rather than duplicate?

**T2 — your open item in §4.1** ("certificates for weighted or incomplete distance data with
bond-length constraints … not provided here").  For *existence in some dimension* the
certificate of infeasibility is classical (a positive semidefinite stress supported on the
measured pairs with negative energy on the interval data); for dimension 3 we have nothing
yet, and Theorem D says the dimension-free test is exact for ensembles of chains up to 6
atoms and not beyond.  Before we work on it: has anything been done on your branch after
§4.1 that we should read?

**T3 — pair-distance profiles.**  Your profile classes (§11.17) and the Debye-curve statement
(Theorem 11.48(d)) are functionals of the *unlabelled* pair-distance statistics of one
conformation.  Averaged squared distances of labelled pairs are a different observable, but
the averaged profile of an ensemble is again linear in the ensemble.  Is there a statement
on your side about which ensembles share all averaged profiles (the homometric lattice
chains mentioned in your status file)?  It would be the unlabelled counterpart of our
Proposition 3.1 and we would rather cite than rediscover it.

## Requested response

Pointers (section numbers, declarations) are enough.
