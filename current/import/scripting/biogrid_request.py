import requests
import fetch_endpoint as fe
import csv
from core import config as cfg

#PARAMETERS: none
#MODIFIES: output csv
#EFFECTS: gets all human BIOGrid interactions between given proteins. Writes output to csv file.

#REST API URL
request_ext = "/interactions"

#GET request parameters
def get_interactions(gene_names):
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
    r = fe.fetch_endpoint(cfg.BIOGRID_BASE_URL,request_ext,params=params)
    data = r.json()
    print(data)
    #write response to output csv
    with open("current/data/protein_interactions/biogrid_interactions.csv", "w", encoding='UTF8') as file:
        f=csv.writer(file)
        f.writerow(["BIOGRID_INTERACTION_ID", 'ENTREZ_GENE_A', 'ENTREZ_GENE_B', 'BIOGRID_ID_A', 'BIOGRID_ID_B', 'SYSTEMATIC_NAME_A', 'SYSTEMATIC_NAME_B', 'OFFICIAL_SYMBOL_A', 'OFFICIAL_SYMBOL_B','SYNONYMS_A', 'SYNONYMS_B', 'EXPERIMENTAL_SYSTEM', 'EXPERIMENTAL_SYSTEM_TYPE', 'PUBMED_AUTHOR','PUBMED_ID','ORGANISM_A', 'ORGANISM_B','THROUGHPUT','QUANTITATION','MODIFICATION','ONTOLOGY_TERMS', 'QUALIFICATIONS', 'TAGS', 'SOURCEDB'])
        for key,value in data.items():
            f.writerow([value["BIOGRID_INTERACTION_ID"], value['ENTREZ_GENE_A'], value['ENTREZ_GENE_B'], value['BIOGRID_ID_A'], value['BIOGRID_ID_B'], value['SYSTEMATIC_NAME_A'], value['SYSTEMATIC_NAME_B'], value['OFFICIAL_SYMBOL_A'], value['OFFICIAL_SYMBOL_B'],value['SYNONYMS_A'], value['SYNONYMS_B'], value['EXPERIMENTAL_SYSTEM'], value['EXPERIMENTAL_SYSTEM_TYPE'], value['PUBMED_AUTHOR'],value['PUBMED_ID'],value['ORGANISM_A'], value['ORGANISM_B'],value['THROUGHPUT'],value['QUANTITATION'],value['MODIFICATION'],value['ONTOLOGY_TERMS'], value['QUALIFICATIONS'], value['TAGS'], value['SOURCEDB']])
gene_names = cfg.GENE_NAMES
print('BIOGRID: Looking up interactions using gene names',end="")
get_interactions(gene_names=gene_names)
print('Done')