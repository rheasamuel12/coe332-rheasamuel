# The ISS Aquatic
### The following files read through the ISS data set XML file using Docker and the requests library and summarizes four different statistics within their files. This allows for an easier read of the basic components found within the file. 
### Included Files
1. `iss_tracker.py`

   This file reads includes four different functions:
   
   `print_data`: This function takes in the parameters (dictionary, key_string_1, key_string_2) and returns the first and last epoch found within the ISS xml file.
   
   `closest_time`: This function takes in the parameters (dictionary, key_string) and returns the state vector with the closest time to the current time.

   `avg_speed`: This function takes in the parameters (dictionary, key_string) and returns the average speed of the state vectors.
   
   `closest_speed`: This function takes in the parameters (dictionary, key_string) and returns the speed of the state vector with the closest time to the current time.

2. `test_iss_tracker.py`

   This file includes four different testing functions which test their respective functions:
   
   `test_print_data` 

   `test_closest_time`

   `test_avg_speed`
   
   `test_closest_speed` 
3. `Dockerfile`
   
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.

### Building Instructions
To build the python scripts type

`docker build -t username/iss_tracker:1.0 .`

Optionally, you can preface the tag with your Docker Hub username.

### Running/Building Instructions
Make sure you have docker installed before starting. We are mounting the data inside the container at runtime. In the command line type
1. `docker run --rm \
           -v $(pwd):/app \
           rheasamuel/iss_tracker:1.0 \
           iss_tracker.py`

    If you would like to run the pytest for ml_data_reader.py type
2. `docker run --rm -v $(pwd):/app rheasamuel/iss_tracker:1.0 pytest /code/test_iss_tracker.py`

    If you would like to display the DEBUG messages
   
3.`docker run --rm \
           -v $(pwd):/app \
           rheasamuel/iss_tracker:1.0 \
           iss_tracker.py debug`
### Sample Code
```
  s = closest_time(dictionary,key_string)
    x_dot = float(s['X_DOT']['#text'])
    y_dot = float(s['Y_DOT']['#text'])
    z_dot = float(s['Z_DOT']['#text'])
    speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
```
This code is from the closest_speed() function in the iss_tracker.py script. It calls on the closest_time() function to find the state vector with the time closest to the current time. Then it uses that to find the velocities and thus speed.
### Sample Results
```
WARNING:root:4 outputs should occur:
ERROR:root:False

DATA RANGE
The data ranges from February 16, 2024 12:00:00 to February 16, 2024 12:00:00

AVG SPEED
The average speed is:  7.6589224391625175
2024-02-20 01:17:12.874559

CLOSEST TIME
The closest timestamp is 01:18:00
The epoch is 2024-051T01:18:00.000Z
The closest state vector's location is: -1672.38219598964 in the x direction -4092.2556036535502  in the y direction and -1672.38219598964 in the z direction
The closest state vector's veloicty is: 7.4271553034268702 in the x direction -1.13910494000824  in the y direction and 7.4271553034268702 in the z direction

CLOSEST SPEED
Speed closest to time now 7.663013869823896
```
Again, this shows:

  1. The data range of the state vectors.
  
  2. The average speed of the state vectors.
  
  3. The state vector with the closest time to the current time.
  
  4. The speed of the state vector with the closest time to the current time.
