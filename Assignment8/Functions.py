import json
import string
from datetime import datetime

logfile = 'log.json'
with open(logfile, 'r') as logs:
    logData = json.load(logs)


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


def check_username(username):
    import DBFunctions
    username_whitelist = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_" + "'" + ".")
    for row in DBFunctions.get_all_accounts():
        if row[1] == encrypt(username):
            print("Username already exists!\n")
            return False
    if not username[0].isupper() and not username.islower():
        print("Username must start with a letter.\n")
        return False
    if len(username) < 5 or len(username) > 20:
        print("Username must have a length of at least 5 characters and must be no longer than 20 characters.\n")
        return False
    for i in username:
        if i not in username_whitelist:
            print("Username contains invalid characters.\n")
            return False
    return True


def check_password(password):
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


def check_phone_number(phone_number):
    if len(phone_number) != 8:
        print('Phone number is out of range.\n')
        return False
    try:
        int(phone_number)
        return True
    except ValueError:
        print("Phone number is not an integer. It's a string\n")
        return False


def check_string_input(input_list):
    input_whitelist = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "-" + "_" + "'" + "." + "@" + "!" + "+" + " ")
    for input in input_list:
        if len(input) > 40:
            print("Input must not be longer than 40 characters.\n")
            return False
        for i in input:
            if i not in input_whitelist:
                print("Input contains invalid characters.\n")
                return False
        return True


def log_activity(username, activity, information, sus):
    date_time_current = datetime.now()

    count = str(len(logData) + 1)

    date = str(date_time_current.day) + "-" + str(date_time_current.month) + "-" + str(date_time_current.year)
    time = str(date_time_current.hour) + ":" + str(date_time_current.minute) + ":" + str(date_time_current.second)

    with open(logfile, 'r+') as logs:
        logData.append({
            "Id": count,
            "Username": username,
            "Date": encrypt(date),
            "Time": encrypt(time),
            "Activity": encrypt(activity),
            "Additional Information": encrypt(information),
            "Suspicious": encrypt(sus),
            "Read": "False"
        })
        logs.seek(0)
        json.dump(logData, logs, indent=4)
        logs.truncate()
