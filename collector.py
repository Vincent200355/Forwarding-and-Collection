import requests
from requests.auth import HTTPBasicAuth
import time
import configparser

def interval_converter(data):
    """Combining all services and update the intervals

    Args:
        data (list): service list

    Returns:
        list: The recreated datalist
    """

    for i in range(len(data)-1,0,-1):
        data[i][0] = data[i][0] - data[i-1][0]
    return data


def api_request(data, auth):
    """Api-request for the given service

    Args:
        data (list): single service
        auth (list): authentication data
    
    Return:
        jsonOb: jsonOb from Api-request
    """

    interval, service, url = data
    time.sleep(interval)

    return requests.get(url,
            auth = HTTPBasicAuth(auth[0], auth[1])).json()


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
m_data = interval_converter(data)

while True:
    for i in range(4):
        jsonOb = api_request(tuple(m_data[i]), auth)
        # Jsonparser fehlt hier
