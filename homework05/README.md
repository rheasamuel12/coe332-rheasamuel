# The Darjeeling Flask
### The following files read through the ISS data set XML file using flask routes containerized in a Docker file and summarizes  different statistics within their files. This allows for an easier read of the basic components found within the file. 
### Included Files
1. `iss_tracker.py`

   This file reads includes four different functions:
   
   `print_data`: This function takes in the no parameters and returns the entire data set. If query parameters are inputted, then it returns a certain data range of the data set.
   
   `print_epoch`: This function takes in a string epoch through the flask route and returns its state vector.

   `inst_speed`: This function takes in a string epoch through the flask route and returns its speed.
   
   `closest_speed`: This function takes in no parameters and returns the speed of the state vector with the closest time to the current time.

2. `test_iss_tracker.py`

3. `Dockerfile`
   
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.
4. `diagram.png`

    This file includes the software diagram for homework05.

### Diagram
![diagram (1)](https://github.com/rheasamuel12/coe332-rheasamuel/assets/143050090/6a381570-09fd-4bc7-ac8a-60a7aef481cd)
This diagram displays the sequence diagram of the components found within the project. The main components found are the User, Jetstream VM, Docker Container, Flask, and Python files. In the diagram, the text explains how each component relate to one another.
### Building Instructions
To build the python scripts type

`docker build -t username/flask_iss_tracker:1.0 .`

Optionally, you can preface the tag with your Docker Hub username.

### Running/Building Instructions
Make sure you have docker installed before starting. We are mounting the data inside the container at runtime. In the command line type
`docker run --name "iss_tracker" -d -p 5000:5000 username/flask_iss_tracker:1.0`

To run each route:
1. `curl localhost:5000/epochs`

Returns the entire data set

2. `curl "localhost:5000/epochs?limit=int&offset=int"`

Returns modified list of Epochs given query parameters. Make sure to replace `int` with a integer value.

3. curl localhost:5000/epochs<epoch>

Returns state vectors for a specific Epoch from the data set

4. curl localhost:5000/epochs<epoch>/speed

Returns the speed for a specific Epoch from the data set


5. curl localhost:5000/now

Returns the state vectors and speed of the closest epoch to current time.

### Sample Code
```
 timestamp_data = data['ndm']['oem']['body']['segment']['data']['stateVector']
    logging.debug("Debug attempt, should be true: %s", timestamp_data != None) #Debugging logging
    for x in timestamp_data:
        if x['EPOCH'] == epoch:
            x_dot = float(x['X_DOT']['#text'])
            y_dot = float(x['Y_DOT']['#text'])
            z_dot = float(x['Z_DOT']['#text'])

            speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)

    return str(speed)
```
This code is from the inst_speed() function in the iss_tracker.py script. It uses the parameter epoch and finds it in the dictionary. Once found, it calculates its speed and returns the value.
### Sample Results
Using this route `curl localhost:5000/epochs/2024-074T12:00:00.000Z/speed`, the following output occurs.
`7.652274797752842`

To test another route, I could call `curl localhost:5000/epochs/2024-074T12:00:00.000Z`. The following output occurs:
```
{
  "EPOCH": "2024-074T12:00:00.000Z",
  "X": {
    "#text": "4361.0105068273897",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "2.25603844265299",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-392.52963816617802",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "7.1858437146965803",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-5202.6075373420399",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "1.35323694656583",
    "@units": "km/s"
  }
}
```
