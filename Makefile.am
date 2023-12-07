AM_INSTALLCHECK_STD_OPTIONS_EXEMPT =
BUILT_SOURCES =
CLEANFILES =
EXTRA_DIST =
man_MANS =
bin_PROGRAMS =
check_PROGRAMS =
noinst_PROGRAMS =
EXTRA_PROGRAMS =
bin_SCRIPTS =
noinst_SCRIPTS =
EXTRA_SCRIPTS =
dist_bin_SCRIPTS =

CLEAN_LOCAL_TARGETS =

TESTS =
TEST_EXTENSIONS =
XFAIL_TESTS =

SUBDIRS =
SUBDIRS += m4
SUBDIRS += include
# whois is dead
# SUBDIRS += admin-py
SUBDIRS += pkg-info
SUBDIRS += palm-scripts
SUBDIRS += traffic

dist_doc_DATA = README.md
doc_DATA = AUTHORS NEWS

ACLOCAL_AMFLAGS = --install

EXTRA_DIST += LICENSE

BUILT_SOURCES += package-subst
EXTRA_DIST    += package-subst.in
CLEANFILES    += package-subst
package-subst: package-subst.in Makefile
	$(SED) \
		-e 's|[@]MKDIR_P@|$(MKDIR_P)|g' \
		-e 's|[@]SED@|$(SED)|g' \
		-e 's|[@]PACKAGE_NAME@|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_TARNAME@|$(PACKAGE_TARNAME)|g' \
		-e 's|[@]PACKAGE_VERSION@|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/package-subst.in > package-subst
	chmod +x package-subst

# Interface variables to be used in included Makefile-files
# Does not work in subdir Makefile.am!
#
# foo/bar: foo/bar.in $(PACKAGE_SUBST_DEP)
#          $(PACKAGE_SUBST) $(srcdir)/foo/bar.in foo/bar
#
PACKAGE_SUBST = ./package-subst
PACKAGE_SUBST_DEP = package-subst

include build-helpers/package-version.mk

# include binary-test/Makefile-files
include bing/Makefile-files
include cdburn/Makefile-files
include colfilter/Makefile-files
include gnome-fixes/Makefile-files
include list-debuginfo-rpms/Makefile-files
include np/Makefile-files
include one/Makefile-files
include params/Makefile-files
include pdf2minibook/Makefile-files
include percheck/Makefile-files
include profile/Makefile-files
include ps2lj4/Makefile-files
include restart-gnome-shell/Makefile-files
include strace-normalize/Makefile-files
include umlxterm/Makefile-files
include watch-xsel/Makefile-files
include xnest/Makefile-files

include m4/ndim-build-rpms.mk

dist-hook: dist-hook-rm-INSTALL-file
dist-hook-rm-INSTALL-file:
	rm -f "$(distdir)/INSTALL"

upload: $(SPECFILE) $(srcdir)/README.md $(srcdir)/NEWS dist srpm
	rsync -avz --progress \
		$(SPECFILE) \
		$(srcdir)/README.md $(srcdir)/NEWS \
		$(srcdir)/misc-scripts/list-debuginfo-rpms \
		$(distdir).tar.xz \
		$(RSYNC_HOST):n-dimensional.de/software/$(PACKAGE_TARNAME)/

clean-local: $(CLEAN_LOCAL_TARGETS)

# End of file.
