"""whois library"""


import socket
import select
import re
import time


class ServerQueryError(Exception):

    """Server query failed somehow"""

    def __init__(self, server, domain):
        self.server = server
        self.domain = domain

    def __str__(self):
        return "Error asking %s about %s" % (self.server, self.domain)
        

class NoWhoisServerError(Exception):

    """No whois server for this domain"""

    def __init__(self, domain):
        self.domain = domain

    def __str__(self):
        return "No whois server for domain %s" % (self.domain)


class UnhandledWhoisServer(Exception):

    """No parser for this whois server"""

    def __init__(self, server):
        self.server = server

    def __str__(self):
        return "No parser handling %s" % (self.server)


class WhoisParseError(Exception):

    """Error parsing whois reply"""

    def __init__(self, page, lineno):
        self.page = page
        self.lineno = lineno

    def __str__(self):
        return "%d: %s" % (self.lineno,
                           self.page.splitlines()[self.lineno-1])


class DomainInfos:

    """Collects all the information about a domain"""

    def __init__(self, domain):
        self.domain = domain
        self.status = None
        self.nameservers = []

    def add_nameserver(self, nameserver):
        self.nameservers.append(nameserver.lower())

    def set_status(self, status):
        self.status = status.lower()

    def set_encoded_domain(self, encoding, domain):
        self.encoded_domain = domain.lower()
        self.encoding = encoding.lower()

    def set_i18n_domain(self, domain):
        self.i18n_domain = domain.lower()

    def set_updated(self, updated):
        self.updated = updated

    def __str__(self):
        x = "DomainInfos for domain %s:\n" % self.domain
        ks = list(vars(self).keys())
        ks.sort()
        for k in ks:
            if not k == 'domain':
                x += "    %s: %s\n" % (k,vars(self)[k])
        return x


class AbstractParser:

    """Abstract parser for whois data"""

    def parse(self, page, infos):
        """Parse the whois results in page.

        Return the parsed data in a format which has to be properly
        designed yet."""
        return infos


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
            for (k,v) in list(re_map.items()):
                match = v.match(line)
                if match:
                    linetype = k
                    break
            # print "%-7s %3d: %s" % (linetype,n,repr(line))
            if match:
                # print "            ", match.groups()
                pass
            else:
                print("Parse error: Unrecognized line type")
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["nserver"]:
                    infos.add_nameserver(value)
                if key in ["status"]:
                    infos.set_status(value)
                if key in ["domain"]:
                    infos.set_i18n_domain(value)
                if key in ["domain-ace"]:
                    infos.set_encoded_domain("ace", value)
                if key in ["changed"]:
                    infos.set_updated(value)
        return infos
    

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
                print("Parse error: Unrecognized line type")
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["Name Server"]:
                    infos.add_nameserver(value)
                if key in ["Status"]:
                    infos.set_status(value)
                if key in ["Updated Date"]:
                    infos.set_updated(value)
        return infos


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
                print("Parse error: Unrecognized line type")
                sys.exit(1)
            if linetype == 'header':
                break
            elif linetype == 'value':
                (key, value) = match.groups()
                if key in ["Name Server"]:
                    infos.add_nameserver(value)
                if key in ["Domain Status"]:
                    infos.set_status(value)
                if key in ["Updated On"]:
                    infos.set_updated(value)
        return infos


class WhoisEngine:

    """The whole beast with user API"""

    parser_list = {
        'whois.denic.de': DenicParser,
        'whois.crsnic.net': CrsnicParser,
        'whois.nic.name': NameParser,
        'whois.publicinterestregistry.net': NameParser,
        'whois.afilias.info': NameParser,
        }


    def __init__(self, rawdata = None):
        self.rawdata = rawdata
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
                except socket.error as xxx_todo_changeme:
                    (ecode, reason) = xxx_todo_changeme.args
                    if ecode in [115, 150]: pass
                    else:
                        raise socket.error(ecode, reason)
                ret = select.select([s],[s],[],30)
                if len(ret[1]) == 0 and len(ret[0]) == 0:
                    s.close()
                    raise TimedOut("on connect ")
                s.setblocking(1)
            except socket.error as xxx_todo_changeme1:
                (ecode, reason) = xxx_todo_changeme1.args
                print(ecode, reason)
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
            raise NoWhoisServerError(domain)
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
        infos = DomainInfos(domain)
        (server,page) = self.query_whois(domain)
        if self.rawdata:
            self.rawdata.write(page)
        # page = open("testdata","r").read()
        if page:
            if server in WhoisEngine.parser_list:
                cls = WhoisEngine.parser_list[server]
                parser = cls()
                return parser.parse(page,infos)
            else:
                raise UnhandledWhoisServer(server)
        else:
            raise ServerQueryError(server,domain)
