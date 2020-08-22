#needs to be adjusted

import re

location_regex = re.compile(r'<b>(?P<location>.*\s(EXT|INT).*)')
character_regex = re.compile(r'<b>\s{25,32}(?P<character>(([A-Z]+|\')\s?)+)')
speech_regex = re.compile(r'^(?!<b>)(<\/b>)?\s{14,20}(?P<speech>\w.*)')

bs_regex = re.compile(r'(\d\d\/\d\d\/\d\d|\(CONTINUED\)|CONTINUED:)')


LOCATION_STR = 'location'
SPEECH_STR = 'speech'


location = {}
location['type'] = LOCATION_STR

speech = {}
speech['type'] = SPEECH_STR
speech['character'] = None
speech['text'] = '' #Setting up default values for writing in files

locationChanged = False 


INPUT_FILE_NAME = 'movies/ThreeMusketeers'
OUTPUT_FILE_NAME = 'threem'


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

def main():
    inFile = open(INPUT_FILE_NAME, 'r') #still works with const as name
    outFile = open(OUTPUT_FILE_NAME, 'w')

    line = inFile.readline()

    while line:
        if not amIBs(line):
            if location_regex.search(line) != None:
                location['text'] = location_regex.search(line).group('location')
                
                if speech['text'] != '': #if location changed, speech is finished
                    speech['text'] = speech['text'][:-1] #last one is ' '
                    outFile.write(str(speech)+'\n') #prolly shoud use json instead
                    speech['text'] = '' #clean text because it's always appended
                    print('one down\n')
                
                outFile.write(str(location)+'\n')
                locationChanged = True
                print('one down\n')

            if character_regex.search(line) != None:
                if (speech['character'] != None) and not locationChanged: #if location is changed, current speech is already written
                #otherwise, change of character means end of the last speech
                    speech['text'] = speech['text'][:-1]
                    outFile.write(str(speech)+'\n')
                    speech['text'] = ''
                    print('one down\n')
                else:
                    locationChanged = False
                speech['character'] = cleanMe(character_regex.search(line).group('character'))
                
            if speech_regex.search(line) != None:
                speech['text'] += cleanMe(speech_regex.search(line).group('speech')) + ' ' #speech is usually written in more lines
        line = inFile.readline()

    inFile.close()
    outFile.close()

main()