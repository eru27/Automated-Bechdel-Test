import json

GET1 = 'characters/'
GET2 = 'characters/woman/'

JSONEXT = '.json'

OUT = 'characters/fixed/'

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

def main():
    movieList = GetMovieList()
    for movie in movieList:
        with open(GET1 + movie + JSONEXT, 'r') as char:
            character = json.loads(char.read())

        with open(GET2 + movie + JSONEXT, 'r') as wom:
            woman = json.loads(wom.read())

        fixed = character
        fixed[0] = woman[0]
        fixed[2] += woman[1]

        with open(OUT + movie + JSONEXT, 'w') as fix:
            fix.write(json.dumps(fixed))

main()