#define _GNU_SOURCE

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <unistd.h>
#include <stdio.h>

#include <dlfcn.h>
#include <errno.h>

#include <limits.h>
#include <stdlib.h>

#define LOG_STRING "libnfat"

#define DEBUG

#ifndef DEBUG
# define __LOG__(msg, params...)
#else
# ifdef USE_SYSLOG
#  include <syslog.h>
#  define __LOG__(msg, params...) \
	do { \
		openlog(LOG_STRING, LOG_PID, LOG_USER); \
		syslog(LOG_INFO, msg, ##params); \
		closelog(); \
	} while (0);
# else
#  define __LOG__(msg, params...) \
	do { \
		fprintf(stderr, "%s[%i]: " msg, \
			LOG_STRING, getpid(), ##params); \
	} while (0);
# endif
#endif

#define LD_WRAP(func) \
	do { \
	if (rtld_next_ ## func == NULL) { \
		char *msg; \
		rtld_next_ ## func = dlsym(RTLD_NEXT, #func); \
		if ((msg=dlerror())!=NULL) { \
			__LOG__("wrapping of %s(): dlsym/dlopen failed: %s\n", \
				#func, msg); \
		} \
		__LOG__("wrapping of %s(): done.\n", #func); \
	} \
	} while (0);

struct _subst_fname {
	char *replace;
	char *by;
};

typedef struct _subst_fname subst_fname;

static const subst_fname subst_map[] = {
	{replace: "/etc/hosts", by: "/etc/resolv.conf"},
	{NULL, NULL}
};

static char *substitute_filename(const char *orig_fname)
{
	int i;
	for (i=0; (subst_map[i].replace != NULL) && 
	       (subst_map[i].by != NULL); i++) {
	}
}

static int (*rtld_next_open) (__const char *__file, int __oflag, ...);
int open (__const char *__file, int __oflag, ...)
{
	char *fname = __file;
	int retval;
	char *retptr;
	char resolved_file[PATH_MAX];
	LD_WRAP(open);
	retptr = realpath(fname, resolved_file);
	if (NULL == retptr) {
		__LOG__("realpath(\"%s\",%p) = %s, errno = %d\n",
			fname, &resolved_file, "NULL", errno);
		return -1;
	}
	char resolved_hosts[PATH_MAX];
	retptr = realpath("/etc/hosts", resolved_hosts);
	if (NULL != retptr) {
		if (strcmp(resolved_hosts, resolved_file) == 0) {
			fname = "/etc/resolv.conf";
		}
	}
	retval = rtld_next_open(fname, __oflag);
	__LOG__("open(\"%s\", 0x%0x, ...) = %d, errno = %d\n", __file, __oflag, retval, errno);
	return retval;
}

/* arch-tag: 8ba5c0da-ec39-4d62-b65c-c8ebd5c49da2 */
