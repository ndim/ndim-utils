#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "report-params.h"


const char *logfile_name = LOGFILE_NAME;


int main(int argc, char *argv[], char *env[])
{
	FILE *logfile = fopen(logfile_name, "a");

	if (!logfile) {
		const char *errstr = strerror(errno);
		fprintf(stderr, "FATAL: %s: %s\n", errstr, logfile_name);
		return EXIT_FAILURE;
	}

	report_params(logfile, argc, argv, env);
	return EXIT_SUCCESS;
}
