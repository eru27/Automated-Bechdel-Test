FEMALE_NAMES = 'names/femaleNamesCleanedLC.csv'
MALE_NAMES = 'names/maleNamesCleanedLC.csv'

def ClassifyNames(namesList):
    with open(FEMALE_NAMES, 'r') as femaleFile:
        femaleBase = femaleFile.read().split(',')
    with open(MALE_NAMES, 'r') as maleFile:
        maleBase = maleFile.read().split(',')
    femaleList = []
    maleList = []
    unknownList = []
    for name in namesList:
        '''
        if name == 'LUIGI':
            print(name)
            '''
        if name.split(' ')[0] in femaleBase:
            #print(name)
            femaleList.append(name)
        elif name.split(' ')[0] in maleBase:
            #print(name)
            maleList.append(name)
        else:
            unknownList.append(name)
    return femaleList, maleList, unknownList