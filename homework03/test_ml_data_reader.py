from ml_data_reader import most_common_class, most_common_location, heaviest_meteorite, avg_distance_between_landings
from gcd_algorithm import solve_gcd
import pytest
def test_most_common_class():
    data = [
        {'recclass': 'A'},
        {'recclass': 'B'},
        {'recclass': 'A'},
        {'recclass': 'C'},
        {'recclass': 'B'}
    ]
    result = most_common_class(data, 'recclass')
    assert result == ('A', 2)
    data_2 = [
        {'recclass': 'A'},
        {'recclass': 'B'},
        {'recclass': 'B'},
        {'recclass': 'C'},
        {'recclass': 'B'},
        {'recclass': 'B'},
        {'recclass': 'B'},
        {'recclass': 'C'},
        {'recclass': 'B'}
    ]
    result_2 = most_common_class(data_2, 'recclass')
    assert result_2 == ('B', 6)
def test_most_common_location():
    data = [
        {'reclat': '30', 'reclong': '-40'},
        {'reclat': '-30', 'reclong': '-40'},
        {'reclat': '30', 'reclong': '40'},
        {'reclat': '-30', 'reclong': '-30'}
    ]
    result = most_common_location(data, 'reclat', 'reclong')
    assert result == ('Southern & Western', 2)
    data_2 = [
        {'reclat': '30', 'reclong': '-40'},
        {'reclat': '30', 'reclong': '60'},
        {'reclat': '30', 'reclong': '40'},
        {'reclat': '-30', 'reclong': '-30'},
   {'reclat': '30', 'reclong': '40'},
        {'reclat': '50', 'reclong': '70'}
    ]
    result = most_common_location(data_2, 'reclat', 'reclong')
    assert result == ('Northern & Eastern', 4)
def test_heaviest_meteorite():
    data = [
        {'name': 'A', 'mass (g)': '100'},
        {'name': 'B', 'mass (g)': '200'},
        {'name': 'C', 'mass (g)': '150'}
    ]
    result = heaviest_meteorite(data, 'mass (g)')
    assert result == ('B', 200)
    data_2 = [
        {'name': 'A', 'mass (g)': '100'},
        {'name': 'B', 'mass (g)': '200'},
        {'name': 'C', 'mass (g)': '150'},
        {'name': 'D', 'mass (g)': '50'},
        {'name': 'E', 'mass (g)': '65'},
        {'name': 'F', 'mass (g)': '450'},
        {'name': 'G', 'mass (g)': '254'}
    ]
    result_2 = heaviest_meteorite(data_2, 'mass (g)')
    assert result_2 == ('F', 450)
#Used ChatGPT to fix errors in this test function
def test_avg_distance_between_landings():
    data = [
        {'reclat': '30', 'reclong': '40'},
        {'reclat': '-30', 'reclong': '-40'},
        {'reclat': '20', 'reclong': '30'}
    ]
    result = avg_distance_between_landings(data, 'reclat', 'reclong')
    # Correct calculation for the expected result
    coordinates = [
        (30, 40, -30, -40),
        (-30, -40, 20, 30)
 ]
    expected_result = sum(solve_gcd(*x) for x in coordinates) / len(coordinates)
    assert result == pytest.approx(expected_result)
    data_2 = [
        {'reclat': '30', 'reclong': '40'},
        {'reclat': '-30', 'reclong': '-40'},
        {'reclat': '20', 'reclong': '30'},
        {'reclat': '-50', 'reclong': '-80'},
        {'reclat': '50', 'reclong': '-30'}
    ]
    result_2 = avg_distance_between_landings(data_2, 'reclat', 'reclong')
    # Correct calculation for the expected result
    coordinates_2 = [
        (30, 40, -30, -40),
        (-30, -40, 20, 30),
        (20,30,-50,-80),
        (-50,-80,50,-30)
    ]
    expected_result_2 = sum(solve_gcd(*x) for x in coordinates_2) / len(coordinates_2)
    assert result_2 == pytest.approx(expected_result_2)
