#include <stdio.h>

#include "config.h"
#include "pkg-info.h"

int main(int argc, char *argv[])
{
  printf("Package:    %s\n"
	 "Full name:  %s\n"
	 "Short name: %s\n"
	 "PVersion:   %s\n"
	 "Version:    %s\n"
	 "TLA Rev:    %s\n"
	 "Bugreports: %s\n"
	 ,
	 PACKAGE,
	 PACKAGE_NAME,
	 PACKAGE_TARNAME,
	 PACKAGE_VERSION,
	 VERSION,
	 TLA_REVISION,
	 PACKAGE_BUGREPORT
	 );
  return 0;
}
