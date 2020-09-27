import json
import re


def CleanMovieName(mn): #leave only letters, numbers and spaces, without special symbols
    movieName = mn
    try:
        movieName = re.sub(r'&.*?;', '', movieName)
    except:
        print('!!!!!!!!!!!!!!!!!!! ', mn)
    movieName = re.sub(r'[^\s\w]+', '', movieName)
    return movieName

with open('/home/anja/Desktop/cornell movie-dialogs corpus/raw_script_urls.txt', 'r', encoding = 'latin-1') as f:
    fi = f.readlines()

for i in range(len(fi)):
    fi[i] = fi[i].split(' +++$+++ ')

print(fi[0])

with open('/home/anja/Documents/petnica2k20/ScriptParser/Bechdel/allmovies.json', 'r') as k:
    kur = json.loads(k.read())

print(kur[0])

rated2 = []
rated3 = []

print(kur[0]['rating'], kur[0]['title'], fi[0][1])

for i in range(len(kur)):
    if kur[i]['rating'] == 2:
        found = False
        counter = 0
        g = len(fi)

        tt = re.compile(r'^' + CleanMovieName(kur[i]['title']) + r'$', flags = re.IGNORECASE)

        while (not found) and counter < g:
            #if CleanMovieName(kur[i]['title']).lower() == CleanMovieName(fi[counter][1]):
            if tt.search(CleanMovieName(fi[counter][1])):
                    found = True
            else:
                    counter += 1
        if found:
            rated2.append((kur[i]['imdbid'], fi[counter][0], kur[i]['title'], fi[counter][2][:-1]))
    elif kur[i]['rating'] == 3:
        found = False
        counter = 0
        g = len(fi)

        tt = re.compile(r'^' + CleanMovieName(kur[i]['title']) + r'$', flags = re.IGNORECASE)

        while (not found) and counter < g:
            #if CleanMovieName(kur[i]['title']).lower() == CleanMovieName(fi[counter][1]):
            if tt.search(CleanMovieName(fi[counter][1])):
                    found = True
            else:
                    counter += 1
        if found:
            rated3.append((kur[i]['imdbid'], fi[counter][0], kur[i]['title'], fi[counter][2][:-1]))

print(rated2[0], rated3[0])
print(len(rated2), len(rated3))

with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/foundraw.json', 'w') as fk:
    fk.write(json.dumps((rated2, rated3)))

print('\ndone :)')