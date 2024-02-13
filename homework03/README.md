# The Royal Containers Assignment
### The following files read through the Meteorite_Landings file using Docker and summarizes four different statistics within their files. This allows for an easier read of the basic components found within the file. 
### Included Files
1. `ml_data_reader.py`

   This file reads includes four different functions:
   
   `most_common_class`: This function takes in the parameters (a_list_of_dicts: List[dict], a_key_string: str) and returns the most common class found within the Meteorite Landing csv file. 

   `most_common_location`: This function takes in the parameters (a_list_of_dicts: List[dict], a_key_string_a: str, a_key_string_b: str) and returns the most common location found within the Meteorite Landing csv file.

   `heaviest_meteorite`: This function takes in the parameters (a_list_of_dicts: List[dict], a_key_string: str) and returns the heaviest meteorite  found within the Meteorite Landing csv file.
   
   `avg_distance_between_landings`: This function takes in the parameters (a_list_of_dicts: List[dict], a_key_string_lat: str, a_key_string_lon: str) and returns the average distance between landings found within the Meteorite Landing csv file. 

2. `test_ml_data_reader.py`

   This file includes four different testing functions which test their respective functions:
   
   `test_most_common_class` 

   `test_most_common_location`

   `test_heaviest_meteorite`
   
   `test_avg_distance_between_landings` 

3. `gcd_algorithm.py`

   This file contains one function `solve_gcd` which creates the great circle distance algorithm.
4.  `test_gcd_algorithm.py`

    This file tests the algorithm `solve_gcd`
5. `Dockerfile`
   
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.
6. `diagram.png`

   This software diagram represents a sequence diagram of the components found within this project.
### Building Instructions
To build the python scripts type

`docker build -t username/ml_data_reader:1.0 .`

Optionally, you can preface the tag with your Docker Hub username.
### Download Instruction
To find the input data, go to `https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data` , click `Export`, and then download as a `CSV file`.

### Running/Building Instructions
Make sure you have docker installed before starting. We are mounting the data inside the container at runtime. Additionally, make sure your `Meteorite_Landings_20240130.csv` file is located in the same path as your other python scripts. In the command line type
1. `docker run --rm -v $PWD/Meteorite_Landings_20240130.csv:/data/Meteorite_Landings_20240130.csv rheasamuel/ml_data_reader:1.0  ml_data_reader.py /data/Meteorite_Landings_20240130.csv`

    If you would like to run the pytest for ml_data_reader.py type
2. `docker run --rm -v $PWD:/Meteorite_Landings_2024013.csv rheasamuel/ml_data_reader:1.0 pytest /code/test_ml_data_reader.py`

    If you would like to run the pytest for gcd_algorithm.py type
3. `docker run --rm -v $PWD:/Meteorite_Landings_2024013.csv rheasamuel/ml_data_reader:1.0 pytest /code/test_gcd_algorithm.py`

### Sample Code
```
  for item in a_list_of_dicts: 
        orig_mass_str = item.get(a_key_string)
        try:
            orig_mass = float(orig_mass_str)
            if orig_mass > mass: #Gets heaviest mass
                name = item.get('name') 
                mass = orig_mass
        except ValueError:
            logging.warning(f'Invalid latitude or longitude: {orig_mass_str}')
            continue
```
This code loops through the dictionary and finds the mass for each item. In order to make sure the value can be converted into a float, we use the try and except method. This will return a warning if it is not a valid value.

### Sample Results
The results of the code should look like:
```
Summmary Statistics: 

The most common class is:  ('L6', 8285)

The most common location is:  ('Southern & Eastern', 21814)

The heaviest meteorite is:  ('Hoba', 60000000.0)

The average distance between landings is:  496.64961308568815
```
Again, this shows:

  1. The most common class and how many classes of this type exist.
  
  2. The most common location and how many meteorites land in this location.
  
  3. The heaviest meteorite name and its mass.
  
  4. The average distance between landings.
