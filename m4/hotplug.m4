# NDIM_CHECK_HOTPLUG()
# --------------------------
# Check to see where this system stores configuration files

AC_DEFUN([NDIM_CHECK_HOTPLUG],
[
AC_MSG_CHECKING([for hotplug directory])
hotplugdir="$sysconfdir/hotplug"
while read dir; do
	if test -d "$dir"; then
		hotplugdir="$dir"
		break
	fi
done <<EOF
$sysconfdir/hotplug
/usr/local/etc/hotplug
/usr/etc/hotplug
/etc/hotplug
EOF
unset dir
AC_SUBST([hotplugdir])
AC_MSG_RESULT([$hotplugdir])
hotplugusbdir="${hotplugdir}/usb"
AC_MSG_CHECKING([for hotplug USB script directory])
AC_SUBST([hotplugusbdir])
AC_MSG_RESULT([$hotplugusbdir])
])
