/**
 * writes file "one.tmp" into current directory until
 * error occurs (disk full, quota exceeded)
 */

#include "compiler-stuff.h"
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE (1 << 20)

int main(int UNUSED_PARM(argc), char UNUSED_PARM(*argv[]))
{

  FILE *file = fopen("one.tmp", "w");
  if (!file) {
    perror("fopen");
    return EXIT_FAILURE;
  }

  char *buf = malloc(BUFSIZE);
  if (!buf) {
    perror("malloc");
    return EXIT_FAILURE;
  }

  for (int i=0; i<BUFSIZE; i++) {
    buf[i]=i;
  }

  size_t count = 0;
  uint64_t blk = 0;
  unsigned int i = 0;
  do {

    /* Update counter in all 1K blocks to make them unique, preventing
     * filesystem deduplication to kick in. */
    for (char *p = buf; p < buf+BUFSIZE; p += 1024) {
      *((uint64_t *)p) = blk++;
    }

    count = fwrite(buf, sizeof(char), BUFSIZE, file);
    ++i;
  } while (count == BUFSIZE);
  printf("Finished. (count,i,blk) = (%zd,%u,%" PRIu64 ")\n", count, i, blk);

  free(buf);
  fclose(file);

  return EXIT_SUCCESS;
}
