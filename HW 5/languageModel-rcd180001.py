from fileinput import filename
import os

import nltk
from nltk import word_tokenize
from nltk.util import ngrams

import pickle

def main():
    #Training File Paths
    englishTrain = "Data/LangId.train.English"
    frenchTrain = "Data/LangId.train.French"
    ItalianTrain = "Data/LangId.train.Italian"

    #Make N-Gram Dictionaries
    uniEng, biEng = langModel(englishTrain)
    uniFre, biFre = langModel(frenchTrain)
    uniIta, biIta = langModel(ItalianTrain)

    #Make pickle files
    pickle.dump(uniEng, open('HW 5/Data/uniEng.p', 'wb'))
    pickle.dump(biEng, open('HW 5/Data/biEng.p', 'wb'))
    pickle.dump(uniFre, open('HW 5/uniFre.p', 'wb'))
    pickle.dump(biFre, open('HW 5/biFre.p', 'wb'))
    pickle.dump(uniIta, open('HW 5/uniIta.p', 'wb'))
    pickle.dump(biIta, open('HW 5/biIta.p', 'wb'))

#Creates the unigram and bigram dictionary
def langModel(fileName):
    #Opens and reads file 
    file = openFile(fileName)
    raw_text = file.read()

    #Gets tokens
    tokens = preprocess(raw_text)

    #Gets n-grams
    unigrams = list(ngrams(tokens,1))
    bigrams = list(ngrams(tokens,2))

    #Get dictionaries
    unigram_dictionary = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dictionary = {t:bigrams.count(t) for t in set(bigrams)}

    return unigram_dictionary, bigram_dictionary

#Preprocesses text and return tokens
def preprocess(raw_text):
    #Remove newlines
    raw_text = raw_text.replace('\n', '');
    
    return word_tokenize(raw_text)

#Opens given file
def openFile(filename):
    #Makes the path of the file
    path = os.path.dirname(__file__)
    trainingFile = os.path.join(path, filename)

    #Opens the file
    return open(trainingFile, "r")

if __name__ == "__main__":
    main()