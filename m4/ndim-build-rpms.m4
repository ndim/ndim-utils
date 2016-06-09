# serial 1
dnl NDIM_BUILD_RPMS
dnl See ndim-build-rpms.README.md for usage instructions.
dnl
m4_pattern_forbid([NDIM_BUILD_RPMS])dnl
AC_DEFUN([NDIM_BUILD_RPMS], [dnl
AC_ARG_VAR([RPMBUILD], [rpm package manager build utility])
AC_PATH_PROG([RPMBUILD], [rpmbuild], [no])

AM_CONDITIONAL([DO_RPMBUILD], [test "x$RPMBUILD" != "xno"])
AC_MSG_CHECKING([whether to do rpmbuild build])
AS_IF([test "x$DO_RPMBUILD_FALSE" = 'x#'],
      [AC_MSG_RESULT([yes])],
      [AC_MSG_RESULT([no])])

AC_ARG_VAR([FEDPKG], [fedora package build utility])
AC_PATH_PROG([FEDPKG], [fedpkg], [no])

AC_MSG_CHECKING([rpmbuild for %{fedora} value])
AS_IF([test "x$RPMBUILD" != "xno"],
      [NDIM_FEDORA_VERSION="$(${RPMBUILD} --eval '%{fedora}')"],
      [NDIM_FEDORA_VERSION="n/a"])
AC_MSG_RESULT([$NDIM_FEDORA_VERSION])
AC_SUBST([NDIM_FEDORA_VERSION])

AC_MSG_CHECKING([rpmbuild for %{_arch} value])
AS_IF([test "x$RPMBUILD" != "xno"],
      [NDIM_RPM_ARCH="$(${RPMBUILD} --eval '%{_arch}')"],
      [NDIM_RPM_ARCH="n/a"])
AC_MSG_RESULT([$NDIM_RPM_ARCH])
AC_SUBST([NDIM_RPM_ARCH])

AC_MSG_CHECKING([whether spec file contains 'BuildArch: noarch' for main package])
dnl Note: m4 eats [], so we need to put more here than sed actually needs
AS_IF([test "xnoarch" = "x$(${SED} -n '/^%package/q; s/^BuildArch:[[[:space:]]]*\(noarch\)[[[:space:]]]*/\1/p' "${srcdir}/package.spec.in")"],
      [NDIM_MAINPKG_NOARCH=yes],
      [NDIM_MAINPKG_NOARCH=no])
AC_MSG_RESULT([$NDIM_MAINPKG_NOARCH])
AC_SUBST([NDIM_MAINPKG_NOARCH])

AC_SUBST([NDIM_i386_MOCK_ROOT], [fedora-${NDIM_FEDORA_VERSION}-i386])

AM_CONDITIONAL([DO_FEDPKG],
               [test "x$RPMBUILD" != "xno" &&
	        test "x$FEDPKG" != "xno" &&
	        test "x$NDIM_FEDORA_VERSION" != "xn/a" &&
	        test "x$NDIM_RPM_ARCH" != "xn/a" ])
AC_MSG_CHECKING([whether to do fedpkg build])
AS_IF([test "x$DO_FEDPKG_FALSE" = 'x#'],
      [AC_MSG_RESULT([yes])],
      [AC_MSG_RESULT([no])])

AM_CONDITIONAL([DO_EXTRA_i386_BUILD],
               [test "x$NDIM_MAINPKG_NOARCH" = "xno" &&
	        test "x$NDIM_RPM_ARCH" = "xx86_64" &&
	        test -f "/etc/mock/${NDIM_i386_MOCK_ROOT}.cfg"])
AC_MSG_CHECKING([whether to do extra fedpkg build for i386 arch])
AS_IF([test "x$DO_EXTRA_i386_BUILD_FALSE" = 'x#'],
      [AC_MSG_RESULT([yes])],
      [AC_MSG_RESULT([no])])
])dnl
dnl
dnl Local Variables:
dnl mode: autoconf
dnl End:
