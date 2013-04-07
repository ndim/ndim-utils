#!/usr/bin/python


"""
%(prog)s - evaluate ppp traffic log and create some statistics.

Syntax:

  %(prog)s
    - Read ppp log from stdin.
    - Print statistics on stdout.
    
  %(prog)s <LOGFILE>
    - Update file <LOGFILE> via HTTP. Save old version to
      <LOGFILE>.bak if necessary.
    - Read ppp log from <LOGFILE>.
    - Print statistics on stdout.
    
  %(prog)s <LOGFILE> <REPORTFILE>
    - Update file <LOGFILE> via HTTP. Save old version to
      <LOGFILE>.bak if necessary.
    - Read ppp log from <LOGFILE>.
    - Print statistics into <REPORTFILE>.

Manually find log lines on router via:

    (cd /var/log; for n in 9 8 7 6 5 4 3 2 1; do zcat daemon.log.${n}.gz; done; cat daemon.log.0 daemon.log) | grep "bytes, received"

The lines will look like:

    Mar 14 13:40:04 hostname pppd[4457]: Sent 104681198 bytes, received 831052288 bytes.

Collect these lines in a file, say, ppp.log.

This program was designed with a LEAF Bering 2 router in mind, but any
linux router with PPP should do.


TODO:
 - nothing :)
 
"""


import sys
import urllib2
import os

router_host = "milou"


debug_level = 3
def debug(level, msg, params = None):
    if debug_level >= level:
        x = msg
        if not params:
            x = msg
        elif type(params) == type(()):
            x = msg % params
        elif type(params) == type({}):
            x = msg % params
        else:
            x = msg % (params)
        sys.stderr.write(x)
        if msg[-1:] != '\n' and msg[-3:] != '...':
            sys.stderr.write('\n')


def format_byte_value(value):
    # print "format value:", repr(value)
    if value > 1024*1014*1024*1024:
        x = "%.1f TB" % (float(value)/(1024*1024*1024*1024))
    elif value > 1024*1024*1024:
        x = "%.1f GB" % (float(value)/(1024*1024*1024))
    elif value > 1024*1024:
        x = "%.1f MB" % (float(value)/(1024*1024))
    elif value > 1024:
        x = "%.1f kB" % (float(value)/(1024))
    else:
        x = "%.1f  B" % (float(value))
    return x


class Stats:

    """Statistics for a number sampled at discrete times."""

    def __init__(self):
        self.values = []

    def append(self, value):
        x = float(value)
        if len(self.values) == 0:
            self.mavg9 = x
            self.mavg4 = x
            self.mavg1 = x
            self.avg = x
            self.max = x
            self.min = x
            self.total = x
        else:
            self.mavg9 = (9*self.mavg9 + 1*x)/10
            self.mavg4 = (4*self.mavg4 + 1*x)/5
            self.mavg1 = (1*self.mavg1 + 1*x)/2
            cnt = len(self.values)
            self.avg = (cnt*self.avg + x) / (cnt+1)
            self.total += x
            if x > self.max:
                self.max = x
            if x < self.min:
                self.min = x
        self.values.append(x)

    def count(self):
        return len(self.values)

    def average(self):
        return (float(self.total)/self.count())


class ByteStats(Stats):

    """Special statistic for a counted number of bytes"""

    pass


class Stage3:

    """Stage3 of the ppp log line parser

    Actually does something with the extracted values.
    """

    def __init__(self, host):
        self.host = host
        self.sent = ByteStats()
        self.rcvd = ByteStats()
        self.traf = ByteStats()
        self.finished = False

    def event(self, timestamp, host, pid, rcvd, sent):
        assert(not self.finished)
        debug(4,"stage3 event: %s", repr(vars()))
        debug(4,"              %s", repr(vars(self)))
        debug(3,"counting sent %d, rcvd %d for %s %2d.", (sent,rcvd,timestamp[0],timestamp[1]))
        self.sent.append(sent)
        self.rcvd.append(rcvd)
        self.traf.append(sent+rcvd)

    def finish(self):
        assert(not self.finished)
        debug(4,"stage3 finis: %s", repr(vars(self)))
        self.finished = True

    def result(self):
        assert(self.finished)
        return self

    def write_stats(self, outfile, detailed = False):
        assert(self.finished)

        def report(msg,fun):
            outfile.write("%s:\n" % msg)
            for k,v in (("total", self.traf),
                        ("sent", self.sent),
                        ("received", self.rcvd)):
                outfile.write("    %-10s" % k)
                val = fun(v)
                for unit,mult in (('year',365.0),                                  
                                  ('month',30.0),
                                  ('week',7.0),
                                  ('day',1.0),
                                  ('hour',1.0/(24)),
                                  ('min',1.0/(24*60)),
                                  ('sec',1.0/(24*60*60))):
                    outfile.write(" %9s/%s" % (format_byte_value(val*mult),unit))
                outfile.write("\n")

        outfile.write("Traffic statistics for router \"%s\"\n\n" % (self.host))

        report("Average traffic (arithmetic average)", lambda x: x.avg)
        outfile.write("\n")

        report("Average traffic (moving average, 1:9)", lambda x: x.mavg9)
        report("Average traffic (moving average, 1:4)", lambda x: x.mavg4)
        report("Average traffic (moving average, 1:1)", lambda x: x.mavg1)
        outfile.write("\n")

        report("Maximum traffic (based on maximum daily values)",
               lambda x: x.max)
        outfile.write("\n")

        report("Minimum traffic (based on minimum daily values)",
               lambda x: x.min)

        if detailed:
            outfile.write("\n")
            outfile.write("Detailed Stats:\n")
            outfile.write("    %-10s %4s\n" % ("days evaluated",self.traf.count()))
            for var,text in ((self.traf, "total"),
                             (self.sent, "sent"),
                             (self.rcvd, "received")):
                outfile.write("    %s traffic:\n" % text)
                for name,value in vars(var).items():
                    if name in ("values"): continue
                    outfile.write("        %-10s %9s\n" % (name,format_byte_value(value)))


class Stage2:

    """Stage 2 of the ppp log parser.

    Handles
    - multiple values per day
    """

    def __init__(self, host):
        self.host = host
        self.next = Stage3(host)

        self.last_date = None

        self.accu_rcvd = None
        self.accu_sent = None

        self.finished = False


    def event(self, timestamp, host, pid, rcvd, sent):
        assert(not self.finished)
        date = "%s %2d" % (timestamp[0], timestamp[1])
        debug(4,"stage2 event: %s", repr(vars()))
        debug(4,"              %s", repr(vars(self)))
        if not self.last_date:
            self.last_date = date
            self.last_timestamp = timestamp
            self.accu_rcvd = rcvd
            self.accu_sent = sent
        elif cmp(date,self.last_date) == 0:
            self.accu_rcvd += rcvd
            self.accu_sent += sent
        else:
            self.next.event(self.last_timestamp, host, pid, self.accu_rcvd, self.accu_sent)
            self.last_date = date
            self.last_timestamp = timestamp
            self.accu_rcvd = rcvd
            self.accu_sent = sent
        self.last_host = host
        self.last_pid = pid


    def finish(self):
        assert(not self.finished)
        debug(4,"stage2 finis: %s", repr(vars(self)))
        self.finished = True
        if self.last_date:
            self.next.event(self.last_timestamp, self.last_host, self.last_pid,
                            self.accu_rcvd, self.accu_sent)
        self.next.finish()


    def result(self):
        return self.next.result()


class Stage1:

    """Stage 1 of the ppp log parser.

    Preprocess the logs, accounting for
    - 32bit counter overflows
    - accumulating counters with same ppp PID
    """

    def __init__(self, host):
        self.host = host
        self.next = Stage2(host)

        self.last_pid = None
        
        self.last_rcvd = None
        self.last_sent = None

        self.finished = False

    def event(self, timestamp, host, pid, rcvd, sent):
        assert(not self.finished)
        debug(4,"stage1 event: %s", repr(vars()))
        debug(4,"              %s", repr(vars(self)))
        if host == self.host:
            if not self.last_pid:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_pid = pid
            elif self.last_pid == pid:

                while rcvd < self.last_rcvd:
                    rcvd += 2**32
                r = rcvd - self.last_rcvd
                assert(r >= 0)
                
                while sent < self.last_sent:
                    sent += 2**32
                s = sent - self.last_sent
                assert(s >= 0)
                
                self.next.event(timestamp, host, pid, r, s)
            else:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_pid = pid
            self.last_rcvd = rcvd
            self.last_sent = sent
        elif host == "gw":
            self.next.event(timestamp, host, pid, rcvd, sent)
        else:
            raise Exception("Unhandled host name: \"%s\"" % host)

    def finish(self):
        assert(not self.finished)
        debug(4,"stage1 finis: %s", repr(vars(self)))
        self.finished = True
        self.next.finish()

    def result(self):
        assert(self.finished)
        return self.next.result()


class LogFileParser:

    def __init__(self, logfile, host):
        self.logfile = logfile
        self.next = Stage1(host)

    def parse(self):       
        for line in self.logfile.readlines():
            if not line:
                continue
            stripped = line.strip()
            if not stripped:
                continue
            debug(3,"line:         %s", repr(stripped))
            
            arr = stripped.split()
            if len(arr) == 0:
                continue
            assert(len(arr) == 11)
            assert(arr[5] == "Sent" and arr[7] == "bytes,"
                   and arr[8] == "received" and arr[10] == "bytes.")

            timestrs = arr[2].split(':')
            timesint = (int(timestrs[0]), int(timestrs[1]), int(timestrs[2]))
            self.next.event(timestamp = (arr[0], int(arr[1]), timesint),
                            host = arr[3],
                            pid = arr[4],
                            sent = int(arr[6]),
                            rcvd = int(arr[9]))
        self.next.finish()

    def result(self):
        return self.next.result()


########################################################################
# HTTP Access stuff
########################################################################


class HTTPParser:

    def __init__(self, url):
        self.x = urllib2.urlopen(url)
        self.lines = []

    def handle_log_line(self, log_line):
        arr = log_line.split()
        if (arr[5] == "Sent" and arr[7] == "bytes,"
            and arr[8] == "received" and arr[10] == "bytes."
            and arr[4][:5] == "pppd[" and arr[4][-2:] == ']:'):
            #print "LOG:", repr(log_line)
            self.lines.append(log_line+'\n')

    def parse(self):
        code_begin = "<tr><td><div><code>\n"
        code_end = "</code></div></td></tr>\n"
        ignore = True
        for line in self.x.readlines():
            if (line == code_begin):
                ignore = False
                continue
            elif line == code_end:
                ignore = True
                continue
            else:
                pass

            if not ignore:
                if line[-5:] == '<br>\n':
                    self.handle_log_line(line[:-5])
                else:
                    pass # some error message like "file doesn't exist"
                #print repr(line[:-4])
                #print repr(line[-4:])
                


def update_logs(log_file, router_host):

    log_url = "http://" + router_host + "/cgi-bin/viewlogs?"
    debug(1,"Getting log files from \"%s\"...", log_url)
    for n in range(30,0,-1):
        log_url += "daemon.log.%d.gz+" % n
    log_url += "daemon.log.0+daemon.log"

    parser = HTTPParser(log_url)
    parser.parse()
    debug(1," done.\n")

    logfile_present = os.path.exists(log_file)

    if logfile_present:
        content = open(log_file, "r").readlines()
    else:
        content = []

    dirty = False
    for new_line in parser.lines:
        if new_line not in content:
            content.append(new_line)
            dirty = True

    if dirty and logfile_present:
        bak = "%s.bak" % log_file
        debug(1,"Renaming old log file %s to %s...",
              (log_file, bak))
        os.rename(log_file, bak)
        debug(1," done.\n")

    if dirty:
        # no, we don't create empty log files
        debug(1,"Writing updated log file to %s...", log_file)
        fd = os.open(log_file, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0600)
        f = os.fdopen(fd,"w")
        for x in content:
            f.write(x)
        f.close()
        debug(1," done.\n")

    
########################################################################
# Main program
########################################################################


def main():

    if len(sys.argv) > 3:
        debug(0,"Syntax error: Too many parameters\n")
        v = { 'prog': sys.argv[0] }
        debug(0, __doc__, v)
        sys.exit(1)

    infile = sys.stdin
    if len(sys.argv) >= 2:
        debug(2, "Non-standard log file: %s\n", sys.argv[1])
        update_logs(sys.argv[1], router_host)
        infile = open(sys.argv[1], "r") # open log file

    outfile = sys.stdout
    if len(sys.argv) >= 3:
        debug(2,"Non-standard report file: %s\n", sys.argv[2])
        outfile = open(sys.argv[2], "w") # open report file
        
    debug(1,"Parsing current log file...")
    parser = LogFileParser(infile, router_host)
    parser.parse()
    stats = parser.result()
    debug(1," done.\n")
    
    stats.write_stats(outfile, True)


if __name__ == '__main__':
    main()
