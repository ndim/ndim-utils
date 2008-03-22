BUILT_SOURCES = build-info.stamp
CLEANFILES = $(BUILT_SOURCES) build-info.h

build-info.stamp:
	BUILD_DATE="$$(TZ=UTC date)"; \
	DATE_YEAR="$$(TZ=UTC date '+%Y')"; \
	for var in BUILD_DATE DATE_YEAR; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "build-info.h"
