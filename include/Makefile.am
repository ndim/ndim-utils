BUILT_SOURCES = package-version.h build-info.h
CLEANFILES = $(BUILT_SOURCES)

package-version.h: $(top_srcdir)/ChangeLog Makefile
	TLA_ARCHIVE="$$(grep -E "^#.*arch-tag: " $<  | sed -e 's/^.*automatic-ChangeLog--//g' -e 's/\/.*$$//g')"; \
	TLA_REV="$$(grep -E -A1 -m1 '^[[:space:]]*Revision:$$' $< | awk '(NR == 2) { print $$1; }')"; \
	TLA_REVISION="$${TLA_ARCHIVE}/$${TLA_REV}"; \
	for var in TLA_REVISION; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "$@"

.PHONY: build-info.h
build-info.h:
	BUILD_DATE="$$(TZ=UTC date)"; \
	DATE_YEAR="$$(TZ=UTC date '+%Y')"; \
	for var in BUILD_DATE DATE_YEAR; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "$@"
