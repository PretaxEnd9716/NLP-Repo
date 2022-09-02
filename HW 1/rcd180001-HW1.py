import pickle
import sys

def main():
    validateArgument()

#Validates Arguments
def validateArgument():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("Error: Invalid path to data")
        exit()

if __name__ == "__main__":
    main()