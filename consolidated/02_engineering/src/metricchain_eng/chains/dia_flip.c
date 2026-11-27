/*
 * dia_flip.c -- single-flip constants of the profile distance on self-avoiding diamond-lattice
 *               chains, and the exact test whether they form a valid torsion-Hamming envelope.
 *
 * MetricChain, Computational Research Division (THY-REQ-0002, question 3(b)).
 * Chain model, geometry and tables are those of dia_enum.c (same source text).
 *
 * Mode A (default): for every torsion j
 *     c_j = max ||N^x - N^x'||_1  over pairs of self-avoiding conformations x, x' whose torsion
 *           words differ in position j only
 *   ("single-flip constants", P_REPORT section 3.3), together with the number of single flips
 *   that stay inside / leave the self-avoiding domain.
 *
 * Mode B (-c c_0,...,c_{n-1} -D Dmax): is  ||N^x - N^y||_1 <= sum_{j : x_j != y_j} c_j  for ALL pairs
 *   of self-avoiding conformations?  A pair differing exactly on a set T of torsions can violate
 *   the inequality only if sum_{j in T} c_j < Dmax, Dmax = largest profile distance between two
 *   conformations (computed from the class table).  The program lists these sets T (|T| >= 2;
 *   single flips satisfy the inequality by the definition of c) and checks, for every conformation
 *   x and every assignment of other states on T, the conformation y obtained from x -- so the test
 *   is exhaustive over all pairs, not a sample.
 *
 * Usage:  dia_flip -n N [-s S_C] [-k K -W W -w w] [-c c_0,..,c_{n-1} -D Dmax]
 * Build:  cc -O3 -o dia_flip dia_flip.c
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

static int n_tors, n_beads, s_cut = 12;
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


static int st[MAXBEADS];                       /* torsion states: 0 t, 1 g+, 2 g- */
static int hist_prefix[MAXBEADS + 1][MAXDIST]; /* pair counts among beads 0..q-1 */
static int next_idx[2][4][4][3];               /* [parity of bond m][i_{m-2}][i_{m-1}][state] -> i_m */
static int width[MAXDIST];                     /* cell widths s_{k+1} - s_k, last one up to s_cut */

#define MAXT 40
static long long cmax[MAXT];
static unsigned long long flips_in[MAXT], flips_out[MAXT];
static unsigned long long n_conf = 0;

/* mode B */
static int modeB = 0;
static long long cvec[MAXT], dmax_all = 0;
#define MAXSETS 200000
static uint64_t set_mask[MAXSETS];
static long long set_budget[MAXSETS];
static int n_sets = 0;
static unsigned long long pairs_checked = 0, pairs_violating = 0;
static long long worst_excess = -(1LL << 60);
static uint64_t worst_mask = 0;

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


static inline long long l1(const int *h, const int *g) {
    long long s = 0;
    int ch = 0, cg = 0;
    for (int d = 0; d < n_dist; d++) {
        ch += h[d]; cg += g[d];
        s += (long long)width[d] * (ch > cg ? ch - cg : cg - ch);
    }
    return s;
}

static void build_next(void) {
    for (int par = 0; par < 2; par++)
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++) {
                for (int s = 0; s < 3; s++) next_idx[par][i][j][s] = -1;
                if (i == j) continue;
                next_idx[par][i][j][0] = i;                        /* trans: same direction index */
                int sgn = par ? 1 : -1;                            /* s_{m-2} s_{m-1} s_m = (-1)^{m+1} */
                for (int t = 0; t < 4; t++) {
                    if (t == i || t == j) continue;
                    const int *u = A[i], *v = A[j], *w = A[t];
                    int cx = v[1] * w[2] - v[2] * w[1];
                    int cy = v[2] * w[0] - v[0] * w[2];
                    int cz = v[0] * w[1] - v[1] * w[0];
                    int triple = sgn * (u[0] * cx + u[1] * cy + u[2] * cz);
                    next_idx[par][i][j][triple > 0 ? 1 : 2] = t;
                }
            }
}

/*
 * Build the conformation whose torsion word is st2 (equal to st before position j0) on top of
 * beads 0..j0+2 of the current conformation.  Returns 1 and its pair counts if it is self-avoiding.
 */
static int build_variant(int j0, const int *st2, int *h) {
    int pos2[MAXBEADS][3], idx2[MAXBEADS];
    int first = j0 + 3, ok = 1, q;
    for (q = first; q < n_beads; q++) occ[lin(pos[q][0], pos[q][1], pos[q][2])] = 0;
    for (int d = 0; d < n_dist; d++) h[d] = hist_prefix[first][d];
    idx2[j0] = idx[j0]; idx2[j0 + 1] = idx[j0 + 1];
    for (int c = 0; c < 3; c++) pos2[first - 1][c] = pos[first - 1][c];
    for (q = first; q < n_beads; q++) {
        int m = q - 1, jt = m - 2;
        int choice = next_idx[m & 1][idx2[m - 2]][idx2[m - 1]][st2[jt]];
        int sign = (m % 2 == 0) ? 1 : -1;
        int x = pos2[q - 1][0] + sign * A[choice][0];
        int y = pos2[q - 1][1] + sign * A[choice][1];
        int z = pos2[q - 1][2] + sign * A[choice][2];
        int base = lin(x, y, z);
        if (occ[base]) { ok = 0; break; }
        const int *offs = disp_off[q % 2], *cls = disp_cls[q % 2];
        int nd = n_disp[q % 2];
        for (int e = 0; e < nd; e++) {
            int p1 = occ[base + offs[e]];
            if (p1 && q - (p1 - 1) >= 3) h[cls[e]]++;
        }
        occ[base] = (int8_t)(q + 1);
        pos2[q][0] = x; pos2[q][1] = y; pos2[q][2] = z;
        idx2[m] = choice;
    }
    for (int r = first; r < q; r++) occ[lin(pos2[r][0], pos2[r][1], pos2[r][2])] = 0;
    for (int r = first; r < n_beads; r++) occ[lin(pos[r][0], pos[r][1], pos[r][2])] = (int8_t)(r + 1);
    return ok;
}

static void leaf(const int *hist) {
    int st2[MAXBEADS], h[MAXDIST];
    n_conf++;
    if (!modeB) {
        for (int j = 0; j < n_tors; j++) {
            for (int t = 0; t < n_tors; t++) st2[t] = st[t];
            for (int alt = 0; alt < 3; alt++) {
                if (alt == st[j]) continue;
                st2[j] = alt;
                if (build_variant(j, st2, h)) {
                    long long d = l1(hist, h);
                    if (d > cmax[j]) cmax[j] = d;
                    flips_in[j]++;
                } else flips_out[j]++;
            }
        }
        return;
    }
    for (int s = 0; s < n_sets; s++) {
        uint64_t mask = set_mask[s];
        int members[MAXT], k = 0, j0 = -1;
        for (int j = 0; j < n_tors; j++)
            if ((mask >> j) & 1) { members[k++] = j; if (j0 < 0) j0 = j; }
        for (int combo = 0; combo < (1 << k); combo++) {       /* each member takes one of its two other states */
            for (int t = 0; t < n_tors; t++) st2[t] = st[t];
            for (int b = 0; b < k; b++) {
                int j = members[b];
                st2[j] = (st[j] + 1 + ((combo >> b) & 1)) % 3;
            }
            if (!build_variant(j0, st2, h)) continue;
            long long ex = l1(hist, h) - set_budget[s];
            pairs_checked++;
            if (ex > worst_excess) { worst_excess = ex; worst_mask = mask; }
            if (ex > 0) pairs_violating++;
        }
    }
}

static void extend(int q, const int *hist) {
    if (q == n_beads) { leaf(hist); return; }
    int m = q - 1, j = m - 2;
    if (j == split_k && split_W > 1) {
        uint64_t c = prefix_counter++;
        if (c % split_W != split_w) return;
    }
    int sign = (m % 2 == 0) ? 1 : -1;
    int par = q % 2;
    for (int state = 0; state < 3; state++) {
        int choice = next_idx[m & 1][idx[m - 2]][idx[m - 1]][state];
        int x = pos[q - 1][0] + sign * A[choice][0];
        int y = pos[q - 1][1] + sign * A[choice][1];
        int z = pos[q - 1][2] + sign * A[choice][2];
        int base = lin(x, y, z);
        if (occ[base]) continue;
        int *h2 = hist_prefix[q + 1];
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
        st[j] = state;
        extend(q + 1, h2);
        occ[base] = 0;
    }
}

static void list_sets(int from, uint64_t mask, long long sum, int size) {
    if (size >= 2) {
        if (n_sets >= MAXSETS) { fprintf(stderr, "too many sets\n"); exit(2); }
        set_mask[n_sets] = mask; set_budget[n_sets] = sum; n_sets++;
    }
    for (int j = from; j < n_tors; j++)
        if (sum + cvec[j] < dmax_all) list_sets(j + 1, mask | ((uint64_t)1 << j), sum + cvec[j], size + 1);
}

int main(int argc, char **argv) {
    const char *cstr = NULL;
    n_tors = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n") && i + 1 < argc) n_tors = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-s") && i + 1 < argc) s_cut = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-k") && i + 1 < argc) split_k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-W") && i + 1 < argc) split_W = strtoull(argv[++i], NULL, 10);
        else if (!strcmp(argv[i], "-w") && i + 1 < argc) split_w = strtoull(argv[++i], NULL, 10);
        else if (!strcmp(argv[i], "-c") && i + 1 < argc) cstr = argv[++i];
        else if (!strcmp(argv[i], "-D") && i + 1 < argc) dmax_all = atoll(argv[++i]);
        else { fprintf(stderr, "usage: dia_flip -n N [-s S_C] [-k K -W W -w w] [-c c0,..,c_{n-1} -D Dmax]\n"); return 2; }
    }
    if (n_tors < 1 || n_tors > MAXT - 4 || n_tors + 3 > MAXBEADS) { fprintf(stderr, "bad -n\n"); return 2; }
    if (s_cut < 4 || s_cut > 28) { fprintf(stderr, "cutoff must be in [4, 28]\n"); return 2; }
    if (split_W < 1 || split_w >= split_W || split_k < 0 || split_k >= n_tors) { fprintf(stderr, "bad split\n"); return 2; }
    n_beads = n_tors + 3;
    build_tables();
    build_next();
    for (int d = 0; d < n_dist; d++) width[d] = (d + 1 < n_dist ? dist_val[d + 1] : s_cut) - dist_val[d];
    if (cstr) {
        modeB = 1;
        char *buf = strdup(cstr), *tok = strtok(buf, ",");
        int k = 0;
        while (tok && k < MAXT) { cvec[k++] = atoll(tok); tok = strtok(NULL, ","); }
        if (k != n_tors || dmax_all <= 0) { fprintf(stderr, "mode B needs n constants and -D Dmax\n"); return 2; }
        list_sets(0, 0, 0, 0);
    }
    occ = calloc((size_t)GRID * GRID * GRID, 1);
    if (!occ) { fprintf(stderr, "out of memory\n"); return 2; }
    idx[0] = 0; idx[1] = 1;
    pos[0][0] = pos[0][1] = pos[0][2] = 0;
    for (int c = 0; c < 3; c++) pos[1][c] = pos[0][c] + A[0][c];
    for (int c = 0; c < 3; c++) pos[2][c] = pos[1][c] - A[1][c];
    for (int q = 0; q < 3; q++) occ[lin(pos[q][0], pos[q][1], pos[q][2])] = (int8_t)(q + 1);
    memset(hist_prefix, 0, sizeof hist_prefix);
    extend(3, hist_prefix[3]);

    printf("# dia_flip n_torsions=%d n_beads=%d s_cut=%d mode=%s split_k=%d split_W=%llu split_w=%llu\n",
           n_tors, n_beads, s_cut, modeB ? "B" : "A", split_k,
           (unsigned long long)split_W, (unsigned long long)split_w);
    printf("# conformations=%llu\n", n_conf);
    if (!modeB) {
        printf("# columns: torsion | c_sf (max ||N^x - N^x'||_1 over single flips) | flips inside the domain | flips leaving it\n");
        for (int j = 0; j < n_tors; j++)
            printf("%d %lld %llu %llu\n", j, cmax[j], flips_in[j], flips_out[j]);
    } else {
        printf("# sets=%d pairs_checked=%llu pairs_violating=%llu worst_excess=%lld worst_mask=%llu\n",
               n_sets, pairs_checked, pairs_violating, pairs_checked ? worst_excess : 0,
               (unsigned long long)worst_mask);
    }
    return 0;
}
