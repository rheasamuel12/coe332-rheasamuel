import yaml
import argparse

# Compute average mass
def compute_average_mass(a_list_of_dicts, a_key_string):
    total_mass = 0.
    for i in range(len(a_list_of_dicts)):
        total_mass += float(a_list_of_dicts[i][a_key_string])
    return (total_mass / len(a_list_of_dicts))

# Check the hemisphere of each landing
def check_hemisphere(latitude: float, longitude: float) -> str:
    if latitude > 0:
        location = 'Northern'
    else:
        location = 'Southern'
    if longitude > 0:
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return location

# Count the amount of classes (Used ChatGPT to fix errors in this function)
def count_classes(a_list_of_dicts, a_key_string):
    classes_count = {}
    total_classes = 0
    for i in a_list_of_dicts:
        recclass = i.get(a_key_string)
        if recclass:
            total_classes += 1
            if recclass in classes_count:
                classes_count[recclass] += 1
            else:
                classes_count[recclass] = 1
    return total_classes, classes_count

# Summarize all the statistics found
def main():
    # Include argparse to accept filename as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='YAML file with meteorite_landing')
    args = parser.parse_args()
    data = {}
    with open(args.file, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    print("Summary Statistics:\n")
    # Count classes
    total_classes, classes_count = count_classes(data['meteorite_landings'], 'recclass')
    print("1.Amount of classes", total_classes)
    print("\n2.Number of different classes:")
    for recclass, count in classes_count.items():
        print(f"{recclass}: {count}")
    # Display the average mass of the meteorite landings:
    print("\n3.The average mass of the meteorite landings is", compute_average_mass(data['meteorite_landings'], 'mass (g)'), "g")

    # Display how many meteorite landings are in specific places
    NE = 0
    NW = 0
    SE = 0
    SW = 0
    for row in data['meteorite_landings']:
        if check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Northern & Eastern":
            NE += 1
        elif check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Northern & Western":
            NW += 1
        elif check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Southern & Eastern":
            SE += 1
        elif check_hemisphere(float(row['reclat']), float(row['reclong'])) == "Southern & Western":
            SW += 1
    print("4.The amount of meteorite landings in the Northern & Eastern Hemisphere is", NE, "\n")
    print("The amount of meteorite landings in the Northern & Western Hemisphere is", NW, "\n")
    print("The amount of meteorite landings in the Southern & Eastern Hemisphere is", SE, "\n")
    print("The amount of meteorite landings in the Southern & Western Hemisphere is", SW, "\n")

if __name__ == "__main__":
    main()

