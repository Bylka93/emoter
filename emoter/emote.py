#!/usr/bin/python
# -*- coding: utf-8 -*-
encoding = "utf-8"
import os
import sys
import random
import datetime
import time
import gc
from future.builtins import input
import pickle as pickle
# import shelve
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
from textblob import TextBlob as TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer
# import sqlite3
import math
import pandas as pd
import numpy as np
import scipy
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import operator
import csv

class Emote(object):

    emoteClassOn = False    # Is Emote being used as a library or class? 
    runningScript = False   # Or is Emote being run as a script directly?
    firstTime = True     # Emote running for the first time?

    pickledOn = False    # Is a pickled database detected?
    SQLDataOn = False    # Is a SQL database detected?

    fullCount = ""  # The string result detailing the full amount of classifications (sorted by type and frequency) that the current training database contains

    writtenAnalysis = False    # Turn writte analysis on?
    levelsAnalysis = True    # Turn full levels analysis on?
    defaultCorpus = ""    # What's the default corpus?

    # connectDB = sqlite3.connect('base_corpus.db') # Using SQL db for base corpus texts

    def __init__(self, message = "", pre_result = "", prob_dist = 0, prob_dist_max = 0, positive = 0, negative = 0, joy = 0, anger = 0, love = 0,
                 hate = 0, certainty = 0, boredom = 0, intensity = 0, regret = 0, challenging = 0, agreeable = 0, desire = 0, calm = 0,
                 sarcastic = 0, emphatic = 0, pride = 0, accusative = 0, admiration = 0, inquisitive = 0, modest = 0, instructive = 0,
                 ambivalence = 0, vulgarity = 0, train = [], cl = NaiveBayesClassifier([]), punctCountDict = {}, wordCount = 0, sentenceCount = 0,
                 normalizedProbValues = {}, sentences = [], sentencesProbValues = [], massResults = []
                 ):

        self.train = train

        # PLACE THE TRAINING DATA (TUPLES) IN SELF.TRAIN BELOW
        # self.train = [
        # ]

        self.train = []

        #


        self.message = message
        self.punctCountDict = punctCountDict
        self.wordCount = wordCount
        self.sentenceCount = sentenceCount

        self.pre_result = pre_result
        self.prob_dist = prob_dist
        self.prob_dist_max = prob_dist_max

        self.positive = positive
        self.negative = negative
        self.joy = joy
        self.anger = anger
        self.love = love
        self.hate = hate
        self.certainty = certainty
        self.boredom = boredom
        self.intensity = intensity
        self.regret = regret
        self.challenging = challenging
        self.agreeable = agreeable
        self.desire = desire
        self.calm = calm
        self.sarcastic = sarcastic
        self.emphatic = emphatic
        self.pride = pride
        self.accusative = accusative
        self.admiration = admiration
        self.inquisitive = inquisitive
        self.modest = modest
        self.instructive = instructive
        self.ambivalence = ambivalence
        self.vulgarity = vulgarity
        self.prob_dist = prob_dist
        self.prob_dist_max = prob_dist_max
        self.cl = cl
        self.normalizedProbValues = normalizedProbValues
        self.sentences = sentences
        self.sentencesProbValues = sentencesProbValues
        self.massResults = massResults

    def getInput(self, _message):
        global firstTime
        global runningScript
        global emoteClassOn
        if runningScript == True:
            if firstTime == False:
                self.message = input('\n\tWrite message to be analyzed: ')
                _message = self.message
                self.countPunct(_message)
                self.countWordSent(_message)
                self.runAnalysis(_message)
            else: 
                print("""\n\tNow starting Emote as a script. Use Emote Mass Analyzer to break down a text into individual sentence 
                 classifications, or import Emote as a library.""")
                print("\n\tThe first time you run the analysis will be a little bit slower.")
                firstTime = False
                self.initialTrain()
        else:
            if firstTime == True:
                # print("\nFIRST TIME IS TRUE")
                print("\n\tRunning Emote as a library..")
                self.message = _message
                emoteClassOn = True
                self.countPunct(_message)
                self.countWordSent(_message)
                self.runAnalysis(_message)
            else:
                # print("\nFIRST TIME IS FALSE")
                emoteClassOn = True
                self.message = _message
                self.countPunct(_message)
                self.countWordSent(_message)
                self.runAnalysis(_message)


    def initialTrain(self):
        # For interchangable corpuses.. uncomment code modifying selectedCorpus 
        # selectedCorpus = input('\n\tEnter the name of the corpus file to load (Press enter to load default, from base_corpus.py): ')
        global defaultCorpus
        global pickledOn
        global SQLDataOn
        global SQLData
        global connectDB
        global fullCount

        fullDatabase = str(self.train)
        countPositive = fullDatabase.count("'positive')", 0, len(fullDatabase)); countNegative = fullDatabase.count("'negative')", 0, len(fullDatabase))
        countLove = fullDatabase.count("'love')", 0, len(fullDatabase)); countHate = fullDatabase.count("'hate')", 0, len(fullDatabase))
        countJoy = fullDatabase.count("'joy')", 0, len(fullDatabase)); countAnger = fullDatabase.count("'anger')", 0, len(fullDatabase))
        countCertainty = fullDatabase.count("'certainty'", 0, len(fullDatabase)); countConfusion = fullDatabase.count("'confusion'", 0, len(fullDatabase))
        countAmusement = fullDatabase.count("'amusement'", 0, len(fullDatabase)); countBoredom = fullDatabase.count("'boredom'", 0, len(fullDatabase))
        countIntensity = fullDatabase.count("'intensity'", 0, len(fullDatabase)); countRegret = fullDatabase.count("'regret'", 0, len(fullDatabase))
        countAgreeable = fullDatabase.count("'agreeable'", 0, len(fullDatabase)); countChallenging = fullDatabase.count("'challenging'", 0, len(fullDatabase))
        countDesire = fullDatabase.count("'desire'", 0, len(fullDatabase)); countCalm = fullDatabase.count("'calm'", 0, len(fullDatabase))
        countEmphatic = fullDatabase.count("'emphatic'", 0, len(fullDatabase)); countSarcastic = fullDatabase.count("'sarcastic'", 0, len(fullDatabase))
        countInstructive = fullDatabase.count("'instructive'", 0, len(fullDatabase)); countAccusative = fullDatabase.count("'accusative'", 0, len(fullDatabase))
        countAdmiration = fullDatabase.count("'admiration'", 0, len(fullDatabase)); countInquisitive = fullDatabase.count("'inquisitive'", 0, len(fullDatabase))
        countModest = fullDatabase.count("'modest'", 0, len(fullDatabase)); countPride = fullDatabase.count("'pride'", 0, len(fullDatabase))
        countAmbivalence = fullDatabase.count("'ambivalence'", 0, len(fullDatabase)); countVulgarity = fullDatabase.count("'vulgarity'", 0, len(fullDatabase))

        fullCount = "\n\tNumbers and types of classifications in loaded database: \n"+ "\t\tPositive: " + str(countPositive) + "\t" + "Negative: " + str(countNegative) + \
            "\t\tJoy: " + str(countJoy) + "\t\t" + "Anger: " + str(countAnger) + "\t\tCertainty: " + str(countCertainty) + "\t" + "Confusion: " + str(countConfusion) + \
            "\t\tCertainty: " + str(countCertainty) + "\t" + "Confusion: " + str(countConfusion) + "\t\tAmusement: " + str(countAmusement) + "\t" + "Boredom: " + str(countBoredom) + \
            "\t\tIntensity: " + str(countIntensity) + "\t" + "Regret: " + str(countRegret) + "\t\tAgreeable: " + str(countAgreeable) + "\t" + "Challenging: " + str(countChallenging) + \
            "\t\tDesire: " + str(countDesire) + "\t" + "Calm: " + str(countCalm) + "\t\tEmphatic: " + str(countEmphatic) + "\t" + "Sarcastic: " + str(countSarcastic) + \
            "\t\tInstructive: " + str(countInstructive) + "\t" + "Accusative: " + str(countAccusative) + "\t\tAdmiration: " + str(countAdmiration) + "\t" + "Inquisitive: " + str(countInquisitive) + \
            "\t\tAdmiration: " + str(countAdmiration) + "\t" + "Inquisitive: " + str(countInquisitive) + "\t\tAmbivalence: " + str(countAmbivalence) + "\t" + "Vulgarity: " + str(countVulgarity)
            "\t\tJoy: " + str(countJoy) + "\t\t" + "Anger: " + str(countAnger) + "\t\tCertainty: " + str(countCertainty) + "\t" + "Confusion: " + str(countConfusion) + \
            "\t\tCertainty: " + str(countCertainty) + "\t" + "Confusion: " + str(countConfusion) + "\t\tAmusement: " + str(countAmusement) + "\t" + "Boredom: " + str(countBoredom) + \
            "\t\tIntensity: " + str(countIntensity) + "\t" + "Regret: " + str(countRegret) + "\t\tAgreeable: " + str(countAgreeable) + "\t" + "Challenging: " + str(countChallenging) + \
            "\t\tDesire: " + str(countDesire) + "\t" + "Calm: " + str(countCalm) + "\t\tEmphatic: " + str(countEmphatic) + "\t" + "Sarcastic: " + str(countSarcastic) + \
            "\t\tInstructive: " + str(countInstructive) + "\t" + "Accusative: " + str(countAccusative) + "\t\tAdmiration: " + str(countAdmiration) + "\t" + "Inquisitive: " + str(countInquisitive) + \
            "\t\tAdmiration: " + str(countAdmiration) + "\t" + "Inquisitive: " + str(countInquisitive) + "\t\tAmbivalence: " + str(countAmbivalence) + "\t" + "Vulgarity: " + str(countVulgarity)

        print("""\n\tNumbers and types of classifications in database to be loaded: \n""")
        print("\t\tPositive: " + str(countPositive) + "\t" + "Negative: " + str(countNegative))
        print("\t\tLove: " + str(countLove) + "\t\t" + "Hate: " + str(countHate))
        print("\t\tJoy: " + str(countJoy) + "\t\t" + "Anger: " + str(countAnger))
        print("\t\tCertainty: " + str(countCertainty) + "\t" + "Confusion: " + str(countConfusion))
        print("\t\tAmusement: " + str(countAmusement) + "\t" + "Boredom: " + str(countBoredom))
        print("\t\tIntensity: " + str(countIntensity) + "\t" + "Regret: " + str(countRegret))
        print("\t\tAgreeable: " + str(countAgreeable) + "\t" + "Challenging: " + str(countChallenging))
        print("\t\tDesire: " + str(countDesire) + "\t" + "Calm: " + str(countCalm))
        print("\t\tEmphatic: " + str(countEmphatic) + "\t" + "Sarcastic: " + str(countSarcastic))
        print("\t\tInstructive: " + str(countInstructive) + "\t" + "Accusative: " + str(countAccusative))
        print("\t\tAdmiration: " + str(countAdmiration) + "\t" + "Inquisitive: " + str(countInquisitive))
        print("\t\tModest: " + str(countModest) + "\t" + "Pride: " + str(countPride))
        print("\t\tAmbivalence: " + str(countAmbivalence) + "\t" + "Vulgarity: " + str(countVulgarity))

        # if selectedCorpus != defaultCorpus and selectedCorpus != "":
            # defaultCorpus = selectedCorpus
        # elif selectedCorpus == "":
            # defaultCorpus = defaultCorpus
        # else:
            # defaultCorpus = "base_corpus.py"
        selectedCorpus = defaultCorpus

        try:
            # path = os.getcwd()
            # path = os.path.join(path, 'data', 'base_corpus.pickle')
            # dir = os.path.dirname(os.path.abspath(__file__))
            # path = os.path.join(dir, 'data', 'base_corpus.pickle')
            dir = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dir, 'data', 'base_corpus.pickle')
            with open(path, 'rb') as fp:
                size = os.path.getsize(path)
                if size > 0:
                    pickledOn = True
                    print("\n\tPickled data found!")
                else:
                    pass
                fp.close()
        except IOError as err:
            pickledOn = False
            # path = os.getcwd()
            # dir = os.path.dirname(os.path.abspath(__file__))
            # path = os.path.join(dir, 'data', 'base_corpus.pickle')
            # path = "/home/jddunn/emoter/data/base_corpus.pickle"
            dir = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dir, 'data', 'base_corpus.pickle')
            print("\n\tNo pickled data found.. now creating and loading pickle..")
        # If corpus text in SQL db..
        # try:
        #     path = os.getcwd()
        #     path = os.path.join(path, '../data', 'base_corpus.db')
        #     with open(path, 'r') as fp:
        #         SQLDataOn = True
        #         size = os.path.getsize(path)
        #         if size > 5:
        #             SQLDataOn = True
        #             print("\n\tNo SQL found.")
        #         else:
        #             SQLDataOn = False
        #             print("\n\tSQL found!")
        #         fp.close()
        # except IOError as err:
        #     SQLDataOn = False
        #     print("\n\tNo SQL data found.. now creating and loading SQL.")

        # SHELVE STUFF
        # READING TRAINING DATA FROM FILE DEFAULTCORPUS
        if pickledOn == False:
            # Code below takes training data from text file input
            # path = os.getcwd()
            # path = os.path.join(path, 'data', 'base_corpus.txt')          
            #     # shelvedData = shelve.open('base_corpus.db')
            #     # if shelvedData:
            #         # pickledOn = True
            # # with open(path, 'r') as fp:
            #     # print(fp)
            # # fp = open(path,'r').read().tt('\n')
            # # fp = open(path, 'r', encoding="utf8")
            # # print("\n\tOpening training data.")
            # # self.train = fp.readlines()
            # # print(self.train)
            # temp = [line[:-1] for line in self.train]
            # print(temp)
            #     # self.train = self.train.rstrip("\r\n")
            #     # for i in self.train:
            #     #     i = i.encode('ascii', 'backslashreplace')
            #     #     i = i.rstrip("\r\n") 
            #     #     print(i)
            # path = os.path.join(path, 'data', 'base_corpus.py')          
                # shelvedData = shelve.open('base_corpus.db')
                # if shelvedData:
                    # pickledOn = True
            # with open(path, 'r') as fp:
                # print(fp)
            # fp = open(path,'r').read().tt('\n')
            # self.train = fp.readlines()
            # temp = [line[:-1] for line in self.train]
            # print(temp)
                # self.train = self.train.rstrip("\r\n")
                # for i in self.train:
                    # i = i.encode('ascii', 'backslashreplace')
                    # i = i.rstrip("\r\n") 
                    # print(i)
            # lines = tuple(open(path, 'r', encoding = 'utf-8'))
            # lines = lines.strip()
            # print(str(lines))
            # self.train = lines
            print(self.train)
            # print(self.train)

            print("\n\tOpening training data.")

            # if SQLDataOn == False: 
                # self.sendToSQL()
                # currentTime = datetime.datetime.now().time()
                # print("\n\n\tTIME NEW DATABASE STARTED TRAINING: ", currentTime)
                # print("""\n\tStarting NaiveBayesClassifer training for """ + str(len(self.train)) + """ supervised classifications.. the initial training period will take a while.""")
            # elif SQLDataOn == True:
                # self.parseFromSQL()

            random.seed(1)
            random.shuffle(self.train)
            self.cl = NaiveBayesClassifier(self.train)
            print("\n\tTraining now..")
            # shelvedData["base"] = cl # SHELF vs PICKLE
            # path = os.getcwd()
            # path = os.path.join(path, 'data', 'base_corpus.pickle')    
            # dir = os.path.dirname(os.path.abspath(__file__))
            dir = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dir, 'data', 'base_corpus.pickle')

            fp = open(path, 'wb')
            print("\n\tLoaded training data into pickle file.")
            pickle.dump(self.cl, fp, protocol=pickle.HIGHEST_PROTOCOL)
            fp.close()
            print("\n\tPickling complete, and will be loaded as the default database corpus next time, skipping the training period.")
            currentTime = datetime.datetime.now().time()
            print("\n\n\tTIME NEW DATABASE FINISHED TRAINING AND SAVING: ", currentTime)
            # shelvedData.close() # SHELF vs PICKLE
        if pickledOn == True:
            try:
                # shelvedData = shelve.open("base_corpus.dat") # SHELF VS PICKLE
                path = os.getcwd()
                path = os.path.join(path, 'data', 'base_corpus.pickle')                
                fp = open(path, 'rb')
                # path = os.getcwd()
                # path = os.path.join(path, 'data', 'base_corpus.pickle')                
                fp = open(path,"rb")
                self.cl = pickle.load(fp)
                fp.close()
                print("\n\tTraining has been loaded from the selected corpus.")
                print("\t\t" + fullCount)
            except IOError as err:
                print("\n\tError training pickle file.. system will exit. Go into the directory, delete the corrupt pickle file, and retry this script to train a new copy.")
                print("\n\tPath was at:", path)  
                sys.exit()
            pass
        if emoteClassOn == True:
            self.runAnalysis(_message)    
        else:
            self.getInput(_message)


    # If corpus data was stored in SQL..
    # def sendToSQL(self):
    #     c.execute("DROP TABLE IF EXISTS Base")
    #     c.execute("CREATE TABLE Base (Date_Sorted TEXT, Source TEXT, Message TEXT);")
    #     for i in self.train:
    #         # print(i)
    #         try:
    #             c.execute("INSERT INTO Base VALUES (?, ?, ?);", ('11-05-2016', 'general', i))
    #             connectDB.commit()
    #             print(i)
    #         except:
    #             print('err')
    #             pass
    #     c.close()

    # def parseFromSQL(self):
    #     global SQLData
    #     global connectDB
    #     print("Training data from SQL..")
    #     try:
    #         # connectDB.row_factory = sqlite3.Row
    #         c.execute("SELECT Message FROM base WHERE 1")
    #         # connectDB.text_factory = lambda x: x.decode("utf-8")
    #         all_rows = cursor.fetchall()
    #         # line = re.sub('[!@#$]', '', line)
    #         # all_rows = [row[0].strip for row in cursor.fetchall()]
    #         # for r in all_rows:
    #             # temp_row = r[0]
    #             # temp_row = temp_row.strip()
    #             # temp_row = re.sub('\r\n', '', temp_row)
    #             # temp_row = re.sub('\\', '', temp_row)
    #             # temp_row = unicodedata.normalize('NFKD', temp_row).encode('ascii','ignore')
    #             # print(temp_row)
    #             # temp_row = temp_row.replace("\\","")
    #             # SQLData.append(unicodedata.normalize('NFKD', temp_row))
    #             # SQLData.append(str(temp_row).strip())
    #     except:
    #         pass


    def countPunct(self, _message):
        numberCount = 0
        periodCount = 0
        commaCount = 0
        exclamationPtCount = 0
        questionMkCount = 0
        for char in _message:
            if char.isdigit() == True:
                numberCount+=1
            elif char == '.':
                periodCount+=1
            elif char == ',':
                commaCount+=1
            elif char == '!': 
                exclamationPtCount+=1
            elif char == '?':
                questionMkCount+=1
            else:
                pass
        self.punctCountDict = {
                        "numbers": numberCount,
                        "periods_end": periodCount,
                        "question_marks": questionMkCount,
                        "exclamation_points": exclamationPtCount,
                        "commas": commaCount
                        }
        return self.punctCountDict


    def countWordSent(self, _message):
        _messageSplitWords = _message.split()
        _messageSplitSent = sent_tokenize(_message)
        self.wordCount = len(_messageSplitWords)
        # print("\n\tWord count in message: " + str(self.wordCount))
        self.sentenceCount = len(_messageSplitSent)
        # print("\n\tSentence count in message: " + str(self.sentenceCount))
        return self.wordCount, self.sentenceCount


    def split_into_sentences(self, _message):
        sentenceTempValStore = []
        self.normalizedProbValues = []
        self.sentences = sent_tokenize(_message)
        if len(self.sentences) > 1:
            for i in self.sentences:
                self.runAnalysis(str(i))
                self.sentencesProbValues.append(self.normalizedProbValues)
            return self.sentencesProbValues
        else:
            pass


    def analyzeCSV(self, path):
        csvData = []
        csvTextData = []
        file = open(path, 'r')
        csv_file = csv.reader(file, delimiter = ",")
        for row in csv_file:
            csvData.append(row[0])
            csvTextData.append(row[1])
        file.close()
        print("\n\t", csvData)
        print("\n\t", csvTextData)
        print("\n\t",csvTextData)
        print("\n\t", csvData)
        self.massResults = []
        for i in range(len(csvTextData)):
            self.runAnalysis(csvTextData[i])
            print(emote.normalizedProbValues)
            self.massResults.append(self.normalizedProbValues)
        # path = os.getcwd()
        # path = os.path.join(path, 'static', 'results.csv')
        dir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(dir, 'static', 'results.csv')
        csvFile = open(path, 'w', newline='')
        for i in range(len(self.massResults)):
            csvIndRowList = []
            csvResults = csv.writer(csvFile, delimiter = ',')
            csvIndRowList.append(csvData[i])
            csvIndRowList.append(csvTextData[i])
            csvIndRowList.append(self.massResults[i][0])
            csvIndRowList.append(self.massResults[i][1])
            csvIndRowList.append(self.massResults[i][2])
            csvIndRowList.append(self.massResults[i][3])
            csvIndRowList.append(self.massResults[i][4])
            csvIndRowList.append(self.massResults[i][5])
            print("\n\tROW LIST", csvIndRowList)
            csvResults.writerow(csvIndRowList)
        csvFile.close()
        return csvResults, csvFile, self.massResults




    def runAnalysis (self, _message):
            global emoteClassOn
            global firstTime 
            global runningScript
            if firstTime == True and emoteClassOn == True:
                print("\n\n\t\t(First time running analysis.. load pickle data. The initial analysis will be slower because of the models loading, and so is automatically run in the beginning.)")
                try:
                    # path = os.getcwd()
                    # path = os.path.join(path, 'data', 'base_corpus.pickle')
                    # Use the path below when uploading to Pythonanywhere
                    # dir = os.path.dirname(__file__)
                    dir = os.path.abspath(os.path.dirname(__file__))
                    path = os.path.join(dir, 'data', 'base_corpus.pickle')
                    with open(path, 'rb') as fp:
                        self.cl = pickle.load(fp)
                        emoteClassOn = False
                        firstTime = False
                except:
                    print("\n\tError gathering pickle file in /data directory. Application exit.")
                    print("\n\tThis was the attempted path that was searched: ", path)
            print("\n\tFinished loading pickle.")
            print("\n\tAnalyzing " + "'"+str(_message)+"'" +"..")
            self.prob_dist = self.cl.prob_classify(_message);
            self.prob_dist_max = self.prob_dist.max()
            # print("\n\tAnalyzing " + "'"+str(_message)+"'" +"..")
            self.prob_dist = self.cl.prob_classify(_message); self.prob_dist_max = self.prob_dist.max()
            self.positive = round(self.prob_dist.prob("positive"), 4); self.negative = round(self.prob_dist.prob("negative"), 4)
            self.joy = round(self.prob_dist.prob("joy"), 4); self.anger = round(self.prob_dist.prob("anger"), 4)
            self.love = round(self.prob_dist.prob("love"), 4); self.hate = round(self.prob_dist.prob("hate"), 4)
            self.certainty = round(self.prob_dist.prob("certainty"), 4); self.confusion = round(self.prob_dist.prob("confusion"), 4)
            self.amusement = round(self.prob_dist.prob("amusement"), 4); self.boredom = round(self.prob_dist.prob("boredom"), 4)
            self.intensity = round(self.prob_dist.prob("intensity"), 4); self.regret = round(self.prob_dist.prob("regret"), 4)
            self.agreeable = round(self.prob_dist.prob("agreeable"), 4); self.challenging = round(self.prob_dist.prob("challenging"), 4)
            self.desire = round(self.prob_dist.prob("desire"), 4); self.calm = round(self.prob_dist.prob("calm"), 4)
            self.emphatic = round(self.prob_dist.prob("emphatic"), 4); self.sarcastic = round(self.prob_dist.prob("sarcastic"), 4)
            self.instructive = round(self.prob_dist.prob("instructive"), 4); self.accusative = round(self.prob_dist.prob("accusative"), 4)
            self.admiration = round(self.prob_dist.prob("admiration"), 4); self.inquisitive = round(self.prob_dist.prob("inquisitive"), 4)
            self.modest = round(self.prob_dist.prob("modest"), 4); self.pride = round(self.prob_dist.prob("pride"),4)
            self.ambivalence = round(self.prob_dist.prob("ambivalence"), 4); self.vulgarity = round(self.prob_dist.prob('vulgarity'),4)
            
            valueList = [self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity]
            
            posNegAbsVal = math.fabs(self.positive - self.negative)
            # Do some normalization if the difference between the positive and negative tone values is too small
            # since positive and negative should lie on opposite sides of the spectrum
            if posNegAbsVal <= .25:
               self.positive = self.positive * math.sqrt(self.positive) * math.sqrt(self.positive) * math.sqrt(self.positive) * math.sqrt(self.positive) 
               self.negative = self.negative * math.sqrt(self.negative) * math.sqrt(self.negative) * math.sqrt(self.negative) * math.sqrt(self.negative)
            else:
                pass

            if runningScript == True:
                print("\n\tProbability Values From NaiveBayesClassifier: ")
                print("\tStrongest Emotion: " + self.prob_dist_max)
                print("\tPositive: " + str(self.positive) + "\tNegative: " + str(self.negative))
                print("\tJoy: " + str(self.joy) + "\tAnger: " + str(self.anger))
                print("\tLove: " + str(self.love) + "\tHate: " + str(self.hate))
                print("\tCertainty: " + str(self.certainty) + "\tConfusion: " + str(self.confusion))
                print("\tAmusement: " + str(self.amusement) + "\tBoredom: " + str(self.boredom))
                print("\tIntensity: " + str(self.intensity) + "\tRegret: " + str(self.regret))
                print("\tAgreeable: " + str(self.agreeable) + "\tChallenging: " + str(self.challenging))
                print("\tDesire: " + str(self.desire) + "\tCalm: " + str(self.calm))
                print("\tEmphatic: " + str(self.emphatic) + "\tSarcastic: " + str(self.sarcastic))
                print("\tInstructive: " + str(self.instructive) + "\tAccusative: " + str(self.accusative))
                print("\tAdmiration: " + str(self.admiration) + "\tInquisitive: " + str(self.inquisitive))
                print("\tModest: " + str(self.modest) + "\tPride: " + str(self.pride))
                print("\tAmbivalence: " + str(self.ambivalence) + "\tVulgarity: " + str(self.vulgarity))

                self.normalizedProbValues = pd.Series({'positive': self.positive, 'negative' : self.negative, 'joy' : self.joy, 'anger' : self.anger,
                                           'love': self.love, 'hate' : self.hate, 'certainty' : self.certainty, 'confusion' : self.confusion,
                                           'amusement' : self.amusement, 'boredom' : self.boredom, 'intensity' : self.intensity, 'regret' : self.regret,
                                           'agreeable': self.agreeable, 'challenging' : self.challenging, 'desire' : self.desire, 'calm' : self.calm,
                                           'emphatic' : self.emphatic, 'sarcastic' : self.sarcastic, 'instructive' : self.instructive, 'accusative' : self.accusative,
                                           'admiration' : self.admiration, 'inquisitive' : self.inquisitive, 'modest' : self.modest, 'pride' : self.pride,
                                           'ambivalence' : self.ambivalence, 'vulgarity' : self.vulgarity})
                # print("Noramlized prob values: " + str(self.normalizedProbValues))

                # print("\n\t",self.normalizedProbValues)
                # print("\n\t", self.normalizedProbValues.describe())
                self.normalizeProbabilityPunctuation(_message)
                # return self.normalizedProbValues, self.prob_dist, self.prob_dist_max, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity
         
            else:
                # self.normalizedProbValues = pd.DataFrame(pdData).astype(np.float32)
                # print("\n\t",self.normalizedProbValues)
                # print("\n\t", self.normalizedProbValues.describe())
                self.normalizeProbabilityPunctuation (_message)
                # return self.normalizedProbValues
                # return self.prob_dist, self.prob_dist_max, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity
                # return self.normalizedProbValues, self.prob_dist, self.prob_dist_max, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity
         
            else:
                # pdData = [{'positive': self.positive, 'negative' : self.negative, 'joy' : self.joy, 'anger' : self.anger,
                #                            'love': self.love, 'hate' : self.hate, 'certainty' : self.certainty, 'confusion' : self.confusion,
                #                            'amusement' : self.amusement, 'boredom' : self.boredom, 'intensity' : self.intensity, 'regret' : self.regret,
                #                            'agreeable': self.agreeable, 'challenging' : self.challenging, 'desire' : self.desire, 'calm' : self.calm,
                #                            'emphatic' : self.emphatic, 'sarcastic' : self.sarcastic, 'instructive' : self.instructive, 'accusative' : self.accusative,
                #                            'admiration' : self.admiration, 'inquisitive' : self.inquisitive, 'modest' : self.modest, 'pride' : self.pride,
                #                            'ambivalence' : self.ambivalence, 'vulgarity' : self.vulgarity}]
                self.normalizedProbValues = pd.Series({'positive': self.positive, 'negative' : self.negative, 'joy' : self.joy, 'anger' : self.anger,
                                           'love': self.love, 'hate' : self.hate, 'certainty' : self.certainty, 'confusion' : self.confusion,
                                           'amusement' : self.amusement, 'boredom' : self.boredom, 'intensity' : self.intensity, 'regret' : self.regret,
                                           'agreeable': self.agreeable, 'challenging' : self.challenging, 'desire' : self.desire, 'calm' : self.calm,
                                           'emphatic' : self.emphatic, 'sarcastic' : self.sarcastic, 'instructive' : self.instructive, 'accusative' : self.accusative,
                                           'admiration' : self.admiration, 'inquisitive' : self.inquisitive, 'modest' : self.modest, 'pride' : self.pride,
                                           'ambivalence' : self.ambivalence, 'vulgarity' : self.vulgarity})
                self.normalizeProbabilityPunctuation (_message)
                # return self.normalizedProbValues
                # return self.prob_dist, self.prob_dist_max, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity
                return self.normalizedProbValues, self.prob_dist, self.prob_dist_max, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity



    def normalizeProbabilityPunctuation (self, _message):
            print("\tNow normalizing probability based on punctuation count..")
            # print("\n\t", self.punctCountDict)
            # print("\tNow normalizing probability based on punctuation count..")
            ############################################################################################################################################################
            # Base values below. Variables will be scaled off of linearly increasing relationships based off these values below, to determine different probability ranges. 
            minWordCountRange = 0
            minSentenceCountRange = 0
            maxWordCountRange = 50
            maxSentenceCountRange = 3
            maxCommaCountRange = 6
            msgWordCountLeveler = 0
            msgSentenceCountLeveler = 0
            punctSlidingThreshold = 1
                # Code below contains the actual sliding algorithm for probability normalization through punctuation
                # START (The values in this if-then don't need to be sliding (mapped to a range), because anything longer than 50 words or 2 sentences will be considered "long").
                # This part of the algorithm is also not adjusted by the leveler, because the progression does not scale well enough based off the original values without manipulation. 
                # Manipulation come from the msgWordCountLeveler and msgSentenceCountLeveler variables
            if minWordCountRange < self.wordCount < maxWordCountRange and minSentenceCountRange < self.sentenceCount <= maxSentenceCountRange:
                # print("\tProbability normalization based off of the first level of scaling.")
                punctSlidingThreshold = 1
                    # Emphatic sentences more likely more likely (deep analytical thinking)
                    # Values below are mapped to linearly scaling variables (to save having to numbers manually and repeatedly, of course).
                    # PunctSlidingThreshold not used for commas for this instance case because multiplying by 1 does not give a high enough threshold
                # if minWordCountRange < self.wordCount < maxWordCountRange and self.sentenceCount >= maxSentenceCountRange and self.punctCountDict['commas'] <= 3:
                #     print("\tLong, slow writing, with many commas.")    
                # elif minWordCountRange < self.wordCount < maxWordCountRange and self.sentenceCount < maxSentenceCountRange and self.punctCountDict['commas'] <= 3:
                #     print("\tQuick, rapid writing. Many short sentences, few commas.")
                # else: 
                #     pass    
                if self.punctCountDict['numbers'] >= punctSlidingThreshold:
                    # More informative or descriptive message more likely
                    # print("\tNumbers detected.")
                    pass
                elif self.punctCountDict['periods_end'] >= punctSlidingThreshold:
                    # print("\tPeriods detected.")
                    pass
                elif self.punctCountDict['question_marks'] >= punctSlidingThreshold:
                    if self.inquisitive <= .1:
                        self.inquisitive = .1
                    else:
                        self.inquisitive = self.inquisitive / math.sqrt(self.inquisitive) * self.punctCountDict['question_marks']
                    # print("\tQuestions detected.")
                elif self.punctCountDict['exclamation_points'] >= punctSlidingThreshold:
                    if self.intensity <= .1:
                        self.intensity = .1
                    else:
                        self.intensity = self.intensity / math.sqrt(self.intensity) * self.punctCountDict['exclamation_points']
                        # print("\tExclamations detected.")
                elif self.punctCountDict['commas'] >= punctSlidingThreshold * 1.5:
                    # print("\tCommas detected.")
                    pass
                else:
                    pass
            # END
            # START
            if self.wordCount > maxWordCountRange or minSentenceCountRange > maxSentenceCountRange:
                # print("\tProbability normaliziation based off of a proportionally increased level of scaling from word / sentence count.")
                msgWordCountLeveler = int(self.wordCount / maxWordCountRange)
                msgSentenceCountLeveler = int(self.sentenceCount / maxSentenceCountRange)
                minWordCountRange = 1 *  msgWordCountLeveler
                minSentenceCountRange = 1 * msgSentenceCountLeveler
                maxWordCountRange = maxWordCountRange * msgWordCountLeveler
                maxSentenceCountRange = minSentenceCountRange * msgSentenceCountLeveler
                # Make sure we're not dividing by 0
                if msgSentenceCountLeveler < 1:
                    msgSentenceCountLeveler = 1
                punctSlidingThreshold = int((punctSlidingThreshold * (msgSentenceCountLeveler * msgWordCountLeveler / msgSentenceCountLeveler)))
                if minWordCountRange < self.wordCount < maxWordCountRange and minSentenceCountRange < self.sentenceCount < maxSentenceCountRange:
                    # Emphatic sentences more likely more likely (deep analytical thinking)
                    # print("\tLong sentence detected.")
                    # Punctuation threshold for commas are slightly higher than end marks, so they are multiplied by 1.5
                    # if minWordCountRange < self.wordCount < maxWordCountRange and self.sentenceCount >= maxSentenceCountRange and self.commas < int(punctSlidingThreshold) * 1.5:
                    #     print("\tQuick, rapid writing. Many short sentences, few commas.")
                    # if minWordCountRange < self.wordCount < maxWordCountRange and self.sentenceCount < maxSentenceCountRange and self.commas >= int(punctSlidingThreshold) * 1.5:
                    #     print("\tLong, slow writing, with many commas.")    
                    if self.punctCountDict['numbers'] >= punctSlidingThreshold:
                        # More informative or descriptive message more likely
                        # print("\tNumbers detected.")
                        pass
                    elif self.punctCountDict['periods_end'] >= punctSlidingThreshold:
                        # print("\tPeriods detected.")
                        pass
                    elif self.punctCountDict['question_marks'] >= punctSlidingThreshold:
                        if self.inquisitve <= .1:
                            self.inquisitve = .1
                        else:
                            self.inquisitive = self.inquisitive / math.sqrt(self.inquisitive) * self.punctCountDict['question_marks']
                        # print("\tQuestions detected.")
                    elif self.punctCountDict['exclamation_points'] >= punctSlidingThreshold:
                        if self.intensity <= .1:
                            self.intensity = .1
                        else:
                            self.intensity = self.intensity / math.sqrt(self.intensity) * self.punctCountDict['exclamation_points']
                            # print("\tExclamations detected.")
                    elif self.punctCountDict['commas'] >= punctSlidingThreshold * 1.5:
                        # print("\tCommas detected.")
                        pass
                    else: 
                        pass
                # END
            ############################################################################################################################################################
            # print("\n\tProbability Values Post-Normalization Counting Punctuation: ")
            # print(self.normalizedProbValues)
            # self.normalizeProbabilityOpposites(_message)
            print("\n\t", self.punctCountDict)
            self.normalizedProbValues = pd.Series({'positive': self.positive, 'negative' : self.negative, 'joy' : self.joy, 'anger' : self.anger,
                                           'love': self.love, 'hate' : self.hate, 'certainty' : self.certainty, 'confusion' : self.confusion,
                                           'amusement' : self.amusement, 'boredom' : self.boredom, 'intensity' : self.intensity, 'regret' : self.regret,
                                           'agreeable': self.agreeable, 'challenging' : self.challenging, 'desire' : self.desire, 'calm' : self.calm,
                                           'emphatic' : self.emphatic, 'sarcastic' : self.sarcastic, 'instructive' : self.instructive, 'accusative' : self.accusative,
                                           'admiration' : self.admiration, 'inquisitive' : self.inquisitive, 'modest' : self.modest, 'pride' : self.pride,
                                           'ambivalence' : self.ambivalence, 'vulgarity' : self.vulgarity})
            self.normalizeProbability(_message)
            # return self.normalizedProbValues


    def normalizeProbability (self, _message):

        print("\n\tNow standardizing probabilities into percentages..")

        self.normalizedProbValues = self.normalizedProbValues.values.reshape(1, -1)

        # self.normalizedProbValues = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(50.0, 100.0), copy = True).fit_transform(self.normalizedProbValues)
        self.normalizedProbValues = preprocessing.StandardScaler(with_mean = False, with_std = False).fit_transform(self.normalizedProbValues)
      
        self.normalizedProbValues = preprocessing.normalize(self.normalizedProbValues, norm = 'max')
        self.normalizedProbValues = np.array(self.normalizedProbValues).tolist()

        normalizedProbValTemp = self.normalizedProbValues

        normalizedProbValTemp = self.normalizedProbValues

        self.normalizedProbValues = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(50.0, 100.0), copy = True).fit_transform(normalizedProbValTemp)
        normalizedProbValTemp = self.normalizedProbValues
        self.normalizedProbValues = preprocessing.StandardScaler(with_mean = False, with_std = False).fit_transform(normalizedProbValTemp)
        normalizedProbValTemp = self.normalizedProbValues
      
        self.normalizedProbValues = preprocessing.normalize(normalizedProbValTemp, norm = 'max')
        normalizedProbValTemp = self.normalizedProbValues
        self.normalizedProbValues = np.array(normalizedProbValTemp).tolist()
        normalizedProbValTemp = self.normalizedProbValues

        # LIST BELOW IS SORTED ALPHABETICALLY BECAUSE OF HOW NUMPY DOES IT

        normalizedAccusative = normalizedProbValTemp[0][0]; normalizedAdmiration = normalizedProbValTemp[0][1]; 
        normalizedAgreeable = normalizedProbValTemp[0][2]; normalizedAmbivalence = normalizedProbValTemp[0][3]; 
        normalizedAmusement = normalizedProbValTemp[0][4]; normalizedAnger = normalizedProbValTemp[0][5]; 
        normalizedBoredom = normalizedProbValTemp[0][6]; normalizedCalm = normalizedProbValTemp[0][7]; 
        normalizedCertainty = normalizedProbValTemp[0][8]; normalizedChallenging = normalizedProbValTemp[0][9]; 
        normalizedConfusion = normalizedProbValTemp[0][10]; normalizedDesire = normalizedProbValTemp[0][11]; 
        normalizedEmphatic = normalizedProbValTemp[0][12]; normalizedHate = normalizedProbValTemp[0][13]; 
        normalizedInquisitive = normalizedProbValTemp[0][14]; normalizedInstructive = normalizedProbValTemp[0][15]; 
        normalizedIntensity = normalizedProbValTemp[0][16]; normalizedJoy = normalizedProbValTemp[0][17]; 
        normalizedLove = normalizedProbValTemp[0][18]; normalizedModest = normalizedProbValTemp[0][19]; 
        normalizedNegative = normalizedProbValTemp[0][20]; normalizedPositive = normalizedProbValTemp[0][21]; 
        normalizedPride = normalizedProbValTemp[0][22]; normalizedRegret = normalizedProbValTemp[0][23]; 
        normalizedSarcastic = normalizedProbValTemp[0][24]; normalizedVulgarity = normalizedProbValTemp[0][25];

        self.positive = float(round(normalizedPositive, 3) * 100); self.negative = float(round(normalizedNegative, 3) * 100);
        self.joy = float(round(normalizedJoy, 3) * 100); self.anger = float(round(normalizedAnger, 3) * 100);
        self.love = float(round(normalizedLove, 3) * 100); self.hate = float(round(normalizedHate, 3) * 100);
        self.certainty = float(round(normalizedCertainty, 3) * 100); self.confusion = float(round(normalizedConfusion, 3) * 100);
        self.amusement = float(round(normalizedAmusement, 3) * 100); self.boredom = float(round(normalizedBoredom, 3) * 100);
        self.intensity = float(round(normalizedIntensity, 3) * 100); self.regret = float(round(normalizedRegret, 3) * 100);
        self.agreeable = float(round(normalizedAgreeable, 3) * 100); self.challenging = float(round(normalizedChallenging, 3) * 100);
        self.desire = float(round(normalizedDesire, 3) * 100); self.calm = float(round(normalizedCalm, 3) * 100);
        self.emphatic = float(round(normalizedEmphatic, 3) * 100); self.sarcastic = float(round(normalizedSarcastic, 3) * 100);
        self.instructive = float(round(normalizedInstructive, 3) * 100); self.accusative = float(round(normalizedAccusative, 3) * 100);
        self.admiration = float(round(normalizedAdmiration, 3) * 100); self.inquisitive = float(round(normalizedInquisitive, 3) * 100);
        self.modest = float(round(normalizedModest, 3) * 100); self.pride = float(round(normalizedPride, 3) * 100);        
        self.ambivalence = float(round(normalizedAmbivalence, 3) * 100); self.vulgarity = float(round(normalizedVulgarity, 3) * 100);

        normalizedProbValTemp = {}

        normalizedProbValTemp['positive'] = self.positive; normalizedProbValTemp['negative'] = self.negative;
        normalizedProbValTemp['joy'] = self.joy; normalizedProbValTemp['anger'] = self.anger;
        normalizedProbValTemp['love'] = self.love; normalizedProbValTemp['hate'] = self.hate;
        normalizedProbValTemp['certainty'] = self.certainty; normalizedProbValTemp['confusion'] = self.confusion;
        normalizedProbValTemp['amusement'] = self.amusement; normalizedProbValTemp['boredom'] = self.boredom;
        normalizedProbValTemp['intensity'] = self.intensity; normalizedProbValTemp['regret'] = self.regret;
        normalizedProbValTemp['agreeable'] = self.agreeable; normalizedProbValTemp['challenging'] = self.challenging;
        normalizedProbValTemp['desire'] = self.desire; normalizedProbValTemp['calm'] = self.calm;
        normalizedProbValTemp['emphatic'] = self.emphatic; normalizedProbValTemp['sarcastic'] = self.sarcastic;
        normalizedProbValTemp['instructive'] = self.instructive; normalizedProbValTemp['accusative'] = self.accusative;
        normalizedProbValTemp['admiration'] = self.admiration; normalizedProbValTemp['inquisitive'] = self.inquisitive;
        normalizedProbValTemp['modest'] = self.modest; normalizedProbValTemp['pride'] = self.pride;        
        normalizedProbValTemp['ambivalence'] = self.ambivalence; normalizedProbValTemp['vulgarity'] = self.vulgarity;

        # print("\n\n\t", normalizedProbValTemp)
        self.normalizedProbValues = normalizedProbValTemp
        normalizedProbValTemp = sorted(self.normalizedProbValues.items(), key=operator.itemgetter(1), reverse = True)
        self.normalizedProbValues = normalizedProbValTemp
        self.normalizedProbValues = list(self.normalizedProbValues)

        print("\n\tFinal results: " + str(self.normalizedProbValues))

        if runningScript == True:
            self.getInput(_message)
            return self.normalizedProbValues, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity

        print("\n\t",self.normalizedProbValues)
        if runningScript == True:
            self.getInput(_message)
            return self.normalizedProbValues, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity
        # self.normalizeProbabilityPunctuation(_message)
        return self.normalizedProbValues, self.positive, self.negative, self.joy, self.anger, self.love, self.hate, self.certainty, self.confusion, self.amusement, self.boredom, self.intensity, self.regret, self.agreeable, self.challenging, self.desire, self.calm, self.emphatic, self.sarcastic, self.instructive, self.accusative, self.admiration, self.inquisitive, self.modest, self.ambivalence, self.vulgarity


    # def normalizeProbabilityOpposites (self, _message):
        
    #     print("\n\tNow normalizing probability based on opposite pariing of tones..")
    #     return self.normalizedProbValues


    # def combineTones (self):
    #     return


    # def writtenAnalysis(self):
    #     return


    # def keywordAssociations(self):
    #     return


    # def giveResponse(self):
    #     return 

    # def testAccuracy(self, testData):
    #     # print("\n\n\t\tNow testing current loaded database with test data for accuracy.")
    #     # print(testData)
    #     testGrade = self.cl.accuracy(testData)
    #     # print("\n\t" + testData + "\tAccuracy Level: " + str(testGrade))
    #     return


if __name__ == '__main__':
    # message = ""
    runningScript = True
    firstTime = True
    defaultCorpus = "base_corpus.py"
    pickledOn = False
    SQLData = []
    SQLDataOn = False
    emoteClassOn = False
    fullCount = ""
    _message = ""
    # connectDB = sqlite3.connect('base_corpus.db')  
    # cursor = connectDB.cursor()  
    # c = connectDB.cursor()    
    emote = Emote()
    emote.getInput(_message)
else: 
    # em = emote.Emote()
    runningScript = False
    pickledOn = False
    defaultCorpus = "base_corpus.py"
    SQLData = []
    SQLDataOn = False
    emoteClassOn = True
    firstTime = True
    fullCount = ""
    # connectDB = sqlite3.connect('base_corpus.db')    
    # cursor = connectDB.cursor()
    # c = connectDB.cursor()    
    emote = Emote()