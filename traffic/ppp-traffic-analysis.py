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

    def __init__(self):
        self.values = []

    def append(self,value):
        x = float(value)
        if len(self.values) == 0:
            self.mavg9 = value
            self.mavg5 = value
            self.avg = value
            self.max = value
            self.min = value
            self.total = value
        else:
            self.mavg9 = 0.9*self.mavg9 + 0.1*x
            self.mavg5 = 0.5*self.mavg5 + 0.5*x
            cnt = len(self.values)
            self.avg = (cnt*self.avg + value) / (cnt+1)
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

    pass


class Stage2:

    def __init__(self):
        self.sent = ByteStats()
        self.rcvd = ByteStats()
        self.traf = ByteStats()

    def event(self, timestamp, host, pid, rcvd, sent):
        # print "stage2 event:", vars()
        self.sent.append(sent)
        self.rcvd.append(rcvd)
        self.traf.append(sent+rcvd)

    def result(self):
        return self

    def write_stats(self, outfile, detailed = False):

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

        report("Average traffic (arithmetic average)", lambda x: x.avg)
        report("Average traffic (moving average, 1:9)", lambda x: x.mavg9)
        report("Average traffic (moving average, 1:1)", lambda x: x.mavg5)
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


class Stage1:

    def __init__(self):
        self.next = Stage2()

        self.last_pid = None
        self.last_date = None
        
        self.last_rcvd = None
        self.last_sent = None

    def event(self, timestamp, host, pid, rcvd, sent):
        #print "stage1 event:", vars()
        #print "             ", vars(self)
        if host == "milou":
            if not self.last_pid:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_pid = pid
            elif self.last_pid == pid:
                if rcvd < self.last_rcvd:
                    rcvd += 2**32
                if sent < self.last_sent:
                    sent += 2**32
                r = rcvd - self.last_rcvd
                s = sent - self.last_sent
                assert(r >= 0)
                assert(s >= 0)
                self.next.event(timestamp, host, pid, r, s)
            else:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_pid = pid
        elif host == "gw":
            date = "%s %2d" % (timestamp[0], int(timestamp[1]))
            if not self.last_date:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_date = date
            elif self.last_date == date:
                r = rcvd - self.last_rcvd
                s = sent - self.last_sent
                assert(r >= 0)
                assert(s >= 0)
                self.next.event(timestamp, host, pid, r, s)
            else:
                self.next.event(timestamp, host, pid, rcvd, sent)
                self.last_date = date
        self.last_rcvd = rcvd
        self.last_sent = sent
                

    def result(self):
        return self.next.result()


class LogFileParser:

    def __init__(self, logfile):
        self.logfile = logfile
        self.next = Stage1()

    def parse(self):       
        for line in self.logfile.readlines():
            if not line:
                continue
    
            arr = line.strip().split()
            if len(arr) == 0:
                continue
            assert(len(arr) == 11)
            assert(arr[5] == "Sent" and arr[7] == "bytes,"
                   and arr[8] == "received" and arr[10] == "bytes.")

            self.next.event(timestamp = arr[0:2],
                            host = arr[3],
                            pid = arr[4],
                            sent = int(arr[6]),
                            rcvd = int(arr[9]))


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
                


def update_logs(log_file):

    router = "milou"
    log_url = "http://" + router + "/cgi-bin/viewlogs?"
    sys.stderr.write("Getting log files from \"%s\"..." % log_url)
    for n in range(30,0,-1):
        log_url += "daemon.log.%d.gz+" % n
    log_url += "daemon.log.0+daemon.log"

    parser = HTTPParser(log_url)
    parser.parse()
    sys.stderr.write(" done.\n")

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
        sys.stderr.write("Renaming old log file %s to %s\n" %
                         (log_file, bak))
        os.rename(log_file, bak)
        sys.stderr.write(" done.\n")

    if dirty:
        # no, we don't create empty log files
        sys.stderr.write("Writing updated log file to %s..." % log_file)
        f = os.fdopen(os.open(log_file, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0600),"w")
        for x in content:
            f.write(x)
        f.close()
        sys.stderr.write(" done.\n")

    
########################################################################
# Main program
########################################################################


def main():
    
    if len(sys.argv) > 3:
        sys.stderr.write("Syntax error: Too many parameters\n")
        v = { 'prog': sys.argv[0] }
        sys.stderr.write(__doc__ % v)
        sys.exit(1)

    infile = sys.stdin
    if len(sys.argv) >= 2:
        update_logs(sys.argv[1])
        #sys.stderr.write("Non-standard log file: %s\n" % sys.argv[1])
        infile = open(sys.argv[1], "r") # open log file

    outfile = sys.stdout
    if len(sys.argv) >= 3:
        #sys.stderr.write("Non-standard report file: %s\n" % sys.argv[2])
        outfile = open(sys.argv[2], "w") # open report file
        
    sys.stderr.write("Parsing log file...")
    parser = LogFileParser(infile)
    parser.parse()
    stats = parser.result()
    sys.stderr.write(" done.\n")
    
    stats.write_stats(outfile, True)


if __name__ == '__main__':
    main()

# arch-tag: d02a3a85-d37d-4c29-8c6d-348f630823b1
