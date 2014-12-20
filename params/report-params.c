#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

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

	do {
		/* must be large enough for "/proc/self/fd/${fd}" */
		char procfd[512];

		/* must be large enough for the readlink(2) result */
		char buf[PATH_MAX + 64*1024];

		fprintf(out, "#fd file\n");
		const int fd_open_max = sysconf(_SC_OPEN_MAX);
		for (int fd=0; fd<fd_open_max; ++fd) {
			const int snp = snprintf(procfd, sizeof(procfd),
						 "/proc/self/fd/%u", fd);
			assert(snp > 0);
			assert(((size_t)snp) < sizeof(procfd));
			const ssize_t ss = readlink(procfd, buf, sizeof(buf));
			if (ss < 0) {
				if (errno == ENOENT) {
					/* ignore closed fd numbers */
				} else {
					perror("readlink");
					exit(EXIT_FAILURE);
				}
			} else {
				fprintf(out, "%3d %s\n", fd, buf);
			}
		}
	} while (0);

	do {
		char buf[PATH_MAX + 64*1024];
		if (NULL == getcwd(buf, sizeof(buf))) {
			fprintf(out, "CWD ERROR: %s", strerror(errno));
		}
		fprintf(out, "CWD %s\n", buf);
	} while (0);
}
