# See ndim-build-rpms.README.md for usage instructions.

CLEAN_LOCAL_TARGETS += clean-local-ndim-build-rpms
clean-local-ndim-build-rpms:
	rm -rf rpm-build rpm-dist 'results_$(PACKAGE_TARNAME)'

SPECFILE = $(PACKAGE_TARNAME).spec
CLEANFILES += $(SPECFILE)
EXTRA_DIST += $(SPECFILE)
EXTRA_DIST += package.spec.in
$(SPECFILE): $(top_srcdir)/package.spec.in Makefile
	$(SED) \
		-e 's,[@]distdir@,$(distdir),g' \
		-e 's,[@]PACKAGE_NAME@,$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_TARNAME@,$(PACKAGE_TARNAME),g' \
		-e 's,[@]PACKAGE_URL@,$(PACKAGE_URL),g' \
		-e "s,[@]RPM_VERSION@,$(RPM_VERSION),g" \
		-e "s,[@]RPM_RELEASE@,$(RPM_RELEASE),g" \
		$(top_srcdir)/package.spec.in > $(SPECFILE)

if DO_RPMBUILD

RPMBUILD_OPTS =
RPMBUILD_OPTS += --define "_sourcedir $${PWD}"
RPMBUILD_OPTS += --define "_builddir $${PWD}/rpm-build"
RPMBUILD_OPTS += --define "_srcrpmdir $${PWD}/rpm-dist"
RPMBUILD_OPTS += --define "_rpmdir $${PWD}/rpm-dist"

rpm: dist-xz
	rm -rf rpm-dist rpm-build
	mkdir  rpm-dist rpm-build
	$(RPMBUILD) $(RPMBUILD_OPTS) -ta $(distdir).tar.xz

if DO_MOCKBUILD

PACKAGE_SRPM = $(PACKAGE_TARNAME)-$(RPM_VERSION)-$(RPM_RELEASE).src.rpm

SRPM_RPMBUILD_OPTS =
SRPM_RPMBUILD_OPTS += --define 'dist %{nil}'
SRPM_RPMBUILD_OPTS += --define "_sourcedir $${PWD}"
SRPM_RPMBUILD_OPTS += --define "_srcrpmdir $${PWD}"

srpm: $(PACKAGE_SRPM)
$(PACKAGE_SRPM): dist-xz $(SPECFILE)
	$(RPMBUILD) $(SRPM_RPMBUILD_OPTS) -bs $(SPECFILE)

MOCK_OPTS =
MOCK_OPTS += --resultdir=$(PWD)/results_$(PACKAGE_TARNAME)/$(RPM_VERSION)/$(RPM_RELEASE)

mockbuild: $(PACKAGE_SRPM)
	$(MOCK) $(MOCK_OPTS) --rebuild $(PACKAGE_SRPM)

mockbuild-all: $(PACKAGE_SRPM)
	@fail=""; succ=""; \
	if test "x$(NDIM_RPM_ARCH)" = "xx86_64" && test "xnoarch" != "x$(${SED} -n '/^%package/q; s/^BuildArch:[[[:space:]]]*\(noarch\)[[[:space:]]]*/\1/p' "${srcdir}/package.spec.in")"; then \
	for mockroot in /etc/mock/fedora-*-x86_64.cfg /etc/mock/epel-*-x86_64.cfg /etc/mock/fedora-*-i386.cfg /etc/mock/epel-*-i386.cfg; do \
		if test -f "$$mockroot"; then :; else echo "No such mock config: $$mockroot"; exit 1; fi; \
		echo "$(MOCK) $(MOCK_OPTS) --root $$mockroot --rebuild $(PACKAGE_SRPM)"; \
		if $(MOCK) $(MOCK_OPTS) --root "$$mockroot" --rebuild $(PACKAGE_SRPM); then \
			succ="$${succ} $$(basename "$${mockroot}")"; \
		else \
			fail="$${fail} $$(basename "$${mockroot}")"; \
		fi; \
	done; \
	else \
	for mockroot in /etc/mock/{fedora,epel}-*-$(NDIM_RPM_ARCH).cfg; do \
		if test -f "$$mockroot"; then :; else echo "No such mock config: $$mockroot"; exit 1; fi; \
		echo "$(MOCK) $(MOCK_OPTS) --root $$mockroot --rebuild $(PACKAGE_SRPM)"; \
		if $(MOCK) $(MOCK_OPTS) --root "$$mockroot" --rebuild $(PACKAGE_SRPM); then \
			succ="$${succ} $$(basename "$${mockroot}")"; \
		else \
			fail="$${fail} $$(basename "$${mockroot}")"; \
		fi; \
	done; \
	fi; \
	for f in $${succ}; do \
		clean=false; \
		echo "SUCC build for $${f}"; \
	done; \
	dirty=false; \
	for f in $${fail}; do \
		dirty=true; \
		echo "FAIL build for $${f}"; \
	done; \
	if "$$dirty"; then \
		echo "Some builds failed."; \
		exit 2; \
	fi

endif

endif
