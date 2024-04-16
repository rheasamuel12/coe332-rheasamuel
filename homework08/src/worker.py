import json
from hotqueue import HotQueue
import redis
import os
from jobs import get_job_by_id, update_job_status, q, rd, results

_redis_ip = os.environ.get('REDIS_IP', 'redis-db')
rd = redis.Redis(host=_redis_ip, port=6379, db=0)
q = HotQueue("queue", host=_redis_ip, port=6379, db=1)
results = redis.Redis(host=_redis_ip, port=6379, db=3)

@q.worker
def do_work(jobid):
    job = get_job_by_id(jobid)
    if job:
        update_job_status(jobid, 'in progress')

        hgnc_id_start = job.get('hgnc_id_start')
        hgnc_id_end = job.get('hgnc_id_end')

        gene_data = []
        for key in rd.keys():
            gene_info = json.loads(rd.get(key))
            hgnc_id = gene_info.get('hgnc_id', '')
            
            # Validate hgnc_id before trying to convert to integer
            if hgnc_id.startswith('HGNC:'):
                hgnc_id = hgnc_id.replace('HGNC:', '')
                try:
                    hgnc_id = int(hgnc_id)
                    if hgnc_id_start <= hgnc_id <= hgnc_id_end:
                        gene_data.append(gene_info)
                except ValueError:
                    # Handle the case where hgnc_id cannot be converted to int
                    continue
        
        # Manually count the occurrences of each location
        location_counts = {}
        for gene in gene_data:
            location = gene['location']
            if location in location_counts:
                location_counts[location] += 1
            else:
                location_counts[location] = 1
        
        # Find the most common location
        most_common_location = max(location_counts, key=location_counts.get, default="No locations found")
        
        # Create the result dictionary with only the location
        result = {
            "Most Common Location found in HGNC_ID parameters given": most_common_location
        }
        
        # Store only the location in results
        results.set(jobid, json.dumps(result))
        
        update_job_status(jobid, 'complete')

if __name__ == '__main__':
    do_work()


