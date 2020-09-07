import json
import re

as_regex = re.compile(r'\sas\s.*')

woman_regex = re.compile(r'woman', flags = re.IGNORECASE)
female_regex = re.compile(r'female', flags = re.IGNORECASE)
lady_regex = re.compile(r'lady', flags = re.IGNORECASE)
man_regex = re.compile(r'man', flags = re.IGNORECASE)
male_regex = re.compile(r'male', flags = re.IGNORECASE)
BS_REGEX_LIST = [woman_regex, female_regex, lady_regex, man_regex, male_regex]

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames


def AmIBS(name):
    isBS = False
    for regex in BS_REGEX_LIST:
        if regex.search(name):
            isBS = True
    return isBS

with open('names/femaleNames2.txt', 'r') as female:
    femaleNames = female.read().split(',')

with open('names/maleNames2.txt', 'r') as male:
    maleNames = male.read().split(',')

movieList = GetMovieList()

gc = 1

log = open('filter.log', 'w')

for movie in movieList:
    fixedCharacters = [[],[],[]]
    try:
        with open('characters/' + movie + '.json') as charF:
            characters = json.loads(charF.read())

        for i in range(len(characters)):
            for j in range(len(characters[i])):
                #print(characters[i][j])
                characters[i][j] = as_regex.sub('', characters[i][j])
                #print(characters[i][j])

----------------------------------------------------------------------------------------------------------
        
        for femaleChar in characters[0]:
            found = False
            counter = 0
            isBS = AmIBS(femaleChar)
            while (not found) and (not isBS) and (counter < len(femaleNames)):
                '''
                if femaleChar == 'Lindsay Jamison ' and femaleNames[counter] == 'Lindsay':
                    n = re.compile(' ' + re.escape(femaleNames[counter]) + ' ', flags = re.IGNORECASE)
                    c = ' ' + femaleChar + ' '
                    print()
                    print('!!!!!!!!!!!!!!!!!!!!!')
                    print()
                    print(n, c, n.search(c), bool(n.search(c)))
                    print()
                    print('!!!!!!!!!!!!!!!!!!!!!')
                    print()
                '''
                name = re.compile(' ' + re.escape(femaleNames[counter]) + ' ', flags= re.IGNORECASE)
                if name.search(' ' + femaleChar + ' '):
                    print('yay')
                    found = True
                counter += 1

            if found:
                fixedCharacters[0].append(femaleChar)
            else:
                fixedCharacters[2].append(femaleChar)
            #print(1)

        print('f-done')

        for maleChar in characters[1]:
            found = False
            counter = 0
            while (not found) and (counter < len(maleNames)):
                name = re.compile(' ' + re.escape(maleNames[counter]) + ' ', flags = re.IGNORECASE)
                if name.search(' ' +  re.escape(maleChar) + ' '):
                    print('yay')
                    found = True
                counter += 1

            if found:
                fixedCharacters[1].append(maleChar)
            else:
                fixedCharacters[2].append(maleChar)
        
        print('m-done')

-------------------------------------------------------------------------

        log.write(str((movie, len(fixedCharacters[2]), fixedCharacters[2])))
        fixedCharacters[2] += characters[2]
    except:
        print(n.search(' ' + re.escape(femaleChar) + ' ', flags = re.IGNORECASE))
        print(movie + '\n')
    
    with open('characters/fixed/' + movie + '.json', 'w') as out:
        out.write(json.dumps(fixedCharacters))
    
    print(str(gc) + '/' + str(len(movieList)) + '\n')
    gc += 1

log.close()