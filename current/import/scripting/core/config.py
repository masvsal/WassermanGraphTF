"""
Load the config file and create any custom variables
that are available for ease of use purposes
"""

import yaml
import os
import sys

BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

with open(BASE_DIR + "/config/config.yml", "r") as configFile:
    data = configFile.read()

data = yaml.load(data, Loader=yaml.FullLoader)

#BIOGRID
BIOGRID_ACCESS_KEY = data["biogrid"]["access_key"]
BIOGRID_BASE_URL = data["biogrid"]["base_url"]
#JASPAR
JASPAR_BASE_URL = data["jaspar"]["base_url"]
#PFAM
#USCS Genome Browser
USCS_BASE_URL = data["uscs"]["base_url"]
#Biomart
ENSEMBL_BASE_URL = data["ensembl_biomart"]["base_url"]
#CTDbase
CTDBASE_BASE_URL = data['ctdbase']['base_url']
#STRING
STRING_BASE_URL = data['string']['base_url']

#TF Sets
GENE_NAMES = data['gene_names']
FIBROBLAST_TO_ENDOTHELIAL = data['fibroblast_to_endothelium']
FIBROBLAST_TO_NEURON = data['fibroblast_to_neuron']
FIBROBLAST_TO_THYMUS = data['fibroblast_to_thymus']
FIBROBLAST_TO_SERTOLI = data['fibroblast_to_sertoli']
FIBROBLAST_TO_HSC = data['fibroblast_to_hsc']

