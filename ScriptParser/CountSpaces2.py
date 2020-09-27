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
    openFile.seek(0)
    script = openFile.readlines()
    
    #key is number of leading spaces in line, value is number of lines with that many leading spaces
    normLines = {}
    
    for line in script:
        spaces = spaces_regex.search(line)
        if spaces:
            num = len(spaces.group('spaces'))
            if num in normLines:
                normLines[num] += 1
            else:
                normLines[num] = 1
    
    characterRange = []
    speechRange = []

    sortedNormal = sorted(normLines, key = normLines.get, reverse = True)
    
    if len(sortedNormal) < 3:
        characterRange = [0,0]
        speechRange = [0,0]
    else:
        
        cr  = max(sortedNormal[0], sortedNormal[1], sortedNormal[2])
        sr = sortedNormal[0] + sortedNormal[1] + sortedNormal[2] - cr - min(sortedNormal[0], sortedNormal[1], sortedNormal[2])
        characterRange = [cr, cr]
        speechRange = [sr, sr]

    dick = {}
    dick['title'] = scriptName
    dick['char'] = characterRange
    dick['speech'] = speechRange

    return dick


res = []

with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/foundraw.json', 'r') as f:
    foundraw = json.loads(f.read())

for movie in foundraw[0]:
    try:
        with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/new/2/' + movie[2]) as fil:
            try:
                res.append(main(movie[2], fil).copy())
            except:
                print(movie[2])
    except:
        print(movie)

for movie in foundraw[1]:
    try:
        with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/new/3/' + movie[2]) as fil:
            try:
                res.append(main(movie[2], fil).copy())
            except:
                print(movie[2])
    except:
        print(movie)

    
with open('spacelogs/reals32222.json', 'w') as k:
    k.write(json.dumps(res))