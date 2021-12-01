"""A dictionary which maps (unique) names to endpoints. Keys are of type str,
values are of type Endpoint.

The ENDPOINTS dictionary must not be modified directly. To register an endpoint
invoke registerEndpoint.
"""
ENDPOINTS = {}

class Endpoint():
	
	def __init__(self, endpointName, pollingInterval):
		"""Constructs a new Endpoint with the given endpointName and
		pollingInterval.
		
		The endpointName must be of type str. The name must not be None nor the
		empty string.
		
		Keyword arguments:
			endpointName -- the name for the endpoint
			pollingInterval -- the polling interval for the endpoint, in
			milliseconds
		
		Raises:
			RuntimeError -- if the given endpointName is not of type str
			RuntimeError -- if the given endpointName is empty
			
		"""
		if not isinstance(endpointName, str):
			raise RuntimeError("endpoint name must be of type str")
		if endpointName == "":
			raise RuntimeError("endpoint name must not be empty")
		self._name = endpointName
		self._interval = pollingInterval
	
	def name(self):
		"""Returns the name of this endpoint.

		Keyword arguments:
			none
			
		Returns:
			a non-empty string which identifies the endpoint
			"""
		return self._name;
	
	def interval(self):
		"""Returns the polling interval for the endpoint, in milliseconds.
		
		Keyword arguments:
			none
		
		Returns:
			an int which represents the polling interval, in milliseconds
		"""
		return self._interval
	
	def __eq__(self, other):
		"""Returns weather other is equal to this endpoint
		
		Keyword arguments:
			other -- an Endpoint to compare to
		
		Returns:
			True, if this endpoint is equal to other, False otherwise
		"""
		return isinstance(other, Endpoint) and self._name == other._name
	
	def __hash__(self):
		"""Returns an int representation for this object.
		
		It is guaranteed that equal objects will produce the same hash value.
		This implies that invoking this method multiple times on the same
		object will produce the same result as long as the object remains
		unchanged.
		
		Keyword arguments:
			none
		
		Returns:
			an int which represents this object
		"""
		return hash(self._name)

def registerEndpoint(name, interval):
	"""Registers a new endpoint with the given name and registers it to the
	ENDPOINTS dictionary.
	
	The name must be unique, i.e. there must not be an endpoint which uses
	an equal name.
	
	The name must be of type str. The name must not be None nor the empty
	string.
	
	Keyword arguments:
		name -- the name for the endpoint
		interval -- the polling interval for the endpoint, in milliseconds
	
	Raises:
		RuntimeError -- if the given name is not of type str
		RuntimeError -- if the given name is empty
		RuntimeError -- if there is a registered endpoint with the given name
		
	"""
	e = Endpoint(name, interval)
	if e.name() in ENDPOINTS:
		raise RuntimeError("an endpoint named \"" + e.name() + "\" is already present")
	ENDPOINTS[e.name()] = e

# Register default endpoints
registerEndpoint("flightplans", 30000)
registerEndpoint("terminal", 15000)
registerEndpoint("radar", 20000)
registerEndpoint("it", 10000)
