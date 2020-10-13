import json
import re

GET1 = 'characters/'
GET2 = 'characters/woman/'

JSONEXT = '.json'

OUT = 'charactersNew/fixed/'

as_regex = re.compile(r'\sas\s.*')

def getMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

def getSecMovieBase():
    with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/foundraw.json', 'r') as mov:
        ml = json.loads(mov.read())

    movieList = []

    for mo in ml[0] + ml[1]:
        movieList.append(mo[2])

    return movieList

def main():
    #movieList = getMovieList()
    movieList = getSecMovieBase()

    for movie in movieList:
        with open(GET1 + movie + JSONEXT, 'r') as char:
            character = json.loads(char.read())

        with open(GET2 + movie + JSONEXT, 'r') as wom:
            woman = json.loads(wom.read())

        fixed = [[], [], []]
        fixed[1] = character[1]
        fixed[1] += character[2]
        fixed[0] = woman[0]
        fixed[2] = woman[1]

        for i in range(3): #cleaning
            for j in range(len(fixed[i])):
                fixed[i][j] = as_regex.sub('', fixed[i][j])
                if fixed[i][j] == ' ':
                    fixed[i][j] = fixed[i][j][:-1]

        with open(OUT + movie + JSONEXT, 'w') as fix:
            fix.write(json.dumps(fixed))

main()