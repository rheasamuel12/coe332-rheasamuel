from gcd_algorithm import solve_gcd
import pytest

def test_solve_gcd():
    #Test 1
    lat_a, lon_a = 10.0, 20.0
    lat_b, lon_b = 10.0, 20.0
    result = solve_gcd(lat_a, lon_a, lat_b, lon_b)
    assert(result, 0.0)


    #Test 2
    lat_a2, lon_a2 = 10.0, 20.0
    lat_b2, lon_b2 = 15.0, 25.0
    result2 = solve_gcd(lat_a, lon_a, lat_b, lon_b)
    assert(result2, 44510.8082991)
