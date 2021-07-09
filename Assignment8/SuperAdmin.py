import SystemAdmin


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
        AdminOptions()
    elif option == '5':
        SystemAdmin.CreateBackup()
    elif option == '6':
        SystemAdmin.ViewLogFiles()
    elif option == '7':
        exit()


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
        AddAdmin()
    elif option == '2':
        ModifyAdmin()
    elif option == '3':
        DeleteAdmin()
    elif option == '4':
        ResetAdminPassword()
    elif option == '5':
        ShowMenu()


def AddAdmin():
    return


def ModifyAdmin():
    return


def DeleteAdmin():
    return


def ResetAdminPassword():
    return

#         Adviser
#         "2. Define and add adviser\n"
#         "3. Modify an adviser's account\n"
#         "4. Delete adviser\n"
#         "5. Reset adviser's password\n"
#
#
#         Admin
#         "6. Define and add admin\n"
#         "7. Modify an admin's account\n"
#         "8. Delete admin\n"
#         "9. Reset admin's password\n"
#
#
#         Client
#         "10. Add Client\n"
#         "11. Retrieve client information\n"
#         "12. Modify client information\n"
#         "13. Delete client\n"
