# Isle of Web Apps
### Descripion
The following files read through the HGNC data and inject it into a Redis database through a Flask interface while also including job functionaily. This dataset provides comprehensive information about various human genes.

Here are somee examples:

hgnc_id: The unique identifier assigned by HGNC to each gene.
symbol: The gene symbol, often used as an abbreviated representation.
name: The full name or description of the gene.
locus_group: The general classification of the gene.
locus_type: Further classification specifying the gene's type.

There are many more that are found within the data as well.

### Included Files
1. `api.py`

   This file reads includes four different functions:

    `submit_job`: This function handles POST and GET requests for creating new jobs and returning the existing jobs.
   
   `handle_data`: This function handles POST, GET, and DELETE requests for data loading into Redis, fetching data from Redis, and deleting all data in Redis.
   
   `all_genes`: This function returns a list of all gene IDs from Redis.

   `gene_id`: This function returns gene information for the given hgnc_id.
   
2. `worker.py`

    This file will contain all of the functionality needed to get jobs from the task queue and execute the jobs.
3. `jobs.py`

    This file will contain all functionality needed for working with jobs in the Redis database and the Hotqueue queue.
4. `Dockerfile`
   
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.
5. `docker-compose.yaml`

    The docker compose simplifies the management of multi-container Docker applications using rules defined in a YAML file

6. `requirements.txt`

    The requirements file contains all the non-standard Python libraries essential for our application.

7. `test_api.py`, `test_worker.py`, `test_jobs.py`

    These files contain the pytest unit tests for each respective file
### Building Instructions
Make sure you have docker and flask installed before starting. To build the python scripts type

`docker-compose build`

### Running/Building Instructions
In the command line type
`docker-compose up -d`

to start the container in the background.
To run each route:
1. `curl -X POST localhost:5000/data`

Puts data into Redis

2. `curl -X GET localhost:5000/data`

Returns all data from Redis

3. `curl -X DELETE localhost:5000/data`

Deletes data in Redis

4. `curl localhost:5000/genes`

Returns json-formatted list of all hgnc_ids

5.`curl localhost:5000/genes/<hgnc_id>`

Returns all data associated with <hgnc_id>

6. `curl localhost:5000/jobs -X POST -d '{"hgnc_id_start":1, "hgnc_id_end":10000}' -H "Content-Type: application/json"`

Creates a new job with a unique identifier (uuid). Make sure to use the paramters "hgnc_id_start" and "hgnc_id_end".

7. `curl localhost:5000/jobs`

Returns the list of existing jobs

8. `curl localhost:5000/jobs/<jobid>`

Returns job information for a given job ID

9. `curl localhost:5000/results/<jobid>`

Returns the most common location found within the parameters "hgnc_id_start" and "hgnc_id_end".

### Pytest
To run pytest, simply type  `docker ps -a` in the command line. Then find the container ID for python api.py. Type `docker exec -it <container ID> pytest` to run the test scripts inside the already running flask container.

### Logging
To view logging messages, simply type  `docker ps -a` in the command line to get the container ID. Then, type `docker logs <container_id> in the command line to see the logging messages/
### Software Diagram
![hw8diagram](https://github.com/rheasamuel12/coe332-rheasamuel/assets/143050090/168a8b16-7782-41a2-aa2f-27def48858ae)
### Sample Code
```
@app.route('/results/<jobid>', methods=['GET', 'POST'])
def ret_info(jobid):
    """
    Returns results from do_work() in worker
    
    Args:
        jobid: The job ID 
    
    Returns:
        dict: Most common location 
    """
    result = get_result_by_id(jobid)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"message": "Job result not found or job is still in progress"}), 404
```
This code is from the ret_info() function in the api.py script. It finds results from the do_work() function in worker.py and returns the most common location

### Sample Results

To test another route, I could call ` curl localhost:5000/genes/HGNC:5`. The following output occurs:
```
{
    "hgnc_id": "HGNC:5",
    "symbol": "A1BG",
    "name": "alpha-1-B glycoprotein",
    "locus_group": "protein-coding gene",
    "locus_type": "gene with protein product",
    "status": "Approved",
    "location": "19q13.43",
    "location_sortable": "19q13.43",
    "alias_symbol": "",
    "alias_name": "",
    "prev_symbol": "",
    "prev_name": "",
    "gene_group": "Immunoglobulin like domain containing",
    "gene_group_id": "594",
    "date_approved_reserved": "1989-06-30",
    "date_symbol_changed": "",
    "date_name_changed": "",
    "date_modified": "2023-01-20",
    "entrez_id": "1",
    "ensembl_gene_id": "ENSG00000121410",
    "vega_id": "OTTHUMG00000183507",
    "ucsc_id": "uc002qsd.5",
    "ena": "",
    "refseq_accession": "NM_130786",
    "ccds_id": "CCDS12976",
    "uniprot_ids": "P04217",
    "pubmed_id": "2591067",
    "mgd_id": "MGI:2152878",
    "rgd_id": "RGD:69417",
    "lsdb": "",
    "cosmic": "",
    "omim_id": "138670",
    "mirbase": "",
    "homeodb": "",
    "snornabase": "",
    "bioparadigms_slc": "",
    "orphanet": "",
    "pseudogene.org": "",
    "horde_id": "",
    "merops": "I43.950",
    "imgt": "",
    "iuphar": "",
    "kznf_gene_catalog": "",
    "mamit-trnadb": "",
    "cd": "",
    "lncrnadb": "",
    "enzyme_id": "",
    "intermediate_filament_db": "",
    "rna_central_ids": "",
    "lncipedia": "",
    "gtrnadb": "",
    "agr": "HGNC:5",
    "mane_select": "ENST00000263100.8, NM_130786.4",
    "gencc": ""
}
```

This route printed out all the data listed with the hgnc_id key.

### Citations
HGNC data set: https://www.genenames.org/download/archive/
