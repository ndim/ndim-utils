#include <stdio.h>
#include <stdlib.h>

#include "report-params.h"


int main(int argc, char *argv[], char *env[])
{
	report_params(stdout, argc, argv, env);
	return EXIT_SUCCESS;
}
