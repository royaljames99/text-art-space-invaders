import json, os, time, hashlib

########LOGIN HANDLER########

def login():
    username = None
    highscore = None
    valid = False
    while not valid:
        os.system("cls")
        print("WELCOME")
        try:
            yNAccount = str(input("DO YOU HAVE AN ACCOUNT YET (Y/N): ")).upper()
        except:
            print("THAT WASN'T A VALID INPUT, PLEASE TRY AGAIN")
            time.sleep(2)
        else:
            if yNAccount not in ["Y","N"]:
                print("THAT WASN'T ONE OF THE OPTIONS, PLEASE REPLY EITHER Y OR N")
                time.sleep(2)
            else:
                if yNAccount.upper() == "N":
                    username, highscore = signUp()
                else:
                    username, highscore = signIn()

        if username != None and highscore != None: #CHECK IF <RETURN>  WAS NOT ENTERED  
            valid = True

    return username, highscore



def signUp():

    valid_characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
    ";",":",",",".","'","!","£","$","%","^","&","?","<",">","@","~","-","_"," ","`","¬","0","1","2","3","4","5","6","7","8","9"]

    loggedIn = False
    while not loggedIn:

        #GET USERNAME
        valid = False
        while not valid:
            valid = True
            os.system("cls")
            try:
                username = str(input("ENTER NEW USERNAME (TYPE   <RETURN>  TO CANCEL): "))
            except:
                print("THAT WASN'T A VALID INPUT, PLEASE TRY AGAIN")
                valid = False
                time.sleep(2)
            else:
                for char in username:
                    if char not in valid_characters:
                        print("INVALID CHARATER USED, PLEASE TRY AGAIN")
                        time.sleep(2)
                        valid = False
            if valid:
                if username.upper() == "RETURN" or username.upper() == "<RETURN>":
                    return None, None
                else:
                    with open("Logins.json", "r") as file:
                        data = json.load(file)
                    for user in data["logins"]:
                        if user["Username"] == username:
                            print("USERNAME ALREADY IN USE")  
                            time.sleep(2)
                            valid = False 
                            break
        
        #GET PASSWORD
        valid = False
        while not valid:
            os.system("cls")
            try:
                password = str(input("ENTER NEW PASSWORD (TYPE   <RETURN>  TO CANCEL): "))
            except:
                print("THAT WASN'T A VALID INPUT, PLEASE TRY AGAIN")
                time.sleep(2)
            else:
                for char in password:
                    if char not in valid_characters:
                        print("INVALID CHARACTER USED, PLEASE TRY AGAIN")
                        time.sleep(2)
                if password.upper() == "RETURN" or password.upper() == "<RETURN>":
                    return None, None
                else:
                    valid = True
        
        with open("Logins.json", "r") as file:
            data = json.load(file)
        
        encPassword = hashlib.sha512()
        password = bytes(password, "ascii")
        encPassword.update(password)
        encPassword = str(encPassword.digest())


        data["logins"].append({"Username":username, "Password":encPassword, "Highscore":0})

        with open("Logins.json", "w") as file:
            json.dump(data, file, indent = 4)
        
        loggedIn = True

    return username, 0


def signIn():

    valid_characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
    ";",":",",",".","'","!","£","$","%","^","&","?","<",">","@","~","-","_"," ","`","¬","0","1","2","3","4","5","6","7","8","9"]

    loggedIn = False
    while not loggedIn:

        #GET USERNAME
        valid = False
        while not valid:
            valid = True
            os.system("cls")
            try:
                username = str(input("ENTER USERNAME (TYPE   <RETURN>  TO CANCEL): "))
            except:
                print("THAT WASN'T A VALID INPUT, PLEASE TRY AGAIN")
                valid = False
                time.sleep(2)
            else:
                for char in username:
                    if char not in valid_characters:
                        print("INVALID CHARATER USED, PLEASE TRY AGAIN")
                        time.sleep(2)
                        valid = False
            if valid:
                if username.upper() == "RETURN" or username.upper() == "<RETURN>":
                    return None, None
                else:
                    pass

        #GET PASSWORD
        valid = False
        while not valid:
            valid = True
            os.system("cls")
            try:
                password = str(input("ENTER PASSWORD (TYPE   <RETURN>  TO CANCEL): "))
            except:
                print("THAT WASN'T A VALID INPUT, PLEASE TRY AGAIN")
                valid = False
                time.sleep(2)
            else:
                for char in password:
                    if char not in valid_characters:
                        print("INVALID CHARACTER USED, PLEASE TRY AGAIN")
                        time.sleep(2)
                        valid = False
            if valid:
                if password.upper() == "RETURN" or password.upper() == "<RETURN>":
                    return None, None
                else:
                    pass
        
        with open("Logins.json", "r") as file:
            data = json.load(file)
        

        encPassword = hashlib.sha512()
        password = bytes(password, "ascii")
        encPassword.update(password)
        encPassword = str(encPassword.digest())


        for login in data["logins"]:
            if login["Username"] == username and login["Password"] == encPassword:
                print("LOGIN SUCESSFUL")
                time.sleep(2)
                return username, login["Highscore"]
        
        print("USERNAME OR PASSWORD INCORRECT")
        time.sleep(2)
