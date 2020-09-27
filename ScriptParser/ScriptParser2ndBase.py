import re
import json
import ClassifyNames
import os.path

location_regex = re.compile(r'.*\s*(?P<location>(EXT|INT).*)')
#character_regex = re.compile(r'\s{25,32}(?P<character>(([A-Z]+|\'|\.)\s?)+)')
#speech_regex = re.compile(r'\s{14,20}(?P<speech>(\w|\.|\').*)')

bs_regex = re.compile(r'(\d\d\/\d\d\/\d\d|\(CONTINUED\)|CONTINUED:|CUT TO|DISSOLVE TO)')


LOCATION_STR = 'location'
SPEECH_STR = 'speech'


location = {}
location['type'] = LOCATION_STR

speech = {}
speech['type'] = SPEECH_STR
speech['character'] = None
speech['text'] = '' #Setting up default values for writing in files

locationChanged = False 


INPUT_FILE_NAME = 'Next'
OUTPUT_FILE_NAME = 'Next'

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    movieNames2 = []
    for movie in matchedList:
        movieNames.append(movie[2]) #third member in a list is name of the movie in the IMSDB base
        movieNames2.append(movie[0])

    return movieNames, movieNames2

def compileRegex(movieName, realSpaces): #find number od spaces for line types and compile regexes ---------------radi?????????????????????
    found = False
    counter = 0
    character_regex = None
    speech_regex = None
    while (not found) and (counter < len(realSpaces)):
        if movieName == realSpaces[counter]['title']:
            found = True
            #print(counter)
            if not(realSpaces[counter]['char'] == [0, 0] and realSpaces[counter]['speech'] == [0, 0]): ################################
                character_regex = re.compile(r'\s{' + re.escape(str(realSpaces[counter]['char'][0])) + r',' + re.escape(str(realSpaces[counter]['char'][1])) + r'}(?P<character>(([A-Z]+|\'|\.)\s?)+)')
                speech_regex = re.compile(r'\s{' + re.escape(str(realSpaces[counter]['speech'][0])) + r',' + re.escape(str(realSpaces[counter]['speech'][1])) + r'}(?P<speech>(\w|\.|\').*)')
        else:
            counter += 1

    return character_regex, speech_regex


def amIBs(line):
    bo = bs_regex.search(line)
    if bo:
        return True
    else:
        return False

def cleanMe(line): #remove '\n' or ' ' from the end of line because regex also gets last \s 
    if (line[-1] is '\n') or (line[-1] is ' '):
        line = line[:-1]
    return line



def parser(movie, read, mn):
    character_regex, speech_regex = compileRegex(movie, read)

    if character_regex and speech_regex and os.path.isfile('RawScripts/new/' + mn):
        inFile = open('RawScripts/new/' + mn, 'r')
        #outFile = open('ParsedScripts/' + movie, 'w')

        parsed = {}
        parsed['title'] = movie

        parsed['script'] = []

        nameSet = set()

        line = inFile.readline()

        while line:
            if not amIBs(line):
                locationChanged = False
                if location_regex.search(line) != None:
                    location['text'] = location_regex.search(line).group('location')
                    
                    if speech['text'] != '' and (not locationChanged): #if location changed, speech is finished
                        speech['text'] = speech['text'][:-1] #last one is ' '
                        parsed['script'].append(speech.copy())
                        if speech['character']:
                            nameSet.add(speech['character'])
                        #outFile.write(str(speech)+'\n') #prolly shoud use json instead
                        speech['character'] = None
                        speech['text'] = '' #clean text because it's always appended
                        #print('one down\n')
                    
                    parsed['script'].append(location.copy())
                    #outFile.write(str(location)+'\n')
                    locationChanged = True
                    #print('one down\n')

                elif character_regex.search(line) != None:
                    if (speech['character'] != None) and not locationChanged: #if location is changed, current speech is already written
                    #otherwise, change of character means end of the last speech
                        speech['text'] = speech['text'][:-1]
                        parsed['script'].append(speech.copy())
                        nameSet.add(speech['character'])
                        #outFile.write(str(speech)+'\n')
                        speech['text'] = ''
                        #print('one down\n')
                    else:
                        locationChanged = False
                    speech['character'] = cleanMe(character_regex.search(line).group('character'))
                    #nameSet.add(speech['character'])
                    
                elif (speech_regex.search(line) != None) and (speech['character'] != None):
                    speech['text'] += cleanMe(speech_regex.search(line).group('speech')) + ' ' #speech is usually written in more lines
            line = inFile.readline()

        if (speech['character'] != None) and (speech['text'] != '') and not locationChanged: #if location is changed, current speech is already written
        #otherwise, change of character means end of the last speech
            speech['text'] = speech['text'][:-1]
            parsed['script'].append(speech.copy())
            #outFile.write(str(speech)+'\n')
            speech['text'] = ''
            #print('one down\n')

        inFile.close()

        #parsed['female'], parsed['male'], parsed['unknown'] = ClassifyNames.ClassifyNames(list(nameSet))
        parsed['characters'] = list(nameSet)

        with open('ParsedScripts/new/' + mn + '.json', 'w') as outFile:
            outFile.write(json.dumps(parsed))
    else:
        print(movie)




###################################################################
print('hi')

with open('spacelogs/reals32222.json', 'r') as f:
    readspaces = json.loads(f.read())

print('hi again')

with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/foundraw.json', 'r') as f:
    foundraw = json.loads(f.read())

for movie in foundraw[0]:
    parser(movie[2], readspaces, '2/' + movie[2])

for movie in foundraw[1]:
    parser(movie[2], readspaces, '3/' + movie[2])

#movielis, mn2 = GetMovieList()

'''
space = [{}]
space[0]['title'] = 'Romeo and Juliet'
space[0]['char'] = [25, 25]
print(space)
#space[0]['char'][0] = 25
space[0]['speech'] = [12, 12]
#space[0]['speech'][0] = 12

parser('Romeo and Juliet', space, 'Romeo and Juliet')

#parser(movielis[0], readspaces)
'''
'''
for movie, mn in zip(movielis, mn2):
    if movie != 'Ace Ventura: Pet Detective':
        parser(movie, readspaces, mn)##
        print('one done')
'''

