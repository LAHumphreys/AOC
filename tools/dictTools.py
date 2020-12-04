def buildDicts(defn):
    results = []
    thisDict = {}
    for line in defn.split("\n"):
        tokens = line.strip()
        if tokens == "":
            if len(thisDict) != 0:
                results.append(thisDict)
            thisDict = {}
        else:
            for pair in tokens.split(" "):
                parts = pair.split(":")
                if len (parts) != 2:
                    raise ValueError
                thisDict[parts[0]] = parts[1]

    if len(thisDict) != 0:
        results.append(thisDict)
    return results