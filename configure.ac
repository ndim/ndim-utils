########################################################################

AC_PREREQ(2.61)
AC_INIT([ndim utility collection],
        [m4_esyscmd([./build-helpers/package-version . version-stamp])],
        [https://github.com/ndim/ndim-utils/issues],
        [ndim-utils],
        [https://github.com/ndim/ndim-utils])
AC_CONFIG_AUX_DIR([auto-aux])
AC_CONFIG_HEADER([include/config.h])
AC_CONFIG_SRCDIR([pkg-info/pkg-info.c])
AC_CONFIG_MACRO_DIRS([auto-m4 m4])
AM_INIT_AUTOMAKE([
  -Wall
  -Werror
  foreign
  1.16
  no-dist-gzip
  dist-xz
  readme-alpha
  tar-pax
  subdir-objects
  std-options
])

########################################################################

AC_PROG_SED
AC_PROG_CC
dnl AC_PROG_CC_C99
AM_PROG_CC_C_O
AC_PROG_INSTALL

AC_LANG_WERROR

########################################################################

m4_pattern_forbid([NDIM_CHECK_])dnl
NDIM_CHECK_SYSTEM_CONFIG
NDIM_CHECK_HOTPLUG
NDIM_CHECK_CONFIGURATION

########################################################################

PKG_CHECK_MODULES([LIBSELINUX], [libselinux],
                  [have_libselinux=yes
                   AC_DEFINE([HAVE_LIBSELINUX], [1], [Whether libselinux is present])],
                  [have_libselinux=no])
AM_CONDITIONAL([HAVE_LIBSELINUX], [test "x$have_libselinux" = "xyes"])

########################################################################

AC_CHECK_FUNCS([getresuid getresgid])

########################################################################

pkgdocdir="${datadir}/doc/${PACKAGE_TARNAME}"
AC_SUBST(pkgdocdir)

########################################################################

AM_CPPFLAGS="$AM_CPPFLAGS -I\$(top_srcdir)/include"
AC_SUBST([AM_CPPFLAGS])

########################################################################

dnl AM_CFLAGS="$AM_CFLAGS -std=gnu99"
AM_CFLAGS="$AM_CFLAGS -std=gnu11"
AM_CFLAGS="$AM_CFLAGS -Wall"
AM_CFLAGS="$AM_CFLAGS -Wextra"
AM_CFLAGS="$AM_CFLAGS -Wpedantic"
AM_CFLAGS="$AM_CFLAGS -Werror"
AC_SUBST([AM_CFLAGS])

########################################################################

AC_ARG_VAR([GIT], [git revision control system])
AC_PATH_PROG([GIT], [git], [no])
AM_CONDITIONAL([HAVE_GIT], [test "x$GIT" != "xno"])

########################################################################

m4_pattern_forbid([NDIM_BUILD_RPMS])dnl
NDIM_BUILD_RPMS()dnl

########################################################################

AC_CONFIG_FILES([Makefile])
AC_CONFIG_FILES([m4/Makefile])
AC_CONFIG_FILES([include/Makefile])
AC_CONFIG_FILES([pkg-info/ndim-utils-info.sh])
AC_CONFIG_FILES([pkg-info/Makefile])
AC_CONFIG_FILES([admin-py/Makefile])
AC_CONFIG_FILES([admin-py/setup.py])
AC_CONFIG_FILES([palm-scripts/Makefile])
AC_CONFIG_FILES([palm-scripts/pilot])
AC_CONFIG_FILES([traffic/Makefile])
AC_CONFIG_FILES([GNUmakefile])
AC_OUTPUT

########################################################################

cat<<EOF

Configuration:
  Package: $PACKAGE
  Version: $VERSION

  srcdir: $srcdir

  CC:     $CC
  prefix: $prefix
  bindir: $bindir

You may run "make" and "make install" now.
EOF
