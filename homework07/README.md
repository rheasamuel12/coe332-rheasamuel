# The Grand Budapest Job
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

6. `curl localhost:5000/jobs -X POST -d '{"symbol":1, "locus_type":2}' -H "Content-Type: application/json"`

Creates a new job with a unique identifier (uuid). Make sure to use the paramters "symbol" and "locus_type".

7. `curl localhost:5000/jobs`

Returns the list of existing jobs

8. `curl localhost:5000/jobs/<jobid>`

Returns job information for a given job ID
### Sample Code
```
@app.route('/jobs', methods=['GET', 'POST'])
def submit_job():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'symbol' not in data or 'locus_type' not in data:
            return jsonify({'error': 'Missing parameters. Please provide symbol and locus_type'}), 400
        job_dict = add_job(data['symbol'], data['locus_type'])
        return "New job added"
    elif request.method == 'GET':
        all_jobs = []
        for jid in jdb.keys():
            job = json.loads(jdb.get(jid))
            all_jobs.append(job)
        return jsonify(all_jobs), 200)
```
This code is from the submit_job() function in the api.py script. It checks if the parameters exist within the data, and then adds the job with the correct parameters.
### Sample Results
Using this route `curl -X POST localhost:5000/data`, the following output occurs.
`Data loaded into Redis`

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

