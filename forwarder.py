import requests
from datetime import timedelta

# url to master endpoint
url = 'http://projekt.patchrequest.com:8080/'

def pushErrorData(ENDPOINT, observedAt, cause, parameter):
        """"
        Pushes an invalid json-Object with some additional information 
        given from the errorHandler to the master of the 'Analyse-Gruppe'.

        Arguments:
            ENDPOINT -- Instance of Endpoint class that contains the endpoint name 
            observedAt -- datetime that indicates when the error probably occured
            cause -- passed observationFailureCause 
            parameter -- invalid json-Object that should be pushed
        """
        observer = ENDPOINT.name()
        data = {'cause' : cause, 'parameter' : parameter}
        pload = [{'kind' : 'error', 'observer' : observer, 'observedAt' : observedAt, 'validUntil' : None, 'data' : data}]
        r = requests.post(url, data = pload)

def pushValidData(ENDPOINT, jsonObject, observedAt):
        """" 
        Pushes an valid json-Object with some additional information
        to the master of the 'Analyse-Gruppe'

        Arguments:
            ENDPOINT -- Instance of Endpoint class that contains the endpoint name and the endpoint polling interval
            observedAt -- datetime that indicates when the error probably occured
            jsonObject -- list with responses
        """
        observer = ENDPOINT.name()
        interval = ENDPOINT.interval() 
        validUntil = observedAt + timedelta(seconds=interval)
        pload = []

        for obj in jsonObject:
            pload.append({'kind' : 'entry', 'observer' : observer, 'observedAt' : observedAt, 'validUntil' : validUntil, 'data' : obj})

        r = requests.post(url, data = pload)

       