import requests
from bs4 import BeautifulSoup
import re
import json

MOVIE_LIST = 'Bechdel/2ratedmovies.csv'

IMSDB_BASE = 'IMSDBBase/'

SCRIPT_BASE = 'RawScripts/'

UNFOUND_NUM = 0

LOG_UNFOUNDSCRIPT = 'RawScripts/logs/unfound'
LOG_MATCHED = 'RawScripts/logs/matched.json'
LOG_UNMATCHED = 'RawScripts/logs/unmatched.json'

def Decode(x):
    if x.isdigit():
        return '#'
    else:
        return x.upper()

def CleanMovieName(movieName):
    movieName = re.sub(r'&.*?;', '', movieName)
    movieName = re.sub(r'[^\s\w]+', '', movieName)
    return movieName

def GetMoviesList():
    movieList_file = open(MOVIE_LIST, 'r')
    movieList = movieList_file.read().split(',')
    movieList_file.close()

    ogMovieList = []
    movieListCleaned = []

    for movie in movieList:
        cleaned = CleanMovieName(movie)
        movieListCleaned.append(cleaned)
        ogMovieList.append(movie)

    return ogMovieList, movieListCleaned

def GetJson(fileName):
    currFile = open(IMSDB_BASE + fileName, 'r')
    scriptList = json.loads(currFile.read())
    currFile.close()

    return fileName, scriptList

def GetScript(fileName, url):
    req = requests.get(url)
    if req.status_code != 200:
        print(req, fileName)
    soup = BeautifulSoup(req.text)
    script = soup.find('pre')
    global UNFOUND_NUM

    if not script:
        UNFOUND_NUM += 1
        with open(LOG_UNFOUNDSCRIPT, 'a') as log:
            log.write(fileName + '\n')
    '''
    if script:
        with open(SCRIPT_BASE + fileName, 'w') as sFile:
            sFile.write(str(script))
    else:
        UNFOUND_NUM += 1
        with open(LOG_UNFOUNDSCRIPT, 'a') as log:
            log.write(fileName + '\n')
            '''
    return

def main():
    ogMovieList, movieList = GetMoviesList()

    matched = []
    unmatched = []

    fileName = Decode(movieList[0][0])
    currFile = open(IMSDB_BASE + fileName, 'r')
    scriptList = json.loads(currFile.read())
    currFile.close()

    for ogMovie, movie in zip(ogMovieList, movieList):
        if Decode(movie[0]) != fileName:
            fileName, scriptList = GetJson(Decode(movie[0]))
        found = False
        counter = len(scriptList) - 2
        while (not found) and (counter >= 0):
            if ogMovie == scriptList[counter]['name']:
                found = True
            elif movie == CleanMovieName(scriptList[counter]['name']):
                found = True
            else: 
                counter -= 1
        if found:
            matched.append((ogMovie, movie, scriptList[counter]['name'], CleanMovieName(scriptList[counter]['name'])))
            GetScript(scriptList[counter]['name'], scriptList[counter]['script'])
        else:
            unmatched.append(ogMovie)

    print(UNFOUND_NUM)

    with open('log', 'w') as log:
        for n in matched:
            log.write(n[0] + '\n')

    with open(LOG_MATCHED, 'w') as logMatched:
        logMatched.write(json.dumps(matched))

    with open(LOG_UNMATCHED, 'w') as logUnmatched:
        logUnmatched.write(json.dumps(unmatched))

    print(len(matched), len(unmatched))

main()