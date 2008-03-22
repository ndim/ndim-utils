#include <stdio.h>

#include "package-version-internal.h"
#include "config.h"
#include "build-info.h"

int main()
{
  printf("%s %s - %s\n"
	 "Copyright (C) 1998-%s Hans Ulrich Niedermann\n\n"
	 "Built from:\n  %s\n"
	 "Build date:\n  %s\n"
	 "Bugreports:\n  %s\n"
	 "%s"
	 ,
	 PACKAGE_TARNAME,
	 PACKAGE_VERSION,
	 PACKAGE_NAME,

	 DATE_YEAR,

         PACKAGE_VERSION_INTERNAL,
	 BUILD_DATE,
	 PACKAGE_BUGREPORT,
	 ""
	 );
  /*
  printf("prefix %s\n"
	 "bindir %s\n"
	 "libdir %s\n",
	 prefix, bindir, libdir);
  */
  printf("Q_PREFIX %s\n"
	 "Q_BINDIR %s\n"
	 "Q_LIBDIR %s\n",
	 Q_PREFIX, Q_BINDIR, Q_LIBDIR);
  printf("UQ_PREFIX %s\n"
	 "UQ_BINDIR %s\n"
	 "UQ_LIBDIR %s\n",
	 UQ_PREFIX, UQ_BINDIR, UQ_LIBDIR);
  return 0;
}
