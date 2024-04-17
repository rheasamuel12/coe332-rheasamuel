import json
from hotqueue import HotQueue
import redis
import logging
import os
from jobs import get_job_by_id, update_job_status, q, rd, results
#Used ChatGPT to fix errors and understand more


_redis_ip = os.environ.get('REDIS_IP', 'redis-db')
rd = redis.Redis(host=_redis_ip, port=6379, db=0)
q = HotQueue("queue", host=_redis_ip, port=6379, db=1)
results = redis.Redis(host=_redis_ip, port=6379, db=3)
def perform_analysis(jobid):
    job = get_job_by_id(jobid)
    if job:
        logging.debug("Updated job status to in progress")
        hgnc_id_start = job.get('hgnc_id_start')
        hgnc_id_end = job.get('hgnc_id_end')

        gene_data = []
        for key in rd.keys():
            gene_info = json.loads(rd.get(key))
            hgnc_id = gene_info.get('hgnc_id', '')
            
            if hgnc_id.startswith('HGNC:'):
                hgnc_id = hgnc_id.replace('HGNC:', '')
                hgnc_id = int(hgnc_id)
                if hgnc_id_start <= hgnc_id <= hgnc_id_end:
                    gene_data.append(gene_info)
                    logging.debug("Added gene data")
                
        
        location_counts = {}
        for gene in gene_data:
            logging.debug("Updating location count")
            location = gene['location']
            if location in location_counts:
                location_counts[location] += 1
            else:
                location_counts[location] = 1
        
        most_common_location = max(location_counts, key=location_counts.get, default="No locations found")
        
        result = {
            "Most Common Location found in HGNC_ID parameters given": most_common_location
        }
        
        results.set(jobid, json.dumps(result))
        
@q.worker
def do_work(jobid):
    """
    Returns most common location based on hgnc_id start and end parameters
    
    Args:
        jobid: The job ID 
    
    Returns:
        dict: Most common location 
    """ 
    job = get_job_by_id(jobid)
    if job:
        update_job_status(jobid, 'in progress')
        logging.debug("Updated job status to in progress")
        perform_analysis(job)
        update_job_status(jobid, 'complete')


if __name__ == '__main__':
    do_work()


