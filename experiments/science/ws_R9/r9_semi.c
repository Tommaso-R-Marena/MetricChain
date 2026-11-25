/* r9_semi.c — workstream R9 (second-round review of the theory report at 658b77f).
 *
 * Exhaustive tests of the "clean-ends semigroup" sketch of THY-RES-0007 §1.3 (answer to our request T-4).
 * OWN CODE, written from the Setting paragraph of theory report §11.22 and from the statement of Lemma
 * 11.68; not derived from the theory division's mylat.py / concat_check.py / t4_semigroup.py (which I read)
 * nor from R2's r2_concat.c (which I did not open before writing this).
 *
 * Lattice: A = {(x,y,z) in (2Z)^3 : x+y+z = 0 mod 4}, B = A + (1,1,1).  Bond vectors a0=(1,1,1),
 * a1=(1,-1,-1), a2=(-1,1,-1), a3=(-1,-1,1): an A site is bonded to +a_i, a B site to -a_i.
 * Height = the coordinate y; every bond changes it by +-1.
 * Walk with N beads: injective sequence of lattice sites, consecutive ones bonded.
 * h_d = #{p<q : q-p >= 3, |x_q - x_p|^2 = d}, d in {3,8,11};  g = #{i : |x_{i+3}-x_i|^2 = 11}.
 * Bridge: first bead strictly lowest, last bead (weakly) highest.
 *
 * DEFINITION UNDER TEST (precise form of "clean ends"; N >= 3):
 *   Let b = x_{N-1}-x_{N-2} (the last bond; an up-bond for every bridge), b' = x_{N-2}-x_{N-3},
 *   u1 = x_1-x_0, u2 = x_2-x_1 (both up-bonds for every bridge).
 *   TOP-CLEAN:    b' is an up-bond, and with t_1 = x_{N-1}+b', t_2 = t_1+b, t_3 = t_2+b' (regarded as beads
 *                 N, N+1, N+2 of the prolonged chain) there is NO pair (t_j, x_p) at chain separation >= 3
 *                 with squared distance in {3,8,11}.
 *   BOTTOM-CLEAN: with s_1 = x_0-u2, s_2 = s_1-u1, s_3 = s_2-u2 (beads -1,-2,-3) there is NO pair (s_j, x_p)
 *                 at chain separation >= 3 with squared distance in {3,8,11}.
 *   CLEAN = TOP-CLEAN and BOTTOM-CLEAN.
 * CLAIMS UNDER TEST:
 *   (S1) for clean x1, x2 the concatenation of Lemma 11.68 (x1, t_1,t_2,t_3, phi(x2)) is a bridge with
 *        N1+N2+3 beads, (h,g) = (h,g)(x1)+(h,g)(x2) EXACTLY, and it is clean.
 *   (S2) every bridge x becomes clean after a head of kh and a tail of kt zigzag beads; cost bounded.
 *        (theory division: kh = kt = 5; this file also tests kh = 2, kt = 3 and smaller values.)
 *
 * usage: r9_semi NMAX NPAIR NSCR OUTDIR [part nparts]
 *   NMAX : enumerate all bridges with 3..NMAX beads (first two bonds fixed: +a0, then -a1)
 *   NPAIR: real concatenations of ALL ordered pairs of clean bridges with at most NPAIR beads
 *   NSCR : the from-scratch cleaning tests (S2) are run for bridges with at most NSCR beads
 *   part/nparts: only the outer index i = part mod nparts of the pair loop (for two processes)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define OFF 64
#define DIM 128
#define IDX(x,y,z) ((((x)+OFF)*DIM + ((y)+OFF))*DIM + ((z)+OFF))
#define MAXB 96

typedef struct { int x, y, z; } P3;
static const int AV[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};

static int16_t *occ;    /* grid of the enumeration: 0 empty, else bead index + 1 */
static int16_t *occ2;   /* scratch grid for walks built from coordinates          */

/* all integer vectors of squared norm 3, 8, 11 (no lattice knowledge) */
static int nv[3]; static int voff[3][64]; static P3 vvec[3][64];

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }

static int mod4(int a) { int r = a % 4; return r < 0 ? r + 4 : r; }
static int mod2(int a) { int r = a % 2; return r < 0 ? r + 2 : r; }
static int is_site(P3 p) {
    int ex = mod2(p.x), ey = mod2(p.y), ez = mod2(p.z);
    if (!ex && !ey && !ez) return mod4(p.x + p.y + p.z) == 0;
    if (ex && ey && ez)    return mod4(p.x + p.y + p.z - 3) == 0;
    return 0;
}
static int sq(P3 a, P3 b) { int dx=a.x-b.x, dy=a.y-b.y, dz=a.z-b.z; return dx*dx+dy*dy+dz*dz; }
static P3 add(P3 a, P3 b) { P3 r = {a.x+b.x, a.y+b.y, a.z+b.z}; return r; }
static P3 sub(P3 a, P3 b) { P3 r = {a.x-b.x, a.y-b.y, a.z-b.z}; return r; }

/* ---------- walks from coordinates, on the scratch grid ---------- */
/* returns 0 if w is a self-avoiding lattice walk (and leaves it placed), else a positive code (nothing placed) */
static int place2(const P3 *w, int n) {
    for (int i = 0; i < n; i++) {
        int bad = 0;
        if (!is_site(w[i])) bad = 1;
        else if (abs(w[i].x) > OFF-6 || abs(w[i].y) > OFF-6 || abs(w[i].z) > OFF-6) die("grid too small");
        else if (i > 0 && sq(w[i], w[i-1]) != 3) bad = 2;
        else if (occ2[IDX(w[i].x, w[i].y, w[i].z)]) bad = 3;
        if (bad) { for (int j = 0; j < i; j++) occ2[IDX(w[j].x, w[j].y, w[j].z)] = 0; return bad; }
        occ2[IDX(w[i].x, w[i].y, w[i].z)] = (int16_t)(i + 1);
    }
    return 0;
}
static void unplace2(const P3 *w, int n) { for (int i = 0; i < n; i++) occ2[IDX(w[i].x, w[i].y, w[i].z)] = 0; }
static int is_bridge(const P3 *w, int n) {
    for (int i = 1; i < n; i++) if (w[i].y <= w[0].y) return 0;
    for (int i = 0; i < n; i++) if (w[i].y > w[n-1].y) return 0;
    return 1;
}
/* (h3,h8,h11,g) of a placed walk straight from the definition (grid look-ups) */
static void profile2(const P3 *w, int n, int hg[4]) {
    hg[0] = hg[1] = hg[2] = hg[3] = 0;
    for (int q = 0; q < n; q++) {
        int id = IDX(w[q].x, w[q].y, w[q].z);
        for (int t = 0; t < 3; t++)
            for (int i = 0; i < nv[t]; i++) { int o = occ2[id + voff[t][i]]; if (o && q - (o-1) >= 3) hg[t]++; }
    }
    for (int i = 0; i + 3 < n; i++) {
        int d = sq(w[i], w[i+3]);
        if (d == 11) hg[3]++; else if (d != 19) die("1-4 distance not 11 or 19");
    }
}
/* the same by the O(n^2) definition, no grid at all (used on samples as an independent check) */
static void profile_brute(const P3 *w, int n, int hg[4]) {
    hg[0] = hg[1] = hg[2] = hg[3] = 0;
    for (int p = 0; p < n; p++) for (int q = p + 3; q < n; q++) {
        int d = sq(w[p], w[q]);
        if (d == 3) hg[0]++; else if (d == 8) hg[1]++; else if (d == 11) hg[2]++;
    }
    for (int i = 0; i + 3 < n; i++) if (sq(w[i], w[i+3]) == 11) hg[3]++;
}
/* extra pairs of a virtual bead at site s with index vi against the walk placed on grid G; c[3] += counts.
   returns -1 if the site itself is occupied */
static int extra_pairs(const int16_t *G, P3 s, int vi, int c[3]) {
    int id = IDX(s.x, s.y, s.z);
    if (G[id]) return -1;
    for (int t = 0; t < 3; t++)
        for (int i = 0; i < nv[t]; i++) { int o = G[id + voff[t][i]]; if (o) { int sep = vi - (o-1); if (sep < 0) sep = -sep; if (sep >= 3) c[t]++; } }
    return 0;
}
/* top data of a walk w (placed on G with labels index+1): b' up?, and for the zigzag continuation with first
   bond c1 the extra-pair counts of t_1..t_k.  Returns -1 on a collision. */
static int top_counts(const int16_t *G, const P3 *w, int n, P3 c1, int k, int c[3]) {
    P3 b = sub(w[n-1], w[n-2]);
    P3 p = w[n-1];
    c[0] = c[1] = c[2] = 0;
    for (int j = 1; j <= k; j++) {
        p = add(p, (j & 1) ? c1 : b);
        if (extra_pairs(G, p, n - 1 + j, c) < 0) return -1;
    }
    return 0;
}
static int bottom_counts(const int16_t *G, const P3 *w, int n, int k, int c[3]) {
    P3 u1 = sub(w[1], w[0]), u2 = sub(w[2], w[1]);
    P3 p = w[0];
    (void)n;
    c[0] = c[1] = c[2] = 0;
    for (int j = 1; j <= k; j++) {
        p = sub(p, (j & 1) ? u2 : u1);
        if (extra_pairs(G, p, -j, c) < 0) return -1;
    }
    return 0;
}
/* clean flags of a walk placed on G, by the definition (k = 3 linker sites at either end) */
static void clean_flags(const int16_t *G, const P3 *w, int n, int *top, int *bot) {
    P3 bp = sub(w[n-2], w[n-3]);
    int c[3];
    *top = 0; *bot = 0;
    if (bp.y == 1) { if (top_counts(G, w, n, bp, 3, c) == 0 && c[0] == 0 && c[1] == 0 && c[2] == 0) *top = 1; }
    if (bottom_counts(G, w, n, 3, c) == 0 && c[0] == 0 && c[1] == 0 && c[2] == 0) *bot = 1;
}

/* ---------- storage of clean bridges for the pair test ---------- */
typedef struct { int n; int hg[4]; int8_t c[3*24]; } stored_t;
static stored_t *store; static long nstore = 0, capstore = 0;

/* ---------- class tables ---------- */
#define HSIZE (1<<17)
typedef struct { int used, h3, h8, h11; uint64_t mall, mclean; } cls_t;
static cls_t *tab;
static void record(int h3, int h8, int h11, int g, int clean) {
    uint32_t key = (uint32_t)(h3 + 64*(h8 + 256*h11));
    uint32_t i = (key * 2654435761u) & (HSIZE-1);
    while (tab[i].used && !(tab[i].h3==h3 && tab[i].h8==h8 && tab[i].h11==h11)) i = (i+1) & (HSIZE-1);
    if (!tab[i].used) { tab[i].used = 1; tab[i].h3 = h3; tab[i].h8 = h8; tab[i].h11 = h11; }
    tab[i].mall |= (1ull << g);
    if (clean) tab[i].mclean |= (1ull << g);
}

/* ---------- per-N statistics ---------- */
static P3 X[MAXB]; static int N, NPAIR, NSCR;
static long n_br, n_top, n_bot, n_clean, n_bpup;
static int maxA[5], maxB[5];                 /* componentwise maxima of the A- and B-parts, [4] = norm */
static long n_d3;
#define NCOMB 8
static const int KH[NCOMB] = {5, 2, 1, 2, 0, 3, 0, 2};
static const int KT[NCOMB] = {5, 3, 3, 2, 3, 0, 0, 1};
static long fail_comb[NCOMB], tried_comb[NCOMB];
static int cmin[NCOMB][4], cmax[NCOMB][5];
static long n_scratch_checked = 0, n_brute_checked = 0;

static void leaf(int h3, int h8, int h11, int g) {
    int n = N;
    n_br++;
    P3 b = sub(X[n-1], X[n-2]), bp = sub(X[n-2], X[n-3]);
    P3 u1 = sub(X[1], X[0]), u2 = sub(X[2], X[1]);
    if (b.y != 1 || u1.y != 1 || u2.y != 1) die("a bridge whose last or first two bonds are not up-bonds");
    int bpup = (bp.y == 1);
    n_bpup += bpup;
    /* admissible c1: b' if it is an up-bond, else the two up-bonds out of the last bead */
    P3 cs[2]; int ncs = 0;
    if (bpup) cs[ncs++] = bp;
    else {
        int sgn = ((n-1) & 1) ? -1 : 1;
        for (int i = 0; i < 4; i++) if (sgn * AV[i][1] == 1) { P3 v = {sgn*AV[i][0], sgn*AV[i][1], sgn*AV[i][2]}; cs[ncs++] = v; }
        if (ncs != 2) die("not two up-bonds out of a site");
    }
    int cB[3];
    if (bottom_counts(occ, X, n, 3, cB) < 0) die("bottom linker site occupied");
    int botclean = (cB[0] == 0 && cB[1] == 0 && cB[2] == 0);
    for (int i = 0; i < 3; i++) if (cB[i] > maxB[i]) maxB[i] = cB[i];
    { int v = 9*cB[0] + 4*cB[1] + cB[2]; if (v > maxB[4]) maxB[4] = v; }
    int topclean = 0;
    int cA[2][3];
    for (int a = 0; a < ncs; a++) {
        if (top_counts(occ, X, n, cs[a], 3, cA[a]) < 0) die("top linker site occupied");
        for (int i = 0; i < 3; i++) if (cA[a][i] > maxA[i]) maxA[i] = cA[a][i];
        if (!bpup) maxA[3] = 1;
        { int v = 9*cA[a][0] + 4*cA[a][1] + cA[a][2] + (bpup ? 0 : 1); if (v > maxA[4]) maxA[4] = v; }
        if (cA[a][0] >= 1) n_d3++;
    }
    if (bpup && cA[0][0] == 0 && cA[0][1] == 0 && cA[0][2] == 0) topclean = 1;
    n_top += topclean; n_bot += botclean;
    int clean = topclean && botclean;
    n_clean += clean;
    record(h3, h8, h11, g, clean);
    if (clean && n <= NPAIR) {
        if (nstore == capstore) { capstore = capstore ? 2*capstore : 4096; store = realloc(store, capstore * sizeof(stored_t)); if (!store) die("memory"); }
        stored_t *s = &store[nstore++];
        s->n = n; s->hg[0] = h3; s->hg[1] = h8; s->hg[2] = h11; s->hg[3] = g;
        for (int i = 0; i < n; i++) { s->c[3*i] = (int8_t)X[i].x; s->c[3*i+1] = (int8_t)X[i].y; s->c[3*i+2] = (int8_t)X[i].z; }
    }
    if (n > NSCR) return;
    /* ---- from-scratch tests on the scratch grid ---- */
    {   /* the incremental (h,g) of the enumeration against the definition */
        int hg[4];
        if (place2(X, n)) die("enumerated walk is not a walk");
        if (!is_bridge(X, n)) die("enumerated walk is not a bridge");
        profile2(X, n, hg);
        if (hg[0] != h3 || hg[1] != h8 || hg[2] != h11 || hg[3] != g) die("incremental profile differs from the definition");
        int t2, b2; clean_flags(occ2, X, n, &t2, &b2);
        if (t2 != topclean || b2 != botclean) die("clean flags differ between the two grids");
        unplace2(X, n);
        n_scratch_checked++;
        if ((n_br & 1023) == 0) { int hb[4]; profile_brute(X, n, hb); if (hb[0]!=h3||hb[1]!=h8||hb[2]!=h11||hb[3]!=g) die("brute-force profile differs"); n_brute_checked++; }
    }
    for (int a = 0; a < ncs; a++) for (int cb = 0; cb < NCOMB; cb++) {
        int kh = KH[cb], kt = KT[cb];
        P3 Y[MAXB]; int m = 0;
        /* head: beads below the first bead, continuing the zigzag of the first two bonds backwards */
        P3 hs[8]; P3 p = X[0];
        for (int j = 1; j <= kh; j++) { p = sub(p, (j & 1) ? u2 : u1); hs[j-1] = p; }
        for (int j = kh; j >= 1; j--) Y[m++] = hs[j-1];
        for (int i = 0; i < n; i++) Y[m++] = X[i];
        p = X[n-1];
        for (int j = 1; j <= kt; j++) { p = add(p, (j & 1) ? cs[a] : b); Y[m++] = p; }
        tried_comb[cb]++;
        if (place2(Y, m)) die("extended walk is not a self-avoiding lattice walk");
        if (!is_bridge(Y, m)) die("extended walk is not a bridge");
        int t2, b2; clean_flags(occ2, Y, m, &t2, &b2);
        if (!(t2 && b2)) fail_comb[cb]++;
        int hg[4]; profile2(Y, m, hg);
        int d[4] = {hg[0]-h3, hg[1]-h8, hg[2]-h11, hg[3]-g};
        for (int i = 0; i < 4; i++) { if (d[i] < cmin[cb][i]) cmin[cb][i] = d[i]; if (d[i] > cmax[cb][i]) cmax[cb][i] = d[i]; }
        { int v = 9*d[0] + 4*d[1] + d[2] + d[3]; if (v > cmax[cb][4]) cmax[cb][4] = v; }
        if (kh >= 3 && kt >= 3) {   /* the cost must be the A-part plus the B-part plus [b' down] */
            if (d[0] != cA[a][0] + cB[0] || d[1] != cA[a][1] + cB[1] || d[2] != cA[a][2] + cB[2] || d[3] != (bpup ? 0 : 1))
                die("cost of head and tail is not A + B");
        }
        unplace2(Y, m);
    }
}

static void dfs(int k, int h3, int h8, int h11, int g, int maxy) {
    if (k == N) { if (X[N-1].y < maxy) return; leaf(h3, h8, h11, g); return; }
    if (X[k-1].y + (N - k) < maxy) return;             /* the last bead could no longer be highest */
    int sgn = ((k-1) & 1) ? -1 : 1;
    for (int bnd = 0; bnd < 4; bnd++) {
        P3 q = {X[k-1].x + sgn*AV[bnd][0], X[k-1].y + sgn*AV[bnd][1], X[k-1].z + sgn*AV[bnd][2]};
        if (q.y <= 0) continue;
        int id = IDX(q.x, q.y, q.z);
        if (occ[id]) continue;
        int c[3] = {0,0,0};
        for (int t = 0; t < 3; t++)
            for (int i = 0; i < nv[t]; i++) { int o = occ[id + voff[t][i]]; if (o && k - (o-1) >= 3) c[t]++; }
        int dg = 0;
        if (k >= 3) { int d = sq(q, X[k-3]); if (d == 11) dg = 1; else if (d != 19) die("bad 1-4 distance"); }
        occ[id] = (int16_t)(k + 1); X[k] = q;
        dfs(k + 1, h3 + c[0], h8 + c[1], h11 + c[2], g + dg, q.y > maxy ? q.y : maxy);
        occ[id] = 0;
    }
}

/* the 8 signed permutations of (x,z) that fix y */
static P3 gact(int gi, P3 v) {
    int sw = gi & 1, s1 = (gi & 2) ? -1 : 1, s2 = (gi & 4) ? -1 : 1;
    P3 r; r.y = v.y;
    if (!sw) { r.x = s1 * v.x; r.z = s2 * v.z; } else { r.x = s1 * v.z; r.z = s2 * v.x; }
    return r;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s NMAX NPAIR NSCR OUTDIR [part nparts]\n", argv[0]); return 1; }
    int NMAX = atoi(argv[1]); NPAIR = atoi(argv[2]); NSCR = atoi(argv[3]);
    const char *outdir = argv[4];
    int part = argc > 6 ? atoi(argv[5]) : 0, nparts = argc > 6 ? atoi(argv[6]) : 1;
    if (NMAX < 3 || NMAX > 24 || NPAIR > 24) die("sizes out of range");
    occ = calloc((size_t)DIM*DIM*DIM, sizeof(int16_t)); occ2 = calloc((size_t)DIM*DIM*DIM, sizeof(int16_t));
    tab = malloc(HSIZE * sizeof(cls_t));
    for (int dx = -3; dx <= 3; dx++) for (int dy = -3; dy <= 3; dy++) for (int dz = -3; dz <= 3; dz++) {
        int d2 = dx*dx + dy*dy + dz*dz, t = d2 == 3 ? 0 : d2 == 8 ? 1 : d2 == 11 ? 2 : -1;
        if (t < 0) continue;
        voff[t][nv[t]] = (dx*DIM + dy)*DIM + dz; vvec[t][nv[t]].x = dx; vvec[t][nv[t]].y = dy; vvec[t][nv[t]].z = dz; nv[t]++;
    }
    if (nv[0] != 8 || nv[1] != 12 || nv[2] != 24) die("vector counts");
    printf("# r9_semi NMAX=%d NPAIR=%d NSCR=%d part=%d/%d\n", NMAX, NPAIR, NSCR, part, nparts);
    printf("# combinations (head,tail): "); for (int cb = 0; cb < NCOMB; cb++) printf("(%d,%d) ", KH[cb], KT[cb]); printf("\n");
    for (N = 3; N <= NMAX; N++) {
        clock_t t0 = clock();
        memset(tab, 0, HSIZE * sizeof(cls_t));
        n_br = n_top = n_bot = n_clean = n_bpup = n_d3 = 0;
        memset(maxA, 0, sizeof maxA); memset(maxB, 0, sizeof maxB);
        memset(fail_comb, 0, sizeof fail_comb); memset(tried_comb, 0, sizeof tried_comb);
        memset(cmin, 0, sizeof cmin); memset(cmax, 0, sizeof cmax);
        X[0].x = 0; X[0].y = 0; X[0].z = 0; X[1].x = 1; X[1].y = 1; X[1].z = 1; X[2].x = 0; X[2].y = 2; X[2].z = 2;
        occ[IDX(0,0,0)] = 1; occ[IDX(1,1,1)] = 2; occ[IDX(0,2,2)] = 3;
        dfs(3, 0, 0, 0, 0, 2);
        occ[IDX(0,0,0)] = 0; occ[IDX(1,1,1)] = 0; occ[IDX(0,2,2)] = 0;
        long ncls = 0, ncls4 = 0, nclsc = 0, ncls4c = 0;
        char fn[512]; snprintf(fn, sizeof fn, "%s/r9_tab_N%d.txt", outdir, N);
        FILE *f = (part == 0) ? fopen(fn, "w") : NULL;
        for (int i = 0; i < HSIZE; i++) if (tab[i].used) {
            ncls++; ncls4 += __builtin_popcountll(tab[i].mall);
            if (tab[i].mclean) { nclsc++; ncls4c += __builtin_popcountll(tab[i].mclean); }
            if (f) fprintf(f, "%d %d %d %llx %llx\n", tab[i].h3, tab[i].h8, tab[i].h11, (unsigned long long)tab[i].mall, (unsigned long long)tab[i].mclean);
        }
        if (f) fclose(f);
        printf("N=%2d bridges=%ld bprime_up=%ld topclean=%ld botclean=%ld clean=%ld | classes h: all=%ld clean=%ld ; (h,g): all=%ld clean=%ld\n",
               N, n_br, n_bpup, n_top, n_bot, n_clean, ncls, nclsc, ncls4, ncls4c);
        printf("      A-part max (d3,d8,d11,dg | norm) = (%d,%d,%d,%d | %d), #(x,c1) with d3>=1: %ld ; B-part max = (%d,%d,%d | %d)\n",
               maxA[0], maxA[1], maxA[2], maxA[3], maxA[4], n_d3, maxB[0], maxB[1], maxB[2], maxB[4]);
        if (N <= NSCR) for (int cb = 0; cb < NCOMB; cb++)
            printf("      head %d tail %d: tried %ld, NOT clean %ld ; cost min (%d,%d,%d,%d) max (%d,%d,%d,%d | norm %d)\n",
                   KH[cb], KT[cb], tried_comb[cb], fail_comb[cb], cmin[cb][0], cmin[cb][1], cmin[cb][2], cmin[cb][3],
                   cmax[cb][0], cmax[cb][1], cmax[cb][2], cmax[cb][3], cmax[cb][4]);
        printf("      [%.1f s]\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
        fflush(stdout);
    }
    printf("# from-scratch profile checks: %ld ; O(n^2) brute-force checks: %ld\n", n_scratch_checked, n_brute_checked);
    /* ---------- (S1): real concatenations of all ordered pairs of stored clean bridges ---------- */
    printf("# stored clean bridges with at most %d beads: %ld\n", NPAIR, nstore);
    clock_t t0 = clock();
    long npairs = 0, nfail_walk = 0, nfail_bridge = 0, nfail_add = 0, nfail_clean = 0, nbrute = 0, nsym_bad = 0;
    P3 a0 = {1,1,1}, ma1 = {-1,1,1};
    for (long i = part; i < nstore; i += nparts) {
        stored_t *s1 = &store[i];
        P3 W[MAXB]; int n1 = s1->n;
        for (int k = 0; k < n1; k++) { W[k].x = s1->c[3*k]; W[k].y = s1->c[3*k+1]; W[k].z = s1->c[3*k+2]; }
        P3 b = sub(W[n1-1], W[n1-2]), bp = sub(W[n1-2], W[n1-3]);
        if (bp.y != 1) die("stored bridge is not top-clean");
        P3 c1 = bp;
        W[n1] = add(W[n1-1], c1); W[n1+1] = add(W[n1], b); W[n1+2] = add(W[n1+1], c1);
        P3 Q = add(W[n1+2], b);
        int gi = -1, ng = 0;
        for (int t = 0; t < 8; t++) { P3 r1 = gact(t, a0), r2 = gact(t, ma1); if (r1.x==c1.x && r1.y==c1.y && r1.z==c1.z && r2.x==b.x && r2.y==b.y && r2.z==b.z) { gi = t; ng++; } }
        if (ng != 1) { nsym_bad++; continue; }
        for (long j = 0; j < nstore; j++) {
            stored_t *s2 = &store[j];
            int n2 = s2->n, m = n1 + 3 + n2;
            for (int k = 0; k < n2; k++) { P3 v = {s2->c[3*k], s2->c[3*k+1], s2->c[3*k+2]}; W[n1+3+k] = add(Q, gact(gi, v)); }
            npairs++;
            if (place2(W, m)) { nfail_walk++; continue; }
            if (!is_bridge(W, m)) nfail_bridge++;
            int hg[4]; profile2(W, m, hg);
            if (hg[0] != s1->hg[0]+s2->hg[0] || hg[1] != s1->hg[1]+s2->hg[1] || hg[2] != s1->hg[2]+s2->hg[2] || hg[3] != s1->hg[3]+s2->hg[3]) nfail_add++;
            int tp, bt; clean_flags(occ2, W, m, &tp, &bt);
            if (!(tp && bt)) nfail_clean++;
            if ((npairs & 4095) == 0) { int hb[4]; profile_brute(W, m, hb); if (hb[0]!=hg[0]||hb[1]!=hg[1]||hb[2]!=hg[2]||hb[3]!=hg[3]) die("brute-force profile of a concatenation differs"); nbrute++; }
            unplace2(W, m);
        }
    }
    printf("(S1) part %d/%d: %ld ordered pairs of clean bridges (N1,N2 <= %d) concatenated from coordinates:\n", part, nparts, npairs, NPAIR);
    printf("     symmetry not unique: %ld ; not a self-avoiding lattice walk: %ld ; not a bridge: %ld ; (h,g) not exactly additive: %ld ; not clean: %ld\n",
           nsym_bad, nfail_walk, nfail_bridge, nfail_add, nfail_clean);
    printf("     O(n^2) brute-force profile checks on concatenations: %ld   [%.1f s]\n", nbrute, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
