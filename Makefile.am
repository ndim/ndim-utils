SUBDIRS = m4 include admin-py cdburn misc misc-scripts tla pkg-info palm-scripts traffic

doc_DATA = README AUTHORS NEWS

ACLOCAL_AMFLAGS = -I m4 --install

EXTRA_DIST = git-version.sh

tag:
	git status;:
	@echo "Wanna tag as v@PACKAGE_VERSION@? Enter to continue, Ctrl-C to abort."
	@read
	git tag v@PACKAGE_VERSION@
