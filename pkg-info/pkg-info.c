#include <stdio.h>

#include "config.h"
#include "package-version.h"
#include "build-info.h"

int main()
{
  printf("%s %s - %s\n"
	 "Copyright (C) 1998-%s Hans Ulrich Niedermann\n\n"
	 "Revision:\n  %s\n"
	 "Build date:\n  %s\n"
	 "Bugreports:\n  %s\n"
	 "%s"
	 ,
	 PACKAGE_TARNAME,
	 PACKAGE_VERSION,
	 PACKAGE_NAME,

	 DATE_YEAR,

         TLA_REVISION,
	 BUILD_DATE,
	 PACKAGE_BUGREPORT,
	 ""
	 );
  return 0;
}
