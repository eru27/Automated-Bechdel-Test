import json
import re

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

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
        
        for femaleChar in characters[0]:
            found = False
            counter = 0
            while (not found) and (counter < len(femaleNames)):
                if re.search(' ' + re.escape(femaleNames[counter]) + ' ', ' ' + re.escape(femaleChar) + ' ', flags = re.IGNORECASE):
                    if femaleChar == 'Female Jogger ':
                        print(femaleNames[counter])
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
                if re.search(' ' + re.escape(maleNames[counter]) + ' ', ' ' +  re.escape(maleChar) + ' ', flags = re.IGNORECASE):
                    found = True
                counter += 1

            if found:
                fixedCharacters[1].append(maleChar)
            else:
                fixedCharacters[2].append(maleChar)
        
        print('m-done')

        log.write(str((movie, len(fixedCharacters[2]), fixedCharacters[2])))
        fixedCharacters[2] += characters[2]
    except:
        print(movie + '\n')
    
    with open('characters/fixed/' + movie + '.json', 'w') as out:
        out.write(json.dumps(fixedCharacters))
    
    print(str(gc) + '/' + str(len(movieList)) + '\n')
    gc += 1

log.close()