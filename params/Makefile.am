CLEANFILES =
EXTRA_DIST =
man_MANS =
bin_PROGRAMS =


bin_PROGRAMS += params-stderr
params_stderr_SOURCES  = params-stderr.c
params_stderr_SOURCES += report-params.c report-params.h


bin_PROGRAMS += params-stdout
params_stdout_SOURCES  = params-stdout.c
params_stdout_SOURCES += report-params.c report-params.h


LOGFILE_NAME = /tmp/params-logfile.log
bin_PROGRAMS += params-logfile
params_logfile_SOURCES   = params-logfile.c
params_logfile_SOURCES  += report-params.c report-params.h
params_logfile_CPPFLAGS  = '-DLOGFILE_NAME="$(LOGFILE_NAME)"'


EXTRA_DIST += params-outfile.1.in

man_MANS += params-stderr.1
CLEANFILES += params-stderr.1
params-stderr.1: params-outfile.1.in
	$(SED) \
		-e 's|[@]OUTFILE[@]|stderr|g' \
		-e 's|[@]PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-outfile.1.in > params-stderr.1

man_MANS += params-stdout.1
CLEANFILES += params-stdout.1
params-stdout.1: params-outfile.1.in
	$(SED) \
		-e 's|[@]OUTFILE[@]|stdout|g' \
		-e 's|[@]PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-outfile.1.in > params-stdout.1

man_MANS   += params-logfile.1
EXTRA_DIST += params-logfile.1.in
CLEANFILES += params-logfile.1
params-logfile.1: params-logfile.1.in
	$(SED) \
		-e 's|[@]LOGFILE_NAME[@]|$(LOGFILE_NAME)|g' \
		-e 's|[@]PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
		-e 's|[@]PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
		< $(srcdir)/params-logfile.1.in > params-logfile.1
