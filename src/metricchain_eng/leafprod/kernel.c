/*
 * kernel.c -- integer kernels of the producer of "shares at the leaves" certificates.
 *
 * Nothing in this file decides whether a certificate is valid: that is the checker's job
 * (src/metricchain_eng/leafcert).  The kernels propose integer messages and evaluate them exactly.
 *
 * MODEL.  n sites, site i with the states 0..k_i-1; integer tables H_i(a); a list of edges e = (u, v),
 * u < v, with integer tables J_e(a, b) (a state of u, b state of v; row-major).  Pairs that are not edges
 * have the zero table and carry zero messages; they never appear here.  The messages of edge e are stored
 * in one vector of length k_u + k_v at offset moff[e]: first m_uv(a), a = 0..k_u-1, then m_vu(b).
 *
 * BOX.  dlen[i] >= 1 is the number of allowed states of site i, listed in dom[koff[i] .. koff[i]+dlen[i]-1].
 *
 * DUAL VALUE of messages m on a box D (what lp_eval returns):
 *
 *     sum_i  min_{a in D_i} [ H_i(a) + sum_{e at i} m_i,e(a) ]
 *   + sum_e  min_{a in D_u, b in D_v} [ J_e(a, b) - m_uv(a) - m_vu(b) ] .
 *
 * It is a lower bound of the energy on D for ANY integers m (every message occurs once with each sign).
 *
 * ASCENT (lp_ascent).  Block-coordinate ascent on that value in integer arithmetic.  Sites with one allowed
 * state are folded into their neighbours once.  The other ("free") sites are ordered breadth first; a
 * sweep is a forward and a backward pass over that order.  Processing a site i:
 *   pull   for every edge to a free site j:  m_ij(a) := min_{b in D_j} [ J(a, b) - m_ji(b) ]   (a in D_i),
 *          after which every such pair has minimum 0 for each a; this maximises the dual value over the
 *          messages of site i;
 *   push   with v = min_a theta_i(a), theta_i(a) = H_i(a) + sum_e m_i,e(a), the excess theta_i(a) - v >= 0
 *          is handed back to the edges towards the sites that come later in the pass, in integer shares
 *          that sum to at most the excess.  The term of site i keeps the minimum >= v and the pairs
 *          receive non-negative amounts, so the dual value does not decrease.
 * Hence the value is non-decreasing from pass to pass (given the fold), it is an integer bounded by the
 * minimum of the energy, and the iteration stops when it reaches `target`, stalls, or hits max_sweeps.
 * On a forest the backward pass is exact dynamic programming (every site has one later neighbour, its
 * breadth-first parent, and hands it its whole excess): one sweep gives the exact minimum.
 *
 * All arithmetic is int64.  The caller guarantees magnitudes far from overflow (model.py bounds the tables
 * by the degree of the graph and checks the messages after every call); compile with -fwrapv so that an
 * overflow, should the guard ever be wrong, yields a wrong proposal (which the checker rejects) and not
 * undefined behaviour.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef int64_t i64;

typedef struct {
    i64 n, ne, S, M;
    const i64 *k;        /* n: number of states                                   */
    const i64 *koff;     /* n+1: offsets of the sites in H and dom                */
    const i64 *H;        /* S                                                      */
    const i64 *eu, *ev;  /* ne: endpoints, eu[e] < ev[e]                           */
    const i64 *joff;     /* ne+1: offsets of the tables in J                       */
    const i64 *J;
    const i64 *moff;     /* ne+1: offsets of the message vectors                   */
    const i64 *aoff;     /* n+1: incident edges of site i are aedge[aoff[i]..aoff[i+1]-1] */
    const i64 *aedge;    /* 2 ne                                                   */
} lp_model;

size_t lp_model_size(void) { return sizeof(lp_model); }

/* Exact dual value of the messages m on the box; U[i], P[e] its terms; arg[i] a minimising state of the
 * term of site i (the first one), if arg is not NULL. */
i64 lp_eval(const lp_model *M, const i64 *dlen, const i64 *dom, const i64 *m, i64 *U, i64 *P, i64 *arg)
{
    i64 total = 0;
    for (i64 i = 0; i < M->n; i++) {
        i64 best = INT64_MAX, barg = -1;
        const i64 *d = dom + M->koff[i];
        for (i64 t = 0; t < dlen[i]; t++) {
            i64 a = d[t];
            i64 v = M->H[M->koff[i] + a];
            for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
                i64 e = M->aedge[q];
                v += (M->eu[e] == i) ? m[M->moff[e] + a] : m[M->moff[e] + M->k[M->eu[e]] + a];
            }
            if (v < best) { best = v; barg = a; }
        }
        U[i] = best;
        if (arg) arg[i] = barg;
        total += best;
    }
    for (i64 e = 0; e < M->ne; e++) {
        i64 u = M->eu[e], v = M->ev[e], ku = M->k[u], kv = M->k[v];
        const i64 *Je = M->J + M->joff[e], *mu = m + M->moff[e], *mv = mu + ku;
        const i64 *du = dom + M->koff[u], *dv = dom + M->koff[v];
        i64 best = INT64_MAX;
        for (i64 s = 0; s < dlen[u]; s++) {
            i64 a = du[s], ma = mu[a];
            const i64 *row = Je + a * kv;
            for (i64 t = 0; t < dlen[v]; t++) {
                i64 b = dv[t], val = row[b] - ma - mv[b];
                if (val < best) best = val;
            }
        }
        P[e] = best;
        total += best;
    }
    return total;
}

/* pull at site i over edge e (other endpoint j, restricted to its box): for every state a listed in
 * (alist, alen), m_i,e(a) := min_{b in D_j} [ J(a, b) - m_j,e(b) ]; the new values are added to acc[a]. */
static void pull_edge(const lp_model *M, const i64 *dlen, const i64 *dom, i64 *m, i64 i, i64 e,
                      const i64 *alist, i64 alen, i64 *acc)
{
    i64 u = M->eu[e], v = M->ev[e], ku = M->k[u], kv = M->k[v];
    const i64 *Je = M->J + M->joff[e];
    i64 *mu = m + M->moff[e], *mv = mu + ku;
    if (i == u) {
        const i64 *dv = dom + M->koff[v];
        i64 nv = dlen[v];
        for (i64 s = 0; s < alen; s++) {
            i64 a = alist ? alist[s] : s;
            const i64 *row = Je + a * kv;
            i64 best = INT64_MAX;
            for (i64 t = 0; t < nv; t++) {
                i64 b = dv[t], val = row[b] - mv[b];
                if (val < best) best = val;
            }
            mu[a] = best;
            acc[a] += best;
        }
    } else {
        const i64 *du = dom + M->koff[u];
        i64 nu = dlen[u];
        for (i64 s = 0; s < alen; s++) {
            i64 b = alist ? alist[s] : s;
            i64 best = INT64_MAX;
            for (i64 t = 0; t < nu; t++) {
                i64 a = du[t], val = Je[a * kv + b] - mu[a];
                if (val < best) best = val;
            }
            mv[b] = best;
            acc[b] += best;
        }
    }
}

/* Pull at site i for EVERY state of its alphabet (the neighbours restricted to their boxes); theta[a]
 * receives H_i(a) + sum_e m_i,e(a).  Used to extend a leaf certificate to other states of site i. */
void lp_pull_site(const lp_model *M, const i64 *dlen, const i64 *dom, i64 *m, i64 i, i64 *theta)
{
    i64 ki = M->k[i];
    for (i64 a = 0; a < ki; a++) theta[a] = M->H[M->koff[i] + a];
    for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++)
        pull_edge(M, dlen, dom, m, i, M->aedge[q], NULL, ki, theta);
}

/* For every site i and every state a of its alphabet: c[koff[i]+a] = H_i(a) + sum_{e at i} min_{b in D_j}
 * [ J(a, b) - m_j,e(b) ], the term of site i after a pull, without changing the messages. */
void lp_probe_all(const lp_model *M, const i64 *dlen, const i64 *dom, const i64 *m, i64 *c)
{
    for (i64 x = 0; x < M->S; x++) c[x] = M->H[x];
    for (i64 e = 0; e < M->ne; e++) {
        i64 u = M->eu[e], v = M->ev[e], ku = M->k[u], kv = M->k[v];
        const i64 *Je = M->J + M->joff[e], *mu = m + M->moff[e], *mv = mu + ku;
        const i64 *du = dom + M->koff[u], *dv = dom + M->koff[v];
        i64 nu = dlen[u], nv = dlen[v];
        i64 *cu = c + M->koff[u], *cv = c + M->koff[v];
        for (i64 a = 0; a < ku; a++) {
            const i64 *row = Je + a * kv;
            i64 best = INT64_MAX;
            for (i64 t = 0; t < nv; t++) {
                i64 b = dv[t], val = row[b] - mv[b];
                if (val < best) best = val;
            }
            cu[a] += best;
        }
        for (i64 b = 0; b < kv; b++) {
            i64 best = INT64_MAX;
            for (i64 t = 0; t < nu; t++) {
                i64 a = du[t], val = Je[a * kv + b] - mu[a];
                if (val < best) best = val;
            }
            cv[b] += best;
        }
    }
}

/* Block-coordinate ascent (see the header).  m is updated in place.  Returns the dual value computed by
 * the passes (equal to lp_eval of the result; the caller re-evaluates).  info[0] = sweeps performed,
 * info[1] = 1 if the target was reached, info[2] = number of free sites, info[3] = value after the fold
 * and the first forward pass, info[4] = passes performed.  Returns INT64_MIN if no pass was made
 * (max_sweeps <= 0 with a free site: only the fold is applied) or if memory is exhausted (info[0] = -1).
 * wmode 0: the whole excess is pushed (shares differ by at most one unit); wmode 1: shares
 * floor(excess / max(n_in, n_out)), the rest stays at the site. */
i64 lp_ascent(const lp_model *M, const i64 *dlen, const i64 *dom, i64 *m, i64 target, i64 max_sweeps,
              i64 patience, i64 wmode, i64 *info)
{
    i64 n = M->n, ne = M->ne;
    i64 *order = malloc((size_t)(4 * n + 2) * sizeof *order);
    i64 *fedge = malloc((size_t)(2 * ne + 1) * sizeof *fedge);
    i64 *base = malloc((size_t)(2 * M->S + 1) * sizeof *base);
    if (!order || !fedge || !base) { free(order); free(fedge); free(base); info[0] = -1; return INT64_MIN; }
    i64 *pos = order + n, *foff = order + 2 * n, *theta = base + M->S;
    i64 cfixed = 0, nfree = 0;

    for (i64 i = 0; i < n; i++) pos[i] = (dlen[i] > 1) ? -2 : -1;     /* -2 free and not yet ordered; -1 fixed */
    /* fold the edges with exactly one fixed endpoint into the free endpoint */
    for (i64 e = 0; e < ne; e++) {
        i64 u = M->eu[e], v = M->ev[e], ku = M->k[u], kv = M->k[v];
        const i64 *Je = M->J + M->joff[e];
        i64 *mu = m + M->moff[e], *mv = mu + ku;
        if (pos[u] == -1 && pos[v] != -1) {
            i64 a = dom[M->koff[u]], ma = mu[a];
            const i64 *dv = dom + M->koff[v];
            for (i64 t = 0; t < dlen[v]; t++) { i64 b = dv[t]; mv[b] = Je[a * kv + b] - ma; }
        } else if (pos[u] != -1 && pos[v] == -1) {
            i64 b = dom[M->koff[v]], mb = mv[b];
            const i64 *du = dom + M->koff[u];
            for (i64 s = 0; s < dlen[u]; s++) { i64 a = du[s]; mu[a] = Je[a * kv + b] - mb; }
        } else if (pos[u] == -1 && pos[v] == -1) {
            i64 a = dom[M->koff[u]], b = dom[M->koff[v]];
            cfixed += Je[a * kv + b] - mu[a] - mv[b];
        }
    }
    /* terms of the fixed sites; base of the free sites; free-free adjacency */
    i64 nf = 0;
    for (i64 i = 0; i < n; i++) {
        foff[i] = nf;
        const i64 *d = dom + M->koff[i];
        if (pos[i] == -1) {
            i64 a = d[0], v = M->H[M->koff[i] + a];
            for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
                i64 e = M->aedge[q];
                v += (M->eu[e] == i) ? m[M->moff[e] + a] : m[M->moff[e] + M->k[M->eu[e]] + a];
            }
            cfixed += v;
            continue;
        }
        for (i64 t = 0; t < dlen[i]; t++) base[M->koff[i] + d[t]] = M->H[M->koff[i] + d[t]];
        for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
            i64 e = M->aedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
            if (pos[j] == -1) {
                const i64 *mi = (M->eu[e] == i) ? m + M->moff[e] : m + M->moff[e] + M->k[M->eu[e]];
                for (i64 t = 0; t < dlen[i]; t++) base[M->koff[i] + d[t]] += mi[d[t]];
            } else {
                fedge[nf++] = e;
            }
        }
    }
    foff[n] = nf;
    /* breadth-first order of the free sites */
    for (i64 s = 0; s < n; s++) {
        if (pos[s] != -2) continue;
        pos[s] = nfree; order[nfree++] = s;
        for (i64 h = pos[s]; h < nfree; h++) {
            i64 i = order[h];
            for (i64 q = foff[i]; q < foff[i + 1]; q++) {
                i64 e = fedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
                if (pos[j] == -2) { pos[j] = nfree; order[nfree++] = j; }
            }
        }
    }

    i64 best = INT64_MIN, stall = 0, sweeps = 0, passes = 0, value = INT64_MIN, reached = 0, first = INT64_MIN;
    if (nfree == 0) {                       /* every site is fixed: the value is a constant */
        value = first = cfixed;
        reached = value >= target;
        max_sweeps = 0;
    }
    while (sweeps < max_sweeps && !reached) {
        for (int dir = 0; dir < 2 && !reached; dir++) {
            value = cfixed;
            for (i64 h = 0; h < nfree; h++) {
                i64 i = order[dir == 0 ? h : nfree - 1 - h];
                const i64 *d = dom + M->koff[i];
                i64 nd = dlen[i];
                for (i64 t = 0; t < nd; t++) theta[d[t]] = base[M->koff[i] + d[t]];
                i64 nout = 0, nin = 0;
                for (i64 q = foff[i]; q < foff[i + 1]; q++) {
                    i64 e = fedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
                    pull_edge(M, dlen, dom, m, i, e, d, nd, theta);
                    if ((dir == 0) == (pos[j] > pos[i])) nout++; else nin++;
                }
                i64 v = INT64_MAX;
                for (i64 t = 0; t < nd; t++) if (theta[d[t]] < v) v = theta[d[t]];
                i64 keep = 0;
                if (nout > 0) {
                    i64 W = (wmode == 1 && nin > nout) ? nin : nout;
                    keep = INT64_MAX;
                    for (i64 t = 0; t < nd; t++) {
                        i64 a = d[t], ex = theta[a] - v, share = ex / W, rem = ex - share * W, o = 0;
                        i64 rot = (wmode == 1) ? 0 : (a + passes) % nout;
                        for (i64 q = foff[i]; q < foff[i + 1]; q++) {
                            i64 e = fedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
                            if ((dir == 0) != (pos[j] > pos[i])) continue;
                            i64 give = share;
                            if (wmode != 1) {
                                i64 slot = o + rot; if (slot >= nout) slot -= nout;
                                if (slot < rem) give++;
                            }
                            o++;
                            if (M->eu[e] == i) m[M->moff[e] + a] -= give;
                            else m[M->moff[e] + M->k[M->eu[e]] + a] -= give;
                        }
                        i64 left = (wmode == 1) ? ex - share * nout : 0;
                        if (left < keep) keep = left;
                    }
                }
                value += v + keep;
            }
            passes++;
            if (first == INT64_MIN) first = value;
            if (value >= target) reached = 1;
        }
        sweeps++;
        if (value > best) { best = value; stall = 0; } else if (++stall >= patience) break;
    }
    info[0] = sweeps; info[1] = reached; info[2] = nfree; info[3] = first; info[4] = passes;
    free(order); free(fedge); free(base);
    return value;
}

/* Sequential decoding of messages into a state x of the box.  Fixed sites keep their state; the free sites
 * are visited in the breadth-first order of lp_ascent, and each takes a state (the first) of least
 *     H_i(a) + sum_{j already assigned} J(a, x_j) + sum_{j not yet assigned} m_i,e(a) .
 * After a sweep of lp_ascent (which ends with the backward pass) the messages point towards the start of
 * the order, and on a forest this returns a minimiser of the energy on the box.
 * work: at least 2 n integers.  Returns 0, or -1 if memory is exhausted. */
int lp_decode(const lp_model *M, const i64 *dlen, const i64 *dom, const i64 *m, i64 *x, i64 *work)
{
    i64 n = M->n, nfree = 0;
    i64 *order = work, *pos = work + n;
    for (i64 i = 0; i < n; i++) {
        pos[i] = (dlen[i] > 1) ? -2 : -1;
        if (pos[i] == -1) x[i] = dom[M->koff[i]];
    }
    for (i64 s = 0; s < n; s++) {
        if (pos[s] != -2) continue;
        pos[s] = nfree; order[nfree++] = s;
        for (i64 h = pos[s]; h < nfree; h++) {
            i64 i = order[h];
            for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
                i64 e = M->aedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
                if (pos[j] == -2) { pos[j] = nfree; order[nfree++] = j; }
            }
        }
    }
    for (i64 h = 0; h < nfree; h++) {
        i64 i = order[h], best = INT64_MAX, barg = -1;
        const i64 *d = dom + M->koff[i];
        for (i64 t = 0; t < dlen[i]; t++) {
            i64 a = d[t], cost = M->H[M->koff[i] + a];
            for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
                i64 e = M->aedge[q], u = M->eu[e], v = M->ev[e], j = (u == i) ? v : u;
                if (pos[j] == -1 || pos[j] < h) {          /* fixed, or decoded before */
                    cost += (u == i) ? M->J[M->joff[e] + a * M->k[v] + x[j]] : M->J[M->joff[e] + x[j] * M->k[v] + a];
                } else {
                    cost += (u == i) ? m[M->moff[e] + a] : m[M->moff[e] + M->k[u] + a];
                }
            }
            if (cost < best) { best = cost; barg = a; }
        }
        x[i] = barg;
    }
    return 0;
}

/* The 2-core of the graph of free sites (sites with more than one allowed state, edges between two of
 * them): deg[i] = number of neighbours of i inside the core if i belongs to it, else 0.  Outside the core
 * the free sites hang on trees, where the relaxation loses nothing.  work: at least 2 n integers. */
void lp_core(const lp_model *M, const i64 *dlen, i64 *deg, i64 *work)
{
    i64 n = M->n, top = 0;
    i64 *stack = work, *alive = work + n;
    for (i64 i = 0; i < n; i++) { deg[i] = 0; alive[i] = dlen[i] > 1; }
    for (i64 e = 0; e < M->ne; e++)
        if (alive[M->eu[e]] && alive[M->ev[e]]) { deg[M->eu[e]]++; deg[M->ev[e]]++; }
    for (i64 i = 0; i < n; i++)
        if (alive[i] && deg[i] <= 1) { alive[i] = 0; stack[top++] = i; }
    while (top) {
        i64 i = stack[--top];
        for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
            i64 e = M->aedge[q], j = (M->eu[e] == i) ? M->ev[e] : M->eu[e];
            if (alive[j] && --deg[j] <= 1) { alive[j] = 0; stack[top++] = j; }
        }
    }
    for (i64 i = 0; i < n; i++) if (!alive[i]) deg[i] = 0;
}

/* Energy of the state x. */
i64 lp_energy(const lp_model *M, const i64 *x)
{
    i64 total = 0;
    for (i64 i = 0; i < M->n; i++) total += M->H[M->koff[i] + x[i]];
    for (i64 e = 0; e < M->ne; e++) total += M->J[M->joff[e] + x[M->eu[e]] * M->k[M->ev[e]] + x[M->ev[e]]];
    return total;
}

/* Iterated conditional modes from x (updated in place): every site in turn takes a state of least energy
 * given the others (the current one on ties), restricted to the box if dlen is not NULL; stops when a
 * sweep changes nothing or after max_sweeps.  Returns the energy.  work: at least max_i k_i integers. */
i64 lp_icm(const lp_model *M, const i64 *dlen, const i64 *dom, i64 *x, i64 max_sweeps, i64 *work)
{
    for (i64 sweep = 0; sweep < max_sweeps; sweep++) {
        int changed = 0;
        for (i64 i = 0; i < M->n; i++) {
            i64 ki = M->k[i];
            if (dlen && dlen[i] == 1) continue;
            for (i64 a = 0; a < ki; a++) work[a] = M->H[M->koff[i] + a];
            for (i64 q = M->aoff[i]; q < M->aoff[i + 1]; q++) {
                i64 e = M->aedge[q], kv = M->k[M->ev[e]];
                const i64 *Je = M->J + M->joff[e];
                if (M->eu[e] == i) { const i64 *row = Je + 0; i64 b = x[M->ev[e]]; for (i64 a = 0; a < ki; a++) work[a] += row[a * kv + b]; }
                else { const i64 *row = Je + x[M->eu[e]] * kv; for (i64 a = 0; a < ki; a++) work[a] += row[a]; }
            }
            i64 cur = x[i], bestv = work[cur], besta = cur;
            if (dlen) {
                const i64 *d = dom + M->koff[i];
                for (i64 t = 0; t < dlen[i]; t++) if (work[d[t]] < bestv) { bestv = work[d[t]]; besta = d[t]; }
            } else {
                for (i64 a = 0; a < ki; a++) if (work[a] < bestv) { bestv = work[a]; besta = a; }
            }
            if (besta != cur) { x[i] = besta; changed = 1; }
        }
        if (!changed) break;
    }
    return lp_energy(M, x);
}
