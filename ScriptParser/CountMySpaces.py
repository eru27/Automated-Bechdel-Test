import re
import json
from bs4 import BeautifulSoup

MIN_TRASHOLD = 500

bold_regex = re.compile(r'<b>')
spaces_regex = re.compile(r'(<\/b>)?(<b>)?(?P<spaces>\s*)\S+')

FILE_LOCATION = 'RawScripts/'

LOG = 'spaceLog2.log'

def getMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[2]) #third member in a list is name of the movie in the IMSDB base

    return movieNames

def main(scriptName, openFile):
    #movieNames = getMovieList() #list of movies so we can load scripts by name

    #this was made for logs
    #bolds = []
    #norms = []

    #log = open(LOG, 'w')
    '''
    openFile.seek(0)
    soup = BeautifulSoup(openFile.read())
    '''
    
    valid = True
    if scriptName == 'Ace Ventura: Pet Detective':
        valid = False
    '''
    if soup.p: #there are different types of scripts, the ones with <p> tags are already parsed
        valid = False
        print(soup.p)
        print(str(valid) + '**************************************************************\n\n')
        return None
    '''

    if valid:
        openFile.seek(0)
        script = openFile.readlines()
        
        #key is number of leading spaces in line, value is number of lines with that many leading spaces
        boldLines = {} #we separate bold lines and 'normal' ones (<b> tag)
        normLines = {}
        
        for line in script:
            bold = False
            if bold_regex.search(line):
                bold = True
            spaces = spaces_regex.search(line)
            if spaces:
                num = len(spaces.group('spaces'))
                if bold:
                    if num in boldLines:
                        boldLines[num] += 1
                    else:
                        boldLines[num] = 1
                else:
                    if num in normLines:
                        normLines[num] += 1
                    else:
                        normLines[num] = 1
                '''
                if len(spaces.group('spaces')) == 16 and bold:
                    print('aaaaaaaaa\n\n\n\n' + line)
                '''
        #print(boldLines[32])

        '''
        b = boldLines.copy()
        n = normLines.copy()

        for key in b:
            if boldLines[key] < MIN_TRASHOLD:
                del boldLines[key]

        for key in n:
            if normLines[key] < MIN_TRASHOLD:
                del normLines[key]
        '''
        
        characterRange = []
        speechRange = []

        sortedBold = sorted(boldLines, key = boldLines.get, reverse = True)
        sortedNormal = sorted(normLines, key = normLines.get, reverse = True)
        
        if (sortedBold[0] >= 4):
            characterSpaces = sortedBold[0]
        elif sortedBold[1] < sortedBold[0]: #################
            characterSpaces = sortedBold[0]
        else:
            characterSpaces = sortedBold[1]

        if len(sortedNormal) > 1:
            speechSpaces = max(sortedNormal[0], sortedNormal[1])
            elseSpaces = min(sortedNormal[0], sortedNormal[1])
        else:
            speechSpaces = sortedNormal[0]
            elseSpaces = -100

        print(scriptName)
        print(characterSpaces, speechSpaces)
        print()


        characterRange.append(characterSpaces)
        speechRange.append(speechSpaces)

        if speechSpaces > characterSpaces:
            with open('spaceError', 'a') as sError:
                sError.write(scriptName + '\n')

        for bSpace in sortedBold[1:]:
            if abs(characterSpaces - bSpace) <= 5:
                characterRange.append(bSpace)

        for nSpace in sortedNormal[2:]:
            speechDistance = abs(speechSpaces - nSpace)
            elseDistance = abs(elseSpaces - nSpace)

            if (speechDistance < elseDistance) and speechDistance <= 5:
                speechRange.append(nSpace)
        
        charTuple = (min(characterRange), max(characterRange))
        speechTuple = (min(speechRange), max(speechRange))

        dick = {}

        dick['title'] = scriptName
        dick['char'] = charTuple
        dick['speech'] = speechTuple

        return dick

movies = getMovieList()

res = []

for movie in movies:
    with open('RawScripts/' + movie, 'r') as f:
        try:
            res.append(main(movie, f).copy())
        except:
            print(movie)
    
with open('spacelogs/realspaces2.json', 'w') as k:
    k.write(json.dumps(res))