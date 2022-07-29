# Ciena_UserPass
'''Prompts the user for login credentials'''
import getpass  # Used to hide password


def credentials():
    # Prompt the user for a Username and Password
    reEnter = True
    while reEnter == True:
        print("\nPlease enter your login information to continue")
        username = input("   USERNAME > ")
        password = getpass.getpass("   PASSWORD > ")

        print("\nAre you sure the username/password is correct? Ok to proceed?")
        checkInfo = input("Enter Yes, No, or exit to quit: ")
        checkInfo = checkInfo.upper()
        print()

        if checkInfo[0] == "Y":
            return([username, password])

        elif checkInfo[0] == "E":
            print("Aborting program")
            exit()

        elif checkInfo[0] == "Q":
            print("Aborting program")
            exit()
