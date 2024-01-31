# Summary Statistics Assignment
### The following files read their respective file type and summarizes four different statistics within their files. This allows for an easier read of the basic components found within the file. 
### Included Files
1. `ml_csv_reader.py`
2. `ml_json_reader.py`
3. `ml_xml_reader.py`
4. `ml_yaml_reader.py`

### Running Instructions
In the command line type
1. `python3 ml_csv_reader.py Meteorite_Landings.csv` for the csv reader.
2. `python3 ml_json_reader.py Meteorite_Landings.json` for the json reader.
3. `python3 ml_xml_reader.py Meteorite_Landings.xml` for the xml reader.
4. `python3 ml_yaml_reader.py Meteorite_Landings.yaml` for the yaml reader.

### Sample Code
```
 for row in ml_data['meteorite_landings']:
        if(check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Northern & Eastern"):
            NE+=1
        elif(check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Northern & Western"):
            NW+=1
        elif(check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Southern & Eastern"):
            SE+=1
        elif(check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Southern & Western"):
            SW+=1
```
This code goes through the output of the check_hemisphere method and increments which hemisphere count it is in. In order to print the output, the following code will display the statistics.
```
    print("\n4. The amount of meteorite landings in the Northern & Eastern Hemisphere is", NE, "\n")
    print("The amount of meteorite landings in the Northern & Western Hemisphere is", NW, "\n")
    print("The amount of meteorite landings in the Southern & Eastern Hemisphere is", SE, "\n")
    print("The amount of meteorite landings in the Southern & Western Hemisphere is", SW, "\n")
```
