from fileinput import filename
import os
import sys
import re

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def main():
    #Opens files
    filename = validateArgument()
    file = open(filename, "r")
    
    #Tokenize Text
    raw_text = file.read()
    tokens = word_tokenize(raw_text)

    #Prints Out Lexical Diversity
    sets = set(tokens)
    print("\nLexical Diversity: %.2f" % (len(sets) / len(tokens)))

    #Preprocess Text
    tokens = preprocess(raw_text)

    #Get unique lemmas
    uniqueLem = uniqueLemmas(tokens)

    #Gets the nouns and prints out the first 20 lemmas and their tags
    nouns = posTagging(uniqueLem)
    
    print("Number of Tokens: %d " % len(tokens))
    print("Number of Nouns: %d" % len(nouns))

#POS tagging and returns the nouns
def posTagging(uniqueLem):
    #Gets the tags for each unique lemma 
    tags = nltk.pos_tag(uniqueLem)

    #Print first 20 tags
    for i in range(20):
        print(tags[i])

    #Returns nouns
    return [t for (t, pos) in tags if pos[:2] == 'NN']

#Lemmatizes text and gets the set of unique lemmas
def uniqueLemmas(tokens):
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens]
    return set(lemmatized)

#Preprocess text and returns tokens
def preprocess(raw_text):
    #Remove numbers and punctuation
    text = re.sub(r'[.?!,:;()\-\n\d]',' ', raw_text.lower())

    #Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if not t in stop_words]

    #Remove words that are too short
    tokens = [t for t in tokens if len(t) > 5]

    return tokens

#Validates the argument and returns the absolute path
def validateArgument():
    #Make the Path for the file
    path = os.path.dirname(__file__)
    dataFile = os.path.join(path, sys.argv[1])

    print(dataFile)
    if len(sys.argv) > 1:
        if os.path.exists(dataFile):
            return dataFile
        else:
            print("Error: Invalid Argument")
            exit()
    else:
        print("Error: Invalid Argument")
        exit()

if __name__ == "__main__":
    main()