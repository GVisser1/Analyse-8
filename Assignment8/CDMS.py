import json
import sqlite3
import string
import zipfile
import re
from datetime import datetime
from secrets import compare_digest

global current_user
con = sqlite3.connect('CDMS.db')
cur = con.cursor()
logfile = 'log.json'
choice_input = 'Put in your choice: '
max_failed_attempts = 'Too many failed attempts\n'

with open(logfile, 'r') as logs:
    logData = json.load(logs)


def sign_in():
    global current_user
    allAccounts = DBFunctions.get_all_accounts()
    attempts = 0
    while attempts <= 3:
        username = input("Enter your username: ").lower()
        password = input("Enter your password: ")
        for account in allAccounts:
            if username == Functions.decrypt(account[1]) and password == Functions.decrypt(account[2]):
                print("\nSigned in successfully\n")
                current_user = account
                Functions.log_activity(current_user[1], "Logged in", "", "No")
                check_access_level()
        attempts += 1
        print("\nUsername and/or password is incorrect\n")
    Functions.log_activity(f"{Functions.decrypt('undefined')} ", "Exceeded the maximum amount of sign in attempts",
                           f"Password: {password} is tried in combination with Username: {username}", "Yes")
    lock_out_user()


def checkAccount(): return


def lock_out_user():
    print("\nToo many failed attempts!\nYou are now locked out of the system\n\nPress 'q' to quit\n")
    option = input(choice_input)
    while option != 'q':
        option = input(choice_input)
    if option == 'q':
        quit()


def check_access_level():
    if current_user[6] == 'SuperAdmin':
        SuperAdmin.show_menu()
    elif current_user[6] == 'SystemAdmin':
        SystemAdmin.show_menu()
    elif current_user[6] == 'Adviser':
        Adviser.show_menu()


def return_to_menu():
    print("Do you want to return to the menu? Press y\n")
    option = input(choice_input)
    while option != 'y':
        option = input(choice_input)
    if option == 'y':
        check_access_level()


class Adviser:
    @staticmethod
    def show_menu():
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. Add client\n"
              "2. Retrieve client information\n"
              "3. Modify client information\n"
              "4. Update password\n"
              "5. Exit\n")
        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5']:
            option = input(choice_input)
        if option == '1':
            Adviser.add_client()
        elif option == '2':
            Adviser.retrieve_client_info()
        elif option == '3':
            Adviser.modify_client()
        elif option == '4':
            Adviser.update_password()
        elif option == '5':
            exit()

    @staticmethod
    def add_client():
        while True:
            if DBFunctions.add_client():
                break
        print("\nClient has been added!\n")
        check_access_level()

    @staticmethod
    def retrieve_client_info():
        name = input(
            "\nEnter the name of the client whose information you want to retrieve: ")
        print(f"-------------------------------------\n"
              f"Search results: {name}\n")
        count = 0
        for row in DBFunctions.get_clients_by_name(name):
            # if row[1] == Functions.encrypt(name):
            count += 1
            print(f"Fullname: {Functions.decrypt(row[1])}\n"
                  f"Street & house number: {Functions.decrypt(row[2])}, {Functions.decrypt(row[3])}\n"
                  f"Zip code & city: {Functions.decrypt(row[4])}, {Functions.decrypt(row[5])}\n"
                  f"Email Address: {Functions.decrypt(row[6])}\n"
                  f"Phone Number: {Functions.decrypt(row[7])}\n"
                  f"\n-------------------------------------\n")
        if count == 0:
            print(
                f"No client has been found with the given name: {name}!\n")
        Functions.log_activity(
            current_user[1], "Retrieved Client info", "", "No")
        return_to_menu()

    @staticmethod
    def modify_client():
        while True:
            old_email = input(
                "\nEnter the email address of the client you want to modify: ")
            old_phone_number = "+31-6-" + input("Enter a phone number: +31-6-")
            if DBFunctions.modify_client(old_email, old_phone_number):
                break
        check_access_level()

    @staticmethod
    def update_password():
        while True:
            old_password = input("\nEnter your old password: ")
            if Functions.encrypt(old_password) == current_user[2]:
                if DBFunctions.update_password():
                    break
            else:
                print("Password does not match\n")
                Functions.log_activity(current_user[1], "Failed to Update Password",
                                       f"Given password: {old_password} does not match old password", "Yes")
        check_access_level()


class SystemAdmin:
    @staticmethod
    def show_menu():
        count = 0
        for row in logData:
            if row["Read"] == "False" and Functions.decrypt(row["Suspicious"]) == "Yes":
                count += 1

        alert = ""
        if count == 1:
            alert = f"ALERT: {count} Suspicious unread activity"
        if count > 1:
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

        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5', '6', '7']:
            option = input(choice_input)
        if option == '1':
            SystemAdmin.check_users()
        elif option == '2':
            SystemAdmin.client_options()
        elif option == '3':
            SystemAdmin.adviser_options()
        elif option == '4':
            SystemAdmin.create_backup()
        elif option == '5':
            SystemAdmin.view_log_files()
        elif option == '6':
            SystemAdmin.update_password()
        elif option == '7':
            exit()

    @staticmethod
    def client_options():
        print("\n1. Define and add client\n"
              "2. Retrieve client information\n"
              "3. Modify a client's account\n"
              "4. Delete client\n"
              "5. Return\n")
        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5']:
            option = input(choice_input)
        if option == '1':
            Adviser.add_client()
        elif option == '2':
            Adviser.retrieve_client_info()
        elif option == '3':
            Adviser.modify_client()
        elif option == '4':
            SystemAdmin.delete_client()
        elif option == '5':
            check_access_level()

    @staticmethod
    def adviser_options():
        print("\n1. Define and add adviser\n"
              "2. Modify an adviser's account\n"
              "3. Delete adviser\n"
              "4. Reset adviser's password\n"
              "5. Return\n")
        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5']:
            option = input(choice_input)
        if option == '1':
            SystemAdmin.add_adviser()
        elif option == '2':
            SystemAdmin.modify_adviser()
        elif option == '3':
            SystemAdmin.delete_adviser()
        elif option == '4':
            SystemAdmin.reset_adviser_password()
        elif option == '5':
            check_access_level()

    @staticmethod
    def check_users():
        all_accounts = DBFunctions.get_all_accounts()
        print("-------------------------------------\n"
              "|Username           -           Role|\n"
              "-------------------------------------\n")
        for row in all_accounts:
            print(
                f"{Functions.decrypt(row[1])}           -           {row[6]}\n")
        print("-------------------------------------\n")
        Functions.log_activity(current_user[1], "Checked users", "", "No")
        return_to_menu()

    @staticmethod
    def add_adviser():
        while True:
            if DBFunctions.add_account("Adviser"):
                break
        check_access_level()

    @staticmethod
    def modify_adviser():
        while True:
            username = input(
                "\nEnter the username of the adviser whose account you want to modify: ")
            if DBFunctions.modify_account(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def delete_adviser():
        while True:
            username = input(
                "\nEnter the username of the adviser that you want to delete: ")
            if DBFunctions.delete_account(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def reset_adviser_password():
        while True:
            username = input(
                "\nEnter the username of the adviser whose password you want to reset: ")
            if DBFunctions.reset_password(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def delete_client():
        while True:
            email = input(
                "\nEnter the email of the client that you want to delete: ")
            phone_number = "+31-6-" + \
                input(
                    "Enter the phone number of the client that you want to delete: +31-6-")
            if DBFunctions.delete_client(email, phone_number):
                break
        check_access_level()

    @staticmethod
    def create_backup():
        list_files = ['CDMS.db', logfile]
        with zipfile.ZipFile('Backups.zip', 'w') as zipFile:
            for file in list_files:
                zipFile.write(file)
        print("\nSuccessfully made a backup\n")
        Functions.log_activity(
            current_user[1], "Successfully made a backup", "", "No")
        check_access_level()

    @staticmethod
    def view_log_files():
        print("-----------------------------------\n"
              "|               MENU              |\n"
              "-----------------------------------\n"
              "1. View all logs\n"
              "2. View unread suspicious logs\n"
              "3. Return\n")
        option = input(choice_input)

        while option not in ['1', '2', '3']:
            option = input(choice_input)
        if option == '1':
            print(
                "Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
            for row in logData:
                print(row["Id"] + " | " +
                      Functions.decrypt(row["Username"]) + " | " +
                      Functions.decrypt(row["Date"]) + " | " +
                      Functions.decrypt(row["Time"]) + " | " +
                      Functions.decrypt(row["Activity"]) + " | " +
                      Functions.decrypt(row["Additional Information"]) + " | " +
                      Functions.decrypt(row["Suspicious"]) + "\n")
                with open(logfile, 'w') as logs:
                    row["Read"] = "True"
                    json.dump(logData, logs, indent=4)
            return_to_menu()
        elif option == '2':
            print(
                "Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
            for row in logData:
                if row["Read"] == "False" and Functions.decrypt(row["Suspicious"]) == "Yes":
                    print(row["Id"] + " | " +
                          Functions.decrypt(row["Username"]) + " | " +
                          Functions.decrypt(row["Date"]) + " | " +
                          Functions.decrypt(row["Time"]) + " | " +
                          Functions.decrypt(row["Activity"]) + " | " +
                          Functions.decrypt(row["Additional Information"]) + " | " +
                          Functions.decrypt(row["Suspicious"]) + "\n")
                with open(logfile, 'w') as logs:
                    row["Read"] = "True"
                    json.dump(logData, logs, indent=4)
            return_to_menu()
        elif option == '3':
            check_access_level()

    @staticmethod
    def update_password():
        while True:
            old_password = input("Enter your old password: ")
            if Functions.encrypt(old_password) == current_user[2]:
                if DBFunctions.update_password():
                    break
            else:
                print("Password does not match\n")
                Functions.log_activity(current_user[1], "Failed to Update Password",
                                       f"Given password: {old_password} does not match old password", "Yes")
        check_access_level()


class SuperAdmin:
    @staticmethod
    def show_menu():
        count = 0
        for row in logData:
            if row["Read"] == "False" and Functions.decrypt(row["Suspicious"]) == "Yes":
                count += 1

        alert = ""
        if count == 1:
            alert = f"ALERT: {count} Suspicious unread activity"
        if count > 1:
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

        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5', '6', '7']:
            option = input(choice_input)
        if option == '1':
            SystemAdmin.check_users()
        elif option == '2':
            SystemAdmin.client_options()
        elif option == '3':
            SystemAdmin.adviser_options()
        elif option == '4':
            SuperAdmin.admin_options()
        elif option == '5':
            SystemAdmin.create_backup()
        elif option == '6':
            SystemAdmin.view_log_files()
        elif option == '7':
            exit()

    @staticmethod
    def admin_options():
        print("\n1. Define and add admin\n"
              "2. Modify an admin's account\n"
              "3. Delete admin\n"
              "4. Reset admin's password\n"
              "5. Return\n")
        option = input(choice_input)
        while option not in ['1', '2', '3', '4', '5']:
            option = input(choice_input)
        if option == '1':
            SuperAdmin.add_admin()
        elif option == '2':
            SuperAdmin.modify_admin()
        elif option == '3':
            SuperAdmin.delete_admin()
        elif option == '4':
            SuperAdmin.reset_admin_password()
        elif option == '5':
            check_access_level()

    @staticmethod
    def add_admin():
        while True:
            if DBFunctions.add_account("SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def modify_admin():
        while True:
            username = input(
                "\nEnter the username of the admin whose account you want to modify: ")
            if DBFunctions.modify_account(username, "SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def delete_admin():
        while True:
            username = input(
                "\nEnter the username of the admin that you want to delete: ")
            if DBFunctions.delete_account(username, "SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def reset_admin_password():
        while True:
            username = input(
                "\nEnter the username of the admin whose password you want to reset: ")
            if DBFunctions.reset_password(username, "SystemAdmin"):
                break
        check_access_level()


class Functions:
    @staticmethod
    def encrypt(text):
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
    def decrypt(encrypted_text):
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
    def input_username(input_message, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"{input_message}: ")
            if Functions.check_username(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for username: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def input_password(input_message, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"{input_message}: ")
            if Functions.check_password(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for password: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def input_email(input_message, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"{input_message}: ")
            if Functions.check_email(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for email: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def input_zip_code(input_message, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"{input_message}: ")
            if Functions.check_zip_code(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for zip code: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def input_phone_number(input_message, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"{input_message}")
            if Functions.check_phone_number(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for phone number: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def input_string(input_type, input_event):
        attempts = 0
        while attempts <= 3:
            input_value = input(f"Enter a {input_type}: ")
            if Functions.check_string_input(input_value):
                return input_value
            else:
                attempts += 1
        print(max_failed_attempts)
        Functions.log_activity(current_user[1], f"Exceeded the maximum amount of attempts when {input_event}",
                               f"Last given input for {input_type}: {input_value}", "Yes")
        return_to_menu()

    @staticmethod
    def check_username(username):
        username_whitelist = list(
            string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_" + "'" + ".")
        for row in DBFunctions.get_all_accounts():
            if row[1] == Functions.encrypt(username):
                print("\nUsername already exists!\n")
                return False
        if not username[0].isupper() and not username.islower():
            print("\nUsername must start with a letter.\n")
            return False
        if len(username) < 5 or len(username) > 20:
            print("\nUsername must have a length of at least 5 characters and must be no longer than 20 characters.\n")
            return False
        for i in username:
            if i not in username_whitelist:
                print("\nUsername contains invalid characters.\n")
                return False
        return True

    @staticmethod
    def check_password(password):
        if len(password) < 8 or len(password) > 30:
            print("\nPassword must have a length of at least 8 characters and must be no longer than 30 characters.\n")
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
            print("\nPassword must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.\n")
            return False
        return True

    @staticmethod
    def check_phone_number(phone_number):
        if len(phone_number) != 8:
            print("\nPhone number is out of range.\n")
            return False
        try:
            int(phone_number)
            return True
        except ValueError:
            print("\nPhone number is not an integer. It's a string\n")
            return False

    @staticmethod
    def check_email(email):
        if len(email) > 50:
            print("\nEmail must not be longer than 50 characters.\n")
            return False
        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            print("\nEmail is invalid\n")
            return False
        return True

    @staticmethod
    def check_zip_code(zip_code):
        if not re.match("(^[0-9]{4}[A-Z]{2}$)", zip_code):
            print("\nZip code is invalid\nCorrect format: 1234AB")
            return False
        return True

    @staticmethod
    def check_string_input(input_list):
        input_whitelist = list(string.ascii_lowercase + string.ascii_uppercase +
                               string.digits + "-" + "_" + "'" + "." + "@" + "!" + "+" + " ")
        for input in input_list:
            if len(input) > 50:
                print("\nInput must not be longer than 50 characters.\n")
                return False
            for i in input:
                if i not in input_whitelist:
                    print("\nInput contains invalid characters.\n")
                    return False
            return True

    @staticmethod
    def log_activity(username, activity, information, sus):
        date_time_current = datetime.now()

        count = str(len(logData) + 1)

        date = str(date_time_current.day) + "-" + \
            str(date_time_current.month) + "-" + str(date_time_current.year)
        time = str(date_time_current.hour) + ":" + \
            str(date_time_current.minute) + ":" + str(date_time_current.second)

        with open(logfile, 'r+') as logs:
            logData.append({
                "Id": count,
                "Username": username,
                "Date": Functions.encrypt(date),
                "Time": Functions.encrypt(time),
                "Activity": Functions.encrypt(activity),
                "Additional Information": Functions.encrypt(information),
                "Suspicious": Functions.encrypt(sus),
                "Read": "False"
            })
            logs.seek(0)
            json.dump(logData, logs, indent=4)
            logs.truncate()


class DBFunctions:
    @staticmethod
    def get_all_accounts():
        cur.execute("SELECT * FROM Accounts")
        return cur.fetchall()

    @staticmethod
    def get_all_clients():
        cur.execute("SELECT * FROM Clients")
        return cur.fetchall()

    @staticmethod
    def get_clients_by_name(name):
        cur.execute("SELECT * FROM Clients WHERE FullName LIKE ?;",
                    ('%'+Functions.encrypt(name)+'%',))
        return cur.fetchall()

    @staticmethod
    def add_account(account_type):
        print(f"\nCreate an account for a new {account_type}.\n")
        username = Functions.input_username(
            "Enter a username", "adding an account")
        password = Functions.input_password(
            "Enter a password", "adding an account")
        first_name = Functions.input_string("first name", "adding an account")
        last_name = Functions.input_string("last name", "adding an account")
        registration_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if Functions.check_username(username) and Functions.check_password(password) and Functions.check_string_input([first_name, last_name]):
            cur.execute(
                "INSERT INTO Accounts (Username, Password, FirstName, LastName, RegistrationDate, Type) VALUES (?, ?, ?, ?, ?, ?);",
                (
                    Functions.encrypt(username), Functions.encrypt(
                        password), Functions.encrypt(first_name), Functions.encrypt(last_name),
                    registration_date,
                    account_type))
            con.commit()
            print(f"\n{account_type} has been added!\n")
            Functions.log_activity(
                current_user[1], f"Added {account_type}", "", "No")
            return True

    @staticmethod
    def add_client():
        full_name = Functions.input_string("full name", "adding a client")
        street_name = Functions.input_string("street name", "adding a client")
        house_number = Functions.input_string(
            "house number", "adding a client")
        zip_code = Functions.input_zip_code(
            "Enter a zip code", "adding a client")
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
        email_address = Functions.input_email(
            "Enter an email address", "adding a client")
        phone_number = Functions.input_phone_number(
            "Enter a phone number: +31-6-", "adding a client")
        if Functions.check_string_input([full_name, street_name, house_number, zip_code, email_address]) and Functions.check_phone_number(
                phone_number):
            cur.execute(
                "INSERT INTO Clients (FullName, StreetName, HouseNumber, ZipCode, City, EmailAddress, PhoneNumber) VALUES (?,?,?,?,?,?,?);",
                (Functions.encrypt(full_name), Functions.encrypt(street_name), Functions.encrypt(house_number), Functions.encrypt(zip_code),
                 Functions.encrypt(city), Functions.encrypt(email_address), Functions.encrypt('+31-6-' + phone_number)))
            con.commit()
            Functions.log_activity(current_user[1], "Added Client", "", "No")
            return True

    @staticmethod
    def modify_account(old_username, account_type):
        for row in DBFunctions.get_all_accounts():
            if row[1] == Functions.encrypt(old_username.lower()) and row[6] == account_type:
                username = Functions.input_username(
                    "Enter a username", "modifying an account").lower()
                password = Functions.input_password(
                    "Enter a password", "modifying an account")
                first_name = Functions.input_string(
                    "first name", "modifying an account")
                last_name = Functions.input_string(
                    "last name", "modifying an account")
                if Functions.check_username(username) and Functions.check_password(password) and Functions.check_string_input(
                        [first_name, last_name]):
                    cur.execute(
                        "UPDATE Accounts SET Username = ?, Password = ?, FirstName = ?, LastName = ? WHERE Username = ?;", (
                            Functions.encrypt(username), Functions.encrypt(
                                password), Functions.encrypt(first_name), Functions.encrypt(last_name),
                            Functions.encrypt(old_username)))
                    con.commit()
                    print(f"\n{account_type}'s account has been modified\n")
                    Functions.log_activity(
                        current_user[1], f"Modified {account_type}", "", "No")
                    return True

    @staticmethod
    def modify_client(old_email, old_phone_number):
        for row in DBFunctions.get_all_clients():
            if row[6] == Functions.encrypt(old_email) and row[7] == Functions.encrypt(old_phone_number):
                full_name = Functions.input_string(
                    "full name", "modifying a client")
                street_name = Functions.input_string(
                    "street name", "modifying a client")
                house_number = Functions.input_string(
                    "house number", "modifying a client")
                zip_code = Functions.input_zip_code(
                    "Enter a zip code", "modifying a client")
                city = ""
                print(
                    "-----------------------------------\n1. Rotterdam\n2. Amsterdam\n3. Den Haag\n4. Utrecht\n5. Eindhoven\n6. Tilburg\n7. "
                    "Groningen\n8.Almere\n9. Breda\n10. Nijmegen\n")
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
                email_address = Functions.input_email(
                    "Enter an email address", "modifying a client")
                phone_number = Functions.input_phone_number(
                    "Enter a phone number: +31-6-", "modifying a client")
                if Functions.check_string_input([full_name, street_name, house_number, zip_code, email_address]) and Functions.check_phone_number(
                        phone_number):
                    cur.execute(
                        "UPDATE Clients SET FullName = ?, StreetName = ?, HouseNumber = ?, ZipCode = ?, "
                        "City = ?, EmailAddress = ?, PhoneNumber = ? WHERE EmailAddress = ? AND PhoneNumber = ?;",
                        (Functions.encrypt(full_name), Functions.encrypt(street_name), Functions.encrypt(house_number), Functions.encrypt(zip_code),
                         Functions.encrypt(city), Functions.encrypt(
                             email_address), Functions.encrypt('+31-6-' + phone_number),
                         Functions.encrypt(old_email), Functions.encrypt(old_phone_number)))
                    con.commit()
                    print("Client has been modified!")
                    Functions.log_activity(
                        current_user[1], "Modified Client", "", "No")
                    return True
            else:
                Functions.log_activity(current_user[1], "Failed to modify Client",
                                       f"Input by current_user: old email address: {old_email}, old phone number: {old_phone_number}", "No")
                print(
                    "No client can be found with the given email address and/or phone number!\n")
                return False

    @staticmethod
    def delete_account(username, account_type):
        for row in DBFunctions.get_all_accounts():
            if row[1] == Functions.encrypt(username.lower()) and row[6] == account_type:
                cur.execute("DELETE FROM Accounts WHERE Username = ?;",
                            (Functions.encrypt(username.lower)))
                con.commit()
                print(f"\n{account_type}'s account has been deleted!\n")
                Functions.log_activity(
                    current_user[1], f"Deleted {account_type}", f"User {username} is deleted", "No")
                return True
        print(f"\nNo {account_type} can be found with the given username!\n")
        Functions.log_activity(current_user[1], f"Failed to delete {account_type}",
                               f"User not found with data: username={username}, account_type={account_type}", "No")
        return False

    @staticmethod
    def delete_client(email, phone_number):
        for row in DBFunctions.get_all_clients():
            if row[6] == Functions.encrypt(email) and row[7] == Functions.encrypt(phone_number):
                cur.execute("DELETE FROM Clients WHERE EmailAddress = ? AND PhoneNumber = ?;",
                            (Functions.encrypt(email), Functions.encrypt(phone_number)))
                con.commit()
                print("\nClient has been deleted!\n")
                Functions.log_activity(
                    current_user[1], "Deleted Client", f"email:{email}, phone_number:{phone_number}", "No")
                return True
        print("\nNo client can be found with the given email and/or phone number!\n")
        Functions.log_activity(current_user[1], "Failed to delete client",
                               f"No client can be found with email={email} and phone number={phone_number}", "No")
        return False

    @staticmethod
    def update_password():
        new_password = Functions.input_password(
            "Enter your new password", "entering a new password")
        if Functions.check_password(new_password):
            cur.execute(
                "UPDATE Accounts SET Password = ? WHERE Username = ?;", (Functions.encrypt(new_password), Functions.encrypt(current_user[1])))
            con.commit()
            print("\nYour password has been changed!\n")
            Functions.log_activity(
                current_user[1], "Updated Password", "", "No")
            return True

    @staticmethod
    def reset_password(username, account_type):
        new_password = Functions.input_password(
            "Enter a new password", "resetting a password")
        for row in DBFunctions.get_all_accounts():
            if row[1] == Functions.encrypt(username.lower()) and row[6] == account_type:
                cur.execute(
                    "UPDATE Accounts SET Password = ? WHERE Username = ?;", (Functions.encrypt(new_password), Functions.encrypt(username)))
                con.commit()
                print(f"\n{account_type}'s password has been changed!\n")
                Functions.log_activity(current_user[1], "Reset password",
                                       f"Reset the password of {username} with account type {account_type} to {new_password}", "No")
                return True
        print(f"No {account_type.lower()} can be found with the given username!")
        Functions.log_activity(current_user[1], f"Failed to reset password",
                               f"User not found with data: username={username}, account_type={account_type}", "No")
        return False


print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
sign_in()
