/* r2_concat.c — workstream R2: exhaustive test of Lemma 11.68 (concatenation of bridges).
 *
 * For ALL ordered pairs (x1, x2) of bridges with 3 <= N1, N2 <= Nmax beads (canonical
 * representatives: first bead at the origin, first two bonds +a0, -a1; every bridge is the
 * image of one of these under a height-preserving lattice symmetry, and the construction is
 * equivariant) and for EVERY admissible choice of c1:
 *   P = last bead of x1, b = last bond, b' = bond before;  c1 = b' if b' is an up-bond,
 *   otherwise each of the up-bonds out of P;
 *   l1 = P+c1, l2 = l1+b, l3 = l2+c1, Q = l3+b;
 *   phi = height-preserving lattice symmetry with phi(x2_0) = Q, linear part (u1,u2) -> (c1,b)
 *         (searched among all 48 signed permutation matrices; the number found is recorded);
 *   x = x1, l1, l2, l3, phi(x2).
 * Checked from coordinates, with nothing taken from the lemma:
 *   every site is a lattice site, consecutive sites at squared distance 3, injective,
 *   N1+N2+3 beads, first bead strictly lowest, last bead highest;
 *   (h,g) by the O(N^2) definition;  delta = (h,g)(x) - (h,g)(x1) - (h,g)(x2);
 *   0<=d3<=1, 0<=d8<=9, 0<=d11<=14, dg = [b' is a down-bond].
 * Output: counts, the number of symmetries found (min/max), histogram of delta, maxima.
 *
 * usage: r2_concat Nmax [Nmax2]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXB 40
typedef struct { int n; int x[MAXB][3]; int h[4]; } walk_t;

static const int A[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};
static walk_t *br; static long nbr=0, capbr=0;
static int cur[MAXB][3], curbond[MAXB], Ntarget;

static int is_lattice(const int *s) {
    int x=s[0],y=s[1],z=s[2];
    if (((x&1)==0)&&((y&1)==0)&&((z&1)==0)) return (((x+y+z)%4)+4)%4==0 ? 1 : 0;   /* A */
    if ((x&1)&&(y&1)&&(z&1)) { int t=x+y+z-3; return ((t%4)+4)%4==0 ? 2 : 0; }      /* B */
    return 0;
}
static int d2(const int *a, const int *b) { int dx=a[0]-b[0],dy=a[1]-b[1],dz=a[2]-b[2]; return dx*dx+dy*dy+dz*dz; }

/* (h3,h8,h11,g) by definition; returns 0 if not a self-avoiding lattice walk */
static int measure(int n, int x[][3], int *h) {
    h[0]=h[1]=h[2]=h[3]=0;
    for (int i=0;i<n;i++) if (!is_lattice(x[i])) return 0;
    for (int i=0;i+1<n;i++) if (d2(x[i],x[i+1])!=3) return 0;
    for (int p=0;p<n;p++) for (int q=p+1;q<n;q++) {
        int d=d2(x[p],x[q]);
        if (d==0) return 0;
        if (q-p>=3) { if (d==3) h[0]++; else if (d==8) h[1]++; else if (d==11) h[2]++; }
        if (q-p==3) { if (d==11) h[3]++; else if (d!=19) return 0; }
    }
    return 1;
}
static int is_bridge(int n, int x[][3]) {
    for (int i=1;i<n;i++) if (x[i][1] <= x[0][1]) return 0;
    for (int i=0;i<n;i++) if (x[i][1] > x[n-1][1]) return 0;
    return 1;
}
static void store(void) {
    if (nbr==capbr) { capbr = capbr? 2*capbr : 1024; br = realloc(br, capbr*sizeof(walk_t)); }
    walk_t *w=&br[nbr++]; w->n=Ntarget; memcpy(w->x, cur, sizeof(int)*3*Ntarget);
    if (!measure(Ntarget, w->x, w->h) || !is_bridge(Ntarget,w->x)) { fprintf(stderr,"enumeration bug\n"); exit(1); }
}
static void gen(int k) {
    if (k==Ntarget) { int my=cur[0][1]; for(int i=0;i<k;i++) if(cur[i][1]>my) my=cur[i][1];
        if (cur[k-1][1]==my) store(); return; }
    int sgn = ((k-1)&1) ? -1 : 1;
    for (int b=0;b<4;b++) { if (b==curbond[k-1]) continue;
        int t[3]={cur[k-1][0]+sgn*A[b][0],cur[k-1][1]+sgn*A[b][1],cur[k-1][2]+sgn*A[b][2]};
        if (t[1]<=0) continue;
        int ok=1; for (int i=0;i<k;i++) if (cur[i][0]==t[0]&&cur[i][1]==t[1]&&cur[i][2]==t[2]) {ok=0;break;}
        if (!ok) continue;
        cur[k][0]=t[0];cur[k][1]=t[1];cur[k][2]=t[2]; curbond[k]=b; gen(k+1);
    }
}

static int G[48][3][3], nG=0;
static void make_group(void) {
    int perm[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    for (int p=0;p<6;p++) for (int s=0;s<8;s++) {
        int M[3][3]; memset(M,0,sizeof M);
        for (int i=0;i<3;i++) M[i][perm[p][i]] = ((s>>i)&1) ? -1 : 1;
        memcpy(G[nG++],M,sizeof M);
    }
}
static void apply(int M[3][3], const int *v, int *o) { for(int i=0;i<3;i++) o[i]=M[i][0]*v[0]+M[i][1]*v[1]+M[i][2]*v[2]; }

int main(int argc, char **argv) {
    int Nmax = argc>1 ? atoi(argv[1]) : 8;
    int Nmax2 = argc>2 ? atoi(argv[2]) : Nmax;
    make_group();
    long start[MAXB+1];
    int NN = Nmax>Nmax2?Nmax:Nmax2;
    for (int N=3;N<=NN;N++) {
        start[N]=nbr; Ntarget=N;
        cur[0][0]=0;cur[0][1]=0;cur[0][2]=0; cur[1][0]=1;cur[1][1]=1;cur[1][2]=1; cur[2][0]=0;cur[2][1]=2;cur[2][2]=2;
        curbond[0]=-1; curbond[1]=0; curbond[2]=1;
        if (N==3) { store(); } else gen(3);
        fprintf(stderr,"bridges N=%d: %ld\n", N, nbr-start[N]);
    }
    start[NN+1]=nbr;
    long npairs=0, nconc=0, nfail=0, nsym_min=99, nsym_max=0;
    long hist3[4]={0}, hist8[16]={0}, hist11[24]={0}, histg[3]={0};
    int mx[4]={0,0,0,0}; long bad_dg=0;
    /* largest norm 9d3+4d8+d11+dg observed */
    int maxnorm=0;
    static int x[2*MAXB+8][3];
    for (long i=0;i<start[Nmax+1];i++) {
        walk_t *w1=&br[i]; int n1=w1->n;
        int *P=w1->x[n1-1];
        int b[3], bp[3];
        for (int k=0;k<3;k++) { b[k]=P[k]-w1->x[n1-2][k]; bp[k]=w1->x[n1-2][k]-w1->x[n1-3][k]; }
        if (b[1]!=1) { fprintf(stderr,"last bond not up\n"); return 1; }
        int bp_down = (bp[1]==-1);
        /* admissible c1 */
        int c1s[2][3], nc=0;
        if (!bp_down) { memcpy(c1s[0],bp,sizeof bp); nc=1; }
        else {
            int latP=is_lattice(P); int sg = (latP==1)?1:-1;
            for (int a=0;a<4;a++) if (sg*A[a][1]==1) { for(int k=0;k<3;k++) c1s[nc][k]=sg*A[a][k]; nc++; }
            if (nc!=2) { fprintf(stderr,"expected two up-bonds\n"); return 1; }
        }
        for (long j=0;j<start[Nmax2+1];j++) {
            walk_t *w2=&br[j]; int n2=w2->n;
            int u1[3],u2[3];
            for (int k=0;k<3;k++) { u1[k]=w2->x[1][k]-w2->x[0][k]; u2[k]=w2->x[2][k]-w2->x[1][k]; }
            npairs++;
            for (int ci=0;ci<nc;ci++) {
                int *c1=c1s[ci];
                int n=0;
                for (int k=0;k<n1;k++) memcpy(x[n++],w1->x[k],sizeof(int)*3);
                int l1[3],l2[3],l3[3],Q[3];
                for (int k=0;k<3;k++) { l1[k]=P[k]+c1[k]; l2[k]=l1[k]+b[k]; l3[k]=l2[k]+c1[k]; Q[k]=l3[k]+b[k]; }
                memcpy(x[n++],l1,sizeof l1); memcpy(x[n++],l2,sizeof l2); memcpy(x[n++],l3,sizeof l3);
                /* the symmetry */
                int found=0, gi=-1;
                for (int g=0;g<48;g++) {
                    int ey[3]={0,1,0}, o[3]; apply(G[g],ey,o);
                    if (!(o[0]==0&&o[1]==1&&o[2]==0)) continue;     /* preserves the height order */
                    int o1[3],o2[3]; apply(G[g],u1,o1); apply(G[g],u2,o2);
                    if (o1[0]==c1[0]&&o1[1]==c1[1]&&o1[2]==c1[2]&&o2[0]==b[0]&&o2[1]==b[1]&&o2[2]==b[2]) { found++; gi=g; }
                }
                if (found<nsym_min) nsym_min=found;
                if (found>nsym_max) nsym_max=found;
                if (found!=1) { nfail++; continue; }
                for (int k=0;k<n2;k++) { int v[3]={w2->x[k][0]-w2->x[0][0],w2->x[k][1]-w2->x[0][1],w2->x[k][2]-w2->x[0][2]}, o[3];
                    apply(G[gi],v,o); x[n][0]=Q[0]+o[0]; x[n][1]=Q[1]+o[1]; x[n][2]=Q[2]+o[2]; n++; }
                int h[4];
                nconc++;
                if (n!=n1+n2+3 || !measure(n,x,h) || !is_bridge(n,x)) { nfail++;
                    if (nfail<5) fprintf(stderr,"FAIL: not a bridge / not a walk (i=%ld j=%ld)\n",i,j); continue; }
                int d[4]; for (int k=0;k<4;k++) d[k]=h[k]-w1->h[k]-w2->h[k];
                if (d[0]<0||d[0]>1||d[1]<0||d[1]>9||d[2]<0||d[2]>14||d[3]<0||d[3]>1) { nfail++;
                    if (nfail<5) fprintf(stderr,"FAIL: delta=(%d,%d,%d,%d) (i=%ld j=%ld)\n",d[0],d[1],d[2],d[3],i,j); continue; }
                if (d[3]!=bp_down) bad_dg++;
                hist3[d[0]]++; hist8[d[1]]++; hist11[d[2]]++; histg[d[3]]++;
                for (int k=0;k<4;k++) if (d[k]>mx[k]) mx[k]=d[k];
                int nm=9*d[0]+4*d[1]+d[2]+d[3]; if (nm>maxnorm) maxnorm=nm;
            }
        }
    }
    printf("bridges (canonical) with 3..%d beads: %ld; second factor 3..%d beads: %ld\n", Nmax, start[Nmax+1], Nmax2, start[Nmax2+1]);
    printf("ordered pairs: %ld; concatenations built (all admissible c1): %ld\n", npairs, nconc);
    printf("number of height-preserving symmetries with (u1,u2)->(c1,b): min %ld max %ld (lemma: exactly 1)\n", nsym_min, nsym_max);
    printf("failures (not a self-avoiding lattice bridge with N1+N2+3 beads, or delta outside [0,1]x[0,9]x[0,14]x{0,1}): %ld\n", nfail);
    printf("delta_g != [b' is a down-bond]: %ld\n", bad_dg);
    printf("observed maxima (d3,d8,d11,dg) = (%d,%d,%d,%d); largest norm 9d3+4d8+d11+dg = %d (beta=60)\n", mx[0],mx[1],mx[2],mx[3],maxnorm);
    printf("histogram d3:"); for(int k=0;k<2;k++) printf(" %d:%ld",k,hist3[k]); printf("\n");
    printf("histogram d8:"); for(int k=0;k<10;k++) printf(" %d:%ld",k,hist8[k]); printf("\n");
    printf("histogram d11:"); for(int k=0;k<15;k++) printf(" %d:%ld",k,hist11[k]); printf("\n");
    printf("histogram dg:"); for(int k=0;k<2;k++) printf(" %d:%ld",k,histg[k]); printf("\n");
    return nfail!=0;
}
