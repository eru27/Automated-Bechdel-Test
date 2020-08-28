FEMALE_NAMES = 'names/femaleNamesCleaned.csv'
MALE_NAMES = 'names/maleNamesCleaned.csv'

def ClassifyNames(namesList):
    with open(FEMALE_NAMES, 'r') as femaleFile:
        femaleBase = femaleFile.read().split(',')
    with open(MALE_NAMES, 'r') as maleFile:
        maleBase = maleFile.read().split(',')
    femaleList = []
    maleList = []
    unknownList = []
    for name in namesList:
        if name in femaleBase:
            femaleList.append(name)
        elif name in maleBase:
            maleList.append(name)
        else:
            unknownList.append(name)
    return femaleList, maleList, unknownList