from fileinput import filename
import os
import sys
import re
from this import d

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from random import randint

def main():
    #Opens files
    filename = validateArgument()
    file = open(filename, "r")
    
    #Tokenize Text
    raw_text = file.read()
    tokens = word_tokenize(raw_text)

    #Prints Out Lexical Diversity
    sets = set(tokens)
    print("\nLexical Diversity: %.2f\n" % (len(sets) / len(tokens)))

    #Preprocess Text
    tokens = preprocess(raw_text)

    #Get unique lemmas
    uniqueLem = uniqueLemmas(tokens)

    #Gets the nouns and prints out the first 20 lemmas and their tags
    nouns = posTagging(uniqueLem)
    
    print("\nNumber of Tokens: %d " % len(tokens))
    print("Number of Nouns: %d\n" % len(nouns))

    #Gets the nouns and their counts
    nouns_dict = nounCount(nouns, tokens)

    #Start the guessing game
    guessingGame(nouns_dict)

#Runs the guessing game
def guessingGame(nouns_dict):
    
    #Sorts Nouns
    sortedNouns = sorted(nouns_dict, key = nouns_dict.get, reverse=True)[:50]

    #Stores Score and the word they're guessing
    score = 5
    word = sortedNouns[randint(0, 49)]
    correctLetters = getAllLetters(word)
    letters = []
    letter = ""

    #Runs Game
    print("Guessing Game")
    while score > 0:
        #Checks if the player finished the word
        if len(correctLetters) == len(letters):
            print("\nYou Solved It!\n")
            letters = []
            word = sortedNouns[randint(0,49)]
            correctLetters = getAllLetters(word)

        #Prints out currently guessed letters
        correctGuess(letters, word)
        print("\n")
        
        #Waits for a letter to be inputted
        while True:
            #Asks the user for a letter
            letter = input("Guess a letter: ").lower()
            
            #Exit
            if letter == '!':
                print("Your Final Score: %d" % score)
                print("Exiting Game")
                exit()
            #Checks if the input is a letter
            elif re.match(r'[^.?!,:;()\-\n\d\s]', letter) and len(letter) == 1:
                break
            #Invalid Input
            else:
                print("Not a letter\n")
                correctGuess(letters, word)
                print("\n")
        
        
        #Correct Letter
        if letter in word:
            letters.append(letter)
            score += 1
            print("Correct! Score is %d" % score)
        #Wrong Letter
        else:
            score -= 1
            print("Wrong! Score is %d" %score)
    
    print("You Lose!\nExiting Game")
    exit()

#Gets all the letters in the word
def getAllLetters(word):
    correctLetters = []

    #Go through each character in a word
    for i in range(len(word)):
        char = word[i]

        #Checks if the letter has been encountered
        if char not in correctLetters:
            correctLetters.append(char)
    
    return correctLetters

#Prints out all the correctly guessed letters
def correctGuess(letters, word):
    #Go through each letter
    for i in range(0, len(word)):
        if word[i] in letters:
            print(word[i], end = " ")
        else:
            print("_", end = " ")

#Makes a dictionary of the nouns and their counts 
def nounCount(nouns, tokens):
    nouns_dict = {}

    #Get the counts for all the nouns
    for t in tokens:
        if t in nouns:
            if t not in nouns_dict:
                nouns_dict[t] = 1
            else:
                nouns_dict[t] += 1

    #Sort the nouns    
    sortedNouns = sorted(nouns_dict, key = nouns_dict.get, reverse=True)
    
    #Print the 50 most common nouns in the file
    print("50 Most Common Nouns")
    for noun in sortedNouns[:50]:
        print(noun, " : ", nouns_dict[noun])

    return nouns_dict

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