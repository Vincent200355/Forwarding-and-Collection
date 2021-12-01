import requests
from requests.auth import HTTPBasicAuth
import time
import configparser
import threading
import endpoints 
from verifier import verifyAPIResponse

def api_request(data, auth):
    """The given data provides a time-interval, the service name and an URL for the given service.
       Sending an API request and forward the response to the verifier.

    Args:
        data (list): data from the given service
        auth (list): authentication data
    """

    interval, service, url = data
    while True:
        time.sleep(interval)

        response = requests.get(url,
                auth = HTTPBasicAuth(auth[0], auth[1])).text
        observedAt = int(round(time.time() * 1000))

        verifyAPIResponse(endpoints.ENDPOINTS[service] , response, observedAt)
        time.sleep(0)


# service data
#  --> FORMAT: [interval, service name, URL]
data = [[ 10, 'it', 'http://asm.fl.dlr.de:10001/it'],
        [ 20, 'radar', 'http://asm.fl.dlr.de:10001/radar'],
        [ 30, 'flightplans', 'http://asm.fl.dlr.de:10001/flightplans'],
        [ 15, 'terminal', 'http://asm.fl.dlr.de:10001/terminal']]


# authentication data
#  --> FORMAT: [username, password]
config = configparser.RawConfigParser()
config.read('credentials.ini')
auth = [config.get('CollectorApi', 'user'), config.get('CollectorApi', 'pass')]

for i in range(4):
    threading.Timer( 0,api_request,[data[i],auth]).start()
            