#include <stdio.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

const char *check_name = "[check]";

int check(int argc, char *argv[])
{
	fprintf(stderr, "nfat testcase\n");
	int fd = open("foodoesnexist", O_RDONLY);
	fprintf(stderr, "nfat testcase done.\n");
	return 0;
}

void fprintarr(FILE *fp,
		const char *title,
		const int argc, char *argv[])
{
	int i;
	fprintf(fp, ",-----[%s]\n", title);
	for (i=0; (i<argc) && (argv[i] != NULL); i++) {
		fprintf(fp, "|%s\n", argv[i]);
	}
	fprintf(fp, "`-----\n", title);
}

int run(int argc, char *argv[])
{
	fprintf(stderr, "nfat checker\n");
	char ld_preload[2000];
	char *lib = "";
	if (argc > 1) {
		lib = argv[1];
	}
	snprintf(ld_preload, sizeof(ld_preload), "LD_PRELOAD=", lib);
	char *envp[4] = {
		"SHELL=/bin/bash",
		"PATH=/bin:/usr/bin",
		ld_preload,
		NULL
	};
	char *_argv[2] = {
		check_name,
		NULL
	};
	const char *path = argv[0];
	fprintarr(stderr, "envp", sizeof(envp)/sizeof(envp[0]), envp);
	fprintarr(stderr, "argv", sizeof(_argv)/sizeof(_argv[0]), _argv);
	return execve(path, _argv, envp);
}

int main(int argc, char *argv[])
{
	return check(argc, argv);

	if (strcmp(check_name, argv[0]) == 0) {
		return check(argc, argv);
	} else {
		return run(argc, argv);
	}
	return 0;
}

/* arch-tag: 3e961e05-3c57-44e3-ad14-cc173912c534 */
