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