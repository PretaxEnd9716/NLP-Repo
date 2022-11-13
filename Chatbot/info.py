from fileinput import filename
import os

import json

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

#Load NLP
nlp = spacy.load("en_core_web_lg")

def obtainGame(username):
    #Intro
    print(f"Board Game Bot: Let's talk about a new board game!")
    input(f"{username}: ")

    #Checks if there's a recommendation
    userFileName = "Data/Users/" + username + ".json"
    with open(os.path.join(os.path.direname(__file__), userFileName)) as userFile:
        userJSON = json.load(userFile)

    recommendAvailable = False
    if userJSON["Recommended Game"] != "":
        recommendAvailable = True
        
    #Asks if they wanna talk about the most recently recommended game
    if recommendAvailable:
        title = userJSON ["Recommended Game"]

        print(f"Board Game Bot: Do you want to talk about my most recent recommendation {title}?")
        recommend = input(f"{username}: ")
        recNLP = nlp(recommend)

        #Asks for their review of the game
        reviewGame(username, title)

        #Delete the recommended game
        userJSON["Recommended Game"] = ""
        with open(os.path.join(os.path.direname(__file__), userFileName)) as userFile:
            json.dump(userJSON, userFile)

    else:
        #Asks for the the title of the game
        print(f"Board Game Bot: What's the title of the board game?")
        title = input(f"{username}: ")
        nlpTitle = nlp(title)
        title = recognizeTitle(nlpTitle)
        
        #Obtain game info
        if(title == "NONE"):
            newGame(username, title)
            
        #Asks the user's opinion on the game
        reviewGame(username, title)

def reviewGame(username, title):
    #Asks for the user's opinion on the game
    print("Board Game Bot: What are your opinions on the board game?")
    review = input(f"{username}: ")
    reviewNLP = nlp(review)

    #Checks the polarity of the review
    like = False
    if(reviewNLP.polarity > 0):
        like = True
    
    #Edit the user json
    userFileName = "Data/Users/" + username + ".json"
    with open(os.path.join(os.path.direname(__file__), userFileName)) as userFile:
        userJSON = json.load(userFile)

    if like:
        likedGames = userJSON["Liked Games"]
        userJSON["Liked Games"] = likedGames.append(title)
    else:
        dislikedGames = userJSON["Disliked Games"]
        userJSON["Disliked Games"] = dislikedGames.append(title)
    
    with open(os.path.join(os.path.direname(__file__), userFileName)) as userFile:
        json.dump(userJSON, userFile)

def newGame(username, title):
    #Asks for the game type
    print(f"Board Game Bot: What type of game is {title}?")
    userType = input(f"{username}: ")
    utNLP = nlp(userType)

    #Checks the similarities each game type
    econNLP = utNLP.similarity(nlp("This game is an economic game"))  #euro games are commonly known as economic games
    euroNLP = utNLP.similarity(nlp("This game is a euro game"))
    themeNLP = utNLP.similarity(nlp("This game is thematic"))
    warNLP = utNLP.similarity(nlp("This game is a wargame"))
    cardNLP = utNLP.similarity(nlp("THis game is a card Game"))
    partyNLP = utNLP.similarity(nlp("This game is a party Game"))

    typeArr = [econNLP, euroNLP, themeNLP, warNLP, cardNLP, partyNLP]
    mostSimType = max(typeArr)

    if mostSimType == econNLP or mostSimType == euroNLP:
        gameType = "Euro"
    elif mostSimType == themeNLP:
        gameType = "Thematic"
    elif mostSimType == warNLP:
        gameType = "Wargame"
    elif mostSimType == cardNLP:
        gameType = "Card Game"
    elif mostSimType == partyNLP:
        gameType = "Party Game"

    #Asks for the complexity of the game
    print(f"Board Game Bot: How complex is {title}?")
    userComplex = input(f"{username}: ")
    ucNLP = nlp(userComplex)

    #Checks the similarity for each complexity
    lightNLP = ucNLP.similarity(nlp("This game is light complexity"))
    medNLP = ucNLP.similarity(nlp("This game is medium complexity"))
    heavyNLP = ucNLP.similarity(nlp("This game is heavy complexity"))

    compArr = [lightNLP, medNLP, heavyNLP]
    mostSimComp = max(compArr)

    if mostSimComp == lightNLP:
        complexity = "Light"
    elif mostSimComp == medNLP:
        complexity = "Medium"
    elif mostSimComp == heavyNLP:
        complexity = "Heavy"

    #Edit game json
    newGameDict = { 
        title: 
        {
            "Complexity": complexity,
            "Type": gameType
        }
    }

    with open(os.path.join(os.path.dirname(__file__), "Data/Games.json"), "w") as gameFile:
        json.dump(newGameDict, gameFile)

#Checks if the board game is in the knowledge base
#TODO: Use 'with' construct
def recognizeTitle(boardGameText):
    #Obtain Game Files
    gameFile = open(os.path.join(os.path.dirname(__file__), "Data/Games.json"))
    gameJSON = json.load(gameFile)

    #Go Through Entities
    for game in boardGameText.ents:
        if game.text.lower() in gameJSON:
            gameFile.close
            return game
    
    #Check each noun and proper noun if it's a game title
    for token in boardGameText:
        if((token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.text in gameJSON):
            gameFile.close
            return token.text

    gameFile.close
    return "NONE"