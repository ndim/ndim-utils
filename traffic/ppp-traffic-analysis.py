
#!/usr/bin/python


"""
traffic.py - evaluate ppp traffic log and create some statistics.

Manually find log lines on router via:

    (cd /var/log; for n in 9 8 7 6 5 4 3 2 1; do zcat daemon.log.${n}.gz; done; cat daemon.log.0 daemon.log) | grep "bytes, received"

The lines will look like:

    Mar 14 13:40:04 hostname pppd[4457]: Sent 104681198 bytes, received 831052288 bytes.

Collect these lines in a file, say, ppp.log.

Then run

    traffic.py ppp.log

and admire the statistics.

TODO:
 - Get log files from router via HTTP, updating (local) ppp log file.
 - Handle monotonously incrementing traffic counters (present since milou).
   This suggests a multi level approach to parsing.
   FIXME
 
"""


import sys


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


class TrafficStats:

    def __init__(self, logfile):
        self._readlog(logfile)

    def _readlog(self, logfile):
        
        self.sent = ByteStats()
        self.rcvd = ByteStats()
        self.traf = ByteStats()
        last_date = None
        last_pid = None

        # go through lines, accumulating values for each day
        while True:
            line = logfile.readline()
            if not line:
                self.sent.append(sent)
                self.rcvd.append(rcvd)
                self.traf.append(sent+rcvd)
                break
       		     
            arr = line.strip().split()
            if len(arr) == 0:
                continue
            assert(len(arr) == 11)
            assert(arr[5] == "Sent" and arr[7] == "bytes," and arr[8] == "received" and arr[10] == "bytes.")
            
            cur_date = "%s %2d" % (arr[0],int(arr[1]))
            if not(last_date):
                sent = 0
                rcvd = 0
                last_date = cur_date
            elif cur_date != last_date:
                self.sent.append(sent)
                self.rcvd.append(rcvd)
                self.traf.append(sent+rcvd)
                sent = 0
                rcvd = 0
                last_date = cur_date
                
            sent += int(arr[6])
            rcvd += int(arr[9])
            


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


syntax = """
Syntax: %s [<infile> [<outfile>]]

  <infile>   Name of ppp log file to read. Defaults to stdin.
  <outfile>  Name of traffic report to write. Defaults to stdout.
  
""" % (sys.argv[0])


def main():
    if len(sys.argv) > 3:
        sys.stderr.write("Syntax error: Too many parameters\n")
        sys.stderr.write(syntax)
        sys.exit(1)
    infile = sys.stdin
    outfile = sys.stdout
    if len(sys.argv) >= 2:
        #sys.stderr.write("Non-standard log file: %s\n" % sys.argv[1])
        infile = open(sys.argv[1], "r") # open log file
    if len(sys.argv) >= 3:
        #sys.stderr.write("Non-standard report file: %s\n" % sys.argv[2])
        outfile = open(sys.argv[2], "w") # open report file
    stats = TrafficStats(infile)
    stats.write_stats(outfile, True)


if __name__ == '__main__':
    print """
    Sorry, but this script "%s" is currently out of order.
    There is a serious bug which makes it unusable.
    Fix that first, and only then run it again.
    """ % sys.argv[0]
    sys.exit(1)
    main()

# arch-tag: d02a3a85-d37d-4c29-8c6d-348f630823b1
