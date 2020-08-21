import re
import json
from bs4 import BeautifulSoup

bold_regex = re.compile(r'<b>')
spaces_regex = re.compile(r'(?P<spaces>\s*).*')

FILE_LOCATION = 'RawScripts/'

LOG = 'spaceLog.log'

def GetMovieList():
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[2])

    return movieNames

def main():
    movieNames = GetMovieList()
    bolds = []
    norms = []

    for movie in movieNames:
        with open(FILE_LOCATION + movie, 'r') as movieScript:
            soup = BeautifulSoup(movieScript.read())
            valid = True
            if soup.p:
                valid = False

        if valid:
            with open(FILE_LOCATION + movie, 'r') as movieScript:
                script = movieScript.readlines()
            
            boldLines = {}
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
            bolds.append(dict(sorted(boldLines.items())))
            norms.append(dict(sorted(normLines.items())))

    for m, b, n in zip(movieNames, bolds, norms):
        with open(LOG, 'w') as log:
            log.write(m + '\n')
            log.write(str(b) + '\n')
            log.write(str(n) + '\n')
            log.write('\n')

main()