# See ndim-build-rpms.README.md for usage instructions.

CLEAN_LOCAL_TARGETS += clean-local-ndim-build-rpms
clean-local-ndim-build-rpms:
	rm -rf rpm-build rpm-dist 'results_$(PACKAGE_TARNAME)'

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

if DO_RPMBUILD

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

endif

if DO_FEDPKG

FEDPKG_OPTS =
FEDPKG_OPTS += --module-name=$(PACKAGE_TARNAME)
FEDPKG_OPTS += --dist=f$(NDIM_FEDORA_VERSION)

.PHONY: mockbuild
mockbuild: dist-xz
	$(FEDPKG) $(FEDPKG_OPTS) mockbuild
if DO_EXTRA_i386_BUILD
	$(FEDPKG) $(FEDPKG_OPTS) mockbuild --root $(NDIM_i386_MOCK_ROOT)
endif

endif
