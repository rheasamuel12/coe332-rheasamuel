from jobs import get_job_by_id, update_job_status, q, rd
import time

@q.worker
def do_work(jobid):
    job = get_job_by_id(jobid)
    if job:
        update_job_status(jobid, 'in progress')
        time.sleep(15) 
        print(“Processing job:“, job_info)
        update_job_status(jobid, 'complete')

if __name__ == '__main__':
    do_work()
