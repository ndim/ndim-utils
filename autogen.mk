#!/usr/bin/make -f

GEN_RECONF = COPYING INSTALL install-sh missing depcomp include/config.h.in
GEN_ACAM = aclocal.m4 configure config.guess config.sub compile mkinstalldirs
GEN_CONF = config.status config.log include/config.h include/stamp-h1 include/stamp-h2
GEN_LIBTOOL = ltmain.sh libtool
GENERATED_FILES = $(GEN_RECONF) $(GEN_ACAM) $(GEN_CONF) $(GEN_LIBTOOL)
GENERATED_DIRS = autom4te.cache

AUTORECONF_OPTS = --verbose -Wall
# AUTORECONF_OPTS =

.PHONY: init
init:
	autoreconf --verbose --install --symlink $(AUTORECONF_OPTS)
	@echo "You may run ./configure now -- probably as \"./configure --help\"."

.PHONY: clean
clean:
	rm -rf $(GENERATED_DIRS)
	rm -f $(GENERATED_FILES)
	find . -type f -name 'Makefile.am' -print | \
		while read file; do \
			echo "$$file" | grep -q '{arch}' && continue; \
			echo "$$file: Removing created files."; \
			base="$$(dirname "$$file")/$$(basename "$$file" .am)"; \
			rm -f "$${base}"; \
			rm -f "$${base}.in"; \
		done
	find . -type f -name '*~' -exec rm -f {} \;
