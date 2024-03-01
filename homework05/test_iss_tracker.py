import pytest
from app import app
from flask import Flask, request
from datetime import datetime

#Used ChatGPT to figure out how to use pytest with flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_print_data_valid(client):
    response = client.get('/epochs?limit=5&offset=0')
    assert response.status_code == 200

def test_print_data_invalid_limit(client):
    response = client.get('/epochs?limit=abc&offset=0')
    assert response.status_code == 200  

def test_print_epoch_valid(client):
    response = client.get('/epochs/valid_epoch')
    assert response.status_code == 200

def test_print_epoch_invalid(client):
    response = client.get('/epochs/invalid_epoch')
    assert response.status_code == 200  

def test_inst_speed_valid(client):
    response = client.get('/epochs/valid_epoch/speed')
    assert response.status_code == 200

def test_inst_speed_invalid(client):
    response = client.get('/epochs/invalid_epoch/speed')
    assert response.status_code == 200 

def test_closest_speed(client):
    response = client.get('/now')
    assert response.status_code == 200




