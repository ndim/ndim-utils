bin_PROGRAMS = @PACKAGE_TARNAME@-info

BUILT_SOURCES = pkg-info.h
CLEANFILES = pkg-info.h

@PACKAGE_TARNAME@_info_SOURCES = pkg-info.c pkg-info.h

.PHONY: pkg-info.h
pkg-info.h:
	BUILD_DATE="$$(TZ=UTC date)"; \
	DATE_YEAR="$$(TZ=UTC date '+%Y')"; \
	xxx="$$(tla revisions --full | tail -n1)"; \
	TLA_REVISION="$$(tla parse-package-name --non-arch "$$xxx")"; \
	TLA_ARCHIVE="$$(tla parse-package-name --arch "$$xxx")"; \
	for var in BUILD_DATE DATE_YEAR TLA_REVISION TLA_ARCHIVE; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "$@"
