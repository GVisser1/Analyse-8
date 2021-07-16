import sqlite3
import zipfile
import json
from datetime import datetime

global currentUser
con = sqlite3.connect('CDMS.db')
cur = con.cursor()

with open('log.json', 'r') as logs:
    logData = json.load(logs)

def SignIn():
    global currentUser
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    for row in DbFunctions.GetAllAccounts():
        if username == Functions.Decrypt(row[1]) and password == Functions.Decrypt(row[2]):
            print("\nSigned in successfully\n")
            currentUser = row
            Functions.LogActivity(currentUser[1], "Logged in", "", "No")
            CheckAccessLevel()
    print("\nUsername and/or password is incorrect\n")
    currentUser = -1
    additionalinfo = "Password " + str(password) + " is tried in combination with Username: " + str(username)
    Functions.LogActivity(username, "Unsuccesful login", additionalinfo, "Yes")
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
        Functions.LogActivity(currentUser[1], "Added Client", "", "No")
        print("\nClient has been added!\n")
        CheckAccessLevel()

    @staticmethod
    def RetrieveClientInfo():
        while True:
            fullName = input("\nEnter the full name of the client whose information you want to retrieve: ")
            allClients = DbFunctions.GetClients(fullName)
            if len(allClients) > 0:
                print(f"-------------------------------------\n"
                      f"Results for clients with the full name: {fullName}\n")
                for row in allClients:
                    print(f"Fullname: {Functions.Decrypt(row[1])}\n"
                          f"Street & house number: {Functions.Decrypt(row[2])}, {Functions.Decrypt(row[3])}\n"
                          f"Zip code & city: {Functions.Decrypt(row[4])}, {Functions.Decrypt(row[5])}\n"
                          f"Email Address: {Functions.Decrypt(row[6])}\n"
                          f"Phone Number: {Functions.Decrypt(row[7])}\n"
                          f"\n-------------------------------------\n")
                break
            else:
                print(f"\nNo clients have been found with the full name: {fullName}!\n")
        Functions.LogActivity(currentUser[1], "Retrieved Client info", "", "No")
        CheckAccessLevel()

    @staticmethod
    def ModifyClient():
        while True:
            oldEmail = input("\nEnter the email address of the client you want to modify: ")
            oldPhoneNumber = "+31-6-" + input("Enter a phone number: +31-6-")
            if DbFunctions.ModifyClient(oldEmail, oldPhoneNumber):
                print("\nClient has been modified!\n")
                break
            else:
                print("No client can be found with the given email address and/or phone number!\n")
        Functions.LogActivity(currentUser[1], "Modified Client", "", "No")
        CheckAccessLevel()

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if oldPassword == currentUser[2]:
                if DbFunctions.UpdatePassword():
                    print("Your password has been changed!\n")
                    Functions.LogActivity(currentUser[1], "Updated Password", "", "No")
                    break
            else:
                print("Password does not match\n")
                Functions.LogActivity(currentUser[1], "Failed to Update Password", f"Given password: {oldPassword} does not match old password: {currentUser[2]}", "Yes")
        CheckAccessLevel()


class SystemAdmin:
    @staticmethod
    def ShowMenu():
        count = 0
        with open('log.json', 'r') as logs:
            for row in logs:
                if row["Unread"] == True and Functions.Decrypt(row["Suspicious"]) == "Yes":
                    count += 1
        
        alert = ""
        if count > 0:
            if count == 1:
                alert = f"ALERT: {count} Suspicious unread activity"
            else:
                alert = f"ALERT: {count} Suspicious unread activities"
        
        print("-----------------------------------\n"
                    "|               MENU              |\n"
                    "-----------------------------------\n"
                    "1. Check users and roles\n"
                    "2. View client options\n"
                    "3. View adviser options\n"
                    "4. Create Backup\n"
                    f"5. View log file(s) {alert} \n" 
                    "6. Update password\n"
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
            SystemAdmin.CreateBackup()
        elif option == '5':
            SystemAdmin.ViewLogFiles()
        elif option == '6':
            SystemAdmin.UpdatePassword()
        elif option == '7':
            exit()

    @staticmethod
    def ClientOptions():
        print("\n1. Define and add client\n"
              "2. Retrieve client information\n"
              "3. Modify a client's account\n"
              "4. Delete client\n"
              "5. Return\n")
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
            SystemAdmin.DeleteClient()
        elif option == '5':
            CheckAccessLevel()

    @staticmethod
    def AdviserOptions():
        print("\n1. Define and add adviser\n"
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
        allAccounts = DbFunctions.GetAllAccounts()
        print("-------------------------------------\n"
              "|Username           -           Role|\n"
              "-------------------------------------\n")
        for row in allAccounts:
            print(f"{Functions.Decrypt(row[1])}           -           {row[6]}\n")
        print("-------------------------------------\n")
        Functions.LogActivity(currentUser[1], "Checked users", "", "No")
        ReturnToMenu()

    @staticmethod
    def AddAdviser():
        print("\nCreate an account for a new Adviser.\n"
              "Username must be between 5 & 20 Characters and must be started with a letter.\n"
              "Password must be between 8 & 30 Characters and must contain at least one lowercase letter, \n"
              "one uppercase letter, one digit, and one special character.\n")

        while True:
            if DbFunctions.AddAccount("Adviser"):
                break
        print("\nAdviser has been added!\n")
        CheckAccessLevel()

    @staticmethod
    def ModifyAdviser():
        while True:
            username = input("\nEnter the username of the adviser whose account you want to modify: ")
            if DbFunctions.ModifyAccount(username, "Adviser"):
                print("Adviser's account has been modified")
                break
            else:
                print("No adviser can be found with the given username!\n")
        CheckAccessLevel()

    @staticmethod
    def DeleteAdviser():
        while True:
            username = input("\nEnter the username of the adviser that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "Adviser"):
                print("\nAdviser has been deleted!\n")
                break
            else:
                print("\nNo adviser can be found with the given username!\n")
                ReturnToMenu()
        CheckAccessLevel()

    @staticmethod
    def ResetAdviserPassword():
        while True:
            username = input("\nEnter the username of the adviser whose password you want to reset: ")
            if DbFunctions.ResetPassword(username, "Adviser"):
                print("\nAdviser's password has been changed!\n")
                break
            else:
                print("\nNo adviser can be found with the given username!\n")
        CheckAccessLevel()

    @staticmethod
    def DeleteClient():
        while True:
            email = input("\nEnter the email of the client that you want to delete: ")
            phoneNumber = "+31-6-" + input("Enter the phone number of the client that you want to delete: +31-6-")
            if DbFunctions.DeleteClient(email, phoneNumber):
                print("\nClient has been deleted!\n")
                Functions.LogActivity(currentUser[1], "Deleted Client", f"email:{email}, phoneNumber:{phoneNumber}", "No")
                break
            else:
                print("\nNo client can be found with the given email and/or phone number!\n")
                Functions.LogActivity(currentUser[1], "Failed to delete client", f"No client can be found with email={email} and phone number={phoneNumber}", "Yes")
        CheckAccessLevel()

    @staticmethod
    def CreateBackup():
        list_files = ['CDMS.db', 'log.json']
        with zipfile.ZipFile('Backups.zip', 'w') as zipFile:
            for file in list_files:
                zipFile.write(file)
        print("\nSuccessfully made a backup\n")
        Functions.LogActivity(currentUser[1], "Successfully made a backup", "", "No")
        CheckAccessLevel()

    @staticmethod
    def ViewLogFiles():
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. View whole log\n"
              "2. View unread\n"
              "3. Return\n")
        option = input("Put in your choice: ")

        while option not in ['1', '2', '3']:
            option = input("Put in your choice: ")
        if option == '1':
            print("Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
            for row in logData:
                print(row["Id"] + " | " + 
                Functions.Decrypt(row["Username"]) + " | " + 
                Functions.Decrypt(row["Date"]) + " | " + 
                Functions.Decrypt(row["Time"]) + " | " + 
                Functions.Decrypt(row["Activity"]) + " | " + 
                Functions.Decrypt(row["Additional Information"]) + " | " + 
                Functions.Decrypt(row["Suspicious"]) + "\n")
            ReturnToMenu()
        elif option == '2':
            print("Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
            for row in logData:
                if row["Unread"]:
                    print(row["Id"] + " | " + 
                    Functions.Decrypt(row["Username"]) + " | " + 
                    Functions.Decrypt(row["Date"]) + " | " + 
                    Functions.Decrypt(row["Time"]) + " | " + 
                    Functions.Decrypt(row["Activity"]) + " | " + 
                    Functions.Decrypt(row["Additional Information"]) + " | " + 
                    Functions.Decrypt(row["Suspicious"]) + "\n")
                row["Unread"] = False
            ReturnToMenu()
        elif option == '3':
            CheckAccessLevel()

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if oldPassword == currentUser[2]:
                if DbFunctions.UpdatePassword():
                    print("Your password has been changed!\n")
                    Functions.LogActivity(currentUser[1], "Updated Password", "", "No")
                    break
            else:
                print("Password does not match\n")
                Functions.LogActivity(currentUser[1], "Failed to Update Password", f"Given password: {oldPassword} does not match old password: {currentUser[2]}", "Yes")
        CheckAccessLevel()


class SuperAdmin:
    @staticmethod
    def ShowMenu():
        count = 0
        with open('log.json', 'r') as logs:
            for row in logs:
                if row["Unread"] == True and Functions.Decrypt(row["Suspicious"]) == "Yes":
                    count += 1
        
        alert = ""
        if count > 0:
            if count == 1:
                alert = f"ALERT: {count} Suspicious unread activity"
            else:
                alert = f"ALERT: {count} Suspicious unread activities"
        
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. Check users and roles\n"
              "2. View client options\n"
              "3. View adviser options\n"
              "4. View admin options\n"
              "5. Create Backup\n"
              f"6. View log file(s) {alert} \n"
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
        print("\n1. Define and add admin\n"
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
        print("\nCreate an account for a new Admin.\n"
              "Username must be between 5 & 20 Characters and must be started with a letter.\n"
              "Password must be between 8 & 30 Characters and must contain at least one lowercase letter, \n"
              "one uppercase letter, one digit, and one special character.\n")

        while True:
            if DbFunctions.AddAccount("SystemAdmin"):
                break
        print("\nAdmin has been added!\n")
        CheckAccessLevel()

    @staticmethod
    def ModifyAdmin():
        while True:
            username = input("\nEnter the username of the admin whose account you want to modify: ")
            if DbFunctions.ModifyAccount(username, "SystemAdmin"):
                print("\nAdmin's account has been modified!\n")
                break
            else:
                print("\nNo admin can be found with the given username!\n")
        CheckAccessLevel()

    @staticmethod
    def DeleteAdmin():
        while True:
            username = input("\nEnter the username of the admin that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "SystemAdmin"):
                print("\nAdmin has been deleted!\n")
                break
            else:
                print("\nNo admin can be found with the given username!\n")
        CheckAccessLevel()

    @staticmethod
    def ResetAdminPassword():
        while True:
            username = input("\nEnter the username of the admin whose password you want to reset: ")
            if DbFunctions.ResetPassword(username, "SystemAdmin"):
                print("\nAdmin's password has been changed!\n")
                break
            else:
                print("\nNo admin can be found with the given username!\n")
        CheckAccessLevel()


class DbFunctions:
    @staticmethod
    def ExecQuery(query):
        cur.execute(query)
        con.commit()

    @staticmethod
    def GetAllAccounts():
        cur.execute("SELECT * FROM Accounts")
        return cur.fetchall()

    @staticmethod
    def GetAllClients():
        cur.execute("SELECT * FROM Clients")
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
            Functions.LogActivity(currentUser[1], f"Added {accountType}", "", "No")
            return True
        else:
            Functions.LogActivity(currentUser[1], f"Failed to add {accountType}", "Input by user: username={username}, password={password}, first name={firstName}, last name={lastName}", "Yes")
            return False

    @staticmethod
    def AddClient():
        fullName = input("Enter a full name: ")
        streetName = input("Enter a street name: ")
        houseNumber = input("Enter a house number: ")
        zipCode = input("Enter a zip code: ")
        city = ""
        print("-----------------------------------\n"
              "1. Rotterdam\n"
              "2. Amsterdam\n"
              "3. Den Haag\n"
              "4. Utrecht\n"
              "5. Eindhoven\n"
              "6. Tilburg\n"
              "7. Groningen\n"
              "8. Almere\n"
              "9. Breda\n"
              "10. Nijmegen\n")
        option = input("Choose a city: ")
        while option not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            option = input("Choose a city: ")
        if option == '1':
            city = "Rotterdam"
        elif option == '2':
            city = "Amsterdam"
        elif option == '3':
            city = "Den Haag"
        elif option == '4':
            city = "Utrecht"
        elif option == '5':
            city = "Eindhoven"
        elif option == '6':
            city = "Tilburg"
        elif option == '7':
            city = "Groningen"
        elif option == '8':
            city = "Almere"
        elif option == '9':
            city = "Breda"
        elif option == '10':
            city = "Nijmegen"
        emailAddress = input("Enter a email address: ")
        phoneNumber = "+31-6-" + input("Enter a phone number: +31-6-")
        DbFunctions.ExecQuery(f"INSERT INTO Clients (FullName, StreetName, HouseNumber, ZipCode, City, EmailAddress, PhoneNumber) "
                              f"VALUES ('{Functions.Encrypt(fullName)}', '{Functions.Encrypt(streetName)}', '{Functions.Encrypt(houseNumber)}', "
                              f"'{Functions.Encrypt(zipCode)}', '{Functions.Encrypt(city)}', "
                              f"'{Functions.Encrypt(emailAddress)}', '{Functions.Encrypt(phoneNumber)}')")
        return True

    @staticmethod
    def ModifyAccount(oldUsername, accountType):
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(oldUsername) and row[6] == accountType:
                username = input("Enter a (new) username: ").lower()
                password = input("Enter a (new) password: ")
                firstName = input("Enter a (new) first name: ")
                lastName = input("Enter a (new) last name: ")
                if Functions.CheckUsername(username) and Functions.CheckPassword(password):
                    DbFunctions.ExecQuery(
                        f"UPDATE Accounts SET Username = '{Functions.Encrypt(username)}', Password = '{Functions.Encrypt(password)}', "
                        f"FirstName = '{Functions.Encrypt(firstName)}', LastName = '{Functions.Encrypt(lastName)}' "
                        f"WHERE Username = '{Functions.Encrypt(oldUsername)}'")
                    Functions.LogActivity(currentUser[1], f"Modified {accountType}", "", "No")
                    return True
                Functions.LogActivity(currentUser[1], f"Failed to modify {accountType}", f"Input by user: username={username}, password={password}, first name={firstName}, last name={lastName}", "Yes")
                return False
        else:
            return False

    @staticmethod
    def ModifyClient(oldEmail, oldPhoneNumber):

        for row in DbFunctions.GetAllClients():
            if row[6] == Functions.Encrypt(oldEmail) and row[7] == Functions.Encrypt(oldPhoneNumber):
                fullName = input("Enter a (new) full name: ")
                streetName = input("Enter a (new) street name: ")
                houseNumber = input("Enter a (new) house number: ")
                zipCode = input("Enter a (new) zip code: ")
                city = ""
                print("-----------------------------------\n"
                      "1. Rotterdam\n"
                      "2. Amsterdam\n"
                      "3. Den Haag\n"
                      "4. Utrecht\n"
                      "5. Eindhoven\n"
                      "6. Tilburg\n"
                      "7. Groningen\n"
                      "8. Almere\n"
                      "9. Breda\n"
                      "10. Nijmegen\n")
                option = input("Choose a (new) city: ")
                while option not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                    option = input("Choose a city: ")
                if option == '1':
                    city = "Rotterdam"
                elif option == '2':
                    city = "Amsterdam"
                elif option == '3':
                    city = "Den Haag"
                elif option == '4':
                    city = "Utrecht"
                elif option == '5':
                    city = "Eindhoven"
                elif option == '6':
                    city = "Tilburg"
                elif option == '7':
                    city = "Groningen"
                elif option == '8':
                    city = "Almere"
                elif option == '9':
                    city = "Breda"
                elif option == '10':
                    city = "Nijmegen"
                emailAddress = input("Enter a (new) email address: ")
                phoneNumber = "+31-6-" + input("Enter a (new) phone number: +31-6-")
                DbFunctions.ExecQuery(
                    f"UPDATE Clients SET FullName = '{Functions.Encrypt(fullName)}', StreetName = '{Functions.Encrypt(streetName)}', "
                    f"HouseNumber = '{Functions.Encrypt(houseNumber)}', ZipCode = '{Functions.Encrypt(zipCode)}', "
                    f"City = '{Functions.Encrypt(city)}', EmailAddress = '{Functions.Encrypt(emailAddress)}', "
                    f"PhoneNumber = '{Functions.Encrypt(phoneNumber)}' "
                    f"WHERE EmailAddress = '{Functions.Encrypt(oldEmail)}' AND PhoneNumber = '{Functions.Encrypt(oldPhoneNumber)}'")
                return True
            else:
                return False

    @staticmethod
    def DeleteAccount(username, accountType):
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(username) and row[6] == accountType:
                DbFunctions.ExecQuery(f"DELETE FROM Accounts WHERE Username = '{Functions.Encrypt(username)}'")
                Functions.LogActivity(currentUser[1], f"Deleted {accountType}", f"User {username} is deleted", "No")
                return True
        Functions.LogActivity(currentUser[1], f"Failed to delete {accountType}", f"User not found with data: username={username}, accountType={accountType}", "Yes")
        return False

    @staticmethod
    def DeleteClient(email, phoneNumber):
        for row in DbFunctions.GetAllClients():
            if row[6] == Functions.Encrypt(email) and row[7] == Functions.Encrypt(phoneNumber):
                DbFunctions.ExecQuery(f"DELETE FROM Clients WHERE EmailAddress = '{Functions.Encrypt(email)}' "
                                      f"AND PhoneNumber = '{Functions.Encrypt(phoneNumber)}'")
                return True
        return False

    @staticmethod
    def UpdatePassword():
        newPassword = input("Enter your new password: ")
        if Functions.CheckPassword(newPassword):
            DbFunctions.ExecQuery(
                f"UPDATE Accounts SET Password = '{Functions.Encrypt(newPassword)}' WHERE Username = '{Functions.Encrypt(currentUser[1])}'")
            return True
        else:
            Functions.LogActivity(currentUser[1], "Failed to Update Password", f"New password did not meet the criteria: {newPassword}", "Yes")
            return False

    @staticmethod
    def ResetPassword(username, accountType):
        newPassword = input("Enter a new password: ")
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(username) and row[6] == accountType and Functions.CheckPassword(newPassword):
                DbFunctions.ExecQuery(
                    f"UPDATE Accounts SET Password = '{Functions.Encrypt(newPassword)}' WHERE Username = '{Functions.Encrypt(username)}'")
                Functions.LogActivity(currentUser[1], "Resetted password", f"Resetted the password of {username} with account type {accountType} to {newPassword}", "No")
                return True
        Functions.LogActivity(currentUser[1], f"Failed to reset password", f"User not found with data: username={username}, accountType={accountType}", "Yes")
        return False


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
        for row in DbFunctions.GetAllAccounts():
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
    
    @staticmethod
    def LogActivity(username, activity, information, sus):
        DateTimeCurrent = datetime.now()

        id = str(len(logData) + 1)

        date = str(DateTimeCurrent.day) + "-" + str(DateTimeCurrent.month) + "-" + str(DateTimeCurrent.year)
        time = str(DateTimeCurrent.hour) + ":" + str(DateTimeCurrent.minute) + ":" + str(DateTimeCurrent.second)

        with open('log.json', 'r+') as logs:
            logData.append({
                "Id": id,
                "Username": Functions.Encrypt(username),
                "Date": Functions.Encrypt(date),
                "Time": Functions.Encrypt(time),
                "Activity": Functions.Encrypt(activity),
                "Additional Information": Functions.Encrypt(information),
                "Suspicious": Functions.Encrypt(sus),
                "Unread":True
            })
            logs.seek(0)
            json.dump(logData, logs, indent=4)
            logs.truncate()

print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
SignIn()

#
# Adviser
# System Admin
# Super Admin -> Hard coded - username: superadmin, password: Admin!23
