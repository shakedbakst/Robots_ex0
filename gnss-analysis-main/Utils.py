import math
import csv
import numpy as np
from scipy.optimize import minimize


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

    print(lat, "    ", lon , "    ", alt)
    return lat, lon, alt


def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def filter_satellite_data(data, gps_time):
    filtered_data = []
    for row in data:
        if (row["GPS time"]) == gps_time:
            filtered_data.append(row)

    return filtered_data


def rms_error(position, data):
    # Position: [X, Y, Z]
    # Data: [{SatPRN, GPS time, Sat.X, Sat.Y, Sat.Z, Pseudo-Range, CN0}]
    sum_squared_errors = 0.0
    for satellite in data:
        x_diff = float(satellite['Sat.X']) - position[0]
        y_diff = float(satellite['Sat.Y']) - position[1]
        z_diff = float(satellite['Sat.Z']) - position[2]
        predicted_range = np.sqrt(x_diff ** 2 + y_diff ** 2 + z_diff ** 2)
        measured_range = float(satellite['Pseudo-Range'])
        sum_squared_errors += (predicted_range - measured_range) ** 2
    return np.sqrt(sum_squared_errors / len(data))


def positioning_algorithm(data):
    # Use the centroid of satellite positions as initial guess
    initial_guess = np.mean([[float(sat['Sat.X']), float(sat['Sat.Y']), float(sat['Sat.Z'])] for sat in data], axis=0)
    result = minimize(rms_error, initial_guess, args=(data,), method='trust-constr')
    if result.success:
        return result.x  # Return the optimized X, Y, Z coordinates
    else:
        raise ValueError("Optimization failed")


def calculate_positioning(file_path, gps_time):
    data = read_csv_file(file_path)
    filtered_data = filter_satellite_data(data, gps_time)
    position = positioning_algorithm(filtered_data)
    print("Computed position (X, Y, Z):", position)
    return position