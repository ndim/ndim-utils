########################################################################

AC_PREREQ(2.59)
AC_INIT([ndim utility collection], [0.1.0],
	[hun@n-dimensional.de], [ndim-utils])
AC_CONFIG_HEADER([include/config.h])
AC_CONFIG_SRCDIR([pkg-info/pkg-info.c])
AM_INIT_AUTOMAKE([gnu 1.8 dist-bzip2])

########################################################################

AC_PROG_CC
AC_PROG_INSTALL

########################################################################

NDIM_CHECK_SYSTEM_CONFIG
NDIM_CHECK_HOTPLUG

########################################################################

pkgdocdir="${datadir}/doc/${PACKAGE_TARNAME}"
AC_SUBST(pkgdocdir)

tlahookdir="${datadir}/${PACKAGE_TARNAME}/tla-hooks"
AC_SUBST(tlahookdir)

########################################################################

AC_CONFIG_FILES([
	Makefile
	m4/Makefile
	cdburn/Makefile
	tla/Makefile
	include/Makefile
	misc-scripts/Makefile
	pkg-info/Makefile
	misc/Makefile
	admin-py/Makefile
	admin-py/setup.py
	palm-scripts/Makefile
	palm-scripts/pilot
	traffic/Makefile
	])
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
