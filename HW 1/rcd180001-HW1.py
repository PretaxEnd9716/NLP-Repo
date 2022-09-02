from fileinput import filename
import pickle
import sys
import os
import re

def main():
    fileName = validateArgument()
    readLines(fileName)
    

#Validates Arguments
def validateArgument():
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            return sys.argv[1]
        else:
            print("Error: Invalid Argument")
            exit()
    else:
        print("Error: Invalid Argument")
        exit()

#Read File
def readLines(fileName):
    with open(fileName, 'r') as file:
        next(file)

        for line in file:
            editedLine = re.sub(r'[\n]', '', line)
            arr = editedLine.split(',')
            
def formatName(name):
    return name

def formatPhone(phone):
    if(re.match(r'\d{3}-\d{3}-\d{4}', phone)):
        return phone

    formattedPhone = ""
    for character in phone:
        

    return formattedPhone

def formatID(id):
    return id

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.lastname = last;
        self.firstname = first;
        self.middle = mi;
        self.employeeId = id;
        self.phone = phone;

    def display(self):
        print("Employee id: {}\n\t{} {} {}\n\t{}".format(self.employeeId, self.firstname, self.middle, self.lastname, self.phone));   

if __name__ == "__main__":
    main()