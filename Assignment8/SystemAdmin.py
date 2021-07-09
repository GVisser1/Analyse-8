import Adviser
import CDMS
import Functions


def ShowMenu():
    print("-----------------------------------\n"
          "|               MENU              |\n"
          "-----------------------------------\n"
          "1. Check users and roles\n"
          "2. View client options\n"
          "3. View adviser options\n"
          "4. Create Backup\n"
          "5. View log file(s)\n"
          "6. Update password\n"
          "7. Exit\n")
    option = input("Put in your choice: ")
    while option not in ['1', '2', '3', '4', '5', '6']:
        option = input("Put in your choice: ")
    if option == '1':
        CheckUsers()
    elif option == '2':
        ClientOptions()
    elif option == '3':
        AdviserOptions()
    elif option == '4':
        CreateBackup()
    elif option == '5':
        ViewLogFiles()
    elif option == '6':
        exit()


def ClientOptions():
    print("1. Define and add client\n"
          "2. Modify a client's account\n"
          "3. Delete client\n"
          "4. Reset client's password\n"
          "5. Return\n")
    option = input("Put in your choice: ")
    while option not in ['1', '2', '3', '4', '5']:
        option = input("Put in your choice: ")
    if option == '1':
        Adviser.AddClient()
    elif option == '2':
        Adviser.ModifyClient()
    elif option == '3':
        DeleteClient()
    elif option == '4':
        Adviser.ResetPassword()
    elif option == '5':
        CDMS.CheckAccessLevel()


def AdviserOptions():
    print("1. Define and add adviser\n"
          "2. Modify an adviser's account\n"
          "3. Delete adviser\n"
          "4. Reset adviser's password\n"
          "5. Return\n")
    option = input("Put in your choice: ")
    while option not in ['1', '2', '3', '4', '5']:
        option = input("Put in your choice: ")
    if option == '1':
        AddAdviser()
    elif option == '2':
        ModifyAdviser()
    elif option == '3':
        DeleteAdviser()
    elif option == '4':
        ResetAdviserPassword()
    elif option == '5':
        CDMS.CheckAccessLevel()


def CheckUsers():
    return


def AddAdviser():
    print("-----------------------------------\n"
          "|           Add Adviser           |\n"
          "-----------------------------------\n"
          "Create an account for a new Adviser.\n"
          "Username must be between 5 & 20 Characters and must be started with a letter.\n"
          "Password must be between 8 & 30 Characters and must contain at least one lowercase \n"
          "letter, one uppercase letter, one digit, and one special character.\n")
    
    loop = True
    while loop:
        username = input("Enter an username: ").lower()
        password = input("Enter a password: ")
        if Functions.CheckUsername(username) and Functions.CheckPassword(password):
            loop = False
    print("User should be created")
    
    #add user to database

def ModifyAdviser():
    return


def DeleteAdviser():
    return


def ResetAdviserPassword():
    return


def DeleteClient():
    return


def CreateBackup():
    return


def ViewLogFiles():
    return


def UpdatePassword():
    return
