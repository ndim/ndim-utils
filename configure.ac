########################################################################

AC_PREREQ(2.61)
AC_INIT([ndim utility collection],
        [m4_esyscmd([./build-helpers/package-version . version-stamp])],
        [hun@n-dimensional.de],
        [ndim-utils],
        [http://n-dimensional.de/software/ndim-utils/])
AC_CONFIG_AUX_DIR([auto-aux])
AC_CONFIG_HEADER([include/config.h])
AC_CONFIG_SRCDIR([pkg-info/pkg-info.c])
AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE([-Wall -Werror foreign 1.11.1 no-dist-gzip dist-xz
                  readme-alpha tar-pax])
dnl TODO: Make us compatible with 'std-options'

########################################################################

AC_PROG_SED
AC_PROG_CC
AC_PROG_INSTALL

########################################################################

m4_pattern_forbid([NDIM_CHECK_])dnl
NDIM_CHECK_SYSTEM_CONFIG
NDIM_CHECK_HOTPLUG
NDIM_CHECK_CONFIGURATION

########################################################################

pkgdocdir="${datadir}/doc/${PACKAGE_TARNAME}"
AC_SUBST(pkgdocdir)

tlahookdir="${datadir}/${PACKAGE_TARNAME}/tla-hooks"
AC_SUBST(tlahookdir)

########################################################################

AC_ARG_VAR([GIT], [git revision control system])
AC_PATH_PROG([GIT], [git], [no])
AM_CONDITIONAL([HAVE_GIT], [test "x$GIT" != "xno"])

########################################################################

AC_CONFIG_FILES([Makefile])
AC_CONFIG_FILES([m4/Makefile])
AC_CONFIG_FILES([cdburn/Makefile])
AC_CONFIG_FILES([tla/Makefile])
AC_CONFIG_FILES([include/Makefile])
AC_CONFIG_FILES([misc-scripts/Makefile])
AC_CONFIG_FILES([misc-scripts/percheck.1])
AC_CONFIG_FILES([pkg-info/ndim-utils-info.sh])
AC_CONFIG_FILES([pkg-info/Makefile])
AC_CONFIG_FILES([misc/Makefile])
AC_CONFIG_FILES([misc/params.1])
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
