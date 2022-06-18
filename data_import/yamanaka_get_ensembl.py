import requests
from core import config as cfg

request_url = cfg.ENSEMBL_BASE_URL + "lookup/id/ENSG00000165029"

params = {
    "content-type":"application/json",
    'expand':0 #1 for extra info
}

r =requests.get(request_url, params=params)

print(r.json())