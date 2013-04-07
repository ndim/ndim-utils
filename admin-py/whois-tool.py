#!/usr/bin/python

"""
Usage:
   %(progname)s [<file-with-list-of-domains>] [<output-file>]
   %(progname)s [<file-with-list-of-domains>]
   %(progname)s

Function:
- Reads domains from the <file-with-list-of-domains>.
  Each line contains one domain, lines starting with # are comments.
- Contacts the appropriate whois server for each domain and parses the
  result.
- The domain and its nameservers are then written to <output-file>.

If either filename is not given, stdout/stdin are used.
"""

"""
Possible ways to evolution:

 * change it into some kind of "DNS lint" which checks that whois and DNS
   are all consistent.
"""


import sys
import string
import time
import whois


def write_nameserver_report(domains,output):
    eng = whois.WhoisEngine(sys.stderr)
    for line in domains.readlines():
        domain = line.strip()
        if (not domain) or (domain[0] in ['#']):
            continue
        result = None
        try:
            result = eng.whois(domain)
        except whois.NoWhoisServerError:
            pass
        if result:
            sys.stderr.write("\n")
            sys.stderr.write(str(result))
            sys.stderr.write("\n")
            # FIXME: handle strings like "ns.foobar.de 1.2.3.4"
            output.write(string.join([domain] + result.nameservers,' '))
            output.write("\n")
            output.flush()
        else:
            output.write("%s #\n" % domain);
            output.flush()


if __name__ == '__main__':
    if "--help" in sys.argv:
        progname = sys.argv[0]
        print __doc__ % vars()
        sys.exit(0)
    infile = sys.stdin
    outfile = sys.stdout
    if len(sys.argv) >= 2:
        infile = open(sys.argv[1], "r")
    if len(sys.argv) >= 3:
        outfile = open(sys.argv[2], "w")
    write_nameserver_report(infile, outfile)
