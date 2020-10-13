from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import sklearn.metrics as metrics

from rake_nltk import Rake

import json
import os
import numpy 
import math
import random

DATA_PATH = 'ScriptParser/conversations/'
JSON_EXT = '.json'

'''
def getMovieList(): #get movies that are found in the IMSDB base
    with open('ScriptParser/RawScripts/logs/matched.json', 'r') as matched:
        matchedList = json.loads(matched.read())
    movieNames = []
    for movie in matchedList:
        movieNames.append(movie[0]) #third member in a list is name of the movie in the Bechdel base

    return movieNames
'''

def getFullMBase():
    with open('/home/anja/Documents/petnica2k20/ScriptParser/RawScripts/logs/allmwc.json', 'r') as am:
        movieList = json.loads(am.read())

    return movieList

def getConversation(convData):
    data = []
    for dialogue in convData:
        currentConv = ''
        for line in dialogue['text']:
            currentConv += line
        if not currentConv == '':
            ####
            '''
            r = Rake()
            r.extract_keywords_from_text(currentConv)
            lis = r.get_ranked_phrases()
            cc = lis[0]
            for word in lis:
                cc += ' ' + word
            currentConv = cc
            '''
            ####
            data.append(currentConv)
    
    return data

def getTrainingData(trainList, value, pathExt):
    X_train = []
    y_train = []

    for movie in trainList: ###################
        if os.path.isfile(DATA_PATH + pathExt + movie + JSON_EXT):
            with open(DATA_PATH + pathExt + movie + JSON_EXT, 'r') as mc:
                convData = json.loads(mc.read())
            
            conversations = getConversation(convData)
            if conversations:
                X_train += conversations
                for i in conversations:
                    y_train.append(value)
            else:
                print(movie + " no conv :'(")
            
            #print('one done')

    return X_train, y_train

def getTestData(testList, value, pathExt):
    X_test = []
    y_testDecode = []
    
    for movie in testList: ###################
        if os.path.isfile(DATA_PATH + pathExt + movie + JSON_EXT):
            with open(DATA_PATH + pathExt + movie + JSON_EXT, 'r') as mc:
                convData = json.loads(mc.read())
            
            conversations = getConversation(convData)
            if conversations:
                y_testDecode.append((value, len(X_test), len(conversations))) #(val, index, len)
                X_test += conversations
            else:
                print(movie + " no conv :'(")
            
            #print('one done')

    return X_test, y_testDecode

def splitData(movieList):
    num2 = math.ceil(len(movieList[0]) * 0.8)
    num3 = num2
    #num3 = math.ceil(len(movieList[1]) * 0.8)
    
    
    print(num2, len(movieList[0]) - num2)
    print(num3, len(movieList[1]) - num3)
    

    trainM2 = random.sample(movieList[0], num2)
    trainM3 = random.sample(movieList[1], num3)

    testM2 = list(set(movieList[0]) - set(trainM2))
    testM3 = list(set(movieList[1]) - set(trainM3))

    return trainM2, testM2, trainM3, testM3

def getData():
    movieList = getFullMBase()

    trainM2, testM2, trainM3, testM3 = splitData(movieList)

    X_train2, y_train2 = getTrainingData(trainM2, 0, '2/')
    X_train3, y_train3 = getTrainingData(trainM3, 1, '3/')

    X_train = X_train2 + X_train3
    y_train = y_train2 + y_train3

    X_test2, y_testDecode2 = getTestData(testM2, 0, '2/')
    X_test3, y_testDecode3 = getTestData(testM3, 1, '3/')

    X_test = X_test2 + X_test3
    y_testDecode = y_testDecode2 + y_testDecode3 

    print(len(X_test2), len(X_test3))
    
    return X_train, X_test, y_train, y_testDecode

def decodeResults(y_pred, y_testDecode):
    y_test = []
    y_res = [] #what model predicted for a movie

    print(y_pred)
    gimme = []

    for movie in y_testDecode:
        y_test.append(movie[0])
        y_res.append(0)

        for i in range(movie[2]):
            y_res[-1] = y_res[-1] or y_pred[movie[1] + i]
            if y_pred[movie[1] + i] == 0:
                gimme.append(movie[1] + i)

    print(y_test)
    print(y_res)
    
    return y_test, y_res, gimme 

def main():
    '''
    X = getData()
    X.append('balette ig, girly stuff, smthn')
    X.append('school, balette dolls going to the mall, lets go to the mall today!')

    y = [1 for val in X]

    y[-2] = 0
    y[-1] = 0

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    '''
    X_train, X_test, y_train, y_testDecode = getData()

    xt = X_test
    #print(X_train[5])

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)

    #print(len(y_train), 'ye')
    #print(len(y_testDecode), 'yeeeee')

    y_pred = mnb.predict(X_test)

    print(len(y_pred), 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    print(len(y_testDecode))

    y, y2, gimme = decodeResults(y_pred, y_testDecode)

    
    for i in gimme:
        print(xt[i] + '\n')
    print(len(xt), type(xt))

    '''
    cnf_mat = metrics.confusion_matrix(y_test, y_pred)

    print(cnf_mat)

    m = metrics.accuracy_score(y_test, y_pred)
    print(m)
    '''
    '''
    for line in cnf_mat:
        for smth in line:
            for k in smth:
                print(k)

    
    with open('idk.json', 'w') as dd:
        dd.write(json.dumps(cnf_mat))
    '''

def main2():
    movieList = getFullMBase()

    X_train, y_train = getTrainingData(movieList[0], 0, '2/')
    X_test, y_testDecode = getTestData(movieList[1], 1, '3/')

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)

    y_pred = mnb.predict(X_test)

    print(y_pred)

#main2()

main()
