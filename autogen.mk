#!/usr/bin/make -f

ACLOCAL_FILES = aclocal.m4

.PHONY: init
init:
	autoreconf --install --symlink --verbose -Wall

clean:
	rm -f $(ACLOCAL_FILES)
