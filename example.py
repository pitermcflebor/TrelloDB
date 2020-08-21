from trello import Trello
import json, datetime
from os import system

client = Trello("YOUR_API_KEY", "YOUR_TOKEN_HERE").getMe()
db = client.getBoardByName('test')
usersColumn = db.getListByName('users')
if usersColumn == None:
    usersColumn = db.createList('users')

def register():
    print('Leave blank to cancel')
    print('')
    username = input('Your username: ')
    if username == '':
        start()
    else:
        user = usersColumn.getCardByName(username)
        if user == None:
            password = input('Your password: ')
            if password == '':
                start()
            else:
                usersColumn.createCard(username, json.dumps({'username':username, 'password':password, 'epoch':str(datetime.datetime.now()) }))
                start()
        else:
            print('That username already exists!')
            register()

def login():
    print('Leave blank to cancel')
    print('')
    username = input('Your username: ')
    if username == '':
        start()
    else:
        user = usersColumn.getCardByName(username)
        userData = json.loads(user.desc)
        if user == None:
            print('Account with that username doesn\'t exists')
            login()
        else:
            password = input('Your password: ')
            if password == '':
                start()
            elif password == userData['password']:
                print('Logged in!')
                print(f'Your registration date was {userData["epoch"]}')
            else:
                print('Password doesn\'t match!')
                login()


def start():
    system('cls')
    print('1 - Register account')
    print('2 - Login account')
    option = input('Select your option: ')
    if option == '1':
        register()
    elif option == '2':
        login()
    else:
        start()

if __name__ == "__main__":
    start()