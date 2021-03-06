dnl
dnl GP_GETTEXT_HACK
dnl
dnl gettext hack, originally designed for libexif, libgphoto2, and Co.
dnl This creates a po/Makevars file with adequate values if the
dnl po/Makevars.template is present.
dnl
dnl Example usage:
dnl    GP_GETTEXT_HACK([${PACKAGE_TARNAME}-${LIBFOO_CURRENT}],
dnl                    [Copyright Holder],
dnl                    [foo-translation@example.org])
dnl    ALL_LINGUAS="de es fr"
dnl    AM_GNU_GETTEXT
dnl    GP_GETTEXT_FLAGS
dnl
dnl You can leave out the GP_GETTEXT_HACK parameters if you want to,
dnl GP_GETTEXT_HACK will try fall back to sensible values in that case:
dnl

AC_DEFUN([GP_GETTEXT_HACK],
[
if test -n "$1"; then
   GETTEXT_PACKAGE=${PACKAGE_TARNAME}
else
   GETTEXT_PACKAGE="$1"
fi
AC_DEFINE_UNQUOTED([GETTEXT_PACKAGE], ["$GETTEXT_PACKAGE"],
                   [The gettext domain we're using])
AC_SUBST([GETTEXT_PACKAGE])
sed_cmds="s|^DOMAIN.*|DOMAIN = ${GETTEXT_PACKAGE}|"
if test -n "$2"; then
   sed_cmds="${sed_cmds};s|^COPYRIGHT_HOLDER.*|COPYRIGHT_HOLDER = $2|"
fi
if test -n "$3"; then
   sed_mb="$3"
elif test -n "$PACKAGE_BUGREPORT"; then
   sed_mb="${PACKAGE_BUGREPORT}"
else
   AC_MSG_ERROR([
*** Your configure.{ac,in} is wrong.
*** Either define PACKAGE_BUGREPORT (by using the 4-parameter AC INIT syntax)
*** or give [GP_GETTEXT_HACK] the second parameter.
***
])
fi
sed_cmds="${sed_cmds};s|^MSGID_BUGS_ADDRESS.*|MSGID_BUGS_ADDRESS = ${sed_mb}|"
# Not so sure whether this hack is all *that* evil...
AC_MSG_CHECKING([for po/Makevars requiring hack])
if test -f po/Makevars.template; then
   sed "$sed_cmds" < po/Makevars.template > po/Makevars
   AC_MSG_RESULT([yes, done.])
else
   AC_MSG_RESULT([no])
fi
])

AC_DEFUN([GP_GETTEXT_FLAGS],
[
AC_REQUIRE([AM_GNU_GETTEXT])
AC_REQUIRE([GP_CONFIG_MSG])
if test "x${BUILD_INCLUDED_LIBINTL}" = "xyes"; then
   AM_CFLAGS="${AM_CFLAGS} -I\$(top_srcdir)/intl"
fi
GP_CONFIG_MSG
GP_CONFIG_MSG([Use translations],[${USE_NLS}])
GP_CONFIG_MSG([Use included libintl],[${BUILD_INCLUDED_LIBINTL}])
])

dnl Local Variables:
dnl mode: autoconf
dnl End:
