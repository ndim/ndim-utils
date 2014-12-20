#include "report-params.h"


void report_params(FILE *out, int argc, char *argv[], char *env[])
{
	do {
		fprintf(out, "#nr environment variable\n");
		for (int i=0; env[i] != NULL; i++)
			fprintf(out, "%3d %s\n", i, env[i]);
	} while (0);

	do {
		fprintf(out, "#nr parameter\n");
		for (int i=0; i<argc; i++)
			fprintf(out, "%3d %s\n", i, argv[i]);
	} while (0);

}
