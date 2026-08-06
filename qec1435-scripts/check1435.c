/* check1435.c — exact distance checker + annealer for [[14,k]] stabilizer codes
 * in binary symplectic representation.
 *
 * Vector = 28-bit word: bits 0..13 X-part a, bits 14..27 Z-part b.
 * sp(u,v) = parity(|u_a&v_b| + |u_b&v_a|); w(v) = popcount(a|b).
 * A [[14,k]] code = isotropic subspace S, dim s = 14-k.
 * d = min symplectic weight over S^perp \ S  (S^perp dim 14+k).
 *
 * Modes:
 *   check  <file>            file: rows "[1 0 ...|0 1 ...]" or hex words, one per line.
 *                            Prints rank, isotropy, exact d, weight profile.
 *   batch  <s>               read candidates from stdin: each line s hex words.
 *                            For each: verify isotropy+rank, compute d with early
 *                            abort at wt<=4; print "i d" (d = exact if >=5, else
 *                            the abort weight found, upper bound). Survivors d>=5
 *                            get exact d. Prints generators of any d>=5 hit.
 *   anneal <seed> <iters> <restarts>   transvection annealing for [[14,3]] d=5.
 *   anneal2 <seed> <iters> <restarts>  anneal [[14,2]] d=5 codes; for each found,
 *                            sweep all 4095 hyperplanes as [[14,3]] candidates.
 *   walk2 <seedfile> <seed> <steps>    d>=5-preserving transvection random walk
 *                            on [[14,2,5]] codes from a 12-row seed matrix;
 *                            per state, syndrome-coverage test (0-covered
 *                            nonzero syndrome <=> [[14,3,5]] hyperplane, then
 *                            exact re-verify). Prints min-coverage progress.
 *
 * cc -O2 -o check1435 check1435.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define NQ 14
#define MASKA ((1u<<NQ)-1u)

static inline int pop(uint32_t x){ return __builtin_popcount(x); }
static inline int sw(uint32_t v){ uint32_t a=v&MASKA, b=v>>NQ; return pop(a|b); }
static inline uint32_t swap_halves(uint32_t v){ return ((v&MASKA)<<NQ)|(v>>NQ); }
static inline int sp(uint32_t u, uint32_t v){ return pop(u & swap_halves(v)) & 1; }

/* rank of set of words */
static int rank_of(const uint32_t *v, int n){
    uint32_t piv[32]; int r=0;
    for(int i=0;i<n;i++){
        uint32_t x=v[i];
        for(int j=0;j<r;j++){ uint32_t hp = piv[j]; uint32_t hb = 1u<<(31-__builtin_clz(hp)); if(x&hb) x^=hp; }
        if(x) piv[r++]=x;
    }
    return r;
}

/* nullspace over F2 of the linear forms v -> parity(v & rows[i]), i<m, in dim=28.
 * out gets basis vectors; returns dim of nullspace. */
static int nullspace(const uint32_t *rows, int m, uint32_t *out){
    /* Build 28 columns? Simpler: Gaussian elimination on m x 28 matrix, track free vars. */
    uint32_t R[32]; int nr=0;
    for(int i=0;i<m;i++) R[nr++]=rows[i];
    /* row reduce */
    int pivcol[32]; int r=0;
    for(int c=0;c<28 && r<nr;c++){
        int p=-1;
        for(int i=r;i<nr;i++) if(R[i]&(1u<<c)){p=i;break;}
        if(p<0) continue;
        uint32_t t=R[r];R[r]=R[p];R[p]=t;
        for(int i=0;i<nr;i++) if(i!=r && (R[i]&(1u<<c))) R[i]^=R[r];
        pivcol[r++]=c;
    }
    int isfree[28]; for(int c=0;c<28;c++) isfree[c]=1;
    for(int i=0;i<r;i++) isfree[pivcol[i]]=0;
    int nd=0;
    for(int c=0;c<28;c++) if(isfree[c]){
        uint32_t v = 1u<<c;
        for(int i=0;i<r;i++) if(R[i]&(1u<<c)) v |= 1u<<pivcol[i];
        out[nd++]=v;
    }
    return nd;
}

/* Given S basis (s vectors, independent, isotropic), compute logical reps L
 * (dim 28-2s... no: dim S^perp = 28-s; logicals = (28-s)-s = 28-2s).
 * Returns number of logicals, fills L. */
static int logicals(const uint32_t *S, int s, uint32_t *L){
    uint32_t rows[32];
    for(int i=0;i<s;i++) rows[i]=swap_halves(S[i]);
    uint32_t NS[32]; int nd = nullspace(rows, s, NS); /* basis of S^perp */
    /* extend S-basis to S^perp basis: greedy rank */
    uint32_t piv[32]; int r=0;
    for(int i=0;i<s;i++){ uint32_t x=S[i];
        for(int j=0;j<r;j++){ uint32_t hp=piv[j]; uint32_t hb=1u<<(31-__builtin_clz(hp)); if(x&hb) x^=hp; }
        if(x) piv[r++]=x; else { fprintf(stderr,"S not independent\n"); exit(2);} }
    int nl=0;
    for(int i=0;i<nd;i++){ uint32_t x=NS[i], orig=NS[i];
        for(int j=0;j<r;j++){ uint32_t hp=piv[j]; uint32_t hb=1u<<(31-__builtin_clz(hp)); if(x&hb) x^=hp; }
        if(x){ piv[r++]=x; L[nl++]=orig; }
    }
    return nl;
}

/* exact min weight over S^perp \ S. s = dim S, nl = #logicals.
 * early_abort: if >0, return as soon as some weight <= early_abort is found
 * (returned value is that weight, an upper bound on d). Else exact. */
static int mindist(const uint32_t *S, int s, const uint32_t *L, int nl, int early_abort){
    int best = 999;
    uint32_t nS = 1u<<s;
    for(uint32_t c=1;c<(1u<<nl);c++){
        uint32_t v0=0;
        for(int j=0;j<nl;j++) if(c&(1u<<j)) v0^=L[j];
        /* gray code walk over span(S) */
        uint32_t v=v0;
        int w=sw(v); if(w<best){best=w; if(early_abort && best<=early_abort) return best;}
        for(uint32_t g=1;g<nS;g++){
            v ^= S[__builtin_ctz(g)];
            w = sw(v); if(w<best){best=w; if(early_abort && best<=early_abort) return best;}
        }
    }
    return best;
}

/* count of vectors of weight <= 4 in S^perp\S (annealing objective, weighted) */
static long objective(const uint32_t *S, int s, const uint32_t *L, int nl){
    long f=0;
    uint32_t nS=1u<<s;
    for(uint32_t c=1;c<(1u<<nl);c++){
        uint32_t v0=0;
        for(int j=0;j<nl;j++) if(c&(1u<<j)) v0^=L[j];
        uint32_t v=v0; int w=sw(v); if(w<=4) f += (5-w)*(5-w);
        for(uint32_t g=1;g<nS;g++){
            v ^= S[__builtin_ctz(g)];
            w=sw(v); if(w<=4) f += (5-w)*(5-w);
        }
    }
    return f;
}

static int check_isotropic(const uint32_t *S, int s){
    for(int i=0;i<s;i++) for(int j=i+1;j<s;j++) if(sp(S[i],S[j])) return 0;
    return 1;
}

static void print_code(const uint32_t *S, int s, FILE *f){
    for(int i=0;i<s;i++) fprintf(f,"%07x%c",S[i], i==s-1?'\n':' ');
}

/* ---------- parsing ---------- */
static int parse_rowline(const char *line, uint32_t *out){
    /* accept "[1 0 ...|...]" bit rows */
    int bits[28]; int nb=0;
    for(const char *p=line;*p;p++){
        if(*p=='0'||*p=='1'){ if(nb<28) bits[nb]= *p-'0'; nb++; }
    }
    if(nb!=28) return 0;
    uint32_t v=0;
    for(int i=0;i<14;i++){ if(bits[i]) v|=1u<<i; if(bits[14+i]) v|=1u<<(14+i); }
    *out=v; return 1;
}

/* ---------- RNG (xoshiro-ish splitmix) ---------- */
static uint64_t rngstate;
static uint64_t rnd64(void){
    uint64_t z = (rngstate += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z>>30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z>>27)) * 0x94d049bb133111ebULL;
    return z ^ (z>>31);
}
static uint32_t rnd28(void){ return (uint32_t)(rnd64() & ((1u<<28)-1)); }

/* random low-symplectic-weight vector: 1..4 qubits, random nonzero Pauli each */
static uint32_t rnd_lowwt(void){
    uint64_t r = rnd64();
    int nq = 1 + (int)(r&3); r>>=2;          /* 1..4 qubits */
    uint32_t v=0;
    for(int i=0;i<nq;i++){
        int qb = (int)(rnd64()%NQ);
        int pauli = 1 + (int)(rnd64()%3);    /* 1=X,2=Z,3=Y */
        if(pauli&1) v |= 1u<<qb;
        if(pauli&2) v |= 1u<<(NQ+qb);
    }
    return v;
}

/* random isotropic subspace of dim s: greedy — add random vectors from current
 * symplectic-orthogonal space */
static void random_isotropic(uint32_t *S, int s){
    int have=0;
    while(have<s){
        uint32_t v=rnd28(); if(!v) continue;
        /* project constraint: need sp(v,S_i)=0 for all i; fix by adding correcting vectors?
           simpler: rejection with repair — find any vector in nullspace of current rows */
        uint32_t rows[32]; for(int i=0;i<have;i++) rows[i]=swap_halves(S[i]);
        uint32_t NS[32]; int nd=nullspace(rows,have,NS);
        /* random combo of nullspace basis */
        uint32_t w=0; for(int i=0;i<nd;i++) if(rnd64()&1) w^=NS[i];
        if(!w) continue;
        /* check independence from S */
        uint32_t tmp[32]; for(int i=0;i<have;i++) tmp[i]=S[i]; tmp[have]=w;
        if(rank_of(tmp,have+1)!=have+1) continue;
        S[have++]=w;
    }
}

/* apply transvection T_v to all generators: x -> x + sp(x,v) v */
static void transvect(uint32_t *S, int s, uint32_t v){
    for(int i=0;i<s;i++) if(sp(S[i],v)) S[i]^=v;
}

/* objective + remember a random offending (weight<=4) vector */
static long objective_off(const uint32_t *S, int s, const uint32_t *L, int nl,
                          uint32_t *offender){
    long f=0; long noff=0;
    uint32_t nS=1u<<s;
    for(uint32_t c=1;c<(1u<<nl);c++){
        uint32_t v0=0;
        for(int j=0;j<nl;j++) if(c&(1u<<j)) v0^=L[j];
        uint32_t v=v0; int w=sw(v);
        if(w<=4){ f += (5-w)*(5-w); noff++; if((rnd64()%noff)==0) *offender=v; }
        for(uint32_t g=1;g<nS;g++){
            v ^= S[__builtin_ctz(g)];
            w=sw(v);
            if(w<=4){ f += (5-w)*(5-w); noff++; if((rnd64()%noff)==0) *offender=v; }
        }
    }
    return f;
}

/* exhaustive greedy descent over all transvections of symplectic weight <= 3;
 * accepts strict improvements, repeats to a local minimum. Returns final f. */
static long polish(uint32_t *S, int s, uint32_t *L, int nl){
    uint32_t off;
    long f = objective_off(S,s,L,nl,&off);
    int improved = 1;
    while(f>0 && improved){
        improved = 0;
        for(int q1=0;q1<NQ && !improved;q1++) for(int p1=1;p1<4 && !improved;p1++){
            uint32_t v1 = ((p1&1)?(1u<<q1):0) | ((p1&2)?(1u<<(NQ+q1)):0);
            for(int q2=q1;q2<NQ && !improved;q2++){
                int p2max = (q2==q1)?1:4; /* q2==q1 sentinel: single-qubit v */
                for(int p2=(q2==q1)?0:1; p2<p2max && !improved; p2++){
                    uint32_t v2 = (q2==q1)?0:(((p2&1)?(1u<<q2):0) | ((p2&2)?(1u<<(NQ+q2)):0));
                    for(int q3=q2;q3<NQ && !improved;q3++){
                        int p3max = (q3==q2)?1:4;
                        for(int p3=(q3==q2)?0:1; p3<p3max && !improved; p3++){
                            uint32_t v3 = (q3==q2)?0:(((p3&1)?(1u<<q3):0) | ((p3&2)?(1u<<(NQ+q3)):0));
                            uint32_t v = v1|v2|v3;
                            uint32_t Sn[16], Ln[16]; uint32_t o2;
                            memcpy(Sn,S,sizeof(uint32_t)*s);
                            memcpy(Ln,L,sizeof(uint32_t)*nl);
                            transvect(Sn,s,v); transvect(Ln,nl,v);
                            long f2 = objective_off(Sn,s,Ln,nl,&o2);
                            if(f2<f){
                                memcpy(S,Sn,sizeof(uint32_t)*s);
                                memcpy(L,Ln,sizeof(uint32_t)*nl);
                                f=f2; improved=1;
                            }
                        }
                    }
                }
            }
        }
    }
    return f;
}

static int anneal_run(int s, long iters, double t0, double t1, uint32_t *Sout){
    /* returns 1 if objective 0 reached.
     * Moves are symplectic transvections T_v applied jointly to S and its
     * logical complement (T_v is symplectic, so S'^perp = T_v S^perp and the
     * updated logicals stay a complement: no nullspace recomputation).
     * Half the moves target a current low-weight offender u: pick v with
     * sp(u,v)=1 so the offender gets moved. Reheat cycles: 4 linear ramps. */
    uint32_t S[16], L[16];
    random_isotropic(S,s);
    int nl_expect = 28-2*s;
    int nl = logicals(S,s,L); if(nl!=nl_expect){ return 0; }
    uint32_t off=0;
    long f = objective_off(S,s,L,nl,&off);
    uint32_t bestS[16]; long bestf=f; memcpy(bestS,S,sizeof(uint32_t)*s);
    int ncycles = 4;
    long cyclen = iters/ncycles + 1;
    long last_polish = -100000;
    for(long it=0; it<iters && f>0; it++){
        double prog = (double)(it % cyclen)/(double)cyclen;
        double T = t0*(1.0-prog) + t1*prog;
        uint32_t v;
        uint64_t coin = rnd64()&3;
        if(f>0 && off && coin==0){
            /* targeted: low-weight v anticommuting with the offender */
            int tries=0;
            do { v=rnd_lowwt(); tries++; } while((!v || sp(off,v)==0) && tries<12);
            if(!v || sp(off,v)==0) continue;
        } else if(coin==1){
            v=rnd28(); if(!v) continue;      /* occasional big jump */
        } else {
            v=rnd_lowwt(); if(!v) continue;  /* local move */
        }
        uint32_t Snew[16], Ln[16];
        memcpy(Snew,S,sizeof(uint32_t)*s);
        memcpy(Ln,L,sizeof(uint32_t)*nl);
        transvect(Snew,s,v);
        transvect(Ln,nl,v);
        uint32_t off2=0;
        long f2 = objective_off(Snew,s,Ln,nl,&off2);
        long df = f2-f;
        if(df<=0 || (T>0 && ((double)(rnd64()>>11)/9007199254740992.0) < exp(-(double)df/T))){
            memcpy(S,Snew,sizeof(uint32_t)*s);
            memcpy(L,Ln,sizeof(uint32_t)*nl);
            f=f2; off=off2;
            if(f<bestf){bestf=f; memcpy(bestS,S,sizeof(uint32_t)*s);}
            if(f>0 && f<=2 && it-last_polish>=5000){
                last_polish = it;
                long fp = polish(S,s,L,nl);
                if(fp<f){ f=fp; if(f<bestf){bestf=f; memcpy(bestS,S,sizeof(uint32_t)*s);} }
                if(f==0) break;
            }
        }
    }
    memcpy(Sout,bestS,sizeof(uint32_t)*s);
    return bestf==0;
}

#include <math.h>


/* ---------- walk2 helpers ---------- */
static uint32_t g_errs[100000]; static int g_ne=0;
static int g_cnt[4096];

static void build_errs(void){
    int ne=0;
    for(int q1=0;q1<NQ;q1++) for(int p1=1;p1<4;p1++){
        uint32_t v1=((p1&1)?(1u<<q1):0)|((p1&2)?(1u<<(NQ+q1)):0);
        g_errs[ne++]=v1;
        for(int q2=q1+1;q2<NQ;q2++) for(int p2=1;p2<4;p2++){
            uint32_t v2=v1|(((p2&1)?(1u<<q2):0)|((p2&2)?(1u<<(NQ+q2)):0));
            g_errs[ne++]=v2;
            for(int q3=q2+1;q3<NQ;q3++) for(int p3=1;p3<4;p3++){
                uint32_t v3=v2|(((p3&1)?(1u<<q3):0)|((p3&2)?(1u<<(NQ+q3)):0));
                g_errs[ne++]=v3;
                for(int q4=q3+1;q4<NQ;q4++) for(int p4=1;p4<4;p4++){
                    g_errs[ne++]=v3|(((p4&1)?(1u<<q4):0)|((p4&2)?(1u<<(NQ+q4)):0));
                }
            }
        }
    }
    g_ne=ne;
}

/* score of a d>=5 [[14,2]] code: min syndrome coverage over nonzero syndromes;
 * score = mn*10000 - (#syndromes at mn), minimize; mn==0 means [[14,3,5]] found */
static long score12(const uint32_t *TT, int *mn_out, int *us_out){
    uint32_t mm[12];
    for(int i=0;i<12;i++) mm[i]=swap_halves(TT[i]);
    memset(g_cnt,0,sizeof g_cnt);
    for(int e=0;e<g_ne;e++){
        uint32_t vv=g_errs[e]; int syn=0;
        for(int i=0;i<12;i++) syn |= (pop(vv&mm[i])&1)<<i;
        g_cnt[syn]++;
    }
    int mn=1<<30, us=-1;
    for(int y=1;y<4096;y++){
        int c=g_cnt[y];
        if(c<mn){ mn=c; us=y; }
    }
    /* tie-break: sum of the 8 smallest nonzero-syndrome counts */
    int small[8]; for(int i=0;i<8;i++) small[i]=1<<30;
    for(int y=1;y<4096;y++){
        int c=g_cnt[y];
        if(c<small[7]){
            int i=7;
            while(i>0 && small[i-1]>c){ small[i]=small[i-1]; i--; }
            small[i]=c;
        }
    }
    long s8=0; for(int i=0;i<8;i++) s8+=small[i];
    *mn_out=mn; *us_out=us;
    return (long)mn*100000 + s8;
}

int main(int argc, char **argv){
    if(argc<2){ fprintf(stderr,"usage: %s check|batch|anneal|anneal2 ...\n",argv[0]); return 1; }

    if(!strcmp(argv[1],"check")){
        FILE *f = fopen(argv[2],"r"); if(!f){perror("open");return 1;}
        char line[4096]; uint32_t S[32]; int s=0;
        while(fgets(line,sizeof line,f)){
            uint32_t v;
            if(strchr(line,'|') && parse_rowline(line,&v)) S[s++]=v;
            else if(strspn(line,"0123456789abcdefABCDEF \n")==strlen(line) && strlen(line)>2){
                char *tok=strtok(line," \n");
                while(tok){ S[s++]=(uint32_t)strtoul(tok,NULL,16); tok=strtok(NULL," \n"); }
            }
        }
        fclose(f);
        printf("read %d generators\n",s);
        int r=rank_of(S,s); printf("rank %d\n",r);
        printf("isotropic %d\n",check_isotropic(S,s));
        if(r!=s || !check_isotropic(S,s)) return 1;
        uint32_t L[32]; int nl=logicals(S,s,L);
        printf("logical dim %d (k=%d)\n",nl,nl/2);
        int d=mindist(S,s,L,nl,0);
        printf("distance %d\n",d);
        return 0;
    }

    if(!strcmp(argv[1],"batch")){
        int s=atoi(argv[2]);
        char line[4096]; long idx=0, nhit=0, nbad=0;
        uint32_t S[32], L[32];
        while(fgets(line,sizeof line,stdin)){
            int ns=0; char *tok=strtok(line," \n");
            while(tok && ns<32){ S[ns++]=(uint32_t)strtoul(tok,NULL,16); tok=strtok(NULL," \n"); }
            if(ns!=s){ nbad++; idx++; continue; }
            if(rank_of(S,s)!=s || !check_isotropic(S,s)){ nbad++; idx++; continue; }
            int nl=logicals(S,s,L);
            if(nl!=28-2*s){ nbad++; idx++; continue; }
            int d=mindist(S,s,L,nl,4);
            if(d>=5){
                d=mindist(S,s,L,nl,0);
                printf("HIT idx=%ld d=%d gens: ",idx,d); print_code(S,s,stdout); fflush(stdout);
                nhit++;
            }
            idx++;
            if(idx%100000==0) fprintf(stderr,"...%ld processed, %ld hits, %ld bad\n",idx,nhit,nbad);
        }
        fprintf(stderr,"batch done: %ld candidates, %ld with d>=5, %ld bad/skipped\n",idx,nhit,nbad);
        printf("SUMMARY candidates=%ld hits=%ld bad=%ld\n",idx,nhit,nbad);
        return 0;
    }

    if(!strcmp(argv[1],"anneal")){
        rngstate = strtoull(argv[2],NULL,10);
        long iters = atol(argv[3]); int restarts=atoi(argv[4]);
        for(int r0=0;r0<restarts;r0++){
            uint32_t S[16];
            if(anneal_run(11,iters,8.0,0.05,S)){
                printf("FOUND d>=5 [[14,3]] gens: "); print_code(S,11,stdout);
                uint32_t L[16]; int nl=logicals(S,11,L);
                printf("verified d=%d\n",mindist(S,11,L,nl,0));
                return 0;
            }
            uint32_t L[16]; int nl=logicals(S,11,L);
            long f=objective(S,11,L,nl);
            printf("restart %d best_obj %ld\n",r0,f); fflush(stdout);
        }
        return 3;
    }

    if(!strcmp(argv[1],"anneal2")){
        /* anneal [[14,2]] (s=12) to d>=5, then sweep 4095 hyperplanes for [[14,3,5]] */
        rngstate = strtoull(argv[2],NULL,10);
        long iters = atol(argv[3]); int restarts=atoi(argv[4]);
        long n142=0;
        for(int r0=0;r0<restarts;r0++){
            uint32_t T[16];
            if(!anneal_run(12,iters,8.0,0.05,T)){
                uint32_t L[16]; int nl=logicals(T,12,L);
                printf("restart %d best_obj %ld\n",r0,objective(T,12,L,nl)); fflush(stdout);
                continue;
            }
            n142++;
            printf("found [[14,2,5]] #%ld: ",n142); print_code(T,12,stdout);
            /* hyperplanes: kernel of nonzero functional phi on F2^12 */
            for(uint32_t phi=1;phi<4096;phi++){
                uint32_t S[16]; int ns=0;
                /* basis of kernel: pick pivot bit j0 = lowest set bit of phi;
                   for each i != j0: if phi_i=1 -> T_i + T_j0 else T_i */
                int j0=__builtin_ctz(phi);
                for(int i=0;i<12;i++){
                    if(i==j0) continue;
                    uint32_t g = T[i];
                    if(phi&(1u<<i)) g ^= T[j0];
                    S[ns++]=g;
                }
                uint32_t L2[16]; int nl2=logicals(S,11,L2);
                if(nl2!=6) continue;
                int d=mindist(S,11,L2,nl2,4);
                if(d>=5){
                    d=mindist(S,11,L2,nl2,0);
                    printf("HIT [[14,3,%d]] from hyperplane %u: ",d,phi);
                    print_code(S,11,stdout);
                    return 0;
                }
            }
            printf("no d>=5 hyperplane in #%ld\n",n142); fflush(stdout);
        }
        printf("SUMMARY found_1425=%ld no_1435\n",n142);
        return 3;
    }

    if(!strcmp(argv[1],"walk2")){
        /* d>=5-preserving random walk on [[14,2,5]] codes starting from a seed
         * file; at every accepted state, syndrome-coverage test: a [[14,3,5]]
         * hyperplane exists iff some nonzero 12-bit syndrome is NOT hit by any
         * Pauli error of symplectic weight <= 4.
         * usage: walk2 <seedfile> <seed> <steps>  */
        FILE *f = fopen(argv[2],"r"); if(!f){perror("open");return 1;}
        char line[4096]; uint32_t T[16]; int s=0;
        while(fgets(line,sizeof line,f)){
            uint32_t v;
            if(strchr(line,'|') && parse_rowline(line,&v)) T[s++]=v;
        }
        fclose(f);
        if(s!=12){ fprintf(stderr,"seed must have 12 generators, got %d\n",s); return 1; }
        rngstate = strtoull(argv[3],NULL,10);
        long steps = atol(argv[4]);
        uint32_t L[16]; int nl=logicals(T,12,L);
        if(nl!=4 || !check_isotropic(T,12)){ fprintf(stderr,"bad seed\n"); return 1; }
        if(mindist(T,12,L,nl,0)<5){ fprintf(stderr,"seed distance <5\n"); return 1; }

        build_errs(); int ne=g_ne;
        fprintf(stderr,"walk2: %d low-weight errors\n",ne);
        long acc=0; int bestun=1<<30;
        uint32_t Tw[16]; memcpy(Tw,T,sizeof(uint32_t)*12);

        int mn, unsyn;
        int hit_resume = 0;
        long fs = score12(Tw,&mn,&unsyn);
        if(mn==0){ hit_resume=0; goto hit; }
        for(long st=0; st<steps; st++){
            if(0){ resume: ; }
            uint32_t v = rnd_lowwt(); if(!v) continue;
            uint32_t Tn[16], Ln2[16];
            memcpy(Tn,Tw,sizeof(uint32_t)*12);
            transvect(Tn,12,v);
            int nl2=logicals(Tn,12,Ln2); if(nl2!=4) continue;
            if(mindist(Tn,12,Ln2,nl2,4)<5) continue;
            int mn2, us2;
            long f2 = score12(Tn,&mn2,&us2);
            /* lexicographic-with-tolerance: never worsen min level; within a
               level allow the low-tail mass to rise slightly (diffusion) */
            if(mn2<mn || (mn2==mn && f2<=fs+2) || (mn2==mn+1 && st%5==0)){
                memcpy(Tw,Tn,sizeof(uint32_t)*12);
                fs=f2; mn=mn2; unsyn=us2; acc++;
                if(mn<bestun){ bestun=mn;
                    fprintf(stderr,"step %ld acc %ld min-coverage %d (x%ld)\n",
                            st,acc,mn,fs%100000L); }
                if(mn==0){ hit_resume=1; goto hit; }
            }
        }
        printf("SUMMARY steps=%ld accepted=%ld best_min_coverage=%d no_hit\n",
               steps,acc,bestun);
        return 3;
    hit:
        {
            /* candidate syndrome uncovered; verify the hyperplane code exactly
               (an impure T can still break it via low-weight stabilizers with
               phi=1, which the syndrome test does not see) */
            int j0=-1;
            for(int i=0;i<12;i++) if(unsyn>>i&1){ j0=i; break; }
            uint32_t Sg[16]; int nsg=0;
            for(int i=0;i<12;i++){ if(i==j0) continue;
                uint32_t g=Tw[i]; if(unsyn>>i&1) g^=Tw[j0]; Sg[nsg++]=g; }
            uint32_t L3[16]; int nl3=logicals(Sg,11,L3);
            int dS = mindist(Sg,11,L3,nl3,0);
            if(dS>=5){
                printf("HIT syndrome %d uncovered on code: ",unsyn);
                print_code(Tw,12,stdout);
                printf("CONFIRMED [[14,3,%d]] gens: ",dS);
                print_code(Sg,11,stdout);
                fflush(stdout);
                return 0;
            }
            fprintf(stderr,"false hit (impure T, d=%d); continuing\n",dS);
            if(hit_resume) goto resume;
            return 4;
        }
    }

    fprintf(stderr,"unknown mode\n");
    return 1;
}
