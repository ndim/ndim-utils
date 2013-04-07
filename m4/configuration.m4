# NDIM_CHECK_CONFIGURATION()
# --------------------------
# Check for build-time definitions.

AC_DEFUN([NDIM_CHECK_CONFIGURATION],
[
AC_MSG_CHECKING([for build-time configuration])
AC_SUBST([prefix])
AC_SUBST([libdir])
AC_SUBST([bindir])
AC_DEFINE_UNQUOTED([UQ_PREFIX],["$prefix"], [installation prefix])
AC_DEFINE_UNQUOTED([UQ_LIBDIR],["$libdir"], [installation libdir])
AC_DEFINE_UNQUOTED([UQ_BINDIR],["$bindir"], [installation bindir])
AC_DEFINE([Q_PREFIX],["$prefix"], [installation prefix])
AC_DEFINE([Q_LIBDIR],["$libdir"], [installation libdir])
AC_DEFINE([Q_BINDIR],["$bindir"], [installation bindir])
PREFIX="$prefix"
LIBDIR="$libdir"
BINDIR="$bindir"
AC_SUBST([PREFIX])
AC_SUBST([LIBDIR])
AC_SUBST([BINDIR])
AC_MSG_RESULT([done.])
])

dnl Local Variables:
dnl mode: autoconf
dnl End:
