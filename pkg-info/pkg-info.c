#include <stdio.h>

#include "config.h"
#include "pkg-info.h"

int main(int argc, char *argv[])
{
  printf("%s %s - %s\n"
	 "Copyright (C) 1998-%s Hans Ulrich Niedermann\n\n"
	 "Bugreports:   %s\n"
	 "Build date:   %s\n"
	 "TLA Archive:  %s\n"
	 "TLA Revision: %s\n"
	 ,
	 PACKAGE_TARNAME,
	 PACKAGE_VERSION,
	 PACKAGE_NAME,
	 DATE_YEAR,
	 PACKAGE_BUGREPORT,
	 BUILD_DATE,
	 TLA_ARCHIVE,
	 TLA_REVISION
	 );
  return 0;
}
