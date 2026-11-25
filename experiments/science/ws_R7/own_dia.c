/* R7 OWN enumerator of the self-avoiding diamond-lattice chain ("dia" of P_REPORT section 0).
 *
 * Written from the model definition, NOT from the engineering division's dia_enum.c (which I have not
 * read at the time of writing):
 *   beads 0..N-1, N = n+3; bonds of length sqrt(3) along the four tetrahedral directions
 *     a0=( 1, 1, 1) a1=( 1,-1,-1) a2=(-1, 1,-1) a3=(-1,-1, 1),
 *   bond m is +a_{i_m} for even m and -a_{i_m} for odd m (two sublattices), i_{m+1} != i_m
 *   (tetrahedral bond angle); torsion j (bonds j, j+1, j+2) is trans iff i_{j+2} = i_j, gauche otherwise
 *   (two gauche states); self-avoiding;
 *   pairs (p,q), q-p >= 3; squared distances below the cutoff S_c = 12 are 3, 8, 11;
 *   class = (h3, h8, h11) = number of such pairs at squared distance 3, 8, 11;
 *   per class: number of conformations, fewest and most gauche torsions.
 * The first two bonds are fixed (+a0, -a1): 3^n torsion words.
 * Mirror reduction: the reflection (x,y,z)->(x,z,y) fixes a0,a1 and swaps a2<->a3, hence maps conformations
 * to conformations, preserves all distances and the number of gauche torsions, and swaps the two gauche
 * choices at the first gauche torsion; so only one of the two is enumerated, with weight 2.
 * (-m 0 switches the reduction off, for testing.)
 *
 * Prefix splitting for long runs: -k K -w W enumerates only the conformations whose first K torsion
 * choices (in the order trans, gaucheA, gaucheB; each 0..2) encode the base-3 number W (0 <= W < 3^K).
 *
 * Output: "h3 h8 h11 count gmin gmax" per class, sorted, preceded by '#' header lines.
 *
 *   cc -O3 -march=native -o own_dia own_dia.c
 *   ./own_dia -n 12
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXB 40
#define G 96                       /* grid side; coordinates offset by G/2 */
#define H3 64
#define H8 160
#define H11 160

static const int A[4][3] = {{1, 1, 1}, {1, -1, -1}, {-1, 1, -1}, {-1, -1, 1}};

static int8_t occ[G][G][G];        /* bead index + 1, 0 = empty */
static int off3[2][4][3], off8[12][3], off11[2][12][3];
static int n_tors, N, use_mirror = 1, split_k = 0;
static long split_w = 0;
static uint64_t *cnt;
static uint8_t *gmn, *gmx;
static uint64_t total = 0;

static inline size_t key(int h3, int h8, int h11) { return ((size_t)h3 * H8 + h8) * H11 + h11; }

static void build_offsets(void) {
    /* squared distance 3: the four bond vectors of the sublattice of the bead (parity = bead index & 1):
       bead q even -> its neighbours are q + a_i ; bead q odd -> q - a_i                                  */
    for (int par = 0; par < 2; par++)
        for (int i = 0; i < 4; i++)
            for (int c = 0; c < 3; c++) off3[par][i][c] = par ? -A[i][c] : A[i][c];
    /* squared distance 8: a_i - a_j, i != j (12 vectors; same for both sublattices) */
    int m = 0;
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            if (i != j) { for (int c = 0; c < 3; c++) off8[m][c] = A[i][c] - A[j][c]; m++; }
    /* squared distance 11: from an even bead: a_i - a_j + a_k with j != i, k != j, k != i (4*3*2/... ) */
    for (int par = 0; par < 2; par++) {
        int cntv = 0;
        int seen[64][3];
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++)
                for (int k = 0; k < 4; k++) {
                    if (j == i || k == j || k == i) continue;
                    int v[3];
                    for (int c = 0; c < 3; c++) v[c] = (par ? -1 : 1) * (A[i][c] - A[j][c] + A[k][c]);
                    int dup = 0;
                    for (int s = 0; s < cntv; s++)
                        if (seen[s][0] == v[0] && seen[s][1] == v[1] && seen[s][2] == v[2]) dup = 1;
                    if (!dup) { memcpy(seen[cntv], v, sizeof v); cntv++; }
                }
        if (cntv != 12) { fprintf(stderr, "offset table error %d\n", cntv); exit(2); }
        for (int s = 0; s < 12; s++) memcpy(off11[par][s], seen[s], sizeof seen[s]);
    }
}

/* number of beads with index <= q-3 at squared distances 3, 8, 11 from position (x,y,z) of bead q */
static inline void contacts(int q, int x, int y, int z, int *c3, int *c8, int *c11) {
    int lim = q - 3 + 1;                         /* stored value = index + 1 <= q - 2 */
    int par = q & 1, a = 0, b = 0, c = 0;
    for (int i = 0; i < 4; i++) {
        int v = occ[x + off3[par][i][0]][y + off3[par][i][1]][z + off3[par][i][2]];
        a += (v != 0 && v <= lim);
    }
    for (int i = 0; i < 12; i++) {
        int v = occ[x + off8[i][0]][y + off8[i][1]][z + off8[i][2]];
        b += (v != 0 && v <= lim);
    }
    for (int i = 0; i < 12; i++) {
        int v = occ[x + off11[par][i][0]][y + off11[par][i][1]][z + off11[par][i][2]];
        c += (v != 0 && v <= lim);
    }
    *c3 = a; *c8 = b; *c11 = c;
}

/* place bead q (q >= 3).  i1 = index of bond q-2 (two back), i2 = index of bond q-1 (previous bond);
   position of bead q-1 is (x,y,z).  g = gauche count so far, seen = a gauche torsion occurred, w = weight. */
static void extend(int q, int i1, int i2, int x, int y, int z, int h3, int h8, int h11, int g, int seen, uint64_t w,
                   long pref) {
    int sgn = ((q - 1) & 1) ? -1 : 1;            /* bond q-1 -> q is bond number q-1 (0-based): + for even */
    int t = q - 3;                                /* 0-based torsion index decided here */
    int choice = 0;
    for (int state = 0; state < 3; state++) {     /* 0 = trans (index i1), 1, 2 = the two gauche indices */
        int i3;
        if (state == 0) i3 = i1;
        else {
            /* the two indices different from i1 and i2, in increasing order */
            int found = 0; i3 = -1;
            for (int i = 0; i < 4; i++) {
                if (i == i1 || i == i2) continue;
                found++;
                if (found == state) { i3 = i; break; }
            }
        }
        choice = state;
        if (t < split_k) {                        /* prefix splitting: digit t of split_w (most significant first) */
            long p = 1;
            for (int s = 0; s < split_k - 1 - t; s++) p *= 3;
            if ((split_w / p) % 3 != choice) continue;
        }
        uint64_t w2 = w; int seen2 = seen, g2 = g;
        if (state != 0) {
            if (use_mirror && !seen) {
                if (state == 2) continue;
                w2 = 2 * w;
            }
            seen2 = 1; g2 = g + 1;
        }
        int nx = x + sgn * A[i3][0], ny = y + sgn * A[i3][1], nz = z + sgn * A[i3][2];
        if (occ[nx][ny][nz]) continue;            /* self-avoidance */
        int c3, c8, c11;
        contacts(q, nx, ny, nz, &c3, &c8, &c11);
        int k3 = h3 + c3, k8 = h8 + c8, k11 = h11 + c11;
        if (q == N - 1) {
            size_t kk = key(k3, k8, k11);
            cnt[kk] += w2;
            if (g2 < gmn[kk]) gmn[kk] = (uint8_t)g2;
            if (g2 > gmx[kk]) gmx[kk] = (uint8_t)g2;
            total += w2;
        } else {
            occ[nx][ny][nz] = (int8_t)(q + 1);
            extend(q + 1, i2, i3, nx, ny, nz, k3, k8, k11, g2, seen2, w2, pref);
            occ[nx][ny][nz] = 0;
        }
    }
}

int main(int argc, char **argv) {
    n_tors = 8;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n")) n_tors = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-m")) use_mirror = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-k")) split_k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-w")) split_w = atol(argv[++i]);
    }
    N = n_tors + 3;
    if (N > MAXB || N + 2 >= G / 2) { fprintf(stderr, "too long\n"); return 2; }
    build_offsets();
    size_t tab = (size_t)H3 * H8 * H11;
    cnt = calloc(tab, sizeof *cnt); gmn = malloc(tab); gmx = calloc(tab, 1);
    memset(gmn, 255, tab);
    int o = G / 2;
    /* beads 0,1,2: bond 0 = +a0, bond 1 = -a1 */
    int p0[3] = {o, o, o};
    int p1[3] = {o + A[0][0], o + A[0][1], o + A[0][2]};
    int p2[3] = {p1[0] - A[1][0], p1[1] - A[1][1], p1[2] - A[1][2]};
    occ[p0[0]][p0[1]][p0[2]] = 1; occ[p1[0]][p1[1]][p1[2]] = 2; occ[p2[0]][p2[1]][p2[2]] = 3;
    if (n_tors == 0) { printf("# trivial\n"); return 0; }
    extend(3, 0, 1, p2[0], p2[1], p2[2], 0, 0, 0, 0, 0, 1, 0);
    size_t ncl = 0;
    for (size_t k = 0; k < tab; k++) if (cnt[k]) ncl++;
    printf("# own_dia n_torsions=%d n_beads=%d s_cut=12 mirror=%d split_k=%d split_w=%ld\n", n_tors, N, use_mirror, split_k, split_w);
    printf("# conformations=%llu classes=%zu\n", (unsigned long long)total, ncl);
    printf("# columns: h3 h8 h11 count gmin gmax\n");
    for (int a = 0; a < H3; a++)
        for (int b = 0; b < H8; b++)
            for (int c = 0; c < H11; c++) {
                size_t kk = key(a, b, c);
                if (cnt[kk]) printf("%d %d %d %llu %d %d\n", a, b, c, (unsigned long long)cnt[kk], gmn[kk], gmx[kk]);
            }
    return 0;
}
