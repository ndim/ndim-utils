#!/usr/bin/python
# *G*armin *U*TM tool by *N*dim.


import sys
import os
import os.path


sys.path = [ "/home/uli/src/gps/pygarmin-0.7" ] + sys.path
from geocoord import utm_to_latlon
import garmin
garmin.debug = 2


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


def read_waypoints(input,prefix=""):
    """Read list of UTM coordinates, and create list of waypoints."""
    wps = []
    east = ''
    north = ''
    square = ''
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
        ident = '%s%03d' % (prefix,int(i))
        el = len(e)
        nl = len(n)
        east = east[0:-el] + e
        north = north[0:-nl] + n
        latlon = utm_to_latlon(square, float(east), float(north))
        wps.append(garmin.Waypoint(ident,
                                   garmin.semi(latlon[0]),
                                   garmin.semi(latlon[1])))
    return wps


config = None
phys = None
gps = None
waypoints = None
wpd = None


if __name__ == '__main__':
    
    config = {}
    config["port"] = "/dev/ttyS0"
    
    print "Configuration:"
    for k,v in config.iteritems():
        print "   ", k, v
        
    print "Connecting to device..."
    phys = garmin.UnixSerialLink(config["port"])
    gps = garmin.Garmin(phys)
    print "Connection established."
    
    print "GPS Product ID:   %i" % gps.prod_id
    print "Descriptions:     %s" % gps.prod_descs
    print "Software version: %2.2f" % gps.soft_ver
    
    waypoints = gps.getWaypoints()
    
    wpd = {}
    for w in waypoints:
        wpd[w.ident] = w
        # Print the waypoints
        #    print w.ident,
        #    lat = garmin.degrees(w.slat)
        #    lon = garmin.degrees(w.slon)
        #    print lat, lon, w.cmnt

# arch-tag: 5224bef2-45ec-4a52-bb90-57b6ff7dd2f4
