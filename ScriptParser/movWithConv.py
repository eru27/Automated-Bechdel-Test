#izvuce filmove u kojima su nadjeni razgovori

import json
import os

def getFullMBase():
    with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/allmov.json', 'r') as am:
        movieList = json.loads(am.read())

    return movieList

def getConversation(convData):
    data = []
    for dialogue in convData:
        currentConv = ''
        for line in dialogue['text']:
            currentConv += line
        if not currentConv == '':
            data.append(currentConv)
    
    return data

movieList = getFullMBase()
newList = [[], []]

for movie in movieList[0]: ###################
    if os.path.isfile('ScriptParser/conversations/2/' + movie + '.json'):
        with open('ScriptParser/conversations/2/' + movie + '.json', 'r') as mc:
            convData = json.loads(mc.read())
        
        conversations = getConversation(convData)
        if conversations:
            if movie not in newList[0]:
                newList[0].append(movie)
        else:
            print(movie + " no conv :'(")

for movie in movieList[1]: ###################
    if os.path.isfile('ScriptParser/conversations/3/' + movie + '.json'):
        with open('ScriptParser/conversations/3/' + movie + '.json', 'r') as mc:
            convData = json.loads(mc.read())
        
        conversations = getConversation(convData)
        if conversations:
            if movie not in newList[1]:
                newList[1].append(movie)
        else:
            print(movie + " no conv :'(")

with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/allmwc.json', 'w') as f:
    f.write(json.dumps(newList))

print(len(movieList[0]), len(movieList[1]))
print(len(newList[0]), len(newList[1]))