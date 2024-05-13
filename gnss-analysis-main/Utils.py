import math


# 1. Calculate the distance 'r' from the origin (0,0,0) to the point (X,Y,Z) using r = sqrt(X^2 + Y^2 + Z^2).
# 2. Calculate the latitude as Lat = asin(Z/r) (in radians).
# 3. Calculate the longitude as Lon = atan2(Y,X) (in radians).
# 4. Finally, the altitude Alt would simply be the distance 'r' minus the radius of the Earth.

def xyz_to_lat_lon_alt(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)  # distance
    lat = math.asin(z / r)  # latitude
    lon = math.atan2(y, x)  # longitude

    earth_radius = 6371  # Radius of the Earth in kilometers
    alt = r - earth_radius

    # Convert angles from radians to degrees
    lat = math.degrees(lat)
    lon = math.degrees(lon)

    # print(lat, "    ", lon , "    ", alt)
    return lat, lon, alt
