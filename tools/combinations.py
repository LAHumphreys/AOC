import itertools
def ExtendAscending(initialValue, validValues, results):
    minValue = initialValue[-1]
    for v in validValues:
        if v >= minValue:
            results.append(initialValue + [v])
    return results

class MinValueMismatch(Exception):
    pass

class MaxValueMismatch(Exception):
    pass

class MaxValueMisCalculation(Exception):
    pass


def ExtendSetAscending(initialValues, validValues, minValue=None, maxValue = None):
    results = []
    initIsMin = False
    minValidValues = []
    maxValidValues = []
    numInitDigits = len(initialValues[0])
    maxInd = -1

    if minValue != None:
        initIsMin = True
        for v in validValues:
            if v >= minValue[numInitDigits]:
                minValidValues.append(v)

    if maxValue != None:
        maxInd = 0
        for v in validValues:
            if v <= maxValue[numInitDigits]:
                maxValidValues.append(v)


    for init in initialValues:
        if initIsMin:
            for i in range(len(init)):
                if init[i] > minValue[i]:
                    initIsMin = False
                    break

        if maxValue != None:
            while maxInd < numInitDigits:
                if init[maxInd] > maxValue[maxInd]:
                    raise MaxValueMisCalculation
                elif init[maxInd] == maxValue[maxInd]:
                    maxInd += 1
                else:
                    break

        if initIsMin and maxInd == numInitDigits:
            minMaxValidValues = []
            for v in maxValidValues:
                if v >= minValue[numInitDigits]:
                    minMaxValidValues.append(v)
            ExtendAscending(init, minMaxValidValues, results)
        elif initIsMin:
            ExtendAscending(init, minValidValues, results)
        elif maxInd == numInitDigits:
            ExtendAscending(init, maxValidValues, results)
        else:
            ExtendAscending(init, validValues, results)
    return results

def GeneratePermutations(validValues: list, choose: int):
    return [p for p in itertools.permutations(validValues, choose)]


def GenerateAscending(length: int, validValues: list, minValue = None, maxValue = None):
    if minValue != None and len(minValue) != length:
        raise MinValueMismatch()

    if maxValue != None and len(maxValue) != length:
        raise MaxValueMismatch()

    results = []
    if length > 0:
        for v in validValues:
            if minValue != None and minValue[0] > v:
                pass
            elif maxValue != None and maxValue[0] < v:
                pass
            else:
                results.append([v])
        currentLen = 1
        while currentLen < length:
            currentLen+=1
            results = ExtendSetAscending(results, validValues, minValue, maxValue)
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
