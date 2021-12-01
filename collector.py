import requests
from requests.auth import HTTPBasicAuth
import time
import configparser
import threading
import endpoints 
from verifier import verifyAPIResponse

def api_request(data, auth):
    """1. Api-request for the given service
       2. call verifier

    Args:
        data (list): single service
        auth (list): authentication data
    
    Return:
        jsonOb: jsonOb from Api-request
    """
    interval, service, url = data
    while True:
        time.sleep(interval)

        json_data = requests.get(url,
                auth = HTTPBasicAuth(auth[0], auth[1])).text

        verifyAPIResponse(endpoints.ENDPOINTS[service] , json_data)
        time.sleep(0)

# -required data
#   [time-interval in sec, servicename, urls
data = [[ 10, 'it', 'http://asm.fl.dlr.de:10001/it'],
        [ 20, 'radar', 'http://asm.fl.dlr.de:10001/radar'],
        [ 30, 'flightplans', 'http://asm.fl.dlr.de:10001/flightplans'],
        [ 15, 'terminal', 'http://asm.fl.dlr.de:10001/terminal']]

# -username & password for Authentication
config = configparser.RawConfigParser()
config.read('credentials.ini')
auth = [config.get('CollectorApi', 'user'), config.get('CollectorApi', 'pass')]

for i in range(4):
    threading.Timer( 0,api_request,[data[i],auth]).start()
            