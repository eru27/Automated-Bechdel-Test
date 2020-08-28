import re
import json
from bs4 import BeautifulSoup

bold_regex = re.compile(r'<b>')
spaces_regex = re.compile(r'(<\/b>)?(<b>)?(?P<spaces>\s*)\S+')

FILE_LOCATION = 'RawScripts/'

LOG = 'spaceLog0.log'

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[2]) #third member in a list is name of the movie in the IMSDB base

    return movieNames

def main():
    movieNames = GetMovieList() #list of movies so we can load scripts by name

    #this was made for logs
    #bolds = []
    #norms = []

    log = open(LOG, 'w')

    for movie in movieNames:
        with open(FILE_LOCATION + movie, 'r') as movieScript:
            soup = BeautifulSoup(movieScript.read())
            valid = True
            if soup.p: #there are different types of scripts, the ones with <p> tags are already parsed
                valid = False

        if valid:
            with open(FILE_LOCATION + movie, 'r') as movieScript:
                script = movieScript.readlines()
            
            #key is number of leading spaces in line, value is number of lines with that many leading spaces
            boldLines = {} #we separate bolded lines and 'normal' ones (<b> tag)
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
            b = boldLines.copy()
            n = normLines.copy()

            for key in b:
                if boldLines[key] < 500:
                    del boldLines[key]

            for key in n:
                if normLines[key] < 500:
                    del normLines[key]
            '''
            
            log.write(movie + '\n')
            log.write(str(sorted(boldLines.items())) + '\n')
            log.write(str(sorted(normLines.items())) + '\n')
            log.write('\n')

    '''
    for m, b, n in zip(movieNames, bolds, norms):
        with open(LOG, 'w') as log:
            log.write(m + '\n')
            log.write(str(b) + '\n')
            log.write(str(n) + '\n')
            log.write('\n')
    '''

main()