from bs4 import BeautifulSoup
import json

with open('RawScripts/logs/matched.json', 'r') as f:
    slist = json.loads(f.read())

for movie in slist:
    with open('RawScripts/' + movie[2], 'r') as m:
        soup = BeautifulSoup(m.read())
        if soup.br or soup.p:
            ok = True
        else:
            ok = False

    if ok:
        m1 = open('RawScripts/' + movie[2], 'r')
        mc = open('RawScripts/clean/' + movie[2], 'w')

        script = m1.readlines()

        for line in script:
            mc.write(line.replace('<br>', '').replace('<p>', '').replace('</p>', ''))

        m1.close()
        mc.close()