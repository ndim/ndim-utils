#ifndef __LIBNFAT_H__


/**********************************************************************
 * Log messages
 **********************************************************************/

#define LOG_STRING "libnfat"

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


/**********************************************************************
 * String substitution
 **********************************************************************/

struct _subst_string {
	char *replace;
	char *by;
};

typedef struct _subst_string subst_string;


/**********************************************************************
 * Wrap library function func
 **********************************************************************/

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


#endif

/* arch-tag: 3878ef09-e4c3-4003-ab31-1c45a784a278 */
