// dp.cpp -- referee's second, independent exact method (transfer-matrix DP per circular ordering)
// for the systems I(a,m,B): template G^B (A G^B)^{m-1} and items C^{a_i}.
//
// Fact used (and checked against the brute-force enumerator on small instances): every pair joins a
// template G with an item C, so in any non-crossing drawing the chords are pairwise nested; a
// structure is a chain of chords (i_1,j_1),...,(i_K,j_K) with template positions decreasing and
// item-circle positions increasing; faces are the regions between consecutive chords plus the
// innermost and the outermost face.
//
// For every circular ordering (template first, items in every order; orderings that differ by a
// permutation of equal items are computed once and weighted by prod mu_s!), and for several
// loop-energy models, computes: number of connected structures, minimum energy, number of
// minimum-energy structures.  Counts are labelled (strands distinguishable).
//
// usage: dp m B a_1 ... a_n
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;
typedef long long ll;

static string u128s(u128 x) { if (x == 0) return "0"; string s; while (x) { s += char('0' + (int)(x % 10)); x /= 10; } reverse(s.begin(), s.end()); return s; }
static inline unsigned long long mix(unsigned long long x) { x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL; x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; return x ^ (x >> 31); }

static string T; static int Lt;
struct Model { string name; ll sigma; int kind; ll p1, p2; };
// energy of a nick-free two-chord face: template unpaired substring T[lo..hi] (may be empty), uI unpaired item bases
static ll gNickFree(const Model &M, int lo, int hi, int uI) {
  int uT = hi - lo + 1;
  if (uT == 0 && uI == 0) return M.sigma;
  switch (M.kind) {
    case 0: return 0;                      // stack-only
    case 1: return M.p1;                   // constant penalty p1
    case 2: {                              // pseudo-random non-negative value depending on the exact loop
      unsigned long long h = mix(M.p2 + 1315423911ULL * (unsigned long long)uI);
      for (int k = lo; k <= hi; k++) h = mix(h ^ (unsigned long long)T[k]);
      h = mix(h ^ (unsigned long long)(uT * 131 + uI));
      return (ll)(h % (unsigned long long)(M.p1 + 1)); }
    case 3: {                              // size-1 bulge with unpaired A free, everything else p1
      if (uT == 1 && uI == 0 && T[lo] == 'A') return 0; return M.p1; }
    case 4: return M.p1 * (uT + uI);       // linear in loop size (p1 may be negative: violates H2)
    case 5: {                              // only bulges get p1 (may be negative), interior loops p2
      if (uT == 0 || uI == 0) return M.p1; return M.p2; }
  }
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: dp m B a1 ... an\n"); return 2; }
  int m = atoi(argv[1]), B = atoi(argv[2]);
  vector<int> a; for (int i = 3; i < argc; i++) a.push_back(atoi(argv[i]));
  int n = a.size();
  T.clear(); for (int t = 0; t < m; t++) { if (t) T += 'A'; T += string(B, 'G'); }
  Lt = T.size();
  int Lc = 0; for (int x : a) Lc += x;
  vector<Model> models = {
    {"stack-only s=-1", -1, 0, 0, 0},
    {"s=-5 const penalty 1000", -5, 1, 1000, 0},
    {"s=-4 random[0,12] seed1", -4, 2, 12, 1},
    {"s=-9 random[0,3] seed2", -9, 2, 3, 2},
    {"s=-2 A-bulge free else 7", -2, 3, 7, 0},
    {"s=-3 linear 2*size", -3, 4, 2, 0},
    // --- models violating (H2)
    {"VIOL s=-10 bulge=-1 interior=0", -10, 5, -1, 0},
    {"VIOL s=-10 bulge=-9 interior=0", -10, 5, -9, 0},
    {"VIOL s=-10 bulge=-10 interior=0", -10, 5, -10, 0},
    {"VIOL s=-10 bulge=-11 interior=0", -10, 5, -11, 0},
    {"VIOL s=-10 bulge=0 interior=-9", -10, 5, 0, -9},
    {"VIOL s=-10 bulge=0 interior=-19", -10, 5, 0, -19},
    {"VIOL s=-10 bulge=0 interior=-21", -10, 5, 0, -21},
  };
  int K = models.size();
  vector<int> seq = a; sort(seq.begin(), seq.end());
  // multiplicity of each distinct length sequence among labelled orderings
  u128 mult = 1; { map<int,int> cnt; for (int x : a) cnt[x]++; for (auto &kv : cnt) for (int t = 2; t <= kv.second; t++) mult *= t; }
  const ll INF = LLONG_MAX / 4;
  vector<ll> best(K, INF); vector<u128> bestCnt(K, 0); u128 totalConn = 0; unsigned long long nSeq = 0;
  vector<int> itemOf(Lc);
  vector<vector<ll>> E(K, vector<ll>(Lt * Lc)); vector<vector<u128>> Cn(K, vector<u128>(Lt * Lc));
  vector<u128> W(Lt * Lc);
  do {
    nSeq++;
    { int p = 0; for (int k = 0; k < n; k++) for (int t = 0; t < seq[k]; t++) itemOf[p++] = k; }
    // chord (i,j): template index i (must be G), item-circle index j. Process chords from the innermost
    // (largest i, smallest j) outwards.
    for (int k = 0; k < K; k++) { fill(E[k].begin(), E[k].end(), INF); fill(Cn[k].begin(), Cn[k].end(), (u128)0); }
    fill(W.begin(), W.end(), (u128)0);
    for (int i = Lt - 1; i >= 0; i--) if (T[i] == 'G') for (int j = 0; j < Lc; j++) {
      int id = i * Lc + j;
      // (i,j) innermost chord: inner face holds template bases > i, the nick template|item0, item bases < j
      if (itemOf[j] == 0) { W[id] += 1; for (int k = 0; k < K; k++) { E[k][id] = 0; Cn[k][id] = 1; } }
      // previous (inner) chord (i2,j2), i2 > i, j2 < j, at most one nick between j2 and j
      for (int i2 = i + 1; i2 < Lt; i2++) if (T[i2] == 'G') for (int j2 = j - 1; j2 >= 0; j2--) {
        int nk = itemOf[j] - itemOf[j2];
        if (nk >= 2) break;
        int id2 = i2 * Lc + j2;
        if (W[id2] == 0) continue;
        W[id] += W[id2];
        for (int k = 0; k < K; k++) {
          ll e = E[k][id2];
          if (nk == 0) e += gNickFree(models[k], i + 1, i2 - 1, j - j2 - 1);   // exterior faces: 0 (H0)
          if (e < E[k][id]) { E[k][id] = e; Cn[k][id] = Cn[k][id2]; }
          else if (e == E[k][id]) Cn[k][id] += Cn[k][id2];
        }
      }
    }
    // outermost chord must lie on the last item (outer face: one nick)
    for (int i = 0; i < Lt; i++) if (T[i] == 'G') for (int j = 0; j < Lc; j++) if (itemOf[j] == n - 1) {
      int id = i * Lc + j; if (W[id] == 0) continue;
      totalConn += W[id] * mult;
      for (int k = 0; k < K; k++) {
        if (E[k][id] < best[k]) { best[k] = E[k][id]; bestCnt[k] = Cn[k][id] * mult; }
        else if (E[k][id] == best[k]) bestCnt[k] += Cn[k][id] * mult;
      }
    }
  } while (next_permutation(seq.begin(), seq.end()));
  printf("SEQS %llu MULT %s\n", nSeq, u128s(mult).c_str());
  printf("CONNECTED %s\n", u128s(totalConn).c_str());
  for (int k = 0; k < K; k++) printf("MODEL %d | %s | sigma %lld | MFE %lld | NMIN %s\n", k, models[k].name.c_str(), models[k].sigma, best[k], u128s(bestCnt[k]).c_str());
  return 0;
}
