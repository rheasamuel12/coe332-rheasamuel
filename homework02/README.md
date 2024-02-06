# Rushmeteorite Assignment
### The following files read through the Meteorite_Landings file and summarizes four different statistics within their files. This allows for an easier read of the basic components found within the file. 
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

### Running Instructions
In the command line type
1. `python3 .\ml_data_analysis.py .\Meteorite_Landings_20240130.csv`

    If you would like to display ERROR messages type
2. `python3 .\ml_data_analysis.py -l ERROR .\Meteorite_Landings_20240130.csv`

    If you would like to display DEBUG messages type
3. `python3 .\ml_data_analysis.py -l DEBUG .\Meteorite_Landings_20240130.csv`

    If you would like to display WARNING messages type
4. `python3 .\ml_data_analysis.py -l WARNING .\Meteorite_Landings_20240130.csv`

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
