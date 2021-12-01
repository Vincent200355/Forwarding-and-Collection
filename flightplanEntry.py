# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
    "callsign":     r"[A-Z0-9]*",
    "ssr":          r"[A-Z][A-Z0-9]*",
    "rules":        r"[A-Z][A-Z0-9]*",
    "aircraft":     r"[A-Z][A-Z0-9]*",
    "wvc":          r"[A-Z]+",
    "equipment":    r"[A-Z/]+",
    "origin":       r"[A-Z]+",
    "eobt":         r"[0-9]+",
    "route":        r"[A-Z0-9 ]+",
    "destination":  r"[A-Z]+",
    "eet":          r"[0-9]+",
    "eta":          r"[0-9]+",
    "status":       r"[a-zA-Z]+",
    "registration": r"[A-Z]+",
    "icao4444":     r"[A-Z0-9/\- ]+"
}


def validateEntry(jsonObj):
    ''' Takes a deeper look into the fetched flightplan object to validate its data.
    Each field is validated through a regular expression.
    :param jsonObj:     the parsed and fetched JSON object
    :return validity:   true/false depending on validation result
    '''

    invalidFields = []

    for item in regExDict:
        # tests if the pattern matches the given object field
        if re.fullmatch(regExDict[item], str(jsonObj[item])):
            pass
        else:
            # field is invalid - will be added to list of invalid fields
            invalidFields.append(item)

    return (len(invalidFields) == 0), invalidFields
