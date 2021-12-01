# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
    "level":        r"[a-zA-Z]+",
    "message":      r"[a-zA-Z0-9 .+]*"
}


def validateEntry(jsonObj):
    ''' Takes a deeper look into the fetched terminal object to validate its data.
    Each field is validated through a regular expression.
    :param jsonObj:     the parsed and fetched JSON object
    :return validity:   true/false depending on validation result
    '''

    invalidFields = []
    for entry in jsonObj:
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

    return (len(invalidFields) == 0), invalidFields
