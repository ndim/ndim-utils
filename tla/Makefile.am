EXTRA_DIST = arch-meta-hook

tlascript_SCRIPTS = hook
CLEANFILES = $(tlascript_SCRIPTS)

hook: arch-meta-hook
	cp $< $@
	chmod +x $@
