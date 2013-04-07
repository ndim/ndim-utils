########################################################################
# --with-upload=remote-host:remote/path/

AC_DEFUN([NDIM_UPLOAD],[dnl
	AC_REQUIRE([GP_CONFIG_MSG])
	AC_MSG_CHECKING([for upload location])
	AC_ARG_WITH([upload],
AS_HELP_STRING([--with-upload],[rsync location to upload to]),
[
do_upload="no"
if test "x${withval}" != "x"; then
	do_upload="yes, to ${withval}"
	AC_SUBST([UPLOAD_LOCATION],[${withval}])
fi
],
[
do_upload="no"
])
AC_MSG_RESULT([${do_upload}])
AM_CONDITIONAL([DO_UPLOAD],[test "x${do_upload}" != "xno"])
GP_CONFIG_MSG([do upload],[${do_upload}])
])dnl

dnl Local Variables:
dnl mode: autoconf
dnl End:
