/* periodic.c -- workstream S: exhaustive search over PERIODIC site sets of the diamond lattice.
 *
 * A sites = fcc lattice with basis f1=(0,2,2), f2=(2,0,2), f3=(2,2,0); B = A + (1,1,1).
 * For every sublattice L' of index k of the fcc lattice (Hermite normal form) and every non-empty subset S of the
 * 2k sites of the cell in which every occupied site has at least `mindeg` occupied neighbours, compute per cell
 *   n = |S|,  E3 = 2 e3,  E8 = 2 e8,  E11 = 2 e11   (sums over occupied sites of occupied neighbours at d^2 = 3, 8, 11)
 * and mark the key (n, E3, E8, E11).  Densities: p3 = E3/(2n) - 1, p8 = E8/(2n) - 1, p11 = E11/(2n).
 *
 * usage:  periodic K mindeg                     -> list of all realised keys for index K
 *         periodic K mindeg n E3 E8 E11         -> print witnesses (HNF and site list) for that key
 * build:  gcc -O3 -march=native -o periodic periodic.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int F[3][3] = {{0,2,2},{2,0,2},{2,2,0}};
static int nb3[2][4][3];        /* neighbour of type t: other type, fcc offset */
static int nb8[12][3];
static int nb11[2][12][3];
static int hnf[3][3];
static int K;

static void init(void) {
    /* A(n) ~ B(n), B(n-e1), B(n-e2), B(n-e3);  B(m) ~ A(m), A(m+e1), A(m+e2), A(m+e3) */
    memset(nb3, 0, sizeof nb3);
    for (int i = 1; i < 4; i++) { nb3[0][i][i-1] = -1; nb3[1][i][i-1] = 1; }
    int c = 0;
    for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) for (int d = -1; d <= 1; d++) {
        int x = a*F[0][0]+b*F[1][0]+d*F[2][0], y = a*F[0][1]+b*F[1][1]+d*F[2][1], z = a*F[0][2]+b*F[1][2]+d*F[2][2];
        if (x*x+y*y+z*z == 8) { nb8[c][0]=a; nb8[c][1]=b; nb8[c][2]=d; c++; }
    }
    if (c != 12) { fprintf(stderr, "nb8 %d\n", c); exit(2); }
    for (int t = 0; t < 2; t++) {
        c = 0; int sg = t ? -1 : 1;
        for (int a = -3; a <= 3; a++) for (int b = -3; b <= 3; b++) for (int d = -3; d <= 3; d++) {
            int x = a*F[0][0]+b*F[1][0]+d*F[2][0] + sg, y = a*F[0][1]+b*F[1][1]+d*F[2][1] + sg, z = a*F[0][2]+b*F[1][2]+d*F[2][2] + sg;
            if (x*x+y*y+z*z == 11) { nb11[t][c][0]=a; nb11[t][c][1]=b; nb11[t][c][2]=d; c++; }
        }
        if (c != 12) { fprintf(stderr, "nb11 %d\n", c); exit(2); }
    }
}

static inline int fdiv(int a, int b) { int q = a / b; if ((a % b) && ((a < 0) != (b < 0))) q--; return q; }

static int coset(int n1, int n2, int n3) {
    int q = fdiv(n1, hnf[0][0]); n1 -= q*hnf[0][0]; n2 -= q*hnf[0][1]; n3 -= q*hnf[0][2];
    q = fdiv(n2, hnf[1][1]); n2 -= q*hnf[1][1]; n3 -= q*hnf[1][2];
    q = fdiv(n3, hnf[2][2]); n3 -= q*hnf[2][2];
    return (n1*hnf[1][1] + n2)*hnf[2][2] + n3;
}

#define MAXS 26
static uint32_t m3[MAXS][4], m8[MAXS][12], m11[MAXS][12];   /* one mask per neighbour (handles multiplicities) */
static int nsite;

static void build_masks(void) {
    nsite = 2*K;
    for (int i = 0; i < hnf[0][0]; i++) for (int j = 0; j < hnf[1][1]; j++) for (int l = 0; l < hnf[2][2]; l++) {
        int c = (i*hnf[1][1] + j)*hnf[2][2] + l;
        for (int t = 0; t < 2; t++) {
            int s = c + t*K;
            for (int q = 0; q < 4; q++)
                m3[s][q] = 1u << (coset(i+nb3[t][q][0], j+nb3[t][q][1], l+nb3[t][q][2]) + (1-t)*K);
            for (int q = 0; q < 12; q++)
                m8[s][q] = 1u << (coset(i+nb8[q][0], j+nb8[q][1], l+nb8[q][2]) + t*K);
            for (int q = 0; q < 12; q++)
                m11[s][q] = 1u << (coset(i+nb11[t][q][0], j+nb11[t][q][1], l+nb11[t][q][2]) + (1-t)*K);
        }
    }
}

#define NMAX 27
#define D3 (4*NMAX)
#define D8 (12*NMAX)
static uint8_t *seen;      /* bitset over (n, E3, E8, E11) */
static inline uint64_t keyidx(int n, int e3, int e8, int e11) { return (((uint64_t)n*D3 + e3)*D8 + e8)*D8 + e11; }

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
    K = atoi(argv[1]); int mindeg = atoi(argv[2]);
    int want = argc >= 7, wn = 0, w3 = 0, w8 = 0, w11 = 0, shown = 0;
    if (want) { wn = atoi(argv[3]); w3 = atoi(argv[4]); w8 = atoi(argv[5]); w11 = atoi(argv[6]); }
    if (2*K > MAXS) return 1;
    init();
    uint64_t nbits = (uint64_t)NMAX*D3*D8*D8;
    seen = calloc(nbits/8 + 1, 1);
    long nsub = 0;
    for (int a = 1; a <= K; a++) if (K % a == 0) for (int d = 1; d <= K/a; d++) if ((K/a) % d == 0) {
        int f = K/a/d;
        for (int b = 0; b < d; b++) for (int c = 0; c < f; c++) for (int e = 0; e < f; e++) {
            hnf[0][0]=a; hnf[0][1]=b; hnf[0][2]=c; hnf[1][0]=0; hnf[1][1]=d; hnf[1][2]=e; hnf[2][0]=0; hnf[2][1]=0; hnf[2][2]=f;
            build_masks(); nsub++;
            uint32_t full = (nsite == 32) ? 0xffffffffu : ((1u << nsite) - 1);
            for (uint32_t S = 1; S <= full; S++) {
                if (!(S & 1) && !(S & (1u << K))) continue;      /* translation: site A(0) or B(0) occupied */
                int n = 0, e3 = 0, e8 = 0, e11 = 0, ok = 1;
                uint32_t T = S;
                while (T) {
                    int s = __builtin_ctz(T); T &= T - 1; n++;
                    int d3 = 0;
                    for (int q = 0; q < 4; q++) d3 += (S & m3[s][q]) != 0;
                    if (d3 < mindeg) { ok = 0; break; }
                    e3 += d3;
                    for (int q = 0; q < 12; q++) { e8 += (S & m8[s][q]) != 0; e11 += (S & m11[s][q]) != 0; }
                }
                if (!ok) continue;
                if (want) {
                    if (n == wn && e3 == w3 && e8 == w8 && e11 == w11 && shown < 3) {
                        shown++;
                        printf("witness: hnf rows (%d %d %d) (0 %d %d) (0 0 %d)  sites:", a, b, c, d, e, f);
                        for (int i = 0; i < hnf[0][0]; i++) for (int j = 0; j < hnf[1][1]; j++) for (int l = 0; l < hnf[2][2]; l++)
                            for (int t = 0; t < 2; t++) {
                                int s = (i*hnf[1][1] + j)*hnf[2][2] + l + t*K;
                                if (S & (1u << s)) printf(" %c(%d,%d,%d)", t ? 'B' : 'A', i, j, l);
                            }
                        printf("\n");
                    }
                } else {
                    uint64_t k = keyidx(n, e3, e8, e11);
                    seen[k >> 3] |= 1 << (k & 7);
                }
            }
        }
    }
    if (!want) {
        printf("# periodic index=%d mindeg=%d sublattices=%ld ; columns: n E3 E8 E11 (per cell, doubled pair counts)\n", K, mindeg, nsub);
        for (int n = 1; n < NMAX; n++) for (int e3 = 0; e3 < D3; e3++) for (int e8 = 0; e8 < D8; e8++) for (int e11 = 0; e11 < D8; e11++) {
            uint64_t k = keyidx(n, e3, e8, e11);
            if (seen[k >> 3] & (1 << (k & 7))) printf("%d %d %d %d\n", n, e3, e8, e11);
        }
    }
    return 0;
}
