#!/usr/bin/make -f

GEN_RECONF = COPYING INSTALL install-sh missing depcomp include/config.h.in
GEN_ACAM = aclocal.m4 configure 
GEN_CONF = config.status config.log include/config.h include/stamp-h1 include/stamp-h2
GENERATED_FILES = $(GEN_RECONF) $(GEN_ACAM) $(GEN_CONF)
GENERATED_DIRS = autom4te.cache

.PHONY: init
init:
	autoreconf --install --symlink --verbose -Wall
	@echo "You may run ./configure now -- probably as \"./configure --help\"."

.PHONY: clean
clean:
	rm -rf $(GENERATED_DIRS)
	rm -f $(GENERATED_FILES)
	find $$(pwd) -type f -name 'Makefile.am' -print | \
		while read file; do \
			rm -f "$$(basename "$file" .am).am"; \
		done
