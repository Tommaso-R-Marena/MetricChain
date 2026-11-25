/* r2_enum.c — workstream R2 (SCI-REV-0002): own enumerator for diamond-lattice walks and bridges.
 *
 * Written from the definitions of theory report §11.22 ("Setting") BEFORE reading the authors'
 * or the engineering division's enumerators.
 *
 * Lattice: A = {(x,y,z) in (2Z)^3 : x+y+z = 0 mod 4}, B = A + (1,1,1).
 * Bond vectors a0=(1,1,1), a1=(1,-1,-1), a2=(-1,1,-1), a3=(-1,-1,1); an A site is bonded to
 * the sites +a_i, a B site to the sites -a_i.
 * Walk with N beads: injective sequence of sites, consecutive sites bonded.
 * Profile h = (h3,h8,h11): h_d = #{p<q : q-p >= 3, |x_q-x_p|^2 = d}.
 * g = #{i : |x_{i+3}-x_i|^2 = 11}  (gauche torsions).
 * Bridge: y(x_0) < y(x_i) for all i >= 1 and y(x_{N-1}) >= y(x_i) for all i.
 *
 * The first bead is the origin (an A site).  Walks: first bond +a0, second bond -a1 (all
 * walks are images of these under lattice symmetries; "conformations" = walks with the
 * first two bonds fixed, 3^n at most).  Bridges: the same two bonds (both are up-bonds).
 *
 * The pair counts are accumulated bead by bead straight from the definition: when bead q is
 * placed, every occupied site at squared distance d from it is a bead p < q; the beads q-1
 * (d=3) and q-2 (d=8) are excluded by index, not by a formula.
 *
 * usage: r2_enum walk|bridge N [dump]
 *   output (stdout): one line per class  "h3 h8 h11 count gmin count_gmin gmax gmask"
 *   gmask = bit mask (hex) of all gauche counts realised in the class.
 *   with a 4th argument "dump": instead print every walk as "h3 h8 h11 g  x0 y0 z0 x1 ..."
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define OFF 40
#define DIM 80
#define IDX(x,y,z) ((((x)+OFF)*DIM + ((y)+OFF))*DIM + ((z)+OFF))
#define MAXN 40

static const int A[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};

static int8_t occ[DIM*DIM*DIM];      /* 0 = empty, else bead index + 1 */
static int px[MAXN], py[MAXN], pz[MAXN];
static int N, bridge_mode, dump_mode;

/* all integer vectors of squared norm 3, 8, 11 (no lattice knowledge used) */
static int nv3, nv8, nv11;
static int v3[64], v8[64], v11[64];

/* class table: open addressing */
#define HSIZE (1<<16)
typedef struct { int used; int h3,h8,h11; uint64_t cnt[MAXN]; } cls_t;
static cls_t *tab;
static uint64_t total = 0;

static void record(int h3, int h8, int h11, int g) {
    uint32_t key = (uint32_t)(h3 + 64*(h8 + 256*h11));
    uint32_t i = (key * 2654435761u) & (HSIZE-1);
    while (tab[i].used && !(tab[i].h3==h3 && tab[i].h8==h8 && tab[i].h11==h11)) i = (i+1)&(HSIZE-1);
    if (!tab[i].used) { tab[i].used=1; tab[i].h3=h3; tab[i].h8=h8; tab[i].h11=h11; }
    tab[i].cnt[g]++;
    total++;
}

static void dfs(int k, int x, int y, int z, int lastbond, int h3, int h8, int h11, int g, int maxy) {
    /* bead k-1 is at (x,y,z); place bead k */
    if (k == N) {
        if (bridge_mode && y < maxy) return;
        if (dump_mode) {
            printf("%d %d %d %d ", h3,h8,h11,g);
            for (int i=0;i<N;i++) printf(" %d %d %d", px[i],py[i],pz[i]);
            printf("\n");
        }
        record(h3,h8,h11,g);
        return;
    }
    int sgn = ((k-1) & 1) ? -1 : 1;          /* bead k-1 on A (even index) -> +a_i */
    for (int b=0;b<4;b++) {
        if (b == lastbond) continue;           /* no immediate reversal */
        int nx = x + sgn*A[b][0], ny = y + sgn*A[b][1], nz = z + sgn*A[b][2];
        if (bridge_mode && ny <= 0) continue;  /* first bead strictly lowest */
        int id = IDX(nx,ny,nz);
        if (occ[id]) continue;
        /* pair counts of the new bead against all earlier beads, from the definition */
        int c3=0,c8=0,c11=0;
        for (int i=0;i<nv3;i++)  { int o=occ[id+v3[i]];  if (o && (k-(o-1))>=3) c3++; }
        for (int i=0;i<nv8;i++)  { int o=occ[id+v8[i]];  if (o && (k-(o-1))>=3) c8++; }
        for (int i=0;i<nv11;i++) { int o=occ[id+v11[i]]; if (o && (k-(o-1))>=3) c11++; }
        int dg = 0;
        if (k >= 3) {
            int dx=nx-px[k-3], dy=ny-py[k-3], dz=nz-pz[k-3];
            int d2=dx*dx+dy*dy+dz*dz;
            if (d2==11) dg=1; else if (d2!=19) { fprintf(stderr,"bad 1-4 distance %d\n",d2); exit(1); }
        }
        occ[id] = (int8_t)(k+1); px[k]=nx; py[k]=ny; pz[k]=nz;
        dfs(k+1, nx,ny,nz, b, h3+c3, h8+c8, h11+c11, g+dg, ny>maxy?ny:maxy);
        occ[id] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr,"usage: %s walk|bridge N [dump]\n", argv[0]); return 1; }
    bridge_mode = !strcmp(argv[1],"bridge");
    N = atoi(argv[2]);
    dump_mode = (argc > 3);
    if (N < 3 || N >= MAXN-2) { fprintf(stderr,"N out of range\n"); return 1; }
    for (int dx=-3;dx<=3;dx++) for (int dy=-3;dy<=3;dy++) for (int dz=-3;dz<=3;dz++) {
        int d2=dx*dx+dy*dy+dz*dz; int o=(dx*DIM+dy)*DIM+dz;
        if (d2==3) v3[nv3++]=o; else if (d2==8) v8[nv8++]=o; else if (d2==11) v11[nv11++]=o;
    }
    tab = calloc(HSIZE, sizeof(cls_t));
    /* beads 0,1,2 fixed: origin, +a0, +a0-a1 */
    px[0]=0;py[0]=0;pz[0]=0; occ[IDX(0,0,0)]=1;
    px[1]=1;py[1]=1;pz[1]=1; occ[IDX(1,1,1)]=2;
    px[2]=0;py[2]=2;pz[2]=2; occ[IDX(0,2,2)]=3;
    /* bead 2 is on A, reached by bond index 1 from bead 1 (a B site) */
    dfs(3, 0,2,2, 1, 0,0,0,0, 2);
    if (!dump_mode) {
        long ncls=0;
        for (int i=0;i<HSIZE;i++) if (tab[i].used) {
            uint64_t c=0, mask=0; int gmin=-1,gmax=-1;
            for (int g=0;g<MAXN;g++) if (tab[i].cnt[g]) { c+=tab[i].cnt[g]; mask|=(1ull<<g); if(gmin<0)gmin=g; gmax=g; }
            printf("%d %d %d %llu %d %llu %d %llx\n", tab[i].h3,tab[i].h8,tab[i].h11,
                   (unsigned long long)c, gmin, (unsigned long long)tab[i].cnt[gmin], gmax, (unsigned long long)mask);
            ncls++;
        }
        fprintf(stderr,"%s N=%d total=%llu classes=%ld\n", argv[1], N, (unsigned long long)total, ncls);
    }
    return 0;
}
