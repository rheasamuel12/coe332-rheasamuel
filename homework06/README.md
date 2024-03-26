# Moonrise Genes
### Descripion
The following files read through the HGNC data and inject it into a Redis database through a Flask interface. This dataset provides comprehensive information about various human genes.

Here are somee examples:

hgnc_id: The unique identifier assigned by HGNC to each gene.
symbol: The gene symbol, often used as an abbreviated representation.
name: The full name or description of the gene.
locus_group: The general classification of the gene.
locus_type: Further classification specifying the gene's type.

There are many more that are found within the data as well.

### Included Files
1. `gene_api.py`

   This file reads includes four different functions:
   
   `handle_data`: This function handles POST, GET, and DELETE requests for data loading into Redis, fetching data from Redis, and deleting all data in Redis.
   
   `all_genes`: This function returns a list of all gene IDs from Redis.

   `gene_id`: This function returns gene information for the given hgnc_id.
   
2. `Dockerfile`
   
    The Dockerfile is a recipe for creating a Docker image containing a sequential set of commands (a recipe) for installing and configuring the application.
3. `docker-compose.yaml`

    The docker compose simplifies the management of multi-container Docker applications using rules defined in a YAML file

4. `requirements.txt`

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

2. `curl -X GET localhost:5000/data"`

Returns all data from Redis

3. `curl -X DELETE localhost:5000/data`

Deletes data in Redis

4. `curl localhost:5000/genes`

Returns json-formatted list of all hgnc_ids

5.`curl localhost:5000/genes/<hgnc_id>`

Returns all data associated with <hgnc_id>

### Sample Code
```
if request.method == 'POST':
        for item in data['response']['docs']:
            hgnc_id = item.get('hgnc_id', '')  
            if hgnc_id:
                rd.set(hgnc_id, json.dumps(item))
        
        return "Data loaded into Redis"
```
This code is from the handle_data() function in the gene_api.py script. It first checks if the request method is post, and then goes through the data to find the hgnc_id. Then it inputs the data in redis using the hgnc_id as the unique key.
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
