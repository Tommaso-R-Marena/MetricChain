/* R7 OWN: single-flip constants of the self-avoiding diamond-lattice chain,
 *     c_j = max || N^x - N^x' ||_1  over pairs of self-avoiding conformations x, x' that differ in torsion j only
 * (j = 1..n; "differ in torsion j only" = same word of torsion STATES t / g+ / g- except at position j, i.e. the tail
 * beyond torsion j is rotated rigidly).  Written from the definition (ENG-RES-0002 section 6 / P_REPORT section 3.3),
 * not from the engineering division's dia_flip.c, which I have not read.
 *
 * Brute force: every self-avoiding conformation is enumerated (no symmetry reduction); for every torsion position and
 * each of the two other states the tail is rebuilt, tested for self-avoidance and its contacts recounted.
 * States: 0 = trans (bond index two back is repeated); +1 / -1 = gauche, distinguished by the sign of the triple
 * product of the three consecutive bond vectors (a geometric, index-independent definition of g+ / g-).
 * Profile distance (cutoff 12; distances 3, 8, 11): 5|dC1| + 3|dC2| + |dC3|, C the cumulative pair counts.
 *
 *   cc -O3 -march=native -o own_flip own_flip.c ;  ./own_flip -n 12
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXB 40
#define G 96

static const int A[4][3] = {{1, 1, 1}, {1, -1, -1}, {-1, 1, -1}, {-1, -1, 1}};
static int8_t occ[G][G][G];
static int off3[2][4][3], off8[12][3], off11[2][12][3];
static int n_tors, N;
static int pos[MAXB][3], idx[MAXB], st[MAXB];      /* idx[m] = index of bond m (bead m -> m+1); st[t] = state of torsion t */
static int prof[MAXB][3];                          /* prof[q] = (h3,h8,h11) counting pairs whose larger index is <= q */
static long cmax[MAXB];
static uint64_t n_conf = 0, n_pairs = 0;

static void build_offsets(void) {
    for (int par = 0; par < 2; par++)
        for (int i = 0; i < 4; i++)
            for (int c = 0; c < 3; c++) off3[par][i][c] = par ? -A[i][c] : A[i][c];
    int m = 0;
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            if (i != j) { for (int c = 0; c < 3; c++) off8[m][c] = A[i][c] - A[j][c]; m++; }
    for (int par = 0; par < 2; par++) {
        int cnt = 0, seen[64][3];
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++)
                for (int k = 0; k < 4; k++) {
                    if (j == i || k == j || k == i) continue;
                    int v[3];
                    for (int c = 0; c < 3; c++) v[c] = (par ? -1 : 1) * (A[i][c] - A[j][c] + A[k][c]);
                    int dup = 0;
                    for (int s = 0; s < cnt; s++) if (seen[s][0] == v[0] && seen[s][1] == v[1] && seen[s][2] == v[2]) dup = 1;
                    if (!dup) { memcpy(seen[cnt], v, sizeof v); cnt++; }
                }
        for (int s = 0; s < 12; s++) memcpy(off11[par][s], seen[s], sizeof seen[s]);
    }
}

static inline void contacts(int q, const int *p, int *c) {
    int lim = q - 2, par = q & 1, a = 0, b = 0, d = 0;
    for (int i = 0; i < 4; i++) { int v = occ[p[0] + off3[par][i][0]][p[1] + off3[par][i][1]][p[2] + off3[par][i][2]]; a += (v != 0 && v <= lim); }
    for (int i = 0; i < 12; i++) { int v = occ[p[0] + off8[i][0]][p[1] + off8[i][1]][p[2] + off8[i][2]]; b += (v != 0 && v <= lim); }
    for (int i = 0; i < 12; i++) { int v = occ[p[0] + off11[par][i][0]][p[1] + off11[par][i][1]][p[2] + off11[par][i][2]]; d += (v != 0 && v <= lim); }
    c[0] = a; c[1] = b; c[2] = d;
}

/* bond vector of bond m with index i: + for even m, - for odd m */
static inline void bvec(int m, int i, int *v) { int s = (m & 1) ? -1 : 1; v[0] = s * A[i][0]; v[1] = s * A[i][1]; v[2] = s * A[i][2]; }

/* index of bond m+2 given the indices of bonds m and m+1 and the torsion state */
static int next_index(int m, int i1, int i2, int state) {
    if (state == 0) return i1;
    int b1[3], b2[3], b3[3];
    bvec(m, i1, b1); bvec(m + 1, i2, b2);
    for (int i = 0; i < 4; i++) {
        if (i == i1 || i == i2) continue;
        bvec(m + 2, i, b3);
        long det = (long)b1[0] * (b2[1] * b3[2] - b2[2] * b3[1]) - (long)b1[1] * (b2[0] * b3[2] - b2[2] * b3[0]) + (long)b1[2] * (b2[0] * b3[1] - b2[1] * b3[0]);
        if ((det > 0) == (state > 0)) return i;
    }
    return -1;
}

static void flips(void) {
    /* called with the complete conformation in pos/idx/st/prof and all beads on the grid */
    for (int t = 0; t < n_tors; t++) {
        int first = t + 3;                                   /* first bead that moves */
        for (int alt = -1; alt <= 1; alt++) {
            if (alt == st[t]) continue;
            /* remove the tail */
            for (int q = first; q < N; q++) occ[pos[q][0]][pos[q][1]][pos[q][2]] = 0;
            int np[MAXB][3], ni[MAXB], ok = 1, placed = first;
            int h[3] = {prof[first - 1][0], prof[first - 1][1], prof[first - 1][2]};
            int i1 = idx[t], i2 = idx[t + 1];
            int cur[3] = {pos[first - 1][0], pos[first - 1][1], pos[first - 1][2]};
            for (int q = first; q < N; q++) {
                int tt = q - 3;                              /* torsion deciding bond q-1 */
                int state = (tt == t) ? alt : st[tt];
                int i3 = next_index(q - 3, i1, i2, state);
                int v[3]; bvec(q - 1, i3, v);
                np[q][0] = cur[0] + v[0]; np[q][1] = cur[1] + v[1]; np[q][2] = cur[2] + v[2];
                if (occ[np[q][0]][np[q][1]][np[q][2]]) { ok = 0; break; }
                int c[3]; contacts(q, np[q], c);
                h[0] += c[0]; h[1] += c[1]; h[2] += c[2];
                occ[np[q][0]][np[q][1]][np[q][2]] = (int8_t)(q + 1);
                placed = q + 1;
                ni[q] = i3; i1 = i2; i2 = i3;
                cur[0] = np[q][0]; cur[1] = np[q][1]; cur[2] = np[q][2];
            }
            if (ok) {
                const int *g = prof[N - 1];
                long a1 = labs((long)h[0] - g[0]);
                long a2 = labs((long)(h[0] + h[1]) - (g[0] + g[1]));
                long a3 = labs((long)(h[0] + h[1] + h[2]) - (g[0] + g[1] + g[2]));
                long d = 5 * a1 + 3 * a2 + a3;
                if (d > cmax[t]) cmax[t] = d;
                n_pairs++;
            }
            for (int q = first; q < placed; q++) occ[np[q][0]][np[q][1]][np[q][2]] = 0;
            /* restore the tail */
            for (int q = first; q < N; q++) occ[pos[q][0]][pos[q][1]][pos[q][2]] = (int8_t)(q + 1);
            (void)ni;
        }
    }
}

static void extend(int q) {
    if (q == N) { n_conf++; flips(); return; }
    for (int state = -1; state <= 1; state++) {
        int i3 = next_index(q - 3, idx[q - 3], idx[q - 2], state);
        int v[3]; bvec(q - 1, i3, v);
        int p[3] = {pos[q - 1][0] + v[0], pos[q - 1][1] + v[1], pos[q - 1][2] + v[2]};
        if (occ[p[0]][p[1]][p[2]]) continue;
        int c[3]; contacts(q, p, c);
        pos[q][0] = p[0]; pos[q][1] = p[1]; pos[q][2] = p[2];
        idx[q - 1] = i3; st[q - 3] = state;
        prof[q][0] = prof[q - 1][0] + c[0]; prof[q][1] = prof[q - 1][1] + c[1]; prof[q][2] = prof[q - 1][2] + c[2];
        occ[p[0]][p[1]][p[2]] = (int8_t)(q + 1);
        extend(q + 1);
        occ[p[0]][p[1]][p[2]] = 0;
    }
}

int main(int argc, char **argv) {
    n_tors = 8;
    for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "-n")) n_tors = atoi(argv[++i]);
    N = n_tors + 3;
    build_offsets();
    int o = G / 2;
    pos[0][0] = o; pos[0][1] = o; pos[0][2] = o;
    for (int c = 0; c < 3; c++) pos[1][c] = pos[0][c] + A[0][c];
    for (int c = 0; c < 3; c++) pos[2][c] = pos[1][c] - A[1][c];
    idx[0] = 0; idx[1] = 1;
    for (int q = 0; q < 3; q++) { occ[pos[q][0]][pos[q][1]][pos[q][2]] = (int8_t)(q + 1); prof[q][0] = prof[q][1] = prof[q][2] = 0; }
    extend(3);
    printf("n=%d conformations=%llu valid single-flip ordered pairs=%llu\nc_sf:", n_tors, (unsigned long long)n_conf, (unsigned long long)n_pairs);
    for (int t = 0; t < n_tors; t++) printf(" %ld", cmax[t]);
    printf("\n");
    return 0;
}
