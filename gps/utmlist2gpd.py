#!/usr/bin/python


import sys

from geocoord import utm_to_latlon


def writemap(f,m):
    keys = m.keys()
    for i in range(len(keys)):
        k = keys[i]
        v = m[k]
        s = str(v)
        if type(v) == float:
            s = "%1.5f" % v
        f.write("%s=\"%s\"" % (str(k), s))
        if i < len(keys)-1:
            f.write(" ")
    f.write("\n")


def convert(input, output, cleaned = None):
    """Read list of UTM coordinates, and write route file for gpspoint."""
    east = ''
    north = ''
    square = ''
    writemap(output,{"type": "route", "routename":"POP-Z61" })
    common_attrs = {
        "type": "routepoint",
        "symbol": "flag",
        "display_options": "symbol+name",
        }
    if cleaned:
        cleaned.write("%5s %3s %9s %9s\n" % ("#name", "squ", "easting", "northing"))
    while True:
        line = input.readline()
        if not line:
            break
        tokens = line.split()
        if line[0] not in ('0','1','2','3','4','5','6','7','8','9'):
            continue
        i = tokens[0] # identifier
        e = tokens[1] # easting (possibly shortened)
        n = tokens[2] # northing (possibly shortened)
        if len(tokens) > 3:
            square = tokens[3] # UTM zone (optional)
        ident = 'PZ%03d' % int(i)
        el = len(e)
        nl = len(n)
        east = east[0:-el] + e
        north = north[0:-nl] + n
        if cleaned:
            cleaned.write("%5s %3s %9s %9s\n" % (ident, square, east, north))

        attrs = common_attrs
        attrs["name"] = ident
        latlon = utm_to_latlon(square, float(east), float(north))
        attrs["latitude"] = latlon[0]
        attrs["longitude"] = latlon[1]
        # output.write("%3s %s %s %7s %7s\n" % (ident, square[0:2], square[2], east, north))
        writemap(output,attrs)
    writemap(output,{"type": "routeend"})


if __name__ == '__main__':
    file_in  = sys.stdin
    file_out = sys.stdout
    file_cln = None
    if len(sys.argv) > 1:
        file_in  = open(sys.argv[1],"r")
    if len(sys.argv) > 2:
        file_out = open(sys.argv[2],"w")
    if len(sys.argv) > 3:
        file_cln = open(sys.argv[3],"w")
    convert(file_in, file_out, file_cln)

# arch-tag: 6e85afa6-8eb0-4149-be1f-1ab2c4e6068d
