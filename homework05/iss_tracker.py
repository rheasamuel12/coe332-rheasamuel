import requests
import math
import xmltodict
from flask import Flask, request
from datetime import datetime
import logging

#Used ChatGPT to fix errors and understand flask

app = Flask(__name__)

response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
data = xmltodict.parse(response.content)

@app.route('/epochs', methods=['GET'])
def print_data():
    """
    Prints a subset of state vector data based on provided limit and offset or prints the entire data set.
    Args:
        None (uses query parameters):
            limit (int): Maximum number of items to return
            offset (int): Index to start returning items from
    Returns:
        result (list of dicts): Set of state vector data
    """
    epochs_list = data['ndm']['oem']['body']['segment']['data']['stateVector']

    limit = request.args.get('limit', 0, type=int)
    offset = request.args.get('offset', 0, type=int)


    if limit != 0:
        try:
            limit = int(limit)
            offset = int(offset)
        except ValueError:
            return "Invalid input, must be integer"

        logging.debug("Debug attempt, should be true: %s", limit != None) 
        logging.debug("Debug attempt, should be true: %s", offset != None) 

        if (offset + limit) <= len(epochs_list):
            if offset == 0:
                result = epochs_list[offset:(offset + limit)]
            else:
                result = epochs_list[offset:((offset + limit)-1)]
            return result
        else:
            return "Invalid input, must be within data range"
    else:
        return epochs_list

@app.route('/epochs/<epoch>', methods=['GET'])
def print_epoch(epoch):
    """
    Prints the state vector data corresponding to a given epoch.
    Args:
        epoch (str): The epoch timestamp to retrieve data for
    Returns:
        x (dict): The state vector data for the given epoch
    """
    dataval = data['ndm']['oem']['body']['segment']['data']['stateVector']
    for x in dataval:
        if x['EPOCH'] == epoch:
            return x

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def inst_speed(epoch):
    """
    Calculates and returns the instantaneous speed for a given epoch.
    Args:
        epoch (str): The epoch timestamp to calculate speed for
    Returns:
        speed (float): The calculated instantaneous speed
    """
    timestamp_data = data['ndm']['oem']['body']['segment']['data']['stateVector']
    logging.debug("Debug attempt, should be true: %s", timestamp_data != None) #Debugging logging
    for x in timestamp_data:
        if x['EPOCH'] == epoch:
            x_dot = float(x['X_DOT']['#text'])
            y_dot = float(x['Y_DOT']['#text'])
            z_dot = float(x['Z_DOT']['#text'])

            speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)

    return str(speed)

@app.route('/now', methods=['GET'])
def closest_speed():
    """
    Calculates and returns the closest speed to the current time.
    Returns:
        speed (float): The calculated speed closest to the current time
    """

    timestamps = [datetime.strptime(i['EPOCH'], "%Y-%jT%H:%M:%S.%fZ") for i in data['ndm']['oem']['body']['segment']['data']['stateVector']]
    time_differences = [abs(x - datetime.now()) for x in timestamps]
    closest_index = time_differences.index(min(time_differences))

    closest_timestamp_data = data['ndm']['oem']['body']['segment']['data']['stateVector'][closest_index]
    logging.debug("Debug attempt, should be true: %s", closest_timestamp_data != None) #Debugging logging
    x_dot = float(closest_timestamp_data['X_DOT']['#text'])
    y_dot = float(closest_timestamp_data['Y_DOT']['#text'])
    z_dot = float(closest_timestamp_data['Z_DOT']['#text'])
    speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)

    return str(speed)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
