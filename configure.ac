AC_PREREQ(2.53)
AC_INIT([ndim utilities], [0.0.0])
AC_CONFIG_SRCDIR(params/params.c)
AC_CONFIG_HEADERS(include/config.h)
AM_INIT_AUTOMAKE([gnu 1.8])

AM_MAINTAINER_MODE

AC_PROG_CC
AC_PROG_INSTALL

AC_CONFIG_FILES()
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
