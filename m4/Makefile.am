m4files = configuration.m4 debug.m4 gp-check-shell-environment.m4 gp-config-msg.m4 gp-gettext-helper.m4 hotplug.m4 systemconfig.m4 upload.m4

EXTRA_DIST = README $(m4files)

noinst_DATA = README

CLEANFILES = README

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
