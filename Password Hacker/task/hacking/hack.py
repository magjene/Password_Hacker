"""
Project: Password Hacker
Stage 5/5: Time-based vulnerability


Description
Your program has successfully hacked the new system! However, you've been spotted: the admin noticed your first failed attempts, found the vulnerability and made a patch. You should overcome this patch and hack the system again. It’s not easy being a hacker!

The admin has improved the server: the program now catches the exception and sends a simple ‘wrong password’ message to the client even when the real password starts with current symbols.

But here's the thing: the admin probably just caught this exception. We know that catching an exception takes the computer a long time, so there should be a delay in the server response when this exception takes place. You can use it to hack the system: count the time period in which the response comes and find out which starting symbols work out for the password.

Objectives
In this stage, you should write a program that uses the time vulnerability to find the password.

Use the list of logins from the previous stage.
Output the result as you did this in the previous stage.
Examples
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Example 1:

> python hack.py localhost 9090
{
    "login" : "su",
    "password" : "fTUe3O99Rre"
}
Example 2:

> python hack.py localhost 9090
{"login": "admin3", "password": "mlqDz33x"}
"""


import json
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


with open(r'.\hacking\logins.txt', 'r') as file:
    logins_list = file.read().split()

host_name, port = sys.argv[1:]
with socket.socket() as client_socket:
    client_socket.connect((host_name, int(port)))

    wrong_login = json.dumps({"result": "Wrong login!"})
    wrong_password = json.dumps({"result": "Wrong password!"})
    exception_happened = json.dumps({"result": "Exception happened during login"})
    connection_success = json.dumps({"result": "Connection success!"})
    login = ''
    password = ''
    for word in logins_list:
        json_send = json.dumps({"login": word.rstrip(), "password": " "})
        client_socket.send(json_send.encode())
        response = client_socket.recv(1024).decode()
        if response != wrong_login:
            login = word.rstrip()
            break
    while True:
        for l in letters:
            json_send = json.dumps({"login": login, "password": password + l})
            client_socket.send(json_send.encode())
            response = client_socket.recv(1024).decode()
            if response == exception_happened:
                password += l
            elif response == connection_success:
                password += l
                print(json.dumps({"login": login, "password": password}))
                exit()

# """
# you might catch both exceptions like
#
# try:
#     send
#     receive
# except (Exc1, Exc2) as e:
#     pass
#
# but it is really not needed if everything is correct
#
# ***************************************
#
# I am sharing with a server that I created to test my solution - problem with the jetbrains check is that
# it does not take too kindly to my debugging statements - I can control the server, and put
# printf the userid / password to see what is going wrong ...hope this helps
#
#
#
#
# import socket
# import random
# import json
#
# abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#
#
# logins_list = [
#     'admin', 'Admin', 'admin1', 'admin2', 'admin3',
#     'user1', 'user2', 'root', 'default', 'new_user',
#     'some_user', 'new_admin', 'administrator',
#     'Administrator', 'superuser', 'super', 'su', 'alex',
#     'suser', 'rootuser', 'adminadmin', 'useruser',
#     'superadmin', 'username', 'username1'
# ]
#
#
# def logins():
#     for login in logins_list:
#         yield login
#
# def random_login():
#     return random.choice(list(logins()))
#
# def random_password():
#     '''function - generating random password of length from 6 to 10'''
#     return ''.join(random.choice(abc) for i in range(random.randint(6, 10)))
#
#
# def server(server_login, server_password):
#     HOST = '127.0.0.1'
#     PORT = 9090
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         try:
#             s.listen(1)
#             print("waiting for new connection")
#             conn, addr = s.accept()
#             print("connection established ")
#             with conn:
#                 while True:
#                     data = conn.recv(1024)
#
#                     try:
#                         login_ = json.loads(data.decode('utf8'))['login']
#                         password_ = json.loads(data.decode('utf8'))['password']
#                     except:
#                         conn.send(json.dumps({'result': 'Bad request!'}).encode('utf8'))
#                         continue
#
#                     if login_ == server_login:
#
#                         if server_password == password_:
#                             conn.send(
#                                 json.dumps({
#                                     'result': 'Connection success!'
#                                 }).encode('utf8'))
#                             break
#                         elif server_password.startswith(password_):
#                             conn.send(
#                                 json.dumps({
#                                     'result': 'Exception happened during login'
#                                 }).encode('utf8'))
#                         else:
#                             conn.send(
#                                 json.dumps({
#                                     'result': 'Wrong password!'
#                                 }).encode('utf8'))
#                     else:
#                         conn.send(json.dumps({'result': 'Wrong login!'}).encode('utf8'))
#         except:
#             pass
#
#
#
#
#
# server_login = random_login()
# print("server login is " + server_login)
# server_password = random_password()
# print("server password is " + server_password)
# while True:
#     server(server_login, server_password)
# """
