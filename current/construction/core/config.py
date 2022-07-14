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

AURADB_URI = data["auradb"]["uri"]
AURADB_USER = data["auradb"]["user"]
AURADB_PASSWORD = data["auradb"]["password"]

GENE2UNIPARC_URI = data['data_uri']['gene2uniparc']
GENE2UNIPROT_URI = data['data_uri']['gene2uniprot']
ALTSEQ_URI = data['data_uri']['alt_seq']

GAF_PRUNED = data['data_uri']['gaf_pruned']
PROT_SEQ = data['data_uri']['cis_bp_prot_seq']
TFCLASS = data['data_uri']['tfclass']
JASPAR_PFM = data['data_uri']['jaspar_pfm']

BIOGRID = data['data_uri']['biogrid']
STRING_ANNOTATION = data['data_uri']['string_annotation']
STRING_INTERACTIONS = data['data_uri']['string_functional_and_physical_interactions']
STRING_PHYSICAL_INTERACTIONS = data['data_uri']['string_physical_interactions']

""" print(GAF_PRUNED)
print(PROT_SEQ)
print(TFCLASS)
print(JASPAR_PFM) """
