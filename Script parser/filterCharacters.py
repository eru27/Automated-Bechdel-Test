import json
import re

as_regex = re.compile(r'\sas\s.*')

woman_regex = re.compile(r'woman', flags = re.IGNORECASE)
female_regex = re.compile(r'female', flags = re.IGNORECASE)
lady_regex = re.compile(r'lady', flags = re.IGNORECASE)
girl_regex = re.compile(r'girl', flags = re.IGNORECASE)
man_regex = re.compile(r'man', flags = re.IGNORECASE)
male_regex = re.compile(r'male', flags = re.IGNORECASE)
guy_regex = re.compile(r'guy', flags = re.IGNORECASE)
boy_regex = re.compile(r'boy', flags = re.IGNORECASE)
#dr_regex = re.compile(r'dr', flags = re.IGNORECASE)
BS_REGEX_LIST = [woman_regex, female_regex, lady_regex, man_regex, male_regex]

FAULTY_LOG = 'characters/logs/badlymatched.log'
FOUND_LOG = 'characters/logs/hiifound.log'

TRASHOLD = 2

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

def GetNames():
    with open('names/femaleNames2.txt', 'r') as female:
        femaleNames = female.read().split(',')

    #with open('names/maleNames2.txt', 'r') as male:
    #    maleNames = male.read().split(',')

    ###############
    femaleNames += ['MRS', 'MISS']
    maleNames = []

    ###############

    return (femaleNames, maleNames)

def main():
    movieList = GetMovieList()
    ogNames = GetNames()

    gc = 1

    #log = open('filter.log', 'w')

    with open(FAULTY_LOG, 'w') as fl:
        fl.write('')

    with open(FOUND_LOG, 'w') as hif:
        hif.write('')

    for movie in movieList:
        fixedCharacters = [[],[],[]]
        try:
            with open('characters/' + movie + '.json', 'r') as charF:
                characters = json.loads(charF.read())

            for i in range(len(characters[0])):
                #print(characters[i][j])
                characters[0][i] = as_regex.sub('', characters[0][i])
                if characters[0][i][-1] == ' ':
                    characters[0][i] = characters[0][i][:-1]
                #print(characters[i][j])

    #----------------------------------------------------------------------------------------------------------
            state = 0
            trash = 0
            trashStore = [[],[]]
            for character in characters[0]:
                found = False
                counter = 0
                isBS = AmIBS(character)
                while (not found) and (not isBS) and (counter < len(ogNames[0])):
                    name = re.compile(' ' + re.escape(ogNames[0][counter]) + ' ', flags= re.IGNORECASE)
                    if name.search(r' ' + character + r' '):
                        print('yay')
                        found = True
                    counter += 1

                if found:
                    fixedCharacters[0].append(character)

                    if state == 0:
                        trash = 0
                    else:
                        trash += 1
                        trashStore[0].append(character)
                else:
                    fixedCharacters[2].append(character)

                    if state == 0:
                        trash += 1
                        trashStore[1].append(character)

                        if trash >= TRASHOLD:
                            state = 1

            with open(FAULTY_LOG, 'a') as fl:
                fl.write(movie + ', ' + str(trashStore) + ', ' + str(trash) + '\n')

            with open(FOUND_LOG, 'a') as hif:
                hif.write(str(movie) + ', ' + str(len(fixedCharacters[0])) + ', ' + str(len(fixedCharacters[2])) + '\n')

            #fixedCharacters[1] = characters[1]
            #fixedCharacters[2] += characters[2]
        except:
            print(name.search(' ' + re.escape(character) + ' ', flags = re.IGNORECASE))
            print(movie + '\n')
        

        with open('characters/woman/' + movie + '.json', 'w') as out:
            out.write(json.dumps((fixedCharacters[0], fixedCharacters[2])))
            
        '''
        with open('characters/fixed/' + movie + '.json', 'w') as out:
            out.write(json.dumps(fixedCharacters))
        '''
        
        print(str(gc) + '/' + str(len(movieList)) + '\n')
        gc += 1

    #log.close()

main()