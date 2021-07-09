#--start section (Encryption and Decryption of the input)
def encrypt(plain_text, key):
    encrypted = ""
    for c in plain_text:
        if c.isupper():
            c_index = ord(c) - ord('A')
            c_shifted = (c_index + key) % 26 + ord('A')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.islower():
            c_index = ord(c) - ord('a')
            c_shifted = (c_index + key) % 26 + ord('a')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.isdigit():
            c_new = (int(c) + key) % 10
            encrypted += str(c_new)
        else:
            encrypted += c
    return encrypted

def decrypt(ciphertext, key):
    decrypted = ""
    for c in ciphertext:
        if c.isupper():
            c_index = ord(c) - ord('A')
            c_og_pos = (c_index - key) % 26 + ord('A')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.islower():
            c_index = ord(c) - ord('a')
            c_og_pos = (c_index - key) % 26 + ord('a')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.isdigit():
            c_og = (int(c) - key) % 10
            decrypted += str(c_og)
        else:
            decrypted += c
    return decrypted
#--end section

#--start section (Checking username and password criteria when creating a new user)
def CheckUsername(username):
    usernameWhitelist = ["-","_","'","."]
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
#--end section