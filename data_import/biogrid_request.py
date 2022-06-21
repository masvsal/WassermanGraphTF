import requests
import json
import csv
from core import config as cfg
import pandas as pd

#PARAMETERS: none
#MODIFIES: output csv
#EFFECTS: gets all human BIOGrid interactions between given proteins. Writes output to csv file.


#REST API URL
request_url = cfg.BIOGRID_BASE_URL + "/interactions"

#list of proteins to search for
geneList = ["KLF4", "MYC", "SOX17", "SOX2", "POU5F1"]

#GET request parameters
params = {
    "accesskey": cfg.BIOGRID_ACCESS_KEY,
    "format": "json",
    "geneList": "|".join(geneList),  # Must be | separated
    "searchNames": "true",  # Search against official names
    "includeInteractors": "false",  # Set to true to get any interaction involving EITHER gene, set to false to get interactions between genes
    "taxId": 9606,  # Limit to Saccharomyces cerevisiae
    "includeHeader": "true",
    "interSpeciesExcluded":False,
}

#execute GET request and parse as JSON
r = requests.get(request_url, params=params)
data = r.json()

#write response to output csv
with open("graph_data/protein_interactions/biogrid_interactions.csv", "w", encoding='UTF8') as file:
    f=csv.writer(file)
    f.writerow(["BIOGRID_INTERACTION_ID", 'ENTREZ_GENE_A', 'ENTREZ_GENE_B', 'BIOGRID_ID_A', 'BIOGRID_ID_B', 'SYSTEMATIC_NAME_A', 'SYSTEMATIC_NAME_B', 'OFFICIAL_SYMBOL_A', 'OFFICIAL_SYMBOL_B','SYNONYMS_A', 'SYNONYMS_B', 'EXPERIMENTAL_SYSTEM', 'EXPERIMENTAL_SYSTEM_TYPE', 'PUBMED_AUTHOR','PUBMED_ID','ORGANISM_A', 'ORGANISM_B','THROUGHPUT','QUANTITATION','MODIFICATION','ONTOLOGY_TERMS', 'QUALIFICATIONS', 'TAGS', 'SOURCEDB'])
    for key,value in data.items():
        f.writerow([value["BIOGRID_INTERACTION_ID"], value['ENTREZ_GENE_A'], value['ENTREZ_GENE_B'], value['BIOGRID_ID_A'], value['BIOGRID_ID_B'], value['SYSTEMATIC_NAME_A'], value['SYSTEMATIC_NAME_B'], value['OFFICIAL_SYMBOL_A'], value['OFFICIAL_SYMBOL_B'],value['SYNONYMS_A'], value['SYNONYMS_B'], value['EXPERIMENTAL_SYSTEM'], value['EXPERIMENTAL_SYSTEM_TYPE'], value['PUBMED_AUTHOR'],value['PUBMED_ID'],value['ORGANISM_A'], value['ORGANISM_B'],value['THROUGHPUT'],value['QUANTITATION'],value['MODIFICATION'],value['ONTOLOGY_TERMS'], value['QUALIFICATIONS'], value['TAGS'], value['SOURCEDB']])
