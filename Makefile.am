AM_INSTALLCHECK_STD_OPTIONS_EXEMPT =
BUILT_SOURCES =
CLEANFILES =
EXTRA_DIST =
man_MANS =
bin_PROGRAMS =
noinst_PROGRAMS =
EXTRA_PROGRAMS =
bin_SCRIPTS =
noinst_SCRIPTS =
EXTRA_SCRIPTS =
dist_bin_SCRIPTS =

SUBDIRS =
SUBDIRS += m4
SUBDIRS += include
SUBDIRS += admin-py
SUBDIRS += pkg-info
SUBDIRS += palm-scripts
SUBDIRS += traffic

doc_DATA = README AUTHORS NEWS

ACLOCAL_AMFLAGS = -I m4 --install

EXTRA_DIST += LICENSE

include build-helpers/package-version.mk

include cdburn/Makefile-files
include misc/Makefile-files
include misc-scripts/Makefile-files
include params/Makefile-files

clean-local:
	rm -rf rpm-build rpm-dist

CLEANFILES += $(PACKAGE_TARNAME).spec
EXTRA_DIST += $(PACKAGE_TARNAME).spec
EXTRA_DIST += package.spec.in
$(PACKAGE_TARNAME).spec: $(top_srcdir)/package.spec.in Makefile
	$(SED) \
		-e 's,[@]distdir@,$(distdir),g' \
		-e 's,[@]PACKAGE_NAME@,$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_TARNAME@,$(PACKAGE_TARNAME),g' \
		-e 's,[@]PACKAGE_URL@,$(PACKAGE_URL),g' \
		-e "s,[@]RPM_VERSION@,$$(echo "$(PACKAGE_VERSION)" | $(SED) s/-.*//),g" \
		-e "s,[@]RPM_RELEASE@,$$(echo "$(PACKAGE_VERSION)" | $(SED) s/.*-/git/),g" \
		$(top_srcdir)/package.spec.in > $(PACKAGE_TARNAME).spec

RPMBUILD = rpmbuild
RPMBUILD_OPTS =
RPMBUILD_OPTS += --define "_sourcedir $${PWD}"
RPMBUILD_OPTS += --define "_builddir $${PWD}/rpm-build"
RPMBUILD_OPTS += --define "_srcrpmdir $${PWD}/rpm-dist"
RPMBUILD_OPTS += --define "_rpmdir $${PWD}/rpm-dist"

.PHONY: rpm
rpm: dist-xz
	rm -rf rpm-dist rpm-build
	mkdir  rpm-dist rpm-build
	$(RPMBUILD) $(RPMBUILD_OPTS) -ta $(distdir).tar.xz

.PHONY: srpm
srpm: dist-xz
	rm -rf rpm-dist rpm-build
	mkdir  rpm-dist rpm-build
	$(RPMBUILD) $(RPMBUILD_OPTS) -ts $(distdir).tar.xz

.PHONY: upload
upload: $(SPECFILE) $(srcdir)/README $(srcdir)/NEWS dist srpm
	rsync -avz --progress \
		$(SPECFILE) \
		$(srcdir)/README $(srcdir)/NEWS \
		$(srcdir)/misc-scripts/list-debuginfo-rpms \
		$(PACKAGE_TARNAME)-$(PACKAGE_VERSION).tar.gz \
		$(PACKAGE_TARNAME)-$(PACKAGE_VERSION).tar.bz2 \
		$(RSYNC_HOST):n-dimensional.de/software/ndim-utils/

# End of file.
