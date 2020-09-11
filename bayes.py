from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import sklearn.metrics as metrics

import json
import os
import numpy 

DATA_PATH = 'ScriptParser/conversations/'
JSON_EXT = '.json'

def getMovieList(): #get movies that are found in the IMSDB base
    with open('ScriptParser/RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames

def getData():
    X = []
    movieList = getMovieList()

    for movie in movieList:
        if os.path.isfile(DATA_PATH + movie + JSON_EXT):
            with open(DATA_PATH + movie + JSON_EXT, 'r') as mc:
                convData = json.loads(mc.read())
            
            for dialogue in convData:
                currentConv = ''
                for text in dialogue['text']:
                    currentConv += text
                if not currentConv == '':
                    X.append(currentConv)
                else:
                    print(movie)
            
            print('one done')

    with open('dump.json', 'w') as dum:
        dum.write(json.dumps(X))

    return X

def main():
    X = getData()
    y = [1 for val in X]

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)

    print(len(y_test))

    y_pred = mnb.predict(X_test)

    cnf_mat = metrics.confusion_matrix(y_test, y_pred)

    print(cnf_mat)
    for line in cnf_mat:
        for smth in line:
            for k in smth:
                print(k)

    '''
    with open('idk.json', 'w') as dd:
        dd.write(json.dumps(cnf_mat))
        '''



main()
