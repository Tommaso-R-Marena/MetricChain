/* v9_cobound.c -- independent verifier V9 for "Theorem R9.1" (SCI-REV-0009 section 4).
 *
 * Written from the Setting paragraph of THEORY_REPORT 11.22 and the definitions of R9_REPORT 4.1.
 * No source code of the reviewed division was read before this file was written.
 *
 * Lattice: A sites = integer points with all coordinates even and x+y+z = 0 mod 4; B = A + (1,1,1).
 * Bonds out of an A site: +a_i, out of a B site: -a_i, a0=(1,1,1), a1=(1,-1,-1), a2=(-1,1,-1), a3=(-1,-1,1).
 * Height = coordinate y.  Walk: injective sequence of sites, consecutive ones bonded.
 * h_d = #{p<q : q-p >= 3, |x_q-x_p|^2 = d}, d = 3, 8, 11;  g = #{i : |x_{i+3}-x_i|^2 = 11}.
 * Bridge: first bead strictly lowest, last bead (weakly) highest.
 *
 * Definitions of R9 (for a bridge x with n beads, u1 = x1-x0, u2 = x2-x1, b = last bond, b' = bond before):
 *   admissible c1: c1 = b' if b' is an up-bond, otherwise either up-bond out of the last bead;
 *   t1 = last + c1, t2 = t1 + b, t3 = t2 + c1 (beads n, n+1, n+2);  s1 = x0 - u2, s2 = s1 - u1, s3 = s2 - u2 (beads -1,-2,-3);
 *   A(x,c1) = (#pairs (t_j, x_p) at chain separation >= 3 with squared distance 3, 8, 11 ; [b' is a down-bond]);
 *   B(x)    = (the same for (s_j, x_p) ; 0);   clean: b' up, A(x,b') = 0, B(x) = 0;
 *   x1 o x2 = x1, t1, t2, t3, phi(x2), phi the height-preserving symmetry with phi(x2_0) = t3 + b, (u1,u2) of x2 -> (c1, b).
 *
 * Everything is counted from coordinates by O(n^2) double loops over pairs of beads (no neighbour tables, no hashing).
 *
 * Mutation switches (compile with -DMUT=k; every one of them must make mode "pairs" report failures):
 *   1  first line of (a) tested without B(x2)          2  B(x1 o x2) compared with B(x2)
 *   3  A(x1 o x2, .) compared with A(x1, c1)          4  A counts pairs at chain separation >= 4 only
 *   5  B counts pairs at chain separation >= 2        6  c1 taken as the OTHER up-bond when b' is an up-bond
 *
 * usage:  v9_cobound pairs  NMAX [full] [threads]     all ordered pairs with N1, N2 <= NMAX
 *         v9_cobound pairs2 N1MAX N2MAX SKIP [threads [N1MIN N2MIN]]
 *                                                     all ordered pairs with N1MIN <= N1 <= N1MAX, N2MIN <= N2 <= N2MAX, except those with both <= SKIP
 *         v9_cobound single NMAX NVAR [threads] [dumpN] every (bridge, c1) with N <= NMAX; head/tail variants for N <= NVAR;
 *                                                     dumpN: write all bridges with N <= dumpN to stdout lines "D ..."
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#ifndef MUT
#define MUT 0
#endif

#define MAXB 72   /* largest number of beads of any walk built here */
#define MAXS 26   /* largest number of beads of an enumerated bridge */

static const int AV[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};

static long long g_fail = 0;

static inline int is_site(const int *p){
    int ex = p[0] & 1, ey = p[1] & 1, ez = p[2] & 1;
    int s = p[0] + p[1] + p[2];
    if (!ex && !ey && !ez) return (s & 3) == 0;
    if (ex && ey && ez) return ((s - 3) & 3) == 0;
    return 0;
}
static inline int is_A(const int *p){ return (p[0] & 1) == 0; }
static inline int sq(const int *a, const int *b){
    int x = a[0]-b[0], y = a[1]-b[1], z = a[2]-b[2];
    return x*x + y*y + z*z;
}
static inline void bonds_out(const int *p, int out[4][3]){
    int s = is_A(p) ? 1 : -1;
    for (int i = 0; i < 4; i++) for (int k = 0; k < 3; k++) out[i][k] = s*AV[i][k];
}

static void print_walk(FILE *f, int (*w)[3], int n){
    for (int i = 0; i < n; i++) fprintf(f, "(%d,%d,%d)%s", w[i][0], w[i][1], w[i][2], i+1 < n ? " " : "");
}

/* walk test + profile, one pass.  returns 0 if w is a self-avoiding lattice walk (then hg is filled), else an error code */
#ifndef REF
/* branch-free inner loop on separate coordinate arrays (the compiler vectorises it); compile with -DREF for the plain version below */
static int walk_hg(int (*w)[3], int n, int hg[4]){
    int X[MAXB], Y[MAXB], Z[MAXB];
    hg[0] = hg[1] = hg[2] = hg[3] = 0;
    for (int i = 0; i < n; i++){ if (!is_site(w[i])) return 1; X[i] = w[i][0]; Y[i] = w[i][1]; Z[i] = w[i][2]; }
    for (int i = 0; i+1 < n; i++) if (sq(w[i], w[i+1]) != 3) return 2;
    for (int i = 0; i+2 < n; i++) if (sq(w[i], w[i+2]) != 8) return 3;      /* 0 would be an immediate reversal */
    int c3 = 0, c8 = 0, c11 = 0, cb = 0;
    for (int i = 0; i < n; i++){
        int xi = X[i], yi = Y[i], zi = Z[i];
        for (int j = i+3; j < n; j++){
            int dx = X[j]-xi, dy = Y[j]-yi, dz = Z[j]-zi;
            int d = dx*dx + dy*dy + dz*dz;
            c3 += (d == 3); c8 += (d == 8); c11 += (d == 11); cb += (d < 12);
        }
    }
    if (cb != c3 + c8 + c11) return 4;                                       /* a pair at squared distance 0 (not injective) or at an impossible one */
    hg[0] = c3; hg[1] = c8; hg[2] = c11;
    for (int i = 0; i+3 < n; i++){
        int d = sq(w[i], w[i+3]);
        if (d == 11) hg[3]++;
        else if (d != 19) return 5;
    }
    return 0;
}
#else
static int walk_hg(int (*w)[3], int n, int hg[4]){
    hg[0] = hg[1] = hg[2] = hg[3] = 0;
    for (int i = 0; i < n; i++) if (!is_site(w[i])) return 1;
    for (int i = 0; i+1 < n; i++) if (sq(w[i], w[i+1]) != 3) return 2;
    for (int i = 0; i+2 < n; i++) if (sq(w[i], w[i+2]) != 8) return 3;      /* 0 would be an immediate reversal */
    for (int i = 0; i < n; i++)
        for (int j = i+3; j < n; j++){
            int d = sq(w[i], w[j]);
            if (d < 12){
                if (d == 3) hg[0]++;
                else if (d == 8) hg[1]++;
                else if (d == 11) hg[2]++;
                else return 4;                                               /* 0: not injective; other values impossible */
            }
        }
    for (int i = 0; i+3 < n; i++){
        int d = sq(w[i], w[i+3]);
        if (d == 11) hg[3]++;
        else if (d != 19) return 5;
    }
    return 0;
}
#endif
static int is_bridge(int (*w)[3], int n){
    for (int i = 1; i < n; i++) if (w[i][1] <= w[0][1]) return 0;
    for (int i = 0; i < n; i++) if (w[i][1] > w[n-1][1]) return 0;
    return 1;
}
/* admissible first linker bonds */
static int admissible(int (*w)[3], int n, int c[2][3]){
    int bp[3];
    for (int k = 0; k < 3; k++) bp[k] = w[n-2][k] - w[n-3][k];
    int out[4][3], m = 0;
    bonds_out(w[n-1], out);
#if MUT == 6
    if (bp[1] == 1){
        for (int i = 0; i < 4; i++) if (out[i][1] == 1 && !(out[i][0] == bp[0] && out[i][2] == bp[2])) for (int k = 0; k < 3; k++) c[0][k] = out[i][k];
        return 1;
    }
#else
    if (bp[1] == 1){ for (int k = 0; k < 3; k++) c[0][k] = bp[k]; return 1; }
#endif
    for (int i = 0; i < 4; i++) if (out[i][1] == 1){ if (m < 2) for (int k = 0; k < 3; k++) c[m][k] = out[i][k]; m++; }
    return m;   /* must be 2 */
}
static void A_of(int (*w)[3], int n, const int *c1, int A[4]){
    int b[3], t[3][3];
    for (int k = 0; k < 3; k++){
        b[k] = w[n-1][k] - w[n-2][k];
        t[0][k] = w[n-1][k] + c1[k];
        t[1][k] = t[0][k] + b[k];
        t[2][k] = t[1][k] + c1[k];
    }
    A[0] = A[1] = A[2] = 0;
    for (int j = 0; j < 3; j++)                 /* t_{j+1} is bead n + j */
        for (int q = 0; q < n; q++){
#if MUT == 4
            if ((n + j) - q < 4) continue;
#else
            if ((n + j) - q < 3) continue;
#endif
            int d = sq(t[j], w[q]);
            if (d == 3) A[0]++; else if (d == 8) A[1]++; else if (d == 11) A[2]++;
        }
    A[3] = (w[n-2][1] - w[n-3][1] == -1);
}
static void B_of(int (*w)[3], int n, int B[4]){
    int u1[3], u2[3], s[3][3];
    for (int k = 0; k < 3; k++){
        u1[k] = w[1][k] - w[0][k];
        u2[k] = w[2][k] - w[1][k];
        s[0][k] = w[0][k] - u2[k];
        s[1][k] = s[0][k] - u1[k];
        s[2][k] = s[1][k] - u2[k];
    }
    B[0] = B[1] = B[2] = B[3] = 0;
    for (int j = 0; j < 3; j++)                 /* s_{j+1} is bead -(j+1) */
        for (int q = 0; q < n; q++){
#if MUT == 5
            if (q + (j + 1) < 2) continue;
#else
            if (q + (j + 1) < 3) continue;
#endif
            int d = sq(s[j], w[q]);
            if (d == 3) B[0]++; else if (d == 8) B[1]++; else if (d == 11) B[2]++;
        }
}
static int is_clean(int (*w)[3], int n){
    int bp[3], A[4], B[4];
    for (int k = 0; k < 3; k++) bp[k] = w[n-2][k] - w[n-3][k];
    if (bp[1] != 1) return 0;
    A_of(w, n, bp, A);
    B_of(w, n, B);
    return !(A[0] | A[1] | A[2] | A[3] | B[0] | B[1] | B[2] | B[3]);
}
/* out = (s_k, ..., s_1, w, t_1, ..., t_m): zigzag head of k beads and zigzag tail of m beads */
static int extend(int (*w)[3], int n, const int *c1, int k, int m, int (*out)[3]){
    int u1[3], u2[3], b[3], cur[3];
    for (int i = 0; i < 3; i++){ u1[i] = w[1][i]-w[0][i]; u2[i] = w[2][i]-w[1][i]; b[i] = w[n-1][i]-w[n-2][i]; cur[i] = w[0][i]; }
    for (int j = 1; j <= k; j++){
        for (int i = 0; i < 3; i++){ cur[i] -= (j & 1) ? u2[i] : u1[i]; out[k-j][i] = cur[i]; }
    }
    for (int q = 0; q < n; q++) for (int i = 0; i < 3; i++) out[k+q][i] = w[q][i];
    for (int i = 0; i < 3; i++) cur[i] = w[n-1][i];
    for (int j = 1; j <= m; j++){
        for (int i = 0; i < 3; i++){ cur[i] += (j & 1) ? c1[i] : b[i]; out[k+n+j-1][i] = cur[i]; }
    }
    return k + n + m;
}
/* the 8 signed permutations with g(e_y) = e_y */
static inline void gmap(int gi, const int *v, int *out){
    int sx = (gi & 1) ? -1 : 1, sz = (gi & 2) ? -1 : 1;
    if (gi & 4){ out[0] = sx*v[2]; out[1] = v[1]; out[2] = sz*v[0]; }
    else       { out[0] = sx*v[0]; out[1] = v[1]; out[2] = sz*v[2]; }
}
static inline int cnorm4(const int *d){   /* norm of a vector with nonnegative entries: 9 d3 + 4 d8 + d11 + dg */
    return 9*d[0] + 4*d[1] + d[2] + d[3];
}

/* ------------------------------------------------------------------ enumeration */
#define G 64
#define OFF 32
#define IDX(p) ((((p)[0]+OFF) << 12) | (((p)[1]+OFF) << 6) | ((p)[2]+OFF))

typedef void (*cb_t)(int (*w)[3], int n, void *ctx);

typedef struct { int w[MAXS][3]; unsigned char *occ; int N; int y0; cb_t cb; void *ctx; } Enum;

static void dfs(Enum *e, int depth, int ymax){
    if (depth == e->N){
        if (e->w[depth-1][1] >= ymax) e->cb(e->w, e->N, e->ctx);
        return;
    }
    int out[4][3];
    bonds_out(e->w[depth-1], out);
    int r = e->N - (depth + 1);
    for (int i = 0; i < 4; i++){
        int q[3];
        for (int k = 0; k < 3; k++) q[k] = e->w[depth-1][k] + out[i][k];
        if (q[1] <= e->y0) continue;
        int ym = ymax > q[1] ? ymax : q[1];
        if (q[1] + r < ym) continue;
        int ix = IDX(q);
        if (e->occ[ix]) continue;
        e->occ[ix] = 1;
        for (int k = 0; k < 3; k++) e->w[depth][k] = q[k];
        dfs(e, depth + 1, ym);
        e->occ[ix] = 0;
    }
}

/* prefixes (all walks with pd beads from the given start, first bead strictly lowest, optional fixed first two bonds) */
typedef struct { int n; int w[MAXS][3]; } Prefix;
typedef struct { Prefix *a; long long n, cap; } PrefList;
static void cb_prefix(int (*w)[3], int n, void *ctx){
    PrefList *L = (PrefList *)ctx;
    if (L->n == L->cap){ L->cap = L->cap ? 2*L->cap : 1024; L->a = realloc(L->a, L->cap*sizeof(Prefix)); }
    L->a[L->n].n = n;
    memcpy(L->a[L->n].w, w, n*sizeof(int[3]));
    L->n++;
}
/* enumerate all prefixes with pd beads: like dfs but without the final-height condition and pruning */
static void dfs_prefix(Enum *e, int depth, int pd, PrefList *L, int reduced){
    if (depth == pd){ cb_prefix(e->w, pd, L); return; }
    int out[4][3];
    bonds_out(e->w[depth-1], out);
    for (int i = 0; i < 4; i++){
        int q[3];
        for (int k = 0; k < 3; k++) q[k] = e->w[depth-1][k] + out[i][k];
        if (q[1] <= e->y0) continue;
        if (reduced && depth == 1 && !(out[i][0] == 1 && out[i][1] == 1 && out[i][2] == 1)) continue;     /* u1 = a0 */
        if (reduced && depth == 2 && !(out[i][0] == -1 && out[i][1] == 1 && out[i][2] == 1)) continue;    /* u2 = -a1 */
        int ix = IDX(q);
        if (e->occ[ix]) continue;
        e->occ[ix] = 1;
        for (int k = 0; k < 3; k++) e->w[depth][k] = q[k];
        dfs_prefix(e, depth + 1, pd, L, reduced);
        e->occ[ix] = 0;
    }
}
static PrefList prefixes(const int *start, int pd, int reduced){
    PrefList L = {0, 0, 0};
    Enum e;
    e.occ = calloc(G*G*G, 1);
    e.y0 = start[1];
    for (int k = 0; k < 3; k++) e.w[0][k] = start[k];
    e.occ[IDX(start)] = 1;
    dfs_prefix(&e, 1, pd, &L, reduced);
    free(e.occ);
    return L;
}
/* run the callback on every bridge with N beads that extends the prefix */
static void enum_from_prefix(const Prefix *p, int N, unsigned char *occ, cb_t cb, void *ctx){
    Enum e;
    e.occ = occ; e.N = N; e.cb = cb; e.ctx = ctx; e.y0 = p->w[0][1];
    int ymax = p->w[0][1];
    for (int i = 0; i < p->n; i++){
        for (int k = 0; k < 3; k++) e.w[i][k] = p->w[i][k];
        occ[IDX(p->w[i])] = 1;
        if (p->w[i][1] > ymax) ymax = p->w[i][1];
    }
    /* pruning test for the prefix itself */
    if (p->w[p->n-1][1] + (N - p->n) >= ymax) dfs(&e, p->n, ymax);
    for (int i = 0; i < p->n; i++) occ[IDX(p->w[i])] = 0;
}

/* ------------------------------------------------------------------ mode "single" */
#define NVARIANT 9
static const int VAR[NVARIANT][2] = {{2,3},{1,3},{2,2},{3,3},{5,5},{0,3},{2,0},{1,2},{1,1}};   /* head, tail */

typedef struct {
    long long nbr[MAXS+1], nclean[MAXS+1], npair[MAXS+1], nbdown[MAXS+1];
    int maxA[MAXS+1][4], maxB[MAXS+1][4], maxnA[MAXS+1], maxnB[MAXS+1];
    long long nAfull[MAXS+1], nBfull[MAXS+1];
    int haveA, haveB; int exA[MAXS][3], exAc[3], exAn, exB[MAXS][3], exBn;
    long long notclean[NVARIANT][MAXS+1], neq[NVARIANT][MAXS+1], ntest[NVARIANT][MAXS+1];
    int maxcost[NVARIANT][4], maxncost[NVARIANT];
    int havex[NVARIANT]; int ex[NVARIANT][MAXS][3], exc[NVARIANT][3], exn[NVARIANT];
    int havexq[NVARIANT]; int exq[NVARIANT][MAXS][3], exqc[NVARIANT][3], exqn[NVARIANT];
    long long bad;
    int nvar, dumpN;
} SStat;

/* deterministic choice of the printed example: fewest beads, then lexicographically smallest coordinate list */
static inline int better(int have, int n, int (*w)[3], int exn, int (*ex)[3]){
    if (!have || n < exn) return 1;
    if (n > exn) return 0;
    for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++){ if (w[i][k] < ex[i][k]) return 1; if (w[i][k] > ex[i][k]) return 0; }
    return 0;
}
static void cb_single(int (*w)[3], int n, void *ctx){
    SStat *s = (SStat *)ctx;
    int hg[4], B[4], c[2][3], A[4], x[MAXB][3], hg2[4];
    int rc = walk_hg(w, n, hg);
    if (rc || !is_bridge(w, n)){ s->bad++; return; }
    s->nbr[n]++;
    B_of(w, n, B);
    int nc = admissible(w, n, c);
    if (nc < 1 || nc > 2){ s->bad++; return; }
    if (nc == 2) s->nbdown[n]++;
    int cl = is_clean(w, n);
    s->nclean[n] += cl;
    for (int k = 0; k < 4; k++) if (B[k] > s->maxB[n][k]) s->maxB[n][k] = B[k];
    if (cnorm4(B) > s->maxnB[n]) s->maxnB[n] = cnorm4(B);
    if (B[0] == 0 && B[1] == 3 && B[2] == 4){
        s->nBfull[n]++;
        if (better(s->haveB, n, w, s->exBn, s->exB)){ s->haveB = 1; s->exBn = n; memcpy(s->exB, w, n*sizeof(int[3])); }
    }
    for (int ci = 0; ci < nc; ci++){
        A_of(w, n, c[ci], A);
        s->npair[n]++;
        for (int k = 0; k < 4; k++) if (A[k] > s->maxA[n][k]) s->maxA[n][k] = A[k];
        if (cnorm4(A) > s->maxnA[n]) s->maxnA[n] = cnorm4(A);
        if (A[0] == 1 && A[1] == 6 && A[2] == 10 && A[3] == 1){
            s->nAfull[n]++;
            if (better(s->haveA, n, w, s->exAn, s->exA)){ s->haveA = 1; s->exAn = n; memcpy(s->exA, w, n*sizeof(int[3])); memcpy(s->exAc, c[ci], sizeof(int[3])); }
        }
        if (s->dumpN && n <= s->dumpN){
            #pragma omp critical(dump)
            {
                printf("D %d %d %d %d %d | %d %d %d %d | %d %d %d %d | %d %d %d | %d |", n, hg[0], hg[1], hg[2], hg[3],
                       A[0], A[1], A[2], A[3], B[0], B[1], B[2], B[3], c[ci][0], c[ci][1], c[ci][2], cl);
                for (int i = 0; i < n; i++) printf(" %d %d %d", w[i][0], w[i][1], w[i][2]);
                printf("\n");
            }
        }
        int qh[4];
        for (int k = 0; k < 4; k++) qh[k] = hg[k] + A[k] + B[k];
        for (int v = 0; v < NVARIANT; v++){
            if (v > 0 && n > s->nvar) break;
            int n2 = extend(w, n, c[ci], VAR[v][0], VAR[v][1], x);
            int rc2 = walk_hg(x, n2, hg2);
            if (rc2 || !is_bridge(x, n2) || n2 != n + VAR[v][0] + VAR[v][1]){ s->bad++; continue; }
            s->ntest[v][n]++;
            int cl2 = is_clean(x, n2);
            int eq = (hg2[0] == qh[0] && hg2[1] == qh[1] && hg2[2] == qh[2] && hg2[3] == qh[3]);
            if (!cl2){
                s->notclean[v][n]++;
                if (better(s->havex[v], n, w, s->exn[v], s->ex[v])){ s->havex[v] = 1; s->exn[v] = n; memcpy(s->ex[v], w, n*sizeof(int[3])); memcpy(s->exc[v], c[ci], sizeof(int[3])); }
            }
            if (!eq){
                s->neq[v][n]++;
                if (better(s->havexq[v], n, w, s->exqn[v], s->exq[v])){ s->havexq[v] = 1; s->exqn[v] = n; memcpy(s->exq[v], w, n*sizeof(int[3])); memcpy(s->exqc[v], c[ci], sizeof(int[3])); }
            }
            int cost[4];
            for (int k = 0; k < 4; k++){ cost[k] = hg2[k] - hg[k]; if (cost[k] > s->maxcost[v][k]) s->maxcost[v][k] = cost[k]; if (cost[k] < 0) s->bad++; }
            if (cnorm4(cost) > s->maxncost[v]) s->maxncost[v] = cnorm4(cost);
        }
    }
}

static void merge_sstat(SStat *t, const SStat *s){
    for (int n = 0; n <= MAXS; n++){
        t->nbr[n] += s->nbr[n]; t->nclean[n] += s->nclean[n]; t->npair[n] += s->npair[n]; t->nbdown[n] += s->nbdown[n];
        t->nAfull[n] += s->nAfull[n]; t->nBfull[n] += s->nBfull[n];
        if (s->maxnA[n] > t->maxnA[n]) t->maxnA[n] = s->maxnA[n];
        if (s->maxnB[n] > t->maxnB[n]) t->maxnB[n] = s->maxnB[n];
        for (int k = 0; k < 4; k++){
            if (s->maxA[n][k] > t->maxA[n][k]) t->maxA[n][k] = s->maxA[n][k];
            if (s->maxB[n][k] > t->maxB[n][k]) t->maxB[n][k] = s->maxB[n][k];
        }
        for (int v = 0; v < NVARIANT; v++){ t->notclean[v][n] += s->notclean[v][n]; t->neq[v][n] += s->neq[v][n]; t->ntest[v][n] += s->ntest[v][n]; }
    }
    if (s->haveA && better(t->haveA, s->exAn, (int (*)[3])s->exA, t->exAn, t->exA)){ t->haveA = 1; t->exAn = s->exAn; memcpy(t->exA, s->exA, sizeof(t->exA)); memcpy(t->exAc, s->exAc, sizeof(t->exAc)); }
    if (s->haveB && better(t->haveB, s->exBn, (int (*)[3])s->exB, t->exBn, t->exB)){ t->haveB = 1; t->exBn = s->exBn; memcpy(t->exB, s->exB, sizeof(t->exB)); }
    for (int v = 0; v < NVARIANT; v++){
        for (int k = 0; k < 4; k++) if (s->maxcost[v][k] > t->maxcost[v][k]) t->maxcost[v][k] = s->maxcost[v][k];
        if (s->maxncost[v] > t->maxncost[v]) t->maxncost[v] = s->maxncost[v];
        if (s->havex[v] && better(t->havex[v], s->exn[v], (int (*)[3])s->ex[v], t->exn[v], t->ex[v])){ t->havex[v] = 1; t->exn[v] = s->exn[v]; memcpy(t->ex[v], s->ex[v], sizeof(t->ex[v])); memcpy(t->exc[v], s->exc[v], sizeof(t->exc[v])); }
        if (s->havexq[v] && better(t->havexq[v], s->exqn[v], (int (*)[3])s->exq[v], t->exqn[v], t->exq[v])){ t->havexq[v] = 1; t->exqn[v] = s->exqn[v]; memcpy(t->exq[v], s->exq[v], sizeof(t->exq[v])); memcpy(t->exqc[v], s->exqc[v], sizeof(t->exqc[v])); }
    }
    t->bad += s->bad;
}

static int mode_single(int NMAX, int NVAR, int threads, int dumpN){
    static SStat tot;
    memset(&tot, 0, sizeof(tot));
    int start[3] = {0, 0, 0};
    double t0 = omp_get_wtime();
    printf("# mode single: reduced enumeration (start at the origin, an A site; first two bonds a0 = (1,1,1), -a1 = (-1,1,1)); N <= %d; head/tail variants for N <= %d; %d threads\n", NMAX, NVAR, threads);
    for (int N = 3; N <= NMAX; N++){
        int pd = N < 9 ? 3 : 9;
        PrefList L = prefixes(start, pd, 1);
        #pragma omp parallel num_threads(threads)
        {
            SStat *s = calloc(1, sizeof(SStat));
            s->nvar = NVAR; s->dumpN = dumpN;
            unsigned char *occ = calloc(G*G*G, 1);
            #pragma omp for schedule(dynamic, 1)
            for (long long i = 0; i < L.n; i++) enum_from_prefix(&L.a[i], N, occ, cb_single, s);
            #pragma omp critical(merge)
            merge_sstat(&tot, s);
            free(occ); free(s);
        }
        free(L.a);
        printf("N %2d: bridges %10lld  clean %10lld  (bridge,c1) %10lld  b' down %10lld | max A (%d,%d,%d;%d) norm %2d  #A=(1,6,10;1): %lld | max B (%d,%d,%d;%d) norm %2d  #B=(0,3,4;0): %lld | [%.0f s]\n",
               N, tot.nbr[N], tot.nclean[N], tot.npair[N], tot.nbdown[N],
               tot.maxA[N][0], tot.maxA[N][1], tot.maxA[N][2], tot.maxA[N][3], tot.maxnA[N], tot.nAfull[N],
               tot.maxB[N][0], tot.maxB[N][1], tot.maxB[N][2], tot.maxB[N][3], tot.maxnB[N], tot.nBfull[N], omp_get_wtime() - t0);
        fflush(stdout);
    }
    printf("# walks that failed a walk/bridge/sign test (must be 0): %lld\n", tot.bad);
    for (int v = 0; v < NVARIANT; v++){
        int nmaxv = v == 0 ? NMAX : NVAR;
        long long T = 0, F = 0, Q = 0;
        for (int n = 3; n <= nmaxv; n++){ T += tot.ntest[v][n]; F += tot.notclean[v][n]; Q += tot.neq[v][n]; }
        printf("variant head %d + tail %d, N <= %d: %lld pairs (bridge,c1); result NOT clean: %lld; (h,g) != q-hat: %lld; max cost (%d,%d,%d;%d), largest norm %d\n",
               VAR[v][0], VAR[v][1], nmaxv, T, F, Q, tot.maxcost[v][0], tot.maxcost[v][1], tot.maxcost[v][2], tot.maxcost[v][3], tot.maxncost[v]);
        if (F){
            printf("   not clean per N:");
            for (int n = 3; n <= nmaxv; n++) if (tot.notclean[v][n]) printf(" %d:%lld", n, tot.notclean[v][n]);
            printf("\n   a smallest counterexample (N = %d, c1 = (%d,%d,%d)): ", tot.exn[v], tot.exc[v][0], tot.exc[v][1], tot.exc[v][2]);
            print_walk(stdout, tot.ex[v], tot.exn[v]); printf("\n");
        }
        if (Q){
            printf("   (h,g) != q-hat per N:");
            for (int n = 3; n <= nmaxv; n++) if (tot.neq[v][n]) printf(" %d:%lld", n, tot.neq[v][n]);
            printf("\n   a smallest counterexample (N = %d, c1 = (%d,%d,%d)): ", tot.exqn[v], tot.exqc[v][0], tot.exqc[v][1], tot.exqc[v][2]);
            print_walk(stdout, tot.exq[v], tot.exqn[v]); printf("\n");
        }
    }
    if (tot.haveA){ printf("first (x, c1) with A = (1,6,10;1): N = %d, c1 = (%d,%d,%d): ", tot.exAn, tot.exAc[0], tot.exAc[1], tot.exAc[2]); print_walk(stdout, tot.exA, tot.exAn); printf("\n"); }
    else printf("no (x, c1) with A = (1,6,10;1) for N <= %d\n", NMAX);
    if (tot.haveB){ printf("first x with B = (0,3,4;0): N = %d: ", tot.exBn); print_walk(stdout, tot.exB, tot.exBn); printf("\n"); }
    else printf("no x with B = (0,3,4;0) for N <= %d\n", NMAX);
    printf("# time %.1f s\n", omp_get_wtime() - t0);
    return tot.bad != 0;
}

/* ------------------------------------------------------------------ mode "pairs" */
typedef struct {
    int n;
    signed char w[MAXS][3];
    int hg[4], B[4];
    int nc; int c[2][3]; int A[2][4];
    int clean;
} Br;
typedef struct { Br *a; long long n, cap; long long bad; } BrList;

static void cb_store(int (*w)[3], int n, void *ctx){
    BrList *L = (BrList *)ctx;
    if (L->n == L->cap){ L->cap = L->cap ? 2*L->cap : 4096; L->a = realloc(L->a, L->cap*sizeof(Br)); }
    Br *b = &L->a[L->n];
    b->n = n;
    for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++) b->w[i][k] = (signed char)w[i][k];
    if (walk_hg(w, n, b->hg) || !is_bridge(w, n)){ L->bad++; return; }
    B_of(w, n, b->B);
    b->nc = admissible(w, n, b->c);
    if (b->nc < 1 || b->nc > 2){ L->bad++; return; }
    for (int ci = 0; ci < b->nc; ci++) A_of(w, n, b->c[ci], b->A[ci]);
    b->clean = is_clean(w, n);
    L->n++;
}

typedef struct {
    long long nconc, npairs, ncleanpairs, fail;
    int maxerr[4], maxnerr;
} PStat;

static void report_fail(const char *what, const Br *x1, int ci, const Br *x2, int (*y)[3], int n){
    #pragma omp critical(fail)
    {
        g_fail++;
        if (g_fail <= 20){
            printf("FAIL %s: N1 = %d, N2 = %d, c1 = (%d,%d,%d)\n  x1 = ", what, x1->n, x2->n, x1->c[ci][0], x1->c[ci][1], x1->c[ci][2]);
            for (int i = 0; i < x1->n; i++) printf("(%d,%d,%d) ", x1->w[i][0], x1->w[i][1], x1->w[i][2]);
            printf("\n  x2 = ");
            for (int i = 0; i < x2->n; i++) printf("(%d,%d,%d) ", x2->w[i][0], x2->w[i][1], x2->w[i][2]);
            printf("\n  y  = ");
            if (y) print_walk(stdout, y, n);
            printf("\n");
            fflush(stdout);
        }
    }
}

static void check_pair(const Br *x1, int ci, const Br *x2, PStat *st){
    int y[MAXB][3], n1 = x1->n, n2 = x2->n, n = n1 + n2 + 3;
    int b[3], c1[3], u1[3], u2[3], t[3], Q[3];
    for (int i = 0; i < n1; i++) for (int k = 0; k < 3; k++) y[i][k] = x1->w[i][k];
    for (int k = 0; k < 3; k++){
        b[k] = x1->w[n1-1][k] - x1->w[n1-2][k];
        c1[k] = x1->c[ci][k];
        u1[k] = x2->w[1][k] - x2->w[0][k];
        u2[k] = x2->w[2][k] - x2->w[1][k];
    }
    for (int k = 0; k < 3; k++){
        t[k] = y[n1-1][k] + c1[k];      y[n1][k]   = t[k];
        t[k] += b[k];                   y[n1+1][k] = t[k];
        t[k] += c1[k];                  y[n1+2][k] = t[k];
        Q[k] = t[k] + b[k];
    }
    int cnt = 0, gsel = -1, im1[3], im2[3];
    for (int gi = 0; gi < 8; gi++){
        gmap(gi, u1, im1); gmap(gi, u2, im2);
        if (im1[0] == c1[0] && im1[1] == c1[1] && im1[2] == c1[2] && im2[0] == b[0] && im2[1] == b[1] && im2[2] == b[2]){ cnt++; gsel = gi; }
    }
    if (cnt != 1){ st->fail++; report_fail("height-preserving symmetry not unique", x1, ci, x2, NULL, 0); return; }
    for (int i = 0; i < n2; i++){
        int d[3], gd[3];
        for (int k = 0; k < 3; k++) d[k] = x2->w[i][k] - x2->w[0][k];
        gmap(gsel, d, gd);
        for (int k = 0; k < 3; k++) y[n1+3+i][k] = Q[k] + gd[k];
    }
    st->nconc++;
    int hg[4];
    if (walk_hg(y, n, hg)){ st->fail++; report_fail("concatenation is not a self-avoiding lattice walk", x1, ci, x2, y, n); return; }
    if (!is_bridge(y, n)){ st->fail++; report_fail("concatenation is not a bridge", x1, ci, x2, y, n); return; }
    int err[4], ok = 1;
    for (int k = 0; k < 4; k++){
        err[k] = hg[k] - x1->hg[k] - x2->hg[k];
#if MUT == 1
        if (err[k] != x1->A[ci][k]) ok = 0;
#else
        if (err[k] != x1->A[ci][k] + x2->B[k]) ok = 0;
#endif
    }
    if (!ok){ st->fail++; report_fail("(h,g)(x1 o x2) != (h,g)(x1) + (h,g)(x2) + A(x1,c1) + B(x2)", x1, ci, x2, y, n); return; }
    for (int k = 0; k < 4; k++) if (err[k] > st->maxerr[k]) st->maxerr[k] = err[k];
    if (cnorm4(err) > st->maxnerr) st->maxnerr = cnorm4(err);
    int By[4];
    B_of(y, n, By);
#if MUT == 2
    const int *Bref = x2->B;
#else
    const int *Bref = x1->B;
#endif
    if (By[0] != Bref[0] || By[1] != Bref[1] || By[2] != Bref[2] || By[3] != Bref[3]){ st->fail++; report_fail("B(x1 o x2) != B(x1)", x1, ci, x2, y, n); return; }
    int cy[2][3];
    int ncy = admissible(y, n, cy);
    if (ncy != x2->nc){ st->fail++; report_fail("number of admissible c1 of the concatenation differs from that of x2", x1, ci, x2, y, n); return; }
    for (int cj = 0; cj < x2->nc; cj++){
        int gc[3], found = 0, Ay[4];
        gmap(gsel, x2->c[cj], gc);
        for (int m = 0; m < ncy; m++) if (cy[m][0] == gc[0] && cy[m][1] == gc[1] && cy[m][2] == gc[2]) found = 1;
        if (!found){ st->fail++; report_fail("phi(c1'') is not admissible for the concatenation", x1, ci, x2, y, n); return; }
        A_of(y, n, gc, Ay);
#if MUT == 3
        for (int k = 0; k < 4; k++) if (Ay[k] != x1->A[ci][k]) found = 0;
#else
        for (int k = 0; k < 4; k++) if (Ay[k] != x2->A[cj][k]) found = 0;
#endif
        if (!found){ st->fail++; report_fail("A(x1 o x2, phi(c1'')) != A(x2, c1'')", x1, ci, x2, y, n); return; }
        for (int k = 0; k < 4; k++)
            if (hg[k] + Ay[k] + By[k] != (x1->hg[k] + x1->A[ci][k] + x1->B[k]) + (x2->hg[k] + x2->A[cj][k] + x2->B[k])){
                st->fail++; report_fail("q-hat not additive", x1, ci, x2, y, n); return;
            }
        st->npairs++;
    }
    int cly = is_clean(y, n);
    int expect = (x1->B[0] == 0 && x1->B[1] == 0 && x1->B[2] == 0) && (x2->nc == 1 && !(x2->A[0][0] | x2->A[0][1] | x2->A[0][2] | x2->A[0][3]));
    if (cly != expect){ st->fail++; report_fail("cleanliness of the concatenation is not (lower end of x1 clean and upper end of x2 clean)", x1, ci, x2, y, n); return; }
    if (x1->clean && x2->clean){
        st->ncleanpairs++;
        if (err[0] | err[1] | err[2] | err[3]){ st->fail++; report_fail("clean pair: (h,g) not exactly additive", x1, ci, x2, y, n); return; }
        if (!cly){ st->fail++; report_fail("clean pair: concatenation not clean", x1, ci, x2, y, n); return; }
    }
}

/* x1 runs over the bridges with N1MIN..N1MAX beads, x2 over those with N2MIN..N2MAX beads;
   pairs with N1 <= SKIP and N2 <= SKIP are skipped (covered by an earlier run) */
static int mode_pairs(int N1MAX, int N2MAX, int SKIP, int N1MIN, int N2MIN, int full, int threads){
    int NMAX = N1MAX > N2MAX ? N1MAX : N2MAX;
    BrList L = {0, 0, 0, 0};
    double t0 = omp_get_wtime();
    unsigned char *occ = calloc(G*G*G, 1);
    long long cntN[MAXS+1], cleanN[MAXS+1], pairN[MAXS+1];
    memset(cntN, 0, sizeof(cntN)); memset(cleanN, 0, sizeof(cleanN)); memset(pairN, 0, sizeof(pairN));
    int starts[2][3] = {{0,0,0},{1,1,1}};
    for (int si = 0; si < (full ? 2 : 1); si++)
        for (int N = 3; N <= NMAX; N++){
            PrefList P = prefixes(starts[si], 3, !full);
            for (long long i = 0; i < P.n; i++) enum_from_prefix(&P.a[i], N, occ, cb_store, &L);
            free(P.a);
        }
    free(occ);
    long long npc = 0;
    for (long long i = 0; i < L.n; i++){ cntN[L.a[i].n]++; cleanN[L.a[i].n] += L.a[i].clean; pairN[L.a[i].n] += L.a[i].nc; npc += L.a[i].nc; }
    printf("# mode pairs: %s; N1 <= %d, N2 <= %d", full ? "FULL set (start at an A site and at a B site, all four choices of the first two bonds)" :
           "reduced set (start at the origin, first two bonds a0, -a1)", N1MAX, N2MAX);
    if (N1MIN > 3 || N2MIN > 3) printf(", N1 >= %d, N2 >= %d", N1MIN, N2MIN);
    if (SKIP) printf(" (pairs with N1 <= %d and N2 <= %d skipped)", SKIP, SKIP);
    printf("; %d threads\n", threads);
    printf("# bridges per N (clean; (bridge,c1)):");
    for (int N = 3; N <= NMAX; N++) printf(" %d: %lld (%lld; %lld)", N, cntN[N], cleanN[N], pairN[N]);
    printf("\n# total: %lld bridges, %lld pairs (bridge, c1); enumeration errors (must be 0): %lld; [%.1f s]\n", L.n, npc, L.bad, omp_get_wtime() - t0);
    fflush(stdout);
    PStat tot;
    memset(&tot, 0, sizeof(tot));
    #pragma omp parallel num_threads(threads)
    {
        PStat st;
        memset(&st, 0, sizeof(st));
        #pragma omp for schedule(dynamic, 8)
        for (long long i1 = 0; i1 < L.n; i1++){
            const Br *x1 = &L.a[i1];
            if (x1->n > N1MAX || x1->n < N1MIN) continue;
            for (int ci = 0; ci < x1->nc; ci++)
                for (long long i2 = 0; i2 < L.n; i2++){
                    if (L.a[i2].n > N2MAX || L.a[i2].n < N2MIN) continue;
                    if (x1->n <= SKIP && L.a[i2].n <= SKIP) continue;
                    check_pair(x1, ci, &L.a[i2], &st);
                }
        }
        #pragma omp critical(merge)
        {
            tot.nconc += st.nconc; tot.npairs += st.npairs; tot.ncleanpairs += st.ncleanpairs; tot.fail += st.fail;
            for (int k = 0; k < 4; k++) if (st.maxerr[k] > tot.maxerr[k]) tot.maxerr[k] = st.maxerr[k];
            if (st.maxnerr > tot.maxnerr) tot.maxnerr = st.maxnerr;
        }
    }
    printf("concatenations built from coordinates (x1, c1, x2): %lld\n", tot.nconc);
    printf("ordered pairs ((x1,c1), (x2,c1'')) with all identities of (a) checked: %lld\n", tot.npairs);
    printf("ordered pairs of clean bridges (exact additivity of (h,g), concatenation clean): %lld\n", tot.ncleanpairs);
    printf("failures: %lld\n", tot.fail);
    printf("error vector (h,g)(x1 o x2) - (h,g)(x1) - (h,g)(x2): componentwise maxima (%d,%d,%d;%d), largest norm %d\n",
           tot.maxerr[0], tot.maxerr[1], tot.maxerr[2], tot.maxerr[3], tot.maxnerr);
    printf("# time %.1f s\n", omp_get_wtime() - t0);
    return tot.fail != 0 || L.bad != 0;
}

int main(int argc, char **argv){
    if (argc >= 3 && !strcmp(argv[1], "pairs")){
        int NMAX = atoi(argv[2]);
        int full = argc >= 4 && !strcmp(argv[3], "full");
        int threads = argc >= 5 ? atoi(argv[4]) : 2;
        if (NMAX > MAXS - 1 || 2*NMAX + 3 > MAXB){ fprintf(stderr, "NMAX too large\n"); return 2; }
        return mode_pairs(NMAX, NMAX, 0, 3, 3, full, threads);
    }
    if (argc >= 5 && !strcmp(argv[1], "pairs2")){
        int N1MAX = atoi(argv[2]), N2MAX = atoi(argv[3]), SKIP = atoi(argv[4]);
        int threads = argc >= 6 ? atoi(argv[5]) : 2;
        int NM = N1MAX > N2MAX ? N1MAX : N2MAX;
        if (NM > MAXS - 1 || N1MAX + N2MAX + 3 > MAXB){ fprintf(stderr, "sizes too large\n"); return 2; }
        int N1MIN = argc >= 7 ? atoi(argv[6]) : 3, N2MIN = argc >= 8 ? atoi(argv[7]) : 3;
        return mode_pairs(N1MAX, N2MAX, SKIP, N1MIN, N2MIN, 0, threads);
    }
    if (argc >= 4 && !strcmp(argv[1], "single")){
        int NMAX = atoi(argv[2]), NVAR = atoi(argv[3]);
        int threads = argc >= 5 ? atoi(argv[4]) : 2;
        int dumpN = argc >= 6 ? atoi(argv[5]) : 0;
        if (NMAX > MAXS - 1){ fprintf(stderr, "NMAX too large\n"); return 2; }
        return mode_single(NMAX, NVAR, threads, dumpN);
    }
    fprintf(stderr, "usage: v9_cobound pairs NMAX [full|reduced] [threads]\n       v9_cobound single NMAX NVAR [threads] [dumpN]\n");
    return 2;
}
