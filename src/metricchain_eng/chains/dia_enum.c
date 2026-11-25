/*
 * dia_enum.c -- exhaustive enumeration of self-avoiding rotamer chains on the diamond lattice.
 *
 * MetricChain, Computational Research Division.  Independent implementation of the chain model
 * of docs/workstreams/P_REPORT.md section 0 ("dia"), written from the definitions there (the
 * workstream's own scripts were never in the repository):
 *
 *   beads 0..N-1, N = n+3, n torsions with states t, g+, g- (180, +60, -60 degrees);
 *   tetrahedral bond angle, bond vectors (+-1,+-1,+-1): squared distances are integers
 *   (bonded 3, 1-3 pairs 8, 1-4 pairs 19 (t) / 11 (g));
 *   excluded volume = self-avoidance (no two beads on one lattice site);
 *   pairs  P = {(p,q) : q-p >= 3};  profile of a conformation = for every squared distance
 *   s < S_c the number of pairs of P at squared distance s.
 *
 * For every profile class (distinct vector of pair counts) the program reports
 *   count      number of conformations (all 3^n torsion words that are self-avoiding),
 *   gmin       smallest number of gauche torsions in the class,
 *   count_gmin number of conformations attaining gmin,
 *   gmax       largest number of gauche torsions in the class,
 * and, optionally, the bitmap of realised trans/gauche patterns (bit j = torsion j is gauche).
 *
 * Geometry.  Sublattice A = {even coordinates, x+y+z = 0 mod 4}, B = A + (1,1,1).  With
 * a_0..a_3 = (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), bond m is  +a_{i_m}  for even m and
 * -a_{i_m} for odd m, and i_{m+1} != i_m (no immediate reversal).  Torsion j is carried by
 * bonds j, j+1, j+2: trans iff i_{j+2} = i_j, otherwise gauche, the sign being the sign of the
 * triple product b_j . (b_{j+1} x b_{j+2}).  By lattice symmetry the first two bonds are fixed
 * (i_0 = 0, i_1 = 1); the remaining n bonds have three choices each: 3^n phantom chains.
 *
 * Mirror reduction.  A reflection maps g+ <-> g- at every torsion and preserves all distances,
 * so only chains whose first gauche torsion is g+ are generated, with weight 2 (the all-trans
 * chain has weight 1).  Disable with -m 0 to check the reduction.
 *
 * Parallel splitting.  With -k K -W W -w w only the subtrees below those depth-K prefixes whose
 * running index (in depth-first order, after the mirror reduction) is = w mod W are explored.
 * The union over w = 0..W-1 is the full enumeration; class tables are merged by adding counts
 * and taking min/max, bitmaps by OR.
 *
 * Usage:  dia_enum -n N_TORSIONS [-c S_C] [-m 0|1] [-k K -W W -w w] [-b bitmap_file]
 * Output: text on stdout (header lines start with '#', then one line per class).
 *
 * Build:  cc -O3 -march=native -o dia_enum dia_enum.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXBEADS 40
#define GRID 96          /* grid edge; coordinates lie in [-(N-1), N-1], displacements in [-5,5] */
#define OFF 48
#define MAXDIST 7        /* number of distinct squared distances below the cutoff */
#define KBITS 9          /* bits per pair count in a class key (counts < 512) */
#define MAXDISP 256
#define HBITS 20
#define HSIZE (1u << HBITS)

static const int A[4][3] = {{1, 1, 1}, {1, -1, -1}, {-1, 1, -1}, {-1, -1, 1}};

static int n_tors, n_beads, s_cut = 12, mirror = 1;
static int split_k = 0;
static uint64_t split_W = 1, split_w = 0, prefix_counter = 0;

static int n_dist;                       /* number of distance classes */
static int dist_val[MAXDIST];            /* their squared distances, ascending */
static int n_disp[2];                    /* displacement tables for A sites (0) and B sites (1) */
static int disp_off[2][MAXDISP];         /* linear grid offsets */
static int disp_cls[2][MAXDISP];         /* distance class of each displacement */

static int8_t *occ;                      /* grid: bead index + 1, or 0 */
static int pos[MAXBEADS][3];
static int idx[MAXBEADS];                /* bond direction indices */

typedef struct {
    uint64_t key;        /* packed pair counts, 0xffff.. = empty */
    uint64_t count;
    uint64_t count_gmin;
    int gmin, gmax;
} Entry;
static Entry *table;
static uint32_t n_classes = 0;

static uint8_t *bitmap = NULL;           /* realised trans/gauche patterns */
static uint64_t n_leaves_w = 0;          /* weighted number of conformations */

static inline int lin(int x, int y, int z) {
    return ((x + OFF) * GRID + (y + OFF)) * GRID + (z + OFF);
}

static int is_site(int x, int y, int z, int parity) {
    /* parity 0: sublattice A, parity 1: sublattice B */
    int s = ((x + y + z) % 4 + 4) % 4;
    if (parity == 0) return (x % 2 == 0) && (y % 2 == 0) && (z % 2 == 0) && s == 0;
    return (abs(x) % 2 == 1) && (abs(y) % 2 == 1) && (abs(z) % 2 == 1) && s == 3;
}

static void build_tables(void) {
    int seen[64];
    memset(seen, 0, sizeof seen);
    int R = 1;
    while (R * R < s_cut) R++;
    /* distance classes: squared lengths < s_cut of lattice displacements from either sublattice */
    for (int par = 0; par < 2; par++)
        for (int x = -R; x <= R; x++)
            for (int y = -R; y <= R; y++)
                for (int z = -R; z <= R; z++) {
                    int s = x * x + y * y + z * z;
                    if (s == 0 || s >= s_cut) continue;
                    /* from a site of sublattice `par` at the origin of that sublattice */
                    int ox = par, oy = par, oz = par; /* A origin (0,0,0), B origin (1,1,1) */
                    if (is_site(ox + x, oy + y, oz + z, 0) || is_site(ox + x, oy + y, oz + z, 1))
                        seen[s] = 1;
                }
    n_dist = 0;
    for (int s = 1; s < s_cut && s < 64; s++)
        if (seen[s]) {
            if (n_dist >= MAXDIST) { fprintf(stderr, "too many distance classes\n"); exit(2); }
            dist_val[n_dist++] = s;
        }
    for (int par = 0; par < 2; par++) {
        n_disp[par] = 0;
        int ox = par, oy = par, oz = par;
        for (int x = -R; x <= R; x++)
            for (int y = -R; y <= R; y++)
                for (int z = -R; z <= R; z++) {
                    int s = x * x + y * y + z * z;
                    if (s == 0 || s >= s_cut) continue;
                    if (!(is_site(ox + x, oy + y, oz + z, 0) || is_site(ox + x, oy + y, oz + z, 1)))
                        continue;
                    int c = -1;
                    for (int d = 0; d < n_dist; d++)
                        if (dist_val[d] == s) c = d;
                    if (n_disp[par] >= MAXDISP) { fprintf(stderr, "displacement table full\n"); exit(2); }
                    disp_off[par][n_disp[par]] = (x * GRID + y) * GRID + z;
                    disp_cls[par][n_disp[par]] = c;
                    n_disp[par]++;
                }
    }
}

static inline uint64_t pack(const int *h) {
    uint64_t k = 0;
    for (int d = 0; d < n_dist; d++) {
        if (h[d] >= (1 << KBITS)) { fprintf(stderr, "pair count overflow\n"); exit(2); }
        k = (k << KBITS) | (uint64_t)h[d];
    }
    return k;
}

static void record(const int *h, int g, uint64_t pattern, uint64_t w) {
    uint64_t key = pack(h);
    uint32_t i = (uint32_t)((key * 0x9E3779B97F4A7C15ull) >> (64 - HBITS));
    for (;;) {
        Entry *e = &table[i];
        if (e->key == key) {
            e->count += w;
            if (g < e->gmin) { e->gmin = g; e->count_gmin = w; }
            else if (g == e->gmin) e->count_gmin += w;
            if (g > e->gmax) e->gmax = g;
            break;
        }
        if (e->key == UINT64_MAX) {
            e->key = key; e->count = w; e->count_gmin = w; e->gmin = g; e->gmax = g;
            if (++n_classes > HSIZE / 2) { fprintf(stderr, "class table full\n"); exit(2); }
            break;
        }
        i = (i + 1) & (HSIZE - 1);
    }
    n_leaves_w += w;
    if (bitmap) bitmap[pattern >> 3] |= (uint8_t)(1u << (pattern & 7));
}

/*
 * Place bead q (q >= 3) and recurse.  State: beads 0..q-1 placed, hist = pair counts so far,
 * g = gauche count so far, pattern = gauche bits so far, seen_gauche = whether a gauche torsion
 * has occurred, w = weight (1 until the mirror reduction has been applied, then 2).
 */
static void extend(int q, const int *hist, int g, uint64_t pattern, int seen_gauche, uint64_t w) {
    if (q == n_beads) {
        record(hist, g, pattern, w);
        return;
    }
    int m = q - 1;                 /* index of the bond that ends at bead q */
    int j = m - 2;                 /* index of the torsion fixed by this bond */
    if (j == split_k && split_W > 1) {
        uint64_t c = prefix_counter++;
        if (c % split_W != split_w) return;
    }
    int sign = (m % 2 == 0) ? 1 : -1;
    int par = q % 2;               /* bead q is on sublattice A (even q) or B (odd q) */
    for (int choice = 0; choice < 4; choice++) {
        if (choice == idx[m - 1]) continue;
        int is_gauche = (choice != idx[m - 2]);
        uint64_t w2 = w;
        int seen2 = seen_gauche;
        if (is_gauche) {
            if (mirror && !seen_gauche) {
                /* chirality of the torsion: sign of b_{m-2} . (b_{m-1} x b_m) */
                int s2 = ((m - 2) % 2 == 0) ? 1 : -1, s1 = ((m - 1) % 2 == 0) ? 1 : -1;
                const int *u = A[idx[m - 2]], *v = A[idx[m - 1]], *t = A[choice];
                int cx = v[1] * t[2] - v[2] * t[1];
                int cy = v[2] * t[0] - v[0] * t[2];
                int cz = v[0] * t[1] - v[1] * t[0];
                int triple = s2 * s1 * sign * (u[0] * cx + u[1] * cy + u[2] * cz);
                if (triple < 0) continue;      /* keep g+ only; its mirror image is counted by weight */
                w2 = 2 * w;
            }
            seen2 = 1;
        }
        int x = pos[q - 1][0] + sign * A[choice][0];
        int y = pos[q - 1][1] + sign * A[choice][1];
        int z = pos[q - 1][2] + sign * A[choice][2];
        int base = lin(x, y, z);
        if (occ[base]) continue;               /* not self-avoiding */
        int h2[MAXDIST];
        for (int d = 0; d < n_dist; d++) h2[d] = hist[d];
        const int *offs = disp_off[par], *cls = disp_cls[par];
        int nd = n_disp[par];
        for (int e = 0; e < nd; e++) {
            int p1 = occ[base + offs[e]];
            if (p1 && q - (p1 - 1) >= 3) h2[cls[e]]++;
        }
        occ[base] = (int8_t)(q + 1);
        pos[q][0] = x; pos[q][1] = y; pos[q][2] = z;
        idx[m] = choice;
        extend(q + 1, h2, g + is_gauche, pattern | ((uint64_t)is_gauche << j), seen2, w2);
        occ[base] = 0;
    }
}

int main(int argc, char **argv) {
    const char *bitmap_path = NULL;
    n_tors = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n") && i + 1 < argc) n_tors = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-c") && i + 1 < argc) s_cut = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-m") && i + 1 < argc) mirror = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-k") && i + 1 < argc) split_k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-W") && i + 1 < argc) split_W = strtoull(argv[++i], NULL, 10);
        else if (!strcmp(argv[i], "-w") && i + 1 < argc) split_w = strtoull(argv[++i], NULL, 10);
        else if (!strcmp(argv[i], "-b") && i + 1 < argc) bitmap_path = argv[++i];
        else { fprintf(stderr, "usage: dia_enum -n N [-c S_C] [-m 0|1] [-k K -W W -w w] [-b file]\n"); return 2; }
    }
    if (n_tors < 1 || n_tors + 3 > MAXBEADS || n_tors + 3 + 6 > OFF) { fprintf(stderr, "bad -n\n"); return 2; }
    if (s_cut < 4 || s_cut > 28) { fprintf(stderr, "cutoff must be in [4, 28]\n"); return 2; }
    if (split_W < 1 || split_w >= split_W || split_k < 0 || split_k >= n_tors) { fprintf(stderr, "bad split\n"); return 2; }
    n_beads = n_tors + 3;
    build_tables();
    if (n_dist * KBITS > 63) { fprintf(stderr, "key overflow\n"); return 2; }

    occ = calloc((size_t)GRID * GRID * GRID, 1);
    table = malloc(sizeof(Entry) * HSIZE);
    if (!occ || !table) { fprintf(stderr, "out of memory\n"); return 2; }
    for (uint32_t i = 0; i < HSIZE; i++) table[i].key = UINT64_MAX;
    size_t bm_bytes = ((size_t)1 << n_tors) / 8 + 1;
    if (bitmap_path) {
        bitmap = calloc(bm_bytes, 1);
        if (!bitmap) { fprintf(stderr, "out of memory\n"); return 2; }
    }

    /* first three beads: bond 0 = +a_0, bond 1 = -a_1 */
    idx[0] = 0; idx[1] = 1;
    pos[0][0] = pos[0][1] = pos[0][2] = 0;
    for (int c = 0; c < 3; c++) pos[1][c] = pos[0][c] + A[0][c];
    for (int c = 0; c < 3; c++) pos[2][c] = pos[1][c] - A[1][c];
    for (int q = 0; q < 3; q++) occ[lin(pos[q][0], pos[q][1], pos[q][2])] = (int8_t)(q + 1);

    int hist0[MAXDIST];
    memset(hist0, 0, sizeof hist0);
    extend(3, hist0, 0, 0, 0, 1);

    printf("# dia_enum n_torsions=%d n_beads=%d s_cut=%d mirror=%d split_k=%d split_W=%llu split_w=%llu\n",
           n_tors, n_beads, s_cut, mirror, split_k, (unsigned long long)split_W, (unsigned long long)split_w);
    printf("# distances");
    for (int d = 0; d < n_dist; d++) printf(" %d", dist_val[d]);
    printf("\n# conformations=%llu classes=%u\n", (unsigned long long)n_leaves_w, n_classes);
    printf("# columns: pair counts at each distance | count | gmin | count_gmin | gmax\n");
    for (uint32_t i = 0; i < HSIZE; i++) {
        Entry *e = &table[i];
        if (e->key == UINT64_MAX) continue;
        for (int d = 0; d < n_dist; d++)
            printf("%d ", (int)((e->key >> (KBITS * (n_dist - 1 - d))) & ((1u << KBITS) - 1)));
        printf("%llu %d %llu %d\n", (unsigned long long)e->count, e->gmin,
               (unsigned long long)e->count_gmin, e->gmax);
    }
    if (bitmap_path) {
        FILE *f = fopen(bitmap_path, "wb");
        if (!f) { fprintf(stderr, "cannot write bitmap\n"); return 2; }
        fwrite(bitmap, 1, bm_bytes, f);
        fclose(f);
    }
    return 0;
}
