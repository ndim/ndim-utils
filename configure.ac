AC_PREREQ(2.59)
AC_INIT([ndim utility collection], [0.0.0],
	[hun@n-dimensional.de], [ndim-utils])
AC_CONFIG_HEADER([include/config.h])
AC_CONFIG_SRCDIR(params/params.c)
AM_INIT_AUTOMAKE([gnu 1.8])

AM_MAINTAINER_MODE

AC_PROG_CC
AC_PROG_INSTALL

AC_CONFIG_FILES([
	Makefile
	cdburn/Makefile
	misc-scripts/Makefile
	params/Makefile
	])
AC_OUTPUT

cat<<EOF

Configuration:
  Package: $PACKAGE
  Version: $VERSION

  srcdir:  $srcdir
  CC:      $CC
  prefix:  $prefix
  bindir:  $bindir
EOF
