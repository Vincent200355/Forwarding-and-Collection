# Uses regular expressions
import re

# pattern (as RegExp) for each field
regExDict = {
    "observer":     r"terminal",
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

    for item in regExDict:
        # tests if the pattern matches the given object field
        if re.fullmatch(regExDict[item], str(jsonObj[item])):
            pass
        else:
            # field is invalid - will be added to list of invalid fields
            invalidFields.append(item)

    return (len(invalidFields) == 0), invalidFields


if __name__ == "__main__":
    validity = validateEntry({"observer":"terminal","level":"info","message":"The restaurant in Terminal 2 are now open"})
    print(validity)