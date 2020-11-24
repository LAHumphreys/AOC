def LoadInts(file):
    result = []
    with open(file) as f:
        for l in f.readlines():
            result.append(int(l))

    return result

def LoadIntList(file):
    result = []
    with open(file) as f:
        for tok in f.read().split(","):
            result.append(int(tok))

    return result


def LoadLists(file):
    result = []
    with open(file) as f:
        for lin in f.readlines():
            if lin[-1] == "\n":
                lin = lin[0:-1]
            working = []
            for tok in lin.split(","):
                working.append(tok)
            result.append(working)

    return result
