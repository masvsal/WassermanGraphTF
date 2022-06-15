import requests
import csv
from core import config as cfg
import utility_functions as utilfcns

#PARAMETERS:
#MODIFIES: csv file for storing tf family info, csv file for storing tf pfm info
#EFFECTS: queries jasper database for annotation information relating to yamanaka proteins. 
#Saves response to separate csv files.

#REST API URL
request_url = cfg.JASPAR_BASE_URL + "/api/v1/matrix"

#yamanaka TFs
gene_names = ["KLF4", "MYC", "SOX17", "SOX2", "POU5F1"]
jaspar_annotation = []

#parameters for GET request
params = {
    'page':1, #mandatory
    'page_size':500,
    'collection': "CORE",
    'tax_id':9606,
    'version': "latest",
    'name': ''
}

#one large api call (useful for queries w many TFs):
""" 
while len(primary_TFs) > 0:
    r = requests.get(request_url,params=params)
    response = r.json()
    results = response['results']

    for entry in results:
        for TF in primary_TFs:
            if (TF == entry['name']):
                print(entry)
                primary_TFs.remove(TF)

    if(not response['next']):
        break

    params["page"]+=1 """

#multiple small api calls (useful for small TF networks)
#saves basic info about TFs as a map
for i in range(len(gene_names)):
    params['name'] = gene_names[i]
    r = requests.get(request_url,params=params)
    response = r.json()
    results = response['results']
    for result in results:
        print(result)
        jaspar_annotation += [{
            'search_keyword':gene_names[i],
            'protein_name':result['name'],
            'latest_matrix_id':result['matrix_id'],
            'collection':result['collection'],
            'url':result['url']
            }]


#multiple small api calls
#enriches basic TF map by adding new profile details
for i in range(len(jaspar_annotation)):
    request_url_specific = request_url + "/" + jaspar_annotation[i]['latest_matrix_id']
    r = requests.get(request_url_specific)
    response = r.json()
    print(response)
    jaspar_annotation[i]['pubmed_ids'] = response['pubmed_ids']
    jaspar_annotation[i]['medline'] = response['medline']
    jaspar_annotation[i]['tffm'] = response['tffm']
    jaspar_annotation[i]['pfm'] = response['pfm']
    jaspar_annotation[i]['uniprot_ids'] = response['uniprot_ids']
    jaspar_annotation[i]['family'] = response['family']
    jaspar_annotation[i]['class'] = response['class']
    jaspar_annotation[i]['collection'] = response['collection']
    jaspar_annotation[i]['group'] = response['tax_group'] + '[' + utilfcns.list_to_pipe_del(response['species']) + ']'
    jaspar_annotation[i]['data type'] = response['type']
    jaspar_annotation[i]['data_source'] = response['source']

for i in range(len(jaspar_annotation)):
    jaspar_annotation[i]['uniprot_ids'] = utilfcns.list_to_pipe_del(jaspar_annotation[i]['uniprot_ids'])
    jaspar_annotation[i]['pubmed_ids'] = utilfcns.list_to_pipe_del(jaspar_annotation[i]['pubmed_ids'])
    jaspar_annotation[i]['medline'] = utilfcns.list_to_pipe_del(jaspar_annotation[i]['medline'])
    jaspar_annotation[i]['family'] = utilfcns.list_to_pipe_del(jaspar_annotation[i]['family'])
    jaspar_annotation[i]['class'] = utilfcns.list_to_pipe_del(jaspar_annotation[i]['class'])
    #TODO: make ACGT in pfm lists

#saves family info in TF map to output csv
with open("graph_data/gene_annotations/jaspar_TF_Class_Family.csv", "w",  encoding='UTF8') as file:
    f = csv.writer(file)
    f.writerow(['protein_name', "uniprot_ids", "jaspar_id", 'url', "collection", 'family', 'class', "pubmed_ids", "medline", 'tax_group'])
    for i in jaspar_annotation:
        f.writerow([i['protein_name'], i["uniprot_ids"], i["latest_matrix_id"], i['url'], i["collection"], i['family'], i['class'], i['pubmed_ids'], i['medline'], i['group']])

#saves PFM info in TF map to output csv
with open("graph_data/gene_annotations/jaspar_TF_PFM.csv", "w",  encoding='UTF8') as file:
    f = csv.writer(file)
    f.writerow(['protein_name', 'uniprot_ids', 'jaspar_id', 'url', "collection",'A', 'C', 'G', 'T', "pubmed_ids", "medline", 'tax_group', 'data_type', 'data_source'])
    for i in jaspar_annotation:
        f.writerow([i['protein_name'], i["uniprot_ids"], i["latest_matrix_id"],i['url'], i["collection"], i['pfm']["A"], i['pfm']["C"], i['pfm']["G"], i['pfm']["T"], i['pubmed_ids'], i['medline'], i['group'], i['data type'], i['data_source']])

 




    

