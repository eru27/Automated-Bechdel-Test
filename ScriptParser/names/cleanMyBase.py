femaleNames_file = open('names/femaleNames.csv', 'r')
maleNames_file = open('names/maleNames.csv', 'r')

femaleNames = femaleNames_file.read().split(',')
maleNames = maleNames_file.read().split(',')

femaleNames_file.close()
maleNames_file.close()

femaleSet = set(femaleNames)
maleSet = set(maleNames)

print(len(femaleSet), len(maleSet))

intersect = femaleSet.intersection(maleSet)

femaleSet = femaleSet - intersect
maleSet = maleSet - intersect


femaleList = list(femaleSet)
maleList = list(maleSet)

femaleList.sort()
maleList.sort()

for i in range(len(femaleList)):
    femaleList[i] = femaleList[i].upper()

for j in range(len(maleList)):
    maleList[j] = maleList[j].upper()

femaleNamesCleaned = open('names/femaleNamesCleanedLC.csv', 'w')
maleNamesCleaned = open('names/maleNamesCleanedLC.csv', 'w')

femaleNamesCleaned.write(femaleList[0].replace("'", ''))
for name in femaleList[1:]:
    femaleNamesCleaned.write(',' + name.replace("'", ''))

femaleNamesCleaned.close()

maleNamesCleaned.write(maleList[0].replace("'", ''))
for name in maleList[1:]:
    maleNamesCleaned.write(',' + name.replace("'", ''))

maleNamesCleaned.close()
