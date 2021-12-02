from endpoints import Endpoint, ENDPOINTS
from errorHandler import handleError
from flightplanEntry import validateEntry as validateFlightplanEntry
from forwarder import pushValidData as forwardEntries
from itEntry import validateEntry as validateITEntry
from json import loads as parseJSON
from json.decoder import JSONDecodeError
from observationFailureCause import EXTRANEOUS_RESPONSE, MALFORMED_RESPONSE
from radarEntry import validateEntry as validateRadarEntry
from terminalEntry import validateEntry as validateTerminalEntry
from unifier import unify

def verifyAPIResponse(endpoint, response, observedAt):
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
	
	_verifyStructure(endpoint, jsonObj, observedAt)

def _verifyStructure(endpoint, jsonObj, observedAt):
	
	if endpoint == ENDPOINTS["flightplans"]:
		valid, incorrectKeys = validateFlightplanEntry(jsonObj)
	elif endpoint == ENDPOINTS["terminal"]:
		valid, incorrectKeys = validateTerminalEntry(jsonObj)
	elif endpoint == ENDPOINTS["radar"]:
		valid, incorrectKeys = validateRadarEntry(jsonObj)
	elif endpoint == ENDPOINTS["it"]:
		valid, incorrectKeys = validateITEntry(jsonObj)
	else:
		valid = false
		incorrectKeys = None
	
	if not valid:
		# handle syntax error
		p = None
		if incorrectKeys != None and len(incorrectKeys) > 0:
			p = str(incorrectKeys)
		print("Encountered an error whilst handling response of endpoint " + endpoint.name() + ":");
		print("Response was: " + str(jsonObj))
		handleError(EXTRANEOUS_RESPONSE, parameter=p, endpoint=endpoint, observedAt=observedAt)
		return
	
	print("Endpoint " + endpoint.name() + " delivered " + str(len(jsonObj)) + " " + ("entity" if len(jsonObj) == 1 else "entities"))
	
	unify(endpoint, observedAt, jsonObj)
	forwardEntries(endpoint, jsonObj, observedAt)
	
