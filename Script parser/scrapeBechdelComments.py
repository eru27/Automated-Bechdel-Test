import json
import requests
from bs4 import BeautifulSoup

B_URL = 'https://bechdeltest.com/view/'

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames


def main():
    movieList = GetMovieList()

    with open('Bechdel/allmovies.json', 'r') as bb:
        bechdelBase = json.loads(bb.read())

    for i in range(len(movieList)):
        movieList[i] = movieList[i].replace(' The', ', The')

    for movie in movieList:
        found = False
        counter = 0
        while not found and counter < len(bechdelBase):
            if bechdelBase[counter]['title'] == movie:
                found = True
            else:
                counter += 1

        if counter == len(bechdelBase):
            print(movie)
        else:
            req = requests.get(B_URL + str(bechdelBase[counter]['id']))

            soup = BeautifulSoup(req.text)

            good = soup.findAll(text = ' said:')
            bad = soup.findAll(text = ' disagreed with the rating and said:')

            if len(good) > 2 or len(bad) > 2:
                print(movie)
                print(len(good), len(bad), '\n')

main()