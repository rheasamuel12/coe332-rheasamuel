import pytest
import json
import os
import sys
import redis

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jobs import add_job, get_job_by_id, update_job_status, results, rd

def test_add_job():
    """Test the add_job function."""
    hgnc_id_start = 5
    hgnc_id_end = 10

    job_dict = add_job(hgnc_id_start, hgnc_id_end)
    assert job_dict is not None
    assert "id" in job_dict
    assert "status" in job_dict
    assert "hgnc_id_start" in job_dict
    assert "hgnc_id_end" in job_dict

def test_get_job_by_id():
    """Test the get_job_by_id function."""
    hgnc_id_start = 5
    hgnc_id_end = 10

    job_dict = add_job(hgnc_id_start, hgnc_id_end)
    job_id = job_dict["id"]

    retrieved_job = get_job_by_id(job_id)
    assert retrieved_job is not None
    assert retrieved_job["id"] == job_id
    assert retrieved_job["hgnc_id_start"] == hgnc_id_start
    assert retrieved_job["hgnc_id_end"] == hgnc_id_end

def test_update_job_status():
    """Test the update_job_status function."""
    hgnc_id_start = 5
    hgnc_id_end = 10

    job_dict = add_job(hgnc_id_start, hgnc_id_end)
    job_id = job_dict["id"]

    updated_status = "completed"
    update_job_status(job_id, updated_status)

    retrieved_job = get_job_by_id(job_id)
    assert retrieved_job is not None
    assert retrieved_job["status"] == updated_status

def test_get_result_by_id():
    """Test the get_result_by_id function."""
    hgnc_id_start = 5
    hgnc_id_end = 10

    job_dict = add_job(hgnc_id_start, hgnc_id_end)
    job_id = job_dict["id"]

    result = {"result_key": "result_value"}
    results.set(job_id, json.dumps(result))

    retrieved_result = results.get(job_id)
    assert retrieved_result is not None
    assert json.loads(retrieved_result) == result

