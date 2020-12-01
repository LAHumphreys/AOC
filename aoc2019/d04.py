from tools.combinations import GenerateAscending

def validValue(val, reqdRun=None):
    valid = False
    gotReqd = False

    if reqdRun is None:
        gotReqd = True

    if len(val) == 6:
        last = val[0]
        run = 1
        longestRun = 1
        for v in val[1:]:
            if v == last:
                run += 1
            elif v < last:
                return False
            else:
                if run > longestRun:
                    longestRun = run
                if run == reqdRun:
                    gotReqd = True
                run = 1
            last = v

        if run > longestRun:
            longestRun = run

        if run == reqdRun:
            gotReqd = True

        if longestRun >= 2 and gotReqd:
            valid = True

    return valid

def validValue2(val):
    return validValue(val, reqdRun=2)

if __name__ == "__main__":
    minValue = [1,5,3,5,1,7]
    maxValue = [6,3,0,3,9,5]
    numPart1 = 0
    numPart2 = 0
    for g in GenerateAscending(6, [1,2,3,4,5,6,7,8,9], minValue=minValue, maxValue=maxValue):
        if validValue(g):
            numPart1 += 1

        if validValue2(g):
            numPart2 += 1

    print("Part 1: {0}".format(numPart1))
    print("Part 2: {0}".format(numPart2))
