import sqlite3
import zipfile
import json
from secrets import compare_digest

global current_user
con = sqlite3.connect('CDMS.db')
cur = con.cursor()
logfile = 'log.json'
choice_input = 'Put in your choice: '

with open(logfile, 'r') as logs:
    logData = json.load(logs)


def sign_in():
    import Functions, DBFunctions
    global current_user
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    for row in DBFunctions.get_all_accounts():
        if username == Functions.decrypt(row[1]) and compare_digest(password, Functions.decrypt(row[2])):
            print("\nSigned in successfully\n")
            current_user = row
            Functions.log_activity(current_user[1], "Logged in", "", "No")
            check_access_level()
    print("\nUsername and/or password is incorrect\n")
    current_user = -1
    Functions.log_activity(Functions.encrypt(username), "Unsuccessful login",
                           f"Password {password} is tried in combination with Username: {username}", "Yes")
    sign_in()


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
        import DBFunctions
        while True:
            if DBFunctions.add_client():
                break
        print("\nClient has been added!\n")
        check_access_level()

    @staticmethod
    def retrieve_client_info():
        import Functions, DBFunctions
        full_name = input("\nEnter the full name of the client whose information you want to retrieve: ")
        print(f"-------------------------------------\n"
              f"Results for clients with the full name: {full_name}\n")
        count = 0
        for row in DBFunctions.get_all_clients():
            if row[1] == Functions.encrypt(full_name):
                count += 1
                print(f"Fullname: {Functions.decrypt(row[1])}\n"
                      f"Street & house number: {Functions.decrypt(row[2])}, {Functions.decrypt(row[3])}\n"
                      f"Zip code & city: {Functions.decrypt(row[4])}, {Functions.decrypt(row[5])}\n"
                      f"Email Address: {Functions.decrypt(row[6])}\n"
                      f"Phone Number: {Functions.decrypt(row[7])}\n"
                      f"\n-------------------------------------\n")
        if count == 0:
            print(f"No client has been found with the full name: {full_name}!\n")
        Functions.log_activity(current_user[1], "Retrieved Client info", "", "No")
        return_to_menu()

    @staticmethod
    def modify_client():
        import DBFunctions
        while True:
            old_email = input("\nEnter the email address of the client you want to modify: ")
            old_phone_number = "+31-6-" + input("Enter a phone number: +31-6-")
            if DBFunctions.modify_client(old_email, old_phone_number):
                break
        check_access_level()

    @staticmethod
    def update_password():
        import Functions, DBFunctions
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


class SystemAdmin:
    @staticmethod
    def show_menu():
        import Functions
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
        import DBFunctions
        import Functions
        all_accounts = DBFunctions.get_all_accounts()
        print("-------------------------------------\n"
              "|Username           -           Role|\n"
              "-------------------------------------\n")
        for row in all_accounts:
            print(f"{Functions.decrypt(row[1])}           -           {row[6]}\n")
        print("-------------------------------------\n")
        Functions.log_activity(current_user[1], "Checked users", "", "No")
        return_to_menu()

    @staticmethod
    def add_adviser():
        import DBFunctions
        while True:
            if DBFunctions.add_account("Adviser"):
                break
        check_access_level()

    @staticmethod
    def modify_adviser():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the adviser whose account you want to modify: ")
            if DBFunctions.modify_account(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def delete_adviser():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the adviser that you want to delete: ")
            if DBFunctions.delete_account(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def reset_adviser_password():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the adviser whose password you want to reset: ")
            if DBFunctions.reset_password(username, "Adviser"):
                break
        check_access_level()

    @staticmethod
    def delete_client():
        import DBFunctions
        while True:
            email = input("\nEnter the email of the client that you want to delete: ")
            phone_number = "+31-6-" + input("Enter the phone number of the client that you want to delete: +31-6-")
            if DBFunctions.delete_client(email, phone_number):
                break
        check_access_level()

    @staticmethod
    def create_backup():
        import Functions
        list_files = ['CDMS.db', logfile]
        with zipfile.ZipFile('Backups.zip', 'w') as zipFile:
            for file in list_files:
                zipFile.write(file)
        print("\nSuccessfully made a backup\n")
        Functions.log_activity(current_user[1], "Successfully made a backup", "", "No")
        check_access_level()

    @staticmethod
    def view_log_files():
        import Functions
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
            print("Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
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
            print("Id | Username | Date | Time | Activity | Additional Information | Suspicious\n")
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
        import DBFunctions
        import Functions
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
        import Functions
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
        import DBFunctions
        while True:
            if DBFunctions.add_account("SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def modify_admin():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the admin whose account you want to modify: ")
            if DBFunctions.modify_account(username, "SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def delete_admin():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the admin that you want to delete: ")
            if DBFunctions.delete_account(username, "SystemAdmin"):
                break
        check_access_level()

    @staticmethod
    def reset_admin_password():
        import DBFunctions
        while True:
            username = input("\nEnter the username of the admin whose password you want to reset: ")
            if DBFunctions.reset_password(username, "SystemAdmin"):
                break
        check_access_level()


print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
sign_in()
