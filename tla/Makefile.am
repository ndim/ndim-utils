EXTRA_DIST = arch-meta-hook commit-sendlog commit-archive-mirror

tlahook_SCRIPTS = arch-meta-hook commit-sendlog commit-archive-mirror

pkgdoc_DATA = arch-meta-hook.txt

clean-generic:
	rm -f arch-meta-hook.txt

arch-meta-hook.txt: arch-meta-hook Makefile
	(read; read; \
	while read -r line; \
	do \
		[ "$$line" = "" ] && break; \
		echo "$$line"; \
	done) < $< | \
	sed -e 's/^# //g' -e 's/^#$$//g' > $@
