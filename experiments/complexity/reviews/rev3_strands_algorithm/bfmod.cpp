// Referee's brute-force enumerator, C++ version with pruning (review3).
// Enumerates all pairs (Y, S): Y a word of strand species (each species i exactly n_i times), S a connected
// non-crossing structure on the circular arrangement Y.  For every S computes the product of loop weights
// modulo the prime p = 2^61 - 1 and the rotational symmetry R(Y,S).  Output: for every R and every alpha in the
// list, T[R][alpha] = sum over pairs with symmetry exactly R of w(S)^alpha mod p, and the number of pairs.
// With option "necklace" only one representative of each rotation class of words is enumerated and weighted
// by the size of the class (c / v(Y)).
//
// Loop model (tables supplied by the caller, already reduced mod p):
//   hairpin   hp[u][a][b]            u unpaired, closing letters a (5' side), b
//   two-pair  il[l1][a1][b1][l2][a2][b2]  (caller supplies a table invariant under swapping the two segments)
//   multiloop ma * mb^b * mc^u
//   a face with exactly one nick: weight 1;  a face with >= 2 nicks: structure rejected (disconnected)
//
// Input (stdin): k ; k lines "seq count" ; nalpha alphas ; mode (0 all words, 1 necklaces) ; Nmax ;
//   hp table ((Nmax+1)*16 numbers) ; il table ((Nmax+1)^2*256 numbers) ; ma mb mc
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef unsigned __int128 u128;
static const u64 P = (1ULL << 61) - 1;
static inline u64 mulmod(u64 a, u64 b) { u128 z = (u128)a * b; u64 lo = (u64)(z & P), hi = (u64)(z >> 61); u64 s = lo + hi; if (s >= P) s -= P; return s; }
static inline u64 addmod(u64 a, u64 b) { u64 s = a + b; if (s >= P) s -= P; return s; }
static u64 powmod(u64 a, long long e) { // e >= 0
    u64 r = 1; while (e > 0) { if (e & 1) r = mulmod(r, a); a = mulmod(a, a); e >>= 1; } return r; }
static u64 invmod(u64 a) { return powmod(a, (long long)(P - 2)); }

int k, N, c, Nmax;
vector<string> spseq; vector<int> spcnt;
vector<long long> alphas;
vector<u64> hpT, ilT; u64 ma, mb, mc;
int lett[64]; bool nickAfter[64]; int partnerArr[64];
vector<int> word; vector<int> startPos;
vector<int> validShifts; // base shifts (in positions) of nontrivial rotations preserving the word
u64 mult; // multiplicity of the current word (necklace mode)
map<int, vector<u64>> T; map<int, u64> cntR; unsigned long long nstruct = 0;
u64 mbpow[80], mcpow[80];

static inline int code(char ch) { return ch == 'A' ? 0 : ch == 'C' ? 1 : ch == 'G' ? 2 : 3; }
static inline bool canpair(int a, int b) { return a + b == 3; } // A(0)-T(3), C(1)-G(2)
static inline u64 HP(int u, int a, int b) { return hpT[(u * 4 + a) * 4 + b]; }
static inline u64 IL(int l1, int a1, int b1, int l2, int a2, int b2) {
    return ilT[((((( (size_t)l1 * 4 + a1) * 4 + b1) * (Nmax + 1) + l2) * 4 + a2) * 4 + b2)]; }

struct Face { int a, b; int nn; int nch; int unp; int d, e; };

void leaf(u64 w) {
    // symmetry
    int R = 1;
    for (int sh : validShifts) {
        bool ok = true;
        for (int p = 0; p < N && ok; ++p) {
            int q = partnerArr[p]; int pp = p + sh; if (pp >= N) pp -= N;
            if (q < 0) { if (partnerArr[pp] >= 0) ok = false; }
            else { int qq = q + sh; if (qq >= N) qq -= N; if (partnerArr[pp] != qq) ok = false; }
        }
        if (ok) ++R;
    }
    ++nstruct;
    cntR[R] += mult;
    auto &v = T[R]; if (v.empty()) v.assign(alphas.size(), 0);
    u64 winv = 0; bool haveinv = false;
    for (size_t t = 0; t < alphas.size(); ++t) {
        long long al = alphas[t]; u64 x;
        if (al == 0) x = 1;
        else if (al > 0) x = powmod(w, al);
        else { if (!haveinv) { winv = invmod(w); haveinv = true; } x = powmod(winv, -al); }
        v[t] = addmod(v[t], mulmod(x, mult % P));
    }
}

// continuation-passing enumeration.  face stack is explicit.
vector<Face> fstack;
void walk(int pos, int end, u64 w, const function<void(u64)> &cont);

void closeFace(u64 w, const function<void(u64)> &cont) {
    Face &f = fstack.back();
    u64 fw = 1;
    if (f.a < 0) { // outer face: must have exactly one nick (the wrap nick), guaranteed by pruning
        if (f.nn != 1) return;
    } else if (f.nn == 0) {
        if (f.nch == 0) fw = HP(f.b - f.a - 1, lett[f.a], lett[f.b]);
        else if (f.nch == 1) fw = IL(f.d - f.a - 1, lett[f.a], lett[f.d], f.b - f.e - 1, lett[f.e], lett[f.b]);
        else fw = mulmod(ma, mulmod(mbpow[f.nch + 1], mcpow[f.unp]));
    }
    cont(mulmod(w, fw));
}

void walk(int pos, int end, u64 w, const function<void(u64)> &cont) {
    if (pos > end) { closeFace(w, cont); return; }
    size_t idx = fstack.size() - 1;
    Face saved = fstack[idx];
    // option 1: pos unpaired
    {
        int nn2 = saved.nn + (nickAfter[pos] ? 1 : 0);
        if (nn2 <= 1) {
            fstack[idx].nn = nn2; fstack[idx].unp = saved.unp + 1;
            walk(pos + 1, end, w, cont);
            fstack[idx] = saved;
        }
    }
    // option 2: pos paired with q
    for (int q = pos + 1; q <= end; ++q) {
        if (!canpair(lett[pos], lett[q])) continue;
        int nnp = saved.nn + (nickAfter[q] ? 1 : 0);
        if (nnp > 1) continue; // the parent face would get a second nick when leaving q
        partnerArr[pos] = q; partnerArr[q] = pos;
        Face child; child.a = pos; child.b = q; child.nn = nickAfter[pos] ? 1 : 0; child.nch = 0; child.unp = 0; child.d = child.e = -1;
        fstack.push_back(child);
        int pq = q, pe = end; Face sv = saved; int ppos = pos;
        walk(pos + 1, q - 1, w, [&, pq, pe, sv, ppos, idx](u64 w2) {
            // child face complete: pop it, continue the parent face after q
            Face ch = fstack.back(); fstack.pop_back();
            Face before = fstack[idx];
            fstack[idx] = sv; fstack[idx].nn = sv.nn + (nickAfter[pq] ? 1 : 0); fstack[idx].nch = sv.nch + 1;
            if (sv.nch == 0) { fstack[idx].d = ppos; fstack[idx].e = pq; }
            walk(pq + 1, pe, w2, cont);
            fstack[idx] = before; fstack.push_back(ch);
        });
        fstack.pop_back();
        partnerArr[pos] = -1; partnerArr[q] = -1;
    }
    fstack[idx] = saved;
}

int main() {
    if (!(cin >> k)) return 1;
    spseq.resize(k); spcnt.resize(k); c = 0;
    for (int i = 0; i < k; ++i) { cin >> spseq[i] >> spcnt[i]; c += spcnt[i]; }
    int na; cin >> na; alphas.resize(na); for (auto &a : alphas) cin >> a;
    int mode; cin >> mode; cin >> Nmax;
    hpT.resize((size_t)(Nmax + 1) * 16); for (auto &x : hpT) cin >> x;
    ilT.resize((size_t)(Nmax + 1) * (Nmax + 1) * 256); for (auto &x : ilT) cin >> x;
    cin >> ma >> mb >> mc;
    mbpow[0] = mcpow[0] = 1; for (int i = 1; i < 80; ++i) { mbpow[i] = mulmod(mbpow[i - 1], mb); mcpow[i] = mulmod(mcpow[i - 1], mc); }
    word.clear(); for (int i = 0; i < k; ++i) for (int j = 0; j < spcnt[i]; ++j) word.push_back(i);
    sort(word.begin(), word.end());
    unsigned long long nwords = 0;
    do {
        // rotation class handling
        int v = 0; bool isMin = true;
        for (int j = 0; j < c; ++j) {
            bool same = true; int cmp = 0;
            for (int t = 0; t < c; ++t) { int a = word[(t + j) % c], b = word[t]; if (a != b) { same = false; cmp = (a < b) ? -1 : 1; break; } }
            if (same) ++v; else if (cmp < 0) isMin = false;
        }
        if (mode == 1) { if (!isMin) continue; mult = c / v; } else mult = 1;
        ++nwords;
        N = 0; startPos.assign(c, 0);
        for (int t = 0; t < c; ++t) { startPos[t] = N; const string &s = spseq[word[t]]; for (size_t i = 0; i < s.size(); ++i) { lett[N] = code(s[i]); nickAfter[N] = (i + 1 == s.size()); ++N; } }
        validShifts.clear();
        for (int j = 1; j < c; ++j) { bool same = true; for (int t = 0; t < c && same; ++t) if (word[(t + j) % c] != word[t]) same = false; if (same) validShifts.push_back(startPos[j]); }
        for (int i = 0; i < N; ++i) partnerArr[i] = -1;
        fstack.clear(); Face outer; outer.a = -1; outer.b = -1; outer.nn = 0; outer.nch = 0; outer.unp = 0; outer.d = outer.e = -1; fstack.push_back(outer);
        walk(0, N - 1, 1, [&](u64 w) { leaf(w); });
    } while (next_permutation(word.begin(), word.end()));
    cout << "words " << nwords << " structs " << nstruct << "\n";
    for (auto &kv : T) {
        cout << "R " << kv.first << " count " << cntR[kv.first];
        for (u64 x : kv.second) cout << " " << x;
        cout << "\n";
    }
    return 0;
}
