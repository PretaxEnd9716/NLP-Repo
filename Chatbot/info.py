from fileinput import filename
import os

import json

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

#Load NLP
nlp = spacy.load("en_core_web_lg")

#Obtain Game Files
gameFile = open(os.path.join(os.path.dirname(__file__), "Data/Games.json"))
gameJSON = json.load(gameFile)

def obtainGame(username):
    #Intro
    print(f"Board Game Bot: Let's talk about a new board game!")
    input(f"{username}: ")

    #Asks for the the title of the game
    print(f"Board Game Bot: What's the title of the board game?")
    title = input(f"{username}: ")
    nlpTitle = nlp(title)
    title = recognizeTitle(nlpTitle)
    
    #Checks if the title is recognizes
    if(title == "NONE"):
        newGame(username, title)
    else:
        recognizedGame(username, title)

def recognizedGame(username, title):
    #Asks for the user's opinion on the game
    print(f"Board Game Bot: What are your opinions on the board game?")
    review = input(f"{username}: ")
    reviewNLP = nlp(review)


    return False

def newGame(username, title):
    return True

#Checks if the board game is in the knowledge base
def recognizeTitle(boardGameText):
    #Go Through Entities
    for game in boardGameText.ents:
        if game.text.lower() in gameJSON:
            return game
    
    #Check each noun and proper noun if it's a game title
    for token in boardGameText:
        if((token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.text in gameJSON):
            return token.text

    return "NONE"