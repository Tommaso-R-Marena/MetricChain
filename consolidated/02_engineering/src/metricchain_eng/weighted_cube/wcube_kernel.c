/* wcube_kernel.c -- exact vertex enumeration of the Lipschitz polytope of a weighted cube, by orbits,
 * and floating-point scans of the vertex set (request R10-E1 of the science division).
 *
 * The polytope:  P(w) = { phi : {0,1}^L -> R,  |phi(x) - phi(x ^ e_i)| <= w_i for every x and i } / constants,
 * with positive INTEGER weights w_i.  The constraint matrix is the incidence matrix of the cube graph (totally
 * unimodular), so every vertex is an integer vector once phi(0) = 0, and all arithmetic here is in machine
 * integers (int32, range checked): the enumeration is exact.
 *
 * Facts used (proved in the docstring of polytope.py):
 *  (V)  phi in P(w) is a vertex  <=>  the graph of tight edges (|difference| = w_i) is connected.
 *  (E)  Orient every tight edge from its lower to its higher end (an acyclic digraph).  The edges of P(w) that
 *       leave the vertex phi are exactly the directions -1_U, U a proper non-empty subset of the nodes such that
 *       no tight arc leaves U (an "up-set") and both U and its complement are connected in the tight graph.
 *       Along such an edge phi' = phi - s 1_U with  s = min over cube edges {x not in U, y in U} of
 *       phi(y) - phi(x) + w_e  (> 0), and phi' is the adjacent vertex.
 *  (C)  The graph of a polytope is connected.  Hence a set of vertices that contains one vertex and is closed
 *       under (E) is the whole vertex set.
 *
 * Symmetry: coordinate permutations that preserve the weights (table supplied by the caller), the 2^L
 * translations x -> x ^ t, and phi -> -phi.  wc_enumerate() runs a breadth-first search over ORBITS: every
 * vertex is replaced by the canonical member of its orbit (the lexicographically least image whose value at
 * node 0 is its minimum, shifted to 0), all neighbours (E) of every canonical member are generated, and the
 * search stops when no new orbit appears.  Closure under (E) of the union of the orbits follows because the
 * group maps neighbours to neighbours.
 *
 * Nothing here is taken from the code of the other divisions.
 */
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define WC_MAXL 5
#define WC_MAXN 32
#define WC_MAXPERM 120
#define WC_RANGE (1 << 29)   /* |values| must stay below this (checked) */
#define WC_MAXW (1 << 20)    /* largest admissible weight */

typedef struct {
    int L, n, nperm;
    int w[WC_MAXL];
    uint8_t perm[WC_MAXPERM][WC_MAXN];
    uint32_t full;
} wc_geom;

/* ------------------------------------------------------------------ storage of the orbit representatives */
static int32_t *g_reps = NULL;  /* nrep x n, canonical members */
static int32_t *g_stab = NULL;  /* order of the stabiliser */
static int32_t *g_deg = NULL;   /* number of polytope edges at the representative (-1: not processed) */
static int64_t g_nrep = 0, g_cap = 0;
static int64_t *g_table = NULL; /* open addressing, entries are indices + 1 */
static int64_t g_tcap = 0;
static int g_error = 0;         /* 1: value range exceeded, 2: out of memory, 3: internal inconsistency */

void wc_free(void) {
    free(g_reps); free(g_stab); free(g_deg); free(g_table);
    g_reps = NULL; g_stab = NULL; g_deg = NULL; g_table = NULL;
    g_nrep = 0; g_cap = 0; g_tcap = 0; g_error = 0;
}

static uint64_t hash_key(const int32_t *k, int n) {
    uint64_t h = 0x243F6A8885A308D3ULL;
    for (int i = 0; i < n; i++) {
        h ^= (uint64_t)(uint32_t)k[i];
        h *= 0x9E3779B97F4A7C15ULL;
        h ^= h >> 29;
    }
    return h;
}

static int table_grow(int n) {
    int64_t ncap = g_tcap ? 2 * g_tcap : (1 << 12);
    int64_t *nt = (int64_t *)calloc((size_t)ncap, sizeof(int64_t));
    if (!nt) return 0;
    for (int64_t i = 0; i < g_nrep; i++) {
        uint64_t h = hash_key(g_reps + i * n, n) & (uint64_t)(ncap - 1);
        while (nt[h]) h = (h + 1) & (uint64_t)(ncap - 1);
        nt[h] = i + 1;
    }
    free(g_table);
    g_table = nt;
    g_tcap = ncap;
    return 1;
}

/* returns the index of the key, inserting it if absent; *isnew tells which; -1 on memory failure */
static int64_t table_find_or_insert(const int32_t *key, int n, int stab, int *isnew) {
    if (2 * (g_nrep + 1) > g_tcap && !table_grow(n)) { g_error = 2; return -1; }
    uint64_t h = hash_key(key, n) & (uint64_t)(g_tcap - 1);
    while (g_table[h]) {
        int64_t idx = g_table[h] - 1;
        if (memcmp(g_reps + idx * n, key, (size_t)n * sizeof(int32_t)) == 0) { *isnew = 0; return idx; }
        h = (h + 1) & (uint64_t)(g_tcap - 1);
    }
    if (g_nrep == g_cap) {
        int64_t ncap = g_cap ? 2 * g_cap : 1024;
        int32_t *r = (int32_t *)realloc(g_reps, (size_t)ncap * (size_t)n * sizeof(int32_t));
        if (!r) { g_error = 2; return -1; }
        g_reps = r;
        int32_t *s = (int32_t *)realloc(g_stab, (size_t)ncap * sizeof(int32_t));
        if (!s) { g_error = 2; return -1; }
        g_stab = s;
        int32_t *d = (int32_t *)realloc(g_deg, (size_t)ncap * sizeof(int32_t));
        if (!d) { g_error = 2; return -1; }
        g_deg = d;
        g_cap = ncap;
    }
    memcpy(g_reps + g_nrep * n, key, (size_t)n * sizeof(int32_t));
    g_stab[g_nrep] = stab;
    g_deg[g_nrep] = -1;
    g_table[h] = g_nrep + 1;
    *isnew = 1;
    return g_nrep++;
}

/* ------------------------------------------------------------------ canonical member of an orbit
 * Candidates: the images  x -> eps * N[perm_k(x) ^ t]  whose value at node 0 is the minimum of the image,
 * i.e. (eps = +) N[t] = min N, (eps = -) N[t] = max N; each shifted so that the value at node 0 is 0.
 * The canonical member is the lexicographically least candidate; the number of candidates equal to it is the
 * order of the stabiliser (the group elements carrying phi to one given member of its orbit form a coset). */
static void canonical(const wc_geom *G, const int32_t *N, int32_t *out, int *stab) {
    int n = G->n;
    int32_t mn = N[0], mx = N[0];
    for (int v = 1; v < n; v++) {
        if (N[v] < mn) mn = N[v];
        if (N[v] > mx) mx = N[v];
    }
    int have = 0, count = 0;
    for (int eps = 0; eps < 2; eps++) {
        int32_t ref = eps ? mx : mn;
        for (int t = 0; t < n; t++) {
            if (N[t] != ref) continue;
            for (int k = 0; k < G->nperm; k++) {
                const uint8_t *pm = G->perm[k];
                int x = 0, cmp = 0;
                if (have) {
                    for (; x < n; x++) {
                        int32_t v = eps ? ref - N[pm[x] ^ t] : N[pm[x] ^ t] - ref;
                        if (v != out[x]) { cmp = (v < out[x]) ? -1 : 1; break; }
                    }
                    if (cmp == 0) { count++; continue; }
                    if (cmp > 0) continue;
                }
                for (; x < n; x++) out[x] = eps ? ref - N[pm[x] ^ t] : N[pm[x] ^ t] - ref;
                have = 1;
                count = 1;
            }
        }
    }
    *stab = count;
}

/* ------------------------------------------------------------------ the edges of the polytope at a vertex */
typedef struct {
    const wc_geom *G;
    int32_t N[WC_MAXN];
    uint32_t up[WC_MAXN], dn[WC_MAXN], adj[WC_MAXN], upcl[WC_MAXN], dncl[WC_MAXN];
    int64_t deg;
    int64_t max_reps;
    int stop;
    int connected;
} wc_vertex;

static inline int ctz32(uint32_t x) { return __builtin_ctz(x); }

static uint32_t component(const wc_vertex *V, uint32_t seed, uint32_t allowed) {
    uint32_t comp = seed, frontier = seed;
    while (frontier) {
        int v = ctz32(frontier);
        frontier &= frontier - 1;
        uint32_t nw = V->adj[v] & allowed & ~comp;
        comp |= nw;
        frontier |= nw;
    }
    return comp;
}

static uint32_t succ_of(const wc_vertex *V, uint32_t D) {
    uint32_t s = 0;
    while (D) { int v = ctz32(D); D &= D - 1; s |= V->up[v]; }
    return s;
}

static uint32_t pred_of(const wc_vertex *V, uint32_t U) {
    uint32_t s = 0;
    while (U) { int v = ctz32(U); U &= U - 1; s |= V->dn[v]; }
    return s;
}

static void build_dag(wc_vertex *V) {
    const wc_geom *G = V->G;
    int n = G->n, L = G->L;
    for (int v = 0; v < n; v++) { V->up[v] = 0; V->dn[v] = 0; }
    for (int x = 0; x < n; x++)
        for (int i = 0; i < L; i++) {
            if ((x >> i) & 1) continue;
            int y = x | (1 << i);
            int32_t d = V->N[y] - V->N[x];
            if (d == G->w[i]) { V->up[x] |= 1u << y; V->dn[y] |= 1u << x; }
            else if (d == -G->w[i]) { V->up[y] |= 1u << x; V->dn[x] |= 1u << y; }
        }
    int order[WC_MAXN];
    for (int v = 0; v < n; v++) order[v] = v;
    for (int a = 1; a < n; a++) { /* insertion sort by value */
        int v = order[a], b = a - 1;
        while (b >= 0 && V->N[order[b]] > V->N[v]) { order[b + 1] = order[b]; b--; }
        order[b + 1] = v;
    }
    for (int a = 0; a < n; a++) {
        int v = order[a];
        uint32_t m = 1u << v, d = V->dn[v];
        while (d) { int z = ctz32(d); d &= d - 1; m |= V->dncl[z]; }
        V->dncl[v] = m;
    }
    for (int a = n - 1; a >= 0; a--) {
        int v = order[a];
        uint32_t m = 1u << v, u = V->up[v];
        while (u) { int z = ctz32(u); u &= u - 1; m |= V->upcl[z]; }
        V->upcl[v] = m;
    }
    for (int v = 0; v < n; v++) V->adj[v] = V->up[v] | V->dn[v];
    V->connected = (component(V, 1u, G->full) == G->full);
}

/* one edge of the polytope: U is the up-set that is lowered */
static void emit(wc_vertex *V, uint32_t U) {
    const wc_geom *G = V->G;
    int n = G->n, L = G->L;
    V->deg++;
    int32_t s = INT32_MAX;
    uint32_t D = G->full & ~U;
    while (D) {
        int x = ctz32(D);
        D &= D - 1;
        for (int i = 0; i < L; i++) {
            int y = x ^ (1 << i);
            if ((U >> y) & 1) {
                int32_t c = V->N[y] - V->N[x] + G->w[i];
                if (c < s) s = c;
            }
        }
    }
    if (s <= 0 || s == INT32_MAX) { g_error = 3; V->stop = 1; return; }
    int32_t N2[WC_MAXN], key[WC_MAXN];
    for (int v = 0; v < n; v++) {
        N2[v] = V->N[v] - (((U >> v) & 1) ? s : 0);
        if (N2[v] > WC_RANGE || N2[v] < -WC_RANGE) { g_error = 1; V->stop = 1; return; }
    }
    int stab, isnew;
    canonical(G, N2, key, &stab);
    if (table_find_or_insert(key, n, stab, &isnew) < 0) { V->stop = 1; return; }
    if (g_nrep > V->max_reps) V->stop = 1;
}

/* Enumeration of the pairs (D, U): D a connected down-set, U = complement connected.
 * recD: the fixed source s1 lies in D.  State: D (connected down-set containing s1), F (nodes forced into U,
 * an up-set disjoint from D).  Invariant: if F is non-empty, the complement of D is connected.
 * Branch on a successor y of D outside D and F: either y joins U (F grows by the up-closure of y) or y joins D
 * (D grows by the down-closure of y).  Whenever F is non-empty the components of the complement of D that do
 * not contain F must be absorbed into D (they cannot belong to a connected U); if F meets two components the
 * branch is empty.  Every surviving state contains at least one solution (exclude all remaining candidates),
 * so the work is proportional to the output. */
static void recD(wc_vertex *V, uint32_t D, uint32_t F) {
    if (V->stop) return;
    uint32_t full = V->G->full;
    uint32_t front = succ_of(V, D) & ~D & ~F;
    if (!front) {
        if (F) emit(V, full & ~D);
        return;
    }
    int y = ctz32(front);
    uint32_t F2 = F | V->upcl[y];
    if (F) recD(V, D, F2);
    else {
        uint32_t K = component(V, 1u << y, full & ~D);
        recD(V, full & ~K, F2);
    }
    uint32_t D2 = D | V->dncl[y];
    if (F) {
        uint32_t K = component(V, F & (0u - F), full & ~D2);
        if (F & ~K) return;
        recD(V, full & ~K, F);
    } else recD(V, D2, 0);
}

/* recU: the fixed source s1 lies in U (mirror image of recD: U grows by predecessors, F is forced into D). */
static void recU(wc_vertex *V, uint32_t U, uint32_t F) {
    if (V->stop) return;
    uint32_t full = V->G->full;
    uint32_t front = pred_of(V, U) & ~U & ~F;
    if (!front) {
        if (F) emit(V, U);
        return;
    }
    int y = ctz32(front);
    uint32_t F2 = F | V->dncl[y];
    if (F) recU(V, U, F2);
    else {
        uint32_t K = component(V, 1u << y, full & ~U);
        recU(V, full & ~K, F2);
    }
    uint32_t U2 = U | V->upcl[y];
    if (F) {
        uint32_t K = component(V, F & (0u - F), full & ~U2);
        if (F & ~K) return;
        recU(V, full & ~K, F);
    } else recU(V, U2, 0);
}

static int set_geom(wc_geom *G, int L, const int32_t *w, int nperm, const uint8_t *perm) {
    if (L < 1 || L > WC_MAXL || nperm < 1 || nperm > WC_MAXPERM) return 0;
    G->L = L;
    G->n = 1 << L;
    G->nperm = nperm;
    G->full = (G->n == 32) ? 0xFFFFFFFFu : ((1u << G->n) - 1u);
    for (int i = 0; i < L; i++) {
        if (w[i] <= 0 || w[i] > WC_MAXW) return 0;
        G->w[i] = w[i];
    }
    for (int k = 0; k < nperm; k++)
        for (int x = 0; x < G->n; x++) {
            if (perm[k * G->n + x] >= G->n) return 0;
            G->perm[k][x] = perm[k * G->n + x];
        }
    return 1;
}

/* Breadth-first search over orbits, started at the additive vertex phi(x) = sum_i w_i x_i.
 * Returns the number of orbit representatives found (all processed iff *status == 0).
 * status: 0 complete; 1 stopped because more than max_reps orbits were found; 2 stopped because the orbits
 * found so far contain more than max_vertices vertices; 3 value range exceeded; 4 out of memory;
 * 5 internal inconsistency (a representative with a disconnected tight graph, or a non-positive step);
 * 6 bad arguments.  The results stay in static storage until wc_free(). */
int64_t wc_enumerate(int L, const int32_t *w, int nperm, const uint8_t *perm, int64_t max_reps,
                     int64_t max_vertices, int64_t *n_processed, int64_t *total_vertices, int64_t *total_degree,
                     int *status) {
    wc_geom G;
    wc_free();
    if (!set_geom(&G, L, w, nperm, perm)) { *status = 6; return 0; }
    int n = G.n;
    int64_t ngroup = 2LL * nperm * n;
    int32_t start[WC_MAXN], key[WC_MAXN];
    for (int x = 0; x < n; x++) {
        start[x] = 0;
        for (int i = 0; i < L; i++)
            if ((x >> i) & 1) start[x] += G.w[i];
    }
    int stab, isnew;
    canonical(&G, start, key, &stab);
    if (table_find_or_insert(key, n, stab, &isnew) < 0) { *status = 4; return 0; }
    int64_t tv = ngroup / stab, td = 0, counted = 1, i = 0;
    *status = 0;
    for (; i < g_nrep; i++) {
        wc_vertex V;
        V.G = &G;
        memcpy(V.N, g_reps + i * n, (size_t)n * sizeof(int32_t));
        V.deg = 0;
        V.max_reps = max_reps;
        V.stop = 0;
        build_dag(&V);
        if (!V.connected) { g_error = 3; break; }
        int s1 = 0;
        while (V.dn[s1]) s1++;
        recD(&V, V.dncl[s1], 0);
        recU(&V, V.upcl[s1], 0);
        if (g_error) break;
        for (; counted < g_nrep; counted++) tv += ngroup / g_stab[counted];
        if (V.stop) { *status = 1; break; }
        g_deg[i] = (int32_t)V.deg;
        td += V.deg;
        if (tv > max_vertices) { *status = 2; i++; break; }
    }
    for (; counted < g_nrep; counted++) tv += ngroup / g_stab[counted];
    if (g_error == 1) *status = 3;
    else if (g_error == 2) *status = 4;
    else if (g_error == 3) *status = 5;
    *n_processed = i;
    *total_vertices = tv;
    *total_degree = td;
    return g_nrep;
}

void wc_fetch(int n, int32_t *reps, int32_t *stab, int32_t *deg) {
    memcpy(reps, g_reps, (size_t)g_nrep * (size_t)n * sizeof(int32_t));
    memcpy(stab, g_stab, (size_t)g_nrep * sizeof(int32_t));
    memcpy(deg, g_deg, (size_t)g_nrep * sizeof(int32_t));
}

/* The neighbours (E) of ONE vertex, not reduced by symmetry (used by the tests and by the closure check):
 * writes up to max_out neighbours (each normalised to value 0 at node 0) and returns their number, or -1 if
 * the tight graph of N is not connected, -2 on bad arguments. */
typedef struct { int32_t *out; int64_t max_out, count; int n; } wc_sink;
static wc_sink *g_sink = NULL;

static void emit_plain(wc_vertex *V, uint32_t U) {
    const wc_geom *G = V->G;
    int n = G->n, L = G->L;
    int32_t s = INT32_MAX;
    uint32_t D = G->full & ~U;
    while (D) {
        int x = ctz32(D);
        D &= D - 1;
        for (int i = 0; i < L; i++) {
            int y = x ^ (1 << i);
            if ((U >> y) & 1) {
                int32_t c = V->N[y] - V->N[x] + G->w[i];
                if (c < s) s = c;
            }
        }
    }
    if (g_sink->count < g_sink->max_out) {
        int32_t *o = g_sink->out + g_sink->count * n;
        int32_t c0 = V->N[0] - ((U & 1u) ? s : 0);
        for (int v = 0; v < n; v++) o[v] = V->N[v] - (((U >> v) & 1) ? s : 0) - c0;
    }
    g_sink->count++;
}

static void recD_plain(wc_vertex *V, uint32_t D, uint32_t F) {
    uint32_t full = V->G->full;
    uint32_t front = succ_of(V, D) & ~D & ~F;
    if (!front) {
        if (F) emit_plain(V, full & ~D);
        return;
    }
    int y = ctz32(front);
    uint32_t F2 = F | V->upcl[y];
    if (F) recD_plain(V, D, F2);
    else {
        uint32_t K = component(V, 1u << y, full & ~D);
        recD_plain(V, full & ~K, F2);
    }
    uint32_t D2 = D | V->dncl[y];
    if (F) {
        uint32_t K = component(V, F & (0u - F), full & ~D2);
        if (F & ~K) return;
        recD_plain(V, full & ~K, F);
    } else recD_plain(V, D2, 0);
}

static void recU_plain(wc_vertex *V, uint32_t U, uint32_t F) {
    uint32_t full = V->G->full;
    uint32_t front = pred_of(V, U) & ~U & ~F;
    if (!front) {
        if (F) emit_plain(V, U);
        return;
    }
    int y = ctz32(front);
    uint32_t F2 = F | V->dncl[y];
    if (F) recU_plain(V, U, F2);
    else {
        uint32_t K = component(V, 1u << y, full & ~U);
        recU_plain(V, full & ~K, F2);
    }
    uint32_t U2 = U | V->upcl[y];
    if (F) {
        uint32_t K = component(V, F & (0u - F), full & ~U2);
        if (F & ~K) return;
        recU_plain(V, full & ~K, F);
    } else recU_plain(V, U2, 0);
}

int64_t wc_neighbours(int L, const int32_t *w, const int32_t *N, int32_t *out, int64_t max_out) {
    wc_geom G;
    uint8_t id[WC_MAXN];
    for (int x = 0; x < WC_MAXN; x++) id[x] = (uint8_t)x;
    if (!set_geom(&G, L, w, 1, id)) return -2;
    wc_vertex V;
    V.G = &G;
    memcpy(V.N, N, (size_t)G.n * sizeof(int32_t));
    V.deg = 0;
    V.stop = 0;
    V.max_reps = 0;
    build_dag(&V);
    if (!V.connected) return -1;
    wc_sink sink = {out, max_out, 0, G.n};
    g_sink = &sink;
    int s1 = 0;
    while (V.dn[s1]) s1++;
    recD_plain(&V, V.dncl[s1], 0);
    recU_plain(&V, V.upcl[s1], 0);
    g_sink = NULL;
    return sink.count;
}

/* Canonical member and stabiliser order of one vertex (exposed for the tests). */
int wc_canonical(int L, const int32_t *w, int nperm, const uint8_t *perm, const int32_t *N, int32_t *out) {
    wc_geom G;
    int stab;
    if (!set_geom(&G, L, w, nperm, perm)) return -1;
    canonical(&G, N, out, &stab);
    return stab;
}

/* ------------------------------------------------------------------ floating-point scans of all vertices
 * A vertex in a chamber is phi = u A + us B with integer arrays A, B (see the report); only one member per
 * orbit is stored.  The scans run over all images  x -> eps * (A, B)[perm_k(x) ^ t]  of all stored members
 * (duplicates when the stabiliser is not trivial are harmless).  Image index: g = (eps * n + t) * nperm + k.
 *
 * Gibbs law of an image: weights W(x) = pi(x) exp(-phi(x)), Z = sum W.
 *   KL(pi_phi || Q) = (1/Z) sum_x W(x) [ln pi(x) - phi(x) - ln Q(x)] - ln Z,
 *   c_t(phi)        = sum_x pi_phi(x)^t Q_t(x)^(1-t) = Z^(-t) sum_x [pi(x)^t Q_t(x)^(1-t)] exp(-t phi(x)).
 */
typedef struct { double val; int64_t rep; int32_t g; } wc_top;

typedef struct {
    int n, nperm;
    const uint8_t *perm;
    const int8_t *A, *B;
} wc_images;

/* are the images g1 and g2 of the stored member r the same vertex (modulo constants)? */
static int same_image(const wc_images *I, int64_t r, int32_t g1, int32_t g2) {
    int n = I->n;
    const int8_t *a = I->A + r * n, *b = I->B + r * n;
    const uint8_t *p1 = I->perm + (size_t)(g1 % I->nperm) * n, *p2 = I->perm + (size_t)(g2 % I->nperm) * n;
    int t1 = (g1 / I->nperm) % n, t2 = (g2 / I->nperm) % n;
    int e1 = (g1 / (I->nperm * n)) ? -1 : 1, e2 = (g2 / (I->nperm * n)) ? -1 : 1;
    int a1 = e1 * a[p1[0] ^ t1], b1 = e1 * b[p1[0] ^ t1], a2 = e2 * a[p2[0] ^ t2], b2 = e2 * b[p2[0] ^ t2];
    for (int x = 1; x < n; x++) {
        if (e1 * a[p1[x] ^ t1] - a1 != e2 * a[p2[x] ^ t2] - a2) return 0;
        if (e1 * b[p1[x] ^ t1] - b1 != e2 * b[p2[x] ^ t2] - b2) return 0;
    }
    return 1;
}

/* keeps the K largest values, sorted in decreasing order; an image that is the same vertex as an entry
 * already present (possible when the stabiliser of the stored member is not trivial) is not inserted twice.
 * The test compares the IMAGES themselves; the values only select which entries are compared (two images of
 * the same vertex have values that agree up to rounding). */
static void top_insert(wc_top *top, int K, int *ntop, double val, int64_t rep, int32_t g, const wc_images *I) {
    int pos = *ntop;
    if (pos == K && val <= top[K - 1].val) return;
    double tol = 1e-9 * (fabs(val) > 1.0 ? fabs(val) : 1.0);
    for (int i = 0; i < *ntop; i++) {
        if (top[i].val < val - tol) break;
        if (top[i].val <= val + tol && top[i].rep == rep && same_image(I, rep, top[i].g, g)) return;
    }
    if (pos == K) pos = K - 1;
    else (*ntop)++;
    while (pos > 0 && top[pos - 1].val < val) { top[pos] = top[pos - 1]; pos--; }
    top[pos].val = val;
    top[pos].rep = rep;
    top[pos].g = g;
}

/* Scan for the capacity problem.  Outputs: the K largest values of KL(pi_phi || Q) with their (rep, g),
 * the number of images above thr, and the number of images scanned.  Returns the number of top entries. */
int wc_scan_kl(int L, int nperm, const uint8_t *perm, int64_t nrep, const int8_t *A, const int8_t *B,
               const double *logpi, double u, double us, const double *lnQ, int K, double *top_val,
               int64_t *top_rep, int32_t *top_g, double thr, int64_t *n_above, int64_t *n_scanned) {
    int n = 1 << L;
    if (L < 1 || L > WC_MAXL || nperm < 1 || nperm > WC_MAXPERM || K < 1) return -1;
    wc_top *top = (wc_top *)malloc((size_t)K * sizeof(wc_top));
    if (!top) return -1;
    wc_images I = {n, nperm, perm, A, B};
    int ntop = 0;
    int64_t above = 0, scanned = 0;
    double pi[WC_MAXN], l0[WC_MAXN];
    for (int x = 0; x < n; x++) { pi[x] = exp(logpi[x]); l0[x] = logpi[x] - lnQ[x]; }
    for (int64_t r = 0; r < nrep; r++) {
        const int8_t *a = A + r * n, *b = B + r * n;
        double E[WC_MAXN], ep[WC_MAXN], em[WC_MAXN];
        double emin = 0.0, emax = 0.0;
        for (int v = 0; v < n; v++) {
            E[v] = u * a[v] + us * b[v];
            if (v == 0 || E[v] < emin) emin = E[v];
            if (v == 0 || E[v] > emax) emax = E[v];
        }
        for (int v = 0; v < n; v++) {
            ep[v] = exp(-(E[v] - emin)); /* eps = +1: phi = E - emin >= 0 */
            em[v] = exp(E[v] - emax);    /* eps = -1: phi = emax - E >= 0 */
        }
        for (int eps = 0; eps < 2; eps++) {
            const double *ee = eps ? em : ep;
            for (int t = 0; t < n; t++)
                for (int k = 0; k < nperm; k++) {
                    const uint8_t *pm = perm + (size_t)k * n;
                    double Z = 0.0, S = 0.0;
                    for (int x = 0; x < n; x++) {
                        int v = pm[x] ^ t;
                        double wgt = pi[x] * ee[v];
                        double phi = eps ? emax - E[v] : E[v] - emin;
                        Z += wgt;
                        S += wgt * (l0[x] - phi);
                    }
                    double kl = S / Z - log(Z);
                    scanned++;
                    if (kl > thr) above++;
                    top_insert(top, K, &ntop, kl, r, (int32_t)((eps * n + t) * nperm + k), &I);
                }
        }
    }
    for (int i = 0; i < ntop; i++) { top_val[i] = top[i].val; top_rep[i] = top[i].rep; top_g[i] = top[i].g; }
    free(top);
    *n_above = above;
    *n_scanned = scanned;
    return ntop;
}

/* Scan for the Renyi problem at T orders t_j with centres Q_j:  for every j the K SMALLEST values of
 * c_{t_j}(phi) (i.e. the K largest values of -ln c) with their (rep, g).
 * pq: T x n, pq[j][x] = pi(x)^{t_j} Q_j(x)^{1 - t_j}.  Outputs top_val (T x K, values of -ln c, decreasing),
 * top_rep, top_g, ntop (T).  Returns 0, or -1 on bad arguments. */
int wc_scan_renyi(int L, int nperm, const uint8_t *perm, int64_t nrep, const int8_t *A, const int8_t *B,
                  const double *logpi, double u, double us, int T, const double *ts, const double *pq, int K,
                  double *top_val, int64_t *top_rep, int32_t *top_g, int32_t *ntop_out) {
    int n = 1 << L;
    if (L < 1 || L > WC_MAXL || nperm < 1 || nperm > WC_MAXPERM || K < 1 || T < 1 || T > 64) return -1;
    wc_top *top = (wc_top *)malloc((size_t)K * (size_t)T * sizeof(wc_top));
    double *et = (double *)malloc((size_t)T * 2 * WC_MAXN * sizeof(double));
    if (!top || !et) { free(top); free(et); return -1; }
    wc_images I = {n, nperm, perm, A, B};
    int ntop[64];
    for (int j = 0; j < T; j++) ntop[j] = 0;
    double pi[WC_MAXN];
    for (int x = 0; x < n; x++) pi[x] = exp(logpi[x]);
    for (int64_t r = 0; r < nrep; r++) {
        const int8_t *a = A + r * n, *b = B + r * n;
        double E[WC_MAXN], ep[WC_MAXN], em[WC_MAXN];
        double emin = 0.0, emax = 0.0;
        for (int v = 0; v < n; v++) {
            E[v] = u * a[v] + us * b[v];
            if (v == 0 || E[v] < emin) emin = E[v];
            if (v == 0 || E[v] > emax) emax = E[v];
        }
        for (int v = 0; v < n; v++) {
            ep[v] = exp(-(E[v] - emin));
            em[v] = exp(E[v] - emax);
        }
        for (int j = 0; j < T; j++)
            for (int v = 0; v < n; v++) {
                et[(2 * j) * WC_MAXN + v] = exp(-ts[j] * (E[v] - emin));
                et[(2 * j + 1) * WC_MAXN + v] = exp(ts[j] * (E[v] - emax));
            }
        for (int eps = 0; eps < 2; eps++) {
            const double *ee = eps ? em : ep;
            for (int t = 0; t < n; t++)
                for (int k = 0; k < nperm; k++) {
                    const uint8_t *pm = perm + (size_t)k * n;
                    uint8_t idx[WC_MAXN];
                    double Z = 0.0;
                    for (int x = 0; x < n; x++) {
                        idx[x] = (uint8_t)(pm[x] ^ t);
                        Z += pi[x] * ee[idx[x]];
                    }
                    double lz = log(Z);
                    int32_t g = (int32_t)((eps * n + t) * nperm + k);
                    for (int j = 0; j < T; j++) {
                        const double *e2 = et + (size_t)(2 * j + eps) * WC_MAXN;
                        const double *q = pq + (size_t)j * n;
                        double s = 0.0;
                        for (int x = 0; x < n; x++) s += q[x] * e2[idx[x]];
                        double val = ts[j] * lz - log(s); /* -ln c_t */
                        top_insert(top + (size_t)j * K, K, &ntop[j], val, r, g, &I);
                    }
                }
        }
    }
    for (int j = 0; j < T; j++) {
        ntop_out[j] = ntop[j];
        for (int i = 0; i < ntop[j]; i++) {
            top_val[(size_t)j * K + i] = top[(size_t)j * K + i].val;
            top_rep[(size_t)j * K + i] = top[(size_t)j * K + i].rep;
            top_g[(size_t)j * K + i] = top[(size_t)j * K + i].g;
        }
    }
    free(top);
    free(et);
    return 0;
}
