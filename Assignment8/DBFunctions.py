import sqlite3
from datetime import datetime

con = sqlite3.connect('CDMS.db')
cur = con.cursor()


def get_all_accounts():
    cur.execute("SELECT * FROM Accounts")
    return cur.fetchall()


def get_all_clients():
    cur.execute("SELECT * FROM Clients")
    return cur.fetchall()


def add_account(account_type):
    import Functions
    from CDMS import current_user
    print(f"\nCreate an account for a new {account_type}.\n")
    username = input("Enter a username: ").lower()
    password = input("Enter a password: ")
    first_name = input("Enter a first name: ")
    last_name = input("Enter a last name: ")
    registration_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if Functions.check_username(username) and Functions.check_password(password) and Functions.check_string_input([first_name, last_name]):
        cur.execute(
            "INSERT INTO Accounts (Username, Password, FirstName, LastName, RegistrationDate, Type) VALUES (?, ?, ?, ?, ?, ?);",
            (
                Functions.encrypt(username), Functions.encrypt(password), Functions.encrypt(first_name), Functions.encrypt(last_name),
                registration_date,
                account_type))
        con.commit()
        print(f"\n{account_type} has been added!\n")
        Functions.log_activity(current_user[1], f"Added {account_type}", "", "No")
        return True

    Functions.log_activity(current_user[1], f"Failed to add {account_type}",
                           f"Input by current_user: username={username}, password={password}, first name={first_name}, last name={last_name}", "Yes")
    return False


def add_client():
    import Functions
    from CDMS import current_user
    full_name = input("Enter a full name: ")
    street_name = input("Enter a street name: ")
    house_number = input("Enter a house number: ")
    zip_code = input("Enter a zip code: ")
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
    email_address = input("Enter a email address: ")
    phone_number = input("Enter a phone number: +31-6-")
    if Functions.check_string_input([full_name, street_name, house_number, zip_code, email_address]) and Functions.check_phone_number(phone_number):
        cur.execute(
            "INSERT INTO Clients (FullName, StreetName, HouseNumber, ZipCode, City, EmailAddress, PhoneNumber) VALUES (?,?,?,?,?,?,?);",
            (Functions.encrypt(full_name), Functions.encrypt(street_name), Functions.encrypt(house_number), Functions.encrypt(zip_code),
             Functions.encrypt(city), Functions.encrypt(email_address), Functions.encrypt('+31-6-' + phone_number)))
        con.commit()
        Functions.log_activity(current_user[1], "Added Client", "", "No")
        return True
    Functions.log_activity(current_user[1], "Failed to add Client",
                           f"Input by current_user: full name: {full_name}, street name & house number: {street_name} {house_number}, "
                           f"zip code: {zip_code}, email address: {email_address}, phone number: {phone_number}", "Yes")
    return False


def modify_account(old_username, account_type):
    import Functions
    from CDMS import current_user
    for row in get_all_accounts():
        if row[1] == Functions.encrypt(old_username.lower()) and row[6] == account_type:
            username = input("Enter a (new) username: ").lower()
            password = input("Enter a (new) password: ")
            first_name = input("Enter a (new) first name: ")
            last_name = input("Enter a (new) last name: ")
            if Functions.check_username(username) and Functions.check_password(password) and Functions.check_string_input([first_name, last_name]):
                cur.execute(
                    "UPDATE Accounts SET Username = ?, Password = ?, FirstName = ?, LastName = ? WHERE Username = ?;", (
                        Functions.encrypt(username), Functions.encrypt(password), Functions.encrypt(first_name), Functions.encrypt(last_name),
                        Functions.encrypt(old_username)))
                con.commit()
                print(f"\n{account_type}'s account has been modified\n")
                Functions.log_activity(current_user[1], f"Modified {account_type}", "", "No")
                return True
            Functions.log_activity(current_user[1], f"Failed to modify {account_type}",
                                   f"Input by current_user: username = {username}, password = {password}, "
                                   f"first name = {first_name}, last name = {last_name}", "Yes")
            return False
    Functions.log_activity(current_user[1], "Failed to modify account",
                           f"Input by current_user: old username= {old_username}", "Yes")
    print(f"No {account_type} can be found with the given username!\n")
    return False


def modify_client(old_email, old_phone_number):
    import Functions
    from CDMS import current_user
    for row in get_all_clients():
        if row[6] == Functions.encrypt(old_email) and row[7] == Functions.encrypt(old_phone_number):
            full_name = input("Enter a (new) full name: ")
            street_name = input("Enter a (new) street name: ")
            house_number = input("Enter a (new) house number: ")
            zip_code = input("Enter a (new) zip code: ")
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
            email_address = input("Enter a (new) email address: ")
            phone_number = input("Enter a (new) phone number: +31-6-")
            if Functions.check_string_input([full_name, street_name, house_number, zip_code, email_address]) and Functions.check_phone_number(
                    phone_number):
                cur.execute(
                    "UPDATE Clients SET FullName = ?, StreetName = ?, HouseNumber = ?, ZipCode = ?, "
                    "City = ?, EmailAddress = ?, PhoneNumber = ? WHERE EmailAddress = ? AND PhoneNumber = ?;",
                    (Functions.encrypt(full_name), Functions.encrypt(street_name), Functions.encrypt(house_number), Functions.encrypt(zip_code),
                     Functions.encrypt(city), Functions.encrypt(email_address), Functions.encrypt('+31-6-' + phone_number),
                     Functions.encrypt(old_email), Functions.encrypt(old_phone_number)))
                con.commit()
                print("Client has been modified!")
                Functions.log_activity(current_user[1], "Modified Client", "", "No")
                return True
            else:
                Functions.log_activity(current_user[1], "Failed to modify Client",
                                       f"Input by current_user: full name: {full_name}, street name & house number: {street_name} {house_number}, "
                                       f"zip code: {zip_code}, email address: {email_address}, phone number: {phone_number}", "Yes")
                return False
        else:
            Functions.log_activity(current_user[1], "Failed to modify Client",
                                   f"Input by current_user: old email address: {old_email}, old phone number: {old_phone_number}", "Yes")
            print("No client can be found with the given email address and/or phone number!\n")
            return False


def delete_account(username, account_type):
    import Functions
    from CDMS import current_user
    for row in get_all_accounts():
        if row[1] == Functions.encrypt(username.lower()) and row[6] == account_type:
            cur.execute("DELETE FROM Accounts WHERE Username = ?;", (Functions.encrypt(username.lower)))
            con.commit()
            print(f"\n{account_type}'s account has been deleted!\n")
            Functions.log_activity(current_user[1], f"Deleted {account_type}", f"User {username} is deleted", "No")
            return True
    print(f"\nNo {account_type} can be found with the given username!\n")
    Functions.log_activity(current_user[1], f"Failed to delete {account_type}",
                           f"User not found with data: username={username}, account_type={account_type}", "Yes")
    return False


def delete_client(email, phone_number):
    import Functions
    from CDMS import current_user
    for row in get_all_clients():
        if row[6] == Functions.encrypt(email) and row[7] == Functions.encrypt(phone_number):
            cur.execute("DELETE FROM Clients WHERE EmailAddress = ? AND PhoneNumber = ?;",
                        (Functions.encrypt(email), Functions.encrypt(phone_number)))
            con.commit()
            print("\nClient has been deleted!\n")
            Functions.log_activity(current_user[1], "Deleted Client", f"email:{email}, phone_number:{phone_number}", "No")
            return True
    print("\nNo client can be found with the given email and/or phone number!\n")
    Functions.log_activity(current_user[1], "Failed to delete client",
                           f"No client can be found with email={email} and phone number={phone_number}", "Yes")
    return False


def update_password():
    import Functions
    from CDMS import current_user
    new_password = input("Enter your new password: ")
    if Functions.check_password(new_password):
        cur.execute(
            "UPDATE Accounts SET Password = ? WHERE Username = ?;", (Functions.encrypt(new_password), Functions.encrypt(current_user[1])))
        con.commit()
        print("\nYour password has been changed!\n")
        Functions.log_activity(current_user[1], "Updated Password", "", "No")
        return True
    else:
        Functions.log_activity(current_user[1], "Failed to Update Password", f"New password did not meet the criteria: {new_password}", "Yes")
        return False


def reset_password(username, account_type):
    import Functions
    from CDMS import current_user
    new_password = input("Enter a new password: ")
    if not Functions.check_password(new_password):
        Functions.log_activity(current_user[1], f"Failed to reset password",
                               f"User not found with data: username={username}, account_type={account_type}", "Yes")
        return False
    for row in get_all_accounts():
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
                           f"User not found with data: username={username}, account_type={account_type}", "Yes")
    return False
