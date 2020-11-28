def ExtendAscending(initialValue, validValues, results):
    minValue = initialValue[-1]
    for v in validValues:
        if v >= minValue:
            results.append(initialValue + [v])
    return results

def ExtendSetAscending(initialValues, validValues):
    results = []
    for init in initialValues:
        ExtendAscending(init, validValues, results)
    return results

class MinValueMismatch(Exception):
    pass

def GenerateAscending(length: int, validValues: list, minValue = None):
    if minValue != None and len(minValue) != length:
        raise MinValueMismatch()

    results = []
    if length > 0:
        for v in validValues:
            if minValue != None and minValue[0] > v:
                continue
            results.append([v])
        currentLen = 1
        while currentLen < length:
            currentLen+=1
            results = ExtendSetAscending(results, validValues)
    return results

def Generate(length: int, validValues: list, consecutiveRepeats=0):
    results = []
    if length > 0:
        for v in validValues:
            results.append([v])

        i = 1
        while i < length:
            new_results = []
            for header in results:
                for v in validValues:
                    new_results.append(header + [v])
            results = new_results
            i+=1

        if consecutiveRepeats > 0:
            new_results = []
            for result in results:
                repeated = 0
                i = 1
                while repeated < consecutiveRepeats and i < length:
                    if result[i - 1 - repeated] == result[i]:
                        repeated +=1
                    else:
                        repeated=0
                    i+=1
                if repeated >= consecutiveRepeats:
                    new_results.append(result)

            results = new_results

    return results
