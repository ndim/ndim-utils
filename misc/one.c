/**
 * writes file "one.tmp" into current directory until
 * error occurs (disk full, quota exceeded)
 */

#include "compiler-stuff.h"
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
  int i = 0;
  do {
    count = fwrite(buf, sizeof(char), BUFSIZE, file);
    i++;
  } while (count == BUFSIZE);
  printf("Finished. (count,i) = (%zd,%d)\n", count, i);

  free(buf);
  fclose(file);

  return EXIT_SUCCESS;
}
