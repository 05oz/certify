/* tt3pack.c — exact maximum arc-disjoint TT3 (transitive triple) packing in tournaments.
 *
 * Input:  lines on stdin, each a string of C(n,2) chars '0'/'1' — gentourng default
 *         output (upper triangle row-by-row): char at position p(i,j) [i<j, rows
 *         i=0..n-2, j=i+1..n-1] is '1' iff arc i->j, '0' iff arc j->i.
 * Usage:  tt3pack n target
 *         target > 0 : per tournament, stop as soon as a packing of size >= target
 *                      is found (certified lower bound with witness);
 *                      if search exhausts below target, the exact maximum is known.
 *         target = 0 : full exact maximum for every input line.
 *
 * Output: one line per input:
 *         <lineno> <bits> <GE|MAX> <k> <i,j,k;i,j,k;...>
 *         GE k  : witness packing of k arc-disjoint TT3s found (k>=target)
 *         MAX k : search exhausted; k is the exact maximum (with witness)
 *
 * Exactness: DFS branches on a live free arc e (fewest free triples through it):
 *   either e is covered by one of its free triples, or e is left uncovered (dead).
 *   Bound: cnt + floor(live_free_arcs/3) <= best prunes. This enumerates all
 *   maximal packings implicitly => the returned MAX value is the true maximum.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, npairs, target;
static int pidx[16][16];            /* pair index i<j */
static int adj[16][16];             /* adj[i][j]=1 iff i->j */

typedef struct { uint64_t mask; int a,b,c; } Tri;
static Tri tris[256];
static int ntris;
static int tris_on_arc[64][64];     /* arc p -> list of triple indices */
static int ntris_on_arc[64];

static int best, found_stop;
static int curset[32], bestset[32];

static void dfs(uint64_t used, uint64_t dead, int cnt) {
    if (found_stop) return;
    if (cnt > best) {
        best = cnt;
        memcpy(bestset, curset, sizeof(int)*(size_t)cnt);
        if (target > 0 && best >= target) { found_stop = 1; return; }
    }
    uint64_t blocked = used | dead;
    /* close arcs with no free triple (improves the /3 bound) */
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int p = 0; p < npairs; p++) {
            if (blocked & (1ULL << p)) continue;
            int has = 0;
            for (int t = 0; t < ntris_on_arc[p]; t++)
                if (!(tris[tris_on_arc[p][t]].mask & blocked)) { has = 1; break; }
            if (!has) { blocked |= 1ULL << p; dead |= 1ULL << p; changed = 1; }
        }
    }
    int live_free = npairs - __builtin_popcountll(blocked);
    if (cnt + live_free/3 <= best) return;
    if (live_free == 0) return;
    /* pick live arc with fewest free triples (>=1 guaranteed) */
    int bestp = -1, bcnt = 1<<30;
    for (int p = 0; p < npairs; p++) {
        if (blocked & (1ULL << p)) continue;
        int c = 0;
        for (int t = 0; t < ntris_on_arc[p]; t++)
            if (!(tris[tris_on_arc[p][t]].mask & blocked)) c++;
        if (c < bcnt) { bcnt = c; bestp = p; if (c == 1) break; }
    }
    /* branch: cover bestp by each free triple */
    for (int t = 0; t < ntris_on_arc[bestp]; t++) {
        int ti = tris_on_arc[bestp][t];
        if (tris[ti].mask & blocked) continue;
        curset[cnt] = ti;
        dfs(used | tris[ti].mask, dead, cnt + 1);
        if (found_stop) return;
    }
    /* branch: leave bestp uncovered */
    dfs(used, dead | (1ULL << bestp), cnt);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s n target\n", argv[0]); return 2; }
    n = atoi(argv[1]); target = atoi(argv[2]);
    npairs = n*(n-1)/2;
    if (n < 3 || n > 11) { fprintf(stderr, "bad n\n"); return 2; }
    int p = 0;
    for (int i = 0; i < n; i++)
        for (int j = i+1; j < n; j++) pidx[i][j] = p++;
    char line[256];
    long lineno = 0;
    while (fgets(line, sizeof line, stdin)) {
        size_t len = strlen(line);
        while (len && (line[len-1]=='\n' || line[len-1]=='\r')) line[--len] = 0;
        if ((int)len != npairs) { if (len) fprintf(stderr, "line %ld: bad length %zu\n", lineno+1, len); continue; }
        lineno++;
        for (int i = 0; i < n; i++)
            for (int j = i+1; j < n; j++) {
                int b = line[pidx[i][j]] == '1';
                adj[i][j] = b; adj[j][i] = !b;
            }
        /* transitive triples */
        ntris = 0;
        memset(ntris_on_arc, 0, sizeof ntris_on_arc);
        for (int i = 0; i < n; i++)
            for (int j = i+1; j < n; j++)
                for (int k = j+1; k < n; k++) {
                    int a_ = adj[i][j], b_ = adj[j][k], c_ = adj[i][k];
                    /* cyclic iff (i->j->k->i) or (j->i, i->k, k->j) */
                    int cyc = (a_ && b_ && !c_) || (!a_ && !b_ && c_);
                    if (cyc) continue;
                    tris[ntris].mask = (1ULL<<pidx[i][j]) | (1ULL<<pidx[j][k]) | (1ULL<<pidx[i][k]);
                    tris[ntris].a = i; tris[ntris].b = j; tris[ntris].c = k;
                    ntris++;
                }
        for (int t = 0; t < ntris; t++) {
            Tri *tr = &tris[t];
            int q1 = pidx[tr->a][tr->b], q2 = pidx[tr->b][tr->c], q3 = pidx[tr->a][tr->c];
            tris_on_arc[q1][ntris_on_arc[q1]++] = t;
            tris_on_arc[q2][ntris_on_arc[q2]++] = t;
            tris_on_arc[q3][ntris_on_arc[q3]++] = t;
        }
        best = -1; found_stop = 0;
        dfs(0, 0, 0);
        printf("%ld %s %s %d ", lineno, line, (target > 0 && best >= target) ? "GE" : "MAX", best);
        for (int t = 0; t < best; t++) {
            Tri *tr = &tris[bestset[t]];
            printf("%d,%d,%d%c", tr->a, tr->b, tr->c, t+1==best ? '\n' : ';');
        }
        if (best == 0) printf("-\n");
    }
    fflush(stdout);
    return 0;
}
