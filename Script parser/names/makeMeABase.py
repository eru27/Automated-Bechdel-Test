path = 'names/names/yob'
ext = '.txt'

female = []
male = []

for i in range(1880,2018):
    with open(path + str(i) + ext, 'r') as openFileObject:
        for line in openFileObject:
            current = line[:-1].split(',')
            if (current[1] == 'F') and (current[0] not in female) and (int(current[2]) > 499):
                female.append(current[0])
            elif (current[0] not in male) and (int(current[2]) > 499):
                male.append(current[0])
    openFileObject.close()
    print(i, '\n')

female.sort()
male.sort()

fe = open('femaleNames2.txt', 'w')

fe.write(female[0].replace("'",''))
for name in female[1:]:
    fe.write(',' + name.replace("'", ''))

fe.close()

ma = open('maleNames2.txt', 'w')

ma.write(male[0].replace("'", ''))
for name in male[1:]:
    ma.write(',' + name.replace("'", ''))

ma.close()