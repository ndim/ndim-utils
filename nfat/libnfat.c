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

#define DEBUG
#undef USE_SYSLOG
#include "libnfat.h"


/**********************************************************************
 * Filename substitution
 **********************************************************************/

static const subst_string subst_map[] = {
	{replace: "/etc/hosts", by: "/etc/resolv.conf"},
	{NULL, NULL}
};

static const char *substitute_filename(const char *orig_fname)
{
	int i;
	char *retptr;
	char resolved_orig[PATH_MAX];
	retptr = realpath(orig_fname, resolved_orig);
	if (NULL == retptr) {
		__LOG__("realpath(\"%s\",%p) = %s, errno = %d\n",
			orig_fname, &resolved_orig, "NULL", errno);
		return orig_fname;
	}
	for (i=0; (subst_map[i].replace != NULL) && 
	       (subst_map[i].by != NULL); i++) {
		char resolved_this[PATH_MAX];
		retptr = realpath(subst_map[i].replace, resolved_this);
		if (NULL != retptr) {
			if (strcmp(resolved_this, resolved_orig) == 0) {
				return subst_map[i].by;
			}
		}
	}
	return orig_fname;
}


/**********************************************************************
 * Wrap open(2)
 **********************************************************************/

static int (*rtld_next_open) (__const char *__file, int __oflag, ...);
int open (__const char *__file, int __oflag, ...)
{
	const char *fname = substitute_filename(__file);
	int retval;
	char *retptr;
	LD_WRAP(open);
	retval = rtld_next_open(fname, __oflag);
	__LOG__("open(\"%s\", 0x%0x, ...) = %d, errno = %d\n", fname, __oflag, retval, errno);
	return retval;
}


/*
 * Local Variables:
 * mode: c
 * c-basic-offset: 8
 * End:
 */
/* arch-tag: 8ba5c0da-ec39-4d62-b65c-c8ebd5c49da2 */
