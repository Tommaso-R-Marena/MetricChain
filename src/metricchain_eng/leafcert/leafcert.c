/*
 * leafcert.c -- exact checker for "shares at the leaves" certificates.
 *
 * Format and rule: science division, docs/science/workstreams/P7_REPORT.md, sections 5.1-5.3, at commit
 * 2b4ccdf of research/scientific-translation (their request P7-E2).  Written from that text.
 *
 * STATEMENT.  A certificate consists of an instance on n sites, site i with the states 0..k_i-1 (integer
 * tables H_i(a) and J_ij(a,b) for i < j), an integer bound L, a list of leaf certificates (U, P2, m) and a
 * branching tree.  If leafcert_check returns LC_ACCEPT then
 *
 *        sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j)  >=  L      for every x with 0 <= x_i < k_i.
 *
 * WHAT IS CHECKED.  A node of the tree is a leaf node (it names a leaf certificate) or a branch on a site
 * that no ancestor has branched on, with exactly one child per state of that site.  The box D of a leaf
 * node is D_i = {a} if the path from the root fixes site i to a, and D_i = {0..k_i-1} otherwise.  For
 * every leaf node, with (U, P2, m) the certificate it names, in this order:
 *
 *   (S)  for every site i and every a in D_i:            U_i   <= H_i(a) + sum_{j != i} m_ij(a)
 *   (P)  for every pair i < j, a in D_i, b in D_j:       P2_ij <= J_ij(a,b) - m_ij(a) - m_ji(b)
 *   (T)                                                  L     <= sum_i U_i + sum_{i<j} P2_ij
 *
 * Leaf nodes are visited depth first, the children of a branch in increasing order of the state, and the
 * first inequality that fails is reported.  The whole input is validated before any arithmetic is done.
 *
 * WHY THIS IMPLIES THE STATEMENT.  (a) A branch is on a site that no ancestor fixed and has a child for
 * every state of that site, so the box of a node is the union of the boxes of its children; hence every x
 * lies in the box of some leaf node.  (b) For x in the box of a leaf node, (S) holds at (i, x_i) for every
 * i and (P) at (i, j, x_i, x_j) for every i < j; adding them gives sum U + sum P2 <= energy(x), because
 * every m_ij(x_i) occurs once with each sign; with (T), L <= energy(x).
 *
 * Only additions, subtractions and comparisons of integers are used; there is no floating point in this
 * file, no minimisation and no enumeration of the domain.
 *
 * ARITHMETIC.  Every integer of the input must fit in 64 bits (otherwise LC_REJECT_RANGE: this checker
 * does not decide such an input).  Sums are accumulated in 128 bits: a sum has at most
 * LC_MAX_SITES + LC_MAX_SITES^2/2 < 2^24 terms of absolute value at most 2^63, so its absolute value is
 * below 2^87 and cannot overflow.  Each addition is nevertheless made with the compiler's overflow check.
 * Compiled with -DLC_ACC64 the accumulators have 64 bits and an addition that overflows gives
 * LC_REJECT_OVERFLOW (never a wrapped value); that build exists to exercise the overflow checks.
 *
 * INPUT (ASCII; tokens separated by blanks, tabs or newlines; integers in decimal, "-" for negative
 * numbers, no "+", no leading zeros, no "-0"):
 *
 *   leafcert 1
 *   sites n
 *   shape k_0 ... k_{n-1}
 *   bound L
 *   h i   H_i(0) ... H_i(k_i-1)                                  for i = 0 .. n-1
 *   j i j   J_ij(0,0) ... J_ij(0,k_j-1) J_ij(1,0) ...            for the pairs i < j, lexicographic
 *   leaves T
 *   then, for t = 0 .. T-1:
 *     leaf t
 *     u   U_0 ... U_{n-1}
 *     p   P2_ij for the pairs i < j, lexicographic
 *     m i j   m_ij(0) ... m_ij(k_i-1)                            for the ordered pairs i != j, lexicographic
 *   tree
 *   NODE
 *   end
 *
 *   NODE  :=  L t   |   B i c  0 NODE  1 NODE  ...  (c-1) NODE        with c = k_i
 *
 * Every leaf certificate must be named by at least one node.  Nothing may follow "end".
 *
 * Library:    cc -std=c11 -O2 -shared -fPIC -o libleafcert.so leafcert.c
 * Executable: cc -std=c11 -O2 -DLEAFCERT_MAIN -o leafcert leafcert.c ;  ./leafcert FILE...
 *             (exit status 0: every file accepted; 1: some file rejected; 2: a file could not be read)
 */
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#if !defined(__SIZEOF_INT128__)
#error "leafcert.c needs a compiler with the type __int128 (gcc or clang on a 64-bit target)"
#endif
__extension__ typedef __int128 i128;
__extension__ typedef unsigned __int128 u128;
_Static_assert(sizeof(size_t) >= 8, "leafcert.c assumes a 64-bit size_t");

#ifdef LC_ACC64
typedef int64_t acc_t;
#define LC_ACC_BITS 64
#else
typedef i128 acc_t;
#define LC_ACC_BITS 128
#endif

#define LC_MAX_SITES   4096u                 /* n */
#define LC_MAX_STATES  1048576u              /* k_i */
#define LC_MAX_INTS    ((size_t)1 << 26)     /* integers of the instance; integers of the leaf certificates */
#define LC_MAX_NODES   ((size_t)1 << 26)     /* nodes of the tree */

enum {
    LC_ACCEPT = 0,
    LC_REJECT_INEQUALITY = 1,   /* an inequality (S), (P) or (T) fails                         */
    LC_REJECT_FORMAT = 2,       /* the input is not a well-formed certificate                  */
    LC_REJECT_RANGE = 3,        /* an integer of the input does not fit in 64 bits             */
    LC_REJECT_LIMIT = 4,        /* a size limit of this implementation, or memory              */
    LC_REJECT_OVERFLOW = 5      /* an accumulator overflowed (64-bit build only; see above)    */
};
enum { LC_INEQ_NONE = 0, LC_INEQ_SITE = 1, LC_INEQ_PAIR = 2, LC_INEQ_TOTAL = 3 };

typedef struct {
    int64_t status;             /* one of the LC_ codes above                                             */
    int64_t inequality;         /* LC_INEQ_*: which inequality failed                                     */
    int64_t leaf;               /* index of the leaf certificate of the failing leaf node                 */
    int64_t visit;              /* rank of the failing leaf node in the traversal (0 = first)             */
    int64_t i, a, j, b;         /* sites and states of the failing inequality; -1 where there is none     */
    int64_t lhs_hi;             /* left-hand side (U_i, P2_ij or L), high and low 64 bits                 */
    uint64_t lhs_lo;
    int64_t rhs_hi;             /* right-hand side (the sum), high and low 64 bits                        */
    uint64_t rhs_lo;
    int64_t path_len;           /* number of (site, state) pairs on the path to the failing leaf node     */
    int64_t bound;              /* L (valid once the header has been read)                                */
    int64_t bound_valid;
    uint64_t sites;
    uint64_t leaf_certificates; /* T                                                                      */
    uint64_t leaf_boxes;        /* leaf nodes of the tree                                                 */
    uint64_t depth;             /* largest number of branches above a leaf node                           */
    uint64_t cert_integers;     /* T * (n + n(n-1)/2 + (n-1) sum_i k_i)                                   */
    uint64_t instance_integers; /* sum_i k_i + sum_{i<j} k_i k_j                                          */
    uint64_t additions;         /* additions and comparisons performed (up to and including a failure)   */
    uint64_t comparisons;
    int64_t token;              /* for LC_REJECT_FORMAT/RANGE/LIMIT: index of the token concerned, or -1  */
    char message[160];
} leafcert_result;

typedef struct {
    /* input */
    const unsigned char *cur, *end;
    int64_t ntok;               /* tokens read so far */
    /* instance */
    size_t n, npairs, S;        /* sites, pairs, sum of the k_i */
    size_t *k, *koff, *jbase;   /* koff[i] = k_0 + .. + k_{i-1}; jbase[i] = offset in J of the pair (i, i+1) */
    int64_t *H, *J;
    int64_t L;
    /* leaf certificates: T blocks of `stride` integers: U (n), P2 (npairs), m ((n-1) * S, site-major) */
    size_t T, stride;
    int64_t *leaves;
    unsigned char *used;
    /* tree in preorder */
    unsigned char *nkind;       /* 0 leaf node, 1 branch */
    size_t *nval;               /* leaf certificate, or site */
    size_t nnodes, ncap;
    /* traversal */
    int64_t *fixed;             /* fixed[i]: the state site i is fixed to, or -1 */
    int64_t *path;              /* (site, state) pairs from the root */
    size_t depth, pos;
    int overflow;
    leafcert_result *res;
    int64_t *path_out;
    size_t path_cap;
} ctx;

/* ------------------------------------------------------------------------------------------------ messages */
static void msg_set(leafcert_result *r, const char *text) {
    size_t len = strlen(text);
    if (len >= sizeof r->message) len = sizeof r->message - 1;
    memcpy(r->message, text, len);
    r->message[len] = '\0';
}

static void msg_cat(leafcert_result *r, const char *text) {
    size_t have = strlen(r->message), len = strlen(text);
    if (have + len >= sizeof r->message) len = sizeof r->message - 1 - have;
    memcpy(r->message + have, text, len);
    r->message[have + len] = '\0';
}

static void msg_cat_u(leafcert_result *r, uint64_t v) {
    char buf[24];
    size_t at = sizeof buf;
    buf[--at] = '\0';
    do { buf[--at] = (char)('0' + (int)(v % 10u)); v /= 10u; } while (v != 0u);
    msg_cat(r, buf + at);
}

static int reject(ctx *c, int status, const char *text) {
    if (c->res->status == LC_ACCEPT) {
        c->res->status = status;
        c->res->token = c->ntok - 1;
        msg_set(c->res, text);
    }
    return 1;
}

/* ------------------------------------------------------------------------------------------------ tokens */
static int is_blank(unsigned char ch) { return ch == ' ' || ch == '\n' || ch == '\t' || ch == '\r'; }

/* next token; returns 0 at the end of the input */
static int token(ctx *c, const unsigned char **tok, size_t *len) {
    while (c->cur < c->end && is_blank(*c->cur)) c->cur++;
    if (c->cur == c->end) return 0;
    *tok = c->cur;
    while (c->cur < c->end && !is_blank(*c->cur)) c->cur++;
    *len = (size_t)(c->cur - *tok);
    c->ntok++;
    return 1;
}

static int expect(ctx *c, const char *word) {
    const unsigned char *tok;
    size_t len;
    if (!token(c, &tok, &len)) {
        c->ntok++;
        reject(c, LC_REJECT_FORMAT, "input ends; expected the keyword '");
    } else if (len != strlen(word) || memcmp(tok, word, len) != 0) {
        reject(c, LC_REJECT_FORMAT, "expected the keyword '");
    } else {
        return 0;
    }
    msg_cat(c->res, word);
    msg_cat(c->res, "'");
    return 1;
}

/* decimal integer; 0: ok, 1: not an integer in the grammar, 2: an integer outside 64 bits */
static int parse_i64(const unsigned char *t, size_t len, int64_t *out) {
    size_t at = 0;
    int negative = 0, over = 0;
    uint64_t acc = 0;
    if (len == 0) return 1;
    if (t[0] == '-') { negative = 1; at = 1; }
    if (at == len) return 1;
    if (t[at] == '0' && (len - at > 1 || negative)) return 1;      /* leading zero, "-0" */
    for (; at < len; at++) {
        unsigned digit;
        if (t[at] < '0' || t[at] > '9') return 1;
        digit = (unsigned)(t[at] - '0');
        if (!over) {
            if (acc > (UINT64_MAX - digit) / 10u) over = 1;
            else acc = acc * 10u + digit;
        }
    }
    if (over) return 2;
    if (negative) {
        if (acc > (uint64_t)INT64_MAX + 1u) return 2;
        *out = (acc == (uint64_t)INT64_MAX + 1u) ? INT64_MIN : -(int64_t)acc;
    } else {
        if (acc > (uint64_t)INT64_MAX) return 2;
        *out = (int64_t)acc;
    }
    return 0;
}

/* an integer of the certificate */
static int read_value(ctx *c, int64_t *out) {
    const unsigned char *tok;
    size_t len;
    int rc;
    if (!token(c, &tok, &len)) { c->ntok++; return reject(c, LC_REJECT_FORMAT, "input ends where an integer is expected"); }
    rc = parse_i64(tok, len, out);
    if (rc == 1) return reject(c, LC_REJECT_FORMAT, "not an integer");
    if (rc == 2) return reject(c, LC_REJECT_RANGE, "integer outside the 64-bit range");
    return 0;
}

static int read_values(ctx *c, int64_t *out, size_t count) {
    for (size_t q = 0; q < count; q++)
        if (read_value(c, out + q)) return 1;
    return 0;
}

/* a count or an index: an integer v with 0 <= v <= max; `what` names it in the message */
static int read_number(ctx *c, size_t max, size_t *out, const char *what, int limit_status) {
    const unsigned char *tok;
    size_t len;
    int64_t v = 0;
    int rc;
    if (!token(c, &tok, &len)) {
        c->ntok++;
        reject(c, LC_REJECT_FORMAT, "input ends where this is expected: ");
        msg_cat(c->res, what);
        return 1;
    }
    rc = parse_i64(tok, len, &v);
    if (rc == 1 || (rc == 0 && v < 0)) {
        reject(c, LC_REJECT_FORMAT, "not a non-negative integer: ");
        msg_cat(c->res, what);
        return 1;
    }
    if (rc == 2 || (uint64_t)v > (uint64_t)max) {
        reject(c, limit_status, "too large: ");
        msg_cat(c->res, what);
        return 1;
    }
    *out = (size_t)v;
    return 0;
}

/* the next token must be the number `want` (a label that the grammar fixes) */
static int expect_number(ctx *c, size_t want, const char *what) {
    const unsigned char *tok;
    size_t len;
    int64_t v = 0;
    if (!token(c, &tok, &len)) { c->ntok++; reject(c, LC_REJECT_FORMAT, "input ends where this is expected: "); }
    else if (parse_i64(tok, len, &v) != 0 || v < 0 || (uint64_t)v != (uint64_t)want) reject(c, LC_REJECT_FORMAT, "unexpected value of: ");
    else return 0;
    msg_cat(c->res, what);
    msg_cat(c->res, " (expected ");
    msg_cat_u(c->res, (uint64_t)want);
    msg_cat(c->res, ")");
    return 1;
}

/* `count` more tokens cannot fit in what is left of the input */
static int too_short_for(ctx *c, size_t count) {
    size_t left = (size_t)(c->end - c->cur);
    if (count > left / 2u + 1u) return reject(c, LC_REJECT_FORMAT, "input too short for the sizes it declares");
    return 0;
}

static void *alloc(ctx *c, size_t count, size_t size) {
    void *p = NULL;
    size_t bytes;
    if (__builtin_mul_overflow(count, size, &bytes) || (p = malloc(bytes ? bytes : 1u)) == NULL)
        reject(c, LC_REJECT_LIMIT, "out of memory");
    return p;
}

/* ------------------------------------------------------------------------------------------------ parsing */
static int parse_instance(ctx *c) {
    size_t n, jints = 0;
    if (expect(c, "leafcert") || expect(c, "1") || expect(c, "sites")) return 1;
    if (read_number(c, LC_MAX_SITES, &n, "number of sites", LC_REJECT_LIMIT)) return 1;
    if (n == 0) return reject(c, LC_REJECT_FORMAT, "no site");
    if (too_short_for(c, n)) return 1;
    c->n = n;
    c->npairs = n * (n - 1u) / 2u;
    c->res->sites = n;
    if (!(c->k = alloc(c, n, sizeof *c->k)) || !(c->koff = alloc(c, n + 1u, sizeof *c->koff)) ||
        !(c->jbase = alloc(c, n, sizeof *c->jbase)) || !(c->fixed = alloc(c, n, sizeof *c->fixed)) ||
        !(c->path = alloc(c, 2u * n, sizeof *c->path)))
        return 1;
    if (expect(c, "shape")) return 1;
    c->koff[0] = 0;
    for (size_t i = 0; i < n; i++) {
        if (read_number(c, LC_MAX_STATES, &c->k[i], "number of states of a site", LC_REJECT_LIMIT)) return 1;
        if (c->k[i] == 0) return reject(c, LC_REJECT_FORMAT, "a site without states (empty domain)");
        c->koff[i + 1u] = c->koff[i] + c->k[i];           /* <= 2^12 * 2^20 */
        c->fixed[i] = -1;
    }
    c->S = c->koff[n];
    for (size_t i = 0; i < n; i++) {                       /* jbase[i] = sum_{i' < i} k_i' * (k_{i'+1} + .. + k_{n-1}) */
        c->jbase[i] = jints;
        jints += c->k[i] * (c->S - c->koff[i + 1u]);       /* <= 2^20 * 2^32, and jints is checked every round */
        if (jints > LC_MAX_INTS) return reject(c, LC_REJECT_LIMIT, "instance too large");
    }
    if (c->S > LC_MAX_INTS) return reject(c, LC_REJECT_LIMIT, "instance too large");
    c->res->instance_integers = c->S + jints;
    if (expect(c, "bound") || read_value(c, &c->L)) return 1;
    c->res->bound = c->L;
    c->res->bound_valid = 1;
    if (too_short_for(c, c->S + jints)) return 1;
    if (!(c->H = alloc(c, c->S, sizeof *c->H)) || !(c->J = alloc(c, jints, sizeof *c->J))) return 1;
    for (size_t i = 0; i < n; i++)
        if (expect(c, "h") || expect_number(c, i, "site of a row of H") || read_values(c, c->H + c->koff[i], c->k[i])) return 1;
    for (size_t i = 0; i < n; i++)
        for (size_t j = i + 1u; j < n; j++) {
            int64_t *table = c->J + c->jbase[i] + c->k[i] * (c->koff[j] - c->koff[i + 1u]);
            if (expect(c, "j") || expect_number(c, i, "first site of a table of J") ||
                expect_number(c, j, "second site of a table of J") || read_values(c, table, c->k[i] * c->k[j]))
                return 1;
        }
    return 0;
}

static int parse_leaves(ctx *c) {
    size_t n = c->n, total;
    if (expect(c, "leaves")) return 1;
    if (read_number(c, LC_MAX_INTS, &c->T, "number of leaf certificates", LC_REJECT_LIMIT)) return 1;
    if (c->T == 0) return reject(c, LC_REJECT_FORMAT, "no leaf certificate");
    c->stride = n + c->npairs + (n - 1u) * c->S;           /* <= 2^12 + 2^23 + 2^12 * 2^26 */
    if (__builtin_mul_overflow(c->T, c->stride, &total) || total > LC_MAX_INTS)
        return reject(c, LC_REJECT_LIMIT, "leaf certificates too large");
    if (too_short_for(c, total)) return 1;
    c->res->leaf_certificates = c->T;
    c->res->cert_integers = total;
    if (!(c->leaves = alloc(c, total, sizeof *c->leaves)) || !(c->used = alloc(c, c->T, 1u))) return 1;
    memset(c->used, 0, c->T);
    for (size_t t = 0; t < c->T; t++) {
        int64_t *U = c->leaves + t * c->stride, *P = U + n, *M = P + c->npairs;
        if (expect(c, "leaf") || expect_number(c, t, "index of a leaf certificate")) return 1;
        if (expect(c, "u") || read_values(c, U, n)) return 1;
        if (expect(c, "p") || read_values(c, P, c->npairs)) return 1;
        for (size_t i = 0; i < n; i++)
            for (size_t j = 0; j < n; j++) {
                size_t block;
                if (j == i) continue;
                block = (j < i) ? j : j - 1u;              /* rank of j among the sites other than i */
                if (expect(c, "m") || expect_number(c, i, "first site of a message vector") ||
                    expect_number(c, j, "second site of a message vector") ||
                    read_values(c, M + (n - 1u) * c->koff[i] + block * c->k[i], c->k[i]))
                    return 1;
            }
    }
    return 0;
}

static int push_node(ctx *c, unsigned char kind, size_t val) {
    if (c->nnodes == c->ncap) {
        size_t cap = c->ncap ? 2u * c->ncap : 64u;
        unsigned char *nk;
        size_t *nv;
        if (cap > LC_MAX_NODES) return reject(c, LC_REJECT_LIMIT, "tree too large");
        nk = realloc(c->nkind, cap);
        if (nk) c->nkind = nk;
        nv = realloc(c->nval, cap * sizeof *nv);
        if (nv) c->nval = nv;
        if (!nk || !nv) return reject(c, LC_REJECT_LIMIT, "out of memory");
        c->ncap = cap;
    }
    c->nkind[c->nnodes] = kind;
    c->nval[c->nnodes] = val;
    c->nnodes++;
    return 0;
}

/* One node and its subtree.  The recursion is at most n + 1 deep: a branch needs a site that is not fixed. */
static int parse_node(ctx *c, size_t depth) {
    const unsigned char *tok;
    size_t len, site, count, t;
    if (!token(c, &tok, &len)) { c->ntok++; return reject(c, LC_REJECT_FORMAT, "input ends inside the tree"); }
    if (len == 1 && tok[0] == 'L') {
        if (read_number(c, c->T - 1u, &t, "index of a leaf certificate in the tree", LC_REJECT_FORMAT)) return 1;
        c->used[t] = 1;
        c->res->leaf_boxes++;
        if (depth > c->res->depth) c->res->depth = depth;
        return push_node(c, 0, t);
    }
    if (!(len == 1 && tok[0] == 'B')) return reject(c, LC_REJECT_FORMAT, "a node of the tree must begin with L or B");
    if (read_number(c, c->n - 1u, &site, "site of a branch", LC_REJECT_FORMAT)) return 1;
    if (c->fixed[site] != -1) return reject(c, LC_REJECT_FORMAT, "branch on a site that an ancestor has already fixed");
    if (read_number(c, SIZE_MAX / 2u, &count, "number of children of a branch", LC_REJECT_FORMAT)) return 1;
    if (count < c->k[site]) return reject(c, LC_REJECT_FORMAT, "branch with fewer children than states of its site (missing child)");
    if (count > c->k[site]) return reject(c, LC_REJECT_FORMAT, "branch with more children than states of its site (extra child)");
    if (push_node(c, 1, site)) return 1;
    for (size_t a = 0; a < count; a++) {
        if (expect_number(c, a, "state of a child (children must be the states 0, 1, .. in this order)")) return 1;
        c->fixed[site] = (int64_t)a;
        if (parse_node(c, depth + 1u)) return 1;
    }
    c->fixed[site] = -1;
    return 0;
}

static int parse_tree(ctx *c) {
    const unsigned char *tok;
    size_t len;
    if (expect(c, "tree") || parse_node(c, 0) || expect(c, "end")) return 1;
    if (token(c, &tok, &len)) return reject(c, LC_REJECT_FORMAT, "data after 'end'");
    for (size_t t = 0; t < c->T; t++)
        if (!c->used[t]) {
            c->ntok = 0;
            reject(c, LC_REJECT_FORMAT, "a leaf certificate is not referenced by the tree: ");
            msg_cat_u(c->res, t);
            return 1;
        }
    return 0;
}

/* ------------------------------------------------------------------------------------------------ checking */
#define ACC_ADD(c, x, y) do { if (__builtin_add_overflow((x), (acc_t)(y), &(x))) (c)->overflow = 1; } while (0)
#define ACC_SUB(c, x, y) do { if (__builtin_sub_overflow((x), (acc_t)(y), &(x))) (c)->overflow = 1; } while (0)

static void put128(i128 v, int64_t *hi, uint64_t *lo) {
    *lo = (uint64_t)v;
    *hi = (int64_t)(v >> 64);
}

/* record the failing inequality (or an overflow) of the leaf node being visited */
static int fail(ctx *c, int inequality, size_t t, int64_t i, int64_t a, int64_t j, int64_t b, i128 lhs, i128 rhs) {
    leafcert_result *r = c->res;
    r->status = c->overflow ? LC_REJECT_OVERFLOW : LC_REJECT_INEQUALITY;
    r->inequality = inequality;
    r->leaf = (int64_t)t;
    r->i = i; r->a = a; r->j = j; r->b = b;
    if (!c->overflow) {
        put128(lhs, &r->lhs_hi, &r->lhs_lo);
        put128(rhs, &r->rhs_hi, &r->rhs_lo);
    }
    r->path_len = (int64_t)c->depth;
    for (size_t q = 0; q < 2u * c->depth && q < c->path_cap; q++) c->path_out[q] = c->path[q];
    msg_set(r, c->overflow ? "an accumulator overflowed (64-bit build)" :
               inequality == LC_INEQ_SITE ? "U_i > H_i(a) + sum_j m_ij(a)" :
               inequality == LC_INEQ_PAIR ? "P2_ij > J_ij(a,b) - m_ij(a) - m_ji(b)" : "L > sum U + sum P2");
    return 1;
}

/* the leaf certificate t on the current box; 0 if all its inequalities hold */
static int check_leaf(ctx *c, size_t t) {
    const size_t n = c->n;
    const int64_t *U = c->leaves + t * c->stride, *P = U + n, *M = P + c->npairs;
    size_t p = 0;
    acc_t sum;
    /* (S) */
    for (size_t i = 0; i < n; i++) {
        const size_t ki = c->k[i];
        const size_t lo = c->fixed[i] < 0 ? 0u : (size_t)c->fixed[i], hi = c->fixed[i] < 0 ? ki : lo + 1u;
        const int64_t *Hi = c->H + c->koff[i], *Mi = M + (n - 1u) * c->koff[i];
        for (size_t a = lo; a < hi; a++) {
            sum = Hi[a];
            for (size_t block = 0; block + 1u < n; block++) {
                ACC_ADD(c, sum, Mi[block * ki + a]);
                c->res->additions++;
            }
            c->res->comparisons++;
            if (c->overflow || !((acc_t)U[i] <= sum))
                return fail(c, LC_INEQ_SITE, t, (int64_t)i, (int64_t)a, -1, -1, U[i], sum);
        }
    }
    /* (P) */
    for (size_t i = 0; i < n; i++) {
        const size_t ki = c->k[i];
        const size_t ilo = c->fixed[i] < 0 ? 0u : (size_t)c->fixed[i], ihi = c->fixed[i] < 0 ? ki : ilo + 1u;
        for (size_t j = i + 1u; j < n; j++, p++) {
            const size_t kj = c->k[j];
            const size_t jlo = c->fixed[j] < 0 ? 0u : (size_t)c->fixed[j], jhi = c->fixed[j] < 0 ? kj : jlo + 1u;
            const int64_t *Jij = c->J + c->jbase[i] + ki * (c->koff[j] - c->koff[i + 1u]);
            const int64_t *mij = M + (n - 1u) * c->koff[i] + (j - 1u) * ki;     /* j > i: rank j - 1 among the others */
            const int64_t *mji = M + (n - 1u) * c->koff[j] + i * kj;            /* i < j: rank i among the others     */
            for (size_t a = ilo; a < ihi; a++)
                for (size_t b = jlo; b < jhi; b++) {
                    sum = Jij[a * kj + b];
                    ACC_SUB(c, sum, mij[a]);
                    ACC_SUB(c, sum, mji[b]);
                    c->res->additions += 2u;
                    c->res->comparisons++;
                    if (c->overflow || !((acc_t)P[p] <= sum))
                        return fail(c, LC_INEQ_PAIR, t, (int64_t)i, (int64_t)a, (int64_t)j, (int64_t)b, P[p], sum);
                }
        }
    }
    /* (T) */
    sum = U[0];
    for (size_t i = 1; i < n; i++) { ACC_ADD(c, sum, U[i]); c->res->additions++; }
    for (size_t q = 0; q < c->npairs; q++) { ACC_ADD(c, sum, P[q]); c->res->additions++; }
    c->res->comparisons++;
    if (c->overflow || !((acc_t)c->L <= sum))
        return fail(c, LC_INEQ_TOTAL, t, -1, -1, -1, -1, c->L, sum);
    return 0;
}

/* visit the node at c->pos and its subtree (the tree has been validated: recursion at most n + 1 deep) */
static int visit(ctx *c) {
    const size_t node = c->pos++;
    size_t site;
    if (c->nkind[node] == 0) {
        if (check_leaf(c, c->nval[node])) return 1;
        c->res->visit++;
        return 0;
    }
    site = c->nval[node];
    for (size_t a = 0; a < c->k[site]; a++) {
        c->fixed[site] = (int64_t)a;
        c->path[2u * c->depth] = (int64_t)site;
        c->path[2u * c->depth + 1u] = (int64_t)a;
        c->depth++;
        if (visit(c)) return 1;
        c->depth--;
    }
    c->fixed[site] = -1;
    return 0;
}

/* ------------------------------------------------------------------------------------------------ interface */
int leafcert_check(const unsigned char *buf, size_t len, leafcert_result *res, int64_t *path_out, size_t path_cap) {
    ctx c;
    memset(&c, 0, sizeof c);
    memset(res, 0, sizeof *res);
    res->i = res->a = res->j = res->b = -1;
    res->leaf = -1;
    res->token = -1;
    c.cur = buf;
    c.end = buf + len;
    c.res = res;
    c.path_out = path_out;
    c.path_cap = path_out ? path_cap : 0u;
    if (!parse_instance(&c) && !parse_leaves(&c) && !parse_tree(&c)) {
        res->token = -1;
        if (!visit(&c)) msg_set(res, "all inequalities hold");
    }
    free(c.k); free(c.koff); free(c.jbase); free(c.H); free(c.J); free(c.leaves); free(c.used);
    free(c.nkind); free(c.nval); free(c.fixed); free(c.path);
    return (int)res->status;
}

size_t leafcert_result_size(void) { return sizeof(leafcert_result); }

int leafcert_acc_bits(void) { return LC_ACC_BITS; }

/* ------------------------------------------------------------------------------------------------ executable */
#ifdef LEAFCERT_MAIN
#include <stdio.h>

static void out_u(uint64_t v) {
    char buf[24];
    size_t at = sizeof buf;
    buf[--at] = '\0';
    do { buf[--at] = (char)('0' + (int)(v % 10u)); v /= 10u; } while (v != 0u);
    fputs(buf + at, stdout);
}

static void out_128(int64_t hi, uint64_t lo) {
    u128 mag;
    i128 v = (i128)(((u128)(uint64_t)hi << 64) | lo);
    char buf[48];
    size_t at = sizeof buf;
    buf[--at] = '\0';
    mag = v < 0 ? (u128)0 - (u128)v : (u128)v;
    do { buf[--at] = (char)('0' + (int)(mag % 10u)); mag /= 10u; } while (mag != 0u);
    if (v < 0) buf[--at] = '-';
    fputs(buf + at, stdout);
}

static void out_i(int64_t v) { out_128(v < 0 ? -1 : 0, (uint64_t)v); }

static int check_file(const char *name) {
    static const char *const words[] = { "", "inequality", "format", "range", "limit", "overflow" };
    static const char *const ineq[] = { "", "site", "pair", "total" };
    leafcert_result r;
    unsigned char *buf = NULL;
    size_t len = 0, cap = 0;
    int64_t *path;
    FILE *f = strcmp(name, "-") == 0 ? stdin : fopen(name, "rb");
    if (!f) { fprintf(stderr, "leafcert: cannot open %s\n", name); return 2; }
    for (;;) {
        size_t got;
        if (len == cap) {
            unsigned char *grown = realloc(buf, cap = cap ? 2u * cap : 65536u);
            if (!grown) { fprintf(stderr, "leafcert: out of memory reading %s\n", name); free(buf); if (f != stdin) fclose(f); return 2; }
            buf = grown;
        }
        got = fread(buf + len, 1, cap - len, f);
        len += got;
        if (got == 0) break;
    }
    if (ferror(f)) { fprintf(stderr, "leafcert: error reading %s\n", name); free(buf); if (f != stdin) fclose(f); return 2; }
    if (f != stdin) fclose(f);
    path = malloc(2u * LC_MAX_SITES * sizeof *path);
    if (!path) { fprintf(stderr, "leafcert: out of memory\n"); free(buf); return 2; }
    leafcert_check(buf, len, &r, path, 2u * LC_MAX_SITES);
    fputs(name, stdout);
    if (r.status == LC_ACCEPT) {
        fputs(": ACCEPT bound=", stdout); out_i(r.bound);
    } else {
        fputs(": REJECT ", stdout); fputs(words[r.status], stdout);
        if (r.status == LC_REJECT_INEQUALITY || r.status == LC_REJECT_OVERFLOW) {
            fputs(" inequality=", stdout); fputs(ineq[r.inequality], stdout);
            fputs(" visit=", stdout); out_i(r.visit);
            fputs(" leaf=", stdout); out_i(r.leaf);
            fputs(" path=", stdout);
            for (int64_t q = 0; q < r.path_len; q++) { if (q) fputs(",", stdout); out_i(path[2 * q]); fputs(":", stdout); out_i(path[2 * q + 1]); }
            fputs(" i=", stdout); out_i(r.i); fputs(" a=", stdout); out_i(r.a);
            fputs(" j=", stdout); out_i(r.j); fputs(" b=", stdout); out_i(r.b);
            if (r.status == LC_REJECT_INEQUALITY) {
                fputs(" lhs=", stdout); out_128(r.lhs_hi, r.lhs_lo);
                fputs(" rhs=", stdout); out_128(r.rhs_hi, r.rhs_lo);
            }
            fputs(" bound=", stdout); out_i(r.bound);
        } else {
            fputs(" token=", stdout); out_i(r.token);
        }
    }
    if (r.status == LC_ACCEPT || r.status == LC_REJECT_INEQUALITY || r.status == LC_REJECT_OVERFLOW) {
        fputs(" leaf_certificates=", stdout); out_u(r.leaf_certificates);
        fputs(" leaf_boxes=", stdout); out_u(r.leaf_boxes);
        fputs(" depth=", stdout); out_u(r.depth);
        fputs(" cert_integers=", stdout); out_u(r.cert_integers);
        fputs(" instance_integers=", stdout); out_u(r.instance_integers);
        fputs(" additions=", stdout); out_u(r.additions);
        fputs(" comparisons=", stdout); out_u(r.comparisons);
    }
    fputs(" # ", stdout); fputs(r.message, stdout); fputs("\n", stdout);
    free(path);
    free(buf);
    return r.status == LC_ACCEPT ? 0 : 1;
}

int main(int argc, char **argv) {
    int worst = 0;
    if (argc < 2) { fprintf(stderr, "usage: leafcert FILE...   (- for standard input)\n"); return 2; }
    for (int q = 1; q < argc; q++) {
        int rc = check_file(argv[q]);
        if (rc > worst) worst = rc;
    }
    return worst;
}
#endif
