import json
import re

def getFullMBase():
    with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/allmwc.json', 'r') as am:
        movieList = json.loads(am.read())

    return movieList

