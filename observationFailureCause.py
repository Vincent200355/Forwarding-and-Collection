"""An observation error that indicates that a data source endpoint is
unavailable, i.e. that no TCP connection can be established.

Errors of this kind are detected by the collector.

Do note that the provided API endpoints are unable to use HTTPS. Therefore,
no certificate validation can occur and no corresponding error case is defined.
"""
ENDPOINT_UNAVAILABLE = "ENDPOINT_UNAVAILABLE"

"""An observation error that indicates that a data source endpoint is
reachable, i.e. a TCP connection could be established, but fails to provide a
(complete) HTTP response (after some timeout defined by the collector).

The collector may, after receiving a partial response, reject the response as
MALFORMED_RESPONSE instead of using ENDPOINT_UNRESPONSIVE.

Errors of this kind are detected by the collector.
"""
ENDPOINT_UNRESPONSIVE = "ENDPOINT_UNRESPONSIVE"

"""An observation error that indicates that a data source endpoint is
reachable, i.e. a TCP connection could be established, and responsive, i.e.
it provided at least one byte worth of response, but the response cannot be
parsed, because it is syntactically invalid.

An error of this kind is detected if a HTTP response is malformed or if the
JSON contained within the HTTP body is malformed.

In case of malformed HTTP, errors of this kind are detected by the collector.
In case of malformed JSON, errors of this kind are detected by the verifier.
"""
MALFORMED_RESPONSE = "MALFORMED_RESPONSE"

"""An observation error that indicates that a data source provided a valid JSON
response, but that response contained some unexpected extraneous content. This
may indicate that the data format has changed, in which case the expected data
format has to be updated.

Errors of this kind are detected by the verifier.
"""
EXTRANEOUS_RESPONSE = "EXTRANEOUS_RESPONSE"

"""An observation error that indicates that some unexpected exceptional
condition occurred. Errors of this kind may occur at any time. Errors need not
be directly related to any communication to the data source or data consumer.

Errors of this kind may be detected by any component.
"""
INTERNAL_ERROR = "INTERNAL_ERROR"
