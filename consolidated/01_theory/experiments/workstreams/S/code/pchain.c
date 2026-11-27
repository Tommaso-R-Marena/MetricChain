/* pchain.c -- workstream S: exhaustive enumeration of PERIODIC CHAIN SYSTEMS on the diamond lattice.
 *
 * A chain system with period lattice L' (a sublattice of index K of the fcc lattice of A sites) is a set of
 * bonds, invariant under L', in which every site has degree 0 or 2 and every component is an INFINITE chain
 * (in the quotient: every cycle has a non-zero winding vector).  For each such system: per cell
 *   n = number of occupied sites, e3, e8, e11 = numbers of pairs of occupied sites at squared distance 3, 8, 11
 *   (pair orbits per cell; these depend on the site set only), g = number of gauche torsions (a path bond whose
 *   two flanking path bonds have different bond types).
 * Densities of the chain system: p3 = e3/n - 1, p8 = e8/n - 1, p11 = e11/n, gauche density g/n.
 *
 * usage:  pchain K                      -> all keys (n e3 e8 e11) with gmin, gmax  (over all sublattices of index K)
 *         pchain K PART NPARTS          -> the same for the sublattices number = PART mod NPARTS (to split long runs)
 *         pchain K n e3 e8 e11 g        -> up to 2 witnesses with these values (g = -1: any)
 * build:  gcc -O3 -march=native -o pchain pchain.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int F[3][3] = {{0,2,2},{2,0,2},{2,2,0}};
static int nb8[12][3], nb11[2][12][3];
static int hnf[3][3];
static int K;

static void init(void) {
    int c = 0;
    for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) for (int d = -1; d <= 1; d++) {
        int x = a*F[0][0]+b*F[1][0]+d*F[2][0], y = a*F[0][1]+b*F[1][1]+d*F[2][1], z = a*F[0][2]+b*F[1][2]+d*F[2][2];
        if (x*x+y*y+z*z == 8) { nb8[c][0]=a; nb8[c][1]=b; nb8[c][2]=d; c++; }
    }
    for (int t = 0; t < 2; t++) {
        c = 0; int sg = t ? -1 : 1;
        for (int a = -3; a <= 3; a++) for (int b = -3; b <= 3; b++) for (int d = -3; d <= 3; d++) {
            int x = a*F[0][0]+b*F[1][0]+d*F[2][0] + sg, y = a*F[0][1]+b*F[1][1]+d*F[2][1] + sg, z = a*F[0][2]+b*F[1][2]+d*F[2][2] + sg;
            if (x*x+y*y+z*z == 11) { nb11[t][c][0]=a; nb11[t][c][1]=b; nb11[t][c][2]=d; c++; }
        }
    }
}
static inline int fdiv(int a, int b) { int q = a / b; if ((a % b) && ((a < 0) != (b < 0))) q--; return q; }
/* reduce n to its coset representative; lam = n - rep */
static int reduce(int n1, int n2, int n3, int *lam) {
    int o1 = n1, o2 = n2, o3 = n3;
    int q = fdiv(n1, hnf[0][0]); n1 -= q*hnf[0][0]; n2 -= q*hnf[0][1]; n3 -= q*hnf[0][2];
    q = fdiv(n2, hnf[1][1]); n2 -= q*hnf[1][1]; n3 -= q*hnf[1][2];
    q = fdiv(n3, hnf[2][2]); n3 -= q*hnf[2][2];
    if (lam) { lam[0] = o1 - n1; lam[1] = o2 - n2; lam[2] = o3 - n3; }
    return (n1*hnf[1][1] + n2)*hnf[2][2] + n3;
}

#define MAXK 14
static int bidx[MAXK][4], wrap[MAXK][4][3];
static uint32_t m3[2*MAXK][4], m8[2*MAXK][12], m11[2*MAXK][12];
static int lastA[MAXK];
static int rep[MAXK][3];

static void build(void) {
    for (int i = 0; i < hnf[0][0]; i++) for (int j = 0; j < hnf[1][1]; j++) for (int l = 0; l < hnf[2][2]; l++) {
        int c = (i*hnf[1][1] + j)*hnf[2][2] + l;
        rep[c][0] = i; rep[c][1] = j; rep[c][2] = l;
        for (int q = 0; q < 4; q++) {
            int n[3] = {i, j, l};
            if (q) n[q-1] -= 1;                               /* A(n) ~ B(n - e_q), e_0 = 0 */
            bidx[c][q] = reduce(n[0], n[1], n[2], wrap[c][q]);
            m3[c][q] = 1u << (bidx[c][q] + K);
        }
        for (int q = 0; q < 12; q++) {
            m8[c][q] = 1u << reduce(i+nb8[q][0], j+nb8[q][1], l+nb8[q][2], NULL);
            m8[c+K][q] = m8[c][q] << K;
            m11[c][q] = 1u << (reduce(i+nb11[0][q][0], j+nb11[0][q][1], l+nb11[0][q][2], NULL) + K);
            m11[c+K][q] = 1u << reduce(i+nb11[1][q][0], j+nb11[1][q][1], l+nb11[1][q][2], NULL);
        }
    }
    for (int c = 0; c < K; c++) for (int q = 0; q < 4; q++) {
        /* B(m) ~ A(m + e_q): neighbours of B vertex b = bidx[c][q] include A vertex c */
        m3[bidx[c][q] + K][q] = 1u << c;
    }
    for (int b = 0; b < K; b++) lastA[b] = -1;
    for (int c = 0; c < K; c++) for (int q = 0; q < 4; q++) if (c > lastA[bidx[c][q]]) lastA[bidx[c][q]] = c;
}

#define NN 29
#define D3 (2*NN)
#define D8 (6*NN)
static uint8_t *gmn, *gmx;
static inline size_t kidx(int n, int e3, int e8, int e11) { return (((size_t)n*D3 + e3)*D8 + e8)*D8 + e11; }

static int choice[MAXK];            /* bitmask of chosen edges at A vertex c */
static int degB[MAXK], bedge[MAXK][2][2];
static int want = 0, wn, w3, w8, w11, wg, shown = 0;
static int part = 0, nparts = 1;
static unsigned long long nleaf = 0, nvalid = 0;
static const int PAIRS[6] = {3, 5, 6, 9, 10, 12};

static void leaf(void) {
    nleaf++;
    uint32_t S = 0; int n = 0;
    for (int c = 0; c < K; c++) if (choice[c]) { S |= 1u << c; n++; }
    for (int b = 0; b < K; b++) if (degB[b] == 2) { S |= 1u << (b + K); n++; }
    if (n == 0) return;
    /* cycles: all windings non-zero; gauche count */
    int vis[MAXK]; memset(vis, 0, sizeof vis);
    int g = 0;
    for (int c0 = 0; c0 < K; c0++) if (choice[c0] && !vis[c0]) {
        int w[3] = {0,0,0};
        int c = c0, e = __builtin_ctz(choice[c0]);          /* leave A vertex c by edge e */
        for (;;) {
            vis[c] = 1;
            int b = bidx[c][e];
            w[0] += wrap[c][e][0]; w[1] += wrap[c][e][1]; w[2] += wrap[c][e][2];
            /* at b: the other path edge */
            int k = (bedge[b][0][0] == c && bedge[b][0][1] == e) ? 1 : 0;
            int c2 = bedge[b][k][0], e2 = bedge[b][k][1];
            w[0] -= wrap[c2][e2][0]; w[1] -= wrap[c2][e2][1]; w[2] -= wrap[c2][e2][2];
            /* bond (c,e) is flanked at A by the other edge of c, at B by edge e2 */
            int eo = __builtin_ctz(choice[c] & ~(1 << e));
            if (eo != e2) g++;
            /* bond (c2,e2) is flanked at B by e, at A (c2) by the other edge of c2 */
            int e3_ = __builtin_ctz(choice[c2] & ~(1 << e2));
            if (e3_ != e) g++;
            c = c2; e = e3_;
            if (c == c0 && e == __builtin_ctz(choice[c0])) break;
        }
        if (w[0] == 0 && w[1] == 0 && w[2] == 0) return;     /* a finite ring */
    }
    int e3 = 0, e8 = 0, e11 = 0;
    uint32_t T = S;
    while (T) {
        int s = __builtin_ctz(T); T &= T - 1;
        for (int q = 0; q < 4; q++) e3 += (S & m3[s][q]) != 0;
        for (int q = 0; q < 12; q++) { e8 += (S & m8[s][q]) != 0; e11 += (S & m11[s][q]) != 0; }
    }
    e3 /= 2; e8 /= 2; e11 /= 2;
    nvalid++;
    if (want) {
        if (n == wn && e3 == w3 && e8 == w8 && e11 == w11 && (wg < 0 || g == wg) && shown < 2) {
            shown++;
            printf("witness g=%d: hnf rows (%d %d %d) (0 %d %d) (0 0 %d); path bonds A(n)-type:", g,
                   hnf[0][0], hnf[0][1], hnf[0][2], hnf[1][1], hnf[1][2], hnf[2][2]);
            for (int c = 0; c < K; c++) if (choice[c]) {
                int a = __builtin_ctz(choice[c]), b = __builtin_ctz(choice[c] & ~(1 << a));
                printf(" A(%d,%d,%d):a%d,a%d", rep[c][0], rep[c][1], rep[c][2], a, b);
            }
            printf("\n");
        }
        return;
    }
    size_t k = kidx(n, e3, e8, e11);
    if (gmn[k] == 255 || g < gmn[k]) gmn[k] = (uint8_t)g;
    if (gmx[k] == 255 || g > gmx[k]) gmx[k] = (uint8_t)g;
}

static void dfs(int c) {
    if (c == K) { leaf(); return; }
    for (int o = 0; o < 7; o++) {
        int ch = o ? PAIRS[o-1] : 0;
        int ok = 1, saved[4], ns = 0;
        for (int q = 0; q < 4 && ok; q++) if (ch & (1 << q)) {
            int b = bidx[c][q];
            if (degB[b] >= 2) { ok = 0; break; }
            bedge[b][degB[b]][0] = c; bedge[b][degB[b]][1] = q; degB[b]++; saved[ns++] = b;
        }
        if (ok) {
            for (int q = 0; q < 4; q++) { int b = bidx[c][q]; if (lastA[b] == c && degB[b] == 1) { ok = 0; break; } }
        }
        if (ok) { choice[c] = ch; dfs(c + 1); choice[c] = 0; }
        for (int i = 0; i < ns; i++) degB[saved[i]]--;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    K = atoi(argv[1]);
    if (K > MAXK) return 1;
    if (argc == 4) { part = atoi(argv[2]); nparts = atoi(argv[3]); }
    if (argc >= 7) { want = 1; wn = atoi(argv[2]); w3 = atoi(argv[3]); w8 = atoi(argv[4]); w11 = atoi(argv[5]); wg = atoi(argv[6]); }
    init();
    size_t tot = (size_t)NN*D3*D8*D8;
    if (!want) { gmn = malloc(tot); gmx = malloc(tot); memset(gmn, 255, tot); memset(gmx, 255, tot); }
    long nsub = 0;
    for (int a = 1; a <= K; a++) if (K % a == 0) for (int d = 1; d <= K/a; d++) if ((K/a) % d == 0) {
        int f = K/a/d;
        for (int b = 0; b < d; b++) for (int c = 0; c < f; c++) for (int e = 0; e < f; e++) {
            hnf[0][0]=a; hnf[0][1]=b; hnf[0][2]=c; hnf[1][0]=0; hnf[1][1]=d; hnf[1][2]=e; hnf[2][0]=0; hnf[2][1]=0; hnf[2][2]=f;
            nsub++;
            if ((nsub - 1) % nparts != part) continue;
            build();
            memset(degB, 0, sizeof degB); memset(choice, 0, sizeof choice);
            dfs(0);
        }
    }
    if (!want) {
        printf("# pchain index=%d sublattices=%ld leaves=%llu chain_systems=%llu ; columns: n e3 e8 e11 gmin gmax (per cell)\n", K, nsub, nleaf, nvalid);
        for (int n = 1; n < NN; n++) for (int e3 = 0; e3 < D3; e3++) for (int e8 = 0; e8 < D8; e8++) for (int e11 = 0; e11 < D8; e11++) {
            size_t k = kidx(n, e3, e8, e11);
            if (gmn[k] != 255) printf("%d %d %d %d %d %d\n", n, e3, e8, e11, gmn[k], gmx[k]);
        }
    }
    return 0;
}
