TESTS = nfattest.sh

#bin_PROGRAMS =

check_PROGRAMS = syslogtest nfattest nfattest.sh

lib_LTLIBRARIES = libnfat.la

nfattest.sh: nfattest libnfat.la Makefile
	echo '#!/bin/sh' > $@
	echo 'this="$$(dirname "$$0")"' >> $@
	echo 'LD_PRELOAD=$${this}/.libs/libnfat.so $${this}/$<' >> $@
	chmod +x $@

libnfat_la_SOURCES = libnfat.c
libnfat_la_CFLAGS = -save-temps
libnfat_la_LDFLAGS = -ldl

nfattest_SOURCES = nfattest.c

syslogtest_SOURCES = syslogtest.c
