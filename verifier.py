from endpoints import Endpoint, ENDPOINTS
from errorHandler import handleError
from json import loads as parseJSON
from json.decoder import JSONDecodeError
from observationFailureCause import MALFORMED_RESPONSE

def verifyAPIResponse(endpoint, response):
	"""Parses and verifies the given response of the given endpoint and passes
	it to the next stage.
	
	If the response is valid, it will be passed on to the unifier. Otherwise,
	an error is passed to the errorHandler.
	
	The name must be of type str. The name must not be None nor the empty
	string.
	
	Keyword arguments:
		endpoint -- the endpoint (of type Endpoint) which produced the response
		response -- the response str
	"""
	
	if not isinstance(response, str):
		print("Cannot handle an API response of type " + type(response))
		handleError(INTERNAL_ERROR);
		return;
	try:
		jsonObj = parseJSON(response)
	except JSONDecodeError:
		handleError(MALFORMED_RESPONSE, parameter=response);
		return;
	
	_verifyStructure(endpoint, jsonObj)

def _verifyStructure(endpoint, jsonObj):
	# TODO verify that endpoint is an expected endpoint
	# TODO verify structure of jsonObj with respect to endpoint and pass results to the unifier
	pass
