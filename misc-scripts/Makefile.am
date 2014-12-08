CLEANFILES =
bin_SCRIPTS =
dist_bin_SCRIPTS =
man_MANS =
EXTRA_DIST =

EXTRA_DIST  += bing
bin_SCRIPTS += bing

EXTRA_DIST  += watch-xsel.in
bin_SCRIPTS += watch-xsel
CLEANFILES  += watch-xsel
watch-xsel: watch-xsel.in
	sed \
		-e 's|[@]PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< "$<" > "$@"

EXTRA_DIST  += xnest
bin_SCRIPTS += xnest

EXTRA_DIST  += umlxterm
bin_SCRIPTS += umlxterm

EXTRA_DIST  += ps2lj4
bin_SCRIPTS += ps2lj4

EXTRA_DIST  += np
bin_SCRIPTS += np

EXTRA_DIST  += colfilter
bin_SCRIPTS += colfilter

EXTRA_DIST  += percheck
bin_SCRIPTS += percheck

EXTRA_DIST  += percheck.1.in
man_MANS    += percheck.1

EXTRA_DIST  += list-debuginfo-rpms
bin_SCRIPTS += list-debuginfo-rpms

EXTRA_DIST  += pdf2minibook
bin_SCRIPTS += pdf2minibook

dist_bin_SCRIPTS += strace-normalize

profiledir   = $(sysconfdir)/profile.d
EXTRA_DIST  += ndim-utils.sh
profile_DATA = ndim-utils.sh
