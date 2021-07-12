import sqlite3
import zipfile
from datetime import datetime

global currentUser
con = sqlite3.connect('CDMS.db')
cur = con.cursor()


def SignIn():
    global currentUser
    print(Functions.Decrypt("ehzmwiv") + "-" + Functions.Decrypt("Ehzmwiv!67"))
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    for row in DbFunctions.GetAccounts():
        if username == Functions.Decrypt(row[1]) and password == Functions.Decrypt(row[2]):
            print("Signed in successfully\n")
            currentUser = row
            CheckAccessLevel()
    print("Username and/or password is incorrect\n")
    currentUser = -1
    SignIn()


def CheckAccessLevel():
    if currentUser[6] == 'SuperAdmin':
        SuperAdmin.ShowMenu()
    elif currentUser[6] == 'SystemAdmin':
        SystemAdmin.ShowMenu()
    elif currentUser[6] == 'Adviser':
        Adviser.ShowMenu()


def ReturnToMenu():
    print("Do you want to return to the menu? Press y\n")
    option = input("Put in your choice: ")
    while option != 'y':
        option = input("Put in your choice: ")
    if option == 'y':
        CheckAccessLevel()


def StopAction():
    print("Do you want to return to the menu? Press [y/n]\n")
    option = input("Put in your choice: ")
    while option not in ['y', 'n']:
        option = input("Put in your choice: ")
    if option == 'y':
        CheckAccessLevel()
    elif option == 'n':
        return


class Adviser:
    @staticmethod
    def ShowMenu():
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. Add client\n"
              "2. Retrieve client information\n"
              "3. Modify client information\n"
              "4. Update password\n"
              "5. Exit\n")
        option = input("Put in your choice: ")
        while option not in ['1', '2', '3', '4', '5']:
            option = input("Put in your choice: ")
        if option == '1':
            Adviser.AddClient()
        elif option == '2':
            Adviser.RetrieveClientInfo()
        elif option == '3':
            Adviser.ModifyClient()
        elif option == '4':
            Adviser.UpdatePassword()
        elif option == '5':
            exit()

    @staticmethod
    def AddClient():
        DbFunctions.AddClient()
        CheckAccessLevel()

    @staticmethod
    def RetrieveClientInfo():
        while True:
            fullName = input("Enter the full name of the client whose information you want to retrieve: ")
            allClients = DbFunctions.GetClients(fullName)
            if len(allClients) > 0:
                print(f"{allClients}\n")
                print(f"-------------------------------------\n"
                      f"Results for clients with the full name: {fullName}\n")
                for row in allClients:
                    print(f"Fullname: {Functions.Decrypt(row[1])}\n"
                          f"Street & house number: {Functions.Decrypt(row[2])}, {Functions.Decrypt(row[3])}\n"
                          f"Zip code & city: {Functions.Decrypt(row[4])}, {Functions.Decrypt(row[5])}\n"
                          f"Email Address: {Functions.Decrypt(row[6])}\n"
                          f"Phone Number: +31-6-{Functions.Decrypt(row[7])}\n"
                          f"-------------------------------------\n")
                break
            else:
                print(f"\nNo clients have been found with the full name: {fullName}!\n")
        CheckAccessLevel()

    @staticmethod
    def ModifyClient():
        return

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if oldPassword == currentUser[2]:
                DbFunctions.UpdatePassword()
                print("Your password has been changed!\n")
                break
            else:
                print("Password does not match\n")
        CheckAccessLevel()


class SystemAdmin:
    @staticmethod
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
            SystemAdmin.CheckUsers()
        elif option == '2':
            SystemAdmin.ClientOptions()
        elif option == '3':
            SystemAdmin.AdviserOptions()
        elif option == '4':
            SystemAdmin.CreateBackup()
        elif option == '5':
            SystemAdmin.ViewLogFiles()
        elif option == '6':
            exit()

    @staticmethod
    def ClientOptions():
        print("1. Define and add client\n"
              "2. Retrieve client information\n"
              "3. Modify a client's account\n"
              "4. Delete client\n"
              "5. Reset client's password\n"
              "6. Return\n")
        option = input("Put in your choice: ")
        while option not in ['1', '2', '3', '4', '5', '6']:
            option = input("Put in your choice: ")
        if option == '1':
            Adviser.AddClient()
        elif option == '2':
            Adviser.RetrieveClientInfo()
        elif option == '3':
            Adviser.ModifyClient()
        elif option == '4':
            SystemAdmin.DeleteClient()
        elif option == '5':
            Adviser.UpdatePassword()
        elif option == '6':
            CheckAccessLevel()

    @staticmethod
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
            SystemAdmin.AddAdviser()
        elif option == '2':
            SystemAdmin.ModifyAdviser()
        elif option == '3':
            SystemAdmin.DeleteAdviser()
        elif option == '4':
            SystemAdmin.ResetAdviserPassword()
        elif option == '5':
            CheckAccessLevel()

    @staticmethod
    def CheckUsers():
        allAccounts = DbFunctions.GetAccounts()
        print("-------------------------------------\n"
              "|Username           -           Role|\n"
              "-------------------------------------\n")
        for row in allAccounts:
            print(f"{Functions.Decrypt(row[1])}           -           {row[6]}\n")
        print("-------------------------------------\n")
        ReturnToMenu()

    @staticmethod
    def AddAdviser():
        print("-----------------------------------\n"
              "|           Add Adviser           |\n"
              "-----------------------------------\n"
              "Create an account for a new Adviser.\n"
              "Username must be between 5 & 20 Characters and must be started with a letter.\n"
              "Password must be between 8 & 30 Characters and must contain at least one lowercase letter, "
              "one uppercase letter, one digit, and one special character.\n")

        while True:
            if DbFunctions.AddAccount("Adviser"):
                break
        print("Adviser has been added\n")
        CheckAccessLevel()

    @staticmethod
    def ModifyAdviser():
        return

    @staticmethod
    def DeleteAdviser():
        while True:
            username = input("\nEnter the username of the adviser that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "Adviser"):
                print("Adviser has been deleted!\n")
                break
            else:
                print("No adviser can be found with the given username\n")
                ReturnToMenu()
        CheckAccessLevel()

    @staticmethod
    def ResetAdviserPassword():
        return

    @staticmethod
    def DeleteClient():
        return

    @staticmethod
    def CreateBackup():
        list_files = ['CDMS_Copy.db', 'CDMS_Copy2.db']
        with zipfile.ZipFile('Backups.zip', 'w') as zipFile:
            for file in list_files:
                zipFile.write(file)
        print("\nSuccessfully made a backup\n")
        CheckAccessLevel()

    @staticmethod
    def ViewLogFiles():
        return

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if oldPassword == currentUser[2]:
                DbFunctions.UpdatePassword()
                print("Your password has been changed!\n")
                break
            else:
                print("Password does not match\n")


class SuperAdmin:
    @staticmethod
    def ShowMenu():
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. Check users and roles\n"
              "2. View client options\n"
              "3. View adviser options\n"
              "4. View admin options\n"
              "5. Create Backup\n"
              "6. View log file(s)\n"
              "7. Exit\n")
        option = input("Put in your choice: ")
        while option not in ['1', '2', '3', '4', '5', '6', '7']:
            option = input("Put in your choice: ")
        if option == '1':
            SystemAdmin.CheckUsers()
        elif option == '2':
            SystemAdmin.ClientOptions()
        elif option == '3':
            SystemAdmin.AdviserOptions()
        elif option == '4':
            SuperAdmin.AdminOptions()
        elif option == '5':
            SystemAdmin.CreateBackup()
        elif option == '6':
            SystemAdmin.ViewLogFiles()
        elif option == '7':
            exit()

    @staticmethod
    def AdminOptions():
        print("1. Define and add admin\n"
              "2. Modify an admin's account\n"
              "3. Delete admin\n"
              "4. Reset admin's password\n"
              "5. Return\n")
        option = input("Put in your choice: ")
        while option not in ['1', '2', '3', '4', '5']:
            option = input("Put in your choice: ")
        if option == '1':
            SuperAdmin.AddAdmin()
        elif option == '2':
            SuperAdmin.ModifyAdmin()
        elif option == '3':
            SuperAdmin.DeleteAdmin()
        elif option == '4':
            SuperAdmin.ResetAdminPassword()
        elif option == '5':
            CheckAccessLevel()

    @staticmethod
    def AddAdmin():
        print("-----------------------------------\n"
              "|           Add Admin           |\n"
              "-----------------------------------\n"
              "Create an account for a new Admin.\n"
              "Username must be between 5 & 20 Characters and must be started with a letter.\n"
              "Password must be between 8 & 30 Characters and must contain at least one lowercase letter, "
              "one uppercase letter, one digit, and one special character.\n")

        while True:
            if DbFunctions.AddAccount("SystemAdmin"):
                break
        print("Admin has been added\n")
        CheckAccessLevel()

    @staticmethod
    def ModifyAdmin():
        while True:
            if DbFunctions.ModifyAccount("Admin"):
                print("Admin's account has been modified")
                break
            else:
                print("No admin can be found with the given username!\n")
                ReturnToMenu()
        CheckAccessLevel()

    @staticmethod
    def DeleteAdmin():
        while True:
            username = input("\nEnter the username of the admin that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "Admin"):
                print("Admin has been deleted!\n")
                break
            else:
                print("No admin can be found with the given username!\n")
                ReturnToMenu()
        CheckAccessLevel()

    @staticmethod
    def ResetAdminPassword():
        return


class DbFunctions:
    @staticmethod
    def ExecQuery(query):
        cur.execute(query)
        con.commit()

    @staticmethod
    def GetAccounts():
        cur.execute("SELECT * FROM Accounts")
        return cur.fetchall()

    @staticmethod
    def GetClients(fullName):
        cur.execute(f"SELECT * FROM Clients WHERE FullName = '{Functions.Encrypt(fullName)}'")
        return cur.fetchall()

    @staticmethod
    def AddAccount(accountType):
        username = input("Enter a username: ").lower()
        password = input("Enter a password: ")
        firstName = input("Enter a first name: ")
        lastName = input("Enter a last name: ")
        registrationDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if Functions.CheckUsername(username) and Functions.CheckPassword(password):
            DbFunctions.ExecQuery(f"INSERT INTO Accounts (Username, Password, FirstName, LastName, RegistrationDate, Type) "
                                  f"VALUES ('{Functions.Encrypt(username)}', '{Functions.Encrypt(password)}', "
                                  f"'{Functions.Encrypt(firstName)}', '{Functions.Encrypt(lastName)}', '{registrationDate}', '{accountType}')")
            return True
        else:
            return False

    @staticmethod
    def AddClient():
        fullName = input("Enter a full name: ")
        streetName = input("Enter a password: ")
        houseNumber = input("Enter a first name: ")
        zipCode = input("Enter a last name: ")
        city = input("Enter a city: ")  # CHOOSE OPTION 10 CITIES
        emailAddress = input("Enter an email: ")
        phoneNumber = input("Enter a phone number: +31-6-")
        DbFunctions.ExecQuery(f"INSERT INTO Clients (FullName, StreetName, HouseNumber, ZipCode, City, EmailAddress, PhoneNumber) "
                              f"VALUES ('{Functions.Encrypt(fullName)}', '{Functions.Encrypt(streetName)}', '{Functions.Encrypt(houseNumber)}', "
                              f"'{Functions.Encrypt(zipCode)}', '{Functions.Encrypt(city)}', "
                              f"'{Functions.Encrypt(emailAddress)}', '{Functions.Encrypt(phoneNumber)}')")
        return True

    @staticmethod
    def ModifyAccount(accountType):
        username = input("\nEnter the username of the admin's account that you want to modify: ")
        return

    @staticmethod
    def DeleteAccount(username, accountType):
        for row in DbFunctions.GetAccounts():
            if row[1] == Functions.Encrypt(username) and row[6] == accountType:
                DbFunctions.ExecQuery(f"DELETE FROM Accounts WHERE Username = '{Functions.Encrypt(username)}'")
                return True
        return False

    @staticmethod
    def UpdatePassword():
        newPassword = input("Enter your new password: ")
        DbFunctions.ExecQuery(
            f"UPDATE Accounts SET Password = '{Functions.Encrypt(newPassword)}' WHERE Username = '{Functions.Decrypt(currentUser[1])}'")
        return


class Functions:
    @staticmethod
    def Encrypt(text):
        encrypted = ""
        for c in text:
            if c.isupper():
                c_index = ord(c) - ord('A')
                c_shifted = (c_index + 4) % 26 + ord('A')
                c_new = chr(c_shifted)
                encrypted += c_new
            elif c.islower():
                c_index = ord(c) - ord('a')
                c_shifted = (c_index + 4) % 26 + ord('a')
                c_new = chr(c_shifted)
                encrypted += c_new
            elif c.isdigit():
                c_new = (int(c) + 4) % 10
                encrypted += str(c_new)
            else:
                encrypted += c
        return encrypted

    @staticmethod
    # Decrypt data using Caesar Cipher
    def Decrypt(encrypted_text):
        decrypted = ""
        for c in encrypted_text:
            if c.isupper():
                c_index = ord(c) - ord('A')
                c_og_pos = (c_index - 4) % 26 + ord('A')
                c_og = chr(c_og_pos)
                decrypted += c_og
            elif c.islower():
                c_index = ord(c) - ord('a')
                c_og_pos = (c_index - 4) % 26 + ord('a')
                c_og = chr(c_og_pos)
                decrypted += c_og
            elif c.isdigit():
                c_og = (int(c) - 4) % 10
                decrypted += str(c_og)
            else:
                decrypted += c
        return decrypted

    @staticmethod
    # Validates the entered username
    def CheckUsername(username):
        usernameWhitelist = ["-", "_", "'", "."]
        for row in DbFunctions.GetAccounts():
            if row[1] == Functions.Encrypt(username):
                print("Username already exists!\n")
                return False
        if not username[0].isupper() and not username.islower():
            print("Username must start with a letter.\n")
            return False
        if len(username) < 5 or len(username) > 20:
            print("Username must have a length of at least 5 characters and must be no longer than 20 characters.\n")
            return False
        for i in username:
            if not i.isupper() and not i.islower() and not i.isdigit() and i not in usernameWhitelist:
                print("Username contains invalid characters.\n")
                return False
        return True

    @staticmethod
    # Validates the entered password
    def CheckPassword(password):
        if len(password) < 8 or len(password) > 30:
            print("Password must have a length of at least 8 characters and must be no longer than 30 characters.\n")
            return False
        checklist = [False, False, False, False]
        for i in password:
            if i.isupper():
                checklist[0] = True
            elif i.islower():
                checklist[1] = True
            elif i.isdigit():
                checklist[2] = True
            else:
                checklist[3] = True
        if False in checklist:
            print("Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.\n")
            print(checklist)
            return False
        return True


print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
SignIn()

#
# Adviser
# System Admin
# Super Admin -> Hard coded - username: superadmin, password: Admin!23
