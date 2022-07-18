import requests, sys
from pprint import pprint

def fetch_endpoint(server, request, params):
    r = requests.get(server+request, params)
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    return r

def fetch_endpoint_POST(server,request,params,header,data):

    r = requests.post(server+request,params=params,headers=header,data=data)

    if not r.ok:
        r.raise_for_status()
        sys.exit()
        
    return r

        