# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
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
            try:
                if re.fullmatch(regExDict[item], str(entry[item])):
                    pass
                else:
                    # field is invalid - will be added to list of invalid fields
                    invalidFields.append(item)
            except KeyError:
                invalidFields.append(item)

        # Integrity check of percentage values - needs to be between 0 and 100.
        if entry["unit"] == "%":
            if 0 <= int(entry["value"]) <= 100:
                pass
            else:
                invalidFields.append(entry["name"])

    return (len(invalidFields) == 0), invalidFields
