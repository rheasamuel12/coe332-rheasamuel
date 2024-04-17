import requests
from flask import Flask, jsonify, request
import logging
import redis
import sys
from jobs import add_job, get_job_by_id, jdb, get_result_by_id
import json
import os

#Used ChatGPT to fix errors and understand more

app = Flask(__name__)
rd = redis.Redis(host='redis-db', port=6379, db=0)
response = requests.get('https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
data = response.json()

log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=log_level)

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

@app.route('/jobs', methods=['GET', 'POST', 'DELETE'])
def submit_job():
    """
    Submits job based on POST or GET message
    
    
    Returns:
        string: Either confirmation of added job or json dictionary of all jobs
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'hgnc_id_start' not in data or 'hgnc_id_end' not in data:
            return jsonify({'error': 'Missing parameters. Please provide a start and end hgnc_id'}), 400
        job_dict = add_job(data['hgnc_id_start'], data['hgnc_id_end'])
        logging.warning("New job added")
        return "New job added", 200
    elif request.method == 'GET':
        all_jobs = [json.loads(jdb.get(jid)) for jid in jdb.keys()]
        logging.debug("Retrieved all jobs")
        return jsonify(all_jobs), 200
    
    

@app.route('/jobs/<jobid>', methods=['GET'])
def get_job(jobid):
    """
    Returns specific job
    
    Args:
        jobid: The job ID 
    
    Returns:
        dict: Job dictionary based on jid
    """
    logging.debug("Retrieved job")
    return get_job_by_id(jobid)


@app.route('/data', methods=['GET','POST','DELETE'])
def handle_data():
    """
    Handles POST, GET, and DELETE requests for data loading into Redis, fetching data from Redis, and deleting all data in Redis.
    
    Returns:
        str: A message confirming the action taken
    """
    if request.method == 'POST':
        for item in data['response']['docs']:
            hgnc_id = item.get('hgnc_id', '')  
            if hgnc_id:
                rd.set(hgnc_id, json.dumps(item))
                logging.debug("Added data")
            else:
                logging.error("Invalid HGNC_ID")
        
        return "Data loaded into Redis", 200

    elif request.method == 'GET':
        return_value = []
        for item in rd.keys():
            val = json.loads(rd.get(item))
            if val:
                return_value.append(val)
                logging.debug("Got data")
            else:
                logging.error("Invalid value")
        return return_value, 200
    
    elif request.method == 'DELETE':
        for item in rd.keys():
            rd.delete(item)
            logging.debug("Deleted data")
        return "All data deleted from Redis", 200
    else:
        logging.error("Invalid method")
        return "Please use one of the following methods: POST, GET, DELETE"

@app.route('/genes', methods=['GET'])
def all_genes():
    """
    Returns a list of all gene IDs from Redis.
    
    Returns:
        list: A json formatted list of gene IDs
    """
    genes = []

    for key in rd.keys():
        value = rd.get(key)
        if value:
            gene_data = json.loads(value)
            hgnc_id = gene_data.get('hgnc_id', '')
            if hgnc_id:
                genes.append(hgnc_id)
                logging.debug("Added gene ID")

    if not genes:
        logging.error("No data in Redis")
        return jsonify({"message": "No data found in Redis"}), 404

    return jsonify(genes), 200

@app.route('/genes/<hgnc_id>', methods=['GET'])
def gene_id(hgnc_id):
    """
    Returns gene information for the given hgnc_id.
    
    Args:
        hgnc_id (str): The HGNC ID of the gene
    
    Returns:
        dict: Gene information
    """
    gene_data = rd.get(hgnc_id)
    
    if gene_data is None:
        logging.error("INVALID GENE ID")
        return jsonify({"error": "Gene ID not found"}), 404

    gene_data = json.loads(gene_data)
    logging.warning("Formatted gene info following")
    gene_info = {
        "hgnc_id": gene_data.get('hgnc_id', ''),
        "symbol": gene_data.get('symbol', ''),
        "name": gene_data.get('name', ''),
        "locus_group": gene_data.get('locus_group', ''),
        "locus_type": gene_data.get('locus_type', ''),
        "status": gene_data.get('status', ''),
        "location": gene_data.get('location', ''),
        "location_sortable": gene_data.get('location_sortable', ''),
        "alias_symbol": gene_data.get('alias_symbol', ''),
        "alias_name": gene_data.get('alias_name', ''),
        "prev_symbol": gene_data.get('prev_symbol', ''),
        "prev_name": gene_data.get('prev_name', ''),
        "gene_group": gene_data.get('gene_group', ''),
        "gene_group_id": gene_data.get('gene_group_id', ''),
        "date_approved_reserved": gene_data.get('date_approved_reserved', ''),
        "date_symbol_changed": gene_data.get('date_symbol_changed', ''),
        "date_name_changed": gene_data.get('date_name_changed', ''),
        "date_modified": gene_data.get('date_modified', ''),
        "entrez_id": gene_data.get('entrez_id', ''),
        "ensembl_gene_id": gene_data.get('ensembl_gene_id', ''),
        "vega_id": gene_data.get('vega_id', ''),
        "ucsc_id": gene_data.get('ucsc_id', ''),
        "ena": gene_data.get('ena', ''),
        "refseq_accession": gene_data.get('refseq_accession', ''),
        "ccds_id": gene_data.get('ccds_id', ''),
        "uniprot_ids": gene_data.get('uniprot_ids', ''),
        "pubmed_id": gene_data.get('pubmed_id', ''),
        "mgd_id": gene_data.get('mgd_id', ''),
        "rgd_id": gene_data.get('rgd_id', ''),
        "lsdb": gene_data.get('lsdb', ''),
        "cosmic": gene_data.get('cosmic', ''),
        "omim_id": gene_data.get('omim_id', ''),
        "mirbase": gene_data.get('mirbase', ''),
        "homeodb": gene_data.get('homeodb', ''),
        "snornabase": gene_data.get('snornabase', ''),
        "bioparadigms_slc": gene_data.get('bioparadigms_slc', ''),
        "orphanet": gene_data.get('orphanet', ''),
        "pseudogene.org": gene_data.get('pseudogene.org', ''),
        "horde_id": gene_data.get('horde_id', ''),
        "merops": gene_data.get('merops', ''),
        "imgt": gene_data.get('imgt', ''),
        "iuphar": gene_data.get('iuphar', ''),
        "kznf_gene_catalog": gene_data.get('kznf_gene_catalog', ''),
        "mamit-trnadb": gene_data.get('mamit-trnadb', ''),
        "cd": gene_data.get('cd', ''),
        "lncrnadb": gene_data.get('lncrnadb', ''),
        "enzyme_id": gene_data.get('enzyme_id', ''),
        "intermediate_filament_db": gene_data.get('intermediate_filament_db', ''),
        "rna_central_ids": gene_data.get('rna_central_ids', ''),
        "lncipedia": gene_data.get('lncipedia', ''),
        "gtrnadb": gene_data.get('gtrnadb', ''),
        "agr": gene_data.get('agr', ''),
        "mane_select": gene_data.get('mane_select', ''),
        "gencc": gene_data.get('gencc', '')
    }
    
    response_json = json.dumps(gene_info, indent=4)
    
    return response_json, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)
