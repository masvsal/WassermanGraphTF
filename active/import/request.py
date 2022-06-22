import requests

class Request:
    def __init__(self, base_url, endpoint, params):
        self.base_url = base_url
        self.endpoint = endpoint
        self.params = params
    def get(self):
        return requests.get(self.base_url + self.endpoint, params=self.params)