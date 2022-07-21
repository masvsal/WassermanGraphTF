import pandas as pd
import fetch_endpoint as fe
import json
from core import config as cfg

#PARAMETERS: none
#MODIFIES: output csv
#EFFECTS: gets all human BIOGrid interactions between given proteins. Writes output to csv file.

#GET request parameters
def get_interactions(gene_names):
    params = {
        "accesskey": cfg.BIOGRID_ACCESS_KEY,
        "format": "json",
        "geneList": "|".join(gene_names),  # Must be | separated
        "searchNames": "true",  # Search against official names
        "includeInteractors": "false",  # Set to true to get any interaction involving EITHER gene, set to false to get interactions between genes
        "taxId": 9606,  # Limit to Saccharomyces cerevisiae
        "includeHeader": "true",
        "interSpeciesExcluded":False,
    }
    #execute GET request and parse as JSON
    r = fe.fetch_endpoint(cfg.BIOGRID_BASE_URL,'/interactions',params=params)
    data = r.json()
    with open('current/data/view.json', 'w') as f:
        json.dump(data, f)
    #write response to output csv
    flattened_response = flatten_dict_of_dicts(data)
    df = pd.json_normalize(flattened_response)
    return df

#biogrid returns json as dictionary of interactions hashed by the interaction ID. Each id maps to an inner dictionary containing further details. 
#This function flattens this into a single dictionary with the interaction ID identifed by 'InteractionID'
#{446464:{detail1:dasd,detail2:dfsd},446481:{detail1:dasd,detail2:dfsd}} -> [{interactionID:446464,detail1:dasd,detail2:dfsd},{interactionID:446481,detail1:dasd,detail2:dfsd}]
def flatten_dict_of_dicts(json_response):
    return_list = []
    for id in json_response:
        id_details = json_response[id]
        id_details['BIOGRID_INTERACTION_ID'] = id
        return_list += [id_details]
    return return_list

def request_biogrid(gene_names):
    print('BIOGRID: Looking up interactions using gene names...',end="")
    df = get_interactions(gene_names=gene_names)
    print('saving...',end="")
    df.to_csv('current/data/protein_interactions/automated_biogrid_interactions.csv',index=False)
    print('done')
