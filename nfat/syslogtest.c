#include <syslog.h>

int main(int argc, char *argv[])
{
	openlog("syslogtest", LOG_PID, LOG_USER);
	syslog(LOG_INFO, "SYSLOG TEST MESSAGE");
	closelog();
	return 0;
}

/* arch-tag: 1cba738f-a5d9-41d8-8583-0271dfbad935 */
