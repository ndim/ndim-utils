#include <stdio.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

const char *check_name = "[check]";

int test(int argc, char *argv[])
{
	const char *filenames[] = {
		"foodoesbarnotblahexist",
		"/etc/hosts",
		"/etc/passwd",
		NULL
	};
	int i;
	for (i=0; filenames[i] != NULL; i++) {
		int fd, cnt;
		char buf[40];
		const char msg[] = "Beginning of file: ";
		fprintf(stderr, "nfat testcase \"%s\"\n", filenames[i]);
		fd = open(filenames[i], O_RDONLY);
		if (fd < 0) {
			fprintf(stderr, "Couldn't open file %s: ",
				filenames[i]);
			perror(NULL);
			continue;
		}
		cnt = read(fd, buf, sizeof(buf));
		if (cnt < 0) {
			fprintf(stderr, "Couldn't read from file %s: ",
				filenames[i]);
			continue;
		}
		write(STDERR_FILENO, msg, strlen(msg));
		write(STDERR_FILENO, buf, cnt);
		write(STDERR_FILENO, "\n", 1);
		close(fd);
		fprintf(stderr, "nfat testcase \"%s\" done.\n", filenames[i]);
	}
	return 0;
}

int main(int argc, char *argv[])
{
	return test(argc, argv);
}

/* arch-tag: 1ff871c2-443a-4c57-9282-dcd199008e2c */
