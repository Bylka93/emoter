#!/usr/bin/python
# -*- coding: utf-8-*-
import os 

import time
import sys

import operator                  

import gc
import re
from nltk.tokenize import sent_tokenize
import re, math
from collections import Counter
from collections import OrderedDict
from difflib import SequenceMatcher
from string import punctuation

import numpy as np    
import fileinput
# import ast

# Import emote library
from emote import emote
WORD = re.compile(r'\w+')

class Emoter(object):

    # Emoter script is not yet written as a library or module
    emoterClassOn = False    # Is Emote being used as a library or modules? 
    runningScript = False   # Or is Emote being run as a script directly?
    firstTime = True     # Emote running for the first time?

    trainingData = {}

    ##
    # Tone Clusters (grouping related tones to create clusters, so that categorizations are more general, and accurate)
    negative_tones_cluster = [
                                "negative", "vulgarity"
                             ]

    positive_tones_cluster = [
                                "positive", "love", "joy", "admiration", "pride"
                             ]

    joy_tones_cluster = [
                            "positive", "love", "joy", "admiration"
                        ]   

    anger_tones_cluster = [
                            "anger", "hate", "accusative", "vulgarity"
                          ]

    sad_tones_cluster = [                  
                            "regret", "negative"
                        ]

    # tones that make up questions cluster (is the user asking a question?)
    question_tones_cluster = [
                                "inquisitive", "confusion", "challenging"
                             ] 

    # tones that make up answers cluster (is the user saying something certain, factual, emphatic / analytical)
    fact_tones_cluster = [
                            "emphatic", "calm", "certainty"
                         ]
    ##
                          
    # Name of the file directory an Emoter bot "brain" (the corpus files for conversation) would be located. Must be created within the data folder
    # to be able to be used and loaded interchangably, along with other corpus files.
    # brain_path = ""

    # different types of messages and response pairs for various conversations                                                                   
    texts_encouragement_needed = []
    texts_criticism_needed = []
    texts_apologetic = []
    texts_questions = []
    texts_facts = []
    texts_greetings = []
    texts_salutations = []
    texts_all = {}

    # Counter of conversation so far
    # num_total_messages = 0
    # num_user_messages = 0
    # num_bot_messages = 0

    # Overall tone levels of the conversation // not yet added
    # overall_conv_tone_lvls = {}
    # user_analysis = {}


    def __init__(self, brain_path = None, message = "", msg_em_results = {}, msg_em_results_dict_full = {}, msg_em_results_dict_strong = {}, msg_em_results_dict_strong_sorted = {},
                 tone_clusters_weights_dict = {}, strongest_tone_clusters = {}, msg_is_positive = False, msg_is_negative = False, msg_is_question = False, msg_is_fact = False,
                 msg_is_anger = False, msg_is_joy = False, msg_is_sad = False, msg_is_emphatic = False, msg_is_desire = False, msg_is_instructive = False, msg_is_certainty = False,
                 msg_is_intensity = False, msg_is_challenging = False, msg_is_confusion = False, msg_is_accusative = False, msg_analysis_description = "", sim_val = 0,
                 response_found = False, default_eliminated = False, matchingStatementResponse = ""
               ):
       self.message = message
       self.brain_path = brain_path
       # if brain_path is None:                # If no input is given..
           # self.brain_path = "fitness_coach" # The default corpus consists of dialog of a virtual fitness coach
           # brain_path = self.brain_path
       # else:
           # self.brain_path = brain_path
       self.msg_em_results = msg_em_results
       self.msg_em_results_dict_full = msg_em_results_dict_full
       self.msg_em_results_dict_strong = msg_em_results_dict_strong; self.msg_em_results_dict_strong_sorted = msg_em_results_dict_strong_sorted
       self.tone_clusters_weights_dict = tone_clusters_weights_dict
       self.strongest_tone_clusters = strongest_tone_clusters
       self.msg_is_positive = msg_is_positive; self.msg_is_negative = msg_is_negative; self.msg_is_question = msg_is_question; self.msg_is_fact = msg_is_fact
       self.msg_is_anger = msg_is_anger; self.msg_is_joy = msg_is_joy; self.msg_is_sad = msg_is_sad; self.msg_is_emphatic = msg_is_emphatic; self.msg_is_desire = msg_is_desire
       self.msg_is_instructive = msg_is_instructive; self.msg_is_certainty = msg_is_certainty; self.msg_is_intensity = msg_is_intensity; self.msg_is_challenging = msg_is_challenging
       self.msg_is_confusion = msg_is_confusion; self.msg_is_accusative = msg_is_accusative
       self.msg_analysis_description = msg_analysis_description
       self.sim_val = sim_val # Similarity value between the message string and response pair string in database
       self.response_found = response_found     # Has the bot found a response yet? (while looping and searching through texts database)
       self.default_eliminated = default_eliminated # Have the default categories within the texts database been eliminated?
       self.matchingStatementResponse = matchingStatementResponse


    def getMsg(self, _message):
        global firstTime
        global runningScript
        global emoterClassOn
        # global num_total_messages
        # global num_user_messages
        global trainingData
        if runningScript == True:
            if firstTime == False:
                self.response_found = False
                self.default_eliminated = False
                self.message = input('\n\n\t  Y O U: ')
                _message = self.message
                # num_total_messages+=1
                # num_user_messages+=1
                self.msg_em_results = emote.runAnalysis(_message)
                os.system('cls')
                print('\n\tEmoter  ' + self.brain_path + '  Analysis Report',)
                # print('\n\tOverall Conversation Levels: ', )
                print('\n\tYour message was: ', _message)
                self.analyzeMessage(_message)
                self.findMsgResponse(_message)
            else: 
                os.system('cls')
                self.brain_path = input("\n\tType in the folder dir (within /data) of the Emoter brain_path you wish to run: \
                    \n\n\t(Just press enter to load the default corpus, which is currently fitness_coach)\n\t")
                if self.brain_path is "":
                    self.brain_path = "fitness_coach"
                print("""\n\n\tNow starting Emoter with loaded corpus  """, self.brain_path)
                # print("""\n\n\tTraining database with loaded Emoter module: """, "fitness coach")
                firstTime = False
                self.trainDatabase(_brain_path = None)
                self.getMsg(_message)
        else:
            if firstTime == True:
                if self.brain_path is None:
                    self.brain_path = "fitness_coach"
                print("\n\tRunning Emoter agent  " + self.brain_path + "  as a library for first time..")
                self.message = _message
                emoterClassOn = True
                firstTime = False
                self.trainDatabase(_brain_path = None)
                self.msg_em_results = emote.runAnalysis(_message)
                self.analyzeMessage(_message)
                self.findMsgResponse(_message)
            else:
                emoterClassOn = True
                self.response_found = False
                self.default_eliminated = False
                self.message = _message
                self.msg_em_results = emote.runAnalysis(_message)
                self.analyzeMessage(_message)
                self.findMsgResponse(_message)
                print("\n\t", self.matchingStatementResponse)
                # Emoter parses tuples into lists but doesn't do a very good job. Fix this sometime
                if self.matchingStatementResponse.startswith(' "'):
                    self.matchingStatementResponse = self.matchingStatementResponse.replace(self.matchingStatementResponse, self.matchingStatementResponse[2:])
                if self.matchingStatementResponse.endswith(')'):
                    self.matchingStatementResponse = self.matchingStatementResponse.replace(self.matchingStatementResponse, self.matchingStatementResponse[:-2])
                if self.matchingStatementResponse.endswith('"'):
                    self.matchingStatementResponse = self.matchingStatementResponse.replace(self.matchingStatementResponse, self.matchingStatementResponse[:-1])
                if self.matchingStatementResponse.endswith('"),'):
                    self.matchingStatementResponse = self.matchingStatementResponse.replace(self.matchingStatementResponse, self.matchingStatementResponse[:-3])
                if self.matchingStatementResponse.startswith('"'):
                    self.matchingStatementResponse = self.matchingStatementResponse.replace(self.matchingStatementResponse, self.matchingStatementResponse[1:])
                return self.matchingStatementResponse


    # By default, the initial trained corpus for the Emoter library is the fitness_coach (located within the data folder.)
    # To make your own Emoter library with a default corpus, just edit the brain_path default parameter below, with the string
    # being the file directory name of your new bot's corpus files (which must be located within Emoter's data directory).
    # Otherwise, if you are running Emoter as a class or library, you can call emoter.trainDatabase(dir_path) to load
    # different corpuses stored in the data folder.

    def trainDatabase(self, _brain_path):
        global texts_all
        if _brain_path is None:
            _brain_path = self.brain_path
        else:
            self.brain_path = _brain_path
        global texts_encouragement_needed; global texts_criticism_needed; global texts_questions; global texts_facts;  global texts_apologetic;
        global texts_tasks; global texts_greetings; global texts_salutation;

        # See fitness_coach texts (used as default texts below) for an example on conversation texts
        # Customize the data below to make your own Emoter chatbot to use as a library
        # Texts should be a list of tuples. First element of the tuple should be a user message, and the second element is the paired bot response.
        # Add more conversations / texts as needed for every Emoter agent persona

        texts_greetings = []; texts_salutations = []; texts_encouragement_needed = []; texts_criticism_needed = []
        texts_questions = []; texts_facts = []; texts_tasks = []; texts_apologetic = []

        texts_all = {}

        texts_all['all'] = []

        texts_all['greetings'] = []

        texts_all['salutations'] = []

        texts_all['encouragement_needed'] = []

        texts_all['criticism_needed'] = []
        
        texts_all['questions'] = []

        texts_all['facts'] = []

        texts_all['tasks'] = []

        texts_all['apologetic'] = []

        # Reads text files in bot folders within /data, loading text to the corresponding corpus categories.
        print("\n\tReading text corpus from..", self.brain_path)
        dir = os.path.abspath(os.path.dirname(__file__))
        # dir = os.path.dirname(__file__)
        # path = os.path.join(dir, 'data', 'base_corpus.pickle')

        # Because of the way Emoter is parsing text files right now, the matchingStatementResponse value has to remove the last character, which will be a ')' after the end quotes.
        # try:    
        path = os.path.join(dir, 'data', self.brain_path, 'texts_all.txt')
        with open(path, 'r', encoding = 'utf8', errors = 'ignore') as f:
            for bline in f:
                try:
                    line = tuple(re.split(r'\t+', bline.strip()))
                    texts_all['all'].append(line)
                except UnicodeDecodeError:
                    continue
                # texts_all['all'] = [ast.literal_eval(line) for line in f]
                # texts_all['all'] = [tuple(map(str, i.split('),'))) for i in f]
                # if path[]
                # texts_all['all'] = [tuple(line.strip().split('",')) for line in f.readlines()]
            # print("\n\t",texts_all['all'])
        # except:
            # print("\n\tError retrieving file 'texts_all.txt' for corpus.")
            # pass
        try:
            path = os.path.join(dir, 'data', self.brain_path, 'texts_greetings.txt')
            with open(path) as f:
                # texts_all['greetings'] = [ast.literal_eval(line) for line in f]
                # texts_all['greetings'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['greetings'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_greetings.txt' for corpus.")
            pass
        try:
            path = os.path.join(dir, 'data', self.brain_path, 'texts_salutations.txt')
            with open(path) as f:
                # texts_all['salutations'] = [ast.literal_eval(line) for line in f]
                # texts_all['salutations'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['salutations'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_salutations.txt' for corpus.")
            pass
        try:           
            path = os.path.join(dir, 'data', self.brain_path, 'texts_encouragement_needed.txt')
            with open(path) as f:
                # texts_all['encouragement_needed'] = [ast.literal_eval(line) for line in f]
                # texts_all['encouragement_needed'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['encouragement_needed'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_encouragement_needed.txt' for corpus.")
            pass
        try:           
            path = os.path.join(dir, 'data', self.brain_path, 'texts_criticism_needed.txt')
            with open(path) as f:
                # texts_all['crticisim_needed'] = [ast.literal_eval(line) for line in f]
                # texts_all['criticism_needed'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['criticism_needed'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_criticism_needed.txt' for corpus.")
            pass
        try:           
            path = os.path.join(dir, 'data', self.brain_path, 'texts_questions.txt')
            with open(path) as f:
                # texts_all['questions'] = [ast.literal_eval(line) for line in f]
                # texts_all['questions'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['questions'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_questions.txt' for corpus.")
            pass
        try:
            path = os.path.join(dir, 'data', self.brain_path, 'texts_facts.txt')
            with open(path) as f:
                # texts_all['facts'] = [ast.literal_eval(line) for line in f]
                # texts_all['facts'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['facts'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_facts.txt' for corpus.")
            pass
        try:
            path = os.path.join(dir, 'data', self.brain_path, 'texts_tasks.txt')
            with open(path) as f:
                # texts_all['tasks'] = [ast.literal_eval(line) for line in f]
                # texts_all['tasks'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['tasks'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_tasks.txt' for corpus.")
            pass
        try:     
            path = os.path.join(dir, 'data', self.brain_path, 'texts_apologetic.txt')
            with open(path) as f:
                # texts_all['apologetic'] = [ast.literal_eval(line) for line in f]
                # texts_all['apologetic'] = [tuple(map(str, i.split(','))) for i in f]
                texts_all['apologetic'] = [tuple(line.strip().split('",')) for line in f.readlines()]
        except:
            print("\n\tError retrieving file 'texts_apologetic.txt' for corpus.")
            pass
        # Randomize conversations / texts with numpy, so the same response isn't found every time something is said (since multiple appropriate responses is desirable)
        # The shuffling is done once when Emoter loads the initial training data. To reshuffle, just call the function trainDatabase(path_dir) again.
        np.random.shuffle(texts_all['greetings'])
        np.random.shuffle(texts_all['salutations'])
        np.random.shuffle(texts_all['encouragement_needed'])
        np.random.shuffle(texts_all['criticism_needed'])
        np.random.shuffle(texts_all['questions'])
        np.random.shuffle(texts_all['facts'])
        np.random.shuffle(texts_all['tasks'])
        np.random.shuffle(texts_all['apologetic'])
        np.random.shuffle(texts_all['all'])

        # texts_all['encouragement_needed'] = texts_encouragement_needed; texts_all['criticism_needed'] = texts_criticism_needed; texts_all['questions'] = texts_questions; texts_all['facts'] = texts_facts;
        # texts_all['tasks'] = texts_tasks;  texts_all['apologetic'] = texts_apologetic; texts_all['greetings'] = texts_greetings; texts_all['salutations'] = texts_salutations
        print("\n\tNow beginning initial Emote analysis (required on every restart) with demo data..")
        if runningScript == True:
            emote.runAnalysis("")
            print("\n\tFinished required initial analysis test.")
        # return _brain_path
        return texts_all


    def parseMessage(self, _message):
        tone_1 = ""; tone_2 = ""; tone_3 = ""; tone_4 = ""; tone_5 = ""; tone_6 = ""; tone_7 = ""; tone_8 = ""
        tone_1_val = 0; tone_2_val = 0; tone_3_val = 0; tone_4_val = 0; tone_5_val = 0; tone_6_val = 0; tone_7_val = 0; tone_8_val = 0
        tone_1 = self.msg_em_results[0][0]; tone_1_val = self.msg_em_results[0][1]; 
        tone_2 = self.msg_em_results[1][0]; tone_2_val = self.msg_em_results[1][1] 
        tone_3 = self.msg_em_results[2][0]; tone_3_val = self.msg_em_results[2][1] 
        tone_4 = self.msg_em_results[3][0]; tone_4_val = self.msg_em_results[3][1] 
        tone_5 = self.msg_em_results[4][0]; tone_5_val = self.msg_em_results[4][1] 
        tone_6 = self.msg_em_results[5][0]; tone_6_val = self.msg_em_results[5][1] 
        tone_7 = self.msg_em_results[6][0]; tone_7_val = self.msg_em_results[6][1] 
        tone_8 = self.msg_em_results[7][0]; tone_8_val = self.msg_em_results[7][1] 
        self.msg_em_results_dict_full = {}
        self.msg_em_results_dict_full['tone_1'] = [tone_1, tone_1_val]; self.msg_em_results_dict_full['tone_2'] = [tone_2, tone_2_val]; 
        self.msg_em_results_dict_full['tone_3'] = [tone_3, tone_3_val]; self.msg_em_results_dict_full['tone_4'] = [tone_4, tone_4_val]; 
        self.msg_em_results_dict_full['tone_5'] = [tone_5, tone_5_val]; self.msg_em_results_dict_full['tone_6'] = [tone_6, tone_6_val]; 
        self.msg_em_results_dict_full['tone_7'] = [tone_7, tone_7_val]; self.msg_em_results_dict_full['tone_8'] = [tone_8, tone_8_val]; 
        # print("\n\tMessage results analysis full dictionary: ", msg_em_results_dict_full)
        self.msg_em_results_dict_strong = {}
        self.msg_em_results_dict_strong['tone_1'] = [tone_1, tone_1_val]; self.msg_em_results_dict_strong['tone_2'] = [tone_2, tone_2_val]; 
        self.msg_em_results_dict_strong['tone_3'] = [tone_3, tone_3_val]; self.msg_em_results_dict_strong['tone_4'] = [tone_4, tone_4_val]; 
        # msg_em_results_dict_strong['tone_5'] = [tone_5, tone_5_val]
        print("\n\tStrongest tones detected: ", "\n\t\t", self.msg_em_results[0][0], self.msg_em_results[0][1], "\t", 
                self.msg_em_results[1][0], self.msg_em_results[1][1], "\t", self.msg_em_results[2][0], self.msg_em_results[2][1],
              "\n\t\t", self.msg_em_results[3][0], self.msg_em_results[3][1], "\t", self.msg_em_results[4][0], self.msg_em_results[4][1])
        self.strongest_detected_tone = str(self.msg_em_results_dict_strong['tone_1'][0])
        self.strongest_detected_tone_val = str(self.msg_em_results_dict_strong['tone_1'][1])
        self.classifyToneClusters(_message)
        return self.msg_em_results_dict_strong


    def classifyToneClusters(self, _message):
        global texts_greetings
        print("\n\tCalculating tone cluster weights..")
        positive_tones_cluster_weight = 1; negative_tones_cluster_weight = 1; joy_tones_cluster_weight = 1; anger_tones_cluster_weight = 1;
        sad_tones_cluster_weight = 1; question_tones_cluster_weight = 1; fact_tones_cluster_weight = 1;
        for tone, value in self.msg_em_results_dict_strong.items():
            for i in range(len(self.positive_tones_cluster)):
                if value[0] == self.positive_tones_cluster[i]:
                    positive_tones_cluster_weight = positive_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tPositive tones cluster weight: ", (round(positive_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.negative_tones_cluster)):
                if value[0] == self.negative_tones_cluster[i]:
                    negative_tones_cluster_weight = negative_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tNegative tones cluster weight: ", (round(negative_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.joy_tones_cluster)):
                if value[0] == self.joy_tones_cluster[i]:
                    joy_tones_cluster_weight = joy_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tJoy tones cluster weight: ", (round(joy_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.anger_tones_cluster)):
                if value[0] == self.anger_tones_cluster[i]:
                    anger_tones_cluster_weight = anger_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tAnger tones cluster weight: ", (round(anger_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.sad_tones_cluster)):
                if value[0] == self.sad_tones_cluster[i]:
                    sad_tones_cluster_weight = sad_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tSad tones cluster weight: ", (round(sad_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.question_tones_cluster)):
                if value[0] == self.question_tones_cluster[i]:
                    question_tones_cluster_weight = question_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tQuestions tones cluster weight: ", (round(question_tones_cluster_weight, 2)))
                else:
                    pass
            for i in range(len(self.fact_tones_cluster)):
                if value[0] == self.fact_tones_cluster[i]:
                    fact_tones_cluster_weight = fact_tones_cluster_weight * math.sqrt(value[1])
                    # print("\t\t\tFacts tones cluster weight: ", (round(fact_tones_cluster_weight, 2)))
                else:
                    pass

        self.tone_clusters_weights_dict = {'positive': positive_tones_cluster_weight, 'negative': negative_tones_cluster_weight, 
                                      'joy': joy_tones_cluster_weight, 'anger': anger_tones_cluster_weight,
                                      'sad': sad_tones_cluster_weight, 'question': question_tones_cluster_weight
                                     }
        self.tone_clusters_weights_dict = sorted(self.tone_clusters_weights_dict.items(), key = operator.itemgetter(1),reverse = True)

        # print("\t  Tone cluster weights: ", tone_clusters_weights_dict)
        return self.tone_clusters_weights_dict


    def analyzeMessage(self, _message):
        self.parseMessage(_message)
        self.strongest_tone_clusters = {}
        self.tone_cluster_1 = self.tone_clusters_weights_dict[0][0]; self.tone_cluster_1_val = self.tone_clusters_weights_dict[0][1];
        self.tone_cluster_2 = self.tone_clusters_weights_dict[1][0]; self.tone_cluster_2_val = self.tone_clusters_weights_dict[1][1];
        self.tone_cluster_3 = self.tone_clusters_weights_dict[2][0]; self.tone_cluster_3_val = self.tone_clusters_weights_dict[2][1];
        self.tone_cluster_4 = self.tone_clusters_weights_dict[3][0]; self.tone_cluster_4_val = self.tone_clusters_weights_dict[3][1];
        # If tone cluster weights are greater than their default values..
        if self.tone_cluster_1_val > 1:
            self.strongest_tone_clusters['1'] = self.tone_cluster_1
        else:
            pass
        if self.tone_cluster_2_val > 1:
            self.strongest_tone_clusters['2'] = self.tone_cluster_2
        else:
            pass
        if self.tone_cluster_3_val > 1:
            self.strongest_tone_clusters['3'] = self.tone_cluster_3
        else:
            pass
        if self.tone_cluster_4_val > 1:
            self.strongest_tone_clusters['4'] = self.tone_cluster_4
        else:
            pass
        # print("\n\tStrongest tone clusters: ", tone_cluster_1, "\t", tone_cluster_2, "\t", tone_cluster_3, "\t")
        self.msg_em_results_dict_strong_sorted = sorted(self.msg_em_results_dict_strong.items(),key = operator.itemgetter(0))
        # print("\n\tSorted strongest individual tones: ", msg_em_results_dict_strong_sorted)
        print("\n\tCreating analysis report based on tone grouping..")
        self.msg_is_positive = False; self.msg_is_negative = False; self.msg_is_question = False; self.msg_is_fact = False; self.msg_is_anger = False; self.msg_is_joy = False; 
        self.msg_is_sad = False; self.msg_is_emphatic = False; self.msg_is_desire = False; self.msg_is_instructive = False; self.msg_is_certainty = False;
        self.msg_is_intensity = False; self.msg_is_challenging = False; self.msg_is_confusion = False; self.msg_is_accusative = False;  
        self.msg_analysis_description = ""
        # Some emotional classifications work better as clusters (joy, anger, negative, positive) because they're more encompassing, 
        # whereas other tones are significant enough on their own (emphatic, desire, instructive, etc.)
        for key, value in self.strongest_tone_clusters.items():
            print("\n\t\t", key, "\t", value)
            if value == 'positive':
                self.msg_is_positive = True
                self.msg_analysis_description+=("\n\t\tUser expresssed a positive sentiment. ")
            if value == 'negative': 
                self.msg_is_negative = True
                self.msg_analysis_description+=("\n\t\tUser expresssed a negative sentiment. ")
            if value == 'question':
                self.msg_is_question = True
                self.msg_analysis_description+=("\n\t\tUser is asking a question or expressing a request. ")
            if value == 'fact':
                self.msg_is_fact = True
                self.msg_analysis_description+=("\n\t\tUser is making a definite statement or opinion. ")
            if value == 'anger':
                self.msg_is_anger = True
                self.msg_analysis_description+=("\n\t\tUser is feeling angry or impatient or hateful. ")
            if value == 'joy':
                self.msg_is_joy = True
                self.msg_analysis_description+=("\n\t\tUser is feeling joyous or enthusiastic. ")
            if value == 'sad':
                self.msg_is_sad = True
                self.msg_analysis_description+=("\n\t\tUser is feeling unhappy or regretful. ")
        for key, value in self.msg_em_results_dict_strong.items():
            if value[0] == 'emphatic':
                self.msg_is_emphatic = True
                self.msg_analysis_description+=("\n\t\tUser's sentiment is emphatic and / or analytical. ")
            if value[0] == 'desire':
                self.msg_is_desire = True
                self.msg_analysis_description+=("\n\t\tUser is expressing desire, or wanting something. ")
            if value[0] == 'instructive':
                self.msg_is_instructive = True
                self.msg_analysis_description+=("\n\t\tUser is being instructive or giving a task. ")
            if value[0] == 'certainty':
                self.msg_is_certainty = True
                self.msg_analysis_description+=("\n\t\tUser is certain about what was said. ")
            if value[0] == 'intensity':
                self.msg_is_intensity = True
                self.msg_analysis_description+=("\n\t\tUser is expressing strong feelings. ")
            if value[0] == 'challenging':
                self.msg_is_challenging = True
                self.msg_analysis_description+=("\n\t\tUser is being challenging, discouraging, or disagreeable. ")
            if value[0] == 'confusion':
                self.msg_is_confusion = True
                self.msg_analysis_description+=("\n\t\tUser is expressing uncertainty or confusion. ")
            if value[0] == 'accusative':
                self.msg_is_accusative = True
                self.msg_analysis_description+=("\n\t\tUser is expressing or asking something accusative in nature. ")
        print("\n\tMessage analysis description: ", self.msg_analysis_description)
        # Will need to keep track of overall number of messages and maintain appropriate overall conversation levels
        # print("\n\tNumber of messages in conversation: ", num_total_messages)
        return self.msg_analysis_description


    # Begin process for determining bot response
    def findMsgResponse(self, _message):
        global texts_all
        np.random.shuffle(texts_all['all'])
        # print("\n\tFull text database: ", texts_all)
        # Based on message tones (booleans), find the right database. nested branching structures
        # Add your own branches based on how the bot should respond
        if self.response_found:
            # print("\n\tMatching response found!: ", self.matchingStatementResponse)
            print("\n\tMatching response found!: ", self.matchingStatementResponse[:-1])
            # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
            return self.matchingStatementResponse
        else:
            print("\n\tNow determining best possible agent response..")
            self.matchingStatementResponse = ""
            # Change these around based on what makes sense according to the personality?
            # General presets..
            # If the user is angry, look for messages that are apologetic / sympathetic
            if self.msg_is_anger:
                self.text_db_to_search = []
                self.text_db_to_search = texts_all['apologetic']
                self.new_text_db_to_search = 'apologetic'
                self.searchDatabase(_message)
            # If the user is being negative, look for messages that are encouraging / positive
            if self.msg_is_sad or self.msg_is_negative:
                self.text_db_to_search = []
                self.text_db_to_search = texts_all['encouragement_needed']
                self.new_text_db_to_search = 'encouragement_needed'
                self.searchDatabase(_message)
            # If the user is being accusative or difficult, respond with defensiveness 
            # (probably have to be careful with this for a customer service bot or something)
            if self.msg_is_accusative or self.msg_is_challenging:
                self.text_db_to_search = texts_all['criticism_needed']
                self.new_text_db_to_search = 'criticism_needed'
                self.searchDatabase(_message)
            # If the user is asking a question or giving instructions, respond with some acknowledgement
            # of performing the requested task.
            if self.msg_is_question or self.msg_is_instructive:
                self.text_db_to_search = texts_all['tasks']
                self.new_text_db_to_search = 'tasks'
                self.searchDatabase(_message)
            # If the user is simply stating something, look for statements to respond back with.
            if self.msg_is_fact or self.msg_is_emphatic:
                self.text_db_to_search = texts_all['facts']
                self.new_text_db_to_search = 'facts'
                self.searchDatabase(_message)

        # If no responses are found in the selected response category, then Emoter will look for matching responses
        # based on similarity of the inputted message in its entire conversation corpus.


    def searchDatabase(self, _message):
        global texts_all
        print("\n\tText database to search (eliminate:  greetings, salutations) : \n", "\t\t*", self.new_text_db_to_search, "*\n")

        # These thresholds and loops determine personalities of Emoter chatbots. How likely is an agent to give responses, based on designed personality traits?
        # These thresholds should be edited and manipulated as needed per persona.
        # Eventually, the thresholds need to scale inversely proportionally to the number of words in a given message. So if a user asks a question that's only 
        # 3 words, for example, then the threshold should be higher because that requires a more specific answer. For longer messages, the threshold should 
        # become smaller with scale, because the bot is less likely to find a matching response for longer sequences.

        lastVal = 0
        comparedVal = 0
        threshold = .99
        try:
            if not self.response_found and not self.default_eliminated:
                threshold = .99
                # print("\n\tSearching greetings..")
                _message = _message.lower()
                _message = self.strip_punctuation(_message)
                for each in texts_all['greetings']:
                    each_str = str(each[0])
                    each_str = each_str.lower()
                    each_str = self.strip_punctuation(each_str)
                    lastVal = comparedVal
                    comparedVal = self.compareSimilarities(_message, each_str)
                    print("\n\t", each_str, comparedVal)
                    if comparedVal > lastVal:
                        lastVal = comparedVal
                    if lastVal >= threshold:
                        self.response_found = True
                        self.matchingStatementResponse = each[1]
                        print("\n\tBest possible response found.")
                        print("\n\n\t  Y O U : ", "\t", _message)
                        print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse[:-1])
                        # print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse)
                        if not self.emoterClassOn and runningScript:
                            self.getMsg(_message)
                        else:
                            return self.matchingStatementResponse
                            # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
                    # print("Compared val with: ", "\t", comparedVal, "\t", each[0])
                    if lastVal <= threshold:
                        if threshold >= .75:
                            threshold -= .05
                            # print("\n\tNo matching response found.. lowering threshold.\t", threshold)
                        else:
                            # print("\n\tScanning other databases..")
                            self.response_found = False
                            # self.default_eliminated = True
                            pass
        except:
            pass
        try:
            if not self.response_found and not self.default_eliminated:
                threshold = .99
                _message = _message.lower()
                _message = self.strip_punctuation(_message)
                for each in texts_all['salutations']:
                    # print("\n\tSearching salutations..")
                    # compareSimilarities(message, each[0])
                    each_str = str(each[0])
                    each_str = each_str.lower()
                    each_str = self.strip_punctuation(each_str)
                    lastVal = comparedVal
                    comparedVal = self.compareSimilarities(_message, each_str)
                    # print("\n\t", each_str, comparedVal)
                    if comparedVal > lastVal:
                        lastVal = comparedVal
                    if lastVal >= threshold:
                        self.response_found = True
                        self.matchingStatementResponse = each[1]
                        print("\tBest possible response found.")
                        print("\n\n\t  Y O U : ", "\t", _message)
                        print("\n\n\t  E M O T E R  : ", "\t", self.matchingStatementResponse[:-1])
                        # print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse)
                        if not self.emoterClassOn and runningScript:
                            self.getMsg(_message)
                        else:
                            return self.matchingStatementResponse
                            # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
                    # print("Compared val with: ", "\t", comparedVal, "\t", each[0])
                    if lastVal < threshold:
                        if threshold >= .75:
                            threshold -= .05
                            # print("\n\tNo matching response found.. lowering threshold.\t", threshold)
                        else:
                            # print("\n\tScanning other databases..")
                            self.response_found = False
                            self.default_eliminated = True
                            pass
        except:
            pass
        try:
            if not self.response_found:
                threshold = .99
                _message = _message.lower()
                _message = self.strip_punctuation(_message)
                for each in texts_all[self.new_text_db_to_search]:
                    each_str = str(each[0])
                    each_str = each_str.lower()
                    each_str = self.strip_punctuation(each_str)
                    lastVal = comparedVal
                    comparedVal = self.compareSimilarities(_message, each_str)
                    # print("\n\t", each_str, comparedVal)
                    if comparedVal > lastVal:
                        lastVal = comparedVal
                    if lastVal >= threshold:
                        self.response_found = True
                        self.matchingStatementResponse = each[1]
                        print("\tBest possible response found.")
                        print("\n\n\t  Y O U : ", "\t", _message)
                        print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse[:-1])  
                        # print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse)
                        if not self.emoterClassOn and runningScript:
                            self.getMsg(_message)
                        else:
                            return self.matchingStatementResponse
                            # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
                    if lastVal < threshold:
                        if threshold >= .65:
                            threshold -= .05
                            # print("\n\tNo matching response found in:", new_text_db_to_search, "lowering threshold.\t", threshold)
                        else:
                            # print("\n\tScanning other databases..")
                            self.response_found = False
                            pass
        except:
            pass
                    # getMsg()
        # If resposne can't be found in matching database, just look through everything.
        # For now, it looks through "all" the texts, but eventually, it should look for second, third, or even fourth and fifth closest matching text / conversation.
        try:
            if not self.response_found:
                threshold = 1.0
                _message = _message.lower()
                _message = self.strip_punctuation(_message)
                for each in texts_all['all']:
                    # print("\n\tLENGTH OF TEXTS: ", len(texts_all['all']))
                    # print("\n\tEACH IN ALL: ", each)
                    each_str = str(each[0])
                    each_str = each_str.lower()
                    each_str = self.strip_punctuation(each_str)
                    lastVal = comparedVal
                    comparedVal = self.compareSimilarities(_message, each_str)
                    # print("\n\t", each_str, comparedVal)
                    # print("\n\t", each, each_str, comparedVal, lastVal, threshold)
                    if comparedVal > lastVal:
                        lastVal = comparedVal
                    if lastVal >= threshold:
                        self.response_found = True
                        self.matchingStatementResponse = each[1]
                        print("\tBest possible response found.")
                        print("\n\n\t  Y O U : ", "\t", _message)
                        print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse[:-1])
                        # print("\n\n\t  E M O T E R : ", "\t", self.matchingStatementResponse)
                        if not self.emoterClassOn and runningScript:
                            self.getMsg(_message)
                        else:
                            return self.matchingStatementResponse
                            # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
                    if lastVal < threshold:
                        if threshold > 0:
                            threshold -= .001
                            # print("\n\tNo matching response found.. lowering threshold.\t", threshold)
                        else:
                            # print("\n\n\tAgent failiure. Could not find response in database! Please try again.")
                            self.response_found = False
                            if not self.emoterClassOn and runningScript:
                                self.getMsg(_message)
        except:
            pass
        # self.matchingStatementResponse = self.matchingStatementResponse[:-1]
        # return self.matchingStatementResponse


    # Determine sentence similarities through Python's SequenceMatcher

    def compareSimilarities(self, inputted_user_msg, stored_user_msgs):
        # get_cosine(inputted_user_msg, stored_user_msg_match)
        # print("\n\tComparing: ", "\t", inputted_user_msg, "\t", stored_user_msgs)
        self.sim_val = self.get_cosine(inputted_user_msg, stored_user_msgs)
        # self.sim_val = self.similar(inputted_user_msg, stored_user_msgs)
        return self.sim_val

    # Python code for similarities
    # def similar(self, a, b):
    #     return SequenceMatcher(None, a, b).ratio()

    def strip_punctuation(self, s):
        return ''.join(c for c in s if c not in punctuation)

    # Cosine Similarities

    def get_cosine(self, vec1, vec2):
        vec1 = self.text_to_vector(str(vec1))
        vec2 = self.text_to_vector(str(vec2))
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
         words = WORD.findall(text)
         return Counter(words)


if __name__ == '__main__':
    runningScript = True
    firstTime = True
    emoterClassOn = False
    _message = ""
    brain_path = "" # Default conversation corpus
    emoter = Emoter(brain_path)
    emoter.getMsg(_message)

else:
    runningScript = False
    emoterClassOn = True
    firstTime = True
    emoter = Emoter(brain_path = "") # Default conversation corpus