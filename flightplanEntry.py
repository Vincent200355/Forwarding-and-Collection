# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
    "observer":     r"flightplan",
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


if __name__ == "__main__":
    validity = validateEntry({"observer":"flightplan","callsign":"EWG8XZ","ssr":"A1411","rules":"IS","aircraft":"A320","wvc":"M","equipment":"S/S","origin":"LFPG","eobt":1637971200000,"route":"N0431F370 DH632","destination":"EDDH","eet":7200000,"eta":1637978400000,"status":"closed","registration":"DAAA","icao4444":"FPL-EWG8XZ/A1411-IS-A320/M-S/S-LFPG0000-N0431F370 DH632-EDDH0200-REG/DAAAA"})
    print(validity)