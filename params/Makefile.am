CLEANFILES =

EXTRA_DIST = params-outfile.1.in params-logfile.1.in

man_MANS = params-stderr.1 params-stdout.1 params-logfile.1

bin_PROGRAMS = params-stdout params-stderr params-logfile

params_stderr_SOURCES  = params-stderr.c  report-params.c report-params.h

params_stdout_SOURCES  = params-stdout.c  report-params.c report-params.h

LOGFILE_NAME = /tmp/params-logfile.log
params_logfile_SOURCES = params-logfile.c report-params.c report-params.h
params_logfile_CPPFLAGS = '-DLOGFILE_NAME="$(LOGFILE_NAME)"'

CLEANFILES += params-stderr.1
params-stderr.1: params-outfile.1.in
	$(SED) \
		-e 's|[@]OUTFILE[@]|stderr|g' \
		-e 's|[@]PACKAGE_TARNAME[@]|$(PACKAGE_TARNAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-outfile.1.in > params-stderr.1

CLEANFILES += params-stdout.1
params-stdout.1: params-outfile.1.in
	$(SED) \
		-e 's|[@]OUTFILE[@]|stdout|g' \
		-e 's|[@]PACKAGE_TARNAME[@]|$(PACKAGE_TARNAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-outfile.1.in > params-stdout.1

CLEANFILES += params-logfile.1
params-logfile.1: params-logfile.1.in
	$(SED) \
		-e 's|[@]LOGFILE_NAME[@]|$(LOGFILE_NAME)|g' \
		-e 's|[@]PACKAGE_TARNAME[@]|$(PACKAGE_TARNAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-logfile.1.in > params-logfile.1
