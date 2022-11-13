from fileinput import filename
import os
import json

import introTopic
import info
import recommend

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

#Initialize Chatbot
def init():
    #Load NLP
    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe('spacytextblob')

    #Obtain Username and userfile
    username = input("username: ")
    filename = "Data/Users/" + username.lower() + ".json"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if(os.path.exists(filepath)):
        #Open json file
        #TODO: Clean up with a function
        userFile = open(filepath)
        userJSON = json.load(userFile)
        likedGames = userJSON["Liked Games"]
        dislikedGames = userJSON["Disliked Games"]
        favorite = userJSON["Favorite Type"]
        newUser = False
    else:
        #Create a new user json
        likedGames = []
        dislikedGames = []
        favorite = ""
        newUser = True

    #Runs intro topic
    if(newUser):
        newUser = introTopic.newUserIntro(username, likedGames, dislikedGames, favorite, nlp)
        username = newUser[0]
        likedGames = newUser[1]
        dislikedGames = newUser[2]
        favorite = newUser[3].lower()

        newUserJSON = {
            "Liked Games": likedGames,
            "Disliked Games": dislikedGames,
            "Favorite Type": favorite, 
            "Recommended Game": ""
        }

        #Create user file
        userFileName = "Data/Users/" + username.lower() + ".json"
        with open(os.path.join(os.path.dirname(__file__), userFileName), "w") as userFile:
            json.dump(newUserJSON, userFile)
    else:
        topic = introTopic.oldUserIntro(username, nlp)

        if topic == 1:
            info.obtainGame(username, nlp)
        else:
            recommend.recommendGame(username, nlp)
        
    while True:
        print(f"Board Game Bot: Do you want a board game recommendation, do you wanna talk about a new board game you've played, or do you want to leave?")
        newTopic = input(f"{username}: ")
        topic = nlp(newTopic.lower())

        #Checks which topic to run
        recommendTopic = topic.similarity(nlp("I want a board game recommendation"))
        infoTopic = topic.similarity(nlp("I want to talk about a new board game"))
        leave = topic.similarity(nlp("I want to leave!"))
        topicArr = [recommendTopic, infoTopic, leave]
        maxTopic = max(topicArr)

        if(maxTopic == recommendTopic and recommendTopic >= .75):
            recommend.recommendGame(username, nlp)
        elif(maxTopic == infoTopic and infoTopic >= .75):
            info.obtainGame(username, nlp)
        elif(maxTopic == leave and leave >= .75):
            print(f"Board Game Bot: Goodbye {username}!")
            return None
        else:
            print("Board Game Bot: I don't think I understood you")



if __name__ == "__main__":
    init()