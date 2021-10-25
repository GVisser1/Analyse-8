import sqlite3
import string
import zipfile
import json
from datetime import datetime
from secrets import compare_digest

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
        if username == Functions.Decrypt(row[1]) and compare_digest(password, Functions.Decrypt(row[2])):
            print("\nSigned in successfully\n")
            currentUser = row
            Functions.LogActivity(currentUser[1], "Logged in", "", "No")
            CheckAccessLevel()
    print("\nUsername and/or password is incorrect\n")
    currentUser = -1
    Functions.LogActivity(Functions.Encrypt(username), "Unsuccessful login",
                          f"Password {password} is tried in combination with Username: {username}", "Yes")
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
        while True:
            if DbFunctions.AddClient():
                break
        print("\nClient has been added!\n")
        CheckAccessLevel()

    @staticmethod
    def RetrieveClientInfo():
        fullName = input("\nEnter the full name of the client whose information you want to retrieve: ")
        print(f"-------------------------------------\n"
              f"Results for clients with the full name: {fullName}\n")
        count = 0
        for row in DbFunctions.GetAllClients():
            if row[1] == Functions.Encrypt(fullName):
                count += 1
                print(f"Fullname: {Functions.Decrypt(row[1])}\n"
                      f"Street & house number: {Functions.Decrypt(row[2])}, {Functions.Decrypt(row[3])}\n"
                      f"Zip code & city: {Functions.Decrypt(row[4])}, {Functions.Decrypt(row[5])}\n"
                      f"Email Address: {Functions.Decrypt(row[6])}\n"
                      f"Phone Number: {Functions.Decrypt(row[7])}\n"
                      f"\n-------------------------------------\n")
        if count == 0:
            print(f"No client has been found with the full name: {fullName}!\n")
        Functions.LogActivity(currentUser[1], "Retrieved Client info", "", "No")
        ReturnToMenu()

    @staticmethod
    def ModifyClient():
        while True:
            oldEmail = input("\nEnter the email address of the client you want to modify: ")
            oldPhoneNumber = "+31-6-" + input("Enter a phone number: +31-6-")
            if DbFunctions.ModifyClient(oldEmail, oldPhoneNumber):
                break
        CheckAccessLevel()

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if Functions.Encrypt(oldPassword) == currentUser[2]:
                if DbFunctions.UpdatePassword():
                    break
            else:
                print("Password does not match\n")
                Functions.LogActivity(currentUser[1], "Failed to Update Password",
                                      f"Given password: {oldPassword} does not match old password", "Yes")
        CheckAccessLevel()


class SystemAdmin:
    @staticmethod
    def ShowMenu():
        count = 0
        for row in logData:
            if row["Read"] == "False" and Functions.Decrypt(row["Suspicious"]) == "Yes":
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
        while True:
            if DbFunctions.AddAccount("Adviser"):
                break
        CheckAccessLevel()

    @staticmethod
    def ModifyAdviser():
        while True:
            username = input("\nEnter the username of the adviser whose account you want to modify: ")
            if DbFunctions.ModifyAccount(username, "Adviser"):
                break
        CheckAccessLevel()

    @staticmethod
    def DeleteAdviser():
        while True:
            username = input("\nEnter the username of the adviser that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "Adviser"):
                break
        CheckAccessLevel()

    @staticmethod
    def ResetAdviserPassword():
        while True:
            username = input("\nEnter the username of the adviser whose password you want to reset: ")
            if DbFunctions.ResetPassword(username, "Adviser"):
                break
        CheckAccessLevel()

    @staticmethod
    def DeleteClient():
        while True:
            email = input("\nEnter the email of the client that you want to delete: ")
            phoneNumber = "+31-6-" + input("Enter the phone number of the client that you want to delete: +31-6-")
            if DbFunctions.DeleteClient(email, phoneNumber):
                break
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
              "1. View all logs\n"
              "2. View unread suspicious logs\n"
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
                with open('log.json', 'w') as logs:
                    row["Read"] = "True"
                    json.dump(logData, logs, indent=4)
            ReturnToMenu()
        elif option == '2':
            print("Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
            for row in logData:
                if row["Read"] == "False" and Functions.Decrypt(row["Suspicious"]) == "Yes":
                    print(row["Id"] + " | " +
                          Functions.Decrypt(row["Username"]) + " | " +
                          Functions.Decrypt(row["Date"]) + " | " +
                          Functions.Decrypt(row["Time"]) + " | " +
                          Functions.Decrypt(row["Activity"]) + " | " +
                          Functions.Decrypt(row["Additional Information"]) + " | " +
                          Functions.Decrypt(row["Suspicious"]) + "\n")
                with open('log.json', 'w') as logs:
                    row["Read"] = "True"
                    json.dump(logData, logs, indent=4)
            ReturnToMenu()
        elif option == '3':
            CheckAccessLevel()

    @staticmethod
    def UpdatePassword():
        while True:
            oldPassword = input("Enter your old password: ")
            if Functions.Encrypt(oldPassword) == currentUser[2]:
                if DbFunctions.UpdatePassword():
                    break
            else:
                print("Password does not match\n")
                Functions.LogActivity(currentUser[1], "Failed to Update Password",
                                      f"Given password: {oldPassword} does not match old password", "Yes")
        CheckAccessLevel()


class SuperAdmin:
    @staticmethod
    def ShowMenu():
        count = 0
        for row in logData:
            if row["Read"] == "False" and Functions.Decrypt(row["Suspicious"]) == "Yes":
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
        while True:
            if DbFunctions.AddAccount("SystemAdmin"):
                break
        CheckAccessLevel()

    @staticmethod
    def ModifyAdmin():
        while True:
            username = input("\nEnter the username of the admin whose account you want to modify: ")
            if DbFunctions.ModifyAccount(username, "SystemAdmin"):
                break
        CheckAccessLevel()

    @staticmethod
    def DeleteAdmin():
        while True:
            username = input("\nEnter the username of the admin that you want to delete: ")
            if DbFunctions.DeleteAccount(username, "SystemAdmin"):
                break
        CheckAccessLevel()

    @staticmethod
    def ResetAdminPassword():
        while True:
            username = input("\nEnter the username of the admin whose password you want to reset: ")
            if DbFunctions.ResetPassword(username, "SystemAdmin"):
                break
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
        cur.execute("SELECT * FROM Clients WHERE `FullName` = ?;", (Functions.Encrypt(fullName)))
        return cur.fetchall()

    @staticmethod
    def AddAccount(accountType):
        print(f"\nCreate an account for a new {accountType}.\n")
        username = input("Enter a username: ").lower()
        password = input("Enter a password: ")
        firstName = input("Enter a first name: ")
        lastName = input("Enter a last name: ")
        registrationDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if Functions.CheckUsername(username) and Functions.CheckPassword(password) and Functions.CheckStringInput([firstName, lastName]):
            cur.execute(
                "INSERT INTO Accounts (Username, Password, FirstName, LastName, RegistrationDate, Type) VALUES (?, ?, ?, ?, ?, ?);",
                (
                    Functions.Encrypt(username), Functions.Encrypt(password), Functions.Encrypt(firstName), Functions.Encrypt(lastName),
                    registrationDate,
                    accountType))
            con.commit()
            print(f"\n{accountType} has been added!\n")
            Functions.LogActivity(currentUser[1], f"Added {accountType}", "", "No")
            return True

        Functions.LogActivity(currentUser[1], f"Failed to add {accountType}",
                              f"Input by user: username={username}, password={password}, first name={firstName}, last name={lastName}", "Yes")
        return False

    @staticmethod
    def AddClient():
        fullName = input("Enter a full name: ")
        streetName = input("Enter a street name: ")
        houseNumber = input("Enter a house number: ")
        zipCode = input("Enter a zip code: ")
        city = ""
        print(
            "-----------------------------------\n1. Rotterdam\n2. Amsterdam\n3. Den Haag\n4. Utrecht\n5. Eindhoven\n6. Tilburg\n7. Groningen\n8. "
            "Almere\n9. Breda\n10. Nijmegen\n")
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
        phoneNumber = input("Enter a phone number: +31-6-")
        if Functions.CheckStringInput([fullName, streetName, houseNumber, zipCode, emailAddress]) and Functions.CheckPhoneNumber(phoneNumber):
            cur.execute(
                "INSERT INTO Clients (FullName, StreetName, HouseNumber, ZipCode, City, EmailAddress, PhoneNumber) VALUES (?,?,?,?,?,?,?);",
                (Functions.Encrypt(fullName), Functions.Encrypt(streetName), Functions.Encrypt(houseNumber), Functions.Encrypt(zipCode),
                 Functions.Encrypt(city), Functions.Encrypt(emailAddress), Functions.Encrypt('+31-6-' + phoneNumber)))
            con.commit()
            Functions.LogActivity(currentUser[1], "Added Client", "", "No")
            return True
        Functions.LogActivity(currentUser[1], "Failed to add Client",
                              f"Input by user: full name: {fullName}, street name & house number: {streetName} {houseNumber}, "
                              f"zip code: {zipCode}, email address: {emailAddress}, phone number: {phoneNumber}", "Yes")
        return False

    @staticmethod
    def ModifyAccount(oldUsername, accountType):
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(oldUsername.lower()) and row[6] == accountType:
                username = input("Enter a (new) username: ").lower()
                password = input("Enter a (new) password: ")
                firstName = input("Enter a (new) first name: ")
                lastName = input("Enter a (new) last name: ")
                if Functions.CheckUsername(username) and Functions.CheckPassword(password) and Functions.CheckStringInput([firstName, lastName]):
                    cur.execute(
                        "UPDATE Accounts SET Username = ?, Password = ?, FirstName = ?, LastName = ? WHERE Username = ?;", (
                            Functions.Encrypt(username), Functions.Encrypt(password), Functions.Encrypt(firstName), Functions.Encrypt(lastName),
                            Functions.Encrypt(oldUsername)))
                    con.commit()
                    print(f"\n{accountType}'s account has been modified\n")
                    Functions.LogActivity(currentUser[1], f"Modified {accountType}", "", "No")
                    return True
                Functions.LogActivity(currentUser[1], f"Failed to modify {accountType}",
                                      f"Input by user: username = {username}, password = {password}, "
                                      f"first name = {firstName}, last name = {lastName}", "Yes")
                return False
        Functions.LogActivity(currentUser[1], "Failed to modify account",
                              f"Input by user: old username= {oldUsername}", "Yes")
        print(f"No {accountType} can be found with the given username!\n")
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
                print(
                    "-----------------------------------\n1. Rotterdam\n2. Amsterdam\n3. Den Haag\n4. Utrecht\n5. Eindhoven\n6. Tilburg\n7. "
                    "Groningen\n8.Almere\n9. Breda\n10. Nijmegen\n")
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
                phoneNumber = input("Enter a (new) phone number: +31-6-")
                if Functions.CheckStringInput([fullName, streetName, houseNumber, zipCode, emailAddress]) and Functions.CheckPhoneNumber(phoneNumber):
                    cur.execute(
                        "UPDATE Clients SET FullName = ?, StreetName = ?, HouseNumber = ?, ZipCode = ?, "
                        "City = ?, EmailAddress = ?, PhoneNumber = ? WHERE EmailAddress = ? AND PhoneNumber = ?;",
                        (Functions.Encrypt(fullName), Functions.Encrypt(streetName), Functions.Encrypt(houseNumber), Functions.Encrypt(zipCode),
                         Functions.Encrypt(city), Functions.Encrypt(emailAddress), Functions.Encrypt('+31-6-' + phoneNumber),
                         Functions.Encrypt(oldEmail), Functions.Encrypt(oldPhoneNumber)))
                    con.commit()
                    print("Client has been modified!")
                    Functions.LogActivity(currentUser[1], "Modified Client", "", "No")
                    return True
                else:
                    Functions.LogActivity(currentUser[1], "Failed to modify Client",
                                          f"Input by user: full name: {fullName}, street name & house number: {streetName} {houseNumber}, "
                                          f"zip code: {zipCode}, email address: {emailAddress}, phone number: {phoneNumber}", "Yes")
                    return False
            else:
                Functions.LogActivity(currentUser[1], "Failed to modify Client",
                                      f"Input by user: old email address: {oldEmail}, old phone number: {oldPhoneNumber}", "Yes")
                print("No client can be found with the given email address and/or phone number!\n")
                return False

    @staticmethod
    def DeleteAccount(username, accountType):
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(username.lower()) and row[6] == accountType:
                cur.execute("DELETE FROM Accounts WHERE Username = ?;", (Functions.Encrypt(username.lower)))
                con.commit()
                print(f"\n{accountType}'s account has been deleted!\n")
                Functions.LogActivity(currentUser[1], f"Deleted {accountType}", f"User {username} is deleted", "No")
                return True
        print(f"\nNo {accountType} can be found with the given username!\n")
        Functions.LogActivity(currentUser[1], f"Failed to delete {accountType}",
                              f"User not found with data: username={username}, accountType={accountType}", "Yes")
        return False

    @staticmethod
    def DeleteClient(email, phoneNumber):
        for row in DbFunctions.GetAllClients():
            if row[6] == Functions.Encrypt(email) and row[7] == Functions.Encrypt(phoneNumber):
                cur.execute("DELETE FROM Clients WHERE EmailAddress = ? AND PhoneNumber = ?;",
                            (Functions.Encrypt(email), Functions.Encrypt(phoneNumber)))
                con.commit()
                print("\nClient has been deleted!\n")
                Functions.LogActivity(currentUser[1], "Deleted Client", f"email:{email}, phoneNumber:{phoneNumber}", "No")
                return True
        print("\nNo client can be found with the given email and/or phone number!\n")
        Functions.LogActivity(currentUser[1], "Failed to delete client",
                              f"No client can be found with email={email} and phone number={phoneNumber}", "Yes")
        return False

    @staticmethod
    def UpdatePassword():
        newPassword = input("Enter your new password: ")
        if Functions.CheckPassword(newPassword):
            cur.execute(
                "UPDATE Accounts SET Password = ? WHERE Username = ?;", (Functions.Encrypt(newPassword), Functions.Encrypt(currentUser[1])))
            con.commit()
            print("\nYour password has been changed!\n")
            Functions.LogActivity(currentUser[1], "Updated Password", "", "No")
            return True
        else:
            Functions.LogActivity(currentUser[1], "Failed to Update Password", f"New password did not meet the criteria: {newPassword}", "Yes")
            return False

    @staticmethod
    def ResetPassword(username, accountType):
        newPassword = input("Enter a new password: ")
        if not Functions.CheckPassword(newPassword):
            Functions.LogActivity(currentUser[1], f"Failed to reset password",
                                  f"User not found with data: username={username}, accountType={accountType}", "Yes")
            return False
        for row in DbFunctions.GetAllAccounts():
            if row[1] == Functions.Encrypt(username.lower()) and row[6] == accountType:
                cur.execute(
                    "UPDATE Accounts SET Password = ? WHERE Username = ?;", (Functions.Encrypt(newPassword), Functions.Encrypt(username)))
                con.commit()
                print(f"\n{accountType}'s password has been changed!\n")
                Functions.LogActivity(currentUser[1], "Reset password",
                                      f"Reset the password of {username} with account type {accountType} to {newPassword}", "No")
                return True
        print(f"No {accountType.lower()} can be found with the given username!")
        Functions.LogActivity(currentUser[1], f"Failed to reset password",
                              f"User not found with data: username={username}, accountType={accountType}", "Yes")
        return False


class Functions:
    # Encrypt data using Caesar Cipher
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
        usernameWhitelist = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_" + "'" + ".")
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
            if i not in usernameWhitelist:
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
    def CheckPhoneNumber(phoneNumber):
        if len(phoneNumber) != 8:
            print('Phone number is out of range.\n')
            return False
        try:
            int(phoneNumber)
            return True
        except ValueError:
            print("Phone number is not an integer. It's a string\n")
            return False

    @staticmethod
    def CheckStringInput(inputList):
        inputWhitelist = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_" + "'" + "." + "@" + "!" + "+" + " ")
        for input in inputList:
            if len(input) > 40:
                print("Input must not be longer than 40 characters.\n")
                return False
            for i in input:
                if i not in inputWhitelist:
                    print("Input contains invalid characters.\n")
                    return False
            return True

    @staticmethod
    def LogActivity(username, activity, information, sus):
        DateTimeCurrent = datetime.now()

        count = str(len(logData) + 1)

        date = str(DateTimeCurrent.day) + "-" + str(DateTimeCurrent.month) + "-" + str(DateTimeCurrent.year)
        time = str(DateTimeCurrent.hour) + ":" + str(DateTimeCurrent.minute) + ":" + str(DateTimeCurrent.second)

        with open('log.json', 'r+') as logs:
            logData.append({
                "Id": count,
                "Username": username,
                "Date": Functions.Encrypt(date),
                "Time": Functions.Encrypt(time),
                "Activity": Functions.Encrypt(activity),
                "Additional Information": Functions.Encrypt(information),
                "Suspicious": Functions.Encrypt(sus),
                "Read": "False"
            })
            logs.seek(0)
            json.dump(logData, logs, indent=4)
            logs.truncate()


print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
SignIn()
