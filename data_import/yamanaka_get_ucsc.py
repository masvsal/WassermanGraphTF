import requests
from core import config as cfg


request_url = cfg.USCS_BASE_URL + "/list/tracks"

params = {
    'genome':'',
    'hubURL':''
}

r = requests.get(request_url,params)