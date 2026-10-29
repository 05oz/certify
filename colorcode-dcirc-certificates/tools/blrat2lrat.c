/* blrat2lrat.c -- stream a BINARY LRAT proof (CaDiCaL `--lrat` default) to TEXT LRAT on stdout.
 *
 * Written for the d = 15 proof (about 1e10 literals).  It is a format converter, not a checker, and it is
 * NOT trusted: both checkers replay its output against a CNF they read or regenerate themselves, so a
 * faulty conversion can only make a check fail.  On 2026-10-20 its output was byte-identical to CaDiCaL
 * 3.0.1's own text LRAT on five of the shipped instances (logs/converter_identity_2026-10-20.log).
 *
 * Binary step encoding: 'a' id lits... 0 hints... 0   |   'd' ids... 0
 * every signed x is the unsigned u = 2|x| + (x<0), written as a little-endian base-128 varint.
 * Text: "<id> <lits> 0 <hints> 0\n" and "<last-added-id> d <ids> 0\n"; before the first addition the
 * leading id of a deletion line is the formula's clause count (argv[1] = that count, default 0).
 *
 * Build:  cc -O2 -o blrat2lrat tools/blrat2lrat.c
 * Usage:  ./blrat2lrat NUM_INPUT_CLAUSES < NAME.blrat | gzip -1 > NAME.lrat.gz
 *         (as in REGENERATE.md; for the d = 15 proof NUM_INPUT_CLAUSES = 13932, the CNF's clause count)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static unsigned char ibuf[1 << 22];
static size_t ilen = 0, ipos = 0;

static int nextbyte(void) {
  if (ipos == ilen) {
    ilen = fread(ibuf, 1, sizeof ibuf, stdin);
    ipos = 0;
    if (ilen == 0) return -1;
  }
  return ibuf[ipos++];
}

static int64_t rd_signed(int *eof) {
  uint64_t u = 0; int shift = 0;
  for (;;) {
    int b = nextbyte();
    if (b < 0) { *eof = 1; return 0; }
    u |= (uint64_t)(b & 0x7f) << shift;
    if (b < 0x80) break;
    shift += 7;
    if (shift > 63) { fprintf(stderr, "varint too long\n"); exit(2); }
  }
  return (u & 1) ? -(int64_t)(u >> 1) : (int64_t)(u >> 1);
}

static char obuf[1 << 22];
static size_t opos = 0;
static void flush_out(void) { fwrite(obuf, 1, opos, stdout); opos = 0; }
static void put_i64(int64_t x) {
  char t[24]; int n = 0; uint64_t v;
  if (opos > sizeof obuf - 64) flush_out();
  if (x < 0) { obuf[opos++] = '-'; v = (uint64_t)(-x); } else v = (uint64_t)x;
  do { t[n++] = (char)('0' + v % 10); v /= 10; } while (v);
  while (n) obuf[opos++] = t[--n];
}
static void put_c(char c) { if (opos > sizeof obuf - 64) flush_out(); obuf[opos++] = c; }

int main(int argc, char **argv) {
  int64_t last = argc > 1 ? strtoll(argv[1], 0, 10) : 0;
  long long na = 0, nd = 0;
  int eof = 0;
  for (;;) {
    int tag = nextbyte();
    if (tag < 0) break;
    if (tag == 'a') {
      int64_t id = rd_signed(&eof); if (eof) goto trunc;
      put_i64(id); put_c(' ');
      for (int part = 0; part < 2; part++) {
        for (;;) {
          int64_t x = rd_signed(&eof); if (eof) goto trunc;
          if (x == 0) break;
          put_i64(x); put_c(' ');
        }
        put_c('0'); put_c(part == 0 ? ' ' : '\n');
      }
      last = id; na++;
    } else if (tag == 'd') {
      put_i64(last); put_c(' '); put_c('d'); put_c(' ');
      for (;;) {
        int64_t x = rd_signed(&eof); if (eof) goto trunc;
        if (x == 0) break;
        put_i64(x); put_c(' ');
      }
      put_c('0'); put_c('\n'); nd++;
    } else {
      flush_out(); fprintf(stderr, "unknown step tag byte %d after %lld additions\n", tag, na); return 3;
    }
  }
  flush_out();
  fprintf(stderr, "blrat2lrat: %lld additions, %lld deletion steps\n", na, nd);
  return 0;
trunc:
  flush_out(); fprintf(stderr, "blrat2lrat: TRUNCATED input after %lld additions\n", na); return 4;
}
