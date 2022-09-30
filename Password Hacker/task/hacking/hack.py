"""
Project: Password Hacker
Stage 4/5: Catching exception


Description
The server is becoming smarter along with your hacking program. Now the admin has implemented a security system by login and password. In order to access the site with admin privileges, you need to know the admin's login and password. Fortunately, we have a dictionary of different logins and a very interesting vulnerability. You need to improve your program once again to hack the new system.

Also, now the admin has made a complex password that is guaranteed to be absent in the databases since it's randomly generated from several characters.

The server now uses JSON to send messages.

First of all, you should adjust your program so that it can send the combination of login and password in JSON format to the server. Your request should now look like this:

{
    "login": "admin",
    "password": "12345678"
}
In case of the wrong login, the response you receive looks like this:

{
    "result": "Wrong login!"
}
If you got the login right but failed to find the password, you get this:

{
    "result": "Wrong password!"
}
If some exception happens, you'll see this result:

{
    "result": "Exception happened during login"
}
When you finally succeed in finding both the login and the password, you'll see the following:

{
    "result": "Connection success!"
}
Use the dictionary of typical admin logins. Since you don’t know the login, you should try different variants from the dictionary the same way you did at the previous stage with the passwords.

Use an empty password while searching for the correct login. It matters because you will know that the login is correct the moment you get the ‘wrong password’ result instead of ‘wrong login’.
As for passwords, they’ve become yet harder, so a simple dictionary is no longer enough. Fortunately, a vulnerability has been found: the ‘exception’ message pops up when the symbols you tried for the password match the beginning of the correct one.

Objectives
Your algorithm is the following:

Try all logins with an empty password.
When you find the login, try out every possible password of length 1.
When an exception occurs, you know that you found the first letter of the password.
Use the found login and the found letter to find the second letter of the password.
Repeat until you receive the ‘success’ message.
Finally, your program should print the combination of login and password in JSON format. The examples show two ways of what the output can look like.

Examples
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Example 1:

> python hack.py localhost 9090
{
    "login" : "superuser",
    "password" : "aDgT9tq1PU0"
}
Example 2:

> python hack.py localhost 9090
{"login": "new_user", "password": "Sg967s"}
"""


import json
import itertools
import socket
import sys

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
           'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'A', 'B', 'C', 'D', 'E', 'F', 'G',
           'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']

host_name, port = sys.argv[1:]
with socket.socket() as client_socket:
    client_socket.connect((host_name, int(port)))

    wrong_login = json.dumps({"result": "Wrong login!"}, indent=4)
    wrong_password = json.dumps({"result": "Wrong password!"}, indent=4)
    exception_happened = json.dumps({"result": "Exception happened during login"})
    connection_success = json.dumps({"result": "Connection success!"})
    login = ''
    password = ''

    for word in open(r'.\hacking\passwords.txt', 'r'):
        json_send = json.dumps({"login": word.rstrip(), "password": " "}, indent=4)

        client_socket.send(json_send.encode())
        response = client_socket.recv(1024).decode()
        if not response == wrong_login:
            login = word.rstrip()
            break
    c = 260
    while c:
        c -= 1
        for l in letters:
            json_send = json.dumps({"login": login, "password": password + l}, indent=4)

            client_socket.send(json_send.encode())
            response = client_socket.recv(1024).decode()
            if response == exception_happened:
                password += l
            elif response == connection_success:
                print(json.dumps({"login": login, "password": password}))
                exit()

"""
I am sharing with a server that I created to test my solution - problem with the jetbrains check is that 
it does not take too kindly to my debugging statements - I can control the server, and put 
printf the userid / password to see what is going wrong ...hope this helps 




import socket
import random
import json

abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]


def logins():
    for login in logins_list:
        yield login

def random_login():
    return random.choice(list(logins()))

def random_password():
    '''function - generating random password of length from 6 to 10'''
    return ''.join(random.choice(abc) for i in range(random.randint(6, 10)))


def server(server_login, server_password):
    HOST = '127.0.0.1'
    PORT = 9090
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        try:
            s.listen(1)
            print("waiting for new connection")
            conn, addr = s.accept()
            print("connection established ")
            with conn:
                while True:
                    data = conn.recv(1024)

                    try:
                        login_ = json.loads(data.decode('utf8'))['login']
                        password_ = json.loads(data.decode('utf8'))['password']
                    except:
                        conn.send(json.dumps({'result': 'Bad request!'}).encode('utf8'))
                        continue

                    if login_ == server_login:

                        if server_password == password_:
                            conn.send(
                                json.dumps({
                                    'result': 'Connection success!'
                                }).encode('utf8'))
                            break
                        elif server_password.startswith(password_):
                            conn.send(
                                json.dumps({
                                    'result': 'Exception happened during login'
                                }).encode('utf8'))
                        else:
                            conn.send(
                                json.dumps({
                                    'result': 'Wrong password!'
                                }).encode('utf8'))
                    else:
                        conn.send(json.dumps({'result': 'Wrong login!'}).encode('utf8'))
        except:
            pass





server_login = random_login()
print("server login is " + server_login)
server_password = random_password()
print("server password is " + server_password)
while True:
    server(server_login, server_password)
"""
