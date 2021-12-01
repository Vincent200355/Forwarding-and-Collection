import flightplanEntry
import radarEntry
import terminalEntry
import itEntry

def addMetaData(jsonObj):
    valResult = None
    if jsonObj[0] == "flightplan":
        valResult = flightplanEntry.validateEntry(jsonObj)
    elif jsonObj[0] == "radar":
        valResult = radarEntry.validateEntry(jsonObj)
    elif jsonObj[0] == "terminal":
        valResult = terminalEntry.validateEntry(jsonObj)
    elif jsonObj[0] == "it":
        valResult = itEntry.validateEntry(jsonObj)
    else:
        valResult = (False, [])

    return {
        # TODO set validUntil field
    }