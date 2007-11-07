BUILT_SOURCES = git-version.stamp build-info.stamp
CLEANFILES = $(BUILT_SOURCES) git-version.h build-info.h

GIT_VERSION_CMD = $(SHELL) $(top_srcdir)/git-version.sh
git-version.stamp:
	env GIT_DIR="$(top_srcdir)/.git" $(GIT_VERSION_CMD) -s $(top_srcdir) -o git-version.h
	@if test -s "$(srcdir)/git-version.h"; then \
		if cmp "$(srcdir)/git-version.h" "git-version.h"; then :; \
		else \
			echo "Error: $(srcdir)/git-version.h and git-version.h differ."; \
			echo "       You probably want to remove the former."; \
			exit 1; \
		fi; \
	fi

build-info.stamp:
	BUILD_DATE="$$(TZ=UTC date)"; \
	DATE_YEAR="$$(TZ=UTC date '+%Y')"; \
	for var in BUILD_DATE DATE_YEAR; do \
		export var; \
		echo "#define $$var \"$$(eval echo "\$$$$var")\""; \
	done > "build-info.h"
