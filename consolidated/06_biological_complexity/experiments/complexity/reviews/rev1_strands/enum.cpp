// enum.cpp -- referee's independent brute-force enumerator (written from scratch).
//
// Enumerates, for a list of labelled strands, ALL circular orderings (strand 0 fixed first)
// and ALL non-crossing sets of Watson-Crick pairs (A-T, C-G) on the resulting circle.
// For every structure: face decomposition, connectivity by faces ("no face with >=2 nicks")
// AND by union-find, labelled key, physical (indistinguishable-strand) canonical key,
// rotational symmetry degree R, a structural "tiling" test, and a signature = multiset of
// canonical face boundary strings.  Energies are NOT computed here: the driver evaluates
// arbitrary loop-energy functions on the face strings afterwards.
//
// usage: enum [--prune] [--orbit] [--lean] [--quiet] strand0 strand1 ...
//   --prune : cut a branch as soon as a closed face has >= 2 nicks (sound: such structures
//             are disconnected).  Without it every non-crossing pair set is visited.
//   --orbit : additionally compute orbit-canonical keys under permutations of equal strands
//             (brute force over the group) to cross-check the rotation-based physical key.
//   --lean  : keep no per-structure records (no duplicate / physical-class bookkeeping).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;

static int N, C;
static vector<string> strands;          // by label
static vector<int> ord_;                // circular order (labels), ord_[0] == 0
static vector<char> letter;             // by position
static vector<int> sOf, iOf;            // label / index-in-strand by position
static vector<int> startPos;            // start position of k-th strand in the order
static vector<int> partner;
static vector<int> stk;
static int openCnt[256];
static vector<array<int,256>> rem;      // rem[p][x] = #positions >= p with letter x
static bool optPrune = false, optOrbit = false, optQuiet = false, optLean = false;
static vector<int> rotCand;             // rotations r whose type sequence equals that of r=0
static vector<int> rotMin;              // rotations r whose type sequence is lexicographically minimal

static inline char compl_(char a) {
  switch (a) { case 'A': return 'T'; case 'T': return 'A'; case 'C': return 'G'; case 'G': return 'C'; }
  return '?';
}
static inline bool linkIsNick(int p) { // link p -> p+1 (p+1 taken mod N)
  if (p == N - 1) return true;
  return sOf[p] != sOf[p + 1];
}

// ---------- hashing ----------
static inline u64 mix(u64 x) { x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL; x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; return x ^ (x >> 31); }
struct H128 { u64 a = 0x243F6A8885A308D3ULL, b = 0x13198A2E03707344ULL; int n = 0;
  inline void add(u64 v) { a = mix(a ^ v); b = mix(b + v * 0x100000001b3ULL + 7); n++; }
  inline pair<u64,u64> fin() { u64 x = mix(a ^ n), y = mix(b ^ ((u64)n << 17)); return {x, y}; } };

// ---------- statistics ----------
static u64 totalMatchings = 0, nConnected = 0, nDisconnected = 0;
static u64 fact1Mismatch = 0, extCountMismatch = 0, tilingTotal = 0, prunedBranches = 0;
static int maxR = 0;
static unordered_map<string,int> rawId;  // raw (unrotated) face string -> canonical id
static unordered_map<string,int> descId; static vector<string> descs;
struct VecHash { size_t operator()(const vector<int> &v) const { u64 h = 1469598103934665603ULL; for (int x : v) h = mix(h ^ (u64)x); return (size_t)h; } };
static unordered_map<vector<int>,int,VecHash> sigId;
struct SigStat { u64 lab = 0, phys = 0, tiling = 0; string example; vector<int> ids; };
static vector<SigStat> sigs;
struct Rec { u64 a, b; int sig; };
static vector<Rec> labRecs, physRecs, orbRecs;
static vector<vector<int>> groupMaps;   // label permutations preserving sequences

// canonical rotation of a cyclic token string (letters at even offsets)
static string canonRot(const string &s) {
  int L = s.size(); string best = s;
  for (int o = 2; o < L; o += 2) {
    string t = s.substr(o) + s.substr(0, o);
    if (t < best) best = t;
  }
  return best;
}
static int internFace(const string &raw) {
  auto it = rawId.find(raw);
  if (it != rawId.end()) return it->second;
  string c = canonRot(raw);
  auto jt = descId.find(c);
  int id;
  if (jt == descId.end()) { id = descs.size(); descId[c] = id; descs.push_back(c); } else id = jt->second;
  rawId[raw] = id;
  return id;
}

// nick count of the inner face of chord (i,j), i<j
static inline int innerNicks(int i, int j) {
  int nicks = 0, p = i;
  while (true) {
    if (linkIsNick(p)) nicks++;
    int q = p + 1;
    if (q == j) break;
    if (partner[q] == -1) { p = q; continue; }
    p = partner[q];
  }
  return nicks;
}
static inline int outerNicks() {
  int nicks = 0, p = 0;
  while (true) {
    if (partner[p] != -1) p = partner[p];
    if (p == N - 1) break;
    if (linkIsNick(p)) nicks++;
    p++;
  }
  return nicks + 1;
}
static string facebuf;
// inner face of chord (i,j), i<j: token string
static const string &innerFace(int i, int j) {
  string &s = facebuf; s.clear(); s += letter[i];
  int p = i;
  while (true) {
    s += (linkIsNick(p) ? '|' : '-');
    int q = p + 1; s += letter[q];
    if (q == j) break;
    if (partner[q] == -1) { p = q; continue; }
    int e = partner[q]; s += '='; s += letter[e]; p = e;
  }
  s += '=';
  return s;
}
static const string &outerFace() {
  string &s = facebuf; s.clear(); int p = 0;
  while (true) {
    s += letter[p];
    if (partner[p] != -1) { int e = partner[p]; s += '='; s += letter[e]; p = e; }
    if (p == N - 1) break;
    s += (linkIsNick(p) ? '|' : '-'); p++;
  }
  s += '|';
  return s;
}

static vector<int> ufp;
static int uff(int x) { while (ufp[x] != x) { ufp[x] = ufp[ufp[x]]; x = ufp[x]; } return x; }

static vector<int> blockOfT;  // template index -> block id or -1 for non-G
static int nG = 0;
static vector<vector<int>> tpBuf;

static bool isTiling() {
  // every item base paired with a template base; per item the partners are consecutive
  // template indices, decreasing (antiparallel), inside one block; all G's used.
  vector<vector<int>> &tp = tpBuf;
  for (int l = 1; l < C; l++) tp[l].assign(strands[l].size(), -1);
  int npairs = 0;
  for (int p = 0; p < N; p++) if (partner[p] > p) {
    int q = partner[p]; npairs++;
    int lp = sOf[p], lq = sOf[q];
    if (lp == 0 && lq != 0) tp[lq][iOf[q]] = iOf[p];
    else if (lq == 0 && lp != 0) tp[lp][iOf[p]] = iOf[q];
    else return false;
  }
  if (npairs != nG) return false;
  for (int l = 1; l < C; l++) {
    int len = strands[l].size();
    for (int k = 0; k < len; k++) if (tp[l][k] < 0) return false;
    int blk = blockOfT[tp[l][0]]; if (blk < 0) return false;
    for (int k = 0; k + 1 < len; k++) {
      if (tp[l][k + 1] != tp[l][k] - 1) return false;
      if (blockOfT[tp[l][k + 1]] != blk) return false;
    }
  }
  return true;
}

static vector<int> idsBuf;
static vector<pair<int,int>> prsBuf, chBuf, ch0Buf, qBuf, bestBuf;

static void process() {
  totalMatchings++;
  // connectivity by faces: every face has at most one nick
  bool faceConn = true; int nExt = 0;
  { int nk = outerNicks(); if (nk >= 2) faceConn = false; if (nk == 1) nExt++; }
  for (int p = 0; p < N; p++) if (partner[p] > p) { int nk = innerNicks(p, partner[p]); if (nk >= 2) faceConn = false; if (nk == 1) nExt++; }
  // union-find connectivity on bases with covalent bonds and pairs
  for (int p = 0; p < N; p++) ufp[p] = p;
  for (int p = 0; p + 1 < N; p++) if (sOf[p] == sOf[p + 1]) ufp[uff(p)] = uff(p + 1);
  for (int p = 0; p < N; p++) if (partner[p] > p) ufp[uff(p)] = uff(partner[p]);
  bool ufConn = true; { int r = uff(0); for (int p = 1; p < N; p++) if (uff(p) != r) { ufConn = false; break; } }
  if (faceConn != ufConn) fact1Mismatch++;
  if (!ufConn) { nDisconnected++; return; }
  nConnected++;
  if (nExt != C) extCountMismatch++;
  // signature
  vector<int> &ids = idsBuf; ids.clear();
  ids.push_back(internFace(outerFace()));
  for (int p = 0; p < N; p++) if (partner[p] > p) ids.push_back(internFace(innerFace(p, partner[p])));
  sort(ids.begin(), ids.end());
  int sid;
  { auto it = sigId.find(ids); if (it == sigId.end()) { sid = sigs.size(); sigId[ids] = sid; sigs.emplace_back(); sigs.back().ids = ids; } else sid = it->second; }
  SigStat &S = sigs[sid];
  S.lab++;
  bool til = isTiling(); if (til) { S.tiling++; tilingTotal++; }
  if (S.example.empty()) {
    string ex;
    for (int k = 0; k < C; k++) { ex += strands[ord_[k]]; ex += (k + 1 < C ? "+" : ""); }
    ex += " ";
    for (int p = 0; p < N; p++) { ex += (partner[p] == -1 ? '.' : (partner[p] > p ? '(' : ')')); if (p + 1 < N && sOf[p] != sOf[p + 1]) ex += '+'; }
    ex += " order=";
    for (int k = 0; k < C; k++) { ex += to_string(ord_[k]); ex += (k + 1 < C ? "," : ""); }
    S.example = ex;
  }
  // rotational symmetry degree and physical key
  //   chord list in coordinates rotated to start at strand r (positions mod N)
  auto rotChords = [&](int r, vector<pair<int,int>> &ch) {
    ch.clear(); int sh = startPos[r];
    for (int p = 0; p < N; p++) if (partner[p] > p) {
      int a = p - sh; if (a < 0) a += N; int b = partner[p] - sh; if (b < 0) b += N; if (a > b) swap(a, b); ch.push_back({a, b});
    }
    sort(ch.begin(), ch.end());
  };
  rotChords(0, ch0Buf);
  int R = 1;
  for (int r : rotCand) if (r != 0) { rotChords(r, chBuf); if (chBuf == ch0Buf) R++; }
  if (R > maxR) maxR = R;
  if (optLean) return;
  // labelled key
  vector<pair<int,int>> &prs = prsBuf; prs.clear();
  for (int p = 0; p < N; p++) if (partner[p] > p) {
    int a = (sOf[p] << 8) | iOf[p], b = (sOf[partner[p]] << 8) | iOf[partner[p]];
    if (a > b) swap(a, b); prs.push_back({a, b});
  }
  sort(prs.begin(), prs.end());
  { H128 h; for (auto &pr : prs) h.add(((u64)pr.first << 20) | pr.second); auto f = h.fin(); labRecs.push_back({f.first, f.second, sid}); }
  // physical key: min over rotations with minimal type sequence of the rotated chord list
  { bool first = true;
    for (int r : rotMin) { rotChords(r, chBuf); if (first || chBuf < bestBuf) { bestBuf = chBuf; first = false; } }
    H128 h; h.add(0xABCDEF); for (auto &pr : bestBuf) h.add(((u64)pr.first << 20) | pr.second);
    // the minimal type sequence itself is determined by the multiset of strands and rotMin[0]; include it
    for (int k = 0; k < C; k++) { const string &s = strands[ord_[(rotMin[0] + k) % C]]; for (char ch : s) h.add((u64)ch); h.add(0x2F); }
    auto f = h.fin(); physRecs.push_back({f.first, f.second, sid}); }
  // orbit key: min over label permutations of equal-sequence strands
  if (optOrbit) {
    bool first = true;
    for (auto &g : groupMaps) {
      vector<pair<int,int>> &q = qBuf; q.clear();
      for (auto &pr : prs) {
        int a = (g[pr.first >> 8] << 8) | (pr.first & 255), b = (g[pr.second >> 8] << 8) | (pr.second & 255);
        if (a > b) swap(a, b); q.push_back({a, b});
      }
      sort(q.begin(), q.end());
      if (first || q < bestBuf) { bestBuf = q; first = false; }
    }
    H128 h; h.add(0x777); for (auto &pr : bestBuf) h.add(((u64)pr.first << 20) | pr.second);
    auto f = h.fin(); orbRecs.push_back({f.first, f.second, sid});
  }
}

static void dfs(int p) {
  // completability of open chords (necessary condition; sound)
  static const char L4[4] = {'A', 'C', 'G', 'T'};
  for (char x : L4) if (openCnt[(int)x] > rem[p][(int)compl_(x)]) return;
  if (p == N) { if (stk.empty()) process(); return; }
  // 1. unpaired
  partner[p] = -1; dfs(p + 1);
  // 2. close the most recent open chord
  if (!stk.empty() && compl_(letter[stk.back()]) == letter[p]) {
    int q = stk.back(); stk.pop_back(); openCnt[(int)letter[q]]--;
    partner[q] = p; partner[p] = q;
    bool ok = true;
    if (optPrune) { if (innerNicks(q, p) >= 2) { ok = false; prunedBranches++; } }
    if (ok) dfs(p + 1);
    partner[q] = -1; partner[p] = -1;
    stk.push_back(q); openCnt[(int)letter[q]]++;
  }
  // 3. open a chord
  stk.push_back(p); openCnt[(int)letter[p]]++; partner[p] = -2;
  dfs(p + 1);
  stk.pop_back(); openCnt[(int)letter[p]]--; partner[p] = -1;
}

int main(int argc, char **argv) {
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--prune") optPrune = true; else if (a == "--orbit") optOrbit = true; else if (a == "--quiet") optQuiet = true;
    else if (a == "--lean") optLean = true;
    else strands.push_back(a);
  }
  C = strands.size(); N = 0; for (auto &s : strands) N += s.size();
  if (C < 1 || N > 250) { fprintf(stderr, "bad input\n"); return 2; }
  tpBuf.resize(C);
  // template block structure (strand 0), used only by the structural tiling test
  { int blk = 0; blockOfT.assign(strands[0].size(), -1);
    for (size_t k = 0; k < strands[0].size(); k++) { if (strands[0][k] == 'G') { blockOfT[k] = blk; nG++; } else blk++; } }
  // group of label permutations preserving sequences (for --orbit)
  if (optOrbit) {
    vector<int> perm(C); iota(perm.begin(), perm.end(), 0);
    do { bool ok = true; for (int l = 0; l < C; l++) if (strands[perm[l]] != strands[l]) { ok = false; break; } if (ok) groupMaps.push_back(perm); } while (next_permutation(perm.begin(), perm.end()));
  }
  letter.assign(N, '?'); sOf.assign(N, 0); iOf.assign(N, 0); partner.assign(N, -1); ufp.assign(N, 0);
  rem.assign(N + 1, array<int,256>());
  vector<int> rest; for (int l = 1; l < C; l++) rest.push_back(l);
  u64 nOrders = 0;
  do {
    ord_.clear(); ord_.push_back(0); for (int l : rest) ord_.push_back(l);
    startPos.assign(C, 0);
    int pos = 0;
    for (int k = 0; k < C; k++) { startPos[k] = pos; const string &s = strands[ord_[k]]; for (size_t t = 0; t < s.size(); t++) { letter[pos] = s[t]; sOf[pos] = ord_[k]; iOf[pos] = t; pos++; } }
    for (int x = 0; x < 256; x++) rem[N][x] = 0;
    for (int p = N - 1; p >= 0; p--) { rem[p] = rem[p + 1]; rem[p][(int)letter[p]]++; }
    // rotations: type sequences
    { vector<string> ts(C);
      for (int r = 0; r < C; r++) { string t; for (int k = 0; k < C; k++) { t += strands[ord_[(r + k) % C]]; t += '/'; } ts[r] = t; }
      rotCand.clear(); rotMin.clear();
      string mn = *min_element(ts.begin(), ts.end());
      for (int r = 0; r < C; r++) { if (ts[r] == ts[0]) rotCand.push_back(r); if (ts[r] == mn) rotMin.push_back(r); } }
    fill(partner.begin(), partner.end(), -1); stk.clear(); memset(openCnt, 0, sizeof(openCnt));
    dfs(0);
    nOrders++;
  } while (next_permutation(rest.begin(), rest.end()));

  // duplicates among labelled keys (same labelled structure met twice => under two orderings)
  u64 dupLab = 0, nLab = labRecs.size();
  sort(labRecs.begin(), labRecs.end(), [](const Rec &x, const Rec &y) { return x.a != y.a ? x.a < y.a : x.b < y.b; });
  for (size_t i = 1; i < labRecs.size(); i++) if (labRecs[i].a == labRecs[i - 1].a && labRecs[i].b == labRecs[i - 1].b) dupLab++;
  // physical classes
  u64 nPhys = 0;
  sort(physRecs.begin(), physRecs.end(), [](const Rec &x, const Rec &y) { return x.a != y.a ? x.a < y.a : x.b < y.b; });
  u64 physSigClash = 0;
  for (size_t i = 0; i < physRecs.size(); i++) {
    if (i == 0 || physRecs[i].a != physRecs[i - 1].a || physRecs[i].b != physRecs[i - 1].b) { nPhys++; sigs[physRecs[i].sig].phys++; }
    else if (physRecs[i].sig != physRecs[i - 1].sig) physSigClash++;
  }
  u64 nOrb = 0;
  if (optOrbit) {
    sort(orbRecs.begin(), orbRecs.end(), [](const Rec &x, const Rec &y) { return x.a != y.a ? x.a < y.a : x.b < y.b; });
    for (size_t i = 0; i < orbRecs.size(); i++) if (i == 0 || orbRecs[i].a != orbRecs[i - 1].a || orbRecs[i].b != orbRecs[i - 1].b) nOrb++;
  }
  printf("ORDERS %llu\n", nOrders);
  printf("VISITED %llu\n", totalMatchings);
  printf("CONNECTED %llu\n", nConnected);
  printf("DISCONNECTED %llu\n", nDisconnected);
  printf("PRUNED %llu\n", prunedBranches);
  printf("FACT1_MISMATCH %llu\n", fact1Mismatch);
  printf("EXTCOUNT_MISMATCH %llu\n", extCountMismatch);
  printf("LEAN %d\n", optLean ? 1 : 0);
  printf("DUP_LABELLED %llu\n", dupLab);
  printf("LABELLED %llu\n", nLab);
  printf("PHYS %llu\n", nPhys);
  printf("PHYS_SIG_CLASH %llu\n", physSigClash);
  if (optOrbit) printf("ORBIT %llu\nGROUP %zu\n", nOrb, groupMaps.size());
  printf("MAXR %d\n", maxR);
  printf("TILING %llu\n", tilingTotal);
  printf("NDESC %zu\n", descs.size());
  for (size_t i = 0; i < descs.size(); i++) printf("DESC %zu %s\n", i, descs[i].c_str());
  printf("NSIG %zu\n", sigs.size());
  if (!optQuiet) for (size_t i = 0; i < sigs.size(); i++) {
    printf("SIG %zu %llu %llu %llu :", i, sigs[i].lab, sigs[i].phys, sigs[i].tiling);
    for (int id : sigs[i].ids) printf(" %d", id);
    printf(" ; %s\n", sigs.size() < 300000 ? sigs[i].example.c_str() : "-");
  }
  return 0;
}
