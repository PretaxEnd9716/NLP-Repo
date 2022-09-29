from fileinput import filename
import os

import nltk
from nltk import word_tokenize
from nltk.util import ngrams

import pickle

import math

def main():
    #Get all predictions 
    predictions = predictText("Data/LangId.test")

    #Calculate and output accuracy
    print("\nAccuracy: ", accuracy("Data/LangId.sol", predictions))


#Calculates Accuracy
def accuracy(filename, predictions):
    #Open solution files
    solFile = open(os.path.join(os.path.dirname(__file__), filename), 'r')
    solLines = solFile.readlines()

    #Read each line and check whether our predictions were correct
    print("\nPredicted/Actual")
    i = 0
    correct = 0
    for line in solLines:
        #Obtain correct language
        lang = line.split(" ")[1]
        lang = lang.replace('\n', '')

        #Check whether prediction was correct
        if lang == predictions[i]:
            correct += 1
        else:
            print("Line {}: {}/{}".format(i, predictions[i], lang))
        i += 1

    solFile.close()

    return correct/i

#Predicts each line of the test file
def predictText(fileName):
    #Read Pickle Files
    uniEng = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/uniEng.p'), 'rb'))
    biEng = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/biEng.p'), 'rb'))
    englishLen = trainingLen(uniEng)

    uniFre = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/uniFre.p'), 'rb'))
    biFre = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/biFre.p'), 'rb'))
    frenchLen = trainingLen(uniFre)
    
    uniIta = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/uniIta.p'), 'rb'))
    biIta = pickle.load(open(os.path.join(os.path.dirname(__file__), 'Data/biIta.p'), 'rb'))
    italianLen = trainingLen(uniIta)

    #Open Files
    testFile = open(os.path.join(os.path.dirname(__file__), fileName), 'r')
    testLines = testFile.readlines()

    #Read each line and predict each language
    predictions = []
    for line in testLines:
        engProb = computeProb(line, uniEng, biEng, englishLen + italianLen + frenchLen)
        freProb = computeProb(line, uniFre, biFre, englishLen + italianLen + frenchLen)
        itaProb = computeProb(line, uniIta, biIta, englishLen + italianLen + frenchLen)

        if(max(engProb, freProb, itaProb) == engProb):
            predictions.append("English") 
        elif(max(engProb, freProb, itaProb) == freProb):
            predictions.append("French")
        else:
            predictions.append("Italian") 

    testFile.close()

    return predictions

#Computes the probability of a line's language from a given language model
def computeProb(line, unigramDict, bigramDict, trainingLength):
    #Gets n-grams of the line
    uniLine = word_tokenize(line)
    biLine = list(ngrams(uniLine, 2))

    #Compute probability
    lp = 1
    for bigram in biLine:
        n = bigramDict[bigram] if bigram in bigramDict else 0 
        d = unigramDict[bigram[0]] if bigram[0] in unigramDict else 0

        lp = lp * ((n + 1) / (d + len(unigramDict)))

    return lp

#Get the number of tokens in the training length
def trainingLen(unigrams):
    length = 0

    #Go through each value and add to length
    for l in unigrams.values():
        length += l

    return length

if __name__ == "__main__":
    main()