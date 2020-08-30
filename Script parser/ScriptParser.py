import re
import json
import ClassifyNames

location_regex = re.compile(r'<b>.*\s(?P<location>(EXT|INT).*)')
#character_regex = re.compile(r'<b>\s{25,32}(?P<character>(([A-Z]+|\'|\.)\s?)+)')
#speech_regex = re.compile(r'^(?!<b>)(<\/b>)?\s{14,20}(?P<speech>(\w|\.).*)')

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
    for movie in matchedList:
        movieNames.append(movie[2]) #third member in a list is name of the movie in the IMSDB base

    return movieNames

def compileRegex(movieName, realSpaces): #find number od spaces for line types and compile regexes ---------------radi?????????????????????
    found = False
    counter = 0
    character_regex = None
    speech_regex = None
    while (not found) and (counter < len(realSpaces)):
        if movieName == realSpaces[counter]['title']:
            found = True
            character_regex = re.compile(r'<b>\s{' + re.escape(str(realSpaces[counter]['char'][0])) + r',' + re.escape(str(realSpaces[counter]['char'][1])) + r'}(?P<character>(([A-Z]+|\'|\.)\s?)+)')
            speech_regex = re.compile(r'^(?!<b>)(<\/b>)?\s{' + re.escape(str(realSpaces[counter]['speech'][0])) + r',' + re.escape(str(realSpaces[counter]['speech'][1])) + r'}(?P<speech>(\w|\.).*)')
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



def parser(movie, read):
    inFile = open('RawScripts/' + movie, 'r')
    #outFile = open('ParsedScripts/' + movie, 'w')

    parsed = {}
    parsed['title'] = movie

    parsed['script'] = []

    nameSet = set()
    
    character_regex, speech_regex = compileRegex(movie, read)
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
                
            elif speech_regex.search(line) != None:
                speech['text'] += cleanMe(speech_regex.search(line).group('speech')) + ' ' #speech is usually written in more lines
        line = inFile.readline()

    if (speech['character'] != None) and not locationChanged: #if location is changed, current speech is already written
                #otherwise, change of character means end of the last speech
                    speech['text'] = speech['text'][:-1]
                    parsed['script'].append(speech.copy())
                    #outFile.write(str(speech)+'\n')
                    speech['text'] = ''
                    #print('one down\n')

    inFile.close()

    parsed['female'], parsed['male'], parsed['unknown'] = ClassifyNames.ClassifyNames(list(nameSet))

    with open('ParsedScripts/json/' + movie, 'w') as outFile:
        outFile.write(json.dumps(parsed))

print('hi')

with open('spacelogs/realspaces.json', 'r') as f:
    readspaces = json.loads(f.read())

print('hi again')

movielis = GetMovieList()

for movie in movielis:
    if movie != 'Ace Ventura: Pet Detective':
        parser(movie, readspaces)
        print('one done')