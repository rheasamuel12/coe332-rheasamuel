import math
def solve_gcd(lat_a, lon_a, lat_b, lon_b):
    lat_a = lat_a*(math.pi/180)
    lat_b = lat_b*(math.pi/180)
    lon_a = lon_a*(math.pi/180)
    lon_b = lon_b*(math.pi/180)
    #d = 6371 * math.acos(math.cos(lat_a)*math.cos(lat_b)*math.cos(lon_a-lon_b)+(math.sin(lat_a)*math.sin(lat_b)))
    val= max(-1, min(1, math.cos(lat_a) * math.cos(lat_b) * math.cos(lon_a - lon_b) + (math.sin(lat_a) * math.sin(lat_b))))
    d = 6371 * math.acos(val)
    return d
