from fileinput import filename
import os

import json

def obtainGame(username, nlp):
    #Intro
    print(f"Board Game Bot: Let's talk about a new board game!")
    input(f"{username}: ")

    #Checks if there's a recommendation
    userFileName = "Data/Users/" + username.lower() + ".json"
    with open(os.path.join(os.path.dirname(__file__), userFileName), "r") as userFile:
        userJSON = json.load(userFile)

    recommendAvailable = False
    if userJSON["Recommended Game"] != "":
        recommendAvailable = True
        title = userJSON ["Recommended Game"]
        
    #Asks if they wanna talk about the most recently recommended game
    if recommendAvailable:
        print(f"Board Game Bot: Do you want to talk about my most recent recommendation: {title}?")
        recommend = input(f"{username}: ")
        recNLP = nlp(recommend)

        yesNLP = recNLP.similarity(nlp("Yes"))
        noNLP = recNLP.similarity(nlp("No"))
        maxChoice = max(yesNLP, noNLP)

        if(maxChoice == yesNLP):
            like = reviewGame(username, nlp)

            likedGames = userJSON["Liked Games"]
            dislikedGames = userJSON["Disliked Games"]
                
            if like:
                likedGames.append(title)
            else:
                dislikedGames.append(title)

            userJSON["Liked Games"] = likedGames
            userJSON["Disliked Games"] = dislikedGames
            userJSON["Recommended Game"] = ""

            with open(os.path.join(os.path.dirname(__file__), userFileName), "w") as userFile:
                json.dump(userJSON, userFile)

            return None

    #Asks for the the title of the game
    title = "NONE"
    while title == "NONE":
        print(f"Board Game Bot: What's the title of the board game?")
        title = input(f"{username}: ")
        nlpTitle = nlp(title)
        title = recognizeTitle(nlpTitle)
        
        if(title == "NONE"):
            print("Board Game Bot: I didn't get the name. Can you try again?")
    
    #Checks if the title is within knowledge base
    with open(os.path.join(os.path.dirname(__file__), "Data/Games.json"), "r") as gameFile:
        gameJSON = json.load(gameFile)

    if title not in gameJSON:
        newGame(username, title, nlp)

    #Asks the user's opinion on the game
    like = reviewGame(username, nlp)

    likedGames = userJSON["Liked Games"]
    dislikedGames = userJSON["Disliked Games"]
                
    if like:
        likedGames.append(title)
    else:
        dislikedGames.append(title)

    userJSON["Liked Games"] = likedGames
    userJSON["Disliked Games"] = dislikedGames

    #Writes JSON
    with open(os.path.join(os.path.dirname(__file__), userFileName), "w") as userFile:
        json.dump(userJSON, userFile)

def reviewGame(username, nlp):
    #Asks for the user's opinion on the game
    print("Board Game Bot: What are your opinions on the board game?")
    review = input(f"{username}: ")
    reviewNLP = nlp(review)

    #Checks the polarity of the review
    like = False
    if(reviewNLP._.blob.polarity > 0):
        like = True

    return like

def newGame(username, title, nlp):
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
        gameType = "War"
    elif mostSimType == cardNLP:
        gameType = "Card"
    elif mostSimType == partyNLP:
        gameType = "Party"

    #Edit game json
    newGameDict = { 
        title: 
        {
            "Type": gameType
        }
    }

    with open(os.path.join(os.path.dirname(__file__), "Data/Games.json"), "r") as gameFile:
        gameJSON = json.load(gameFile)

    gameJSON.update(newGameDict)

    with open(os.path.join(os.path.dirname(__file__), "Data/Games.json"), "w") as gameFile:
        json.dump(gameJSON, gameFile)

#Checks if the board game is in the knowledge base
def recognizeTitle(boardGameText):
    #Go Through Entities
    for game in boardGameText.ents:
        return game.text.lower()
    
    #Check each noun and proper noun if it's a game title
    for token in boardGameText:
        if((token.pos_ == "PROPN" or token.pos_ == "NOUN")):
            return token.text.lower()

    return "NONE"