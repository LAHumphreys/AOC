def LoadInts(file):
    result = []
    with open(file) as f:
        for l in f.readlines():
            result.append(int(l))

    return result