from fileinput import filename
import pickle
import sys
import os
import re

def main():
    fileName = validateArgument()
    dict = readLines(fileName)
    pickle.dump(dict, open('employee.p', 'wb'))
    employees = pickle.load(open('employee.p', 'rb'))

    print("\nEmployee List:\n")
    for employee in employees.values():
        employee.display()
    

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
    dataDict = {}

    with open(fileName, 'r') as file:
        next(file)

        for line in file:
            editedLine = re.sub(r'[\n]', '', line)
            arr = editedLine.split(',')

            #Names
            lastName = formatName(arr[0])
            firstName = formatName(arr[1])
            middleName = formatName(arr[2])

            #ID
            id = formatID(arr[3])

            #Phone
            phone = arr[4].replace(" ", "")
            phone = formatPhone(phone)

            p = Person(lastName, firstName, middleName, id, phone)
            
            if id in dataDict.keys():
                print("\nError: Data contains duplicate id")
            else:
                dataDict[id] = p

    return dataDict

#Formats all name types        
def formatName(name):
    if(name == ''):
        return 'X'

    if(re.match(r'^[A-Z][a-z0-9]*$', name)):
        return name

    formattedName = ""
    currentChar = 0
    for character in name:
        if(currentChar == 0):
            formattedName += name[0].upper()

        else:
            formattedName += name[currentChar].lower()

        currentChar += 1

    return formattedName

def formatPhone(phone):
    if(re.match(r'\d{3}-\d{3}-\d{4}', phone)):
        return phone
    
    if(re.match(r'\d{3}[,.-]?\d{3}[,.-]?\d{4}', phone)):
        formattedPhone = ""
        currentDigit = 0
        currentChar = 0
        for character in phone:
            if(re.match(r'\d', character)):
                formattedPhone += character
                
                if(currentDigit == 2 or currentDigit == 5):
                    formattedPhone += '-'
                
                currentDigit += 1

            currentChar += 1

        return formattedPhone
    
    else:
        validPhone = False
        while validPhone == False:
            print("\nPhone {} is invalid\nEnter phone number in form 123-456-7890".format(phone))
            phone = input("Enter phone number: ")

            if(re.match(r'\d{3}-\d{3}-\d{4}', phone)):
                validPhone = True
            
        
        return phone

def formatID(id):
    if(re.match(r'^[A-Z]{2}[0-9]{4}$', id)):
        return id
    
    if(re.match(r'^[a-zA-Z]{2}[0-9]{4}$', id)):
        formattedID = ""
        for char in id:
            if(re.match(r'\w', char)):
                formattedID += char.upper()

        return formattedID
    
    else:
        validID = False
        while validID == False:
            print("\nID is invalid: {}\nID is two letters followed by 4 digits".format(id))
            id = input("Please enter a valid id: ")
            id = id.upper()

            if(re.match(r'^[A-Z]{2}[0-9]{4}$', id)):
                validID = True

        return id

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.lastname = last;
        self.firstname = first;
        self.middle = mi;
        self.employeeId = id;
        self.phone = phone;

    def display(self):
        print("Employee Id: {}\n\t{} {} {}\n\t{}\n".format(self.employeeId, self.firstname, self.middle, self.lastname, self.phone));   

if __name__ == "__main__":
    main()