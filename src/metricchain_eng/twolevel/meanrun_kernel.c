/* Mean run of Algorithm 2L+ (theory report §11.19): C kernel.
 *
 * A line-by-line port of metricchain_eng/twolevel/meanrun.py (the reference implementation,
 * which documents the model); tests/eng/test_twolevel.py requires the two to agree on random
 * instances.  All quantities are natural logarithms.
 *
 * Build:  cc -O2 -shared -fPIC -o build/libmeanrun.so src/metricchain_eng/twolevel/meanrun_kernel.c -lm
 */
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define LN2 0.6931471805599453
#define TOL 1e-10

enum { POP = 0, NEG = 1, STOP_POP = 2, STOP_UNPOP = 3 };
enum { ST_CLOSED_POP = 0, ST_CLOSED_UNPOP = 1, ST_ABORT_LEVELS = 2, ST_ABORT_SAMPLE = 3 };

typedef struct {
    int n, n_o, J, m_max, L, harper, enforce_abort, oracle; /* oracle: 0 bottom, 1 top */
    double u, lam, b, eta, theta, lK, lnu, psi0, t0;
    /* constants needed for the claims */
    double lpi_dag, lM_bar, lMneg_cap, lcount_factor, x_out, lcnt_const; /* lcnt(x) = max(lK, lcnt_const + x) */
    double tie; /* weights within tie of a level (in the logarithm) are treated as equal to it */
} mr_params;

/* results: indices into res[] */
enum {
    R_STATUS = 0, R_JSTOP, R_RCLOSE, R_LM_LAST, R_LM_MAX, R_LL, R_LU, R_LA, R_NPOP, R_NNEG, R_MIN_POP_RADIUS,
    R_SLACK_VALID_LOWER, R_SLACK_VALID_UPPER, R_SLACK_WIDTH, R_MARGIN_III, R_SLACK_IV_M, R_SLACK_IV_MNEG,
    R_SLACK_IV_MBAR, R_SLACK_V, R_SLACK_VI, R_LCOST, R_COUNT
};

static double logaddexp(double x, double y) {
    if (x == y) return x + LN2;
    double d = x - y;
    if (d > 0) return x + log1p(exp(-d));
    if (d <= 0) return y + log1p(exp(d));
    return x + y; /* NaN */
}

/* number of entries of the ascending array a[0..n-1] that are <= v  (numpy searchsorted side="right") */
static int upper_bound(const double *a, int n, double v) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= v) lo = mid + 1; else hi = mid;
    }
    return lo;
}

/* number of entries that are < v  (side="left") */
static int lower_bound(const double *a, int n, double v) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < v) lo = mid + 1; else hi = mid;
    }
    return lo;
}

/* the largest k >= 0 with |B(m,k)| <= max{1, count} */
static int kball(const double *lball, int m, double logcount) {
    double t = (logcount > 0.0 ? logcount : 0.0) + TOL;
    int k = upper_bound(lball, m + 1, t) - 1;
    return k > 0 ? k : 0;
}

/* the least r in 0..m with |B(m,r)| >= 2^m q */
static int radius(const double *lball, int m, double lq) {
    if (lq >= 0.0) return m;
    if (lq < -LN2) return lower_bound(lball, m + 1, m * LN2 + lq - TOL);
    double l1mq = log(-expm1(lq));
    if (isinf(l1mq)) return m;
    int c = upper_bound(lball, m + 1, m * LN2 + l1mq + TOL) - 1;
    return c >= 0 ? m - c - 1 : m;
}

int mr_run(const mr_params *p, int natoms, const double *lw, const double *lpr, const double *ltail_ge,
           const double *lE, const double *lball, const double *lT, const double *xs, const double *lC,
           int n_grid, const double *grid,
           double *lM, signed char *kind, double *lq_rec, double *lMneg_rec, double *lcalls, double *res) {
    const int n_o = p->n_o, J = p->J, L = p->L;
    const int n_i = p->n - p->n_o;
    const double u = p->u, lam = p->lam, b = p->b, eta = p->eta;
    const double lK = p->lK, lnu = p->lnu;
    const double lth = log(p->theta), l1me = log(1 - eta), l1pe = log(1 + eta);
    const double nln2 = n_o * LN2;
    const double ls0 = -p->psi0 - u * p->n;
    double lell = -p->psi0 + p->n * log((1 + exp(-u)) / 2);
    const double theta_z = p->oracle == 0 ? 1.0 : 0.0;
    const int m_empty = (int)floor(n_o - l1me / LN2 + 1e-12) + 1;
    const double l_e_lam_m1 = log(expm1(lam)), l_1_m_e = log(-expm1(-lam));
    double lA = -INFINITY;
    for (int i = 0; i < natoms; i++) lA = (i == 0) ? lw[i] + lpr[i] : logaddexp(lA, lw[i] + lpr[i]);

    for (int i = 0; i < R_COUNT; i++) res[i] = 0.0;
    res[R_LA] = lA;
    res[R_RCLOSE] = -2;
    res[R_LM_LAST] = -INFINITY;
    res[R_LL] = -INFINITY;
    res[R_LU] = INFINITY;
    res[R_MIN_POP_RADIUS] = INFINITY;
    res[R_SLACK_VALID_LOWER] = res[R_SLACK_VALID_UPPER] = res[R_SLACK_WIDTH] = -INFINITY;
    res[R_MARGIN_III] = INFINITY;
    res[R_SLACK_V] = res[R_SLACK_VI] = -INFINITY;
    res[R_LCOST] = INFINITY;

    int status = ST_ABORT_LEVELS, j_stop = J, npop = 0, nneg = 0, r_close = -2;
    double lsum = -INFINITY, lU_acc = ls0, lM_last = -INFINITY, lL = -INFINITY, lU = INFINITY, min_pop_radius = INFINITY;
    int idx = 0; /* number of atoms with lw <= threshold (thresholds increase with j) */
    for (int j = 0; j <= J; j++) {
        const double lsj = ls0 + lam * j;
        const double thr = lsj - b * theta_z;
        while (idx < natoms && lw[idx] <= thr + p->tie) idx++;
        const double lph = ltail_ge[idx];
        double mpop;
        if (lph >= 0.0) mpop = 0.0; else mpop = ceil(-lph / LN2 - 1e-12); /* +inf if lph = -inf */
        const double lell_in = lell;
        const double lMneg = lnu + lsj - lell_in - b;
        lMneg_rec[j] = lMneg;
        double m_neg = ceil((lMneg - lK) / LN2 - 1e-12);
        if (m_neg < 0) m_neg = 0;
        double m_close = m_empty;
        int r_ok = upper_bound(lE, n_o, lth + b + lell_in - lsj + nln2 + TOL) - 1;
        if (r_ok >= 0) {
            double m2 = ceil((nln2 - l1me - lball[r_ok]) / LN2 - 1e-12);
            if (m2 < 0) m2 = 0;
            if (m2 < m_close) m_close = m2;
        }
        double m_end = mpop;
        if (m_neg < m_end) m_end = m_neg;
        if (m_close < m_end) m_end = m_close;
        if (m_end > p->m_max && p->enforce_abort) {
            status = ST_ABORT_SAMPLE;
            j_stop = j;
            lM[j] = lK + p->m_max * LN2;
            kind[j] = NEG;
            lq_rec[j] = NAN;
            break;
        }
        const double lMj = lK + m_end * LN2;
        lM[j] = lMj;
        if (mpop == m_end) { /* populated at this pass */
            const double lpbar = lph - l1pe;
            if (lsj - b + lpbar > lell) lell = lsj - b + lpbar;
            if (p->harper) {
                int k = kball(lball, n_o, nln2 + lpbar);
                double h = lsj - b - nln2 + lT[k];
                if (h > lell) lell = h;
            }
            double lq = lph - l1me;
            if (lq > 0.0) lq = 0.0;
            int r;
            double ltail;
            if (nln2 + lq < 0.0) { r = -1; ltail = -INFINITY; }
            else {
                r = radius(lball, n_o, lq);
                ltail = (r <= n_o - 1) ? lsj - nln2 + lE[r] : INFINITY;
            }
            lq_rec[j] = lq;
            const double new_sum = logaddexp(lsum, l_1_m_e - b + lsj + lpbar);
            if (ltail <= lth + b + lell) {
                status = ST_CLOSED_POP; r_close = r; lM_last = lMj;
                lL = lell > new_sum ? lell : new_sum;
                lU = logaddexp(lU_acc, ltail);
                kind[j] = STOP_POP;
                j_stop = j;
                break;
            }
            lsum = new_sum;
            lU_acc = logaddexp(lU_acc, l_e_lam_m1 + lsj + lq);
            kind[j] = POP;
            npop++;
            if (r < min_pop_radius) min_pop_radius = r;
        } else if (m_close == m_end) { /* closure at an unpopulated pass */
            double lq = -l1me - m_end * LN2;
            if (lq > 0.0) lq = 0.0;
            int r;
            double ltail;
            if (nln2 + lq < 0.0) { r = -1; ltail = -INFINITY; }
            else {
                r = radius(lball, n_o, lq);
                ltail = (r <= n_o - 1) ? lsj - nln2 + lE[r] : INFINITY;
            }
            lq_rec[j] = lq;
            status = ST_CLOSED_UNPOP; r_close = r; lM_last = lMj;
            lL = lell > lsum ? lell : lsum;
            lU = logaddexp(lU_acc, ltail);
            kind[j] = STOP_UNPOP;
            j_stop = j;
            break;
        } else { /* left as negligible */
            double lq = -l1me - m_end * LN2;
            if (lq > 0.0) lq = 0.0;
            lq_rec[j] = lq;
            lU_acc = logaddexp(lU_acc, l_e_lam_m1 + lsj + lq);
            kind[j] = NEG;
            nneg++;
        }
    }
    double lM_max = -INFINITY;
    for (int j = 0; j <= j_stop; j++) if (lM[j] > lM_max) lM_max = lM[j];

    res[R_STATUS] = status; res[R_JSTOP] = j_stop; res[R_RCLOSE] = r_close; res[R_LM_LAST] = lM_last;
    res[R_LM_MAX] = lM_max; res[R_LL] = lL; res[R_LU] = lU; res[R_NPOP] = npop; res[R_NNEG] = nneg;
    res[R_MIN_POP_RADIUS] = min_pop_radius;

    /* ---- claims --------------------------------------------------------------------------- */
    if (status == ST_CLOSED_POP || status == ST_CLOSED_UNPOP) {
        res[R_SLACK_VALID_LOWER] = lL - lA;
        res[R_SLACK_VALID_UPPER] = lA - lU;
        res[R_SLACK_WIDTH] = (lU - lL) - p->x_out;
    }
    double margin_iii = INFINITY, s_iv_M = -INFINITY, s_iv_Mneg = -INFINITY;
    for (int j = 0; j <= j_stop; j++) {
        if (kind[j] <= NEG) {
            double mg = lq_rec[j] - p->lpi_dag;
            if (mg < margin_iii) margin_iii = mg;      /* NaN (abort level) never compares below */
        }
        double cap = LN2 + lMneg_rec[j];
        if (lK > cap) cap = lK;
        if (lM[j] - cap > s_iv_M) s_iv_M = lM[j] - cap;
        if (lMneg_rec[j] > s_iv_Mneg) s_iv_Mneg = lMneg_rec[j];
    }
    res[R_MARGIN_III] = margin_iii;
    res[R_SLACK_IV_M] = s_iv_M;
    res[R_SLACK_IV_MNEG] = s_iv_Mneg - p->lMneg_cap;
    res[R_SLACK_IV_MBAR] = lM_max - p->lM_bar;
    {
        /* claim (v) at every x of the ladder (rungs 0..L-1) and of the extra grid; claim (vi) on the ladder */
        double s_v = -INFINITY, s_vi = -INFINITY;
        int nx = (n_i > 0 ? L : 0) + n_grid;
        for (int t = 0; t < nx; t++) {
            int on_ladder = (n_i > 0 && t < L);
            double x = on_ladder ? xs[t] : grid[t - (n_i > 0 ? L : 0)];
            if (!(x > 0)) continue;
            int id = 0;
            double best_v = -INFINITY, best_vi = -INFINITY;
            for (int j = 0; j <= j_stop; j++) {
                double th = ls0 + lam * j - x;
                while (id < natoms && lw[id] <= th + p->tie) id++;
                double lp = ltail_ge[id];
                if (lMneg_rec[j] + lp > best_v) best_v = lMneg_rec[j] + lp;
                if (lM[j] + lp > best_vi) best_vi = lM[j] + lp;
            }
            if (best_v - (p->lcount_factor + x) > s_v) s_v = best_v - (p->lcount_factor + x);
            if (n_i > 0) {
                double lcnt = p->lcnt_const + x;
                if (lK > lcnt) lcnt = lK;
                if (best_vi - lcnt > s_vi) s_vi = best_vi - lcnt;
            }
        }
        res[R_SLACK_V] = s_v;
        res[R_SLACK_VI] = s_vi;
    }

    /* ---- evaluations ---------------------------------------------------------------------- */
    if (n_i > 0) {
        const double x0 = xs[0], t0 = p->t0;
        int *dq = (int *)malloc(sizeof(int) * (size_t)(j_stop + 2));
        if (!dq) return 1;
        double lcost = logaddexp(0.0, lM_max);
        lcalls[0] = -INFINITY;
        for (int l = 0; l < L; l++) {
            double alpha, beta;
            if (l == 0) { alpha = t0; beta = x0 - t0; }
            else if (p->oracle == 0) { alpha = 0.0; beta = xs[l] < x0 - t0 ? xs[l] : x0 - t0; }
            else { alpha = xs[l] < t0 ? xs[l] : t0; beta = 0.0; }
            /* sliding-window maximum of lM over [lo(w), hi(w)], both nondecreasing in the atom index */
            int head = 0, tail = 0, next = 0;
            double acc = -INFINITY;
            for (int i = 0; i < natoms; i++) {
                double flo = ceil((lw[i] + b - alpha - ls0) / lam - 1e-12);
                double fhi = ceil((lw[i] + beta - ls0) / lam - 1e-12) - 1;
                if (flo < 0) flo = 0;
                if (fhi > j_stop) fhi = j_stop;
                if (fhi < flo) continue;
                int lo = (int)flo, hi = (int)fhi;
                if (next < lo) { next = lo; head = tail = 0; }
                while (next <= hi) {
                    while (tail > head && lM[dq[tail - 1]] <= lM[next]) tail--;
                    dq[tail++] = next;
                    next++;
                }
                while (tail > head && dq[head] < lo) head++;
                if (tail > head) {
                    double v = lpr[i] + lM[dq[head]];
                    acc = isinf(acc) ? v : logaddexp(acc, v);
                }
            }
            lcalls[l + 1] = acc;
            if (!isinf(acc)) lcost = logaddexp(lcost, acc + lC[l + 1]);
        }
        free(dq);
        res[R_LCOST] = lcost;
    }
    return 0;
}
