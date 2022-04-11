import Users

userList = []
run = 1
loggedIn = False
userId = -1

def addUser():
    username = input("Your name: ")
    password = input("Your password: ")
    email = input("Your email: ")
    name = input("Your name: ")
    userList.append(Users.Users(username, password, email, name))
    print("User " + username + " added.")
    global run
    run = 1

def login():
    username = input("Username: ")
    password = input("Password: ")

    for i in range(len(userList)):
        if (userList[i].getUsername() == username and userList[i].getPassword() == password):
            print("You are logged in. Welcome " + userList[i].getName())
            global loggedIn
            loggedIn = True
            global userId
            userId = i
            break
        else:
            print("User not found.")
            global run
            run = 1

def printUserData():
    print("Name: " + userList[userId].getName())
    print ("Email: " + userList[userId].getEmail())
    print ("Username: " + userList[userId].getUsername())
    print ("Password: *********")
    run = 1
    return run

def logOut():
    global loggedIn
    loggedIn = False
    global userId
    userId = -1
    global run
    run = 1
    return run

def printUsers():
    for i in range(len(userList)):
        print(userList[i].getUsername())

while (run == 1):
    if (loggedIn == False):
        userInput = input("[L]ogin. [A]dd user. E[x]it. [P]rint ").lower()
        if (userInput == "a"):
            addUser()
        elif (userInput == "l"):
            login()
        elif (userInput =="p"):
            printUsers()
        elif (userInput == "x"):
            run = -1
        else:
            print ("Wrong input.")
    elif (loggedIn == True):
        print("Ayoo logged in")
        userInput = input("Type something. [P]rint. E[x]it. [L]ogout.")
        if (userInput == "l"):
            logOut()
        elif (userInput == "x"):
            exit()
        elif (userInput == "p"):
            printUserData()
        


