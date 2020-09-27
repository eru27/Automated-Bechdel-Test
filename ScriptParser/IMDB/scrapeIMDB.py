import requests
import json
from bs4 import BeautifulSoup
import re
import os

URL = 'https://www.imdb.com/title/tt'
OUT = 'characters/'
CASTURL = '/fullcredits?ref_=tt_cl_sm#cast'

def GetMovieList(): #get movies that are found in the IMSDB base
    with open('RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

def getBechdelBase():
    with open('Bechdel/allmovies.json', 'r') as bechdel:
        base = json.loads(bechdel.read())
    
    movieNames = GetMovieList()
    imdbIds = []

    for movie in movieNames:
        for dic in base:
            if dic['title'].replace(',', '') == movie:
                imdbIds.append((movie, dic['imdbid']))
    print(len(imdbIds))
    return imdbIds

def getGender(url):
    req = requests.get('https://www.imdb.com' + url)
    if req.status_code != 200:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(url + '\n')
        return 2
    else:
        soup = BeautifulSoup(req.text)
        data = json.loads(soup.find('script', type = "application/ld+json").text)
        jobs = []
        #print(data['jobTitle'])
        try:
            if type(data['jobTitle']) is list:
                jobs = data['jobTitle']
            else:
                jobs.append(data['jobTitle'])
        except:
            return 2


        #print(jobs)
        if 'Actress' in jobs:
            #print('Actress')
            return 0
        elif 'Actor' in jobs:
            #print('Actor')
            return 1
        else:
            return 2

def main():
    base = getBechdelBase()
    counter = 6
    for movie in base[5:]:
        if not os.path.isfile('characters/' + movie[0] + '.json'):
            print('hi, me stuck')
            female = []
            male = []
            unknown = []
            
            #f = open('IMDB/' + movie[0], 'w')

            fullcast = requests.get(URL + movie[1] + CASTURL)
            fullcast_soup = BeautifulSoup(fullcast.text, 'lxml')
            tags = fullcast_soup.find_all('td', {"class": "primary_photo"})
            #print('hi')
            for tag in tags:
                print('1')
                persUrl = tag.find_parent('tr').find_all(recursive = False)[1].find('a')['href']
                print('2')
                gender = getGender(persUrl)
                print('3')
                charName = tag.find_parent('tr').find_all(recursive = False)[3].text
                print('4')
                charName = re.sub(r'&.*?;', '', charName)
                charName = re.sub(r'[^\s\w]+', '', charName)
                charName = re.sub(r'uncredited', '', charName)
                charName = re.sub('\n', '', charName)
                charName = re.sub(r'\s\s', '', charName)
                #print(charName)
                if charName:
                    if charName[-1] == '':
                        charName = charName[:-1]
                    #print(charName)
                    if gender == 0:
                        female.append(charName)
                    elif gender == 1:
                        male.append(charName)
                    else:
                        unknown.append(charName)
                    #f.write(str(tag.find_parent('tr').find_all(recursive = False)[3]))

            #f.close()
            print('\n' + movie[0])
            with open('characters/' + movie[0] + '.json', 'w') as f:
                f.write(json.dumps((female, male, unknown)))
            print(counter, '/', len(base))
        counter += 1
        
    print('done :)')

#main()

print(getGender('https://www.imdb.com/title/tt0118623/'))