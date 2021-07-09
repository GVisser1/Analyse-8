import sqlite3

import Adviser
import SuperAdmin
import SystemAdmin

global currentUser
con = sqlite3.connect('CDMS.db')
cur = con.cursor()

cur.execute("SELECT * FROM Accounts")
rows = cur.fetchall()


def SignIn():
    global currentUser
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    for row in rows:
        if username == row[1] and password == row[2]:
            print("Signed in successfully\n")
            currentUser = row
            CheckAccessLevel()
        else:
            print("Username and/or password is incorrect\n")
            currentUser = -1
            SignIn()


def CheckAccessLevel():
    if currentUser[3] == 'SuperAdmin':
        SuperAdmin.ShowMenu()
    elif currentUser[3] == 'SystemAdmin':
        SystemAdmin.ShowMenu()
    elif currentUser[3] == 'Adviser':
        Adviser.ShowMenu()


print("---------------------------------------------------\n"
      "|  Welcome to the Clients Data Management System  |\n"
      "---------------------------------------------------\n")
SignIn()

#
# Adviser
# System Admin
# Super Admin -> Hard coded - username: superadmin, password: Admin!23

# Username:
# must have a length of at least 5 characters
# must be no longer than 20 characters
# must be started with a letter
# can contain letters (a-z), numbers (0-9), dashes (-), underscores (_), apostrophes ('), and periods (.)
# no distinguish between lowercase or uppercase letters

# Password:
# must have a length of at least 8 characters
# must be no longer than 30 characters
# can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/
# must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character
