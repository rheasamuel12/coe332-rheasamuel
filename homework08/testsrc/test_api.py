import pytest
import requests


def test_submit_job_post():
    """Test the submit_job route."""
    data = {"hgnc_id_start": 5, "hgnc_id_end": 10}
    response = requests.post('http://127.0.0.1:5000/jobs', json=data)
    assert response.status_code == 200
    assert "New job added" in response.text

def test_submit_job_get():
    """Test the GET request to retrieve all jobs."""
    response = requests.get('http://127.0.0.1:5000/jobs')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_job():
    """Test the GET request to retrieve a job by ID."""
    all_jobs_response = requests.get('http://127.0.0.1:5000/jobs')
    all_jobs = all_jobs_response.json()
    if all_jobs:
        job_id = all_jobs[0]["id"]
        response = requests.get('http://127.0.0.1:5000/jobs/'+job_id)

        assert response.status_code == 200
        assert isinstance(response.json(), dict)



def test_handle_data_post():
    """Test the POST request to handle_data route."""

    data = {
        "response": {
            "docs": [
                {"hgnc_id": "TEST_ID_1", "other_data": "test_data_1"},
                {"hgnc_id": "TEST_ID_2", "other_data": "test_data_2"},
            ]
        }
    }

    response = requests.post('http://127.0.0.1:5000/data', json=data)


    assert response.status_code == 200



def test_handle_data_get():
    """Test the GET request to handle_data route."""
    response = requests.get('http://127.0.0.1:5000/data')
    if response.status_code != 200:
        print(response.content.decode('utf-8'))  # Print response content
    assert response.status_code == 200



def test_handle_data_delete():
    """Test the DELETE request to handle_data route."""
    response = requests.delete('http://127.0.0.1:5000/data')
    assert response.status_code == 200
    assert "All data deleted from Redis" in response.text

def test_all_genes():
    """Test the GET request to all_genes route."""
    data = {
        "response": {
            "docs": [
                {"hgnc_id": "TEST_ID_1", "other_data": "test_data_1"},
                {"hgnc_id": "TEST_ID_2", "other_data": "test_data_2"},
            ]
        }
    }

    response1 = requests.post('http://127.0.0.1:5000/data', json=data)
    response = requests.get('http://127.0.0.1:5000/genes')

    print(response.text)  # Print the response text for debugging

    assert response.status_code == 200

def test_gene_id():
    """Test the GET request to gene_id route with a valid ID."""
    all_genes_response = requests.get('http://127.0.0.1:5000/genes')
    all_genes = all_genes_response.json()

    print(all_genes)  # Print the list of genes for debugging

    if all_genes:
        valid_id = all_genes[0]  
        response = requests.get('http://127.0.0.1:5000/genes/'+valid_id)
        assert response.status_code == 200



