bin_PROGRAMS = params @PACKAGE_TARNAME@-info
params_SOURCES = params.c

BUILT_SOURCES = pkg-info.h
CLEANFILES = pkg-info.h

@PACKAGE_TARNAME@_info_SOURCES = pkg-info.c pkg-info.h

pkg-info.h: Makefile
	TLA_REVISION="$$(tla revisions --full | tail -n1)"; \
	for var in TLA_REVISION; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "$@"
