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
                  readme-alpha tar-pax subdir-objects std-options])
dnl TODO: Make us compatible with 'std-options'

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

AC_ARG_VAR([RPMBUILD], [rpm package manager build utility])
AC_PATH_PROG([RPMBUILD], [rpmbuild], [no])

AC_ARG_VAR([FEDPKG], [fedora package build utility])
AC_PATH_PROG([FEDPKG], [fedpkg], [no])

AM_CONDITIONAL([HAVE_RPMBUILD], [test "x$RPMBUILD" != "xno"])
AM_CONDITIONAL([HAVE_FEDPKG], [test "x$FEDPKG" != "xno"])

AC_MSG_CHECKING([rpmbuild %{fedora} version])
NDIM_FEDORA_VERSION="n/a"
if test "x$RPMBUILD" != "xno"; then
   NDIM_FEDORA_VERSION="$(${RPMBUILD} --eval '%{fedora}')"
fi
AC_MSG_RESULT([$NDIM_FEDORA_VERSION])
AC_SUBST([NDIM_FEDORA_VERSION])

AC_MSG_CHECKING([rpmbuild %{_arch}])
NDIM_RPM_ARCH="n/a"
if test "x$RPMBUILD" != "xno"; then
   NDIM_RPM_ARCH="$(${RPMBUILD} --eval '%{_arch}')"
fi
AC_MSG_RESULT([$NDIM_RPM_ARCH])

AC_MSG_CHECKING([spec file for main package 'BuildArch: noarch'])
dnl Note: m4 eats [], so we need to put more here than sed actually needs
if test "xnoarch" = "x$(${SED} -n '/^%package/q; s/^BuildArch:[[[:space:]]]*\(noarch\)[[[:space:]]]*/\1/p' "${srcdir}/package.spec.in")"; then
   NDIM_MAINPKG_NOARCH=yes
else
   NDIM_MAINPKG_NOARCH=no
fi
AC_MSG_RESULT([$NDIM_MAINPKG_NOARCH])

AC_SUBST([NDIM_i386_MOCK_ROOT], [fedora-${NDIM_FEDORA_VERSION}-i386])
AM_CONDITIONAL([RUN_EXTRA_i386_BUILD],
               [test "x$NDIM_MAINPKG_NOARCH" = "xno" &&
	        test "x$NDIM_RPM_ARCH" = "xx86_64" &&
	        test -f "/etc/mock/${NDIM_i386_MOCK_ROOT}.cfg"])

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
