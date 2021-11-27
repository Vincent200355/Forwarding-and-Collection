import requests
from requests.auth import HTTPBasicAuth
import time
import configparser
import threading

def api_request(data, auth):
    """Api-request for the given service

    Args:
        data (list): single service
        auth (list): authentication data
    
    Return:
        jsonOb: jsonOb from Api-request
    """
    interval, service, url = data
    while True:
        
        time.sleep(interval)

        json_data = service, requests.get(url,
                auth = HTTPBasicAuth(auth[0], auth[1])).json()

        #Validator aufruf fehlt
        time.sleep(0)

# -required data
#   [time-interval in sec, servicename, urls
data = [[ 10, 'IT', 'http://asm.fl.dlr.de:10001/it'],
        [ 20, 'Radar', 'http://asm.fl.dlr.de:10001/radar'],
        [ 30, 'Flightplans', 'http://asm.fl.dlr.de:10001/flightplans'],
        [ 15, 'Terminal', 'http://asm.fl.dlr.de:10001/terminal']]

# -username & password for Authentication
config = configparser.RawConfigParser()
config.read('credentials.ini')
auth = [config.get('CollectorApi', 'user'), config.get('CollectorApi', 'pass')]

data.sort()

for i in range(4):
    threading.Timer( 0,api_request,[data[i],auth]).start()
            