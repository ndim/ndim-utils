bin_PROGRAMS = @PACKAGE_TARNAME@-info

@PACKAGE_TARNAME@_info_SOURCES = pkg-info.c \
	$(top_builddir)/include/package-version.h \
	$(top_builddir)/include/build-info.h

$(top_builddir)/includes/package-version.h:
	$(MAKE) -C $(top_builddir)/include package-version.h

$(top_builddir)/includes/build-info.h:
	$(MAKE) -C $(top_builddir)/include build-info.h
