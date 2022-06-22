from array import array
import requests
from core import config

def list_to_pipe_del(list):
    return "|".join(map(str,list))