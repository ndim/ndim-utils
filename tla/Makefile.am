EXTRA_DIST = arch-meta-hook commit-sendlog commit-archive-mirror

bin_SCRIPTS = arch-meta-hook commit-sendlog commit-archive-mirror

pkgdata_DATA = arch-meta-hook.txt

arch-meta-hook.txt: arch-meta-hook Makefile
	(read; read; \
	while read -r line; \
	do \
		[ "$$line" = "" ] && break; \
		echo "$$line"; \
	done) < $< | \
	sed -e 's/^# //g' -e 's/^#$$//g' > $@
