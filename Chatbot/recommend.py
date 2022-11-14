from fileinput import filename
import os

import json

def recommendGame(username, nlp):
    userFileName = "Data/Users/" + username.lower() + ".json"
    with open(os.path.join(os.path.dirname(__file__), userFileName), "r") as userFile:
        userJSON = json.load(userFile)

    #Intro
    print("Board Game Bot: Let me recommend you a game")
    input(f"{username}: ")

    #Asks if they want a game of their favorite type
    favType = userJSON["Favorite Type"]
    
    print(f"Board Game Bot: Do you want me to recommend a {favType}?")
    favTypeResp = input(f"{username}: ")
    favTypeNLP = nlp(favTypeResp)

    yesNLP = favTypeNLP.similarity(nlp("Yes"))
    noNLP = favTypeNLP.similarity(nlp("No"))
    maxChoice = max(yesNLP, noNLP)
        
    if maxChoice == yesNLP:
        type = favType
    else:
        #Asks for which type of game
        print("Board Game Bot: What type of games do you want me to recommend?")
        recTypeResp = input(f"{username}: ")
        recTypeNLP = nlp(recTypeResp)

        euroNLP = recTypeNLP.similarity(nlp("I want a euro game"))
        themeNLP = recTypeNLP.similarity(nlp("I want a thematic game"))
        warNLP = recTypeNLP.similarity(nlp("I want a wargame"))
        cardNLP = recTypeNLP.similarity(nlp("I want a card game"))
        partyNLP = recTypeNLP.similarity(nlp("I want a party game"))

        typeArr = [euroNLP, themeNLP, warNLP, cardNLP, partyNLP]
        mostSimType = max(typeArr)

        if mostSimType == euroNLP:
            type = "Euro"
        elif mostSimType == themeNLP:
            type = "Thematic"
        elif mostSimType == warNLP:
            type = "Wargame"
        elif mostSimType == cardNLP:
            type = "Card Game"
        elif mostSimType == partyNLP:
            type = "Party Game"

    title = findGame(type, userJSON)

    if(title == "None"):
        print(f"Board Game Bot: I'm sorry, I can't find any more {type} games")
        return None
        
    print(f"Board Game Bot: I recommend {title}!")
    input(f"{username}: ")

    userJSON["Recommended Game"] = title

    with open(os.path.join(os.path.dirname(__file__), userFileName), "w") as userFile:
        json.dump(userJSON, userFile)
        
def findGame(type, userJSON):
    with open(os.path.join(os.path.dirname(__file__), "Data/Games.json"), "r") as gameFile:
        gameJSON = json.load(gameFile)

    likedGames = userJSON["Liked Games"]
    dislikedGames = userJSON["Disliked Games"]
    
    for title in gameJSON.keys():
        game = gameJSON[title]
        gameType = game["Type"]
    
        if gameType.lower() == type.lower():
            if title not in likedGames and title not in dislikedGames:
                return title

    return "NONE"

    