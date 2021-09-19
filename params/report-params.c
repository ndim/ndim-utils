#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#include <sys/types.h>
#include <grp.h>
#include <pwd.h>

#include <selinux/selinux.h>

#include "report-params.h"


static
char *gid_to_name(const gid_t gid)
{
    struct group *g = getgrgid(gid);
    assert(g);

    return(g->gr_name);
}


static
char *uid_to_name(const uid_t uid)
{
    struct passwd *p = getpwuid(uid);
    assert(p);

    return(p->pw_name);
}


static
void report_fds(FILE *out)
{
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
            fprintf(out, "%6d %s\n", fd, buf);
        }
    }
}


static
void report_setXid(FILE *out)
{
    do {
        uid_t ruid, euid, suid;
        assert(0 == getresuid(&ruid, &euid, &suid));
        fprintf(out,
                "%6s ruid=%d(%s) euid=%d(%s) suid=%d(%s)\n",
                "xUID",
                ruid, uid_to_name(ruid),
                euid, uid_to_name(euid),
                suid, uid_to_name(suid));
    } while (0);

    do {
        gid_t rgid, egid, sgid;
        assert(0 == getresgid(&rgid, &egid, &sgid));
        fprintf(out,
                "%6s rgid=%d(%s) egid=%d(%s) sgid=%d(%s)\n",
                "xGID",
                rgid, gid_to_name(rgid),
                egid, gid_to_name(egid),
                sgid, gid_to_name(sgid));
    } while (0);
}


static
void report_grouplist(FILE *out)
{
    gid_t gid_list[256];
    const size_t gid_list_sz =
        sizeof(gid_list)/sizeof(gid_list[0]);
    const int no_groups = getgroups(gid_list_sz, gid_list);
    assert(no_groups >= 0);
    const unsigned int u_no_groups = no_groups;
    fprintf(out, "%6s ", "GRPs");
    for (size_t i=0; i<u_no_groups; ++i) {
        if (i == (u_no_groups-1)) {
            fprintf(out, "%d(%s)\n", gid_list[i],
                    gid_to_name(gid_list[i]));
        } else {
            fprintf(out, "%d(%s),", gid_list[i],
                    gid_to_name(gid_list[i]));
        }
    }
}


static
void report_context(FILE *out)
{
    char *con;
    if (0 == getcon(&con)) {
        fprintf(out, "%6s %s\n", "CTX", con);
        freecon(con);
    }
}


static
void report_misc(FILE *out)
{
    fprintf(out, "Miscellaneous properties\n");

    char buf[PATH_MAX + 64*1024];
    if (NULL == getcwd(buf, sizeof(buf))) {
        fprintf(out, "CWD ERROR: %s", strerror(errno));
    }
    fprintf(out, "%6s %s\n", "CWD", buf);

    fprintf(out, "%6s %d\n", "PID",  getpid());
    fprintf(out, "%6s %d\n", "PPID", getppid());

    fprintf(out, "%6s %d\n", "SID", getsid(0));
    fprintf(out, "%6s %d\n", "PGRP", getpgrp());

    do {
        const uid_t uid = getuid();
        fprintf(out, "%6s %d(%s)\n", "UID",
                uid, uid_to_name(uid));

        const uid_t euid = geteuid();
        fprintf(out, "%6s %d(%s)\n", "EUID",
                euid, uid_to_name(euid));

        const gid_t gid = getgid();
        fprintf(out, "%6s %d(%s)\n", "GID",
                gid, gid_to_name(gid));

        const gid_t egid = getegid();
        fprintf(out, "%6s %d(%s)\n", "EGID",
                egid, gid_to_name(egid));
    } while (0);

    report_setXid(out);
    report_grouplist(out);
    report_context(out);
}


void report_params(FILE *out, int argc, char *argv[], char *env[])
{
    do {
        fprintf(out, "#nr environment variable\n");
        for (int i=0; env[i] != NULL; i++)
            fprintf(out, "%6d %s\n", i, env[i]);
    } while (0);

    do {
        fprintf(out, "#nr parameter\n");
        for (int i=0; i<argc; i++)
            fprintf(out, "%6d %s\n", i, argv[i]);
    } while (0);

    report_fds(out);

    report_misc(out);
}


/*
 * Local Variables:
 * indent-tabs-mode: nil
 * c-basic-offset: 4
 * tab-width: 8
 * End:
 */
