#include <stdio.h>

#include "compiler-stuff.h"

#include "binary-test.h"


static
void by_start_and_end(void)
{
  fputs("S&E: BEGIN\n", stdout);
  for (const char *p=data_start; p<data_end; ++p) {
    fputc(*p, stdout);
  }
  fputs("S&E: END\n", stdout);
}


static
void by_start_and_size(void)
{
  fputs("S&S: BEGIN\n", stdout);
  const ssize_t written = fwrite(data_start, 1, data_size, stdout);
  if (written < 0) {
    perror("fwrite");
  } else {
    const size_t u_written = written;
    if (u_written < data_size) {
      fputs("S&S: written less than everything\n", stdout);
    } else {
      fputs("S&S: written everything (or more)\n", stdout);
    }
  }
  fputs("S&S: END\n", stdout);
}


int main(UNUSED_PARM(int argc), UNUSED_PARM(char *argv[]))
{
  by_start_and_size();
  by_start_and_end();
  return 0;
}
