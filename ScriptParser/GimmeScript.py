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

def CleanMovieName(movieName): #leave only letters, numbers and spaces, without special symbols
    movieName = re.sub(r'&.*?;', '', movieName)
    movieName = re.sub(r'[^\s\w]+', '', movieName)
    return movieName

def GetMoviesList():
    movieList_file = open(MOVIE_LIST, 'r') #list of movies that got 'rating 2' on Bechdel test
    movieList = movieList_file.read().split(',')
    movieList_file.close()

    ogMovieList = []
    movieListCleaned = []

    for movie in movieList: #cleaning list because of the differences in some symbols, leaving words and spaces
        cleaned = CleanMovieName(movie)
        movieListCleaned.append(cleaned)
        ogMovieList.append(movie)

    return ogMovieList, movieListCleaned #returning the original and cleaned list

def GetJson(fileName): #getting data from file that corresponds with the first letter of the movie
    currFile = open(IMSDB_BASE + fileName, 'r')
    scriptList = json.loads(currFile.read())
    currFile.close()

    return fileName, scriptList

def GetScript(fileName, url): #getting script from imsdb.com
    req = requests.get(url)
    if req.status_code != 200:
        print(req, fileName) #consol log because it usually doesn't happen
    soup = BeautifulSoup(req.text)
    script = soup.find('pre') #scripts are usually found within <pre> tag

    global UNFOUND_NUM
    if not script:
        UNFOUND_NUM += 1
        with open(LOG_UNFOUNDSCRIPT, 'a') as log:
            log.write(fileName + '\n') #making log
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
    ogMovieList, movieList = GetMoviesList() #get list of movies that got 'rating 2' on Bechdel test

    #making logs
    matched = []
    unmatched = []

    fileName = Decode(movieList[0][0]) #fileName contains the name of currently loaded file (the first letter of the movie name or # for number)
    currFile = open(IMSDB_BASE + fileName, 'r')
    scriptList = json.loads(currFile.read()) #loaded data
    currFile.close()

    for ogMovie, movie in zip(ogMovieList, movieList):
        if Decode(movie[0]) != fileName:
            fileName, scriptList = GetJson(Decode(movie[0])) #getting data from file that corresponds with the first letter of the movie
        found = False
        counter = len(scriptList) - 2 #last one was '', now is 'Zum Geburtstag' which isn't in tha base anyway so idc and I don't want to fuck up smthn
        while (not found) and (counter >= 0):
            if ogMovie == scriptList[counter]['name']: #first check if the whole movie name match
                found = True
            elif movie == CleanMovieName(scriptList[counter]['name']): #check if cleaned versions match
                found = True
            else: 
                counter -= 1
        if found:
            matched.append((ogMovie, movie, scriptList[counter]['name'], CleanMovieName(scriptList[counter]['name']))) #add match to the log
            GetScript(scriptList[counter]['name'], scriptList[counter]['script']) #download script 
        else:
            unmatched.append(ogMovie)

    print(UNFOUND_NUM) #console log

    #make logs
    with open('log', 'w') as log:
        for n in matched:
            log.write(n[0] + '\n')

    with open(LOG_MATCHED, 'w') as logMatched:
        logMatched.write(json.dumps(matched))

    with open(LOG_UNMATCHED, 'w') as logUnmatched:
        logUnmatched.write(json.dumps(unmatched))

    print(len(matched), len(unmatched)) #console log

main()