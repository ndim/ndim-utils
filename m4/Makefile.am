CLEANFILES =
EXTRA_DIST =

m4_files =
m4_files += configuration.m4
m4_files += debug.m4
m4_files += gp-check-shell-environment.m4
m4_files += gp-config-msg.m4
m4_files += gp-gettext-helper.m4
m4_files += hotplug.m4
m4_files += systemconfig.m4
m4_files += upload.m4

m4_files   += ndim-build-rpms.m4
EXTRA_DIST += ndim-build-rpms.mk
EXTRA_DIST += ndim-build-rpms.README.md

CLEANFILES += README
EXTRA_DIST += README
noinst_DATA = README

README: Makefile
	@echo "Creating $@"
	@echo "This is ndim's autoconf/automake macro collection:" > $@
	@echo "" >> $@
	@for f in $(m4_files); do \
		echo "    $$f"; \
		sed -n 's|^AC_DEFUN(\[\{0,1\}\([^_][^])]*\).*$$|        \1|p' "$(srcdir)/$$f"; \
		echo; \
	done >> $@

# End of Makefile.am.
