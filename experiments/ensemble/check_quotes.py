#!/usr/bin/env python3
"""Do the numbers quoted in docs/ensemble/ENSEMBLE_REPORT.md still agree with the stored outputs?

Three internal-review findings (ER1 F6, ER1 F18, ER2 F2) were sentences of the report that quoted numbers the
scripts did not print.  This table ties sentences of the report to lines of the stored outputs
(experiments/ensemble/output.txt, written by run_all.py, and output_threshold.txt):

  ("lit",   file, text in the stored output, text in the report)
        both texts must occur (white space is normalised);
  ("bound", file, regular expression with one group, bound, text in the report)
        the expression must match, every matched number must be at most `bound` in absolute value, and the text
        must occur in the report.  Used for round-off-level numbers, which differ between machines.

If a script changes what it prints, the first text disappears from the output and this check fails until the
sentence of the report has been looked at again.  It does not prove that a sentence says what the number means;
it proves that the number is the one the script printed.  The table is not exhaustive: it covers the passages
"Numerical check" of the report as of the fourth checkpoint.

Usage: python3 experiments/ensemble/check_quotes.py     (exit code 0 iff every entry holds; run_all.py runs it last)
"""
import pathlib, re, sys

here = pathlib.Path(__file__).resolve().parent
REPORT = here.parent.parent / "docs" / "ensemble" / "ENSEMBLE_REPORT.md"
norm = lambda t: " ".join(t.split())

O, TH = "output.txt", "output_threshold.txt"
FLOAT = r"([-+]?[0-9.]+(?:e[-+]?[0-9]+)?)"
TABLE = [
    # ---- Part I (exposedness_checks.py)
    ("lit", O, "1500/1500 agree (965 identifiable instances)", "965 of the instances are identified"),
    ("bound", O, r"duality gap \(max over 400 instances x 4 tolerances\): " + FLOAT, 3.5e-15,
     "primal and dual values agree to `3·10⁻¹⁵` at four tolerances"),
    ("lit", O, "kappa finite in 301", "(301 instances)"),
    ("bound", O, r"max relative \|omega\(1e-4\)/1e-4 - kappa\|: " + FLOAT, 4.5e-15, "`ω(10⁻⁴)/10⁻⁴ = κ` to `4·10⁻¹⁵`"),
    ("bound", O, r"sup-min formula for kappa_mu: max relative error " + FLOAT, 7e-15, "to `7·10⁻¹⁵`, no sampled `g` exceeds it"),
    ("bound", O, r"exact linearity and weight-independence: " + FLOAT, 5e-16, "to `5·10⁻¹⁶`"),
    # ---- Part II (rigidity_checks.py)
    ("lit", O, "K_4 in R^2, 2 conformers: 1240 non-constant splices", "(1 240; 2 904; 20 440; 79 998)"),
    ("lit", O, "K_4 in R^2, 3 conformers: 2904 non-constant splices", "(1 240; 2 904; 20 440; 79 998)"),
    ("lit", O, "K_5 in R^3, 2 conformers: 20440 non-constant splices, smallest |CM| = 1.623e-03",
     "least `1.6·10⁻³` in absolute value"),
    ("lit", O, "K_5 in R^3, 3 conformers: 79998 non-constant splices", "(1 240; 2 904; 20 440; 79 998)"),
    ("lit", O, "smallest least-squares residual over 180 random splices = 6.007e-04",
     "a residual of at least `6·10⁻⁴` on 180 random splices"),
    ("lit", O, "control: 20/20 planted realisable vectors found", "search finds 20 of 20 planted realisable vectors"),
    ("lit", O, "192/240 splices of the three blocks realised", "240 of 240 agreements, 192 realised"),
    ("lit", O, "agreement with the two-circle criterion 240/240", "240 of 240 agreements, 192 realised"),
    ("lit", O, "203 zeros found in 400 starts (100 near each conformer, 200 random); 128 at conformer 1, 75 at conformer 2, 0 elsewhere",
     "R5: all 203 zeros of the certificate `f` found from 400 starts (100 near each conformer, 200 random)"),
    ("lit", O, "128 at conformer 1, 75 at conformer 2", "one of the conformers (128 and 75)"),
    ("lit", O, "smallest violation of the equations of the variety over all splices = 1.53e-03", "`1.5·10⁻³` over 200 pairs"),
    ("lit", O, "the two conformers and three chimeras in 21/21 pairs", "two conformers and three chimeras in all 21 pairs"),
    ("lit", O, "11.29 (all 21)", "a mixed block `11.3`"),
    ("lit", O, "chimeras realised to 3.0e-15", "chimeras realised to `3·10⁻¹⁵`"),
    ("lit", O, "(LP, 3 weightings) = 0.0e+00", "largest chimera mass compatible with the eight laws is zero"),
    ("lit", O, "the exchanged pair has the same law on every measured edge in 200/200; the law of the unmeasured edge differs in 200/200",
     "R10: Example D2 on 200 random instances"),
    # ---- Part II, platforms (platform_checks.py)
    ("lit", O, "d = 2, 4 legs: smallest residual over 84 non-constant splices = 1.946e-03",
     "(264 splices, least-squares residual at least `1.9·10⁻³`"),
    ("lit", O, "d = 2, 5 legs: smallest residual over 180 non-constant splices", "(264 splices, least-squares residual at least `1.9·10⁻³`"),
    ("lit", O, "d = 3, 7 legs: smallest residual over 80 non-constant splices = 2.366e-03", "(80 splices, at least `2.4·10⁻³`)"),
    ("lit", O, "d = 2, 3 legs (free matroid): splices of nearby poses realised in 20/20 cases", "realised in 20 of 20 cases"),
    ("lit", O, "d = 3, 6 legs (free matroid): splices of nearby poses realised in 20/20 cases", "realised in 20 of 20 cases"),
    ("lit", O, "number of real poses with the three lengths -> {2: 38, 4: 59, 6: 3}", "(38, 59 and 3 of 100 instances; never one)"),
    ("lit", O, "a fourth leg singles out the true pose in 100/100; smallest mismatch of the fourth length at another pose of the fibre: 1.07e-03",
     "a fourth leg singles out the true pose in 100 of 100 (smallest mismatch of the fourth length at another pose of the fibre `1.1·10⁻³`)"),
    # ---- Part III (pair_capacity_checks.py)
    ("lit", O, "n = 5: triples containing a fixed vertex that are faces: 105/105; 4-sets: 445/455", "(105 and 465 triples); 10 of 455"),
    ("lit", O, "n = 6: triples containing a fixed vertex that are faces: 465/465; 4-sets: 1478/1500", "22 of 1 500 sampled four-sets"),
    ("lit", O, "7296 coefficient vectors with >= 2 non-zero entries: largest probability 3/4", "exhaustively on 7 296"),
    ("lit", O, "n = 30, K = 10: spurious sign vector in 119/1500 = 0.0793; 4*C(K,3)*(3/4)^n = 0.0857",
     "`0.079` against `0.086` (`n = 30`, `K = 10`)"),
    ("lit", O, "n = 36, K = 12: spurious sign vector in 16/600 = 0.0267; 4*C(K,3)*(3/4)^n = 0.0280",
     "`0.027` against `0.028` (`n = 36`, `K = 12`)"),
    ("lit", O, "n = 9: 198 random supports (K = 2..6); certificate implies fibre is a point in 198/198",
     "198 random supports with `K = 2, …, 6`"),
    ("lit", O, "smallest certificate gap: 0.434", "observed is `0.43`"),
    ("lit", O, "K = 5.5 n: smallest eigenvalue of sin(pi C/2) = -0.0568", "`−0.057` at `K = 5.5n`"),
    ("lit", O, "K = 6.34 n: smallest eigenvalue of sin(pi C/2) = +0.0119", "`+0.012` at `6.34n`"),
    ("lit", O, "K = 7.0 n: smallest eigenvalue of sin(pi C/2) = +0.0403", "`+0.040` at `7n`"),
    ("lit", O, "8 conformers (rank 8): 444 entries read", "(59, 117, 174, 285, 444 for 1, 2, 3, 5, 8 conformers, against 1 770 pairs)"),
    ("lit", O, "5 conformers (rank 5): 285 entries read", "(59, 117, 174, 285, 444 for 1, 2, 3, 5, 8 conformers, against 1 770 pairs)"),
    # ---- Part IV and V (finite_temperature_checks.py)
    ("bound", O, r"max over the class of TV\(mu, P_a\) - sum_i tau_i = " + FLOAT + r" \(exact", 1.4e-15, "is at most `1.4·10⁻¹⁵`"),
    ("lit", O, "360 (member, centre) pairs: max of TV - sum_i tau_i = -1.02e-01", "with a margin of at least `0.10`"),
    ("lit", O, "one-sided site envelopes (quasi-metrics): 96 cases; mu*_a (cost into the centre) is a member in 96/96",
     "for symmetric and for one-sided site envelopes"),
    ("lit", O, "with the cost out of the centre the measure is a member in 5/96", "is a member in only 5 of 96"),
    ("lit", O, "at most one unsaturated marginal: 60/60", "F3: (d) on 60 members"),
    ("lit", O, "n = 5, b = 1.0: max E[M^2] over the class = 10.233839; double cone: 10.233839; largest spread of a weight on the optimal face = 1.10e-01",
     "`0.110` for `n = 5`, `b = 1` (predicted: `0.1102`)"),
    ("lit", O, "predicted spread at the all-plus state 0.110218", "`0.110` for `n = 5`, `b = 1` (predicted: `0.1102`)"),
    ("bound", O, r"\(200 instances x 4 tolerances\): largest gap " + FLOAT, 1.05e-14, "on 200 random instances: gap `1.0·10⁻¹⁴`"),
    ("lit", O, "kappa = E sech^2(1 + Z) = 0.449600 (Gauss-Hermite), 0.449600 (trapezoid)", "`κ = 0.449600` by two quadratures"),
    ("lit", O, "= kappa/4 = 0.112400", "`0.112400 = κ/4`"),
    ("lit", O, "sqrt(kappa)/2 = 0.3353", "between `0.335·ω(2σ)` and `0.5·ω(2σ)`"),
    ("bound", O, r"every bond satisfied \(6 cases, exact\): max of TV - sum of deficits = " + FLOAT, 4.05e-15,
     "computed exactly, is at most `4·10⁻¹⁵` (six cases)"),
    ("bound", O, r"\(12 references, 1200 members\): max of TV - sum of deficits = " + FLOAT, 2e-15, "at most `2·10⁻¹⁵`"),
    ("lit", O, "(5 cases, exact): max of TV - sum of deficits = +0.196, +0.573, +0.109, +0.165, +0.254; "
               "max of mu(x_j = a_j) - mu*(x_j = a_j) = +0.555, +0.482, +0.057, +0.359, +0.328",
     "the total-variation bound fails by `0.11` to `0.57` and the population bound by `0.06` to `0.56`"),
    ("lit", O, "max of TV - sum of deficits = +0.169599, max population excess = +0.169599 (closed form +0.169599)",
     "equal the closed form `0.169599`"),
    ("lit", O, "(20 up-sets) = +0.00e+00 (positively associated), least lattice defect = -7.753e-03 (not log-supermodular)",
     "the lattice condition fails (defect `−7.8·10⁻³`)"),
    ("lit", O, "the up-set criterion (C) agrees with the exact maximum of TV - sum of deficits in 40/40, the criterion (B) with "
               "the exact maximal population excess in 40/40; (C) holds in 8, (B) in 5, positive association in 5",
     "agrees with the exact maximum of the excess over the class polytope in 40 of 40, and (B) with the exact maximal "
     "population excess in 40 of 40 ((C) holds in 8 of them, (B) and positive association in 5)"),
    ("lit", O, "lam = 11/13: largest pair covariance 0.0e+00; slack of (C) at U = {e_2 or e_3}: -0.043269 (formula (1 - 2 lam)/16 = "
               "-0.043269), least slack over all up-sets -0.043269; exact max of TV - sum of deficits = +0.047731",
     "(exact maxima of the excess `0.0477`, `0`, `0`)"),
    ("lit", O, "least Cov(e_i, N - e_i) = +0.0105 (the conditions (D) hold); at U = {e_2 = e_4 = 1}: E[N | U] - E[N | U^c] = 0.9634 < 1",
     "Every `Cov(e_i, N − e_i)` is at least `0.0105`, and for `U = {e_2 = e_4 = 1}` one has `E[N | U] − E[N | U^c] = 0.9634 < 1`"),
    ("lit", O, "(in the class: True) has TV = 0.2621 > sum of deficits = 0.2525", "has `TV = 0.2621` against a sum of `0.2525`"),
    ("lit", O, "decides the criterion (C) in 228/228 instances (the bound holds in 57 of them)",
     "decides the condition in 228 of 228 instances"),
    # ---- Part VI (lifted_checks.py)
    ("lit", O, "n = 12 (66 pair observables): lift-isolated frequency K = 24: 1.000, K = 33: 1.000, K = 49: 1.000, K = 54: 0.995, K = 66: 0.955",
     "frequency `1.000, 1.000, 1.000, 0.995, 0.955` at `K = 24, 33, 49, 54, 66`"),
    ("lit", O, "38 lift-isolated supports with K = 12..24", "38 lift-isolated supports with 12 to 24 conformers"),
    ("lit", O, "identification confirmed by the fibre LP in 38", "confirmed by a linear programme over all states in all 38"),
    ("lit", O, "46 random pairs of states (14 further pairs with some beta < 0.05 set aside): smallest observed "
               "f / (c* min(d_p^2, d_q^2)) = 1.25", "(14 further pairs with some `β < 0.05` were set aside)"),
    ("lit", O, "smallest observed f / (c* min(d_p^2, d_q^2)) = 1.25", "`1.25` (a pair with shared angles, where the ratio is `1/c*`)"),
    ("lit", O, "is between 0.147 and 0.297 of the bound", "is between `0.15` and `0.30` of the bound of (b)"),
    ("lit", O, "the permanent vanishes at a configuration at distance 1.32 from every state", "at distance `1.32` from all of them"),
    ("lit", O, "cube n = 6, all 41664 triples: Hall condition holds in 30720", "all 41 664 triples of states: the Hall condition holds for 30 720"),
    ("lit", O, "fails in 10944", "it fails for 10 944"),
    ("lit", O, "(zero set strictly larger than the triple in 960)", "strictly larger than the triple for 960"),
    # ---- Part VII (nonlinear_data_checks.py)
    ("lit", O, "ratio data: 60 instances; the optimal ensembles of the linear programme satisfy the ratio constraint; 40 instances "
               "with tolerance compared with 40 000 sampled ensembles each",
     "Q1: ratio data on 60 random instances"),
    ("lit", O, "least norm: 40 clouds in dimension 2 and 3; certificate z*.Phi - r^2 >= 0 on every cloud; features affinely "
               "independent on its zero set in 40", "features are affinely independent on its zero set in all 40"),
    ("lit", O, "largest (mass off the zero set)/(r tau/gamma) = 1.000; largest |mean - z*|/sqrt(2 r tau + tau^2) = 1.000",
     "the largest mass off the zero set is `1.000` of the bound `r_min τ/γ` and the largest displacement of the mean is `1.000` of"),
    ("lit", O, "largest (mass off the farthest configuration)/(tau/gamma') over the clouds = 0.966", "configuration is `0.966` of `τ/γ′`"),
    ("lit", O, "agrees with the subset-sum table in 60/60 (24 consistent)", "agrees with a subset-sum table in 60 of 60 (24 consistent)"),
    ("lit", O, "12 feasible instances: the net of 24 or 96 directions with the certified enlargement never falls below the fine "
               "search (1 440 directions)", "directions (12 instances)"),
    ("lit", O, "agree in 388/388 (62 determined up to the factor); the three-point example of the text: True",
     "agreement in 388 of 388 (62 determined up to the factor)"),
    ("lit", O, "agrees with the existence of an exact cover in 40/40 (20 with a cover)",
     "cover in 40/40 (20 with a cover)"),
    # ---- torus_six_states.py (report section 4c.4: E20a exact, E20b, E20c, E20d)
    ("lit", O, "the zero set of the lifted certificate is finite in all eight charts: ok",
     "the zero set of the lifted certificate is finite in all eight charts"),
    ("lit", O, "all six are rational: the five states and a sixth point: ok", "consists of the five states and a sixth rational point"),
    ("lit", O, "the six lifted outer products are linearly independent (rank 6): ok", "products have rank 6"),
    ("lit", O, "instance 1: rank of the 12 tangential conditions 12; dimension of the numerators vanishing on the curve 15",
     "the twelve conditions have rank 12 and the functions vanishing on the curve have dimension 15"),
    ("lit", O, "instance 2: rank of the 12 tangential conditions 12; dimension of the numerators vanishing on the curve 15",
     "at two rational six-tuples the curve is smooth at the states"),
    ("lit", O, "a measure with the same 27 data and no mass on the six states: in 10/10 instances",
     "finds a measure with the same 27 data and no mass on the six states in 10/10 instances"),
    ("lit", O, "singular value 11 is 0.7860, singular value 12 is below 1e-12", "value 11 is 0.7860, singular value 12 is below 1e-12"),
    ("lit", O, "real components of the curve: 1; the extra function on the curve: minimum above -1e-9, minimum at distance > 0.1 "
               "from the states 0.0023, maximum 2.1750", "(minimum at distance > 0.1 from the states 0.0023, maximum 2.1750)"),
    ("lit", O, "least mass on the six states among measures on the sampled curve with the same data: 1.000000",
     "on the six states among measures on the sampled curve with the same data: 1.000000"),
    ("lit", O, "smallest Hessian eigenvalue of f at the states 0.4199; global minimum of f on the torus above -1e-9 (grid of 48^3 "
               "points and 60 local refinements); local minima away from the states: none: all 60 end at a state",
     "has smallest Hessian eigenvalue 0.4199 at the states"),
    ("lit", O, "real components of the curve: 2; signs of the extra function on them: [-1, 1]",
     "is non-negative on one and non-positive on the other"),
    ("lit", O, "least mass on the six states among measures on the sampled curve with the same data: 0.000000",
     "exists (least mass on the six states 0.000000)"),
    ("lit", O, "r = 2, K = 3: 9 conditions on 9 numerators, rank 8", "8 for three states on `𝕋²`"),
    ("lit", O, "r = 3, K = 6: 24 conditions on 27 numerators, rank 24", "24, 26, 27 for six, seven, eight states on `𝕋³`"),
    ("lit", O, "r = 3, K = 7: 28 conditions on 27 numerators, rank 26", "seven states on `𝕋³` (rank 26, not 27)"),
    ("lit", O, "r = 3, K = 8: 32 conditions on 27 numerators, rank 27", "24, 26, 27 for six, seven, eight states on `𝕋³`"),
    ("lit", O, "r = 4, K = 16: 80 conditions on 81 numerators, rank 80", "80 and 81 for sixteen and seventeen states on `𝕋⁴`"),
    ("lit", O, "r = 4, K = 17: 85 conditions on 81 numerators, rank 81", "80 and 81 for sixteen and seventeen states on `𝕋⁴`"),
    ("lit", O, "its Hessian has eigenvalues of both signs at some state in 12/12 instances",
     "double points has a Hessian with eigenvalues of both signs at some state in 12/12 instances"),
    # ---- misspecification_checks.py (report Part VIII and Proposition E23.1)
    ("lit", O, "the criterion and the direct search agree in 300/300 (176 determined up to the gains and offsets)",
     "agree in 300/300 (176 determined up to the gains and offsets)"),
    ("lit", O, "determined with one common gain: True; with a separate gain for each pair of data: False",
     "If each pair has its own gain it is not"),
    ("lit", O, "1096 random cases (g = square, exp, cube of the modulus; random partitions)", "on 1096 random cases with random partitions"),
    ("bound", O, r"largest violation of convexity " + FLOAT + r", of g\(E phi\) <= D", 1e-10, "refinement are below `10⁻¹⁰`"),
    ("lit", O, "and its target value in the interval computed from it, in 200/200 cases", "computed from `𝒞` in 200/200 cases"),
    ("lit", O, "the library is falsified (no ensemble on it fits) in 49", "the library is falsified in 49"),
    ("lit", O, "it is a valid lower bound in 150/150 (positive in 49; largest loss 0.252)",
     "it is a valid lower bound in 150/150 (positive in 49; largest loss 0.252)"),
    ("lit", O, "K_min <= dim G + 1, in 120/120; the data bound the number of conformers from above (|X_G| < |X|) in 50",
     "in 120/120"),
    ("lit", O, "rank of the correlation matrix <= K_min <= number of conformers in 40/40 (rank = K_min in 39)",
     "most `K_min` in 40/40 (equal in 39)"),
    ("lit", O, "agrees with the existence of an exact cover in 40/40 (25 with a cover)", "on 40/40 random families (25 with a cover)"),
    # ---- torus_four_angles.py (report section 4c.4, Proposition E20e)
    ("lit", O, "seed 0: real components of the curve 1; functions on the curve 36; rank of the 26 conditions 26; candidates 10; "
               "NOT IDENTIFIED: no candidate is positive on the curve (dual margin 0.0800); a twin on the curve with least mass "
               "0.000000 on the states", "dual margin 0.0800; a twin on the curve with least mass 0.000000 on"),
    ("lit", O, "IDENTIFIED: a candidate with minimum 0.0030 on the curve at distance > 0.15 from the states; certificate with "
               "A = 1e+05: smallest Hessian eigenvalue at the states 0.2455, smallest local minimum away from the states 0.0027",
     "a candidate with minimum 0.0030 on the curve at distance > 0.15 from the states; certificate with A = 1e+05: smallest "
     "Hessian eigenvalue at the states 0.2455, smallest local minimum away from the states 0.0027"),
    ("lit", TH, "thirteen random states on T^4, seeds 0..19: IDENTIFIED: 13; NOT IDENTIFIED: 7", "Of 40 random 13-tuples, 26 are"),
    ("lit", TH, "thirteen random states on T^4, seeds 20..39: IDENTIFIED: 13; NOT IDENTIFIED: 3; UNDECIDED (a candidate on the "
                "curve; torus check failed): 1; UNDECIDED (no candidate; no twin found): 3", "4 are left undecided by the"),
    # ---- robustness_checks.py (Propositions E23.1(d), E17.2, E30, E31, E4.1)
    ("lit", O, "comes within 0.0048 of its ends; the truth is inside in every case", "comes within `0.0048` of its ends"),
    ("lit", O, "low-rank-plus-box error sets, 80 random instances", "equals the primal value on 80"),
    ("lit", O, "ellipsoidal error sets, 25 random instances: the primal value never exceeds the dual bound", "two agree within `1.0e-04` on 25 random instances"),
    ("lit", O, "and the two agree within 1.0e-04", "two agree within `1.0e-04` on 25 random instances"),
    ("lit", O, "40 random instances on a circle (720 points; pools of 60, 36 or 24 points)", "on 40 random instances on a"),
    ("lit", O, "the outer interval is 34.2 times as wide as the exact one (median)", "it is 34 times as wide as the exact interval (median)"),
    ("lit", O, "max_x w_x <= R_TV <= min(1, (1/2) sum_x w_x) in 30/30; the upper bound is 1.00 times R_TV (median), at most 1.42",
     "upper bound was at most `1.42` times the radius (median `1.00`)"),
    ("lit", O, "agrees with the subset-sum table in 40/40 (10 with a split)", "with the subset-sum table in 40/40 (10 with a split)"),
    ("lit", O, "never exceeds m eps/(m - K) (largest excess", "the largest mass off the conformers never exceeds `mε/(m − K)` and reaches"),
    ("lit", O, "and reaches 1.000 of it", "1.000 of it"),
    # ---- threshold computations (output_threshold.txt)
    ("lit", TH, "K = 24 K/n = 1.09 face frequency = 0.583", "| 22 (24) | — | 1.00 | 0.58 | 0.08 | 0.00 | 0.00 |"),
    ("lit", TH, "K = 22 K/n = 1.10 face frequency = 0.625", "| 20 (40) | — | 1.00 | 0.63 | 0.10 | 0.00 | 0.00 |"),
    ("lit", TH, "K = 18 K/n = 1.12 face frequency = 0.660", "(`0.66, 0.62, 0.63, 0.58` for `n = 16, 18, 20, 22`)"),
    ("lit", TH, "K = 6 K/n = 0.50 0.995 0.165 0.830 0.000", "with `K = 6` conformers `99.5 %` are faces and `16.5 %` have a certificate of degree 2"),
    ("lit", TH, "K = 9 K/n = 0.75 0.920 0.005 0.915 0.000", "with `K = 9`, `92 %` and `0.5 %`"),
    ("lit", TH, "K = 11 K/n = 0.92 0.815 0.000 0.815 0.000", "with `K = 11`, `81.5 %` and none"),
    ("lit", TH, "K = 3 K/n = 0.30 1.000 0.773 0.227 0.000", "the frequency `0.773` of a degree-2 certificate"),
    ("lit", TH, "K = 20 K/n = 1.11 face frequency = 0.617", "(`0.66, 0.62, 0.63, 0.58` for `n = 16, 18, 20, 22`)"),
    ("lit", TH, "n = 14, data of even order <= 4: 8192 states modulo flip, 1093 features (constant included); lift dimension "
                "C(n-1,<=2) = 92; Cover-type bound 2*D_odd = 598", "against the lift dimension `92` and `2D_odd = 598`"),
    ("lit", TH, "K = 320 face frequency = 1.000 lift-isolated = 0.000 (undecided 0; mean iterations 12.5; 2595 s)",
     "the face frequency is `1.000` at `K = 320`, `0.200` at `K = 340` and `0.000` at `K = 360`"),
    ("lit", TH, "K = 340 face frequency = 0.200 lift-isolated = 0.000 (undecided 0; mean iterations 10.7; 1879 s)",
     "the half-point lies between 320 and 340"),
    ("lit", TH, "K = 360 face frequency = 0.000 lift-isolated = 0.000 (undecided 0; mean iterations 8.9; 1156 s)",
     "the face frequency is `1.000` at `K = 320`, `0.200` at `K = 340` and `0.000` at `K = 360`"),
    ("lit", TH, "n = 14: N = 8192, D = 1092, D/N = 0.133: Gaussian threshold 295.8; lift dimension 92; 2 D_odd = 598",
     "at the size of `n = 14` the curve gives `295.8`"),
    ("lit", TH, "n = 12: N = 2048, D = 561, D/N = 0.274: Gaussian threshold 215.2; lift dimension 67; 2 D_odd = 352",
     "`76.4, 142.0, 215.2`"),
]


def main():
    report = norm(REPORT.read_text())
    texts = {name: norm((here / name).read_text()) for name in (O, TH)}
    bad = []
    for entry in TABLE:
        if entry[0] == "lit":
            _, name, out_text, rep_text = entry
            if norm(out_text) not in texts[name]:
                bad.append(f"not in {name}: {out_text}")
        else:
            _, name, pattern, bound, rep_text = entry
            found = re.findall(pattern, texts[name])
            if not found:
                bad.append(f"no match in {name}: {pattern}")
            elif max(abs(float(v)) for v in found) > bound:
                bad.append(f"bound {bound:g} exceeded in {name} ({', '.join(found)}): {pattern}")
        if norm(rep_text) not in report:
            bad.append(f"not in the report: {rep_text}")
    print(f"quoted numbers: {len(TABLE)} entries, {len(bad)} failure(s)")
    for line in bad:
        print("    " + line)
    print("PASS" if not bad else "FAIL")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
