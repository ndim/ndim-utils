########################################################################
# --enable-debug

AC_DEFUN([NDIM_DEBUG_MODE],
[
AC_REQUIRE([GP_CONFIG_MSG])
AC_MSG_CHECKING([for debug mode])
AC_ARG_ENABLE([debug],
AS_HELP_STRING([--enable-debug],[turn on debugging]),
[
case "${enableval}" in
      	(yes|true|on)
		debug_mode='yes'
		DEBUG_MODE=1
		AC_SUBST(DEBUG_MODE)
		AC_DEFINE([DEBUG_MODE],[1],[whether to include debugging code or not])
		;;
	(*)
		debug_mode='no'
		;;
esac],
[
	debug_mode='no'
])
AC_MSG_RESULT([${debug_mode}])
AM_CONDITIONAL([DEBUG_MODE],[test "x$debug_mode" = "xyes"])
GP_CONFIG_MSG([debug mode],[$debug_mode])
])

dnl Local Variables:
dnl mode: autoconf
dnl End:
