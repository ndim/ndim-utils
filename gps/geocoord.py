#!/usr/bin/python
#
# Disclaimers:
# No, I've got *no* idea about geodetic matters.
# I have *no* idea what values this program outputs.
# The formulas look beautifully complicated, but I don't understand
# them at all.
#
# References:
# [1]  ftp://164.214.2.65/pub/gig/tm8358.2/TM8358_2.pdf
# [2]  http://earth-info.nga.mil/GandG/tm83581/tr83581b.htm
# [3]  http://www.ign.fr/affiche_rubrique.asp?rbr_id=1093&lng_id=FR
# [4a] http://www.posc.org/Epicentre.2_2/DataModel/ExamplesofUsage/eu_cs34.html
# [4b] http://www.posc.org/Epicentre.2_2/DataModel/ExamplesofUsage/eu_cs34c.html
# [5]  http://www.gpsy.com/gpsinfo/geotoutm/gantz/LatLong-UTMconversion.cpp
# [6]  http://www.gmat.unsw.edu.au/snap/gps/gps_survey/chap2/214.htm
# [7]  http://www.wgs84.com/files/wgsman24.pdf
# [8]  http://www.icc.es/geotex/manuals/gpscat.html
# [9]  http://www.hydro.nl/articles/artikel2_en.htm


from math import pi, sin, cos, tan, sqrt


class UnhandledCoordinate(Exception):

    def __init__(self,coord):
        self.coord = coord

    def __str__(self):
        return "Unhandled coordinate: %s" % (self.coord)


class ResultOutOfBounds(Exception):

    def __init__(self, name, value, lower, upper):
        self.name = name
        self.value = value
        self.lower = lower
        self.upper = upper

    def __str__(self):
        return("Calculated result for \"%s\" %s out of bounds (%s .. %s)"
               % (self.name, str(self.value),
                  str(self.lower), str(self.upper)))


class Ellipsoid:

    def __init__(self, a, f1):
        self.a = a
        self.f1 = f1


default_datum = "WGS84"


ellipsoids = {
    # WGS84 according to [6]
    "WGS84": Ellipsoid(6378137.0, 298.257223563),
    # [3] calls this ED50
    # [1] calls this "International" [Section 2-11]
    # [8] says UTM uses ED50
    # [9] says ED50 is "European Datum", often used for North Sea.
    # WTF?
    "ED50": Ellipsoid(6378388.0, f1 = 297.0),
    }


zone_latitudes = (-80,-72,-64,-56,-48,-40,-32,-24,-16,-8,0,8,16,24,32,40,48,56,64,72,84)
zone_letters = ('C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X')
lettermap = {}
for i in range(len(zone_letters)):
    letter  = zone_letters[i]
    min_deg = zone_latitudes[i]
    max_deg = zone_latitudes[i+1]
    zone = 0
    if min_deg < 0:
        zone = 1
    tup = (min_deg, max_deg, zone)
    lettermap[letter] = tup


k0 = 0.9996


def latlon_to_utm(lat, lon, ellipsoid = ellipsoids[default_datum]):
    """Convert latitude/longitude in given datum to UTM coordinates

    Using formulas from
    http://www.posc.org/Epicentre.2_2/DataModel/ExamplesofUsage/eu_cs34h.html

    FIXME: Southern equator, special case zones (Svalbard)
    """
    
    phi = pi/180 * lat
    lambd = pi/180 * lon

    lat0 = 0
    phi0 = pi/180 * lat0
    lon0 = 9
    lambd0 = pi/180 * lon0

    zone_number = 1+int(lon+180)/6
    zone_letter = '?'
    for zone_letter in lettermap.keys():
        if (lettermap[zone_letter][0] <= lat)and(lettermap[zone_letter][1] >= lat):
            break
    else:
        zone_letter = '!'
    zone = "%d%s" % (zone_number,zone_letter)
    
    a = ellipsoid.a
    f1 = ellipsoid.f1

    f = 1/f1
    b = a*(f1-1)/f1
    e2 = f*(2-f)
    e1 = (1-sqrt(1-e2))/(1+sqrt(1-e2))
    ep2 = e2/(1-f)**2
    
    FE = 500000.0
    FN = 0.0
        
    T = tan(phi)
    C = ep2 * cos(phi)**2
    A = (lambd - lambd0) * cos(phi)
    def MM(phi):
        return(a * ( (1 - e2/4 - 3*e2**2/64 - 5*e2**3/256)*phi
                     - (3*e2/8 + 3*e2**2/32 + 45*e2**3/1024)*sin(2*phi)
                     + (15*e2**2/256 + 45*e2**3/1024)*sin(4*phi)
                     - (35*e2**3/3072)*sin(6*phi)))
    M0 = MM(phi0)
    M = MM(phi)
    nu = a/sqrt(1-e2*sin(phi)**2)
    
    E = FE + k0 * nu * (A
                        + (1-T+C)*A**3/6
                        + (5-18*T+T**2+72*C-58*ep2)*A**5/120
                        )
    
    N = FN + k0 * ( M - M0
                    + nu * tan(phi) * ( A**2/2
                                        + (5-T+9*C+4*C**2)*A**4/24
                                        + (61-58*T+T**2+600*C-330*ep2)*A**6/720
                                        )
                    )

    # #########
    #print "Variables:"
    #vs = vars()
    #ks = vs.keys()
    #ks.sort()
    #for k in ks:
    #    v = vs[k]
    #    print "    %-20s %s" % (k,v)

    return "%s %d %d" % (zone,E,N)

    
def utm_to_latlon(zone, E, N, ellipsoid = ellipsoids[default_datum]):
    """Convert UTM coordinates to latitude/longitude in given datum

    Using formulas from
    http://www.posc.org/Epicentre.2_2/DataModel/ExamplesofUsage/eu_cs34h.html

    Zone: Grid Zone Designation [2]
    E: Easting
    N: Northing
    """
    
    E = float(E)
    N = float(N)
    
    zone_letter = zone[-1:]
    FN = 0
    lm = lettermap[zone_letter]
    if lm[2] == 1:
        # southern hemisphere, UTM
        FN = 100000000
    elif lm[2] == 0:
        # northern hemisphere, UTM
        FN = 0
    else:
        # May be UPS instead of UTM
        raise UnhandledCoordinate("%s %s %s" % (zone, E, N))

    zone_number = int(zone[:-1])
    assert(1<=zone_number and zone_number<=60)
    assert(0<=E and E<=1000000)
    assert(0<=N and N<=15000000)

    a = ellipsoid.a
    f1 = ellipsoid.f1

    f = 1/f1
    b = a*(f1-1)/f1
    e2 = f*(2-f)
    e1 = (1-sqrt(1-e2))/(1+sqrt(1-e2))
    ep2 = e2/(1-f)**2
    
    FE = 500000.0
        
    orig_meridian = -180 + 6 * zone_number - 3
    
    M1 = (N - FN) / k0
    mu1 = M1 / (a*(1-e2/4-3*e2**2/64-5*e2**3/256))

    phi1 = (mu1
            + (3*e1/2 - 27*e1**3/32) * sin(2*mu1)
            + (21*e1**2/16 - 55*e1**4/32) * sin(4*mu1)
            + (151*e1**3/96) * sin(6*mu1)
            + (1097*e1**4/512) * sin(8*mu1)
            )
    nu1 = a/sqrt(1-e2*sin(phi1)**2)
    D = (E - FE) / (nu1 * k0)
    T1 = tan(phi1) ** 2
    C1 = ep2 * cos(phi1) ** 2
    lamb = (D
            - (1+2*T1+C1)*D**3/6
            + (5-2*C1+28*T1-3*C1**2+8*ep2+24*T1**2)*D**5/120
            ) / cos(phi1)

    rho1 = a * (1-e2) / sqrt(1-e2*sin(phi1)**2)**3
    phi = phi1 - ( (nu1 * tan(phi1) / rho1) *
                   (D**2/2
                    - (5+3*T1+10*C1-4*C1**2-9*ep2)*D**4/24
                    + (61+90*T1+298*C1+45*T1**2-252*ep2-3*C1**2)*D**6/720)
                   )

    longitude = orig_meridian + lamb * 180.0 / pi
    latitude = phi * 180.0 / pi
    
    if not(lm[0] <= latitude and lm[1] >= latitude):
        raise ResultOutOfBounds("latitude", latitude, lm[0], lm[1])

    # #########
    #print "Variables:"
    #vs = vars()
    #ks = vs.keys()
    #ks.sort()
    #for k in ks:
    #    v = vs[k]
    #    print "    %-20s %s" % (k,v)

    return (latitude,longitude)


def utmsplit(utm):
    tokens = utm.split()
    (zone, easting, northing) = (tokens[0],
                                 int(tokens[1]), int(tokens[2]))
    return(zone,easting,northing)


def testcases():
    tcs = (
        ("32U 491620 5400390",48.75647,8.88598),
        ("32U 493421 5396303",48.71972,8.91056),
        ("00Y 20000000 20000000", 90.0, 0),
        )
    for (utm,lat,lon) in tcs:
        (z,e,n) = utmsplit(utm)
        print
        print "Test case:"
        print "  UTM coordinates:", utm
        u = utm_to_latlon(z,e,n)
        print "Results:"
        print "  WGS84 lat/lon:  ", u
        print "  should be WGS84:", (lat,lon)
        print "  error:          ", (u[0]-lat, u[1]-lon)
        r = latlon_to_utm(lat,lon)
        print "Reverse:"
        print "  UTM:            ", r
        print "  Should be:      ", utm
        (rz,re,rn) = utmsplit(r)
        print "  Error:          ", int(e)-int(re), int(n)-int(rn)
        print


if __name__ == '__main__':
    testcases()

# arch-tag: ebe60519-7c4f-46aa-924b-64ba89123cd5
