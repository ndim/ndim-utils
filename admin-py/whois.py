#!/usr/bin/python


"""whois library"""


import socket
import select
import re
import time


class DomainInfos:

    def __init__(self, domain):
        self.domain = domain
        self.nameservers = []

    def add_nameserver(self, nameserver):
        self.nameservers.append(nameserver)


class AbstractParser:

    """Abstract parser for whois data"""

    def parse(self, page, infos):
        """Parse the whois results in page.

        Return the parsed data in a format which has to be properly
        designed yet."""
        return [ "unknown" ]


class DenicParser(AbstractParser):

    """Parse results from Denic whois server."""

    def parse(self, page, infos):
        """Parse result of whois server.

        Returns only nameservers so far.
        """
        re_map = {
            "comment": re.compile("^%"),
            "empty":   re.compile("^$"),
            "value":   re.compile("^([a-zA-Z\-]+): +(.+)"),
            "header":  re.compile("^((\[[a-zA-Z\-]+\]))+$"),
            }
        nameservers = []
        n = 0
        for line in page.splitlines():
            n = n + 1
            linetype = None
            for (k,v) in re_map.items():
                match = v.match(line)
                if match:
                    linetype = k
                    break
            # print "%-7s %3d: %s" % (linetype,n,repr(line))
            if match:
                # print "            ", match.groups()
                pass
            else:
                print "Parse error: Unrecognized line type"
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["nserver"]:
                    nameservers.append(value.lower())
        return nameservers
    

class CrsnicParser(AbstractParser):

    """Parse results from crsnic whois server"""

    def parse(self, page, infos):
        """Parse result of whois server.

        Returns only nameservers so far.
        """
        re_map = (
            ("empty",   re.compile("^$")),
            ("value",   re.compile("^ +([a-zA-Z\- ]+): +(.+)")),
            ("comment", re.compile("")),
            )
        nameservers = []
        n = 0
        for line in page.splitlines():
            n = n + 1
            linetype = None
            for (k,v) in re_map:
                match = v.match(line)
                if match:
                    linetype = k
                    break
            # print "%-7s %3d: %s" % (linetype,n,repr(line))
            if match:
                # print "            ", match.groups()
                pass
            else:
                print "Parse error: Unrecognized line type"
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["nserver","Name Server"]:
                    nameservers.append(value.lower())
        return nameservers


class NameParser(AbstractParser):

    """Parse results from whois.nic.name"""

    def parse(self, page, infos):
        """Parse result of whois server.

        Returns only nameservers so far.
        """
        re_map = (
            ("empty",   re.compile("^$")),
            ("value",   re.compile("^([a-zA-Z\- ]+): *(.+)")),
            ("comment", re.compile("")),
            )
        nameservers = []
        n = 0
        for line in page.splitlines():
            n = n + 1
            linetype = None
            for (k,v) in re_map:
                match = v.match(line)
                if match:
                    linetype = k
                    break
            # print "%-7s %3d: %s\n" % (linetype,n,repr(line))
            if match:
                # print "            ", match.groups()
                pass
            else:
                print "Parse error: Unrecognized line type"
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["nserver","Name Server"]:
                    nameservers.append(value.lower())
        return nameservers


class WhoisEngine:

    """The whole beast with user API"""

    parser_list = {
        'whois.denic.de': DenicParser,
        'whois.crsnic.net': CrsnicParser,
        'whois.nic.name': NameParser,
        'whois.publicinterestregistry.net': NameParser,
        'whois.afilias.info': NameParser,
        }


    def __init__(self):
        # read in list of whois servers
        f = open("whoislist","r")
        self.whois_servers = {}
        for line in f.readlines():
            t = line.strip().split('|')
            if t[1] == 'NONE':
                pass
            elif t[1] == 'WEB':
                pass
            else:
                self.whois_servers[t[0]] = t[1]


    def connected_socket(self,whois_server):
        """Return an opened socket to the whois server"""
        s = None
        while s == None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setblocking(0)
                try:
                    s.connect((whois_server, 43))
                except socket.error, (ecode, reason):
                    if ecode in [115, 150]: pass
                    else:
                        raise socket.error, (ecode, reason)
                ret = select.select([s],[s],[],30)
                if len(ret[1]) == 0 and len(ret[0]) == 0:
                    s.close()
                    raise TimedOut, "on connect "
                s.setblocking(1)
            except socket.error, (ecode, reason):
                print ecode, reason
                time.sleep(10)
                s = None
        return s


    def query_whois(self,domain):
        """Pose the actual query and read in the results"""
        idx = domain.rindex('.')
        (sld,tld) = (domain[:idx],domain[idx+1:])
        whois_server = None
        try:
            whois_server = self.whois_servers[tld]
        except KeyError:
            return None
        s = self.connected_socket(whois_server)
        query = domain
        if tld == "de":
            query = "-T ace,dn " + query
        s.send("%s\r\n" % query)
        page = ""
        while 1:
            data = s.recv(8196)
            if not data:
                break
            page = page + data
        s.close()
        return (whois_server,page)


    def whois(self,domain):
        """Execute and parse whois query for the given domain"""
        (server,page) = self.query_whois(domain)
        # page = open("testdata","r").read()
        if page and WhoisEngine.parser_list.has_key(server):
            cls = WhoisEngine.parser_list[server]
            parser = cls()
            return parser.parse(page)
        else:
            return ['UNKNOWN/UNHANDLED']

# arch-tag: ff80d68a-8a64-468b-9e69-51c6157580b2
