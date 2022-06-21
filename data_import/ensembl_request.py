from core import config as cfg
import request

def test_connection(request):
    request.endpoint = "info/ping"
    r = request.get()
    print(r.json())


params = {
    "content-type":"application/json",
    'expand':0 #1 for extra info
}

request = request(cfg.ENSEMBL_BASE_URL, "", params)

try:
    test_connection(request)
except:
    print("unable to establish connection")