from datetime import datetime;

def handleError(observationFailureCause, parameter=None, observedAt=datetime.now()):
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
		string that caused a observationFailureCause.MALFORMED_RESPONSE error,
		or None if the error is not parametrized. (default: None)
		observedAt - a datetime that indicates when the error occurred.
		(default: datetime.now())
	"""
	# TODO implement
	# Any error must be passed to the forwarder so it can be forwarded to the alerting component
	# Any error must be passed to the database so it can be stored persistently
	print("An error occurred: " + str(observationFailureCause) + "(" + str(parameter) + ") at " + str(observedAt))
