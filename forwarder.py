import requests

def pushData(kind, observer, observedAt, cause, parameter):
        """"
        Pushes an invalid json-Object with some additional information 
        given from the errorHandler to the master of the 'Analyse-Gruppe'.

        Arguments:
            kind -- normally always set to 'error'
            observer -- observer which probably caused an error
            observedAt -- datetime that indicates when the error probably occured
            cause -- passed observationFailureCause 
            parameter -- invalid json-Object that should be pushed
        """
        # url to master endpoint
        url = 'http://projekt.patchrequest.com:8080/'

        pload = {'kind' : kind, 'observer' : observer, 'observedAt' : observedAt, 'cause' : cause, 'parameter' : parameter}
        r = requests.post(url, data = pload)