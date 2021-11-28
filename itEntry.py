# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
    "observer":     r"it",
    "name":         r"[a-zA-Z-]+",
    "unit":         r"(%)|(count)|(Mb/s)|(-)",
    "value":        r"[a-zA-Z0-9 <>]+"
}


def validateEntry(jsonObj):
    ''' Takes a deeper look into the fetched it object to validate its data.
    Each field is validated through a regular expression.
    :param jsonObj:     the parsed and fetched JSON object
    :return validity:   true/false depending on validation result
    '''

    invalidFields = []

    for entry in jsonObj:
        # nested for loops because of it entry structure (list)
        for item in regExDict:
            # tests if the pattern matches the given object field
            if re.fullmatch(regExDict[item], str(jsonObj[item])):
                pass
            else:
                # field is invalid - will be added to list of invalid fields
                invalidFields.append(item)

        # Integrity check of percentage values - needs to be between 0 and 100.
        if entry["unit"] == "%":
            if 0 <= int(entry["value"]) <= 100:
                pass
            else:
                invalidFields.append(entry["name"])

    return (len(invalidFields) == 0), invalidFields


if __name__ == "__main__":
    validity = validateEntry([{"observer": "it", "name":"server-cpu-usage","unit":"%","value":27},{"observer": "it","name":"server-ram-usage","unit":"%","value":21},{"observer": "it","name":"server-login-failed","unit":"count","value":91},{"observer": "it", "name":"server-login-success","unit":"count","value":1031},{"observer": "it", "name":"traffic-upload","unit":"Mb/s","value":41},{"observer": "it","name":"traffic-download","unit":"Mb/s","value":97},{"observer": "it","name":"news","unit":"-","value":"all systems running normal<br>"}])
    print(validity)