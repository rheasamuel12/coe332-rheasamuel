import csv
import argparse
from gcd_algorithm import solve_gcd
from typing import List
import logging
import socket

#Used ChatGPT to fix some error problems 
 
def most_common_class(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Iterates through a list of dictionaries, pulling out values associated with the key given. Returns the most common class and count associated with it.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        most_class (string): String of the most common class
        count (int): Int representing how many meteorites land in these two hemispheres
"""
    classes_count = {} #List containing classes found
    most_class = None
    count = 0
    for i in a_list_of_dicts: 
        #Looping through a list of dictionaries and finding if the class is already in classes_count, if not, it is added.
        # If it is, it is incremented
        recclass = i.get(a_key_string) 
        if recclass in classes_count:
            classes_count[recclass] += 1
        else:
            classes_count[recclass] = 1

        if classes_count[recclass] > count: 
            most_class = recclass
            count = classes_count[recclass] #Highest increment is set to count

    logging.debug("Debug attempt, should be true: %s", count != 0) #Debugging logging, cannot = 0
    return most_class, count


def most_common_location(a_list_of_dicts: List[dict], a_key_string_a: str, a_key_string_b: str) -> float:
    """
 Iterates through a list of dictionaries, pulling out values associated with the key given. Returns the most common location(hemisphere) and count associated with it.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).
    Returns:
        most_common (string): Short string listing the two most common hemispheres.
        count (int): Int representing how many meteorites land in these two hemispheres
    """
    location_list = {} #Empty list to add the hemispheres found
    most_common = None
    count = 0

    for entry in a_list_of_dicts: #Loop through dictionary and find hemispheres
        lat_str = entry.get(a_key_string_a)
        lon_str = entry.get(a_key_string_b)
        try:
            lat = float(lat_str)
            lon = float(lon_str)
        except ValueError:
            logging.warning(f'Invalid latitude or longitude: {lat_str}, {lon_str}')
            continue
        location = 'Northern' if (lat > 0) else 'Southern'
        location = f'{location} & Eastern' if (lon > 0) else f'{location} & Western'

        if location in location_list:
            location_list[location] += 1
        else:
            location_list[location] = 1

        if location_list[location] > count: #Highest increment is set to count
            most_common = location
            count = location_list[location]

    logging.debug("Debug attempt, should be true: %s", count != 0) #Debugging logging, cannot = 0
    return most_common, count

def heaviest_meteorite(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Iterates through a list of dictionaries, pulling out values associated with the key given. Returns the heaviest meteorite and its mass

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        name (string) : string representing the name of the heaviest meteorite
        mass (float): float representing the heaviest meteorite 
"""
    mass = 0
    orig_mass = 0
    name = None

    for item in a_list_of_dicts: #Loops through dictionary list
        orig_mass_str = item.get(a_key_string)
        try:
            orig_mass = float(orig_mass_str)
            if orig_mass > mass: #Gets heaviest mass
                name = item.get('name') 
                mass = orig_mass
        except ValueError:
            logging.warning(f'Invalid latitude or longitude: {orig_mass_str}')
            continue

    logging.debug("Debug attempt, should be true: %s", mass != 0) #Debugging logging, cannot = 0
    return name, mass

def avg_distance_between_landings(a_list_of_dicts: List[dict], a_key_string_lat: str, a_key_string_lon: str) -> float:
    """
    Iterates through a list of dictionaries, pulling out values associated with the key given. Returns the average distance between meteorites.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        avg_distance (float): float representing the average distance between meteorites 
"""
    avg_distance = 0
    #Have to find the values of the current latitude and longitude values and meteorite in front of it as well
    for i in range(len(a_list_of_dicts) - 1):
        lat_a = a_list_of_dicts[i].get(a_key_string_lat)
        lon_a = a_list_of_dicts[i].get(a_key_string_lon)
        lat_b = a_list_of_dicts[i + 1].get(a_key_string_lat) 
        lon_b = a_list_of_dicts[i + 1].get(a_key_string_lon)
        try:
            lat_a = float(lat_a)
            lon_a = float(lon_a)
            lat_b = float(lat_b)
            lon_b = float(lon_b)
            #Finds avg distance using solve_gcd method
            avg_distance += solve_gcd(lat_a, lon_a, lat_b, lon_b)
        except ValueError:
            logging.warning(f'Invalid latitude or longitude: {lat_a}, {lon_a},{lat_b},{lon_b}')
            continue
        
    # Calculate the average distance
    logging.debug("\nDebug attempt, should be true: %s", avg_distance != 0) #Debugging logging, cannot = 0
    avg_distance /= (len(a_list_of_dicts) - 1)
    return avg_distance 

def main():
    #Include argparse for logging and file input
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', type=str, required=False,default='ERROR',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
    parser.add_argument('file', help='CSV file with meteorite_landing')
    args = parser.parse_args()

    format_str = '[%(asctime)s {0}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'.format(socket.gethostname())
    logging.basicConfig(level=args.loglevel, format=format_str)

    data = {}
    data['meteorite_landings'] = []

    with open(args.file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['meteorite_landings'].append(dict(row))


    #logging.warning("Message: Should print four outputs (COMMON CLASS, COMMON LOCATION, HEAVIEST METEORITE, AVG DISTANCE)")
    print("Summmary Statistics: ")
    print("\nThe most common class is: " , most_common_class(data['meteorite_landings'], 'recclass'))
    print("\nThe most common location is: ", most_common_location(data['meteorite_landings'], 'reclat', 'reclong'))
    print("\nThe heaviest meteorite is: ", heaviest_meteorite(data['meteorite_landings'], 'mass (g)'))
    print("\nThe average distance between landings is: ", avg_distance_between_landings(data['meteorite_landings'], 'reclat', 'reclong'))
    
  
if __name__ == '__main__':
    main()
                     