from fileinput import filename
import os

import spacy

def oldUserIntro(username):
    #Load NLP
    nlp = spacy.load("en_core_web_lg")

    #Intro
    print(f"Board Game Bot: Welcome back {username}!")
    input(f"{username}: ")

    #Ask whether to recommend Do you want a board game recommendation or do you wanna talk about a new board game you've played
    while(True):
        
        print(f"Board Game Bot: Do you want a board game recommendation or do you wanna talk about a new board game you've played?")
        newTopic = input(f"{username}: ")
        topic = nlp(newTopic)

        #Checks which topic to run
        recommend = nlp("I want a board game recommendation")
        recommendationSimilarity = recommend.similarity(topic)

        info = nlp("I played a new board game")
        infoSimilarity = info.similarity(topic)

        if(recommendationSimilarity > infoSimilarity and recommendationSimilarity >= .75):
            return 0
        elif(recommendationSimilarity < infoSimilarity and infoSimilarity >= .75):
            return 1
        else:
            print("Board Game Bot: I don't think I understood you")

def newUserIntro(username):
    #Load NLP
    nlp = spacy.load("en_core_web_lg")


    return username