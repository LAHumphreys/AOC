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
