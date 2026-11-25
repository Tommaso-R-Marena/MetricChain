/* enum.c -- workstream S: own enumerator of self-avoiding chains on the diamond lattice.
 *
 * Sites: A = {(x,y,z) all even, x+y+z = 0 mod 4},  B = A + (1,1,1).
 * Bonds: from an A site +a_i, from a B site -a_i, a_0..a_3 = (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1).
 * Profile of a chain with N beads: h_d = #{(p,q): q-p >= 3, |x_q-x_p|^2 = d}, d = 3, 8, 11.
 * Gauche count: #{i : |x_{i+3}-x_i|^2 = 11}.
 *
 * modes
 *   walk    first bead at the origin (A), bonds 0,1 fixed to +a0, -a1 (all chains up to lattice symmetry;
 *           number of leaves = number of self-avoiding torsion words, as in the other division's tables)
 *   bridge  y-bridges: y(x_0) < y(x_i) for all i >= 1 and y(x_{N-1}) >= y(x_i) for all i;
 *           first bead at the origin, first bond +a0 (the other up-bond +a2 is the image under the
 *           rotation (x,z)->(-x,-z); bridges starting on B are images under a glide that preserves y)
 *   hsw     half-space walks: y(x_0) < y(x_i) for all i >= 1 (first bond +a0)
 *   arch    y(x_0) < y(x_i) for 0 < i < N-1 and y(x_{N-1}) = y(x_0) + 0 or... (not used)
 *
 * output: one line per class (h3 h8 h11): count gmin gmax gmask(hex, bit g set iff some chain of the class
 *         has g gauche torsions)
 *
 * build: gcc -O3 -march=native -o enum enum.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define G 80
#define OFF 40
#define MAXN 40
#define HB 20
#define HS (1u << HB)

static const int Avec[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};
static int N, mode;                 /* mode 0 walk, 1 bridge, 2 hsw */
static int8_t occ[G*G*G];
static int px[MAXN], py[MAXN], pz[MAXN], bidx[MAXN];
static int noff[2], offl[2][32], offc[2][32];   /* neighbour offsets (linear) and distance class, per sublattice */
static int bondl[2][4];

typedef struct { uint32_t key; int used; uint64_t count; int gmin, gmax; uint64_t gmask; } Ent;
static Ent *tab;
static uint64_t nleaves = 0;

static inline int lin(int x, int y, int z) { return ((x+OFF)*G + (y+OFF))*G + (z+OFF); }

static void build(void) {
    for (int par = 0; par < 2; par++) {
        noff[par] = 0;
        int sg = par ? -1 : 1;
        for (int i = 0; i < 4; i++) bondl[par][i] = (sg*Avec[i][0]*G + sg*Avec[i][1])*G + sg*Avec[i][2];
        for (int x = -3; x <= 3; x++) for (int y = -3; y <= 3; y++) for (int z = -3; z <= 3; z++) {
            int s = x*x + y*y + z*z, c = -1;
            if (s == 3) c = 0; else if (s == 8) c = 1; else if (s == 11) c = 2; else continue;
            /* is (x,y,z) a displacement from a site of sublattice par to a lattice site? */
            int ok = 0;
            int ev = (x%2 == 0) && (y%2 == 0) && (z%2 == 0);
            int od = (abs(x)%2 == 1) && (abs(y)%2 == 1) && (abs(z)%2 == 1);
            int sm = (((x+y+z) % 4) + 4) % 4;
            if (ev && sm == 0) ok = 1;                      /* same sublattice */
            if (od && par == 0 && sm == 3) ok = 1;          /* A -> B */
            if (od && par == 1 && sm == 1) ok = 1;          /* B -> A */
            if (!ok) continue;
            offl[par][noff[par]] = (x*G + y)*G + z; offc[par][noff[par]] = c; noff[par]++;
        }
        if (noff[par] != 28) { fprintf(stderr, "neighbour table has %d entries\n", noff[par]); exit(2); }
    }
}

static inline void record(int h3, int h8, int h11, int g) {
    uint32_t key = (uint32_t)h3 | ((uint32_t)h8 << 10) | ((uint32_t)h11 << 20);
    uint32_t i = (key * 2654435761u) >> (32 - HB);
    for (;;) {
        Ent *e = &tab[i];
        if (!e->used) { e->used = 1; e->key = key; e->count = 1; e->gmin = e->gmax = g; e->gmask = 1ull << g; return; }
        if (e->key == key) { e->count++; if (g < e->gmin) e->gmin = g; if (g > e->gmax) e->gmax = g; e->gmask |= 1ull << g; return; }
        i = (i + 1) & (HS - 1);
    }
}

/* k = number of beads placed; bead k-1 at (px,py,pz)[k-1]; h = pair counts so far; g = gauche so far; ymax so far */
static void rec(int k, int h3, int h8, int h11, int g, int ymax) {
    if (k == N) {
        if (mode == 1 && py[k-1] < ymax) return;
        nleaves++;
        record(h3, h8, h11, g);
        return;
    }
    int par = (k - 1) & 1;              /* sublattice of bead k-1 (bead 0 on A) */
    int sg = par ? -1 : 1;
    int base = lin(px[k-1], py[k-1], pz[k-1]);
    for (int i = 0; i < 4; i++) {
        if (k >= 2 && i == bidx[k-2]) continue;
        int nl = base + bondl[par][i];
        if (occ[nl]) continue;
        int x = px[k-1] + sg*Avec[i][0], y = py[k-1] + sg*Avec[i][1], z = pz[k-1] + sg*Avec[i][2];
        if (mode >= 1) {
            if (y <= 0) continue;                               /* first bead strictly lowest */
            if (mode == 1) {                                    /* the last bead must be able to reach the top */
                int ym = ymax > y ? ymax : y;
                if (y + (N - 1 - k) < ym) continue;
            }
        }
        /* pairs of the new bead k with beads j <= k-3 */
        int d3 = 0, d8 = 0, d11 = 0;
        int npar = k & 1;
        for (int t = 0; t < 28; t++) {
            int o = occ[nl + offl[npar][t]];
            if (o && k - (o - 1) >= 3) { int c = offc[npar][t]; if (c == 0) d3++; else if (c == 1) d8++; else d11++; }
        }
        int dg = 0;
        if (k >= 3) {
            int dx = x - px[k-3], dy = y - py[k-3], dz = z - pz[k-3];
            if (dx*dx + dy*dy + dz*dz == 11) dg = 1;
        }
        px[k] = x; py[k] = y; pz[k] = z; bidx[k-1] = i; occ[nl] = (int8_t)(k + 1);
        rec(k + 1, h3 + d3, h8 + d8, h11 + d11, g + dg, ymax > y ? ymax : y);
        occ[nl] = 0;
    }
}

static int cmp(const void *a, const void *b) {
    uint32_t x = ((const Ent*)a)->key, y = ((const Ent*)b)->key;
    return x < y ? -1 : x > y;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: enum walk|bridge|hsw NBEADS\n"); return 1; }
    mode = !strcmp(argv[1], "walk") ? 0 : !strcmp(argv[1], "bridge") ? 1 : 2;
    N = atoi(argv[2]);
    if (N < 3 || N > 36) return 1;
    build();
    tab = calloc(HS, sizeof(Ent));
    memset(occ, 0, sizeof occ);
    px[0] = py[0] = pz[0] = 0; occ[lin(0,0,0)] = 1;
    px[1] = 1; py[1] = 1; pz[1] = 1; bidx[0] = 0; occ[lin(1,1,1)] = 2;
    if (mode == 0) {
        px[2] = 0; py[2] = 2; pz[2] = 2; bidx[1] = 1; occ[lin(0,2,2)] = 3;
        rec(3, 0, 0, 0, 0, 2);
    } else {
        rec(2, 0, 0, 0, 0, 1);
    }
    int nc = 0;
    Ent *out = malloc(sizeof(Ent) * 200000);
    for (uint32_t i = 0; i < HS; i++) if (tab[i].used) out[nc++] = tab[i];
    qsort(out, nc, sizeof(Ent), cmp);
    printf("# enum mode=%s n_beads=%d leaves=%llu classes=%d\n", argv[1], N, (unsigned long long)nleaves, nc);
    printf("# columns: h3 h8 h11 count gmin gmax gmask\n");
    for (int i = 0; i < nc; i++)
        printf("%u %u %u %llu %d %d %llx\n", out[i].key & 1023, (out[i].key >> 10) & 1023, out[i].key >> 20,
               (unsigned long long)out[i].count, out[i].gmin, out[i].gmax, (unsigned long long)out[i].gmask);
    return 0;
}
