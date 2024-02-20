#!/usr/bin/env python3
import math
import pytest
from datetime import datetime
from iss_tracker import print_data, closest_time, avg_speed, closest_speed
#Used ChatGPT to fix errors

def test_print_data():
    sample_data= {'ndm': {'oem': {'body': {'segment': {'metadata': {
                            'START_TIME': '2024-047T12:00:00.000Z',
                            'STOP_TIME': '2024-047T15:30:20.123Z' }}}}},
        'stateVector': [
            {
                'EPOCH': '2024-047T12:00:00.000Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '4.86633012990265'},
                'Y_DOT': {'#text': '-2.7743207039670099'},
                'Z_DOT': {'#text': '5.2293448011352002'}
            },
            {
                'EPOCH': '2024-047T15:30:20.123Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '3.86633012990265'},
                'Y_DOT': {'#text': '-1.7743207039670099'},
                'Z_DOT': {'#text': '6.2293448011352002'}
            }
        ]
    }
    expected_start_time = 'February 16, 2024 12:00:00'
    expected_stop_time = 'February 16, 2024 15:30:20'
    x,y = print_data(sample_data['ndm']['oem']['body']['segment']['metadata'], 'START_TIME', 'STOP_TIME')
    assert x == expected_start_time

def test_closest_time():
    sample_data={'ndm': {'oem': {'body': {'segment': {'metadata': {
                            'START_TIME': '2024-047T12:00:00.000Z',
                            'STOP_TIME': '2024-047T15:30:20.123Z' }}}}},
        'stateVector': [
            {
                'EPOCH': '2024-047T12:00:00.000Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '4.86633012990265'},
                'Y_DOT': {'#text': '-2.7743207039670099'},
                'Z_DOT': {'#text': '5.2293448011352002'}
            },
        ]
    }
    closest_time_result = closest_time(sample_data, 'stateVector')
    assert closest_time_result['EPOCH'] ==  '2024-047T12:00:00.000Z'
def test_avg_speed():
    sample_data={'ndm': {'oem': {'body': {'segment': {'metadata': {
                            'START_TIME': '2024-047T12:00:00.000Z',
                            'STOP_TIME': '2024-047T15:30:20.123Z' }}}}},
        'stateVector': [
            {
                'EPOCH': '2024-047T12:00:00.000Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '4.86633012990265'},
                'Y_DOT': {'#text': '-2.7743207039670099'},
                'Z_DOT': {'#text': '5.2293448011352002'}
            },
            {
                'EPOCH': '2024-047T15:30:20.123Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '3.86633012990265'},
                'Y_DOT': {'#text': '-1.7743207039670099'},
                'Z_DOT': {'#text': '6.2293448011352002'}
            }
        ]
    }
    expected_avg_speed = (math.sqrt(4.86633012990265**2 + (-2.7743207039670099)**2 + 5.2293448011352002**2) +
                          math.sqrt(3.86633012990265**2 + (-1.7743207039670099)**2 + 6.2293448011352002**2)) / 2
    assert avg_speed(sample_data, 'stateVector') == expected_avg_speed

def test_closest_speed():
    sample_data={'ndm': {'oem': {'body': {'segment': {'metadata': {
                            'START_TIME': '2024-047T12:00:00.000Z',
                            'STOP_TIME': '2024-047T15:30:20.123Z' }}}}},
        'stateVector': [
            {
                'EPOCH': '2024-047T12:00:00.000Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '4.86633012990265'},
                'Y_DOT': {'#text': '-2.7743207039670099'},
                'Z_DOT': {'#text': '5.2293448011352002'}
            },
            {
                'EPOCH': '2024-047T15:30:20.123Z',
                'X': {'#text': '-4986.0259430215301'},
                'Y': {'#text': '-3800.9118236775798'},
                'Z': {'#text': '2615.0507852302399'},
                'X_DOT': {'#text': '3.86633012990265'},
                'Y_DOT': {'#text': '-1.7743207039670099'},
                'Z_DOT': {'#text': '6.2293448011352002'}
            }
        ]
    }
    closest_speed_result = closest_speed(sample_data, 'stateVector')
    assert closest_speed_result == 7.543305594058163  


