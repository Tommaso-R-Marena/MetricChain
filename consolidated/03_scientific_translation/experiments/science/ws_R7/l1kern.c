/* R7 own kernel: pairwise l1 distances between rows of a (C x P) double matrix.
   Written before reading engineering code. */
#include <math.h>
#include <stdint.h>
#include <stdlib.h>

/* full distance matrix */
void l1_full(const double *S, int64_t C, int64_t P, double *D) {
    for (int64_t a = 0; a < C; a++) {
        const double *ra = S + a * P;
        D[a * C + a] = 0.0;
        for (int64_t b = a + 1; b < C; b++) {
            const double *rb = S + b * P;
            double acc = 0.0;
            for (int64_t k = 0; k < P; k++) acc += fabs(ra[k] - rb[k]);
            D[a * C + b] = acc;
            D[b * C + a] = acc;
        }
    }
}

/* counts[t*C + a] = #{b : D(a,b) <= thr[t] + tol} (b = a included);
   also returns in mind[t] the smallest |D(a,b) - thr[t]| over a != b            */
void l1_ball_counts(const double *S, int64_t C, int64_t P, const double *thr, int64_t T,
                    double tol, int64_t *counts, double *mind) {
    for (int64_t t = 0; t < T; t++) mind[t] = INFINITY;
    for (int64_t i = 0; i < T * C; i++) counts[i] = 0;
    for (int64_t a = 0; a < C; a++) {
        const double *ra = S + a * P;
        for (int64_t t = 0; t < T; t++) counts[t * C + a] += 1;
        for (int64_t b = a + 1; b < C; b++) {
            const double *rb = S + b * P;
            double acc = 0.0;
            for (int64_t k = 0; k < P; k++) acc += fabs(ra[k] - rb[k]);
            for (int64_t t = 0; t < T; t++) {
                double m = fabs(acc - thr[t]);
                if (m < mind[t]) mind[t] = m;
                if (acc <= thr[t] + tol) { counts[t * C + a] += 1; counts[t * C + b] += 1; }
            }
        }
    }
}

/* nearest distinct neighbour distance of every row: nn[a] = min_{b != a} D(a,b) */
void l1_nearest(const double *S, int64_t C, int64_t P, double *nn) {
    for (int64_t a = 0; a < C; a++) nn[a] = INFINITY;
    for (int64_t a = 0; a < C; a++) {
        const double *ra = S + a * P;
        for (int64_t b = a + 1; b < C; b++) {
            const double *rb = S + b * P;
            double acc = 0.0;
            for (int64_t k = 0; k < P; k++) acc += fabs(ra[k] - rb[k]);
            if (acc < nn[a]) nn[a] = acc;
            if (acc < nn[b]) nn[b] = acc;
        }
    }
}

/* R7: integer-valued distances and ties of the cover relation, without storing the matrix.
   n_int      = number of unordered pairs a<b with |D - rint(D)| < tol
   near       = smallest |D - rint(D)| among the others
   ties[e]    = number of ORDERED pairs (a,y), a != y, with |D(a,y) - (gmin[y] + eps[e])| < tol
   nearest[e] = smallest |D(a,y) - (gmin[y] + eps[e])| among the others                              */
void l1_integer_stats(const double *S, int64_t C, int64_t P, const double *gmin, const double *eps, int64_t E,
                      double tol, int64_t *n_int, double *near, int64_t *ties, double *nearest) {
    *n_int = 0; *near = INFINITY;
    for (int64_t e = 0; e < E; e++) { ties[e] = 0; nearest[e] = INFINITY; }
    for (int64_t a = 0; a < C; a++) {
        const double *ra = S + a * P;
        for (int64_t b = a + 1; b < C; b++) {
            const double *rb = S + b * P;
            double acc = 0.0;
            for (int64_t k = 0; k < P; k++) acc += fabs(ra[k] - rb[k]);
            double f = fabs(acc - rint(acc));
            if (f < tol) (*n_int)++; else if (f < *near) *near = f;
            for (int64_t e = 0; e < E; e++) {
                double s1 = fabs(acc - (gmin[b] + eps[e]));   /* centre a, point b */
                double s2 = fabs(acc - (gmin[a] + eps[e]));   /* centre b, point a */
                if (s1 < tol) ties[e]++; else if (s1 < nearest[e]) nearest[e] = s1;
                if (s2 < tol) ties[e]++; else if (s2 < nearest[e]) nearest[e] = s2;
            }
        }
    }
}
