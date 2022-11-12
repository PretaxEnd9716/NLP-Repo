from fileinput import filename
import os

import json

import spacy

#Load NLP
nlp = spacy.load("en_core_web_lg")

#Obtain Game Files
gameFile = open(os.path.join(os.path.dirname(__file__), "Data/Games.json"))
gameJSON = json.load(gameFile)

def oldUserIntro(username):
    #Intro
    print(f"Board Game Bot: Welcome back {username}!")
    input(f"{username}: ")

    #Ask whether to recommend Do you want a board game recommendation or do you wanna talk about a new board game you've played
    while(True):
        
        print(f"Board Game Bot: Do you want a board game recommendation or do you wanna talk about a new board game you've played?")
        newTopic = input(f"{username}: ")
        topic = nlp(newTopic.lower())

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

def newUserIntro(username, likedGames, dislikedGames, favorite):
    #Intro
    print(f"Board Game Bot: Hi {username}, welcome to Board Game Bot")
    input(f"{username}: ")

    print(f"Board Game Bot: I'm here to give you board game recommendations!")
    print(f"Board Game Bot: First, we need to gather some information")
    input(f"{username}: ")

    #Gather liked games
    print(f"Board Game Bot: What are your favorite board games?")
    favBoardGames = input(f"{username}: ")
    fav = nlp(favBoardGames)
    likedGames = recognizeBoardGames(fav)
    

    #Gather disliked games
    print(f"Board Game Bot: What are board games you dislike?")
    dislikedBoardGames = input(f"{username}: ")
    dislike = nlp(dislikedBoardGames)
    dislikedGames = recognizeBoardGames(dislike)

    #Game types
    euroType = nlp("Euro")
    themType = nlp("Thematic")
    warType = nlp("Wargame")
    cardType = nlp("Card Game")
    partyType = nlp("Party Game")

    #Gather game type
    print(f"Board Game Bot: What kind of games do you want to play?")
    gameType = input(f"{username}: ")
    type = nlp(gameType.lower())

    typeArr = [type.similarity(nlp("Euro")), type.similarity(nlp("Thematic")), type.similarity(nlp("Wargame")), type.similarity(nlp("Card Game")), type.similarity(nlp("Party Game"))]
    mostSimType = max(typeArr)

    def switch(mostSimType):
        if mostSimType == euroType.similarity(type):
            favorite = "Euro"
        elif mostSimType == themType.similarity(type):
            favorite = "Thematic"
        elif mostSimType == warType.similarity(type):
            favorite = "Wargame"
        elif mostSimType == cardType.similarity(type):
            favorite = "Card Game"
        elif mostSimType == partyType.similarity(type):
            favorite = "Party Game"

    return username, likedGames, dislikedGames, favorite

#Recognize Board Games
def recognizeBoardGames(boardGameText):
    recognizedBoardGames = [] 
    
    #Entity recognition
    #TODO: Switch to obtain text rather than entity
    recognizedBoardGames = [game for game in boardGameText.ents if game.text.lower() in gameJSON]
    
    #Checking each noun and checking whether they're in the board game knowledge base
    #TODO: Clean up if statement and append in the text rather than the token
    for token in boardGameText:
        if(token not in recognizedBoardGames and (token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.text in gameJSON):
            recognizedBoardGames.append(token)

    return recognizedBoardGames