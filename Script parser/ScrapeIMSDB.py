import requests
from bs4 import BeautifulSoup
import re
import json

URL = 'https://www.imsdb.com/alphabetical/'
INDEX = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

movie_regex = re.compile(r'<a href="(?P<link>\/Movie Scripts\/.*?html)".*?>(?P<name>.*?)<\/a>')


for letter in INDEX:
    req = requests.get(URL + letter)
    soup = BeautifulSoup(req.text)
    tags = soup.find_all('a')

    movie = {}
    movie_list = []

    f = open('IMSDBBase/take2/' + letter, 'w')

    for tag in tags:
        reg = movie_regex.search(str(tag))
        if reg != None:
            movie['name'] = reg.group('name').replace('&amp;', '&')
            movie['link'] = 'https://www.imsdb.com' + reg.group('link').replace('&amp;', '&')
            movie['script'] = 'https://www.imsdb.com/scripts/' + reg.group('name').replace(':', '').replace(' ', '-').replace('&amp;', '&') + '.html'
            movie_list.append(movie.copy())
            print('one gone')
    f.write(json.dumps(movie_list))
    f.close()