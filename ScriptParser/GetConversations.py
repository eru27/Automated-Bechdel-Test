import json
import re

SCRIPTS_PATH = 'ParsedScripts/'
CHARACTERS_PATH = 'characters/fixed/'

OUT = 'conversations/'

woman_regex = re.compile(r'woman', flags = re.IGNORECASE)
female_regex = re.compile(r'female', flags = re.IGNORECASE)
lady_regex = re.compile(r'lady', flags = re.IGNORECASE)
girl_regex = re.compile(r'girl', flags = re.IGNORECASE)

fem_reg_list = [woman_regex, female_regex, lady_regex, girl_regex]

def getMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

def classifyNames(nameList, charList):
    namesDict = {}
    femnamescount = 0
    for name in nameList:
        name_regex = re.compile(r' ' + re.escape(name) + r' ', flags = re.IGNORECASE)
        clase = -1
        for regex in fem_reg_list:
            if regex.search(name):
                clase = 2
        if clase == -1:
            for i in range(3):
                found = False
                counter = 0
                while not found and counter < len(charList[i]):
                    if name_regex.search(r' ' + charList[i][counter] + r' '):
                        found = True
                        clase = i
                    counter += 1

        if clase == 0:
            femnamescount += 1
            namesDict[name] = 0
        elif clase == 2:
            namesDict[name] = 2
        else:
            namesDict[name] = 1
    print(femnamescount, '\n')
    return namesDict

'''
def IsCharFemale(name, charList):
    name_regex = re.compile(' ' + re.escape(name) + ' ', flags = re.IGNORECASE)
    found = False
    counter = 0

    counter = 0
    while not found and counter < len(charList[0]):
        if name_regex.search(' ' + charList[0][counter] + ' '):
            found = True
        counter += 1

    counter = 0
    while found and counter < len(charList[1]):
        if name_regex.search(' ' + charList[1][counter] + ' '):
            found = False
        counter += 1

    counter = 0
    while found and counter < len(charList[2]):
        if name_regex.search(' ' + charList[2][counter] + ' '):
            found = False
        counter += 1
    
    if found:
        print('horrayy')
    return found
'''

def main():
    movieList = getMovieList()

    for movie in movieList:
        print(movie)
        Convos = []

        with open(SCRIPTS_PATH + movie + '.json', 'r') as scr:
            script = json.loads(scr.read())

        with open(CHARACTERS_PATH + movie + '.json', 'r') as ch:
            charList = json.loads(ch.read())

        character = classifyNames(script["characters"], charList)
        convo = {}
        femConv = True
        convo["characters"] = []
        convo["text"] = []

        if movie == 'Wild Wild West':
            print(character)

        for line in script["script"]:
            #print(line)
            if line["type"] == 'speech' and line["character"] and femConv:
                if line["character"] in character:
                    if character[line["character"]] == 0 or character[line["character"]] == 2:
                        if character[line["character"]] == 0:
                            if line["character"] not in convo["characters"]:
                                convo["characters"].append(line["character"])
                        convo["text"].append(line["text"])
                    else:
                        if len(convo["characters"]) > 1:
                            print('found')################
                            Convos.append(convo.copy())
                        femConv = False
                else:
                    print('Not found char ', line["character"], 'in ', movie, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            elif line["type"] == 'location':
                if femConv and len(convo["characters"]) > 1:
                    print('found')################
                    Convos.append(convo.copy())
                #else: #################
                #    print('notfound')################3
                
                femConv = True
                convo["characters"] = []
                convo["text"] = []

        #print(character)

        if Convos:
            #print('one gone\n')
            with open(OUT + movie + '.json', 'w') as outf:
                outf.write(json.dumps(Convos))
                
        else:
            if movie == '25th Hour':
                print(character)
            print(movie + ' none :(\n')



main()