EXTRA_DIST = arch-meta-hook

if TLA_SCRIPTS

tlascript_SCRIPTS = hook
CLEANFILES = $(tlascript_SCRIPTS)

pkgdata_DATA = arch-meta-hook.txt

hook: arch-meta-hook
	cp $< $@
	chmod +x $@

arch-meta-hook.txt: arch-meta-hook Makefile
	(read; read; \
	while read -r line; \
	do \
		[ "$$line" = "" ] && break; \
		echo "$$line"; \
	done) < $< | \
	sed -e 's/^# //g' -e 's/^#$$//g' > $@

endif
