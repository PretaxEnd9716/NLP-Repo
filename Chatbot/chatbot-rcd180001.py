from fileinput import filename
import os
import json

import introTopic

#Initialize Chatbot
def init():
    #Obtain Username and userfile
    username = input("username: ")
    filename = "Data/Users/" + username.lower() + ".json"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if(os.path.exists(filepath)):
        #Open json file
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

    #Obtain Game Files
    gameFile = open(os.path.join(os.path.dirname(__file__), "Data/Games.json"))
    gameJSON = json.load(gameFile)

    #Loads intro topic
    if(newUser):
        topic = introTopic.newUserIntro(username)
    else:
        topic = introTopic.oldUserIntro(username)



def newUser(likedGames, dislikedGames, favorite, filepath):
    newUser = {
        "Liked Games": likedGames,
        "Disliked Games": dislikedGames,
        "Favorite Type": favorite
    }
    newJSON = json.dumps(newUser)
        
    #Create json file
    with open(filepath, "w") as userFile:
        userFile.write(newJSON)

if __name__ == "__main__":
    init()