import requests
from requests.auth import HTTPBasicAuth
import time
import configparser
import threading
import endpoints 
from errorHandler import handleError
from observationFailureCause import INTERNAL_ERROR
from traceback import print_exception
from verifier import verifyAPIResponse

def thread_run(data, auth):
	while True:
		try:
			api_request(data, auth)
		except BaseException as e:
			handleError(INTERNAL_ERROR)
			if isinstance(e, Exception):
				print("Encountered an uncaught exception:")
				print_exception(e)
				if hasattr(e, "verifierCtx") and isinstance(e.verifierCtx, dict):
					ctx = e.verifierCtx
					del e.verifierCtx
					print("Context:")
					keys = ctx.keys()
					if len(keys) > 0:
						for key in keys:
							print("\t" + key + ": " + str(ctx[key]))
					else:
						print("<no information>")
					print("Attempting to continue.")
					print()
					print()
				else:
					print("The exception does not seem to be caused by response verification. The current thread will exit.")
					return
			else:
				if isinstance(e, KeyboardInterrupt) or isinstance(e, SystemExit) or isinstance(e, GeneratorExit):
					raise e
				print("Encountered a fatal uncaught exception:")
				print_exception(e)
				print("The current thread will exit.")
				return

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
    threading.Timer( 0,thread_run,[data[i],auth]).start()
            