import json
import redis
import os
import sys

#Used ChatGPT to fix errors and understand more


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jobs import results, rd, q, get_job_by_id, add_job
from worker import do_work, perform_analysis

def test_do_work():
    hgnc_id_start = 1
    hgnc_id_end = 5

    job_dict = add_job(hgnc_id_start, hgnc_id_end)
    job_id = job_dict["id"]

    print(job_id)
    
    gene_data = [
        {"hgnc_id": "HGNC:1", "location": "Location1"},
        {"hgnc_id": "HGNC:2", "location": "Location2"},
        {"hgnc_id": "HGNC:3", "location": "Location1"},
        {"hgnc_id": "HGNC:4", "location": "Location2"},
        {"hgnc_id": "HGNC:5", "location": "Location2"},
        {"hgnc_id": "HGNC:6", "location": "Location3"}  
    ]

    for i, gene_info in enumerate(gene_data):
        rd.set(f"gene_{i}", json.dumps(gene_info))

    q.put(job_id)
    results.delete(job_id)
    rd.flushdb()
    results.flushdb()

    perform_analysis(job_id)

    result = json.loads(results.get(job_id))

    expected_result = {
        "Most Common Location found in HGNC_ID parameters given": "Location3"
    }
    assert result != expected_result

    results.delete(job_id)
    rd.flushdb()
    results.flushdb()


if __name__ == "__main__":
    test_do_work()


