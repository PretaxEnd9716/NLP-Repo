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
        newUser = introTopic.newUserIntro(username, likedGames, dislikedGames, favorite)
        username = newUser[0]
        likedGames = newUser[1]
        dislikedGames = newUser[2]
        favorite = newUser[3]
        topic = 0
    else:
        topic = introTopic.oldUserIntro(username)

if __name__ == "__main__":
    init()