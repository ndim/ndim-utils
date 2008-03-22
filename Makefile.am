EXTRA_DIST =
CLEANFILES =
BUILT_SOURCES =

SUBDIRS = m4 include admin-py cdburn misc misc-scripts tla pkg-info palm-scripts traffic

doc_DATA = README AUTHORS NEWS

ACLOCAL_AMFLAGS = -I m4 --install

include build-scripts/package-version.mk

EXTRA_DIST += $(PACKAGE_TARNAME).spec $(PACKAGE_TARNAME).spec.in

clean-local:
	rm -rf rpm-build rpm-dist

SPECFILE = $(PACKAGE_TARNAME).spec

RPMBUILD = rpmbuild
RPMBUILD_OPTS =
RPMBUILD_OPTS += --define "_sourcedir $${PWD}"
RPMBUILD_OPTS += --define "_builddir $${PWD}/rpm-build"
RPMBUILD_OPTS += --define "_srcrpmdir $${PWD}/rpm-dist"
RPMBUILD_OPTS += --define "_rpmdir $${PWD}/rpm-dist"

.PHONY: rpm
rpm: dist $(SPECFILE)
	rm -rf rpm-dist rpm-build
	mkdir rpm-dist rpm-build
	$(RPMBUILD) $(RPMBUILD_OPTS) -ba $(SPECFILE)

.PHONY: srpm
srpm: dist $(SPECFILE)
	rm -rf rpm-dist rpm-build
	mkdir rpm-dist rpm-build
	$(RPMBUILD) $(RPMBUILD_OPTS) -bs $(SPECFILE)

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
