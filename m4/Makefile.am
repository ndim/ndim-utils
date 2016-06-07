CLEANFILES =
EXTRA_DIST =

EXTRA_DIST += configuration.m4
EXTRA_DIST += debug.m4
EXTRA_DIST += gp-check-shell-environment.m4
EXTRA_DIST += gp-config-msg.m4
EXTRA_DIST += gp-gettext-helper.m4
EXTRA_DIST += hotplug.m4
EXTRA_DIST += systemconfig.m4
EXTRA_DIST += upload.m4

EXTRA_DIST += ndim-build-rpms.m4
EXTRA_DIST += ndim-build-rpms.mk
EXTRA_DIST += ndim-build-rpms.README.md

CLEANFILES += README
EXTRA_DIST += README
noinst_DATA = README

README: Makefile
	@echo "Creating $@"
	@echo "This is ndim's autoconf/automake macro collection:" > $@
	@echo "" >> $@
	@for f in $(srcdir)/*.m4; do \
		echo "   $$(basename "$$f")"; \
		sed -n 's|^AC_DEFUN(\[\{0,1\}\([^_][^])]*\).*$$|      \1|p' "$$f"; \
		echo; \
	done >> $@

# End of Makefile.am.
