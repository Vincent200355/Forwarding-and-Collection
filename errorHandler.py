import time
import connection as con
from forwarder import pushErrorData as forwardError
from observationFailureCause import INTERNAL_ERROR
database = con.Connection()

def handleError(observationFailureCause, parameter=None, endpoint=None, observedAt=round(time.time() * 1000)):
	"""Handles an error by passing it to the forwarder and the database.
	
	The passed observationFailureCause must be defined by the
	observationFailureCause module. Otherwise, no exception will be risen, but
	an observationFailureCause.INTERNAL_ERROR will occur.
	
	This function will not raise any exception. Instead, if this function fails
	to handle an error which is not of type
	observationFailureCause.INTERNAL_ERROR, an error of type
	observationFailureCause.INTERNAL_ERROR will occur. If this function fails
	to report an error of type observationFailureCause.INTERNAL_ERROR, the
	error will be discarded after attempting to deliver the error message.
	
	Keyword arguments:
		observationFailureCause - a observation failure cause as defined by the
		observationFailureCause module
		parameter - a string parameter for the error, e.g. the malformed JSON
		endpoint - The endpoint which caused the error or None if the error is
		not related to a specific endpoint or the endpoint the error is related
		to cannot be detected
		string that caused a observationFailureCause.MALFORMED_RESPONSE error,
		or None if the error is not parametrized. (default: None)
		observedAt - a datetime that indicates when the error occurred.
		(default: datetime.now())
	"""
	print("An error occurred: " + str(observationFailureCause) + "(" + str(parameter) + ") " + (("for endpoint " + endpoint.name()) if endpoint != None else "for an unknown endpoint") + " at " + str(observedAt))
	try:
		database.write("error", {"observer": endpoint.name(),"observedAt":observedAt,"cause":observationFailureCause,"parameter":parameter})
		# forwardError(endpoint, observedAt, observationFailureCause, parameter)
		# Any error must be passed to the database so it can be stored persistently
	except Exception as e:
		if observationFailureCause == INTERNAL_ERROR:
			# Failed to handle unexpected error. There is nothing that can be
			# done
			print("An error occurred whilst handling an unexpected error: " + str(e))
			print("This error will be ignored")
		else:
			print("An error occurred whilst handling an error: " + str(e))
			handleError(INTERNAL_ERROR, observedAt=round(time.time() * 1000))