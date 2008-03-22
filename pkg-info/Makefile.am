EXTRA_DIST = ndim-utils-info.sh.in

bin_PROGRAMS = @PACKAGE_TARNAME@-info

bin_SCRIPTS = ndim-utils-info.sh ndim-utils-info2.sh

BUILT_SOURCES = moo.stamp

@PACKAGE_TARNAME@_info_SOURCES = pkg-info.c
@PACKAGE_TARNAME@_info_SOURCES += \
	$(top_builddir)/include/build-info.h
@PACKAGE_TARNAME@_info_CPPFLAGS = -I$(top_builddir)

moo.stamp:
	$(MAKE) -C $(top_builddir)/include

CLEANFILES = ndim-utils-info2.sh
ndim-utils-info2.sh: ndim-utils-info.sh.in
	sed \
		-e 's|[@]prefix[@]|$(prefix)|g' \
		-e 's|[@]bindir[@]|$(bindir)|g' \
		-e 's|[@]libdir[@]|$(libdir)|g' \
		-e 's|[@]Q_PREFIX[@]|$(Q_PREFIX)|g' \
		-e 's|[@]Q_BINDIR[@]|$(Q_BINDIR)|g' \
		-e 's|[@]Q_LIBDIR[@]|$(Q_LIBDIR)|g' \
		-e 's|[@]UQ_PREFIX[@]|$(UQ_PREFIX)|g' \
		-e 's|[@]UQ_BINDIR[@]|$(UQ_BINDIR)|g' \
		-e 's|[@]UQ_LIBDIR[@]|$(UQ_LIBDIR)|g' \
	< "$<" > "$@"
