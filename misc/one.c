/**
 * writes file "one.tmp" into current directory until 
 * error occurs (disk full, quota exceeded)
 */

#include "compiler-stuff.h"
#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE (1 << 20)

int main(int UNUSED_PARM(argc), char UNUSED_PARM(*argv[])) {
  FILE *file;
  char *buf;
  int i;
  size_t count;
  file = fopen("one.tmp","w");
  buf = malloc(BUFSIZE);
  if (!file || !buf) {
    printf("Error.");
    return(1);
  }
  for (i=0; i<BUFSIZE; i++) {
    buf[i]=i;
  }
  i = 0;
  do {
    count = fwrite(buf,sizeof(char),BUFSIZE,file);
    i++;
  } while (count == BUFSIZE);
  printf("Finished. (count,i) = (%d,%d)\n",count,i);
  fclose(file);
  free(buf);
  return 0;
}

/* arch-tag: 4c015a35-7193-4bbc-8c53-b86254656882 */
