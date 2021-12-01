# Forwarder JSON Format

This document defines the JSON object format the Forwarding and Collection module passes to the analysis module.

### General format

Any message consists of exactly one list. The list contains one event object for every entity collected by the Forwarding and Collection module. If an endpoint provides multiple entitites to the collector, each entity will be wrapped into a separate event object.
The list may contain zero or more events. An empty list is used to indicate that there are no events to forward, but the forwarder is still active.

### Timestamps

Timestamps defined by thsi document are always a `number` which specifies the number of *milliseconds* since midnight of 1st Jan 1970 UTC. 
Note that timestamps in the original data are not translated and may use a different format.

### Event objects

There are two kinds of event objects: `entry` events and `error` events. Every event contains a string entry named `kind` , which indicates the kind of event.

### Entry events

An event of type `entry` always contains the following keys:

- `kind`: Always `"entry"`.
- `observer`: The observer which produced the entry. The value is one of `"flightplan"`, `"terminal"`, `"radar"` or `"it"`
- `observedAt`: The timestamp at which the entry was observed. If the collector receives identical entities multiple times in a row, this timestamp will remain the same and only the validity will increase.
- `validUntil`: The timestamp until which the entry is valid. An entry is considered valid until the next scheduled run of the collector for the source of the entry.
- `data`: The JSON data received by the collector. The data is valid JSON and will contain all keys expected for entries provided by the correspoinding endpoint. The data will not contain any unexpected keys. (In case of invalid JSON, missing keys or extraneous keys an appropriate error will be produced instead of an entry)

An event of type `entry` never contains any keys except those listed above.

Example:

	{
		"kind": "entry",
		"observer": "terminal",
		"observedAt": 1609459200000,
		"validUntil": 1609459201000,
		"data": {
			"level": "warning",
			"message": "Please wear your masks in the terminal and keep distance"
		}
	}

### Error events

An event of type `error` always contains the following keys:

- `kind`: Always `"error"`.
- `observer`: The observer which caused the error. The value is one of `"flightplan"`, `"terminal"`, `"radar"`, `"it"` **or `null`**.
- `observedAt`: The timestamp at which the error occurred. This may be the timestamp at which an invalid entry was observed, but this need not be the case.
- `validUntil`: Unused, always `0`. Added only to match the format expected by the analysis module.
- `data`: A JSON object which contains exactly the following keys:
	- `cause`: The cause of the error, which is one of:
		- `"ENDPOINT_UNAVAILABLE"`: An observation error that indicates that a data source endpoint is unavailable, i.e. that no TCP connection can be established.
		- `"ENDPOINT_UNRESPONSIVE"`: An observation error that indicates that a data source endpoint is reachable, i.e. a TCP connection could be established, but fails to provide a (complete) HTTP response (after some timeout defined by the collector).
		- `"MALFORMED_RESPONSE"`: An observation error that indicates that a data source endpoint is reachable, i.e. a TCP connection could be established, and responsive, i.e. it provided at least one byte worth of response, but the response cannot be parsed, because it is syntactically invalid.
	An error of this kind is detected if a HTTP response is malformed or if the JSON contained within the HTTP body is malformed. The `parameter` may contain a string that contains the invalid response that caused the error.
		- `"EXTRANEOUS_RESPONSE"`: An observation error that indicates that a data source provided a valid JSON response, but that response contained some unexpected extraneous content. This may indicate that the data format has changed, in which case the expected data format has to be updated. The `parameter` of the event will be a string that contains the full (valid) JSON that caused this error.
		- `"INTERNAL_ERROR"`: An observation error that indicates that some unexpected exceptional condition occurred. Errors of this kind may occur at any time. Errors need not be directly related to any communication to the data source or data consumer.
	- `parameter`: Additional information on the error depending on the cause or `null`  if no error detail is provided.

An event of type `error` never contains any keys except those listed above.


Example:

	{
		"kind": "error",
		"observer": null,
		"observedAt": 1609459200000,
		"validUntil": 0,
		"data": {
			"cause": "INTERNAL_ERROR",
			"parameter": null
		}
	}

## Full example

A message created by the Forwarding and Collection module may look like the following (This example can also be found in `collectionReportSample.json`):

	[
		{
			"kind": "entry",
			"observer": "flightplan",
			"observedAt": 1609459200000,
			"validUntil": 1609459201000,
			"data": {
				"callsign": "EWG8XZ",
				"ssr": "A1411",
				"rules": "IS",
				"aircraft": "A320",
				"wvc": "M",
				"equipment": "S/S",
				"origin": "LFPG",
				"eobt": 1637712000000,
				"route": "N0431F370 DH632",
				"destination": "EDDH",
				"eet": 7200000,
				"eta": 1637719200000,
				"status": "closed",
				"registration": "DAAA",
				"icao4444": "FPL-EWG8XZ/A1411-IS-A320/M-S/S-LFPG0000-N0431F370 DH632-EDDH0200-REG/DAAAA"
			}
		},
		{
			"kind": "entry",
			"observer": "terminal",
			"observedAt": 1609459200000,
			"validUntil": 1609459201000,
			"data": {
				"level": "warning",
				"message": "Please wear your masks in the terminal and keep distance"
			}
		},
		{
			"kind": "entry",
			"observer": "radar",
			"observedAt": 1609459200000,
			"validUntil": 1609459201000,
			"data": {
				"callsign": "EWG6UC",
				"date": 1637755430782,
				"lat": 9.997445,
				"lon": 53.628698,
				"alt": 0
			}
		},
		{
			"kind": "entry",
			"observer": "it",
			"observedAt": 1609459200000,
			"validUntil": 1609459201000,
			"data": {
				"name": "server-cpu-usage",
				"unit": "%",
				"value": 42
			}
		},
		{
			"kind": "error",
			"observer": "radar",
			"observedAt": 1609459200000,
			"validUntil": 0,
			"data": {
				"cause": "MALFORMED_RESPONSE",
				"parameter": "[{\"text\":\"This is not a valid JSON structure, because there is no closing bracked for the following object\"}, {]"
			}
		},
		{
			"kind": "error",
			"observer": null,
			"observedAt": 1609459200000,
			"validUntil": 0,
			"data": {
				"cause": "INTERNAL_ERROR",
				"parameter": null
			}
		}
	]
