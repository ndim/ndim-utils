# NDIM_CHECK_SYSTEM_CONFIG()
# --------------------------
# Check to see where this system stores configuration files

AC_DEFUN([NDIM_CHECK_SYSTEM_CONFIG],
[
AC_MSG_CHECKING([for system configuration directory])
while read dir; do
	if test -d "$dir"; then
		configdir="$dir"
		break
	fi
done <<EOF
/etc/sysconfig
/etc/default
EOF
unset dir
configdir="$sysconfdir"
AC_SUBST([configdir])
AC_MSG_RESULT([$configdir])
])
