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


import sys
import time
from whois import WhoisEngine


def write_nameserver_report(domains,output):
    eng = WhoisEngine()
    for line in domains.readlines():
        domain = line.strip()
        if (not domain) or (domain[0] in ['#']):
            continue
        result = eng.whois(domain)
        output.write(string.join([domain] + result,' '))
        output.write("\n")
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


# arch-tag: 1763989b-4b5a-4144-8d38-7e41d09ebcba