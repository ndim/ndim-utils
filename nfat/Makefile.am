TESTS = nfattest.sh

#bin_PROGRAMS =

check_PROGRAMS = syslogtest nfattest

check_SCRIPTS = nfattest.sh

lib_LTLIBRARIES = libnfat.la

nfattest.sh: nfattest libnfat.la Makefile
	echo '#!/bin/sh' > $@
	echo 'this="$$(dirname "$$0")"' >> $@
	echo 'LD_PRELOAD=$${this}/.libs/libnfat.so $${this}/$<' >> $@
	chmod +x $@

libnfat_la_SOURCES = libnfat.c libnfat.h
libnfat_la_CFLAGS = -save-temps -Werror
libnfat_la_LDFLAGS = -ldl -Werror

nfattest_SOURCES = nfattest.c

syslogtest_SOURCES = syslogtest.c
