import mysql.connector

connection = mysql.connector.connect(
    host='xxx.x.x.x',
    port= 0000,
    database = 'bank',
    user= 'root',
    password='xxxxxxxxxxxxx',
    autocommit= True
)

userData = []
action = ""
primaryActions= ["Log In", "Create account", "Exit"]
secondaryActions= ["Saldo", "Depositar", "Sacar", "Transferir", "Exit"]
loggedIn = False


def primaryactionsprint():
    global action
    print("Choose on of the following actions: ")
    for action in primaryActions:
        print("- " +  action)
    action = input("Type: ")



def secondaryactionsprint():
    global action
    print(f"{userData[1]}, what would you like to do now?")
    for action in secondaryActions:
        print("- " +  action)
    action = input("Type: ")


def login():
    global loggedIn
    username = input("Please type username: ")
    password = input("Please type password: ")

    sql = f"SELECT * FROM users WHERE username = '{username}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    if cursor.rowcount == 0:
        print(f"Username is not registered, try again!")
        login()
    else:
        for row in result:
            if row[2] == password:
                print("Welcome " + username + "!")
                userData.append(row[0])
                userData.append(row[1])
                userData.append(row[2])
                loggedIn = True
            else:
                print("Wrong password, try again!")
                login()


def createaccount():
    username = input("Type username: ")
    password = input("Type password: ")

    usercreate = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    moneyadd = f"INSERT INTO money (amount) VALUE ({500})"
    cursor = connection.cursor()
    cursor.execute(usercreate)
    cursor.execute(moneyadd)

    print("User created successfully and 500 euros added to bank account!")



def cases():
    global action
    if action == "Log In":
        login()
    elif action == "Exit":
        print("Thank you for using Nordea Bank!")
    elif action == "Create account":
        createaccount()
    elif action == "Saldo":
        sql = f"SELECT amount FROM money, users WHERE users.ID= money.ID AND users.username = '{userData[1]}' AND users.password = '{userData[2]}' "
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(f"Your balance is {row[0]} euros")
    elif action == "Depositar":
        addedamount =  int(input("How much would like to deposit: "))
        sql = f"UPDATE money SET amount = amount + '{addedamount}' WHERE money.ID = '{userData[0]}'"
        cursor =connection.cursor()
        cursor.execute(sql)
        print("Dinero depositado con exito")

    elif action == "Sacar":
        withdraw = int(input("How much would like to withdraw: "))
        sql = f"UPDATE money SET amount = amount - '{withdraw}' WHERE money.ID = '{userData[0]}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        print("Dinero sacado con exito!")

    elif action == "Transferir":
         reciever = input("Please enter reciever's username: ")

         sql = f"SELECT ID, username FROM users WHERE username = '{reciever}'"
         cursor = connection.cursor()
         cursor.execute(sql)
         result = cursor.fetchall()

         for row in result:
             if row[1] == reciever:
                 print("User found!")
                 amount = int(input("How much would you like to transfer: "))
                 transferquery = f"UPDATE money SET amount = amount + '{amount}' WHERE ID = '{row[0]}'"
                 withdrawquery = f"UPDATE money SET amount = amount - '{amount}' WHERE ID = '{userData[0]}'"
                 cursor = connection.cursor()
                 cursor.execute(transferquery)
                 cursor.execute(withdrawquery)
                 print("Money transferred successfully")
             else:
                 print("User not found!")

    else:
        print("Error, try again!")



def start():
      print("Welcome to Nordea Bank!")
      while not loggedIn:
          primaryactionsprint()
          cases()
          if action == "Exit":
              break

      while loggedIn:
          secondaryactionsprint()
          cases()
          if action == "Exit":
              break



start()