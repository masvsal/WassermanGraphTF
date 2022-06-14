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
