#!/usr/bin/env python3
import requests
import math
import sys
import xmltodict
from typing import List
import logging
from datetime import datetime, timezone
#Used ChatGPT to figure out datetime and fix errors

def print_data(dictionary, key_string_1, key_string_2):
    """
    Prints first epoch and last epoch range.
    Args:
        dictionary (list): A list of dictionaries

        key_string_1 (string): A key that appears in each dictionary associated
                               with the desired value
        key_string_1 (string): A key that appears in each dictionary associated
                               with the desired value
    Returns:
        formatted_date, formatted_date_2 (string): string representing first epoch and last epoch
    """
    dt_object = datetime.strptime(dictionary[key_string_1], "%Y-%jT%H:%M:%S.%fZ")
    formatted_date = dt_object.strftime("%B %d, %Y %H:%M:%S")
    dt_object2 = datetime.strptime(dictionary[key_string_2], "%Y-%jT%H:%M:%S.%fZ")
    formatted_date_2 = dt_object.strftime("%B %d, %Y %H:%M:%S")

    
    logging.debug("Debug attempt, should be true: %s", formatted_date != None) #Debugging logging
    logging.debug("Debug attempt, should be true: %s", formatted_date != None) #Debugging logging
    

    print("\nDATA RANGE")
    print("The data ranges from",  formatted_date, "to", formatted_date_2)
    return formatted_date, formatted_date_2


def closest_time(dictionary, key_string):
    """
    Prints state vector with closest time to current time.
    Args:
        dictionary (list): A list of dictionaries

        key_string (string): A key that appears in each dictionary associated
                               with the desired value
    Returns:
         closest_timestamp_data (dict): dictionary element of the closest timestamp data to the current time
"""


    print(datetime.now())
    timestamps = [datetime.strptime(i['EPOCH'], "%Y-%jT%H:%M:%S.%fZ") for i in dictionary[key_string]]
    time_differences = [abs(x - datetime.now()) for x in timestamps]
    closest_index = time_differences.index(min(time_differences))
    closest_timestamp_data = dictionary[key_string][closest_index]
    formatted_closest_time = timestamps[closest_index].strftime("%H:%M:%S")


    logging.debug("Debug attempt, should be true: %s", closest_timestamp_data != None) #Debugging logging
    

    print("\nCLOSEST TIME")
    print("The closest timestamp is", formatted_closest_time)
    print("The epoch is", closest_timestamp_data['EPOCH'])
    print("The closest state vector's location is:",  closest_timestamp_data['X']['#text'], "in the x direction" , closest_timestamp_data['Y']['#text'], " in the y direction and", closest_timestamp_data['X']['#text'], "in the z direction")
    print("The closest state vector's veloicty is:", closest_timestamp_data['X_DOT']['#text'], "in the x direction" , closest_timestamp_data['Y_DOT']['#text'], " in the y direction and", closest_timestamp_data['X_DOT']['#text'], "in the z direction")
    return closest_timestamp_data

def avg_speed(dictionary,key_string):
    """
    Prints average speed of the state vectors.
    Args:
        dictionary (list): A list of dictionaries

        key_string (string): A key that appears in each dictionary associated
                               with the desired value
    Returns:
         avgspeed (float): float with average speed of the state vectors
    """

    speed = 0
    total = 0
    
    for x in dictionary[key_string]:
        x_dot = float(x['X_DOT']['#text'])  
        y_dot = float(x['Y_DOT']['#text'])  
        z_dot = float(x['Z_DOT']['#text'])  
        
        speed += math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
        total += 1
    
    logging.debug("Debug attempt, should be true: %s", x_dot != 0) #Debugging logging, cannot = 0
    logging.debug("Debug attempt, should be true: %s", y_dot != 0) #Debugging logging, cannot = 0
    logging.debug("Debug attempt, should be true: %s", z_dot != 0) #Debugging logging, cannot = 0
    
    print("\nAVG SPEED")
    print("The average speed is: ", speed/total) 
    return speed / total

def closest_speed(dictionary,key_string):
    """
    Prints the speed of a state vector closest to the current time 
    Args:
        dictionary (list): A list of dictionaries

        key_string (string): A key that appears in each dictionary associated
                               with the desired value
    Returns:
        speed (float): The speed of the state vector closest to current time
    """
    s = closest_time(dictionary,key_string)
    x_dot = float(s['X_DOT']['#text'])  
    y_dot = float(s['Y_DOT']['#text'])  
    z_dot = float(s['Z_DOT']['#text'])
    speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)


    logging.debug("Debug attempt, should be true: %s", x_dot != 0) #Debugging logging, cannot = 0
    logging.debug("Debug attempt, should be true: %s", y_dot != 0) #Debugging logging, cannot = 0
    logging.debug("Debug attempt, should be true: %s", z_dot != 0) #Debugging logging, cannot = 0
    
    logging.error(speed == 0)
    print("\nCLOSEST SPEED")
    print("Speed closest to time now", speed)
    return speed



def main():
    logging.warning("4 outputs should occur:")
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    data = xmltodict.parse(response.content)

    #Used ChatGPT to figure out how to input logging level in command line
    if len(sys.argv) > 1:
        log_level = sys.argv[1]
    else:
        log_level = 'none'
    if log_level == 'debug':
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    elif log_level == 'warning':
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
    print_data(data['ndm']['oem']['body']['segment']['metadata'], 'START_TIME', 'STOP_TIME')
    avg_speed(data['ndm']['oem']['body']['segment']['data'], 'stateVector')
    closest_speed(data['ndm']['oem']['body']['segment']['data'], 'stateVector')

if __name__ == "__main__":
    main()
