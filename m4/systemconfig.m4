# NDIM_CHECK_SYSTEM_CONFIG()
# --------------------------
# Check to see where this system stores configuration files

AC_DEFUN([NDIM_CHECK_SYSTEM_CONFIG],
[
AC_MSG_CHECKING([for system configuration directory])
configdir="/etc"
while read dir
do
	if [ -d "$dir" ]
	then
		configdir="$dir"
		break
	fi
done <<EOF
/etc/sysconfig
/etc/default
EOF
unset dir
AC_SUBST([configdir])
AC_MSG_RESULT([$configdir])
])
