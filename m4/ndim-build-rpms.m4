# serial 2
dnl NDIM_BUILD_RPMS
dnl See ndim-build-rpms.README.md for usage instructions.
dnl
m4_pattern_forbid([NDIM_BUILD_RPMS])dnl
AC_DEFUN([NDIM_BUILD_RPMS], [dnl
AC_ARG_VAR([RPMBUILD], [rpm package manager build utility])
AC_PATH_PROG([RPMBUILD], [rpmbuild], [no])

AC_SUBST([RPM_VERSION], [$(echo "${PACKAGE_VERSION}" | ${SED} s/-.*//)])
AC_SUBST([RPM_RELEASE], [$(echo "${PACKAGE_VERSION}" | ${SED} s/.*-/1git/)])

AM_CONDITIONAL([DO_RPMBUILD], [test "x$RPMBUILD" != "xno"])
AC_MSG_CHECKING([whether we can do rpmbuild builds])
AS_IF([test "x$DO_RPMBUILD_FALSE" = 'x#'],
      [AC_MSG_RESULT([yes])],
      [AC_MSG_RESULT([no])])

AC_ARG_VAR([MOCK], [rpm package builder using chroots])
AC_PATH_PROG([MOCK], [mock], [no])

AC_MSG_CHECKING([rpmbuild for %{_arch} value])
AS_IF([test "x$RPMBUILD" != "xno"],
      [NDIM_RPM_ARCH="$(${RPMBUILD} --eval '%{_arch}')"],
      [NDIM_RPM_ARCH="n/a"])
AC_MSG_RESULT([$NDIM_RPM_ARCH])
AC_SUBST([NDIM_RPM_ARCH])

AM_CONDITIONAL([DO_MOCKBUILD],
               [test "x$RPMBUILD" != "xno" &&
	        test "x$MOCK" != "xno" &&
	        test "x$NDIM_RPM_ARCH" != "xn/a" ])
AC_MSG_CHECKING([whether we can do mock builds])
AS_IF([test "x$DO_MOCKBUILD_FALSE" = 'x#'],
      [AC_MSG_RESULT([yes])],
      [AC_MSG_RESULT([no])])
])dnl
dnl
dnl Local Variables:
dnl mode: autoconf
dnl End:
