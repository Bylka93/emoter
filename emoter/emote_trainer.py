# Emote Trainer Wrapper / Mass Analyzer
# Command line interface for mass analysis for Emote, and to train Emote's classification system using TextBlob's API
# Note: Training features have not yet been implemented yet
# All that's really working is mass analyzing text files through the CLI

#!/usr/bin/python
# -*- coding: utf-8-*-
encoding = "utf-8"
import os 
import sys
from emote import emote
import time
import gc
import re
import csv
import os
from nltk.tokenize import sent_tokenize

data = ""
trainingFile = ""
trainingData = []
testData = {}

openingCSV = False
openingText = False
openingPDF = False

csvOutputData = False

csvData = []
csvTextData = []
csvResults = []
csvFile = {}

massResults = []
sentences = []

def startInterface():
    global openingCSV
    global openingText
    global openingPDF
    print("\n\tNow starting Emote Mass Analyzer..")
    option = input("\n\tTo analyze a file with Emote, enter in the type name ('PDF', 'Text', or 'CSV'), or enter 'Train' or 'Test': ")
    option = option.lower()
    if option == 'pdf':
        # print("PDF file input.")
        openingPDF = True
        openPDF(path, data)
    elif option == 'text':
        # print("Text file input.")
        openingText = True
        openFile(path, data)
    elif option == 'csv':
        # print("CSV file input.")
        openingCSV = True
        parseCSV(path, csvData, csvTextData)
    elif option == 'train':
        addToDatabase(trainingFile, trainingData)
    elif option == 'test':
        testEmote(testData)
    else:
        print("\n\tBad command entered. Please try again.")
        startInterface()


def openFile(path, data):
    global csvOutputData
    path = input("\n\tEnter the name of the text and extension of the text, CSV, or PDF file (has to be in directory 'texts') to be mass analyzed in Emote: ")
    try:
        p = os.getcwd()
        p = os.path.join(p, 'texts', path)
        print(p)
        file = open(p, 'r')
        data = file.read()
        text = data
        split_into_sentences(text)
        return data
    except IOError as err:
        print("Error opening path to file.")
        # self.openFile(path, data)
            # print("\n\tI/O error({0}): {1}".format(errno, strerror))  
    option = input("\n\tOutput classification results to CSV file? (Yes / No)")
    option = option.lower()
    if option == 'yes':
        csvOutputData = True
    elif option == 'no':
        csvOutputData = False
    else:
        ("Commad not understood!")
        startInterface()
    return


def parseText(path):
    csvData = []
    csvTextData = []
    file = open(path, 'r')
    csv_file = csv.reader(file, delimiter = ",")
    for row in csv_file:
        csvData.append(row[0])
        csvTextData.append(row[1])
    file.close()
    analyzeCSV(csvData, csvTextData, massResults, csvFile)
    print("\n\t", csvData)
    print("\n\t", csvTextData)
    return csvData, csvTextData


def analyzeText(csvData, csvTextData, csvFile):
    print("\n\t",csvTextData)
    print("\n\t", csvData)
    global massResults
    massResults = []
    csvResults = {}
    csvFile = {}
    for i in range(len(csvTextData)):
        emote.getInput(csvTextData[i])
        # print(emote.normalizedProbValues)
        massResults.append(emote.normalizedProbValues)
    csvFile = open('static/results.csv', 'w', newline='')
    for i in range(len(massResults)):
        # with open('static/results.csv', 'w', newline='') as csvFile:
        csvIndRowList = []
        csvResults = csv.writer(csvFile, delimiter = ',')
        csvIndRowList.append(csvData[i])
        csvIndRowList.append(csvTextData[i])
        csvIndRowList.append(massResults[i][0])
        csvIndRowList.append(massResults[i][1])
        csvIndRowList.append(massResults[i][2])
        csvIndRowList.append(massResults[i][3])
        csvIndRowList.append(massResults[i][4])
        csvIndRowList.append(massResults[i][5])
        print("\n\tROW LIST", csvIndRowList)
        csvResults.writerow(csvIndRowList)
    csvFile.close()
    return csvResults, csvFile


def openPDF(path, data):
    return


# def openCSV(path, data):
#     path = input("\n\tEnter the name of the text and extension of the text, CSV, or PDF file (has to be in same directory) to be mass analyzed in Emote: ")
#     try:
#         with open(path) as csvfile:
#             reader = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
#             datalist = []
#             datalist = list(reader)
#             return datalist
#     except IOError as err:
#         print("Error opening path to file.")
#     startInterface()
#     return




def split_into_sentences(text):
    print("CLASSIFYING MULTIPLE SENTENCES")
    global sentences
    sentences = []
    # Code below splits sentences without NLTK Tokenizer
    # START
    # caps = "([A-Z])"
    # prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    # suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    # starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    # acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    # websites = "[.](com|net|org|io|gov)"
    # digits = "([0-9])"
    # print("\n\tTaking input file, converting to text, and splitting it up into sentences..")
    # text = " " + text + "  "
    # text = text.replace("\n"," ")
    # text = re.sub(prefixes,"\\1<prd>",text)
    # text = re.sub(websites,"<prd>\\1",text)
    # if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    # text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    # text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    # text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    # text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    # text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    # text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    # text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    # text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    # if '"' in text: text = text.replace('."','".')
    # if "\"" in text: text = text.replace(".\"","\".")
    # if "!" in text: text = text.replace("!\"","\"!")
    # if "?" in text: text = text.replace("?\"","\"?")
    # text = text.replace(".",".<stop>")
    # text = text.replace("?","?<stop>")
    # text = text.replace("!","!<stop>")
    # text = text.replace("<prd>",".")
    # sentences = text.split("<stop>")
    # sentences = sentences[:-1]
    # sentences = [s.strip() for s in sentences]
    # END
    sentences = sent_tokenize(text)
    print("\n\tSENTENCES", sentences)
    sendToEmote()
    # return sentences


def sendToEmote():
    # pickledData = pickle.load(open("base_corpus.pickle", "wb"))
    # print(emote.objectToPickle)
    # print(sentences)
    global sentences
    global massResults
    massResults = []
    print("""\n\n\tEach sentence found in the text will now be output with the strongest classification associated with it on screen.""")
    print("""\n\tEmote will classify: """ + str(len(sentences)) + " detected sentences.")
    countSentences = int(len(sentences))
    print("COUNT: ", countSentences)
    # sentences = []
    # for num, sent in enumerate(sentences):
    for m in sentences:
        print("\n\t", m)
        # print("\n\tMESSAGE, message")
        # gc.disable()
        # print("\n\tI", i)
        emote.getInput(m)
        # print("\n")
        # print("\n\tH1", message)
        # print("\n\tH2", emote.normalizedProbValues)
        # print("\n"+emote.pre_result)
        # gc.enable()
        # return emote.normalizedProbVals
        massResults.append(emote.normalizedProbValues)
    # massResult.append(emote.result)
    print("\n\tMASS:" , massResults)
    # returnAsCSV(massresults)
    # timeTotal = time.time() - timeToClassify
    # m, s = divmod(s,  60)
    # timeTotal = m + " :" + s + " "
    # print("""\n\n\n\tEmote took """ + str(timeTotal) + " time to classify the text of " + sentences.length + " detected sentences.")
    # outputOption(massResults)
    # return massResults


# Code below is not functional
def outputOption(massResults):
    option = input("\n\tOutput results into data for 'training' or 'spreadsheet' (enter one): ")
    option = option.lower()
    if option == 'training':
        print("\n\tOutputting data into traininable format.")
        outputTraining(massResults)
    elif option == 'spreadsheet':
        print("\n\tOutputting data into CSV with full results.")
        outputSpreadsheet(massResults)
    else:
        print("\n\tCommand not understood!")
        outputOption(massResults)


def outputTraining(massResults):
    startInterfaCe()


def outputSpreadsheet(massResults):
    startInterfaCe()

# Code below is not functional
def addToDatabase(trainingFile, trainingData):
    
    # USING SHELF 
    try:
        pickledData = shelve.open('base_corpus.db', writeback = True)
        train = pickledData["base"]
        # train = pickle.load(open("base_corpus.pickle", "rb" ) )
        # cl = NaiveBayesClassifier(train)
        print("\n\tLoaded pickled default database corpus.")
        # pickledData.close()
    except IOError as err:
        # print("\n\tI/O error({0}): {1}".format(errno, strerror))  
        print("\n\tError training pickle file.. system will exit. Go into the directory, delete the corrupt pickle file, and retry this script to train a new copy.")  
        # sys.exit()
    trainingFile = raw_input("\n\tEnter the directory / name of the text file to train (with extension): ")
    with open(trainingFile, "rb") as fp:
        for i in fp.readlines():
            # tmp = i.decode('string_escape')
            # tmp = i.decode('utf-8').strip()
            tmp = i.strip()
            # tmp = i.replace('\r', ' ').replace('\n', '')
            # tmp = i.replace('\\', ' ').replace('\'', '')
            # tmp = i.replace('\\', ' ').replace('\"', '')
            # i = i.strip()
            tmp = tmp.split(",")
            try:
                trainingData.append((str(tmp[0]), str(tmp[1])))
            except:
                pass
    for data in trainingData:
        try:
            pickledData["base"].append(data)
        except:
            pass
    pickledData.sync()
    pickledData.close()
    print("\n\tTraining data added to the default database corpus.")
    startInterface()

# Code below is not functional
def testEmote(testData):
    testFileLoc = input("Enter the file name of the text you would like to test against Emote for accuracy (Must be in the same directory and labelled as .txt):")
    try:
        print(str(testFileLoc))
    except:
        print("Did not find the text file.")
        startInterface()
    # for line in open (str(testFileLoc)):     
        # print(str(testFileLoc))   
        # testDataTemp = line.split()
        # testDataTemp = str(testDataTemp)
        # print(testDataTemp)
        # testData.append(testDataTemp)
        # print(testData)
    # print(testData)
    with open(str(testFileLoc)) as testData:
        print(testData)
        emote.testAccuracy(testData)
    print("\n\n\t\tTesting done.")
    startInterfaCe()

        # print("\n\tNo test data file found.")
        # startInterface()


if __name__ == '__main__':
    path = ""
    data = ""
    trainingFile = ""
    trainingData = []
    csvData = []
    csvTextData = []
    csvResults = []
    csvIndRowList = []
    testData = {}
    csvFile = {}
    massResults = []
    sentences = []
    startInterface()
else:
    path = ""
    data = ""
    trainingFile = ""
    trainingData = []
    csvData = []
    csvTextData = []
    csvResults = []
    csvIndRowList = []
    testData = {}
    csvFile = {}
    massResults = []
    sentences = []